import logging
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestOrm

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL implementation of the IGenerationRequestRepository interface.
    Handles data access operations for GenerationRequest entities using SQLAlchemy.
    """

    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    def _to_domain(self, orm_obj: GenerationRequestOrm) -> GenerationRequest:
        """Maps an ORM object to a domain model."""
        return GenerationRequest.parse_obj(orm_obj.__dict__)

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest by its unique ID."""
        try:
            stmt = select(GenerationRequestOrm).where(GenerationRequestOrm.id == request_id)
            result = await self._db.execute(stmt)
            orm_request = result.scalar_one_or_none()
            if orm_request:
                return self._to_domain(orm_request)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error getting request by ID {request_id}: {e}", exc_info=True)
            raise

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest to the database."""
        try:
            orm_request = GenerationRequestOrm(**generation_request.dict())
            self._db.add(orm_request)
            await self._db.flush()
            await self._db.refresh(orm_request)
            logger.info(f"Added new generation request {orm_request.id} to the database.")
        except SQLAlchemyError as e:
            logger.error(f"Database error adding request: {e}", exc_info=True)
            await self._db.rollback()
            raise

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest in the database."""
        try:
            update_data = generation_request.dict(exclude={'id', 'created_at'})
            stmt = (
                update(GenerationRequestOrm)
                .where(GenerationRequestOrm.id == generation_request.id)
                .values(**update_data)
            )
            result = await self._db.execute(stmt)
            if result.rowcount == 0:
                logger.warning(f"Attempted to update non-existent request ID {generation_request.id}")
                # Depending on strictness, you might raise an error here
            else:
                 logger.debug(f"Updated generation request {generation_request.id} in the database.")
        except SQLAlchemyError as e:
            logger.error(f"Database error updating request {generation_request.id}: {e}", exc_info=True)
            await self._db.rollback()
            raise

    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists all GenerationRequests for a specific user, with pagination."""
        try:
            stmt = (
                select(GenerationRequestOrm)
                .where(GenerationRequestOrm.user_id == user_id)
                .order_by(GenerationRequestOrm.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            result = await self._db.execute(stmt)
            orm_requests = result.scalars().all()
            return [self._to_domain(req) for req in orm_requests]
        except SQLAlchemyError as e:
            logger.error(f"Database error listing requests for user {user_id}: {e}", exc_info=True)
            raise