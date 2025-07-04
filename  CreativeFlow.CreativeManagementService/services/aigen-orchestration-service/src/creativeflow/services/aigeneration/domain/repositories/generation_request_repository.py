"""
Interface (abstract base class) for the GenerationRequest repository.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest


class IGenerationRequestRepository(ABC):
    """
    Defines the contract for data access operations related to GenerationRequest entities.
    This follows the Dependency Inversion Principle, allowing the application layer to
    depend on this abstraction rather than a concrete implementation.
    """

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """
        Retrieves a GenerationRequest by its unique ID.
        
        :param request_id: The UUID of the request.
        :return: A GenerationRequest object or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, generation_request: GenerationRequest) -> None:
        """
        Adds a new GenerationRequest to the persistence layer.
        
        :param generation_request: The GenerationRequest object to add.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, generation_request: GenerationRequest) -> None:
        """
        Updates an existing GenerationRequest in the persistence layer.
        
        :param generation_request: The GenerationRequest object with updated values.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """
        Lists all GenerationRequests for a specific user, with pagination.
        
        :param user_id: The ID of the user.
        :param skip: The number of records to skip for pagination.
        :param limit: The maximum number of records to return.
        :return: A list of GenerationRequest objects.
        """
        raise NotImplementedError