```python
import uuid
from typing import List, Optional

from core.exceptions import ForbiddenError, WebhookNotFoundError
from domain.models.webhook import Webhook, WebhookEvent
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.messaging.webhook_publisher import IWebhookPublisher
from infrastructure.security.hashing import hash_secret
from pydantic import HttpUrl


class WebhookService:
    """
    Handles business logic for webhook management and event triggering.
    """

    def __init__(
        self,
        webhook_repo: IWebhookRepository,
        webhook_publisher: IWebhookPublisher,
    ):
        self.webhook_repo = webhook_repo
        self.webhook_publisher = webhook_publisher

    async def register_webhook(
        self,
        user_id: uuid.UUID,
        target_url: str,
        event_types: List[str],
        secret: Optional[str] = None,
    ) -> Webhook:
        """Creates and saves a new webhook subscription."""
        hashed_secret = hash_secret(secret) if secret else None

        # Validate event types against the Enum
        valid_event_types = [WebhookEvent(et) for et in event_types]

        webhook = Webhook(
            user_id=user_id,
            target_url=HttpUrl(target_url),
            event_types=valid_event_types,
            hashed_secret=hashed_secret,
        )
        await self.webhook_repo.add(webhook)
        return webhook

    async def list_webhooks_for_user(self, user_id: uuid.UUID) -> List[Webhook]:
        """Lists all webhooks for a given user."""
        return await self.webhook_repo.list_by_user_id(user_id)

    async def get_webhook_by_id(
        self, webhook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Webhook:
        """
        Gets a webhook by ID, ensuring ownership.
        """
        webhook = await self.webhook_repo.get_by_id(webhook_id)
        if not webhook:
            raise WebhookNotFoundError()
        if webhook.user_id != user_id:
            raise ForbiddenError("You do not have permission to access this webhook.")
        return webhook

    async def update_webhook(
        self,
        webhook_id: uuid.UUID,
        user_id: uuid.UUID,
        target_url: Optional[str],
        event_types: Optional[List[str]],
        secret: Optional[str],
        is_active: Optional[bool],
    ) -> Webhook:
        """Updates a webhook's configuration."""
        webhook_to_update = await self.get_webhook_by_id(webhook_id, user_id)

        if target_url is not None:
            webhook_to_update.target_url = HttpUrl(target_url)
        if event_types is not None:
            webhook_to_update.event_types = [WebhookEvent(et) for et in event_types]
        if secret is not None:
            # If secret is updated, re-hash it
            webhook_to_update.hashed_secret = hash_secret(secret)
        if is_active is not None:
            webhook_to_update.is_active = is_active

        await self.webhook_repo.update(webhook_to_update)
        return webhook_to_update

    async def delete_webhook(self, webhook_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """Deletes a webhook."""
        # Ensure user owns the webhook before deleting
        await self.get_webhook_by_id(webhook_id, user_id)
        await self.webhook_repo.delete(webhook_id)

    async def trigger_event_for_user_webhooks(
        self, user_id: uuid.UUID, event_type: WebhookEvent, payload: dict
    ) -> None:
        """
        Finds all active webhooks for a user and a specific event,
        and publishes them to the message queue.
        This method would be called by other services when an event occurs.
        """
        webhooks = await self.webhook_repo.list_by_user_id_and_event_type(
            user_id, event_type
        )
        for webhook in webhooks:
            if webhook.is_active:
                await self.webhook_publisher.publish_webhook_event(
                    webhook=webhook, event_type=event_type.value, payload=payload
                )
```