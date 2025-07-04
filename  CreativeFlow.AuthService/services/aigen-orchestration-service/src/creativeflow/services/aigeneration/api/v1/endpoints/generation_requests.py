import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import (
    OrchestrationService,
    GenerationRequestNotFoundError,
    GenerationRequestStateError,
)
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest as DomainGenerationRequest

logger = logging.getLogger(__name__)
router = APIRouter()

def domain_to_read_schema(domain_model: DomainGenerationRequest) -> schemas.GenerationRequestRead:
    """Helper to convert domain model to Pydantic read schema."""
    return schemas.GenerationRequestRead.from_orm(domain_model)


@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new AI Generation Request",
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Initiates a new AI creative generation process.

    This endpoint accepts the initial parameters for a generation, performs
    credit checks, queues the job for the n8n workflow engine, and returns
    the initial state of the generation request.
    """
    logger.info(f"Received generation request for user {request_payload.user_id} and project {request_payload.project_id}")
    generation_request = await orchestration_svc.initiate_generation(
        request_data=request_payload
    )
    return domain_to_read_schema(generation_request)


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status",
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Retrieves the current status and details of a specific generation request.
    """
    try:
        logger.debug(f"Fetching status for request_id: {request_id}")
        generation_request = await orchestration_svc.get_generation_status(request_id)
        return domain_to_read_schema(generation_request)
    except GenerationRequestNotFoundError as e:
        logger.warning(f"Generation request not found: {request_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select a Sample and Initiate Final Generation",
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Selects a generated sample to proceed with high-resolution final generation.

    This triggers a new job for the n8n engine to upscale or finalize the chosen creative.
    """
    try:
        logger.info(f"Received sample selection for request {request_id} by user {sample_selection.user_id}")
        generation_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            selected_sample_id=sample_selection.selected_sample_id,
            user_id=sample_selection.user_id,
            desired_resolution=sample_selection.desired_resolution,
        )
        return domain_to_read_schema(generation_request)
    except GenerationRequestNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, GenerationRequestStateError) as e: # ValueError for invalid sample ID
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate Samples",
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Triggers a regeneration of the initial samples, optionally with an updated prompt.
    """
    try:
        logger.info(f"Received sample regeneration request for {request_id} by user {regeneration_request.user_id}")
        generation_request = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance,
        )
        return domain_to_read_schema(generation_request)
    except GenerationRequestNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except GenerationRequestStateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))