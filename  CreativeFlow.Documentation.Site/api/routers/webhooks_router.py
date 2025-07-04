```python
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from api.dependencies.authentication import (
    AuthenticatedUser,
    get_current_authenticated_user,
)
from api.dependencies.common import get_webhook_service
from api.schemas.base_schemas import StatusResponseSchema
from api.schemas.webhook_schemas import (
    WebhookCreateSchema,
    WebhookResponseSchema,
    WebhookUpdateSchema,
)
from application.services.webhook_service import WebhookService
from core.exceptions import ForbiddenError, WebhookNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks (Management)"],
    dependencies=[Depends(get_current_authenticated_user)],
)


@router.post(
    "/",
    response_model=WebhookResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new Webhook",
)
async def register_webhook(
    payload: WebhookCreateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Registers a new webhook endpoint for the authenticated user to receive
    notifications for specific event types.
    """
    logger.info(f"User {user.id} registering webhook for URL '{payload.target_url}'.")
    webhook = await service.register_webhook(
        user_id=user.id,
        target_url=str(payload.target_url),
        event_types=payload.event_types,
        secret=payload.secret,
    )
    # The response schema doesn't include the secret, which is correct.
    return WebhookResponseSchema.model_validate(webhook)


@router.get(
    "/",
    response_model=List[WebhookResponseSchema],
    summary="List all Webhooks for the user",
)
async def list_webhooks(
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> List[WebhookResponseSchema]:
    """
    Retrieves a list of all webhooks registered by the authenticated user.
    """
    logger.info(f"User {user.id} requesting list of their webhooks.")
    webhooks = await service.list_webhooks_for_user(user_id=user.id)
    return [WebhookResponseSchema.model_validate(w) for w in webhooks]


@router.get(
    "/{webhook_id}",
    response_model=WebhookResponseSchema,
    summary="Get a specific Webhook",
)
async def get_webhook(
    webhook_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Retrieves details for a single webhook by its ID.
    Ensures the webhook belongs to the authenticated user.
    """
    logger.info(f"User {user.id} requesting details for webhook {webhook_id}.")
    webhook = await service.get_webhook_by_id(webhook_id=webhook_id)
    if not webhook or webhook.user_id != user.id:
        raise WebhookNotFoundError()
    return WebhookResponseSchema.model_validate(webhook)


@router.put(
    "/{webhook_id}",
    response_model=WebhookResponseSchema,
    summary="Update a Webhook",
)
async def update_webhook(
    webhook_id: uuid.UUID,
    payload: WebhookUpdateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> WebhookResponseSchema:
    """
    Updates the properties of an existing webhook, such as its target URL,
    event subscriptions, secret, or active status.
    """
    logger.info(f"User {user.id} updating webhook {webhook_id}.")
    # Verify ownership first
    webhook_to_update = await service.get_webhook_by_id(webhook_id=webhook_id)
    if not webhook_to_update or webhook_to_update.user_id != user.id:
        raise WebhookNotFoundError()

    updated_webhook = await service.update_webhook(
        webhook_id=webhook_id,
        target_url=str(payload.target_url) if payload.target_url else None,
        event_types=payload.event_types,
        secret=payload.secret,
        is_active=payload.is_active,
    )
    return WebhookResponseSchema.model_validate(updated_webhook)


@router.delete(
    "/{webhook_id}",
    response_model=StatusResponseSchema,
    summary="Delete a Webhook",
)
async def delete_webhook(
    webhook_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: WebhookService = Depends(get_webhook_service),
) -> StatusResponseSchema:
    """
    Deletes a webhook registration. The endpoint will no longer receive notifications.
    """
    logger.info(f"User {user.id} deleting webhook {webhook_id}.")
    # Verify ownership
    webhook_to_delete = await service.get_webhook_by_id(webhook_id)
    if not webhook_to_delete:
        logger.warning(f"Attempt to delete non-existent webhook {webhook_id}.")
        return StatusResponseSchema(message="Webhook deleted successfully.")

    if webhook_to_delete.user_id != user.id:
        raise ForbiddenError("You can only delete your own webhooks.")

    await service.delete_webhook(webhook_id=webhook_id)
    return StatusResponseSchema(message="Webhook deleted successfully.")
```