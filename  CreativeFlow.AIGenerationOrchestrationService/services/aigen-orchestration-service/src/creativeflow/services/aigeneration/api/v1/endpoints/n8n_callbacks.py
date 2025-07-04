"""
FastAPI router for handling asynchronous callbacks from the n8n Workflow Engine.

These endpoints are crucial for updating the status of generation requests
as they are processed by the n8n workflows. They receive results, errors,
and status updates, and delegate processing to the OrchestrationService.
"""

import logging
from typing import Optional, Dict

from fastapi import APIRouter, Depends, Header, HTTPException, status

from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service
from creativeflow.services.aigeneration.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


async def verify_n8n_secret(x_callback_secret: Optional[str] = Header(None)):
    """
    Dependency to verify a shared secret from n8n callbacks.

    This provides a basic layer of security to ensure that callbacks originate
    from a trusted source (n8n).
    """
    if settings.N8N_CALLBACK_SECRET:
        if x_callback_secret is None:
            logger.warning("N8N callback received without secret header.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="X-Callback-Secret header is missing."
            )
        if x_callback_secret != settings.N8N_CALLBACK_SECRET:
            logger.error("N8N callback received with invalid secret.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid X-Callback-Secret."
            )
    else:
        # In development or non-production environments, the secret may not be set.
        logger.warning("N8N_CALLBACK_SECRET is not set. Skipping callback verification.")


@router.post(
    "/sample-result",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Handle n8n sample generation callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> Dict[str, str]:
    """
    Webhook endpoint for n8n to post the results of a sample generation job.
    """
    logger.info("Received n8n sample result callback for request ID: %s", callback_payload.generation_request_id)
    try:
        await orchestration_svc.process_n8n_sample_callback(callback_payload)
        return {"status": "received"}
    except Exception as e:
        # Log the error but still return a 200 OK to n8n to prevent retries.
        # The error needs to be handled internally (e.g., via monitoring and alerts).
        logger.error(
            "Error processing n8n sample callback for request %s: %s",
            callback_payload.generation_request_id, e, exc_info=True
        )
        # Returning a 200 OK with an error status in the body is a robust
        # webhook pattern that prevents the sender from endlessly retrying.
        return {"status": "error_processing"}


@router.post(
    "/final-result",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Handle n8n final generation callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> Dict[str, str]:
    """
    Webhook endpoint for n8n to post the results of a final asset generation job.
    """
    logger.info("Received n8n final result callback for request ID: %s", callback_payload.generation_request_id)
    try:
        await orchestration_svc.process_n8n_final_asset_callback(callback_payload)
        return {"status": "received"}
    except Exception as e:
        logger.error(
            "Error processing n8n final result callback for request %s: %s",
            callback_payload.generation_request_id, e, exc_info=True
        )
        return {"status": "error_processing"}


@router.post(
    "/error",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Handle n8n error callback",
    dependencies=[Depends(verify_n8n_secret)],
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
) -> Dict[str, str]:
    """
    Webhook endpoint for n8n to report an error during a generation job.
    """
    logger.warning(
        "Received n8n error callback for request ID: %s. Error: %s",
        callback_payload.generation_request_id,
        callback_payload.error_message
    )
    try:
        await orchestration_svc.handle_n8n_error(callback_payload)
        return {"status": "received"}
    except Exception as e:
        logger.error(
            "Error processing n8n error callback for request %s: %s",
            callback_payload.generation_request_id, e, exc_info=True
        )
        return {"status": "error_processing"}