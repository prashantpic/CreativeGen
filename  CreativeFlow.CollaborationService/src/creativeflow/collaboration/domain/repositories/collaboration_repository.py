from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from uuid import UUID

# Placeholders for domain models and value objects
SessionId = TypeVar('SessionId', bound=UUID)
UserId = TypeVar('UserId', bound=str)
CollaborationSession = TypeVar('CollaborationSession')
Presence = TypeVar('Presence')

class ICollaborationSessionRepository(ABC, Generic[SessionId, CollaborationSession]):
    """
    Interface for a repository managing CollaborationSession aggregates.
    A collaboration session represents a live, shared document editing instance.
    """

    @abstractmethod
    async def get_by_id(self, session_id: SessionId) -> Optional[CollaborationSession]:
        """
        Retrieves a collaboration session by its unique identifier.

        Args:
            session_id (SessionId): The unique ID of the session.

        Returns:
            Optional[CollaborationSession]: The session aggregate if found, else None.
        """
        pass

    @abstractmethod
    async def save(self, session: CollaborationSession) -> None:
        """
        Saves a collaboration session (either creating a new one or updating an existing one).

        Args:
            session (CollaborationSession): The session aggregate to save.
        """
        pass

    @abstractmethod
    async def delete(self, session_id: SessionId) -> None:
        """
        Deletes a collaboration session by its unique identifier.

        Args:
            session_id (SessionId): The unique ID of the session to delete.
        """
        pass


class IPresenceRepository(ABC, Generic[SessionId, UserId, Presence]):
    """
    Interface for a repository managing user presence information within sessions.
    Presence indicates which users are currently active in a session and may include
    cursor position or other ephemeral state.
    """

    @abstractmethod
    async def get_presence(self, session_id: SessionId, user_id: UserId) -> Optional[Presence]:
        """
        Retrieves the presence state for a specific user in a specific session.

        Args:
            session_id (SessionId): The ID of the collaboration session.
            user_id (UserId): The ID of the user.

        Returns:
            Optional[Presence]: The user's presence information if it exists, else None.
        """
        pass

    @abstractmethod
    async def save_presence(self, presence: Presence) -> None:
        """
        Saves a user's presence information.
        This is typically a write-through operation to a fast data store like Redis,
        often with a time-to-live (TTL) to automatically expire stale presence.

        Args:
            presence (Presence): The presence entity to save.
        """
        pass

    @abstractmethod
    async def get_all_in_session(self, session_id: SessionId) -> List[Presence]:
        """
        Retrieves all active presence states for a given session.

        Args:
            session_id (SessionId): The ID of the collaboration session.

        Returns:
            List[Presence]: A list of all active presence information for the session.
        """
        pass

    @abstractmethod
    async def delete_presence(self, session_id: SessionId, user_id: UserId) -> None:
        """
        Explicitly deletes a user's presence information from a session.
        This is typically called on user disconnect.

        Args:
            session_id (SessionId): The ID of the collaboration session.
            user_id (UserId): The ID of the user whose presence to delete.
        """
        pass