import logging
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas
from ....core.dependencies import get_orchestration_service
from ....application.services.orchestration_service import OrchestrationService, InsufficientCreditsError, InvalidGenerationStateError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI Generation Request",
    description="Initiates a new AI creative generation process by creating a request, checking and deducting credits, and publishing a job to the n8n queue.",
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to create and start a new AI generation request.
    """
    logger.info(f"Received generation request for user {request_payload.user_id} and project {request_payload.project_id}")
    try:
        generation_request = await orchestration_svc.initiate_generation(
            user_id=request_payload.user_id,
            request_data=request_payload,
        )
        return generation_request
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except Exception as e:
        logger.error(f"Error initiating generation for user {request_payload.user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred while initiating the generation.")

@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    summary="Get Generation Request Status",
    description="Retrieves the current status and details of a specific generation request by its ID.",
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to fetch the status of an ongoing or completed generation request.
    """
    logger.info(f"Fetching status for request ID: {request_id}")
    generation_request = await orchestration_svc.get_generation_status(request_id)
    if not generation_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation request not found")
    return generation_request

@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    summary="Select a Sample for Final Generation",
    description="Selects a generated sample and triggers the final high-resolution generation process.",
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to select a sample and initiate the final asset generation.
    """
    logger.info(f"Received sample selection for request ID: {request_id}, sample ID: {sample_selection.selected_sample_id}")
    try:
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            selected_sample_id=sample_selection.selected_sample_id,
            user_id=sample_selection.user_id,
            desired_resolution=sample_selection.desired_resolution
        )
        return updated_request
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except InvalidGenerationStateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e: # For invalid sample ID
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e: # Propagate existing HTTP exceptions (like 404)
        raise e
    except Exception as e:
        logger.error(f"Error processing sample selection for request {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred during sample selection.")


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    summary="Regenerate Samples",
    description="Triggers a new sample generation process for an existing request, potentially with an updated prompt.",
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to trigger sample regeneration.
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
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except InvalidGenerationStateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing sample regeneration for request {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred during sample regeneration.")