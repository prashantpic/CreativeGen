import logging
from uuid import UUID, uuid4
from datetime import datetime
import json

from ..dtos import (
    GenerationRequestCreateDTO,
    N8NSampleResultDTO,
    N8NFinalResultDTO,
    N8NErrorDTO,
    SampleSelectionDTO,
    RegenerateSamplesRequestDTO,
    GenerationJobParameters
)
from ...domain.models.generation_request import GenerationRequest
from ...domain.models.generation_status import GenerationStatus
from ...domain.repositories.generation_request_repository import IGenerationRequestRepository
from ...infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from .credit_service_client import CreditServiceClient
from .notification_service_client import NotificationServiceClient
from ...core.config import Settings
from ...core.error_handlers import (
    GenerationJobPublishError, 
    GenerationRequestNotFoundError, 
    InvalidGenerationStateError
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

    async def initiate_generation(self, request_data: GenerationRequestCreateDTO) -> GenerationRequest:
        logger.info(f"Initiating generation for user {request_data.user_id}")
        
        # 1. Credit/Subscription Check
        # As per REQ-016, sample generation costs 0.25 credits
        required_credits_for_sample = 0.25
        await self._credit_service_client.check_credits(request_data.user_id, required_credits_for_sample)
        
        # 2. Create GenerationRequest Record
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            status=GenerationStatus.VALIDATING_CREDITS,
            input_parameters=request_data.dict(exclude={'user_id', 'project_id'}),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            credits_cost_sample=required_credits_for_sample
        )
        await self._repo.add(new_request)
        logger.info(f"Created generation request record {new_request.id}")

        # 3. Deduct Credits
        await self._credit_service_client.deduct_credits(
            user_id=new_request.user_id,
            request_id=new_request.id,
            amount=required_credits_for_sample,
            action_type="sample_generation_fee"
        )
        new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        await self._repo.update(new_request)
        
        # 4. Prepare and Publish n8n Job Payload
        job_payload = self._prepare_n8n_job_payload(new_request, "sample_generation")
        try:
            await self._rabbitmq_publisher.publish_generation_job(
                job_payload=json.loads(job_payload.json()), # Convert Pydantic model to dict then to JSON string
                routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE
            )
        except Exception as e:
            logger.error(f"Failed to publish job for request {new_request.id}: {e}", exc_info=True)
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to publish job to queue.")
            await self._repo.update(new_request)
            # Attempt to refund credits
            await self._credit_service_client.refund_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=required_credits_for_sample,
                reason="System error: Failed to queue generation job"
            )
            raise GenerationJobPublishError(f"Failed to publish job for request {new_request.id}")

        # 5. Update Status
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        logger.info(f"Successfully published job and updated status for request {new_request.id}")

        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFoundError(f"Generation request with ID {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultDTO) -> None:
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logger.error(f"Received sample callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.update_status(GenerationStatus.AWAITING_SELECTION)
        request.sample_asset_infos = [sample.dict() for sample in callback_data.samples]
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(callback_data.samples)} samples.")

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

        request.update_status(GenerationStatus.COMPLETED)
        request.final_asset_info = callback_data.final_asset.dict()
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to COMPLETED.")

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
        status = GenerationStatus.FAILED
        # Example: a specific error code for content policy violations
        if error_data.error_code == "CONTENT_POLICY_VIOLATION":
            status = GenerationStatus.CONTENT_REJECTED
        
        request.update_status(status, error_message=error_message)
        request.error_details = error_data.error_details
        
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for request {request.id}: {error_data.error_details}")

        # Credit Refund Logic
        # For simplicity, assume any error that is not CONTENT_REJECTED is a system error
        is_system_error = status != GenerationStatus.CONTENT_REJECTED
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            credits_to_refund = 0
            if error_data.failed_stage == "sample_processing" and request.credits_cost_sample:
                credits_to_refund = request.credits_cost_sample
            elif error_data.failed_stage == "final_processing" and request.credits_cost_final:
                credits_to_refund = request.credits_cost_final

            if credits_to_refund > 0:
                logger.info(f"Attempting to refund {credits_to_refund} credits for failed request {request.id}")
                await self._credit_service_client.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=credits_to_refund,
                    reason=f"System error during AI generation stage: {error_data.failed_stage}"
                )
        
        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(self, request_id: UUID, regeneration_data: RegenerateSamplesRequestDTO) -> GenerationRequest:
        request = await self._get_and_validate_request(request_id, regeneration_data.user_id)
        
        # Credit Check & Deduction for Regeneration (cost is same as initial)
        cost = request.credits_cost_sample or 0.25
        await self._credit_service_client.check_credits(regeneration_data.user_id, cost)
        await self._credit_service_client.deduct_credits(
            user_id=regeneration_data.user_id,
            request_id=request_id,
            amount=cost,
            action_type="sample_regeneration_fee"
        )
        
        # Update request with new prompt if provided
        if regeneration_data.updated_prompt:
            request.input_prompt = regeneration_data.updated_prompt
            request.input_parameters['input_prompt'] = regeneration_data.updated_prompt
        if regeneration_data.updated_style_guidance:
            request.style_guidance = regeneration_data.updated_style_guidance
            request.input_parameters['style_guidance'] = regeneration_data.updated_style_guidance

        # Prepare and publish job
        job_payload = self._prepare_n8n_job_payload(request, "sample_regeneration")
        await self._rabbitmq_publisher.publish_generation_job(json.loads(job_payload.json()), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)

        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(request)
        return request

    async def select_sample_and_initiate_final(self, request_id: UUID, selection_data: SampleSelectionDTO) -> GenerationRequest:
        request = await self._get_and_validate_request(request_id, selection_data.user_id, required_status=GenerationStatus.AWAITING_SELECTION)
        
        # Validate selected sample ID
        if not any(sample['asset_id'] == selection_data.selected_sample_id for sample in request.sample_asset_infos):
            raise InvalidGenerationStateError(f"Selected sample ID {selection_data.selected_sample_id} not found in request {request_id}.")

        # Credit Check & Deduction (e.g., 1 credit for final generation)
        cost_final = 1.0 
        await self._credit_service_client.check_credits(selection_data.user_id, cost_final)
        await self._credit_service_client.deduct_credits(
            user_id=selection_data.user_id,
            request_id=request_id,
            amount=cost_final,
            action_type="final_generation_fee"
        )
        request.credits_cost_final = cost_final
        request.selected_sample_id = selection_data.selected_sample_id

        # Prepare and publish job
        job_payload = self._prepare_n8n_job_payload(
            request, 
            "final_generation", 
            extra_params={
                "selected_sample_id": selection_data.selected_sample_id,
                "desired_resolution": selection_data.desired_resolution
            }
        )
        await self._rabbitmq_publisher.publish_generation_job(json.loads(job_payload.json()), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)

        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        return request

    async def _get_and_validate_request(self, request_id: UUID, user_id: str, required_status: GenerationStatus = None) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFoundError(f"Generation request with ID {request_id} not found.")
        if request.user_id != user_id:
            # In a real system, this would be a 403 Forbidden, but for simplicity we raise 404.
            raise GenerationRequestNotFoundError(f"Generation request with ID {request_id} not found for this user.")
        if required_status and request.status != required_status:
            raise InvalidGenerationStateError(f"Operation not allowed on request {request_id} with status '{request.status.value}'. Required status: '{required_status.value}'.")
        return request

    def _prepare_n8n_job_payload(self, request: GenerationRequest, job_type: str, extra_params: dict = None) -> GenerationJobParameters:
        callback_base = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR
        
        payload_data = {
            "generation_request_id": request.id,
            "user_id": request.user_id,
            "project_id": request.project_id,
            "job_type": job_type,
            "callback_url_error": f"{callback_base}{api_prefix}/n8n-callbacks/error",
            **request.input_parameters
        }

        if job_type in ["sample_generation", "sample_regeneration"]:
             payload_data["callback_url_sample_result"] = f"{callback_base}{api_prefix}/n8n-callbacks/sample-result"

        if job_type == "final_generation":
             payload_data["callback_url_final_result"] = f"{callback_base}{api_prefix}/n8n-callbacks/final-result"

        if extra_params:
            payload_data.update(extra_params)
            
        return GenerationJobParameters(**payload_data)