import logging
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from creativeflow.services.aigeneration.api.v1.schemas import (
    GenerationRequestCreate,
    GenerationRequestRead,
    SampleSelection,
    RegenerateSamplesRequest
)
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.core.error_handlers import (
    InsufficientCreditsError,
    ResourceNotFoundError,
    InvalidStateError,
    GenerationJobPublishError,
    CreditDeductionError
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new AI generation request"
)
async def create_generation_request(
    request_data: GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Initiates a new AI creative generation process.

    This endpoint accepts the parameters for a new generation, validates them,
    checks and deducts credits, and queues the job for processing.

    - **user_id**: The ID of the user making the request.
    - **project_id**: The ID of the project this generation belongs to.
    - **input_prompt**: The main text prompt for the AI.
    - **...**: Other generation parameters.

    Returns the initial state of the generation request, including its unique ID and status.
    The response code is 202 Accepted, indicating the request has been accepted for processing.
    """
    try:
        logger.info(f"Received generation request for user {request_data.user_id} in project {request_data.project_id}")
        generation_request = await orchestration_svc.initiate_generation(request_data)
        return generation_request
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except (GenerationJobPublishError, CreditDeductionError) as e:
        # These are internal failures after the request has been accepted in principle.
        # Logging is done in the service, here we translate to a client-facing error.
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error during generation initiation for user {request_data.user_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred while initiating the generation.")

@router.get(
    "/{request_id}",
    response_model=GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get generation request status and results"
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Retrieves the current status and details of a specific generation request.
    This can be used to poll for results.

    - **request_id**: The unique identifier of the generation request.
    """
    try:
        logger.debug(f"Fetching status for request ID: {request_id}")
        generation_request = await orchestration_svc.get_generation_status(request_id)
        return generation_request
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{request_id}/select-sample",
    response_model=GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Select a sample and trigger final generation"
)
async def select_sample_for_final_generation(
    request_id: UUID,
    selection_data: SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Selects a generated sample to proceed with final, high-resolution generation.

    - **request_id**: The ID of the generation request, which must be in 'AWAITING_SELECTION' status.
    - **selected_sample_id**: The asset ID of the chosen sample.
    - **user_id**: The user making the selection (for validation).
    - **desired_resolution**: Optional override for the final asset resolution.
    """
    try:
        logger.info(f"User {selection_data.user_id} selected sample {selection_data.selected_sample_id} for request {request_id}")
        updated_request = await orchestration_svc.select_sample_and_initiate_final(
            request_id=request_id,
            selection_data=selection_data
        )
        return updated_request
    except (ResourceNotFoundError, InvalidStateError) as e:
        # Combine 404 and 409 into a clear client error.
        # E.g. "Request not found" or "Request is not awaiting sample selection."
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ResourceNotFoundError) else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except (GenerationJobPublishError, CreditDeductionError) as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=GenerationRequestRead,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger regeneration of samples"
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_data: RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Triggers a new batch of samples to be generated for a request.
    This may incur additional credit costs.

    - **request_id**: The ID of the original generation request.
    - **user_id**: The user making the request (for validation).
    - **updated_prompt**: Optional new prompt to use for regeneration.
    - **updated_style_guidance**: Optional new style guidance.
    """
    try:
        logger.info(f"User {regeneration_data.user_id} requested sample regeneration for request {request_id}")
        updated_request = await orchestration_svc.trigger_sample_regeneration(
            request_id=request_id,
            regeneration_data=regeneration_data
        )
        return updated_request
    except (ResourceNotFoundError, InvalidStateError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ResourceNotFoundError) else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=str(e))
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    except (GenerationJobPublishError, CreditDeductionError) as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))