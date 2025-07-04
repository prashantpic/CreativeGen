import uuid
from typing import Any, Dict, List, Optional

from pydantic import HttpUrl

from ....developer_platform.core import exceptions
from ....developer_platform.domain.models.webhook import (
    Webhook as WebhookDomainModel,
)
from ....developer_platform.domain.models.webhook import WebhookEvent
from ....developer_platform.domain.repositories.webhook_repository import (
    IWebhookRepository,
)
from ....developer_platform.infrastructure.messaging.webhook_publisher import (
    WebhookPublisher,
)
from ....developer_platform.infrastructure.security import hashing


class WebhookService:
    """
    Handles business logic for webhook registration, management, and event triggering.
    """

    def __init__(
        self,
        webhook_repo: IWebhookRepository,
        webhook_publisher: WebhookPublisher,
    ):
        """
        Initializes the WebhookService.

        Args:
            webhook_repo: The repository for accessing webhook data.
            webhook_publisher: The client for publishing webhook events to a message queue.
        """
        self.webhook_repo = webhook_repo
        self.webhook_publisher = webhook_publisher

    async def register_webhook(
        self,
        user_id: uuid.UUID,
        target_url: HttpUrl,
        event_types: List[str],
        secret: Optional[str] = None,
    ) -> WebhookDomainModel:
        """
        Registers a new webhook for a user.

        Args:
            user_id: The ID of the user registering the webhook.
            target_url: The URL to which webhook events will be sent.
            event_types: A list of event types to subscribe to.
            secret: An optional secret for signing webhook payloads.

        Returns:
            The created Webhook domain model.
        """
        hashed_secret = hashing.hash_secret(secret) if secret else None

        # Validate event types against the domain enum
        valid_event_types = [WebhookEvent(et) for et in event_types]

        webhook_domain = WebhookDomainModel(
            user_id=user_id,
            target_url=target_url,
            event_types=valid_event_types,
            hashed_secret=hashed_secret,
        )
        await self.webhook_repo.add(webhook_domain)
        return webhook_domain

    async def trigger_event_for_user_webhooks(
        self, user_id: uuid.UUID, event_type: WebhookEvent, payload: Dict[str, Any]
    ):
        """
        Finds all webhooks for a user subscribed to a specific event and
        triggers them by publishing to the message queue.

        Args:
            user_id: The ID of the user who owns the webhooks.
            event_type: The type of event that occurred.
            payload: The data payload associated with the event.
        """
        webhooks = await self.webhook_repo.list_by_user_id_and_event_type(
            user_id, event_type
        )
        for webhook in webhooks:
            if webhook.is_active:
                await self.webhook_publisher.publish_webhook_event(
                    webhook=webhook, event_type=event_type.value, payload=payload
                )

    async def list_webhooks_for_user(self, user_id: uuid.UUID) -> List[WebhookDomainModel]:
        """
        Lists all webhooks for a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of Webhook domain models.
        """
        return await self.webhook_repo.list_by_user_id(user_id)

    async def get_webhook_by_id(
        self, webhook_id: uuid.UUID, user_id: uuid.UUID
    ) -> WebhookDomainModel:
        """
        Retrieves a single webhook by its ID, ensuring user ownership.

        Args:
            webhook_id: The ID of the webhook to retrieve.
            user_id: The ID of the user making the request.

        Returns:
            The Webhook domain model.

        Raises:
            WebhookNotFoundError: If the webhook is not found or not owned by the user.
        """
        webhook = await self.webhook_repo.get_by_id(webhook_id)
        if not webhook or webhook.user_id != user_id:
            raise exceptions.WebhookNotFoundError()
        return webhook

    async def update_webhook(
        self,
        webhook_id: uuid.UUID,
        user_id: uuid.UUID,
        target_url: Optional[HttpUrl] = None,
        event_types: Optional[List[str]] = None,
        secret: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> WebhookDomainModel:
        """
        Updates an existing webhook.

        Args:
            webhook_id: The ID of the webhook to update.
            user_id: The ID of the user making the request.
            target_url: The new target URL.
            event_types: The new list of event types.
            secret: A new secret. If provided, the old one will be replaced.
            is_active: The new active status.

        Returns:
            The updated Webhook domain model.
        """
        webhook = await self.get_webhook_by_id(webhook_id, user_id)

        if target_url is not None:
            webhook.target_url = target_url
        if event_types is not None:
            webhook.event_types = [WebhookEvent(et) for et in event_types]
        if secret is not None:
            webhook.hashed_secret = hashing.hash_secret(secret)
        if is_active is not None:
            webhook.is_active = is_active

        await self.webhook_repo.update(webhook)
        return webhook

    async def delete_webhook(self, webhook_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """
        Deletes a webhook.

        Args:
            webhook_id: The ID of the webhook to delete.
            user_id: The ID of the user making the request.
        """
        # Ensure the user owns the webhook before deleting
        await self.get_webhook_by_id(webhook_id, user_id)
        await self.webhook_repo.delete(webhook_id)