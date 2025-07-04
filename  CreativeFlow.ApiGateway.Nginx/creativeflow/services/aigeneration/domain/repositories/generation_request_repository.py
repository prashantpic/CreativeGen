from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest


class IGenerationRequestRepository(ABC):
    """
    Interface (Abstract Base Class) for the GenerationRequest repository.
    Defines the contract for data persistence operations related to GenerationRequest entities,
    decoupling the domain logic from the specific database implementation.
    """

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """
        Retrieves a GenerationRequest by its unique identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, generation_request: GenerationRequest) -> None:
        """
        Adds a new GenerationRequest to the repository.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, generation_request: GenerationRequest) -> None:
        """
        Updates an existing GenerationRequest in the repository.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[GenerationRequest]:
        """
        Retrieves a list of GenerationRequests for a specific user, with pagination.
        """
        raise NotImplementedError