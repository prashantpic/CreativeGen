"""
API Endpoints for n8n Workflow Engine Callbacks.

This router provides secure webhook endpoints for the n8n workflow engine to
report back on the status of generation jobs. It handles successful results
for both sample and final asset generation, as well as error conditions.
"""

import logging

from fastapi import APIRouter, Depends, status

from .....core.dependencies import get_orchestration_service, verify_n8n_callback_secret
from .....application.services.orchestration_service import OrchestrationService
from ..schemas import (
    N8NSampleResultPayload,
    N8NFinalResultPayload,
    N8NErrorPayload,
)

router = APIRouter(
    dependencies=[Depends(verify_n8n_callback_secret)]
)
logger = logging.getLogger(__name__)

@router.post(
    "/sample-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Sample Generation Callback",
    description="Receives the results of a successful sample generation task from n8n.",
)
async def handle_n8n_sample_generation_callback(
    callback_payload: N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook for n8n to post sample generation results.

    - The endpoint is secured by a shared secret dependency.
    - It delegates the processing of the callback data to the OrchestrationService.
    - Returns an immediate 202 Accepted response to n8n.
    """
    logger.info(f"Received sample result callback for request ID: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_sample_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Final Generation Callback",
    description="Receives the result of a successful final asset generation task from n8n.",
)
async def handle_n8n_final_generation_callback(
    callback_payload: N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook for n8n to post final asset generation results.

    - Secured by a shared secret dependency.
    - Delegates processing to the OrchestrationService.
    - Returns an immediate 202 Accepted response.
    """
    logger.info(f"Received final result callback for request ID: {callback_payload.generation_request_id}")
    await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Error Callback",
    description="Receives error details from n8n if a generation task fails.",
)
async def handle_n8n_error_callback(
    callback_payload: N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook for n8n to report errors during the generation workflow.

    - Secured by a shared secret dependency.
    - Delegates error handling, including potential credit refunds, to the OrchestrationService.
    - Returns an immediate 202 Accepted response.
    """
    logger.error(
        f"Received error callback for request ID: {callback_payload.generation_request_id}. "
        f"Message: {callback_payload.error_message}"
    )
    await orchestration_svc.handle_n8n_error(callback_payload)
    return {"status": "received"}