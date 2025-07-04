import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import (
    OrchestrationService, InsufficientCreditsError, GenerationRequestNotFoundError, InvalidGenerationStateError
)
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new Generation Request"
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Initiates a new AI creative generation process.

    This endpoint accepts the parameters for a new generation, validates them,
    checks and deducts credits, and queues the job for processing.
    """
    try:
        generation_request = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except Exception as e:
        # Catch other potential errors from the service layer
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status"
)
async def get_generation_request_status(
    request_id: uuid.UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Retrieves the current status and details of a specific generation request.
    """
    try:
        generation_request = await orchestration_svc.get_generation_status(request_id=request_id)
        return generation_request
    except GenerationRequestNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select a Sample for Final Generation"
)
async def select_sample_for_final_generation(
    request_id: uuid.UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Selects a generated sample and triggers the final high-resolution generation.
    """
    try:
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            user_id=sample_selection.user_id,
            selected_sample_id=sample_selection.selected_sample_id,
            desired_resolution=sample_selection.desired_resolution
        )
        return updated_request
    except (GenerationRequestNotFoundError, InvalidGenerationStateError) as e:
        # Map domain errors to appropriate HTTP status codes
        if isinstance(e, GenerationRequestNotFoundError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if isinstance(e, InvalidGenerationStateError):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate Samples"
)
async def regenerate_samples(
    request_id: uuid.UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Triggers a new sample generation process for an existing request,
    optionally with an updated prompt or style.
    """
    try:
        updated_request = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance
        )
        return updated_request
    except (GenerationRequestNotFoundError, InvalidGenerationStateError) as e:
        if isinstance(e, GenerationRequestNotFoundError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if isinstance(e, InvalidGenerationStateError):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))