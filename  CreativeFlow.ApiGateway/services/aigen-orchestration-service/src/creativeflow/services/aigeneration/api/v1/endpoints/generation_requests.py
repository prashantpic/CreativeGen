import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new AI Generation Request"
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Initiates a new AI creative generation process.

    This endpoint accepts all parameters for a generation, validates them,
    checks and deducts user credits, and queues a job for the AI workflow engine.

    - **user_id**: The ID of the user initiating the request.
    - **project_id**: The project to which this generation belongs.
    - **input_prompt**: The primary text prompt for generation.
    - **...** (other generation parameters)
    """
    try:
        logger.info(f"Received generation request for user {request_payload.user_id} in project {request_payload.project_id}")
        generation_request = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request
    except HTTPException as e:
        # Re-raise known HTTP exceptions (like 402, 404 from the service layer)
        raise e
    except Exception as e:
        logger.error(f"Error initiating generation for user {request_payload.user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while initiating the generation request."
        )

@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status"
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Retrieves the current status and details of a specific generation request.
    """
    logger.info(f"Fetching status for request ID: {request_id}")
    return await orchestration_svc.get_generation_status(request_id)

@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select a Sample for Final Generation"
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Selects a generated sample to proceed with final, high-resolution generation.

    This triggers a new job for the AI workflow engine to upscale or finalize the chosen creative.
    """
    try:
        logger.info(f"User {sample_selection.user_id} selected sample {sample_selection.selected_sample_id} for request {request_id}")
        return await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            user_id=sample_selection.user_id,
            selected_sample_id=sample_selection.selected_sample_id,
            desired_resolution=sample_selection.desired_resolution
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error selecting sample for request {request_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while selecting the sample."
        )

@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate Samples"
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Triggers a new sample generation process for an existing request.

    This can be used if the initial samples were not satisfactory.
    It may incur additional credit costs.
    """
    try:
        logger.info(f"User {regeneration_request.user_id} requested sample regeneration for request {request_id}")
        return await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error regenerating samples for request {request_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during sample regeneration."
        )