import logging
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestDB

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL implementation of the IGenerationRequestRepository interface.
    Handles data access operations for GenerationRequest entities using SQLAlchemy.
    """

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    def _map_db_to_domain(self, db_obj: GenerationRequestDB) -> GenerationRequest:
        """Maps a SQLAlchemy DB model to a domain model."""
        return GenerationRequest.parse_obj(db_obj.__dict__)

    def _map_domain_to_db_dict(self, domain_obj: GenerationRequest) -> dict:
        """Maps a domain model to a dictionary suitable for DB insertion/update."""
        return domain_obj.dict()

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest entity by its unique identifier."""
        logger.debug(f"Fetching generation request with id: {request_id}")
        result = await self._db_session.get(GenerationRequestDB, request_id)
        if result:
            return self._map_db_to_domain(result)
        logger.warning(f"Generation request with id: {request_id} not found in DB.")
        return None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest entity to the database."""
        logger.info(f"Adding new generation request with id: {generation_request.id}")
        db_obj_data = self._map_domain_to_db_dict(generation_request)
        db_obj = GenerationRequestDB(**db_obj_data)
        self._db_session.add(db_obj)
        await self._db_session.flush()
        logger.info(f"Successfully added generation request {generation_request.id}")

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest entity in the database."""
        logger.info(f"Updating generation request with id: {generation_request.id}")
        
        # We need to fetch the existing object to update it in the session
        db_obj = await self._db_session.get(GenerationRequestDB, generation_request.id)
        if not db_obj:
            logger.error(f"Attempted to update a non-existent generation request: {generation_request.id}")
            # In a real app, might raise a custom DataConsistencyError
            raise ValueError("Cannot update a generation request that does not exist.")

        update_data = self._map_domain_to_db_dict(generation_request)
        
        for key, value in update_data.items():
            setattr(db_obj, key, value)
            
        await self._db_session.flush()
        logger.info(f"Successfully updated generation request {generation_request.id}")

    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists GenerationRequest entities for a specific user, with pagination."""
        logger.debug(f"Listing generation requests for user: {user_id} with skip: {skip}, limit: {limit}")
        
        query = (
            select(GenerationRequestDB)
            .where(GenerationRequestDB.user_id == user_id)
            .order_by(GenerationRequestDB.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        result = await self._db_session.execute(query)
        db_objects = result.scalars().all()
        
        return [self._map_db_to_domain(db_obj) for db_obj in db_objects]