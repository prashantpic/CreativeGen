import logging
from typing import Optional
from uuid import UUID
import json

from fastapi import HTTPException, status

from creativeflow.services.aigeneration.core.config import get_settings
from creativeflow.services.aigeneration.application.dtos import GenerationRequestCreateDTO, N8NSampleResultDTO, N8NFinalResultDTO, N8NErrorDTO
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from .credit_service_client import CreditServiceClient, InsufficientCreditsError, CreditServiceError
from .notification_service_client import NotificationServiceClient

# Custom Application Exceptions
class GenerationRequestNotFound(HTTPException):
    def __init__(self, request_id: UUID):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Generation request with ID '{request_id}' not found.")

class InvalidGenerationState(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class JobPublishError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to publish generation job: {detail}")

logger = logging.getLogger(__name__)

# As per REQ-016
CREDITS_COST_SAMPLE = 0.25
CREDITS_COST_REGENERATION = 0.25
CREDITS_COST_FINAL_DEFAULT = 1.0
CREDITS_COST_FINAL_UPSCALE = 2.0


class OrchestrationService:
    """
    Core application service for orchestrating the AI creative generation pipeline.
    Manages the end-to-end AI creative generation process, from request intake to final asset delivery notification.
    """
    def __init__(
        self,
        repo: IGenerationRequestRepository,
        rabbitmq_publisher: RabbitMQPublisher,
        credit_service_client: CreditServiceClient,
        notification_client: NotificationServiceClient,
    ):
        self._repo = repo
        self._rabbitmq_publisher = rabbitmq_publisher
        self._credit_service_client = credit_service_client
        self._notification_client = notification_client
        self.settings = get_settings()

    async def initiate_generation(self, request_data: GenerationRequestCreateDTO) -> GenerationRequest:
        """
        Initiates a new AI creative generation workflow.
        REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-016
        """
        logger.info(f"Initiating generation for user '{request_data.user_id}' in project '{request_data.project_id}'.")

        # 1. Credit/Subscription Check
        required_credits = CREDITS_COST_SAMPLE
        try:
            subscription_tier = await self._credit_service_client.get_user_subscription_tier(request_data.user_id)
            if subscription_tier.lower() in ["team", "enterprise"]:  # Example tiers with free samples
                 logger.info(f"User '{request_data.user_id}' on tier '{subscription_tier}', skipping sample credit check.")
                 required_credits = 0.0
            else:
                await self._credit_service_client.check_credits(request_data.user_id, required_credits)
        except (InsufficientCreditsError, CreditServiceError) as e:
            logger.warning(f"Credit check failed for user '{request_data.user_id}': {e.detail}")
            raise e

        # 2. Create GenerationRequest Record
        new_request = GenerationRequest(
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            input_parameters=request_data.dict(exclude={"user_id", "project_id", "input_prompt", "style_guidance"}),
            status=GenerationStatus.VALIDATING_CREDITS
        )
        await self._repo.add(new_request)
        logger.info(f"Created GenerationRequest record with ID: {new_request.id}")

        # 3. Deduct Credits
        if required_credits > 0:
            try:
                await self._credit_service_client.deduct_credits(
                    user_id=request_data.user_id,
                    request_id=new_request.id,
                    amount=required_credits,
                    action_type="sample_generation_fee"
                )
                new_request.credits_cost_sample = required_credits
                logger.info(f"Deducted {required_credits} credits for sample generation for request {new_request.id}.")
            except CreditServiceError as e:
                logger.error(f"Credit deduction failed for request {new_request.id}. Error: {e.detail}")
                new_request.update_status(GenerationStatus.FAILED, error_message="Credit deduction failed.")
                await self._repo.update(new_request)
                raise e

        # 4. Prepare and Publish n8n Job
        try:
            job_payload = self._prepare_n8n_job_payload(new_request, "sample_generation")
            new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
            await self._repo.update(new_request)
            
            self._rabbitmq_publisher.publish_generation_job(
                job_payload=job_payload,
                routing_key=self.settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                exchange_name=self.settings.RABBITMQ_GENERATION_EXCHANGE
            )
            logger.info(f"Published sample generation job for request {new_request.id} to RabbitMQ.")
        except Exception as e:
            logger.critical(f"Failed to publish RabbitMQ job for request {new_request.id}: {e}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to queue generation job.")
            await self._repo.update(new_request)
            # Attempt to refund credits if they were deducted
            if new_request.credits_cost_sample > 0:
                await self._try_refund_credits(new_request, new_request.credits_cost_sample, "Job publishing failure")
            raise JobPublishError(str(e))

        # 5. Final Status Update
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        
        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Retrieves the status and details of a specific generation request."""
        generation_request = await self._repo.get_by_id(request_id)
        if not generation_request:
            raise GenerationRequestNotFound(request_id)
        return generation_request

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultDTO) -> None:
        """Processes the callback from n8n after sample generation is complete. REQ-008"""
        logger.info(f"Processing n8n sample callback for request ID: {callback_data.generation_request_id}")
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received n8n sample callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.add_sample_result(callback_data.samples)
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(callback_data.samples)} samples.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            metadata={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultDTO) -> None:
        """Processes the callback from n8n after final asset generation is complete. REQ-009"""
        logger.info(f"Processing n8n final asset callback for request ID: {callback_data.generation_request_id}")
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received n8n final asset callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.set_final_asset(callback_data.final_asset)
        request.update_status(GenerationStatus.COMPLETED)
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to COMPLETED with final asset.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is generated and ready!",
            metadata={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )

    async def handle_n8n_error(self, error_data: N8NErrorDTO) -> None:
        """Handles error callbacks from n8n. REQ-007.1, REQ-016"""
        logger.error(f"Processing n8n error callback for request ID: {error_data.generation_request_id}. Error: {error_data.error_message}")
        request = await self._repo.get_by_id(error_data.generation_request_id)
        if not request:
            logger.error(f"Received n8n error callback for non-existent request ID: {error_data.generation_request_id}")
            return

        # Determine new status
        new_status = GenerationStatus.FAILED
        if error_data.error_code and "CONTENT_POLICY" in error_data.error_code.upper():
            new_status = GenerationStatus.CONTENT_REJECTED
        
        request.update_status(new_status, error_message=error_data.error_message, error_details=error_data.error_details)
        
        # Log detailed errors if enabled
        if self.settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for request {request.id}: {error_data.error_details}")

        # Credit Refund Logic
        # Assuming system errors don't have specific "user error" codes like CONTENT_POLICY
        is_system_error = new_status == GenerationStatus.FAILED
        if self.settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE and is_system_error:
            credits_to_refund = 0
            if error_data.failed_stage == "sample_processing" and request.credits_cost_sample:
                credits_to_refund = request.credits_cost_sample
            elif error_data.failed_stage == "final_processing" and request.credits_cost_final:
                credits_to_refund = request.credits_cost_final

            if credits_to_refund > 0:
                await self._try_refund_credits(request, credits_to_refund, f"System error during {error_data.failed_stage}")

        await self._repo.update(request)

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            metadata={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str] = None, updated_style_guidance: Optional[str] = None) -> GenerationRequest:
        """Triggers a regeneration of samples for an existing request. REQ-008, REQ-016"""
        logger.info(f"Triggering sample regeneration for request {request_id} by user {user_id}.")
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            raise InvalidGenerationState("User not authorized to modify this request.")
        
        if request.status not in [GenerationStatus.AWAITING_SELECTION, GenerationStatus.FAILED, GenerationStatus.CONTENT_REJECTED]:
            raise InvalidGenerationState(f"Cannot regenerate from current status: {request.status.value}")

        # Credit Check & Deduction for Regeneration
        required_credits = CREDITS_COST_REGENERATION
        try:
            await self._credit_service_client.deduct_credits(
                user_id=user_id,
                request_id=request_id,
                amount=required_credits,
                action_type="sample_regeneration_fee"
            )
            request.credits_cost_sample = (request.credits_cost_sample or 0) + required_credits
            logger.info(f"Deducted {required_credits} credits for regeneration of request {request.id}.")
        except (InsufficientCreditsError, CreditServiceError) as e:
            logger.warning(f"Credit check failed for regeneration for user '{user_id}': {e.detail}")
            raise e

        # Prepare new job payload
        if updated_prompt:
            request.input_prompt = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
            
        job_payload = self._prepare_n8n_job_payload(request, "sample_regeneration")
        self._rabbitmq_publisher.publish_generation_job(job_payload, self.settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self.settings.RABBITMQ_GENERATION_EXCHANGE)
        
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(request)
        
        logger.info(f"Published sample regeneration job for request {request.id}.")
        return request

    async def select_sample_and_initiate_final(self, request_id: UUID, selected_sample_id: str, user_id: str, desired_resolution: Optional[str] = None) -> GenerationRequest:
        """Selects a sample and initiates the final, high-resolution generation. REQ-009, REQ-016"""
        logger.info(f"User {user_id} selected sample {selected_sample_id} for request {request_id}.")
        request = await self.get_generation_status(request_id)
        
        if request.user_id != user_id:
            raise InvalidGenerationState("User not authorized to modify this request.")
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidGenerationState(f"Cannot select sample from current status: {request.status.value}")
        if not any(s.asset_id == selected_sample_id for s in request.sample_asset_infos):
            raise InvalidGenerationState(f"Selected sample ID '{selected_sample_id}' not found in this request.")
            
        # Credit Check & Deduction for Final Generation
        required_credits = CREDITS_COST_FINAL_UPSCALE if desired_resolution and "4k" in desired_resolution.lower() else CREDITS_COST_FINAL_DEFAULT
        try:
             await self._credit_service_client.deduct_credits(
                user_id=user_id,
                request_id=request_id,
                amount=required_credits,
                action_type="final_generation_fee"
            )
             request.credits_cost_final = required_credits
             logger.info(f"Deducted {required_credits} credits for final generation of request {request.id}.")
        except (InsufficientCreditsError, CreditServiceError) as e:
            logger.warning(f"Credit check failed for final generation for user '{user_id}': {e.detail}")
            raise e
            
        # Prepare Job
        request.set_selected_sample(selected_sample_id, desired_resolution)
        job_payload = self._prepare_n8n_job_payload(request, "final_generation")
        self._rabbitmq_publisher.publish_generation_job(job_payload, self.settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self.settings.RABBITMQ_GENERATION_EXCHANGE)
        
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        
        logger.info(f"Published final generation job for request {request.id}.")
        return request

    def _prepare_n8n_job_payload(self, request: GenerationRequest, job_type: str) -> dict:
        """Helper method to construct the JSON payload for n8n workflows."""
        base_url = self.settings.N8N_CALLBACK_BASE_URL
        payload = {
            "generation_request_id": str(request.id),
            "user_id": request.user_id,
            "project_id": request.project_id,
            "input_prompt": request.input_prompt,
            "style_guidance": request.style_guidance,
            "input_parameters": request.input_parameters,
            "callback_url_error": f"{base_url}{self.settings.API_V1_STR}/n8n-callbacks/error",
            "job_type": job_type
        }
        
        if job_type in ["sample_generation", "sample_regeneration"]:
            payload["callback_url_sample_result"] = f"{base_url}{self.settings.API_V1_STR}/n8n-callbacks/sample-result"
        
        if job_type == "final_generation":
            payload["callback_url_final_result"] = f"{base_url}{self.settings.API_V1_STR}/n8n-callbacks/final-result"
            payload["selected_sample_id"] = request.selected_sample_id
            payload["desired_resolution"] = request.input_parameters.get("desired_resolution")

        return payload

    async def _try_refund_credits(self, request: GenerationRequest, amount: float, reason: str) -> None:
        """Internal helper to attempt a credit refund and log the outcome."""
        try:
            success = await self._credit_service_client.refund_credits(
                user_id=request.user_id,
                request_id=request.id,
                amount=amount,
                reason=reason
            )
            if success:
                logger.info(f"Successfully refunded {amount} credits for request {request.id}. Reason: {reason}")
            else:
                logger.error(f"Credit service failed to process refund for request {request.id}.")
        except Exception as e:
            logger.error(f"Exception during credit refund attempt for request {request.id}: {e}", exc_info=True)