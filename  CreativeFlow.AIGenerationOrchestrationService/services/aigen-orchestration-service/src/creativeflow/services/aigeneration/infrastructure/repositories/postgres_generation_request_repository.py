"""
postgres_generation_request_repository.py

PostgreSQL implementation of the IGenerationRequestRepository interface.
Handles data access operations for GenerationRequest entities using SQLAlchemy.
"""

import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.asset_info import AssetInfo
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestORM

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL repository for AI generation requests. Implements the repository
    interface using SQLAlchemy's async capabilities.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.

        Args:
            db_session: An SQLAlchemy AsyncSession provided by dependency injection.
        """
        self._db_session = db_session

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a generation request by its UUID."""
        stmt = select(GenerationRequestORM).where(GenerationRequestORM.id == request_id)
        result = await self._db_session.execute(stmt)
        orm_request = result.scalar_one_or_none()
        return self._to_domain(orm_request) if orm_request else None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new generation request to the database."""
        orm_request = self._from_domain(generation_request)
        self._db_session.add(orm_request)
        await self._db_session.flush()
        logger.info(f"Added GenerationRequest with ID {generation_request.id} to the database.")

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing generation request in the database."""
        orm_request_data = self._from_domain(generation_request, for_update=True)
        stmt = (
            update(GenerationRequestORM)
            .where(GenerationRequestORM.id == generation_request.id)
            .values(**orm_request_data)
        )
        await self._db_session.execute(stmt)
        await self._db_session.flush()
        logger.info(f"Updated GenerationRequest with ID {generation_request.id} in the database.")


    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists generation requests for a specific user, with pagination."""
        stmt = (
            select(GenerationRequestORM)
            .where(GenerationRequestORM.user_id == user_id)
            .order_by(GenerationRequestORM.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._db_session.execute(stmt)
        orm_requests = result.scalars().all()
        return [self._to_domain(req) for req in orm_requests]

    def _to_domain(self, orm_request: GenerationRequestORM) -> GenerationRequest:
        """Maps a SQLAlchemy ORM object to a domain model."""
        if not orm_request:
            return None
        
        return GenerationRequest(
            id=orm_request.id,
            user_id=orm_request.user_id,
            project_id=orm_request.project_id,
            input_prompt=orm_request.input_prompt,
            style_guidance=orm_request.style_guidance,
            input_parameters=orm_request.input_parameters,
            status=GenerationStatus(orm_request.status),
            error_message=orm_request.error_message,
            sample_asset_infos=[AssetInfo(**info) for info in orm_request.sample_asset_infos] if orm_request.sample_asset_infos else [],
            selected_sample_id=orm_request.selected_sample_id,
            final_asset_info=AssetInfo(**orm_request.final_asset_info) if orm_request.final_asset_info else None,
            credits_cost_sample=float(orm_request.credits_cost_sample) if orm_request.credits_cost_sample is not None else None,
            credits_cost_final=float(orm_request.credits_cost_final) if orm_request.credits_cost_final is not None else None,
            ai_model_used=orm_request.ai_model_used,
            created_at=orm_request.created_at,
            updated_at=orm_request.updated_at
        )

    def _from_domain(self, domain_request: GenerationRequest, for_update: bool = False) -> dict:
        """
        Maps a domain model to a dictionary suitable for creating or updating
        a SQLAlchemy ORM object.
        """
        data = {
            "user_id": domain_request.user_id,
            "project_id": domain_request.project_id,
            "input_prompt": domain_request.input_prompt,
            "style_guidance": domain_request.style_guidance,
            "input_parameters": domain_request.input_parameters,
            "status": domain_request.status.value,
            "error_message": domain_request.error_message,
            "sample_asset_infos": [info.model_dump() for info in domain_request.sample_asset_infos] if domain_request.sample_asset_infos else None,
            "selected_sample_id": domain_request.selected_sample_id,
            "final_asset_info": domain_request.final_asset_info.model_dump() if domain_request.final_asset_info else None,
            "credits_cost_sample": domain_request.credits_cost_sample,
            "credits_cost_final": domain_request.credits_cost_final,
            "ai_model_used": domain_request.ai_model_used,
        }
        if not for_update:
            data['id'] = domain_request.id
        
        return data