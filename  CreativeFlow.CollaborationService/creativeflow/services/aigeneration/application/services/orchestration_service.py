import json
import logging
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from creativeflow.services.aigeneration.api.v1 import schemas as api_schemas
from creativeflow.services.aigeneration.application import dtos
from creativeflow.services.aigeneration.application.exceptions import (
    EntityNotFoundError, InvalidStateTransitionError
)
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

    def _get_credit_cost(self, action: str) -> float:
        """Determines credit cost based on action. Stub for now."""
        # REQ-016: This logic will be more complex based on subscription, resolution, etc.
        if action == "sample":
            return 0.25
        if action == "final":
            return 1.0
        if action == "regeneration":
            return 0.25
        return 0.0

    async def initiate_generation(self, request_data: api_schemas.GenerationRequestCreate) -> GenerationRequest:
        """Orchestrates the initiation of a new generation request."""
        logger.info("Initiating generation for user %s", request_data.user_id)

        # 1. Credit Check
        required_credits = self._get_credit_cost("sample")
        # In a real scenario, we might check subscription tier first to see if credits are needed
        await self._credit_service_client.check_credits(request_data.user_id, required_credits)

        # 2. Create and persist GenerationRequest record
        new_request = GenerationRequest(
            id=uuid4(),
            user_id=request_data.user_id,
            project_id=request_data.project_id,
            input_prompt=request_data.input_prompt,
            style_guidance=request_data.style_guidance,
            status=GenerationStatus.PENDING,
            input_parameters=request_data.dict(exclude={"user_id", "project_id"}), # store all inputs
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await self._repo.add(new_request)
        logger.debug("Created initial generation request record %s", new_request.id)

        # 3. Deduct Credits
        new_request.update_status(GenerationStatus.VALIDATING_CREDITS)
        await self._credit_service_client.deduct_credits(
            user_id=new_request.user_id,
            request_id=new_request.id,
            amount=required_credits,
            action_type="sample_generation"
        )
        new_request.set_credits_cost(sample_cost=required_credits)
        await self._repo.update(new_request)

        # 4. Prepare and Publish Job
        new_request.update_status(GenerationStatus.PUBLISHING_TO_QUEUE)
        callback_base = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR
        
        job_payload = dtos.GenerationJobParameters(
            generation_request_id=new_request.id,
            user_id=new_request.user_id,
            project_id=new_request.project_id,
            input_prompt=new_request.input_prompt,
            style_guidance=new_request.style_guidance,
            output_format=request_data.output_format,
            custom_dimensions=request_data.custom_dimensions,
            brand_kit_id=request_data.brand_kit_id,
            uploaded_image_references=request_data.uploaded_image_references,
            target_platform_hints=request_data.target_platform_hints,
            emotional_tone=request_data.emotional_tone,
            cultural_adaptation_parameters=request_data.cultural_adaptation_parameters,
            job_type="sample_generation",
            callback_url_sample_result=f"{callback_base}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{callback_base}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{callback_base}{api_prefix}/n8n-callbacks/error",
        )
        
        self._rabbitmq_publisher.publish_generation_job(
            job_payload=json.loads(job_payload.json()),
            routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
            exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE
        )
        logger.info("Published sample generation job for request %s", new_request.id)

        # 5. Update Status and return
        new_request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        await self._repo.update(new_request)
        
        return new_request

    async def get_generation_status(self, request_id: UUID) -> GenerationRequest:
        """Fetches a generation request by its ID."""
        request = await self._repo.get_by_id(request_id)
        if not request:
            raise EntityNotFoundError(f"Generation request with ID {request_id} not found.")
        return request

    async def process_n8n_sample_callback(self, callback_data: api_schemas.N8NSampleResultPayload) -> None:
        """Processes the callback from n8n after sample generation."""
        request = await self.get_generation_status(callback_data.generation_request_id)
        
        request.update_status(GenerationStatus.AWAITING_SELECTION)
        for sample_info in callback_data.samples:
            request.add_sample_result(sample_info.dict())
            
        await self._repo.update(request)
        logger.info("Request %s updated to AWAITING_SELECTION with %d samples.", request.id, len(callback_data.samples))

        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="samples_ready",
            message="Your AI creative samples are ready for review!",
            payload={"request_id": str(request.id)}
        )

    async def process_n8n_final_asset_callback(self, callback_data: api_schemas.N8NFinalResultPayload) -> None:
        """Processes the callback from n8n after final asset generation."""
        request = await self.get_generation_status(callback_data.generation_request_id)

        request.update_status(GenerationStatus.COMPLETED)
        request.set_final_asset(callback_data.final_asset.dict())

        await self._repo.update(request)
        logger.info("Request %s updated to COMPLETED.", request.id)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="final_asset_ready",
            message="Your final AI creative is ready!",
            payload={"request_id": str(request.id), "asset_url": callback_data.final_asset.url}
        )

    async def handle_n8n_error(self, error_data: api_schemas.N8NErrorPayload) -> None:
        """Handles an error callback from n8n."""
        request = await self.get_generation_status(error_data.generation_request_id)

        is_system_error = "content" not in (error_data.error_code or "").lower()
        new_status = GenerationStatus.FAILED if is_system_error else GenerationStatus.CONTENT_REJECTED
        request.update_status(new_status, error_message=error_data.error_message)
        request.input_parameters['error_details'] = error_data.dict(exclude={'generation_request_id'})
        
        if self._settings.ENABLE_DETAILED_N8N_ERROR_LOGGING:
            logger.error("Detailed n8n error for request %s: %s", request.id, error_data.error_details)
        
        # Credit Refund Logic
        if is_system_error and self._settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE:
            amount_to_refund = 0
            failed_stage = error_data.failed_stage or ""
            if "sample" in failed_stage and request.credits_cost_sample:
                amount_to_refund = request.credits_cost_sample
            elif "final" in failed_stage and request.credits_cost_final:
                amount_to_refund = request.credits_cost_final
            
            if amount_to_refund > 0:
                logger.info("Attempting to refund %f credits for request %s due to system error.", amount_to_refund, request.id)
                await self._credit_service_client.refund_credits(
                    user_id=request.user_id,
                    request_id=request.id,
                    amount=amount_to_refund,
                    reason=f"System error during AI generation stage: {failed_stage}"
                )

        await self._repo.update(request)
        
        await self._notification_client.send_notification(
            user_id=request.user_id,
            notification_type="generation_failed",
            message=f"AI generation failed: {error_data.error_message}",
            payload={"request_id": str(request.id)}
        )

    async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str], updated_style_guidance: Optional[str]) -> GenerationRequest:
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
             raise EntityNotFoundError("Request not found for this user.")

        required_credits = self._get_credit_cost("regeneration")
        await self._credit_service_client.check_credits(user_id, required_credits)
        await self._credit_service_client.deduct_credits(
            user_id=user_id,
            request_id=request_id,
            amount=required_credits,
            action_type="sample_regeneration"
        )
        
        # Update prompt if provided
        if updated_prompt:
            request.input_prompt = updated_prompt
            request.input_parameters['input_prompt'] = updated_prompt
        if updated_style_guidance:
            request.style_guidance = updated_style_guidance
            request.input_parameters['style_guidance'] = updated_style_guidance

        # Prepare and publish job
        callback_base = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR
        
        job_payload = dtos.GenerationJobParameters(
            generation_request_id=request.id,
            user_id=request.user_id,
            project_id=request.project_id,
            input_prompt=request.input_prompt,
            style_guidance=request.style_guidance,
            # Reuse other params from original request
            **request.input_parameters,
            job_type="sample_regeneration",
            callback_url_sample_result=f"{callback_base}{api_prefix}/n8n-callbacks/sample-result",
            callback_url_final_result=f"{callback_base}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{callback_base}{api_prefix}/n8n-callbacks/error",
        )

        self._rabbitmq_publisher.publish_generation_job(
            job_payload=json.loads(job_payload.json(exclude_none=True)),
            routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
            exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE
        )
        
        request.update_status(GenerationStatus.PROCESSING_SAMPLES)
        request.set_credits_cost(sample_cost=request.credits_cost_sample + required_credits) # Cumulative
        await self._repo.update(request)
        return request

    async def select_sample_and_initiate_final(self, request_id: UUID, user_id: str, selected_sample_id: str, desired_resolution: Optional[str]) -> GenerationRequest:
        request = await self.get_generation_status(request_id)
        if request.user_id != user_id:
             raise EntityNotFoundError("Request not found for this user.")
        if request.status != GenerationStatus.AWAITING_SELECTION:
            raise InvalidStateTransitionError(f"Cannot select sample for request in '{request.status.value}' state.")
        if not any(s['asset_id'] == selected_sample_id for s in request.sample_asset_infos):
            raise EntityNotFoundError(f"Sample with ID {selected_sample_id} not found in this request.")

        required_credits = self._get_credit_cost("final")
        await self._credit_service_client.check_credits(user_id, required_credits)
        await self._credit_service_client.deduct_credits(
            user_id=user_id,
            request_id=request_id,
            amount=required_credits,
            action_type="final_generation"
        )

        # Prepare and publish job
        callback_base = self._settings.N8N_CALLBACK_BASE_URL
        api_prefix = self._settings.API_V1_STR

        job_payload = dtos.GenerationJobParameters(
            generation_request_id=request.id,
            user_id=request.user_id,
            project_id=request.project_id,
            input_prompt=request.input_prompt,
            # Pass only necessary params for final generation
            **request.input_parameters,
            job_type="final_generation",
            selected_sample_id=selected_sample_id,
            desired_resolution=desired_resolution,
            callback_url_sample_result="", # Not used
            callback_url_final_result=f"{callback_base}{api_prefix}/n8n-callbacks/final-result",
            callback_url_error=f"{callback_base}{api_prefix}/n8n-callbacks/error",
        )

        self._rabbitmq_publisher.publish_generation_job(
            job_payload=json.loads(job_payload.json(exclude_none=True)),
            routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
            exchange_name=self._settings.RABBITMQ_GENERATION_EXCHANGE
        )

        request.set_selected_sample(selected_sample_id)
        request.update_status(GenerationStatus.PROCESSING_FINAL)
        request.set_credits_cost(final_cost=required_credits)
        await self._repo.update(request)
        return request