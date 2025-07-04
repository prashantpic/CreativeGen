from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest

class IGenerationRequestRepository(ABC):
    """
    Interface (Abstract Base Class) for the GenerationRequest repository.
    Defines the contract for data access operations related to GenerationRequest entities.
    """

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """
        Retrieves a GenerationRequest by its unique ID.
        
        :param request_id: The UUID of the generation request.
        :return: A GenerationRequest object or None if not found.
        """
        pass

    @abstractmethod
    async def add(self, generation_request: GenerationRequest) -> None:
        """
        Adds a new GenerationRequest to the repository.
        
        :param generation_request: The GenerationRequest object to add.
        """
        pass

    @abstractmethod
    async def update(self, generation_request: GenerationRequest) -> None:
        """
        Updates an existing GenerationRequest in the repository.
        
        :param generation_request: The GenerationRequest object with updated values.
        """
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """
        Lists all GenerationRequests for a specific user, with pagination.
        
        :param user_id: The ID of the user.
        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of GenerationRequest objects.
        """
        pass