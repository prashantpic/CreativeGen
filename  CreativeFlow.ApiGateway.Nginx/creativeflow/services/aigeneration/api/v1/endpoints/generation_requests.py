```python
import uuid
from fastapi import APIRouter, Depends, status, HTTPException

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.application.exceptions import ApplicationException

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI generation request"
)
async def create_generation_request(
    request_payload: schemas.GenerationRequestCreate,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Initiates a new AI creative generation process.

    - **Validates** the request payload.
    - **Checks and deducts** credits for sample generation.
    - **Creates** a record in the database.
    - **Publishes** a job to the n8n workflow engine.
    """
    try:
        request_domain_model = await orchestration_svc.initiate_generation(request_payload)
        return request_domain_model
    except ApplicationException as e:
        # The custom exception handler will catch this, but we can also handle it here if needed.
        # This re-raise will be caught by the handler in main.py
        raise e
    except Exception as e:
        # Generic catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{request_id}",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Get generation request status"
)
async def get_generation_request_status(
    request_id: uuid.UUID,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Retrieves the current status and details of a specific generation request.
    """
    return await orchestration_svc.get_generation_status(request_id)


@router.post(
    "/{request_id}/select-sample",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Select a sample and initiate final generation"
)
async def select_sample_for_final_generation(
    request_id: uuid.UUID,
    sample_selection: schemas.SampleSelection,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Selects a generated sample to proceed with final, high-resolution generation.

    - **Validates** that the request is in the correct state (`AWAITING_SELECTION`).
    - **Checks and deducts** credits for final generation.
    - **Publishes** a final generation job to the n8n workflow.
    """
    return await orchestration_svc.select_sample_and_initiate_final(
        request_id=request_id,
        selected_sample_id=sample_selection.selected_sample_id,
        user_id=sample_selection.user_id,
        desired_resolution=sample_selection.desired_resolution
    )


@router.post(
    "/{request_id}/regenerate-samples",
    response_model=schemas.GenerationRequestRead,
    status_code=status.HTTP_200_OK,
    summary="Regenerate creative samples"
)
async def regenerate_samples(
    request_id: uuid.UUID,
    regeneration_request: schemas.RegenerateSamplesRequest,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Triggers a regeneration of the initial samples, optionally with an updated prompt.

    - **Checks and deducts** credits for regeneration.
    - **Publishes** a new sample generation job to the n8n workflow.
    """
    return await orchestration_svc.trigger_sample_regeneration(
        request_id=request_id,
        user_id=regeneration_request.user_id,
        updated_prompt=regeneration_request.updated_prompt,
        updated_style_guidance=regeneration_request.updated_style_guidance
    )
```