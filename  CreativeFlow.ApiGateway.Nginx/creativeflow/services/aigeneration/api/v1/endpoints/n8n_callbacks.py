import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import (
    OrchestrationService,
)
from creativeflow.services.aigeneration.core.dependencies import (
    get_orchestration_service,
    verify_n8n_secret,
)
from creativeflow.services.aigeneration.application.dtos import (
    N8NSampleResultDTO,
    N8NFinalResultDTO,
    N8NErrorDTO
)


router = APIRouter(dependencies=[Depends(verify_n8n_secret)])
logger = logging.getLogger(__name__)


@router.post(
    "/sample-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Sample Generation Callback",
    description="Webhook endpoint for n8n to post the results of a successful sample generation job.",
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives sample generation results from the n8n workflow.
    - Updates the generation request status to 'AWAITING_SELECTION'.
    - Stores the metadata for the generated sample assets.
    - Triggers a notification to the user.
    """
    request_id = callback_payload.generation_request_id
    logger.info(
        "Received n8n sample result callback",
        extra={
            "request_id": str(request_id),
            "sample_count": len(callback_payload.samples),
        },
    )
    
    dto = N8NSampleResultDTO.from_orm(callback_payload)
    await orchestration_svc.process_n8n_sample_callback(callback_data=dto)
    
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Final Generation Callback",
    description="Webhook endpoint for n8n to post the results of a successful final asset generation job.",
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives the final, high-resolution asset from the n8n workflow.
    - Updates the generation request status to 'COMPLETED'.
    - Stores the metadata for the final asset.
    - Triggers a notification to the user.
    """
    request_id = callback_payload.generation_request_id
    logger.info(
        "Received n8n final result callback",
        extra={"request_id": str(request_id)},
    )
    
    dto = N8NFinalResultDTO.from_orm(callback_payload)
    await orchestration_svc.process_n8n_final_asset_callback(callback_data=dto)

    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Error Callback",
    description="Webhook endpoint for n8n to report an error that occurred during a generation job.",
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives error details from a failed n8n workflow.
    - Updates the generation request status to 'FAILED' or 'CONTENT_REJECTED'.
    - Stores the error message and details.
    - Initiates a credit refund if applicable.
    - Triggers a failure notification to the user.
    """
    request_id = callback_payload.generation_request_id
    logger.error(
        "Received n8n error callback",
        extra={
            "request_id": str(request_id),
            "error_message": callback_payload.error_message,
            "failed_stage": callback_payload.failed_stage,
        },
    )

    dto = N8NErrorDTO.from_orm(callback_payload)
    await orchestration_svc.handle_n8n_error(error_data=dto)

    return {"status": "received"}