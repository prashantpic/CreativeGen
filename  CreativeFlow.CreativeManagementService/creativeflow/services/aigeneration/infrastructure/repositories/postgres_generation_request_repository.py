import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models.generation_request import GenerationRequest
from ...domain.repositories.generation_request_repository import IGenerationRequestRepository
from ..database.db_config import GenerationRequestModel

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL implementation of the IGenerationRequestRepository interface.
    Handles data access operations for GenerationRequest entities using SQLAlchemy.
    """
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest by its unique ID."""
        stmt = select(GenerationRequestModel).where(GenerationRequestModel.id == request_id)
        result = await self._db_session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            # Map from ORM model to domain model
            return GenerationRequest.parse_obj(model.__dict__)
        return None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest to the database."""
        # Map from domain model to ORM model
        new_model = GenerationRequestModel(**generation_request.dict())
        self._db_session.add(new_model)
        await self._db_session.flush() # Flush to assign defaults like created_at
        await self._db_session.refresh(new_model) # Refresh to get the generated values
        logger.info(f"Added new generation request {new_model.id} to the database.")

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest in the database."""
        # We update specific fields to avoid overwriting the whole record.
        # This is generally safer.
        update_data = generation_request.dict(exclude_unset=True)
        
        # Ensure 'id' is not in the update data itself, it's for the where clause.
        request_id = update_data.pop('id', None)
        if not request_id:
             logger.error("Attempted to update a GenerationRequest without an ID.")
             return
             
        stmt = (
            update(GenerationRequestModel)
            .where(GenerationRequestModel.id == request_id)
            .values(**update_data)
        )
        await self._db_session.execute(stmt)
        await self._db_session.flush()
        logger.debug(f"Updated generation request {request_id} in the database.")


    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists all GenerationRequests for a specific user, with pagination."""
        stmt = (
            select(GenerationRequestModel)
            .where(GenerationRequestModel.user_id == user_id)
            .order_by(GenerationRequestModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._db_session.execute(stmt)
        models = result.scalars().all()
        
        # Map list of ORM models to list of domain models
        return [GenerationRequest.parse_obj(model.__dict__) for model in models]