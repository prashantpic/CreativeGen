import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.core.error_handlers import (
    InsufficientCreditsError,
    CreditServiceError,
    GenerationRequestNotFound,
    InvalidGenerationStateError,
    GenerationJobPublishError,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI Generation Request",
    description="Initiates a new AI creative generation process. This involves credit checks, creating a record, and dispatching a job to the n8n workflow engine.",
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Endpoint to create and initiate a new AI generation request.
    
    - Validates the incoming payload.
    - Checks and deducts credits for the initial sample generation.
    - Creates a persistent record of the request.
    - Publishes a job to the message queue for asynchronous processing.
    """
    try:
        logger.info(f"Received generation request for user {request_payload.user_id} and project {request_payload.project_id}")
        generation_request = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request
    except (InsufficientCreditsError, CreditServiceError, GenerationJobPublishError) as e:
        # These exceptions are handled by dedicated handlers, but re-raising them
        # ensures they are caught. This is more explicit than a generic catch-all.
        raise e
    except Exception as e:
        logger.exception(f"An unexpected error occurred while creating generation request for user {request_payload.user_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred during request initiation.")

@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status",
    description="Retrieves the current status and details of a specific generation request.",
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Fetches the complete state of a generation request by its UUID.
    """
    try:
        logger.debug(f"Fetching status for request_id: {request_id}")
        generation_request = await orchestration_svc.get_generation_status(request_id=request_id)
        return generation_request
    except GenerationRequestNotFound as e:
        raise e

@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Select a Sample for Final Generation",
    description="Selects a generated sample and triggers the final high-resolution asset generation.",
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Endpoint to select a preferred sample and initiate the final generation phase.
    
    - Validates the request is in the 'AWAITING_SELECTION' state.
    - Checks and deducts credits for final generation.
    - Publishes a new job for high-resolution processing.
    """
    try:
        logger.info(f"Received sample selection for request {request_id} by user {sample_selection.user_id}")
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            selected_sample_id=sample_selection.selected_sample_id,
            user_id=sample_selection.user_id,
            desired_resolution=sample_selection.desired_resolution,
        )
        return updated_request
    except (GenerationRequestNotFound, InvalidGenerationStateError, InsufficientCreditsError, GenerationJobPublishError) as e:
        raise e
    except Exception as e:
        logger.exception(f"An unexpected error occurred while selecting sample for request {request_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred while processing the sample selection.")


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Regenerate Samples",
    description="Triggers a new batch of samples to be generated for a request, potentially with an updated prompt.",
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Endpoint to trigger sample regeneration.
    
    - Checks if regeneration is allowed.
    - Checks and deducts credits for the regeneration attempt.
    - Publishes a new job for sample generation.
    """
    try:
        logger.info(f"Received sample regeneration request for {request_id} by user {regeneration_request.user_id}")
        updated_request = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance
        )
        return updated_request
    except (GenerationRequestNotFound, InvalidGenerationStateError, InsufficientCreditsError, GenerationJobPublishError) as e:
        raise e
    except Exception as e:
        logger.exception(f"An unexpected error occurred during sample regeneration for request {request_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred while processing sample regeneration.")