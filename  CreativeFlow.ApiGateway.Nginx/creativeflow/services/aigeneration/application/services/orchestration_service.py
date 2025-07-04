import logging
from uuid import UUID, uuid4
from datetime import datetime
import json

from ..dtos import N8NJobPayloadDTO
from ..domain.repositories.generation_request_repository import IGenerationRequestRepository
from ..infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from .credit_service_client import CreditServiceClient
from .notification_service_client import NotificationServiceClient
from ..domain.models.generation_request import GenerationRequest
from ..domain.models.generation_status import GenerationStatus
from ..domain.models.asset_info import AssetInfo
from ..api.v1.schemas import (
    GenerationRequestCreate,
    N8NSampleResultPayload,
    N8NFinalResultPayload,
    N8NErrorPayload,
)
from ...core.config import Settings
from ...core.error_handlers import (
    InsufficientCreditsError,
    GenerationRequestNotFound,
    InvalidGenerationStateError,
    GenerationJobPublishError,
)

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

    async def initiate_generation(self, request_data: GenerationRequestCreate) -> GenerationRequest:
        # 1. Credit Check
        required_credits_sample = 0.25 # As per REQ-016
        # In a real scenario, this could be dynamic based on request parameters
        # For now, we'll assume a fixed cost for sample generation.
        
        await self._credit_service_client.check_credits(request_data.user_id, required_credits_sample)
        
        # 2. Create Initial DB Record
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            status=GenerationStatus.PENDING,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            # Store all input params in a structured way
            input_parameters={
                "output_format": request_data.output_format,
                "custom_dimensions": request_data.custom_dimensions.dict() if request_data.custom_dimensions else None,
                "brand_kit_id": request_data.brand_kit_id,
                "uploaded_image_references": request_data.uploaded_image_references,
                "target_platform_hints": request_data.target_platform_hints,
                "emotional_tone": request_data.emotional_tone,
                "cultural_adaptation_parameters": request_data.cultural_adaptation_parameters
            },
            credits_cost_sample=required_credits_sample,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        new_request.update_status(GenerationStatus.VALIDATING_CREDITS)
        await self._repo.add(new_request)

        # 3. Deduct Credits
        try:
            await self._credit_service_client.deduct_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=required_credits_sample,
                action_type="sample_generation_fee"
            )
        except InsufficientCreditsError as e:
            new_request.update_status(GenerationStatus.FAILED, "Insufficient credits during deduction.")
            await self._repo.update(new_request)
            raise e

        # 4. Prepare and Publish Job
        new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        await self._repo.update(new_request)

        job_payload = self._prepare_n8n_job_payload(new_request, "sample_generation")
        
        try:
            await self._rabbitmq_publisher.publish_generation_job(
                job_payload=job_payload.dict(),
                routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE,
            )
        except Exception as e:
            logging.exception("Failed to publish job to RabbitMQ.")
            new_request.update_status(GenerationStatus.FAILED, "Failed to queue generation job.")
            await self._repo.update(new_request)
            # Attempt to refund credits on publishing failure
            await self._credit_service_client.refund_credits(
                user_id=new_request.user_id,
                request_id=new_request.id,
                amount=required_credits_sample,
                reason="System error: Failed to publish job to queue."
            )
            raise GenerationJobPublishError() from e

        # 5. Final Status Update
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        
        logging.info(f"Successfully initiated generation request {new_request.id}")
        return await self._repo.get_by_id(new_request.id)

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFound()
        return request

    async def process_n8n_sample_callback(self, callback_data: N8NSampleResultPayload) -> None:
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logging.error(f"Received n8n callback for non-existent request ID: {callback_data.generation_request_id}")
            return

        request.update_status(GenerationStatus.AWAITING_SELECTION)
        for sample_data in callback_data.samples:
            asset_info = AssetInfo(**sample_data.dict())
            request.add_sample_result(asset_info)
        
        await self._repo.update(request)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )
        logging.info(f"Processed sample callback for request {request.id}. Status: AWAITING_SELECTION")

    async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultPayload) -> None:
        request = await self._repo.get_by_id(callback_data.generation_request_id)
        if not request:
            logging.error(f"Received n8n callback for non-existent request ID: {callback_data.generation_request_id}")
            return
            
        request.update_status(GenerationStatus.COMPLETED)
        final_asset_info = AssetInfo(**callback_data.final_asset.dict())
        request.set_final_asset(final_asset_info)
        
        await self._repo.update(request)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": final_asset_info.url}
        )
        logging.info(f"Processed final asset callback for request {request.id}. Status: COMPLETED")

    async def handle_n8n_error(self, error_data: N8NErrorPayload) -> None:
        request = await self._repo.get_by_id(error_data.generation_request_id)
        if not request:
            logging.error(f"Received n8n error callback for non-existent request ID: {error_data.generation_request_id}")
            return

        error_message = error_data.error_message
        status = GenerationStatus.FAILED
        if error_data.error_code == "CONTENT_POLICY_VIOLATION":
            status = GenerationStatus.CONTENT_REJECTED
            error_message = "Generation failed due to content policy violation."

        request.update_status(status, error_message)
        request.error_details = error_data.error_details if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING else None
        
        # Credit Refund Logic
        # Assuming system errors don't have specific error codes like "CONTENT_POLICY_VIOLATION"
        is_system_error = error_data.error_code not in ["CONTENT_POLICY_VIOLATION", "USER_INPUT_ERROR"]
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            credits_to_refund = 0
            if error_data.failed_stage == "sample_processing":
                credits_to_refund = request.credits_cost_sample or 0
            elif error_data.failed_stage == "final_processing":
                credits_to_refund = request.credits_cost_final or 0
            
            if credits_to_refund > 0:
                logging.info(f"Attempting to refund {credits_to_refund} credits for failed request {request.id}")
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
        logging.warning(f"Processed error callback for request {request.id}. Status: {status.value}")

    async def trigger_sample_regeneration(
        self, request_id: UUID, user_id: str, updated_prompt: str = None, updated_style_guidance: str = None
    ) -> GenerationRequest:
        request = await self._get_and_validate_request(request_id, user_id, [GenerationStatus.AWAITING_SELECTION, GenerationStatus.FAILED])
        
        # Credit check & deduction for regeneration
        regen_cost = 0.25 # Same as initial sample cost
        await self._credit_service_client.check_credits(user_id, regen_cost)
        await self._credit_service_client.deduct_credits(user_id, request_id, regen_cost, "sample_regeneration_fee")
        
        # Update request
        request.credits_cost_sample += regen_cost
        if updated_prompt:
            request.input_prompt = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
            
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        request.sample_asset_infos = [] # Clear old samples
        await self._repo.update(request)
        
        # Publish job
        job_payload = self._prepare_n8n_job_payload(request, "sample_regeneration")
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict(), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)

        logging.info(f"Triggered sample regeneration for request {request.id}")
        return await self._repo.get_by_id(request.id)

    async def select_sample_and_initiate_final(
        self, request_id: UUID, selected_sample_id: str, user_id: str, desired_resolution: str = None
    ) -> GenerationRequest:
        request = await self._get_and_validate_request(request_id, user_id, [GenerationStatus.AWAITING_SELECTION])

        if not any(s.asset_id == selected_sample_id for s in request.sample_asset_infos):
            raise InvalidGenerationStateError("Selected sample ID is not valid for this request.")

        # Credit check & deduction for final generation
        final_cost = 1.0 # Base cost for final generation
        if desired_resolution and desired_resolution.lower() in ['4k', '4096x4096']:
            final_cost = 2.0
        
        await self._credit_service_client.check_credits(user_id, final_cost)
        await self._credit_service_client.deduct_credits(user_id, request_id, final_cost, "final_generation_fee")
        
        # Update request
        request.credits_cost_final = final_cost
        request.set_selected_sample(selected_sample_id)
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        await self._repo.update(request)

        # Publish job
        job_payload = self._prepare_n8n_job_payload(request, "final_generation", {"desired_resolution": desired_resolution})
        await self._rabbitmq_publisher.publish_generation_job(job_payload.dict(), self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY, self._settings.RABBITMQ_GENERATION_EXCHANGE)

        logging.info(f"Initiated final generation for request {request.id} with sample {selected_sample_id}")
        return await self._repo.get_by_id(request.id)

    def _prepare_n8n_job_payload(self, request: GenerationRequest, job_type: str, extra_params: dict = None) -> N8NJobPayloadDTO:
        """Helper to construct the payload for n8n."""
        if extra_params is None:
            extra_params = {}
            
        base_url = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR
        
        return N8NJobPayloadDTO(
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
            selected_sample_id=request.selected_sample_id,
            job_type=job_type,
            callback_url_sample_result=f"{base_url}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{base_url}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{base_url}{api_prefix}/n8n-callbacks/error",
            **extra_params
        )

    async def _get_and_validate_request(self, request_id: UUID, user_id: str, allowed_statuses: list[GenerationStatus]) -> GenerationRequest:
        """Helper to fetch a request and validate its ownership and status."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise GenerationRequestNotFound()
        if request.user_id != user_id:
            # Although user_id is in the payload, this is a server-side check against the record's owner
            raise InvalidGenerationStateError("User is not authorized to perform this action on the request.")
        if request.status not in allowed_statuses:
            raise InvalidGenerationStateError(f"Operation only allowed in states: {[s.value for s in allowed_statuses]}. Current state: {request.status.value}")
        return request