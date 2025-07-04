import logging
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone
import json

from ..domain.models.generation_request import GenerationRequest
from ..domain.models.generation_status import GenerationStatus
from ..domain.repositories.generation_request_repository import IGenerationRequestRepository
from ..infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from ..api.v1.schemas import (
    GenerationRequestCreate, N8NSampleResultPayload, N8NFinalResultPayload, N8NErrorPayload
)
from .credit_service_client import CreditServiceClient, InsufficientCreditsError
from .notification_service_client import NotificationServiceClient
from ...core.config import Settings

logger = logging.getLogger(__name__)

# --- Custom Exceptions for the Service Layer ---

class GenerationJobPublishError(Exception):
    def __init__(self, request_id, detail):
        self.request_id = request_id
        self.detail = detail
        super().__init__(f"Failed to publish job for request {request_id}: {detail}")

class InvalidGenerationStateError(Exception):
    def __init__(self, request_id, current_status, expected_status, detail):
        self.request_id = request_id
        self.current_status = current_status
        self.expected_status = expected_status
        self.detail = detail
        super().__init__(f"Invalid state for request {request_id}. Current: {current_status}, Expected: {expected_status}. Detail: {detail}")

class OrchestrationService:
    """
    Contains the core business logic for managing the AI generation pipeline.
    """
    def __init__(
        self,
        repo: IGenerationRequestRepository,
        rabbitmq_publisher: RabbitMQPublisher,
        credit_service_client: CreditServiceClient,
        notification_client: NotificationServiceClient,
        settings: Settings
    ):
        self._repo = repo
        self._rabbitmq_publisher = rabbitmq_publisher
        self._credit_service = credit_service_client
        self._notification_client = notification_client
        self._settings = settings

    async def initiate_generation(self, user_id: str, request_data: GenerationRequestCreate) -> GenerationRequest:
        logger.info(f"Initiating generation for user {user_id}, project {request_data.project_id}")
        
        # Determine credit cost for sample generation
        required_credits_sample = 0.25 # As per REQ-016, this could be dynamic
        
        await self._credit_service.check_credits(user_id, required_credits_sample)
        
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            # Store all input params in a JSONB field for later reference
            input_parameters=request_data.dict(),
            status=GenerationStatus.VALIDATING_CREDITS,
            credits_cost_sample=required_credits_sample
        )
        await self._repo.add(new_request)
        
        try:
            await self._credit_service.deduct_credits(user_id, new_request.id, required_credits_sample, "sample_generation")
        except Exception as e:
            logger.error(f"Credit deduction failed for request {new_request.id}. Rolling back.", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Credit deduction failed.")
            await self._repo.update(new_request)
            raise # Re-raise to be caught by API layer

        new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        await self._repo.update(new_request)

        job_payload = self._prepare_n8n_payload(new_request, "sample_generation")
        
        try:
            await self._rabbitmq_publisher.publish_generation_job(
                job_payload.dict(),
                routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE
            )
        except Exception as e:
            logger.error(f"Failed to publish RabbitMQ job for request {new_request.id}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to queue generation job.")
            await self._repo.update(new_request)
            # Attempt to refund credits
            await self._credit_service.refund_credits(user_id, new_request.id, required_credits_sample, "Job publishing failed")
            raise GenerationJobPublishError(new_request.id, str(e))

        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        
        logger.info(f"Successfully initiated generation request {new_request.id}")
        return new_request

    async def get_generation_status(self, request_id: UUID) -> Optional[GenerationRequest]:
        return await self._repo.get_by_id(request_id)

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultPayload):
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received sample callback for non-existent request ID: {callback_data.generation_request_id}")
            return
        
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        request.sample_asset_infos = [s.dict() for s in callback_data.samples]
        await self._repo.update(request)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )
        logger.info(f"Processed sample callback for request {request.id}")

    async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultPayload):
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received final asset callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.update_status(GenerationStatus.COMPLETED)
        request.final_asset_info = callback_data.final_asset.dict()
        await self._repo.update(request)

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": str(callback_data.final_asset.url)}
        )
        logger.info(f"Processed final asset callback for request {request.id}")

    async def handle_n8n_error(self, error_data: N8NErrorPayload):
        request = await self._repo.get_by_id(error_data.generation_request_id)
        if not request:
            logger.error(f"Received error callback for non-existent request ID: {error_data.generation_request_id}")
            return

        is_content_rejection = "content policy" in error_data.error_message.lower()
        new_status = GenerationStatus.CONTENT_REJECTED if is_content_rejection else GenerationStatus.FAILED
        
        request.update_status(new_status, error_message=error_data.error_message)
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            request.error_details = error_data.error_details
            logger.warning(f"Detailed error for request {request.id}: {error_data.error_details}")

        # REQ-007.1: Credit Refund Logic
        if self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE and not is_content_rejection:
            amount_to_refund = 0
            if error_data.failed_stage == "sample_processing" and request.credits_cost_sample:
                amount_to_refund = request.credits_cost_sample
            elif error_data.failed_stage == "final_processing" and request.credits_cost_final:
                amount_to_refund = request.credits_cost_final

            if amount_to_refund > 0:
                logger.info(f"Attempting to refund {amount_to_refund} credits for system failure on request {request.id}")
                await self._credit_service.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=amount_to_refund,
                    reason=f"System error during AI generation stage: {error_data.failed_stage}"
                )

        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            payload={"request_id": str(request.id)}
        )
        logger.warning(f"Processed error callback for request {request.id}. Status set to {new_status.value}")

    async def select_sample_and_initiate_final(self, request_id: UUID, selected_sample_id: str, user_id: str, desired_resolution: Optional[str]) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request or request.user_id != user_id:
            raise HTTPException(status_code=404, detail="Generation request not found or access denied.")
        
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidGenerationStateError(request.id, request.status, GenerationStatus.AWAITING_SELECTION, "Can only select a sample when request is awaiting selection.")
        
        if not any(s.get('asset_id') == selected_sample_id for s in (request.sample_asset_infos or [])):
            raise ValueError(f"Selected sample ID '{selected_sample_id}' not found in this request.")
        
        required_credits_final = 1.0 # As per REQ-016, could be dynamic based on resolution
        await self._credit_service.check_credits(user_id, required_credits_final)
        await self._credit_service.deduct_credits(user_id, request.id, required_credits_final, "final_generation")

        request.selected_sample_id = selected_sample_id
        request.credits_cost_final = required_credits_final
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        
        job_payload = self._prepare_n8n_payload(request, "final_generation", desired_resolution=desired_resolution)
        
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict(), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)
        
        await self._repo.update(request)
        logger.info(f"Initiated final generation for request {request.id} with sample {selected_sample_id}")
        return request

    async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request or request.user_id != user_id:
            raise HTTPException(status_code=404, detail="Generation request not found or access denied.")

        required_credits_regen = 0.25 # As per REQ-016
        await self._credit_service.check_credits(user_id, required_credits_regen)
        await self._credit_service.deduct_credits(user_id, request.id, required_credits_regen, "sample_regeneration")

        if updated_prompt: request.input_prompt = updated_prompt
        if updated_style_guidance: request.style_guidance = updated_style_guidance
        # Update credits cost (could be cumulative or just the latest)
        request.credits_cost_sample = (request.credits_cost_sample or 0) + required_credits_regen
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        
        job_payload = self._prepare_n8n_payload(request, "sample_regeneration")
        
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict(), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)
        
        await self._repo.update(request)
        logger.info(f"Initiated sample regeneration for request {request.id}")
        return request


    def _prepare_n8n_payload(self, request: GenerationRequest, job_type: str, **kwargs) -> GenerationJobParameters:
        """Helper to construct the JSON payload for n8n jobs."""
        from ..application.dtos import GenerationJobParameters, CustomDimensions

        base_url = str(self._settings.N8N_CALLBACK_BASE_URL)
        api_prefix = self._settings.API_V1_STR
        
        params = request.input_parameters or {}
        
        return GenerationJobParameters(
            generation_request_id=str(request.id),
            user_id=request.user_id,
            project_id=request.project_id,
            input_prompt=request.input_prompt,
            style_guidance=request.style_guidance,
            output_format=params.get("output_format"),
            custom_dimensions=CustomDimensions(**params["custom_dimensions"]) if params.get("custom_dimensions") else None,
            brand_kit_id=params.get("brand_kit_id"),
            uploaded_image_references=params.get("uploaded_image_references"),
            target_platform_hints=params.get("target_platform_hints"),
            emotional_tone=params.get("emotional_tone"),
            cultural_adaptation_parameters=params.get("cultural_adaptation_parameters"),
            callback_url_sample_result=f"{base_url}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{base_url}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{base_url}{api_prefix}/n8n-callbacks/error",
            job_type=job_type,
            selected_sample_id=request.selected_sample_id,
            desired_resolution=kwargs.get("desired_resolution")
        )