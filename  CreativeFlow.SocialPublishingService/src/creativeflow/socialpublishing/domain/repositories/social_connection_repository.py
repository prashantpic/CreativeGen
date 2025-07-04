"""
Interface for the SocialConnection repository.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..models.social_connection import SocialConnection


class ISocialConnectionRepository(ABC):
    """
    Defines the contract for data access operations related to
    SocialConnection entities. This is an abstract interface that will be
    implemented by the infrastructure layer.
    """

    @abstractmethod
    async def get_by_id(self, connection_id: UUID) -> Optional[SocialConnection]:
        """Retrieves a social connection by its unique ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_and_platform(
        self, user_id: str, platform: str
    ) -> Optional[SocialConnection]:
        """Retrieves a social connection for a specific user and platform."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> List[SocialConnection]:
        """Lists all social connections for a given user."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, connection: SocialConnection) -> SocialConnection:
        """Saves (creates or updates) a social connection."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, connection_id: UUID) -> None:
        """Deletes a social connection by its ID."""
        raise NotImplementedError