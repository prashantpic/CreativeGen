"""
Contains the core business logic for the 'Initiate Generation' use case.
It orchestrates validation, persistence, and job publishing.
"""
import logging
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ..dtos import GenerationRequestCreateDTO
from ..interfaces import ICreditService, IGenerationRepository, IJobPublisher
from ...domain.models.generation_request import GenerationRequest, GenerationStatus

logger = logging.getLogger(__name__)


class InsufficientCreditsError(Exception):
    """Custom exception raised when a user does not have enough credits."""
    pass


class InitiateGenerationUseCase:
    """
    Orchestrates the start of an AI generation job, including validation and queuing.
    """

    def __init__(
        self,
        credit_service: ICreditService,
        job_publisher: IJobPublisher,
        generation_repo: IGenerationRepository,
    ):
        self._credit_service = credit_service
        self._job_publisher = job_publisher
        self._generation_repo = generation_repo

    async def execute(
        self, user_id: UUID, request_data: GenerationRequestCreateDTO
    ) -> GenerationRequest:
        """
        Executes the use case logic.

        1. Determines credit cost.
        2. Reserves credits via the credit service.
        3. Creates and persists a GenerationRequest entity.
        4. Publishes a job to the message queue for asynchronous processing.

        Args:
            user_id: The ID of the user initiating the request.
            request_data: The DTO containing the generation parameters.

        Raises:
            InsufficientCreditsError: If the user's balance is too low.

        Returns:
            The newly created GenerationRequest domain entity.
        """
        # 1. Determine the initial credit cost (e.g., for sample generation)
        # This logic can be enhanced based on inputParameters
        initial_cost = Decimal("1.0") * request_data.inputParameters.get("samples", 1)
        logger.info(f"Calculated initial credit cost for user {user_id}: {initial_cost}")

        # 2. Call credit_service to check and reserve credits
        can_afford = await self._credit_service.check_and_reserve_credits(
            user_id=user_id, amount=initial_cost
        )
        if not can_afford:
            logger.warning(f"User {user_id} has insufficient credits for cost {initial_cost}.")
            raise InsufficientCreditsError("Insufficient credits for the operation.")

        # 3. Create a GenerationRequest domain entity
        generation_request = GenerationRequest(
            userId=user_id,
            projectId=request_data.projectId,
            inputPrompt=request_data.inputPrompt,
            styleGuidance=request_data.styleGuidance,
            inputParameters=request_data.inputParameters,
            status=GenerationStatus.PENDING,
            creditsCostSample=initial_cost,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
        )

        # 4. Persist the new entity
        await self._generation_repo.add(generation_request)
        logger.info(f"Persisted new GenerationRequest with ID: {generation_request.id}")
        
        # 5. Mark request as processing before publishing job
        generation_request.mark_as_processing_samples()
        await self._generation_repo.update(generation_request)


        # 6. Construct the job payload for RabbitMQ
        job_payload = {
            "generationId": str(generation_request.id),
            "userId": str(user_id),
            "projectId": str(request_data.projectId),
            "inputPrompt": request_data.inputPrompt,
            "styleGuidance": request_data.styleGuidance,
            "inputParameters": request_data.inputParameters,
        }

        # 7. Publish the job
        await self._job_publisher.publish_generation_job(job_payload)
        logger.info(f"Published generation job for ID: {generation_request.id}")

        # 8. Return the created entity
        return generation_request