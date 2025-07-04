"""
FastAPI router for handling AI creative generation requests.

This module defines the API endpoints that clients use to initiate, monitor,
and manage AI generation tasks. It delegates the core business logic to the
OrchestrationService.
"""
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import (
    OrchestrationService,
    InsufficientCreditsError,
    GenerationRequestStateError,
)
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new AI generation request",
    description="Initiates a new AI creative generation process. This involves validating the request, checking and deducting credits, and queuing a job for the n8n workflow engine.",
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to create and initiate an AI generation request.

    - **request_payload**: Contains all necessary details for the generation, such as prompt, output format, and user/project context.

    Returns the details of the newly created generation request, including its ID and initial status.
    Raises HTTP exceptions for business rule violations like insufficient credits.
    """
    try:
        logger.info(
            "Received generation request for user %s, project %s",
            request_payload.user_id,
            request_payload.project_id
        )
        generation_request_domain = await orchestration_svc.initiate_generation(
            request_data=request_payload
        )
        return generation_request_domain
    except InsufficientCreditsError as e:
        logger.warning("Insufficient credits for user %s to start generation.", request_payload.user_id)
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=str(e),
        )
    except Exception as e:
        logger.error("Failed to initiate generation request: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while initiating the generation request.",
        )


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get generation request status",
    description="Retrieves the current status and details of a specific generation request by its ID.",
)
async def get_generation_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to fetch the status of an AI generation request.

    - **request_id**: The unique identifier of the generation request.

    Returns the full generation request object, including its current status, any generated assets, and error information if applicable.
    """
    logger.info("Fetching status for generation request ID: %s", request_id)
    # The service layer is responsible for raising a 404 HTTPException if not found.
    generation_request_domain = await orchestration_svc.get_generation_status(request_id)
    return generation_request_domain


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select a sample and initiate final generation",
    description="After samples are generated, this endpoint allows the user to select one and trigger the high-resolution final asset generation.",
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to select a sample and proceed to final asset generation.

    - **request_id**: The unique identifier of the generation request.
    - **sample_selection**: The payload containing the ID of the selected sample and desired final resolution.

    Returns the updated generation request object with the new status (`PROCESSING_FINAL`).
    """
    try:
        logger.info(
            "Received sample selection for request %s, user %s, sample %s",
            request_id,
            sample_selection.user_id,
            sample_selection.selected_sample_id
        )
        generation_request_domain = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            selected_sample_id=sample_selection.selected_sample_id,
            user_id=sample_selection.user_id,
            desired_resolution=sample_selection.desired_resolution
        )
        return generation_request_domain
    except InsufficientCreditsError as e:
        logger.warning("Insufficient credits for user %s, final generation request %s.", sample_selection.user_id, request_id)
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except GenerationRequestStateError as e:
        logger.warning("Invalid state for sample selection on request %s: %s", request_id, e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e: # For invalid sample ID
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Failed to process sample selection for request %s: %s", request_id, e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate samples",
    description="Triggers a regeneration of the sample images, potentially with an updated prompt or style guidance. This action may incur additional credit costs.",
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> schemas.GenerationRequestRead:
    """
    Endpoint to trigger sample regeneration for a generation request.

    - **request_id**: The unique identifier of the generation request.
    - **regeneration_request**: Optional updated parameters for the regeneration.

    Returns the updated generation request object with status back to `PROCESSING_SAMPLES`.
    """
    try:
        logger.info("Received sample regeneration request for ID %s by user %s", request_id, regeneration_request.user_id)
        generation_request_domain = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            user_id=regeneration_request.user_id,
            updated_prompt=regeneration_request.updated_prompt,
            updated_style_guidance=regeneration_request.updated_style_guidance,
        )
        return generation_request_domain
    except InsufficientCreditsError as e:
        logger.warning("Insufficient credits for user %s to regenerate samples for request %s.", regeneration_request.user_id, request_id)
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except GenerationRequestStateError as e:
        logger.warning("Invalid state for sample regeneration on request %s: %s", request_id, e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Failed to regenerate samples for request %s: %s", request_id, e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")