"""
Defines abstract base classes (interfaces) for external dependencies like the
database repository, message publisher, and other microservices. This enables
dependency inversion, decoupling business logic from concrete implementations.
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from ..domain.models.generation_request import GenerationRequest


class IGenerationRepository(ABC):
    """
    Interface for data access logic for the GenerationRequest entity.
    """
    @abstractmethod
    async def add(self, generation_request: GenerationRequest) -> None:
        """Persists a new GenerationRequest entity."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest entity by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest entity."""
        raise NotImplementedError


class IJobPublisher(ABC):
    """
    Interface for publishing jobs to a message queue.
    """
    @abstractmethod
    async def publish_generation_job(self, job_payload: Dict[str, Any]) -> None:
        """Publishes a generation job to the queue."""
        raise NotImplementedError


class ICreditService(ABC):
    """
    Interface for interacting with the external credit management service.
    """
    @abstractmethod
    async def check_and_reserve_credits(self, user_id: UUID, amount: Decimal) -> bool:
        """Checks if a user has enough credits and reserves them."""
        raise NotImplementedError

    @abstractmethod
    async def deduct_credits(self, user_id: UUID, generation_id: UUID, amount: Decimal) -> None:
        """Deducts a specified amount of credits from a user's balance."""
        raise NotImplementedError

    @abstractmethod
    async def refund_credits(self, user_id: UUID, generation_id: UUID, amount: Decimal) -> None:
        """Refunds a specified amount of credits to a user's balance."""
        raise NotImplementedError


class INotificationService(ABC):
    """
    Interface for sending notifications to users.
    """
    @abstractmethod
    async def notify_user(self, user_id: UUID, message: Dict[str, Any]) -> None:
        """Sends a notification to a specific user."""
        raise NotImplementedError