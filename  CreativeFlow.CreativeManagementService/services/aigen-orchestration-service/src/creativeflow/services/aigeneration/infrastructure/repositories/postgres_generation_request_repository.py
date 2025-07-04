"""
PostgreSQL implementation of the IGenerationRequestRepository interface.
"""
import logging
from typing import Optional, List
from uuid import UUID

from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestModel

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    Handles data access operations for GenerationRequest entities using PostgreSQL
    with SQLAlchemy's async capabilities.
    """

    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    def _to_domain(self, model: GenerationRequestModel) -> GenerationRequest:
        """Maps the SQLAlchemy model to the domain model."""
        return GenerationRequest.parse_obj(model.__dict__)

    def _to_persistence(self, domain_obj: GenerationRequest) -> dict:
        """Maps the domain model to a dictionary for persistence."""
        return domain_obj.dict()

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest by its unique ID."""
        stmt = select(GenerationRequestModel).where(GenerationRequestModel.id == request_id)
        result = await self._db.execute(stmt)
        model = result.scalars().first()
        return self._to_domain(model) if model else None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest to the database."""
        try:
            model_data = self._to_persistence(generation_request)
            db_model = GenerationRequestModel(**model_data)
            self._db.add(db_model)
            await self._db.commit()
            await self._db.refresh(db_model)
            logger.info(f"Successfully added GenerationRequest {generation_request.id} to DB.")
        except Exception as e:
            logger.error(f"Failed to add GenerationRequest {generation_request.id} to DB: {e}", exc_info=True)
            await self._db.rollback()
            raise

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest in the database."""
        try:
            update_data = self._to_persistence(generation_request)
            # Remove primary key from update data
            update_data.pop('id', None)
            
            stmt = (
                sqlalchemy_update(GenerationRequestModel)
                .where(GenerationRequestModel.id == generation_request.id)
                .values(**update_data)
            )
            await self._db.execute(stmt)
            await self._db.commit()
            logger.info(f"Successfully updated GenerationRequest {generation_request.id} in DB.")
        except Exception as e:
            logger.error(f"Failed to update GenerationRequest {generation_request.id} in DB: {e}", exc_info=True)
            await self._db.rollback()
            raise

    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists GenerationRequests for a specific user with pagination."""
        stmt = (
            select(GenerationRequestModel)
            .where(GenerationRequestModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(GenerationRequestModel.created_at.desc())
        )
        result = await self._db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]