import logging
from uuid import UUID, uuid4
from typing import Optional
from decimal import Decimal

from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.application.dtos import GenerationJobParameters, NotificationRequestDTO
from creativeflow.services.aigeneration.core.error_handlers import GenerationRequestNotFound, InvalidGenerationState, GenerationJobPublishError

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
        settings: Settings
    ):
        self._repo = repo
        self._rabbitmq_publisher = rabbitmq_publisher
        self._credit_service = credit_service_client
        self._notification_client = notification_client
        self._settings = settings

    async def initiate_generation(self, request_data: schemas.GenerationRequestCreate) -> GenerationRequest:
        """Orchestrates the initiation of a new generation request."""
        logger.info(f"Initiating generation for user {request_data.user_id}")

        # 1. Credit Check
        cost = Decimal(self._settings.CREDIT_COST_SAMPLE)
        # TODO: Add logic to check subscription tier and potentially waive cost
        # tier = await self._credit_service.get_user_subscription_tier(request_data.user_id)
        # if tier_allows_free_samples: cost = 0

        await self._credit_service.check_credits(request_data.user_id, float(cost))

        # 2. Create DB record
        new_request = GenerationRequest.create(
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            # Store all input params for potential regeneration
            input_parameters=request_data.dict(exclude={'user_id', 'project_id'})
        )
        new_request.update_status(GenerationStatus.VALIDATING_CREDITS)
        await self._repo.add(new_request)
        logger.info(f"Created GenerationRequest record {new_request.id}")

        # 3. Deduct Credits
        await self._credit_service.deduct_credits(request_data.user_id, new_request.id, float(cost), "sample_generation_fee")
        new_request.credits_cost_sample = cost
        
        # 4. Prepare and Publish Job
        new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        await self._repo.update(new_request)

        job_payload = self._prepare_job_payload(new_request, "sample_generation")
        self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        logger.info(f"Published job {new_request.id} to RabbitMQ.")

        # 5. Final status update
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)

        return new_request
    
    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Fetches a generation request by its ID."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFound(f"Request with id {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: schemas.N8NSampleResultPayload):
        """Processes successful sample generation callback from n8n."""
        request = await self.get_generation_status(callback_data.generation_request_id)
        
        request.add_sample_results([s.dict() for s in callback_data.samples])
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(callback_data.samples)} samples.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: schemas.N8NFinalResultPayload):
        """Processes successful final asset generation callback from n8n."""
        request = await self.get_generation_status(callback_data.generation_request_id)
        
        request.set_final_asset(callback_data.final_asset.dict())
        request.update_status(GenerationStatus.COMPLETED)
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to COMPLETED.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )

    async def handle_n8n_error(self, error_data: schemas.N8NErrorPayload):
        """Handles error callbacks from n8n."""
        request = await self.get_generation_status(error_data.generation_request_id)
        
        # Determine new status
        new_status = GenerationStatus.FAILED
        if error_data.error_code == "CONTENT_POLICY_VIOLATION":
            new_status = GenerationStatus.CONTENT_REJECTED
        
        request.update_status(new_status, error_message=error_data.error_message)
        # In a real app, error_details could be stored in a separate field or table.
        
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for request {request.id}: {error_data.error_details}")
            
        # Refund logic
        is_system_error = new_status == GenerationStatus.FAILED # Simple assumption
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            amount_to_refund = 0.0
            if error_data.failed_stage == 'sample_processing' and request.credits_cost_sample:
                amount_to_refund = float(request.credits_cost_sample)
            elif error_data.failed_stage == 'final_processing' and request.credits_cost_final:
                amount_to_refund = float(request.credits_cost_final)
            
            if amount_to_refund > 0:
                await self._credit_service.refund_credits(
                    request.user_id, request.id, amount_to_refund,
                    "System error during AI generation"
                )
        
        await self._repo.update(request)
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]) -> GenerationRequest:
        """Orchestrates the regeneration of samples."""
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            raise GenerationRequestNotFound() # Obscure the reason for security

        # 1. Credit Check & Deduction
        cost = Decimal(self._settings.CREDIT_COST_REGENERATION)
        await self._credit_service.deduct_credits(user_id, request_id, float(cost), "sample_regeneration_fee")
        request.credits_cost_sample = (request.credits_cost_sample or 0) + cost
        
        # 2. Update prompt if provided
        if updated_prompt:
            request.input_prompt = updated_prompt
            request.input_parameters['input_prompt'] = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
            request.input_parameters['style_guidance'] = updated_style_guidance

        # 3. Prepare and Publish Job
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        job_payload = self._prepare_job_payload(request, "sample_regeneration")
        self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        await self._repo.update(request)
        
        logger.info(f"Published regeneration job for request {request.id}")
        return request

    async def select_sample_and_initiate_final(self, request_id: UUID, user_id: str, selected_sample_id: str, desired_resolution: Optional[str]) -> GenerationRequest:
        """Orchestrates the final asset generation from a selected sample."""
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
            raise GenerationRequestNotFound()
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidGenerationState("Request is not awaiting sample selection.")
        if not any(s['asset_id'] == selected_sample_id for s in request.sample_asset_infos):
            raise ValueError(f"Sample ID {selected_sample_id} not found in this request.")
            
        # 1. Credit Check & Deduction
        # Example logic for cost based on resolution
        cost = Decimal(self._settings.CREDIT_COST_FINAL_HD if desired_resolution == '4K' else self._settings.CREDIT_COST_FINAL_SD)
        await self._credit_service.deduct_credits(user_id, request_id, float(cost), "final_generation_fee")
        request.credits_cost_final = cost

        # 2. Update request and prepare job
        request.set_selected_sample(selected_sample_id)
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        
        job_payload = self._prepare_job_payload(request, "final_generation", desired_resolution=desired_resolution)
        self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        
        await self._repo.update(request)
        logger.info(f"Published final generation job for request {request.id}")
        return request

    def _prepare_job_payload(
        self,
        request: GenerationRequest,
        job_type: str,
        desired_resolution: Optional[str] = None
    ) -> GenerationJobParameters:
        """Helper to construct the n8n job payload."""
        base_callback_url = self._settings.N8N_CALLBACK_BASE_URL.rstrip('/')
        api_prefix = self._settings.API_V1_STR
        
        return GenerationJobParameters(
            generation_request_id=request.id,
            user_id=request.user_id,
            project_id=request.project_id,
            job_type=job_type,
            input_prompt=request.input_prompt,
            style_guidance=request.style_guidance,
            # Pass all original parameters back to n8n
            **request.input_parameters,
            callback_url_sample_result=f"{base_callback_url}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{base_callback_url}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{base_callback_url}{api_prefix}/n8n-callbacks/error",
            selected_sample_id=request.selected_sample_id,
            desired_resolution=desired_resolution
        )