from typing import List, Optional, Protocol
from uuid import UUID

from ..models.webhook import Webhook


class IWebhookRepository(Protocol):
    """
    Interface for Webhook repository defining data access methods.
    This contract ensures that any data persistence implementation for Webhooks
    adheres to the required methods for the application layer.
    """

    async def add(self, webhook: Webhook) -> None:
        """
        Adds a new Webhook domain object to the data store.

        Args:
            webhook: The Webhook domain model instance to persist.
        """
        ...

    async def get_by_id(
        self, webhook_id: UUID, user_id: Optional[UUID] = None
    ) -> Optional[Webhook]:
        """
        Retrieves a Webhook by its unique identifier.

        Args:
            webhook_id: The UUID of the webhook.
            user_id: Optional user UUID to ensure ownership.

        Returns:
            A Webhook domain model instance if found, otherwise None.
        """
        ...

    async def list_by_user_id(self, user_id: UUID) -> List[Webhook]:
        """
        Lists all Webhooks belonging to a specific user.

        Args:
            user_id: The UUID of the user.

        Returns:
            A list of Webhook domain model instances.
        """
        ...

    async def list_by_user_id_and_event_type(
        self, user_id: UUID, event_type: str
    ) -> List[Webhook]:
        """
        Lists all active webhooks for a user that are subscribed to a specific event type.

        Args:
            user_id: The UUID of the user.
            event_type: The event type string to match.

        Returns:
            A list of matching Webhook domain model instances.
        """
        ...

    async def update(self, webhook: Webhook) -> Webhook:
        """
        Updates an existing Webhook in the data store.

        Args:
            webhook: The Webhook domain model instance with updated values.
        
        Returns:
            The updated Webhook domain model instance.
        """
        ...

    async def delete(self, webhook_id: UUID, user_id: UUID) -> bool:
        """
        Deletes a webhook from the data store.

        Args:
            webhook_id: The UUID of the webhook to delete.
            user_id: The UUID of the user owning the webhook.

        Returns:
            True if a webhook was deleted, False otherwise.
        """
        ...