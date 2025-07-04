import logging
from fastapi import APIRouter, Depends, status

from creativeflow.services.aigeneration.core.dependencies import get_orchestration_service, verify_n8n_callback_secret
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.api.v1 import schemas
from creativeflow.services.aigeneration.application import dtos

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/sample-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Sample Generation Callback"
)
async def handle_n8n_sample_generation_callback(
    callback_payload: schemas.N8NSampleResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
    is_secure: bool = Depends(verify_n8n_callback_secret)
):
    """
    Webhook endpoint for n8n to post the results of sample generation.
    """
    logger.info(f"Received sample result callback for request_id: {callback_payload.generation_request_id}")
    internal_dto = dtos.N8NSampleResultInternal(
        generation_request_id=callback_payload.generation_request_id,
        samples=[
            dtos.AssetInfoInternal(**sample.dict()) for sample in callback_payload.samples
        ]
    )
    await orchestration_svc.process_n8n_sample_callback(internal_dto)
    return {"status": "received"}


@router.post(
    "/final-result",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Final Generation Callback"
)
async def handle_n8n_final_generation_callback(
    callback_payload: schemas.N8NFinalResultPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
    is_secure: bool = Depends(verify_n8n_callback_secret)
):
    """
    Webhook endpoint for n8n to post the result of final asset generation.
    """
    logger.info(f"Received final result callback for request_id: {callback_payload.generation_request_id}")
    internal_dto = dtos.N8NFinalResultInternal(
        generation_request_id=callback_payload.generation_request_id,
        final_asset=dtos.AssetInfoInternal(**callback_payload.final_asset.dict())
    )
    await orchestration_svc.process_n8n_final_asset_callback(internal_dto)
    return {"status": "received"}


@router.post(
    "/error",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Handle n8n Error Callback"
)
async def handle_n8n_error_callback(
    callback_payload: schemas.N8NErrorPayload,
    orchestration_svc: OrchestrationService = Depends(get_orchestration_service),
    is_secure: bool = Depends(verify_n8n_callback_secret)
):
    """
    Webhook endpoint for n8n to report an error during workflow execution.
    """
    logger.error(
        f"Received error callback for request_id: {callback_payload.generation_request_id}. "
        f"Message: {callback_payload.error_message}"
    )
    internal_dto = dtos.N8NErrorInternal(
        generation_request_id=callback_payload.generation_request_id,
        error_code=callback_payload.error_code,
        error_message=callback_payload.error_message,
        error_details=callback_payload.error_details,
        failed_stage=callback_payload.failed_stage
    )
    await orchestration_svc.handle_n8n_error(internal_dto)
    return {"status": "received"}