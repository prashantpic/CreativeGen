import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.exceptions import (
    InsufficientCreditsError,
    ResourceNotFoundError,
    InvalidStateError
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create Generation Request"
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Accepts a new AI creative generation request.

    This endpoint initiates the generation process by:
    1. Validating the request payload.
    2. Checking and deducting credits for sample generation.
    3. Creating a record in the database.
    4. Publishing a job to the n8n workflow engine via RabbitMQ.

    Returns a 202 Accepted response as the process is asynchronous. The
    response body contains the initial state of the generation request.
    """
    try:
        logger.info(f"Received generation request for user {request_payload.user_id} and project {request_payload.project_id}")
        generation_request = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except Exception as e:
        logger.error(f"Error initiating generation for user {request_payload.user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to initiate generation.")


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status"
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Retrieves the current status and details of a specific generation request.
    """
    try:
        logger.debug(f"Fetching status for request ID: {request_id}")
        generation_request = await orchestration_svc.get_generation_status(request_id)
        return generation_request
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select Sample for Final Generation"
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Selects a generated sample to proceed with final, high-resolution generation.

    This action requires the generation request to be in the `AWAITING_SELECTION` state.
    It will trigger credit deduction for the final generation and publish a new job to n8n.
    """
    try:
        logger.info(f"Received sample selection for request {request_id} by user {sample_selection.user_id}")
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            user_id=sample_selection.user_id,
            selected_sample_id=sample_selection.selected_sample_id,
            desired_resolution=sample_selection.desired_resolution
        )
        return updated_request
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidStateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except ValueError as e: # For invalid sample_id
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate Samples"
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Triggers a new round of sample generation for an existing request.

    This can be used if the user is not satisfied with the initial samples.
    It may incur additional credit costs.
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
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidStateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))