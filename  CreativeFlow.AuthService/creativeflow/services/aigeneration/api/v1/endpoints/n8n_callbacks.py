import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status

from ..schemas import (
    N8NSampleResultPayload,
    N8NFinalResultPayload,
    N8NErrorPayload,
)
from ....application.services.orchestration_service import OrchestrationService
from ....core.dependencies import get_orchestration_service, verify_n8n_secret

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(verify_n8n_secret)])

@router.post(
    "/sample-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Callback for n8n Sample Generation Completion",
    description="Endpoint for n8n to post the results of a successful sample generation task."
)
async def handle_n8n_sample_generation_callback(
    callback_payload: N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Receives sample generation results from n8n, updates the generation request status
    to AWAITING_SELECTION, stores asset info, and notifies the user.
    """
    logger.info(f"Received n8n sample result callback for request_id: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_sample_callback(callback_data=callback_payload)
    return {"status": "received"}

@router.post(
    "/final-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Callback for n8n Final Generation Completion",
    description="Endpoint for n8n to post the results of a successful final asset generation task."
)
async def handle_n8n_final_generation_callback(
    callback_payload: N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Receives final asset results from n8n, updates the generation request status
    to COMPLETED, stores final asset info, and notifies the user.
    """
    logger.info(f"Received n8n final result callback for request_id: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_final_asset_callback(callback_data=callback_payload)
    return {"status": "received"}

@router.post(
    "/error",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Callback for n8n Errors",
    description="Endpoint for n8n to report an error that occurred during a generation task."
)
async def handle_n8n_error_callback(
    callback_payload: N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Receives error details from n8n, updates the generation request status to FAILED,
    handles credit refunds if applicable, and notifies the user.
    """
    logger.error(
        f"Received n8n error callback for request_id: {callback_payload.generation_request_id}. "
        f"Error: {callback_payload.error_message}"
    )
    await orchestration_svc.handle_n8n_error(error_data=callback_payload)
    return {"status": "received"}