import logging
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.core.error_handlers import InsufficientCreditsError, InvalidGenerationStateError, ApplicationException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create Generation Request",
    description="Initiates a new AI creative generation process."
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Endpoint to receive and initiate a new AI creative generation request.

    - Validates the request payload.
    - Checks for sufficient user credits.
    - Creates a record in the database.
    - Publishes a job to the n8n workflow engine via RabbitMQ.
    """
    logger.info(f"Received generation request for user {request_payload.user_id} and project {request_payload.project_id}")
    try:
        generation_request = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request
    except (InsufficientCreditsError, InvalidGenerationStateError) as e:
        # These exceptions are handled by dedicated handlers, but re-raising with HTTPException
        # can provide more context if needed or ensure consistent handling.
        # The handlers in `error_handlers.py` will catch the custom exception types.
        raise e
    except ApplicationException as e:
        # Catch other application-specific errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during generation initiation: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status",
    description="Retrieves the current status and details of a specific generation request."
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Fetches and returns the complete details of a generation request by its ID.
    """
    logger.info(f"Fetching status for request ID: {request_id}")
    generation_request = await orchestration_svc.get_generation_status(request_id)
    if not generation_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation request not found")
    return generation_request


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Select Sample for Final Generation",
    description="Selects a generated sample to proceed with final, high-resolution generation."
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Triggers the final asset generation phase based on a user-selected sample.

    - Validates that the request is in the correct state (`AWAITING_SELECTION`).
    - Checks and deducts credits for the final generation.
    - Publishes a new job to n8n for upscaling/finalizing the selected asset.
    """
    logger.info(f"Received sample selection for request ID: {request_id}, sample: {sample_selection.selected_sample_id}")
    try:
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            user_id=sample_selection.user_id,
            selected_sample_id=sample_selection.selected_sample_id,
            desired_resolution=sample_selection.desired_resolution
        )
        return updated_request
    except (InsufficientCreditsError, InvalidGenerationStateError) as e:
        raise e
    except ValueError as e: # Catch validation errors from the service layer
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Regenerate Samples",
    description="Triggers a new batch of samples to be generated for a request, optionally with a new prompt."
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Allows a user to request a new set of samples.

    - Checks and deducts credits for the regeneration.
    - Publishes a new sample generation job to n8n.
    """
    logger.info(f"Received sample regeneration request for ID: {request_id}")
    try:
        updated_request = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance
        )
        return updated_request
    except (InsufficientCreditsError, InvalidGenerationStateError) as e:
        raise e