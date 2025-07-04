"""
Contains the business logic to process a successful result or failure from an
n8n workflow callback. It updates the job status, coordinates credit deduction,
and triggers user notifications.
"""
import logging
from decimal import Decimal

from ..dtos import N8NCallbackDTO
from ..interfaces import ICreditService, IGenerationRepository, INotificationService

logger = logging.getLogger(__name__)


class GenerationNotFoundError(Exception):
    """Custom exception raised when a generation request is not found."""
    pass


class ProcessN8NResultUseCase:
    """
    Handles the asynchronous results from the n8n workflow engine.
    """

    def __init__(
        self,
        generation_repo: IGenerationRepository,
        notification_service: INotificationService,
        credit_service: ICreditService,
    ):
        self._generation_repo = generation_repo
        self._notification_service = notification_service
        self._credit_service = credit_service

    async def execute(self, payload: N8NCallbackDTO) -> None:
        """
        Executes the use case logic.

        1. Retrieves the GenerationRequest from the database.
        2. Updates the entity's state based on the payload's status (success/failure).
        3. On success, stores asset URLs, triggers credit deduction, and notifies the user.
        4. On failure, logs the error, triggers a credit refund, and notifies the user.

        Args:
            payload: The DTO containing the n8n callback data.

        Raises:
            GenerationNotFoundError: If no generation request matches the payload's ID.
        """
        generation_request = await self._generation_repo.get_by_id(payload.generationId)
        if not generation_request:
            logger.error(f"GenerationRequest with ID {payload.generationId} not found.")
            raise GenerationNotFoundError("Generation request not found.")

        if payload.status == "failure":
            await self._handle_failure(generation_request, payload)
        elif payload.status == "success":
            await self._handle_success(generation_request, payload)

    async def _handle_failure(self, generation_request, payload: N8NCallbackDTO):
        error_message = payload.error.message if payload.error else "Unknown error from n8n."
        logger.warning(f"Generation {generation_request.id} failed. Reason: {error_message}")

        generation_request.mark_as_failed(error_message)
        await self._generation_repo.update(generation_request)

        # Refund any reserved credits
        if generation_request.creditsCostSample:
            await self._credit_service.refund_credits(
                user_id=generation_request.userId,
                generation_id=generation_request.id,
                amount=generation_request.creditsCostSample
            )
            logger.info(f"Refunded {generation_request.creditsCostSample} credits for failed generation {generation_request.id}.")

        # Notify user of failure
        notification_payload = {
            "type": "generation_failed",
            "generationId": str(generation_request.id),
            "message": f"Your creative generation failed: {error_message}"
        }
        await self._notification_service.notify_user(generation_request.userId, notification_payload)

    async def _handle_success(self, generation_request, payload: N8NCallbackDTO):
        logger.info(f"Processing successful callback for generation {generation_request.id} at stage {payload.stage}")

        if payload.stage == "samples_generated":
            sample_assets_data = [asset.dict() for asset in payload.results.sampleAssets]
            generation_request.mark_as_awaiting_selection(sample_assets_data)
            await self._generation_repo.update(generation_request)
            
            # Deduct credits for sample generation
            if generation_request.creditsCostSample:
                await self._credit_service.deduct_credits(
                    user_id=generation_request.userId,
                    generation_id=generation_request.id,
                    amount=generation_request.creditsCostSample
                )

            # Notify user that samples are ready
            notification_payload = {
                "type": "samples_ready",
                "generationId": str(generation_request.id),
                "message": "Your creative samples are ready for review!",
                "samples": sample_assets_data
            }
            await self._notification_service.notify_user(generation_request.userId, notification_payload)

        elif payload.stage == "final_asset_generated":
            final_asset_id = payload.results.finalAssetId
            generation_request.mark_as_completed(final_asset_id)
            await self._generation_repo.update(generation_request)
            
            # Deduct credits for final generation
            if generation_request.creditsCostFinal:
                 await self._credit_service.deduct_credits(
                    user_id=generation_request.userId,
                    generation_id=generation_request.id,
                    amount=generation_request.creditsCostFinal
                )
            
            # Notify user of completion
            notification_payload = {
                "type": "generation_complete",
                "generationId": str(generation_request.id),
                "message": "Your final creative is complete!",
                "finalAssetId": str(final_asset_id)
            }
            await self._notification_service.notify_user(generation_request.userId, notification_payload)
        else:
            logger.warning(f"Received success callback with unhandled stage: {payload.stage}")