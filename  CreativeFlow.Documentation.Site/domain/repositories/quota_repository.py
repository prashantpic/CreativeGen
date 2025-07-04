```python
import uuid
from typing import Optional, Protocol

from domain.models.usage import Quota


class IQuotaRepository(Protocol):
    """Interface for Quota data persistence operations."""

    async def save(self, quota: Quota) -> None:
        """Saves or updates a quota configuration."""
        ...

    async def get_quota_for_client(self, user_id: uuid.UUID) -> Optional[Quota]:
        """
        Retrieves the quota configuration for a given client, typically
        identified by their user ID as quotas are often user-level.
        """
        ...
```