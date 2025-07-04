import logging
from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.api.v1.schemas import (
    N8NSampleResultPayload,
    N8NFinalResultPayload,
    N8NErrorPayload
)
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service, verify_n8n_secret

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/sample-result",
    status_code=status.HTTP_200_OK,
    summary="Callback for n8n sample generation results",
    dependencies=[Depends(verify_n8n_secret)]
)
async def handle_n8n_sample_generation_callback(
    payload: N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Webhook endpoint for n8n to post the results of a sample generation task.
    This endpoint is secured with a shared secret header.
    """
    logger.info(f"Received sample result callback for request ID: {payload.generation_request_id}")
    await orchestration_svc.process_n8n_sample_callback(payload)
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_200_OK,
    summary="Callback for n8n final asset generation results",
    dependencies=[Depends(verify_n8n_secret)]
)
async def handle_n8n_final_generation_callback(
    payload: N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Webhook endpoint for n8n to post the result of a final asset generation task.
    This endpoint is secured with a shared secret header.
    """
    logger.info(f"Received final result callback for request ID: {payload.generation_request_id}")
    await orchestration_svc.process_n8n_final_asset_callback(payload)
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_200_OK,
    summary="Callback for n8n to report an error during generation",
    dependencies=[Depends(verify_n8n_secret)]
)
async def handle_n8n_error_callback(
    payload: N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Webhook endpoint for n8n to report an error that occurred during a workflow.
    This endpoint is secured with a shared secret header.
    """
    logger.warning(
        f"Received error callback for request ID: {payload.generation_request_id}. "
        f"Stage: {payload.failed_stage}, Error: {payload.error_message}"
    )
    await orchestration_svc.handle_n8n_error(payload)
    return {"status": "received"}