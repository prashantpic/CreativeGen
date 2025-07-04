from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.authentication import get_current_authenticated_user, AuthenticatedUser
from api.dependencies.common import get_webhook_service
from api.schemas.webhook_schemas import (
    WebhookCreateSchema,
    WebhookUpdateSchema,
    WebhookResponseSchema,
)
from api.schemas.base_schemas import StatusResponseSchema
from application.services.webhook_service import WebhookService
from core.exceptions import WebhookNotFoundError, InvalidUserInputError

# Management of Webhooks requires an authenticated user session.
router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    dependencies=[Depends(get_current_authenticated_user)],
)


@router.post(
    "/",
    response_model=WebhookResponseSchema,
    status_code=201,
    summary="Register a new Webhook",
    description="Creates a new webhook subscription for the authenticated user for specific event types."
)
async def register_webhook(
    payload: WebhookCreateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Registers a new webhook endpoint.
    """
    try:
        webhook = await service.register_webhook(
            user_id=user.id,
            target_url=str(payload.target_url),
            event_types=[e.value for e in payload.event_types],
            secret=payload.secret
        )
        return WebhookResponseSchema.model_validate(webhook)
    except InvalidUserInputError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/",
    response_model=List[WebhookResponseSchema],
    summary="List Webhooks",
    description="Retrieves a list of all active webhooks for the authenticated user."
)
async def list_webhooks(
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> List[WebhookResponseSchema]:
    """
    Lists all webhooks for the authenticated user.
    """
    webhooks = await service.list_webhooks_for_user(user_id=user.id)
    return [WebhookResponseSchema.model_validate(wh) for wh in webhooks]


@router.get(
    "/{webhook_id}",
    response_model=WebhookResponseSchema,
    summary="Get Webhook Details",
    description="Retrieves details for a specific webhook belonging to the authenticated user."
)
async def get_webhook(
    webhook_id: UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Retrieves details for a specific webhook, ensuring it belongs to the user.
    """
    try:
        webhook = await service.get_webhook_by_id(webhook_id=webhook_id, user_id=user.id)
        return WebhookResponseSchema.model_validate(webhook)
    except WebhookNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put(
    "/{webhook_id}",
    response_model=WebhookResponseSchema,
    summary="Update a Webhook",
    description="Updates the configuration of a specific webhook."
)
async def update_webhook(
    webhook_id: UUID,
    payload: WebhookUpdateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Updates a webhook's properties, ensuring it belongs to the user.
    """
    try:
        update_data = payload.model_dump(exclude_unset=True)
        # Convert enums to strings if they are present
        if 'event_types' in update_data and update_data['event_types'] is not None:
            update_data['event_types'] = [e.value for e in update_data['event_types']]
        
        updated_webhook = await service.update_webhook(
            webhook_id=webhook_id,
            user_id=user.id,
            update_data=update_data
        )
        return WebhookResponseSchema.model_validate(updated_webhook)
    except (WebhookNotFoundError, InvalidUserInputError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete(
    "/{webhook_id}",
    response_model=StatusResponseSchema,
    summary="Delete a Webhook",
    description="Deletes a webhook subscription."
)
async def delete_webhook(
    webhook_id: UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> StatusResponseSchema:
    """
    Deletes a webhook, ensuring it belongs to the user.
    """
    try:
        await service.delete_webhook(webhook_id=webhook_id, user_id=user.id)
        return StatusResponseSchema(status="success", message="Webhook has been deleted.")
    except WebhookNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)