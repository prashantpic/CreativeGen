from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest


class IGenerationRequestRepository(ABC):
    """
    An abstract interface defining the contract for data persistence
    operations related to the GenerationRequest aggregate.

    This decouples the application logic from the specific database implementation.
    """

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """
        Retrieves a GenerationRequest by its unique identifier.

        :param request_id: The UUID of the generation request.
        :return: A GenerationRequest domain object if found, otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, generation_request: GenerationRequest) -> None:
        """
        Adds a new GenerationRequest to the repository.

        :param generation_request: The GenerationRequest domain object to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, generation_request: GenerationRequest) -> None:
        """
        Updates an existing GenerationRequest in the repository.

        :param generation_request: The GenerationRequest domain object with updated state.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[GenerationRequest]:
        """
        Lists all GenerationRequests for a specific user, with pagination.

        :param user_id: The ID of the user.
        :param skip: The number of records to skip for pagination.
        :param limit: The maximum number of records to return.
        :return: A list of GenerationRequest domain objects.
        """
        raise NotImplementedError