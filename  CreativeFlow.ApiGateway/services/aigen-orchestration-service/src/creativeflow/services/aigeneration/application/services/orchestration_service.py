import logging
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone

from fastapi import HTTPException, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application import dtos
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher

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

    async def initiate_generation(self, request_data: dtos.GenerationRequestCreateDTO) -> GenerationRequest:
        """
        Orchestrates the initiation of a new AI generation request.
        Covers validation, credit check/deduction, DB record creation, and job publishing.
        """
        logger.info(f"Initiating generation for user '{request_data.user_id}'")

        # 1. Credit/Subscription Check
        # As per REQ-016, sample generation costs 0.25 credits.
        required_credits_for_sample = 0.25
        
        # Check if the user's subscription tier gets free samples
        # subscription_tier = await self._credit_service_client.get_user_subscription_tier(request_data.user_id)
        # if subscription_tier in ["Pro", "Team", "Enterprise"]:
        #    required_credits_for_sample = 0
        
        # 2. Create Initial GenerationRequest Record in DB
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            status=GenerationStatus.VALIDATING_CREDITS,
            input_parameters=request_data.dict(exclude={"user_id", "project_id", "input_prompt", "style_guidance"}),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await self._repo.add(new_request)

        # 3. Deduct Credits
        try:
            if required_credits_for_sample > 0:
                await self._credit_service_client.deduct_credits(
                    user_id=new_request.user_id,
                    request_id=new_request.id,
                    amount=required_credits_for_sample,
                    action_type="sample_generation"
                )
            new_request.credits_cost_sample = required_credits_for_sample
            new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
            await self._repo.update(new_request)

        except Exception as e:
            logger.error(f"Credit deduction failed for request {new_request.id}: {e}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Credit deduction failed.")
            await self._repo.update(new_request)
            # Re-raise the original exception to be caught by the API layer
            raise e

        # 4. Prepare and Publish n8n Job Payload
        try:
            base_callback_url = self._settings.N8N_CALLBACK_BASE_URL
            job_payload = dtos.GenerationJobParameters(
                **request_data.dict(),
                generation_request_id=new_request.id,
                callback_url_sample_result=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/sample-result",
                callback_url_final_result=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/final-result",
                callback_url_error=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/error",
                job_type="sample_generation"
            )
            
            await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
            
            # 5. Update Status to Processing
            new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
            await self._repo.update(new_request)
            logger.info(f"Successfully published generation job for request {new_request.id}")
        
        except Exception as e:
            logger.critical(f"Failed to publish job for request {new_request.id}: {e}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to publish generation job.")
            await self._repo.update(new_request)
            # Attempt to refund credits
            if required_credits_for_sample > 0:
                logger.info(f"Attempting to refund credits for failed job publish: {new_request.id}")
                await self._credit_service_client.refund_credits(
                    user_id=new_request.user_id,
                    request_id=new_request.id,
                    amount=required_credits_for_sample,
                    reason="System error: failed to publish job to queue."
                )
            raise e

        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Fetches a generation request by its ID."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation request not found")
        return request

    async def process_n8n_sample_callback(self, callback_data: dtos.N8NSampleResultDTO) -> None:
        """Processes the callback from n8n with generated samples."""
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received sample callback for non-existent request ID: {callback_data.generation_request_id}")
            return
        
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        request.add_sample_results([schemas.AssetInfoBase(**s.dict()) for s in callback_data.samples])
        await self._repo.update(request)
        
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(callback_data.samples)} samples.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: dtos.N8NFinalResultDTO) -> None:
        """Processes the callback from n8n with the final generated asset."""
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received final asset callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.update_status(GenerationStatus.COMPLETED)
        request.set_final_asset(schemas.AssetInfoBase(**callback_data.final_asset.dict()))
        await self._repo.update(request)
        
        logger.info(f"Request {request.id} updated to COMPLETED.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )

    async def handle_n8n_error(self, error_data: dtos.N8NErrorDTO) -> None:
        """Handles error callbacks from n8n, including potential credit refunds."""
        request = await self._repo.get_by_id(error_data.generation_request_id)
        if not request:
            logger.error(f"Received error callback for non-existent request ID: {error_data.generation_request_id}")
            return

        # Determine error type and update status
        error_message = error_data.error_message
        new_status = GenerationStatus.FAILED
        if "content policy" in error_message.lower() or error_data.error_code == "CONTENT_POLICY_VIOLATION":
            new_status = GenerationStatus.CONTENT_REJECTED
        
        request.update_status(new_status, error_message=error_message)
        request.error_details = error_data.error_details
        await self._repo.update(request)
        
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for request {request.id}: {error_data.error_details}")

        # Credit Refund Logic (REQ-007.1)
        # We refund if it's a system error, not a content policy violation, and the feature is enabled.
        is_system_error = new_status == GenerationStatus.FAILED
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            # Determine which stage failed and refund the corresponding cost
            failed_stage = error_data.failed_stage
            amount_to_refund = 0.0
            if failed_stage == "sample_processing" and request.credits_cost_sample:
                amount_to_refund = request.credits_cost_sample
            elif failed_stage == "final_processing" and request.credits_cost_final:
                amount_to_refund = request.credits_cost_final

            if amount_to_refund > 0:
                logger.info(f"Attempting to refund {amount_to_refund} credits for request {request.id} due to system failure.")
                await self._credit_service_client.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=amount_to_refund,
                    reason=f"System error during AI generation stage: {failed_stage}"
                )

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_message}",
            payload={"request_id": str(request.id)}
        )

    async def select_sample_and_initiate_final(
        self, request_id: UUID, user_id: str, selected_sample_id: str, desired_resolution: Optional[str]
    ) -> GenerationRequest:
        """Orchestrates the selection of a sample and initiation of the final generation."""
        request = await self.get_generation_status(request_id)
        
        if request.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized for this request")
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Request is not awaiting selection, current status: {request.status.value}")
        if not any(s.asset_id == selected_sample_id for s in request.sample_asset_infos):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected sample ID is not valid for this request")

        # Credit deduction for final generation (REQ-016)
        # E.g., 1 credit for standard HD, 2 for 4K
        required_credits_final = 1.0
        if desired_resolution and "4k" in desired_resolution.lower():
            required_credits_final = 2.0
            
        try:
            await self._credit_service_client.deduct_credits(
                user_id=request.user_id, request_id=request.id, amount=required_credits_final, action_type="final_generation"
            )
            request.credits_cost_final = required_credits_final
            request.selected_sample_id = selected_sample_id
            await self._repo.update(request)
        except Exception as e:
            logger.error(f"Credit deduction for final generation failed for request {request.id}: {e}", exc_info=True)
            raise e
            
        # Prepare and publish job
        try:
            base_callback_url = self._settings.N8N_CALLBACK_BASE_URL
            job_payload = dtos.GenerationJobParameters(
                generation_request_id=request.id,
                user_id=request.user_id,
                project_id=request.project_id,
                input_prompt=request.input_prompt, # pass original context
                style_guidance=request.style_guidance,
                output_format=request.input_parameters.get("output_format"),
                custom_dimensions=request.input_parameters.get("custom_dimensions"),
                brand_kit_id=request.input_parameters.get("brand_kit_id"),
                uploaded_image_references=request.input_parameters.get("uploaded_image_references"),
                target_platform_hints=request.input_parameters.get("target_platform_hints"),
                emotional_tone=request.input_parameters.get("emotional_tone"),
                cultural_adaptation_parameters=request.input_parameters.get("cultural_adaptation_parameters"),
                callback_url_sample_result="", # Not needed
                callback_url_final_result=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/final-result",
                callback_url_error=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/error",
                job_type="final_generation",
                selected_sample_id=selected_sample_id,
                desired_resolution=desired_resolution or "1024x1024" # Default resolution
            )
            
            await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
            request.update_status(GenerationStatus.PROCESSING_FINAL)
            await self._repo.update(request)
            logger.info(f"Published final generation job for request {request.id}")

        except Exception as e:
            # Handle publish failure and refund credits
            logger.critical(f"Failed to publish final generation job for request {request.id}: {e}", exc_info=True)
            request.update_status(GenerationStatus.FAILED, error_message="Failed to publish final generation job.")
            await self._repo.update(request)
            await self._credit_service_client.refund_credits(
                user_id=request.user_id, request_id=request.id, amount=required_credits_final, reason="System error: failed to publish final job."
            )
            raise e
            
        return request

    async def trigger_sample_regeneration(
        self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]
    ) -> GenerationRequest:
        """Orchestrates the regeneration of samples."""
        request = await self.get_generation_status(request_id)

        if request.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized for this request")
        if request.status not in [GenerationStatus.AWAITING_SELECTION, GenerationStatus.FAILED, GenerationStatus.CONTENT_REJECTED]:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Cannot regenerate from current status: {request.status.value}")

        # Credit deduction for regeneration (same as initial sample cost)
        required_credits_regen = 0.25
        try:
            await self._credit_service_client.deduct_credits(
                user_id=request.user_id, request_id=request.id, amount=required_credits_regen, action_type="sample_regeneration"
            )
            # Potentially update cumulative cost, for now we overwrite/set it.
            request.credits_cost_sample = (request.credits_cost_sample or 0) + required_credits_regen
            await self._repo.update(request)
        except Exception as e:
            logger.error(f"Credit deduction for regeneration failed for request {request.id}: {e}", exc_info=True)
            raise e
            
        # Use updated parameters if provided, else use original
        request.input_prompt = updated_prompt or request.input_prompt
        request.style_guidance = updated_style_guidance or request.style_guidance
        if updated_prompt: request.input_parameters['input_prompt'] = updated_prompt
        if updated_style_guidance: request.input_parameters['style_guidance'] = updated_style_guidance
        
        # Publish job
        try:
            base_callback_url = self._settings.N8N_CALLBACK_BASE_URL
            job_payload = dtos.GenerationJobParameters(
                generation_request_id=request.id,
                user_id=request.user_id,
                project_id=request.project_id,
                input_prompt=request.input_prompt,
                style_guidance=request.style_guidance,
                **request.input_parameters,
                callback_url_sample_result=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/sample-result",
                callback_url_final_result=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/final-result",
                callback_url_error=f"{base_callback_url}{self._settings.API_V1_STR}/n8n-callbacks/error",
                job_type="sample_regeneration"
            )
            
            await self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
            request.update_status(GenerationStatus.PROCESSING_SAMPLES)
            # Clear previous samples and errors
            request.sample_asset_infos = []
            request.error_message = None
            request.error_details = None
            await self._repo.update(request)
            logger.info(f"Published sample regeneration job for request {request.id}")
        except Exception as e:
            # Handle publish failure and refund
            logger.critical(f"Failed to publish regeneration job for request {request.id}: {e}", exc_info=True)
            request.update_status(GenerationStatus.FAILED, error_message="Failed to publish regeneration job.")
            await self._repo.update(request)
            await self._credit_service_client.refund_credits(
                user_id=request.user_id, request_id=request.id, amount=required_credits_regen, reason="System error: failed to publish regeneration job."
            )
            raise e

        return request