"""
Core Application Service for Orchestrating AI Generation.

This service contains the primary business logic for managing the end-to-end
AI creative generation pipeline. It coordinates between API requests, the
database, the message queue, and external services like credit and notification.
"""
import json
import logging
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

from pydantic import ValidationError

from ...core.config import Settings
from ...domain.models.generation_request import GenerationRequest
from ...domain.models.generation_status import GenerationStatus
from ...domain.repositories.generation_request_repository import IGenerationRequestRepository
from ...infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from .credit_service_client import CreditServiceClient, InsufficientCreditsError, CreditServiceError
from .notification_service_client import NotificationServiceClient
from ..dtos import (
    GenerationRequestCreateDTO,
    N8NSampleResultDTO,
    N8NFinalResultDTO,
    N8NErrorDTO,
    GenerationJobParameters
)

logger = logging.getLogger(__name__)

# --- Custom Application Exceptions ---
class GenerationRequestNotFound(Exception):
    pass

class InvalidGenerationStateError(Exception):
    pass

class JobPublishError(Exception):
    pass

# --- Credit Costs (example values, could come from config or a service) ---
CREDIT_COST_SAMPLE_GENERATION = 0.25
CREDIT_COST_REGENERATION = 0.25
CREDIT_COST_FINAL_SD = 1.0
CREDIT_COST_FINAL_HD = 2.0


