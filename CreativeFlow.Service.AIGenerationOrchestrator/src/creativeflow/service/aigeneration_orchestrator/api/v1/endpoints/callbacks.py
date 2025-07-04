"""
Defines the FastAPI router for handling asynchronous callbacks from the n8n
Workflow Engine. This includes endpoints for receiving sample previews and
final asset URLs.
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status

from ....service.aigeneration_orchestrator.app.dtos import N8NCallbackDTO
from ....service.aigeneration_orchestrator.app.use_cases.process_n8n_result import (
    GenerationNotFoundError, ProcessN8NResultUseCase)
from ....service.aigeneration_orchestrator.config.settings import settings
from ..dependencies import get_process_n8n_result_use_case

router = APIRouter()


async def verify_webhook_secret(x_n8n_webhook_secret: str | None = Header(None)):
    """
    Security dependency to verify the webhook secret if it's configured.
    Compares the incoming header with the secret stored in settings.
    """
    if settings.N8N_CALLBACK_SECRET:
        if not x_n8n_webhook_secret:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-N8N-Webhook-Secret header",
            )
        if x_n8n_webhook_secret != settings.N8N_CALLBACK_SECRET:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid webhook secret",
            )


@router.post(
    "/n8n",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_webhook_secret)],
    summary="n8n Workflow Callback",
    description="A webhook endpoint for the n8n workflow engine to post back results.",
    responses={
        200: {"description": "Callback processed successfully"},
        400: {"description": "Invalid payload"},
        403: {"description": "Invalid or missing webhook secret"},
        404: {"description": "Generation ID does not exist"},
        500: {"description": "Error while processing the callback"},
    },
)
async def handle_n8n_result_callback(
    payload: N8NCallbackDTO,
    use_case: ProcessN8NResultUseCase = Depends(get_process_n8n_result_use_case),
):
    """
    Handles the webhook POST request from n8n.

    It depends on the `ProcessN8NResultUseCase` to handle the business logic
    of updating the generation status and notifying other services.
    """
    try:
        await use_case.execute(payload)
        return Response(status_code=status.HTTP_200_OK)
    except GenerationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the callback.",
        ) from e