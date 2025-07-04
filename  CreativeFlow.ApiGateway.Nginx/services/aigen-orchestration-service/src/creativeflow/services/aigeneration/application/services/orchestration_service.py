import json
import logging
from uuid import UUID
from decimal import Decimal

from creativeflow.services.aigeneration.api.v1.schemas import GenerationRequestCreate, SampleSelection, RegenerateSamplesRequest
from creativeflow.services.aigeneration.application.dtos import GenerationJobParameters, N8NSampleResultDTO, N8NFinalResultDTO, N8NErrorDTO
from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.core.error_handlers import InsufficientCreditsError, ResourceNotFoundError, InvalidStateError, GenerationJobPublishError, CreditDeductionError
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest, AssetInfo
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient

logger = logging.getLogger(__name__)

# Define credit costs as per REQ-016
CREDIT_COST_SAMPLE_GENERATION = Decimal("0.25")
CREDIT_COST_FINAL_GENERATION_DEFAULT = Decimal("1.0")
CREDIT_COST_FINAL_GENERATION_HIGH_RES = Decimal("2.0")

class OrchestrationService:
    """Contains the core business logic for the AI generation pipeline."""

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
        self._credit_service_client = credit_service_client
        self._notification_client = notification_client
        self._settings = settings

    async def initiate_generation(self, request_data: GenerationRequestCreate) -> GenerationRequest:
        """Orchestrates the initiation of a new AI generation request."""
        logger.info(f"Initiating generation for user '{request_data.user_id}'.")
        
        # 1. Credit Check
        required_credits = CREDIT_COST_SAMPLE_GENERATION
        await self._credit_service_client.check_credits(request_data.user_id, float(required_credits))
        
        # 2. Create GenerationRequest Record in DB
        new_request = GenerationRequest(
            **request_data.dict(),
            status=GenerationStatus.VALIDATING_CREDITS
        )
        await self._repo.add(new_request)
        logger.info(f"Created generation request record {new_request.id} with status PENDING.")

        try:
            # 3. Deduct Credits
            await self._credit_service_client.deduct_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=float(required_credits),
                action_type="sample_generation_fee"
            )
            new_request.credits_cost_sample = required_credits
            new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
            await self._repo.update(new_request)

            # 4. Prepare and Publish n8n Job
            job_payload = self._prepare_n8n_job_payload(new_request, "sample_generation")
            self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
            logger.info(f"Published sample generation job for request {new_request.id} to RabbitMQ.")

            # 5. Final Status Update
            new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
            await self._repo.update(new_request)

            return new_request

        except (InsufficientCreditsError, CreditDeductionError) as e:
            logger.error(f"Credit error for request {new_request.id}: {e}")
            new_request.update_status(GenerationStatus.FAILED, error_message=str(e))
            await self._repo.update(new_request)
            # Re-raise to be caught by the API layer
            raise e
        except GenerationJobPublishError as e:
            logger.error(f"Failed to publish job for request {new_request.id}: {e}")
            new_request.update_status(GenerationStatus.FAILED, error_message="Failed to queue generation job.")
            await self._repo.update(new_request)
            # Attempt to refund credits for this system failure
            await self._credit_service_client.refund_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=float(required_credits),
                reason="System error: failed to publish job to queue."
            )
            raise e

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Retrieves a generation request by its ID."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise ResourceNotFoundError(f"Generation request with ID '{request_id}' not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultDTO) -> None:
        """Processes the successful sample generation callback from n8n."""
        request = await self._get_request_or_log_error(callback_data.generation_request_id)
        if not request:
            return

        request.update_status(GenerationStatus.AWAITING_SELECTION)
        request.sample_asset_infos = [AssetInfo(**sample.dict()) for sample in callback_data.samples]
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to AWAITING_SELECTION with {len(request.sample_asset_infos)} samples.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultDTO) -> None:
        """Processes the successful final asset generation callback from n8n."""
        request = await self._get_request_or_log_error(callback_data.generation_request_id)
        if not request:
            return

        request.update_status(GenerationStatus.COMPLETED)
        request.final_asset_info = AssetInfo(**callback_data.final_asset.dict())
        
        await self._repo.update(request)
        logger.info(f"Request {request.id} updated to COMPLETED.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={
                "request_id": str(request.id),
                "asset_url": request.final_asset_info.url
            }
        )
    
    async def handle_n8n_error(self, error_data: N8NErrorDTO) -> None:
        """Handles an error callback from n8n."""
        request = await self._get_request_or_log_error(error_data.generation_request_id)
        if not request:
            return

        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error(f"Detailed n8n error for {request.id}: {json.dumps(error_data.dict())}")

        # Determine error type and update status
        is_content_rejection = "content" in (error_data.error_code or "").lower()
        new_status = GenerationStatus.CONTENT_REJECTED if is_content_rejection else GenerationStatus.FAILED
        request.update_status(new_status, error_message=error_data.error_message)
        
        # Credit Refund Logic
        if self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE and not is_content_rejection:
            failed_stage = error_data.failed_stage or ""
            amount_to_refund = 0.0
            
            if "sample" in failed_stage and request.credits_cost_sample:
                amount_to_refund = float(request.credits_cost_sample)
            elif "final" in failed_stage and request.credits_cost_final:
                amount_to_refund = float(request.credits_cost_final)

            if amount_to_refund > 0:
                await self._credit_service_client.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=amount_to_refund,
                    reason=f"System error during AI generation stage: {failed_stage}"
                )

        await self._repo.update(request)
        logger.warning(f"Request {request.id} marked as {new_status.value} due to n8n error.")

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            payload={"request_id": str(request.id)}
        )

    async def select_sample_and_initiate_final(self, request_id: UUID, selection_data: SampleSelection) -> GenerationRequest:
        """Orchestrates selecting a sample and starting the final generation."""
        request = await self.get_generation_status(request_id)

        if request.user_id != selection_data.user_id:
            raise InvalidStateError("User does not have permission for this request.")
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidStateError(f"Request is not awaiting sample selection (status: {request.status.value}).")
        if not any(s.asset_id == selection_data.selected_sample_id for s in request.sample_asset_infos or []):
            raise InvalidStateError("Selected sample ID is not valid for this request.")

        # Determine credit cost and perform check/deduction
        required_credits = CREDIT_COST_FINAL_GENERATION_HIGH_RES if selection_data.desired_resolution else CREDIT_COST_FINAL_GENERATION_DEFAULT
        await self._credit_service_client.check_credits(request.user_id, float(required_credits))
        
        await self._credit_service_client.deduct_credits(
            user_id=request.user_id,
            request_id=request.id,
            amount=float(required_credits),
            action_type="final_generation_fee"
        )

        request.selected_sample_id = selection_data.selected_sample_id
        request.credits_cost_final = required_credits
        request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        await self._repo.update(request)
        
        # Prepare and publish job
        job_payload = self._prepare_n8n_job_payload(
            request, 
            "final_generation", 
            extra_params={"desired_resolution": selection_data.desired_resolution}
        )
        self._rabbitmq_publisher.publish_generation_job(job_payload.dict())

        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)
        logger.info(f"Published final generation job for request {request.id}.")
        return request

    async def trigger_sample_regeneration(self, request_id: UUID, regeneration_data: RegenerateSamplesRequest) -> GenerationRequest:
        """Orchestrates triggering a regeneration of samples."""
        request = await self.get_generation_status(request_id)

        if request.user_id != regeneration_data.user_id:
            raise InvalidStateError("User does not have permission for this request.")
        
        # Check credits (cost is same as initial sample generation)
        required_credits = CREDIT_COST_SAMPLE_GENERATION
        await self._credit_service_client.check_credits(request.user_id, float(required_credits))
        await self._credit_service_client.deduct_credits(
            user_id=request.user_id,
            request_id=request.id,
            amount=float(required_credits),
            action_type="sample_regeneration_fee"
        )
        
        # Update request with new prompt if provided
        if regeneration_data.updated_prompt:
            request.input_prompt = regeneration_data.updated_prompt
        if regeneration_data.updated_style_guidance:
            request.style_guidance = regeneration_data.updated_style_guidance

        # Add to existing credit cost
        request.credits_cost_sample = (request.credits_cost_sample or 0) + required_credits

        # Publish job
        job_payload = self._prepare_n8n_job_payload(request, "sample_regeneration")
        self._rabbitmq_publisher.publish_generation_job(job_payload.dict())
        
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        # Clear previous samples
        request.sample_asset_infos = []
        request.selected_sample_id = None
        await self._repo.update(request)
        logger.info(f"Published sample regeneration job for request {request.id}.")
        return request

    async def _get_request_or_log_error(self, request_id: UUID) -> GenerationRequest | None:
        """Helper to fetch a request and log an error if not found."""
        try:
            return await self.get_generation_status(request_id)
        except ResourceNotFoundError:
            logger.error(f"Received a callback for a non-existent generation request ID: {request_id}")
            return None

    def _prepare_n8n_job_payload(
        self,
        request: GenerationRequest,
        job_type: str,
        extra_params: dict = None
    ) -> GenerationJobParameters:
        """Constructs the JSON payload for an n8n generation job."""
        base_url = str(self._settings.N8N_CALLBACK_BASE_URL).rstrip("/")
        api_prefix = self._settings.API_V1_STR
        callback_base = f"{base_url}{api_prefix}/n8n-callbacks"

        payload_data = request.dict(exclude={'id'})
        payload_data.update({
            "generation_request_id": request.id,
            "job_type": job_type,
            "callback_url_sample_result": f"{callback_base}/sample-result",
            "callback_url_final_result": f"{callback_base}/final-result",
            "callback_url_error": f"{callback_base}/error",
        })
        if extra_params:
            payload_data.update(extra_params)
            
        return GenerationJobParameters(**payload_data)