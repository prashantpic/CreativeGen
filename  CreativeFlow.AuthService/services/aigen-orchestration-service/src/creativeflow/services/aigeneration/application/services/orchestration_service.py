import json
import logging
from typing import Optional
from uuid import UUID, uuid4
from decimal import Decimal

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.application.dtos import GenerationJobParameters
from .credit_service_client import CreditServiceClient
from .notification_service_client import NotificationServiceClient

logger = logging.getLogger(__name__)

# --- Custom Exceptions ---
class OrchestrationServiceError(Exception):
    """Base exception for orchestration service errors."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class GenerationRequestNotFoundError(OrchestrationServiceError):
    pass

class InsufficientCreditsError(OrchestrationServiceError):
    def __init__(self, user_id: str, detail: str):
        self.user_id = user_id
        super().__init__(detail)

class GenerationJobPublishError(OrchestrationServiceError):
    pass

class GenerationRequestStateError(OrchestrationServiceError):
    pass


class OrchestrationService:
    """Contains the core business logic for managing the AI generation pipeline."""

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
        # 1. Credit Check
        # As per REQ-016, sample generation costs 0.25 credits.
        required_credits_for_sample = Decimal("0.25")
        try:
            # First, check if user has enough credits
            await self._credit_service_client.check_credits(request_data.user_id, float(required_credits_for_sample))
        except InsufficientCreditsError as e:
            # Re-raise with user_id for proper handling
            raise InsufficientCreditsError(user_id=request_data.user_id, detail=e.detail)

        # 2. Create DB record
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            input_parameters=request_data.dict(exclude={"user_id", "project_id", "input_prompt", "style_guidance"}),
            status=GenerationStatus.VALIDATING_CREDITS,
            credits_cost_sample=required_credits_for_sample
        )
        await self._repo.add(new_request)

        # 3. Deduct Credits
        try:
            await self._credit_service_client.deduct_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=float(required_credits_for_sample),
                action_type="sample_generation"
            )
        except Exception as e:
            logger.error(f"Credit deduction failed for request {new_request.id}. Rolling back status.", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Credit deduction failed.")
            await self._repo.update(new_request)
            raise InsufficientCreditsError(user_id=new_request.user_id, detail=f"Failed to deduct credits: {e}")

        # 4. Prepare and Publish Job
        job_payload = self._prepare_n8n_payload(new_request, "sample_generation")
        
        try:
            await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
            new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        except Exception as e:
            logger.error(f"Failed to publish generation job for request {new_request.id}", exc_info=True)
            # Critical error: need to refund credits and fail the request
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to queue generation task.")
            await self._credit_service_client.refund_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=float(required_credits_for_sample),
                reason="System error: failed to publish job to queue."
            )
            await self._repo.update(new_request)
            raise GenerationJobPublishError(detail=str(e))

        await self._repo.update(new_request)
        logger.info(f"Successfully initiated generation request {new_request.id}")
        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFoundError(f"Generation request with ID {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: schemas.N8NSampleResultPayload) -> None:
        request = await self.get_generation_status(callback_data.generation_request_id)
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        request.sample_asset_infos = [schemas.SampleAssetInfo(**s.dict()) for s in callback_data.samples]
        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready!",
            payload={"request_id": str(request.id)}
        )
        logger.info(f"Processed sample callback for request {request.id}. Status set to AWAITING_SELECTION.")

    async def process_n8n_final_asset_callback(self, callback_data: schemas.N8NFinalResultPayload) -> None:
        request = await self.get_generation_status(callback_data.generation_request_id)
        request.update_status(GenerationStatus.COMPLETED)
        request.final_asset_info = callback_data.final_asset
        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )
        logger.info(f"Processed final asset callback for request {request.id}. Status set to COMPLETED.")


    async def handle_n8n_error(self, error_data: schemas.N8NErrorPayload) -> None:
        request = await self.get_generation_status(error_data.generation_request_id)
        
        # Log detailed error if enabled
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for {request.id}: {json.dumps(error_data.dict())}")

        # Update status and error message
        # Example logic: "content_rejected" code sets a specific status
        new_status = GenerationStatus.CONTENT_REJECTED if error_data.error_code == "content_rejected" else GenerationStatus.FAILED
        request.update_status(new_status, error_message=error_data.error_message)

        # Credit Refund Logic (REQ-007.1)
        # Assuming system errors don't have specific user-facing codes like "content_rejected"
        is_system_error = error_data.error_code not in ["content_rejected", "bad_prompt"]
        
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            credits_to_refund = 0
            if error_data.failed_stage == "sample_processing" and request.credits_cost_sample:
                credits_to_refund = request.credits_cost_sample
            elif error_data.failed_stage == "final_processing" and request.credits_cost_final:
                credits_to_refund = request.credits_cost_final
            
            if credits_to_refund > 0:
                logger.info(f"Attempting to refund {credits_to_refund} credits for request {request.id} due to system error.")
                await self._credit_service_client.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=float(credits_to_refund),
                    reason=f"System error during AI generation stage: {error_data.failed_stage}"
                )

        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(
        self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]
    ) -> GenerationRequest:
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            raise GenerationRequestNotFoundError("Request not found for this user.") # Obfuscate for security
        
        # As per REQ-016, regeneration costs the same as the initial sample.
        regeneration_cost = request.credits_cost_sample or Decimal("0.25")

        # Deduct credits
        await self._credit_service_client.deduct_credits(
            user_id=user_id, request_id=request_id, amount=float(regeneration_cost), action_type="sample_regeneration"
        )
        
        # Update request details for regeneration
        if updated_prompt:
            request.input_prompt = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
        
        # Re-publish job
        job_payload = self._prepare_n8n_payload(request, "sample_regeneration")
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(request)
        
        logger.info(f"Triggered sample regeneration for request {request.id}")
        return request


    async def select_sample_and_initiate_final(
        self, request_id: UUID, selected_sample_id: str, user_id: str, desired_resolution: Optional[str]
    ) -> GenerationRequest:
        request = await self.get_generation_status(request_id)
        
        if request.user_id != user_id:
            raise GenerationRequestNotFoundError("Request not found for this user.")
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise GenerationRequestStateError(f"Request is in state '{request.status.value}', not 'AWAITING_SELECTION'.")
        if not any(s.asset_id == selected_sample_id for s in request.sample_asset_infos):
            raise ValueError(f"Selected sample ID '{selected_sample_id}' not found in this request.")

        # As per REQ-016, final generation costs 1 credit. We can add logic for resolution-based pricing.
        final_gen_cost = Decimal("1.00")

        await self._credit_service_client.deduct_credits(
            user_id=user_id, request_id=request_id, amount=float(final_gen_cost), action_type="final_generation"
        )
        
        request.selected_sample_id = selected_sample_id
        request.credits_cost_final = final_gen_cost
        
        job_payload = self._prepare_n8n_payload(request, "final_generation", desired_resolution=desired_resolution)
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        
        logger.info(f"Selected sample {selected_sample_id} for request {request.id}. Initiating final generation.")
        return request


    def _prepare_n8n_payload(
        self,
        request: GenerationRequest,
        job_type: str,
        desired_resolution: Optional[str] = None
    ) -> GenerationJobParameters:
        """Helper to construct the payload for n8n."""
        base_url = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR
        
        input_params = request.input_parameters or {}

        return GenerationJobParameters(
            generation_request_id=request.id,
            user_id=request.user_id,
            project_id=request.project_id,
            input_prompt=request.input_prompt,
            style_guidance=request.style_guidance,
            output_format=input_params.get("output_format"),
            custom_dimensions=input_params.get("custom_dimensions"),
            brand_kit_id=input_params.get("brand_kit_id"),
            uploaded_image_references=input_params.get("uploaded_image_references"),
            target_platform_hints=input_params.get("target_platform_hints"),
            emotional_tone=input_params.get("emotional_tone"),
            cultural_adaptation_parameters=input_params.get("cultural_adaptation_parameters"),
            job_type=job_type,
            callback_url_sample_result=f"{base_url}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{base_url}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{base_url}{api_prefix}/n8n-callbacks/error",
            selected_sample_id=request.selected_sample_id,
            desired_resolution=desired_resolution,
        )