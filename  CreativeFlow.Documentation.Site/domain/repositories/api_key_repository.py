```python
import uuid
from typing import List, Optional, Protocol

from domain.models.api_key import APIKey


class IApiKeyRepository(Protocol):
    """Interface for API Key data persistence operations."""

    async def add(self, api_key: APIKey) -> None:
        """Saves a new API key to the database."""
        ...

    async def get_by_id(self, api_key_id: uuid.UUID) -> Optional[APIKey]:
        """Retrieves an API key by its unique ID."""
        ...

    async def get_by_key_prefix(self, key_prefix: str) -> Optional[APIKey]:
        """Retrieves an API key by its non-secret prefix."""
        ...

    async def list_by_user_id(self, user_id: uuid.UUID) -> List[APIKey]:
        """Lists all API keys belonging to a specific user."""
        ...

    async def update(self, api_key: APIKey) -> None:
        """Updates an existing API key in the database."""
        ...
```