```python
import uuid
from typing import List, Optional, Protocol

from domain.models.webhook import Webhook, WebhookEvent


class IWebhookRepository(Protocol):
    """
    Interface for Webhook data persistence operations.
    """

    async def add(self, webhook: Webhook) -> None:
        """Saves a new Webhook to the data store."""
        ...

    async def get_by_id(self, webhook_id: uuid.UUID) -> Optional[Webhook]:
        """Retrieves a Webhook by its unique identifier."""
        ...

    async def list_by_user_id(self, user_id: uuid.UUID) -> List[Webhook]:
        """Retrieves all Webhooks for a specific user."""
        ...

    async def list_by_user_id_and_event_type(
        self, user_id: uuid.UUID, event_type: WebhookEvent
    ) -> List[Webhook]:
        """Retrieves all Webhooks for a user subscribed to a specific event."""
        ...

    async def update(self, webhook: Webhook) -> None:
        """Updates an existing Webhook in the data store."""
        ...

    async def delete(self, webhook_id: uuid.UUID) -> None:
        """Deletes a Webhook from the data store."""
        ...
```