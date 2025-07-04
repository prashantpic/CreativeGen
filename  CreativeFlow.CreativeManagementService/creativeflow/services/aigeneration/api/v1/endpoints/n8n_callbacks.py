import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response

from . import schemas
from ....core.dependencies import get_orchestration_service, verify_n8n_secret
from ....application.services.orchestration_service import OrchestrationService

router = APIRouter(dependencies=[Depends(verify_n8n_secret)])
logger = logging.getLogger(__name__)

@router.post(
    "/sample-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Sample Generation Callback",
    description="Webhook endpoint for n8n to post the results of a successful sample generation task."
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives sample generation results from n8n, updates the request status,
    stores asset info, and notifies the user.
    """
    logger.info(f"Received n8n sample-result callback for request ID: {callback_payload.generation_request_id}")
    try:
        await orchestration_svc.process_n8n_sample_callback(callback_payload)
    except Exception as e:
        # Log the error but don't fail the request to n8n, as it can't do anything about it.
        # This prevents n8n from endlessly retrying.
        logger.error(
            f"Error processing n8n sample-result callback for request ID "
            f"{callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Final Generation Callback",
    description="Webhook endpoint for n8n to post the results of a successful final asset generation task."
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives final asset generation results from n8n, updates the request status
    to COMPLETED, stores final asset info, and notifies the user.
    """
    logger.info(f"Received n8n final-result callback for request ID: {callback_payload.generation_request_id}")
    try:
        await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
    except Exception as e:
        logger.error(
            f"Error processing n8n final-result callback for request ID "
            f"{callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Error Callback",
    description="Webhook endpoint for n8n to post error information when a generation task fails."
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> dict:
    """
    Receives error details from n8n, updates the request status to FAILED,
    logs the error, potentially triggers a credit refund, and notifies the user.
    """
    logger.warning(f"Received n8n error callback for request ID: {callback_payload.generation_request_id}")
    try:
        await orchestration_svc.handle_n8n_error(callback_payload)
    except Exception as e:
        logger.error(
            f"Error processing n8n error callback for request ID "
            f"{callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}