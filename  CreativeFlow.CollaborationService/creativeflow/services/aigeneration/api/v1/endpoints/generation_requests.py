import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service

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
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
) -> schemas.GenerationRequestRead:
    """
    Endpoint to create and start a new AI generation request.

    - **request_payload**: Contains all the necessary inputs like prompt, format, etc.
    - **orchestration_svc**: Injected service that handles the business logic.

    This endpoint will:
    1. Validate inputs.
    2. Check and deduct credits for sample generation.
    3. Create a record in the database.
    4. Publish a job to the n8n workflow engine via RabbitMQ.
    5. Return the initial state of the generation request.
    """
    logger.info("Received request to create generation for user %s", request_payload.user_id)
    generation_request = await orchestration_svc.initiate_generation(
        request_data=request_payload
    )
    return schemas.GenerationRequestRead.from_domain(generation_request)


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Request Status",
    description="Retrieves the current status and details of a generation request."
)
async def get_generation_request_status(
    request_id: UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
) -> schemas.GenerationRequestRead:
    """
    Fetches the details of a specific generation request by its ID.
    """
    logger.info("Fetching status for request_id: %s", request_id)
    generation_request = await orchestration_svc.get_generation_status(request_id)
    return schemas.GenerationRequestRead.from_domain(generation_request)


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Select Sample for Final Generation",
    description="Selects a generated sample and triggers the final high-resolution generation."
)
async def select_sample_for_final_generation(
    request_id: UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
) -> schemas.GenerationRequestRead:
    """
    Endpoint to select a sample and kick off the final asset generation.

    - **request_id**: The ID of the generation request that is awaiting sample selection.
    - **sample_selection**: The ID of the chosen sample and desired final resolution.
    """
    logger.info(
        "Received sample selection for request_id %s, user %s, sample %s",
        request_id, sample_selection.user_id, sample_selection.selected_sample_id
    )
    generation_request = await orchestration_svc.select_sample_and_initiate_final(
        request_id=request_id,
        user_id=sample_selection.user_id,
        selected_sample_id=sample_selection.selected_sample_id,
        desired_resolution=sample_selection.desired_resolution
    )
    return schemas.GenerationRequestRead.from_domain(generation_request)


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Regenerate Samples",
    description="Triggers a regeneration of the initial samples, potentially with an updated prompt."
)
async def regenerate_samples(
    request_id: UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
) -> schemas.GenerationRequestRead:
    """
    Endpoint to request a new batch of samples for a generation request.
    This typically costs additional credits.
    """
    logger.info(
        "Received request to regenerate samples for request_id %s, user %s",
        request_id, regeneration_request.user_id
    )
    generation_request = await orchestration_svc.trigger_sample_regeneration(
        request_id=request_id,
        user_id=regeneration_request.user_id,
        updated_prompt=regeneration_request.updated_prompt,
        updated_style_guidance=regeneration_request.updated_style_guidance,
    )
    return schemas.GenerationRequestRead.from_domain(generation_request)