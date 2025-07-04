import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service, verify_n8n_secret

router = APIRouter(dependencies=[Depends(verify_n8n_secret)])
logger = logging.getLogger(__name__)


@router.post(
    "/sample-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Sample Generation Callback",
    description="Webhook endpoint for n8n to post the results of a sample generation job."
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload = Body(...),
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives sample generation results from n8n.
    Updates the generation request status to `AWAITING_SELECTION` and stores sample asset info.
    """
    request_id = callback_payload.generation_request_id
    logger.info(
        "Received n8n sample result callback for request_id: %s. %d samples received.",
        request_id, len(callback_payload.samples)
    )
    await orchestration_svc.process_n8n_sample_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Final Generation Callback",
    description="Webhook endpoint for n8n to post the result of a final asset generation job."
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload = Body(...),
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives the final generated asset from n8n.
    Updates the generation request status to `COMPLETED` and stores final asset info.
    """
    request_id = callback_payload.generation_request_id
    logger.info(
        "Received n8n final result callback for request_id: %s.", request_id
    )
    await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Error Callback",
    description="Webhook endpoint for n8n to post errors encountered during a generation job."
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload = Body(...),
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives error details from n8n.
    Updates the generation request status to `FAILED`, stores error info,
    and potentially triggers a credit refund.
    """
    request_id = callback_payload.generation_request_id
    logger.error(
        "Received n8n error callback for request_id: %s. Stage: %s, Message: %s",
        request_id, callback_payload.failed_stage, callback_payload.error_message
    )
    await orchestration_svc.handle_n8n_error(callback_payload)
    return {"status": "received"}