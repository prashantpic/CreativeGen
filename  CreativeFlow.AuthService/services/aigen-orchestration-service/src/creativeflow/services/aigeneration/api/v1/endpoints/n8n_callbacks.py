import logging
from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service, verify_n8n_secret

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/sample-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Sample Generation Callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to post the results of a sample generation task.
    """
    logger.info(f"Received sample result callback for request_id: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_sample_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Final Generation Callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to post the result of a final asset generation task.
    """
    logger.info(f"Received final result callback for request_id: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Error Callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to report an error that occurred during a generation task.
    """
    logger.error(
        f"Received error callback for request_id: {callback_payload.generation_request_id}. "
        f"Error: {callback_payload.error_message}"
    )
    await orchestration_svc.handle_n8n_error(callback_payload)
    return {"status": "received"}