import logging
import json
from uuid import UUID
from typing import Optional

from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application import dtos
from creativeflow.services.aigeneration.application.exceptions import (
    ResourceNotFoundError,
    InvalidStateError,
    InsufficientCreditsError,
    GenerationJobPublishError
)

logger = logging.getLogger(__name__)

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
        settings: Settings,
    ):
        self._repo = repo
        self._rabbitmq_publisher = rabbitmq_publisher
        self._credit_service_client = credit_service_client
        self._notification_client = notification_client
        self._settings = settings

    async def initiate_generation(self, request_data: schemas.GenerationRequestCreate) -> GenerationRequest:
        """Orchestrates the initiation of a new AI generation request."""
        logger.info(f"Initiating generation for user {request_data.user_id}")

        # REQ-016: Determine credit cost for samples
        # This can be made more dynamic based on subscription tier, etc.
        required_credits_sample = 0.25
        
        # Check credits if necessary
        await self._credit_service_client.check_credits(request_data.user_id, required_credits_sample)
        
        # Create domain object and persist initial state
        new_request = GenerationRequest.create_new(
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            input_parameters=request_data.dict(exclude={'user_id', 'project_id', 'input_prompt', 'style_guidance'}),
            status=GenerationStatus.PENDING
        )
        await self._repo.add(new_request)
        logger.info(f"Created new generation request {new_request.id} with status PENDING.")

        # Deduct credits
        try:
            new_request.update_status(GenerationStatus.VALIDATING_CREDITS)
            await self._credit_service_client.deduct_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=required_credits_sample,
                action_type="sample_generation"
            )
            new_request.set_credit_cost(sample_cost=required_credits_sample)
            await self._repo.update(new_request)
        except Exception as e:
            new_request.update_status(GenerationStatus.FAILED, error_message=f"Credit deduction failed: {e}")
            await self._repo.update(new_request)
            logger.error(f"Credit deduction failed for request {new_request.id}. Error: {e}")
            # Re-raise to be caught by the endpoint handler
            raise

        # Prepare and publish job
        job_payload = self._prepare_n8n_payload(new_request, "sample_generation")
        await self._rabbitmq_publisher.publish_generation_job(job_payload)
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        logger.info(f"Published sample generation job for request {new_request.id} and set status to PROCESSING_SAMPLES.")

        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Retrieves a generation request by its ID."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise ResourceNotFoundError(f"Generation request with ID {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: dtos.N8NSampleResultInternal) -> None:
        """Processes the callback from n8n when samples are ready."""
        request = await self.get_generation_status(callback_data.generation_request_id)
        
        sample_assets = [sample.dict() for sample in callback_data.samples]
        request.add_sample_results(sample_assets)
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(sample_assets)} samples.")
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: dtos.N8NFinalResultInternal) -> None:
        """Processes the callback from n8n when the final asset is ready."""
        request = await self.get_generation_status(callback_data.generation_request_id)
        
        final_asset = callback_data.final_asset.dict()
        request.set_final_asset(final_asset)
        request.update_status(GenerationStatus.COMPLETED)
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to COMPLETED.")
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": final_asset['url']}
        )

    async def handle_n8n_error(self, error_data: dtos.N8NErrorInternal) -> None:
        """Handles an error callback from n8n."""
        request = await self.get_generation_status(error_data.generation_request_id)
        
        error_message = error_data.error_message
        new_status = GenerationStatus.FAILED

        # Check for content policy violation
        if error_data.error_code in ["CONTENT_POLICY_VIOLATION", "429"]: # Example codes
             new_status = GenerationStatus.CONTENT_REJECTED

        request.update_status(new_status, error_message=error_message)

        # Log detailed errors if enabled
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for request {request.id}: {json.dumps(error_data.dict())}")

        # REQ-007.1: Credit Refund Logic
        if self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            # Simple logic: refund if it's a system error (not content rejection)
            if new_status == GenerationStatus.FAILED:
                cost_to_refund = 0.0
                if error_data.failed_stage == "sample_processing" and request.credits_cost_sample:
                    cost_to_refund = request.credits_cost_sample
                elif error_data.failed_stage == "final_processing" and request.credits_cost_final:
                    cost_to_refund = request.credits_cost_final
                
                if cost_to_refund > 0:
                    try:
                        await self._credit_service_client.refund_credits(
                            user_id=request.user_id,
                            request_id=request.id,
                            amount=cost_to_refund,
                            reason=f"System error during AI generation stage: {error_data.failed_stage}"
                        )
                        logger.info(f"Successfully processed refund of {cost_to_refund} credits for request {request.id}.")
                    except Exception as e:
                        logger.error(f"Failed to process refund for request {request.id}. Error: {e}")

        await self._repo.update(request)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]) -> GenerationRequest:
        """Triggers a regeneration of samples for a request."""
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
             raise ResourceNotFoundError(f"Request {request_id} not found for user {user_id}.")

        # REQ-016: Credit check for regeneration
        regeneration_cost = 0.25 # Can be dynamic
        await self._credit_service_client.check_credits(user_id, regeneration_cost)
        await self._credit_service_client.deduct_credits(user_id, request_id, regeneration_cost, "sample_regeneration")

        request.set_credit_cost(sample_cost=regeneration_cost, append=True) # Logic to append cost
        if updated_prompt:
            request.input_prompt = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance

        job_payload = self._prepare_n8n_payload(request, "sample_regeneration")
        await self._rabbitmq_publisher.publish_generation_job(job_payload)

        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(request)
        logger.info(f"Triggered sample regeneration for request {request.id}.")
        return request

    async def select_sample_and_initiate_final(self, request_id: UUID, user_id: str, selected_sample_id: str, desired_resolution: Optional[str]) -> GenerationRequest:
        """Selects a sample and initiates the final high-resolution generation."""
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            raise ResourceNotFoundError(f"Request {request_id} not found for user {user_id}.")

        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidStateError(f"Request {request_id} is not awaiting selection. Current status: {request.status.value}")

        request.set_selected_sample(selected_sample_id)
        
        # REQ-016: Credit check for final generation
        final_gen_cost = 1.0 # Can be dynamic (e.g., based on resolution)
        await self._credit_service_client.check_credits(user_id, final_gen_cost)
        await self._credit_service_client.deduct_credits(user_id, request_id, final_gen_cost, "final_generation")
        request.set_credit_cost(final_cost=final_gen_cost)

        job_payload = self._prepare_n8n_payload(request, "final_generation", desired_resolution=desired_resolution)
        await self._rabbitmq_publisher.publish_generation_job(job_payload)

        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        logger.info(f"Initiated final generation for request {request.id} with sample {selected_sample_id}.")
        return request

    def _prepare_n8n_payload(self, request: GenerationRequest, job_type: str, **kwargs) -> dict:
        """Helper to construct the JSON payload for n8n."""
        base_url = str(self._settings.N8N_CALLBACK_BASE_URL)
        
        payload_data = dtos.GenerationJobParameters(
            generation_request_id=request.id,
            user_id=request.user_id,
            project_id=request.project_id,
            input_prompt=request.input_prompt,
            style_guidance=request.style_guidance,
            output_format=request.input_parameters.get("output_format"),
            custom_dimensions=request.input_parameters.get("custom_dimensions"),
            brand_kit_id=request.input_parameters.get("brand_kit_id"),
            uploaded_image_references=request.input_parameters.get("uploaded_image_references"),
            target_platform_hints=request.input_parameters.get("target_platform_hints"),
            emotional_tone=request.input_parameters.get("emotional_tone"),
            cultural_adaptation_parameters=request.input_parameters.get("cultural_adaptation_parameters"),
            job_type=job_type,
            callback_url_sample_result=f"{base_url}{self._settings.API_V1_STR}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{base_url}{self._settings.API_V1_STR}/n8n-callbacks/final-result",
            callback_url_error=f"{base_url}{self._settings.API_V1_STR}/n8n-callbacks/error",
            selected_sample_id=request.selected_sample_id,
            desired_resolution=kwargs.get("desired_resolution")
        )
        return payload_data.dict(exclude_none=True)