from typing import List, Optional, Protocol, Tuple
from uuid import UUID

from ..models.api_key import APIKey


class IApiKeyRepository(Protocol):
    """
    Interface for APIKey repository defining data access methods.
    This contract ensures that any data persistence implementation for API Keys
    adheres to the required methods for the application layer.
    """

    async def add(self, api_key: APIKey) -> None:
        """
        Adds a new APIKey domain object to the data store.

        Args:
            api_key: The APIKey domain model instance to persist.
        """
        ...

    async def get_by_id(
        self, api_key_id: UUID, user_id: Optional[UUID] = None
    ) -> Optional[APIKey]:
        """
        Retrieves an APIKey by its unique identifier.

        Args:
            api_key_id: The UUID of the API key.
            user_id: Optional user UUID to ensure ownership.

        Returns:
            An APIKey domain model instance if found, otherwise None.
        """
        ...

    async def get_by_key_prefix(self, key_prefix: str) -> Optional[APIKey]:
        """
        Retrieves an APIKey by its unique key prefix. This is the primary
        method for looking up a key during authentication.

        Args:
            key_prefix: The unique prefix of the API key.

        Returns:
            An APIKey domain model instance if found, otherwise None.
        """
        ...

    async def list_by_user_id(self, user_id: UUID) -> List[APIKey]:
        """
        Lists all API keys belonging to a specific user.

        Args:
            user_id: The UUID of the user.

        Returns:
            A list of APIKey domain model instances.
        """
        ...

    async def update(self, api_key: APIKey) -> APIKey:
        """
        Updates an existing APIKey in the data store.

        Args:
            api_key: The APIKey domain model instance with updated values.
        
        Returns:
            The updated APIKey domain model instance.
        """
        ...