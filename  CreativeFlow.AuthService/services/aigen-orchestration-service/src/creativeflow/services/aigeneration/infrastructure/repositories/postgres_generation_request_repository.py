import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestModel

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL implementation of the IGenerationRequestRepository interface.
    Handles data access operations for GenerationRequest entities using SQLAlchemy.
    """

    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    def _map_to_domain(self, db_model: GenerationRequestModel) -> GenerationRequest:
        """Maps SQLAlchemy model to domain model."""
        return GenerationRequest.from_orm(db_model)

    def _map_to_db_dict(self, domain_model: GenerationRequest) -> dict:
        """Maps domain model to a dict for SQLAlchemy update/insert."""
        # Use Pydantic's dict method to handle JSON serialization correctly
        return domain_model.dict()

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest by its unique ID."""
        stmt = select(GenerationRequestModel).where(GenerationRequestModel.id == request_id)
        result = await self._db.execute(stmt)
        db_model = result.scalar_one_or_none()
        if db_model:
            return self._map_to_domain(db_model)
        return None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest to the database."""
        logger.debug(f"Adding new generation request to DB with id: {generation_request.id}")
        db_model = GenerationRequestModel(**self._map_to_db_dict(generation_request))
        self._db.add(db_model)
        await self._db.flush()
        logger.info(f"Successfully added generation request {generation_request.id} to DB.")

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest in the database."""
        logger.debug(f"Updating generation request in DB with id: {generation_request.id}")
        
        # Pydantic's from_orm creates a new model, so we need to fetch the existing one to update
        # A more performant way is to directly issue an update statement.
        update_data = self._map_to_db_dict(generation_request)
        
        # Remove primary key and created_at from update data
        update_data.pop('id', None)
        update_data.pop('created_at', None)

        stmt = (
            update(GenerationRequestModel)
            .where(GenerationRequestModel.id == generation_request.id)
            .values(**update_data)
        )
        await self._db.execute(stmt)
        await self._db.flush()
        logger.info(f"Successfully updated generation request {generation_request.id} in DB.")


    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists all GenerationRequests for a specific user, with pagination."""
        stmt = (
            select(GenerationRequestModel)
            .where(GenerationRequestModel.user_id == user_id)
            .order_by(GenerationRequestModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._db.execute(stmt)
        db_models = result.scalars().all()
        return [self._map_to_domain(db_model) for db_model in db_models]