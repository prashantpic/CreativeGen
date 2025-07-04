from typing import Optional, Protocol
from uuid import UUID

from ..models.usage import Quota


class IQuotaRepository(Protocol):
    """
    Interface for Quota repository defining data access methods.
    This contract handles the persistence of quota configurations for clients.
    """

    async def save(self, quota: Quota) -> Quota:
        """
        Saves or updates a Quota domain object in the data store.

        Args:
            quota: The Quota domain model instance to persist.
        
        Returns:
            The persisted Quota domain model instance.
        """
        ...

    async def get_by_client_id(self, api_client_id: UUID) -> Optional[Quota]:
        """
        Retrieves the quota configuration for a specific API client.

        Args:
            api_client_id: The UUID of the API client (from the APIKey).

        Returns:
            A Quota domain model instance if a specific quota is configured,
            otherwise None.
        """
        ...