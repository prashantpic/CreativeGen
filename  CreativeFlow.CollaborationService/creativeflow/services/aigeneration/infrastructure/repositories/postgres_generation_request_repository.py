import logging
from typing import Optional, List, cast
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

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

    def _map_orm_to_domain(self, orm_obj: GenerationRequestOrm) -> GenerationRequest:
        """Converts an SQLAlchemy ORM object to a domain model."""
        data = {c.name: getattr(orm_obj, c.name) for c in orm_obj.__table__.columns}
        return GenerationRequest.from_dict(data)

    def _map_domain_to_orm_dict(self, domain_obj: GenerationRequest) -> dict:
        """Converts a domain model to a dictionary suitable for the ORM."""
        data = domain_obj.to_dict()
        data['status'] = domain_obj.status.value # Convert enum to string for storage
        return data

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a generation request by its unique identifier."""
        stmt = select(GenerationRequestOrm).where(GenerationRequestOrm.id == request_id)
        result = await self._db.execute(stmt)
        orm_request = result.scalar_one_or_none()

        if orm_request:
            logger.debug("Found generation request with ID %s in DB.", request_id)
            return self._map_orm_to_domain(orm_request)
        
        logger.debug("Generation request with ID %s not found in DB.", request_id)
        return None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new generation request to the database."""
        orm_data = self._map_domain_to_orm_dict(generation_request)
        orm_request = GenerationRequestOrm(**orm_data)
        self._db.add(orm_request)
        await self._db.commit()
        await self._db.refresh(orm_request)
        logger.info("Added new generation request with ID %s to DB.", generation_request.id)

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing generation request in the database."""
        orm_data = self._map_domain_to_orm_dict(generation_request)
        
        # We only update fields that can change after creation
        update_data = {
            "status": orm_data["status"],
            "error_message": orm_data["error_message"],
            "sample_asset_infos": orm_data["sample_asset_infos"],
            "selected_sample_id": orm_data["selected_sample_id"],
            "final_asset_info": orm_data["final_asset_info"],
            "credits_cost_sample": orm_data["credits_cost_sample"],
            "credits_cost_final": orm_data["credits_cost_final"],
            "ai_model_used": orm_data["ai_model_used"],
            "updated_at": orm_data["updated_at"],
            "input_parameters": orm_data["input_parameters"],
            "input_prompt": orm_data["input_prompt"],
            "style_guidance": orm_data["style_guidance"],
        }
        
        stmt = (
            update(GenerationRequestOrm)
            .where(GenerationRequestOrm.id == generation_request.id)
            .values(**update_data)
        )
        await self._db.execute(stmt)
        await self._db.commit()
        logger.info(
            "Updated generation request with ID %s. New status: %s",
            generation_request.id, generation_request.status.value
        )


    async def list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[GenerationRequest]:
        """Lists all generation requests for a specific user, with pagination."""
        stmt = (
            select(GenerationRequestOrm)
            .where(GenerationRequestOrm.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(GenerationRequestOrm.created_at.desc())
        )
        result = await self._db.execute(stmt)
        orm_requests = result.scalars().all()
        
        return [self._map_orm_to_domain(req) for req in orm_requests]