class OrchestrationService:
    """Orchestrates the AI creative generation workflows."""

    def __init__(
        self,
        repo: IGenerationRequestRepository,
        rabbitmq_publisher: RabbitMQPublisher,
        credit_service_client: CreditServiceClient,
        notification_client: NotificationServiceClient,
        settings: Settings,
    ):
        self._repo = repo
        self._rabbitmq_publisher = rabbitmq_publisher
        self._credit_service = credit_service_client
        self._notification_client = notification_client
        self._settings = settings

    async def initiate_generation(self, request_data: GenerationRequestCreateDTO) -> GenerationRequest:
        """Orchestrates the initiation of a new AI generation request."""
        logger.info(f"Initiating generation for user {request_data.user_id}")

        # 1. Credit Check
        required_credits = CREDIT_COST_SAMPLE_GENERATION
        try:
            # Note: A real implementation might check subscription tier first
            # and skip credit deduction for some plans.
            await self._credit_service.deduct_credits(
                user_id=request_data.user_id,
                request_id=uuid4(), # A temporary ID for the deduction log
                amount=required_credits,
                action_type="sample_generation"
            )
        except (InsufficientCreditsError, CreditServiceError) as e:
            logger.warning(f"Credit check/deduction failed for user {request_data.user_id}: {e}")
            raise e # Re-raise to be caught by error handlers

        # 2. Create GenerationRequest Record
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            status=GenerationStatus.PENDING,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            # Store all other inputs in a flexible JSONB field
            input_parameters={
                "output_format": request_data.output_format,
                "custom_dimensions": request_data.custom_dimensions.dict() if request_data.custom_dimensions else None,
                "brand_kit_id": request_data.brand_kit_id,
                "uploaded_image_references": request_data.uploaded_image_references,
                "target_platform_hints": request_data.target_platform_hints,
                "emotional_tone": request_data.emotional_tone,
                "cultural_adaptation_parameters": request_data.cultural_adaptation_parameters
            },
            credits_cost_sample=required_credits,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        await self._repo.add(new_request)
        logger.info(f"Created GenerationRequest record {new_request.id}")

        # 3. Prepare and Publish n8n Job
        try:
            job_payload = self._prepare_n8n_job_payload(new_request, "sample_generation")
            await self._rabbitmq_publisher.publish_message(job_payload.json())
            new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        except (ValidationError, Exception) as e:
            logger.error(f"Failed to prepare or publish job for request {new_request.id}: {e}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to publish job to queue.")
            # Refund the credits
            await self._credit_service.refund_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=required_credits,
                reason="System error: failed to publish job"
            )
            await self._repo.update(new_request)
            raise JobPublishError("Failed to publish generation job to the message queue.") from e
        
        await self._repo.update(new_request)
        logger.info(f"Published job for request {new_request.id} and updated status to PROCESSING_SAMPLES.")
        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFound(f"Generation request with ID {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultDTO) -> None:
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received sample callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.add_sample_results([s.dict() for s in callback_data.samples])
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        await self._repo.update(request)
        logger.info(f"Updated request {request.id} to AWAITING_SELECTION with {len(callback_data.samples)} samples.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultDTO) -> None:
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received final asset callback for non-existent request ID: {callback_data.generation_request_id}")
            return
            
        request.set_final_asset(callback_data.final_asset.dict())
        request.update_status(GenerationStatus.COMPLETED)
        await self._repo.update(request)
        logger.info(f"Updated request {request.id} to COMPLETED.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is generated and ready!",
            payload={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )

    async def handle_n8n_error(self, error_data: N8NErrorDTO) -> None:
        request = await self._repo.get_by_id(error_data.generation_request_id)
        if not request:
            logger.error(f"Received error callback for non-existent request ID: {error_data.generation_request_id}")
            return

        error_message = error_data.error_message
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING and error_data.error_details:
             logger.error(f"Detailed n8n error for request {request.id}: {json.dumps(error_data.error_details)}")
        
        # Determine status and if refund is applicable
        # This logic can be more sophisticated based on error_code
        is_system_error = "policy" not in error_data.error_message.lower()
        new_status = GenerationStatus.FAILED if is_system_error else GenerationStatus.CONTENT_REJECTED
        
        request.update_status(new_status, error_message=error_message)

        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            credits_to_refund = 0
            if error_data.failed_stage == 'sample_processing' and request.credits_cost_sample:
                credits_to_refund = request.credits_cost_sample
            elif error_data.failed_stage == 'final_processing' and request.credits_cost_final:
                credits_to_refund = request.credits_cost_final
            
            if credits_to_refund > 0:
                logger.info(f"Refunding {credits_to_refund} credits for failed request {request.id}")
                await self._credit_service.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=credits_to_refund,
                    reason=f"System error during AI generation stage: {error_data.failed_stage}"
                )

        await self._repo.update(request)
        logger.info(f"Updated request {request.id} to {new_status.value} due to error.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"Your AI generation failed: {error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(
        self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]
    ) -> GenerationRequest:
        request = await self._get_and_validate_request(request_id, user_id)
        
        # 1. Credit Check for Regeneration
        await self._credit_service.deduct_credits(
            user_id=user_id, request_id=request_id, amount=CREDIT_COST_REGENERATION, action_type="sample_regeneration"
        )
        
        # 2. Update request with new prompt if provided
        if updated_prompt:
            request.input_prompt = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
        
        # 3. Publish job
        job_payload = self._prepare_n8n_job_payload(request, "sample_regeneration")
        await self._rabbitmq_publisher.publish_message(job_payload.json())
        
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        request.credits_cost_sample = (request.credits_cost_sample or 0) + CREDIT_COST_REGENERATION
        await self._repo.update(request)
        logger.info(f"Published regeneration job for request {request.id}")
        return request

    async def select_sample_and_initiate_final(
        self, request_id: UUID, user_id: str, selected_sample_id: str, desired_resolution: Optional[str]
    ) -> GenerationRequest:
        request = await self._get_and_validate_request(
            request_id, user_id, expected_status=GenerationStatus.AWAITING_SELECTION
        )

        if not any(sample.get('asset_id') == selected_sample_id for sample in request.sample_asset_infos):
            raise InvalidGenerationStateError(f"Selected sample ID {selected_sample_id} not found in request {request_id}.")

        # 1. Credit check for final generation
        required_credits = CREDIT_COST_FINAL_HD if desired_resolution == "4K" else CREDIT_COST_FINAL_SD
        await self._credit_service.deduct_credits(
            user_id=user_id, request_id=request_id, amount=required_credits, action_type="final_generation"
        )

        request.selected_sample_id = selected_sample_id
        request.credits_cost_final = required_credits

        # 2. Publish Job
        job_payload = self._prepare_n8n_job_payload(
            request, "final_generation", selected_sample_id=selected_sample_id, desired_resolution=desired_resolution
        )
        await self._rabbitmq_publisher.publish_message(job_payload.json())
        
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        logger.info(f"Published final generation job for request {request.id}")
        return request

    def _prepare_n8n_job_payload(
        self, request: GenerationRequest, job_type: str, **kwargs
    ) -> GenerationJobParameters:
        """Helper to construct the job payload for RabbitMQ."""
        callback_base = self._settings.N8N_CALLBACK_BASE_URL.rstrip('/')
        
        payload_data = {
            "generation_request_id": request.id,
            "user_id": request.user_id,
            "project_id": request.project_id,
            "input_prompt": request.input_prompt,
            "style_guidance": request.style_guidance,
            **request.input_parameters,
            "job_type": job_type,
            "callback_url_sample_result": f"{callback_base}{self._settings.API_V1_STR}/n8n-callbacks/sample-result",
            "callback_url_final_result": f"{callback_base}{self._settings.API_V1_STR}/n8n-callbacks/final-result",
            "callback_url_error": f"{callback_base}{self._settings.API_V1_STR}/n8n-callbacks/error",
            **kwargs
        }
        return GenerationJobParameters(**payload_data)

    async def _get_and_validate_request(
        self, request_id: UUID, user_id: str, expected_status: Optional[GenerationStatus] = None
    ) -> GenerationRequest:
        """Fetches a request and performs common validations."""
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            logger.warning(f"User {user_id} attempted to access request {request_id} owned by {request.user_id}")
            raise GenerationRequestNotFound(f"Generation request with ID {request_id} not found.")
        
        if expected_status and request.status != expected_status:
            raise InvalidGenerationStateError(
                f"Request {request_id} is in status '{request.status.value}', but expected '{expected_status.value}'."
            )
        return request