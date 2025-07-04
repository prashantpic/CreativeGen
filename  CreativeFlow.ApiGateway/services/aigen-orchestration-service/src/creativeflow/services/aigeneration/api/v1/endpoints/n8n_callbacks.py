import logging
from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service, verify_n8n_secret

router = APIRouter(dependencies=[Depends(verify_n8n_secret)])
logger = logging.getLogger(__name__)

@router.post(
    "/sample-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Sample Generation Callback"
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to call when sample generation is complete.
    This endpoint is secured by a shared secret in the 'X-Callback-Secret' header.
    """
    logger.info(f"Received sample result callback for request ID: {callback_payload.generation_request_id}")
    try:
        await orchestration_svc.process_n8n_sample_callback(callback_payload)
    except Exception as e:
        # Log the error but don't fail the request to n8n, as it might cause unwanted retries.
        # The service should be robust enough to handle this internally.
        logger.error(
            f"Error processing sample callback for {callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}

@router.post(
    "/final-result",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Final Generation Callback"
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to call when final asset generation is complete.
    This endpoint is secured by a shared secret in the 'X-Callback-Secret' header.
    """
    logger.info(f"Received final result callback for request ID: {callback_payload.generation_request_id}")
    try:
        await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
    except Exception as e:
        logger.error(
            f"Error processing final result callback for {callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}

@router.post(
    "/error",
    status_code=status.HTTP_200_OK,
    summary="Handle n8n Error Callback"
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
):
    """
    Webhook endpoint for n8n to call when an error occurs during workflow execution.
    This endpoint is secured by a shared secret in the 'X-Callback-Secret' header.
    """
    logger.warning(f"Received error callback for request ID: {callback_payload.generation_request_id}. Message: {callback_payload.error_message}")
    try:
        await orchestration_svc.handle_n8n_error(callback_payload)
    except Exception as e:
        logger.error(
            f"Error processing error callback for {callback_payload.generation_request_id}: {e}",
            exc_info=True
        )
    return {"status": "received"}