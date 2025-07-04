"""
Interface for the PublishJob repository.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..models.publish_job import PublishJob


class IPublishJobRepository(ABC):
    """
    Defines the contract for data access operations related to PublishJob entities.
    This interface will be implemented by the infrastructure layer.
    """

    @abstractmethod
    async def get_by_id(self, job_id: UUID) -> Optional[PublishJob]:
        """Retrieves a publishing job by its unique ID."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(
        self, user_id: str, platform: Optional[str] = None, status: Optional[str] = None
    ) -> List[PublishJob]:
        """Lists all publishing jobs for a given user, with optional filters."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, job: PublishJob) -> PublishJob:
        """Saves (creates or updates) a publishing job."""
        raise NotImplementedError

    @abstractmethod
    async def find_pending_scheduled_jobs(self, limit: int = 100) -> List[PublishJob]:
        """
        Finds jobs that are scheduled to be published.

        This fetches jobs where status is 'Scheduled' and scheduled_at <= now.
        """
        raise NotImplementedError