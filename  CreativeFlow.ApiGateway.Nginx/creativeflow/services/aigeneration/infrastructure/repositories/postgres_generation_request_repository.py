import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import (
    IGenerationRequestRepository,
)
from creativeflow.services.aigeneration.infrastructure.database.db_config import (
    GenerationRequestOrm,
)

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """

    PostgreSQL implementation of the IGenerationRequestRepository interface.
    It uses SQLAlchemy ORM with an async session to interact with the database.
    This class is responsible for mapping between the GenerationRequest domain model
    and the GenerationRequestOrm database model.
    """
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a generation request by its UUID."""
        stmt = select(GenerationRequestOrm).where(GenerationRequestOrm.id == request_id)
        result = await self._db_session.execute(stmt)
        orm_request = result.scalars().first()
        return self._map_orm_to_domain(orm_request) if orm_request else None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new generation request to the database."""
        orm_request = self._map_domain_to_orm(generation_request)
        self._db_session.add(orm_request)
        await self._db_session.commit()
        await self._db_session.refresh(orm_request)
        logger.info(f"Added generation request {generation_request.id} to the database.")

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing generation request in the database."""
        orm_request = self._map_domain_to_orm(generation_request)
        await self._db_session.merge(orm_request)
        await self._db_session.commit()
        logger.info(f"Updated generation request {generation_request.id} in the database.")


    async def list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[GenerationRequest]:
        """Lists generation requests for a given user with pagination."""
        stmt = (
            select(GenerationRequestOrm)
            .where(GenerationRequestOrm.user_id == user_id)
            .order_by(GenerationRequestOrm.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._db_session.execute(stmt)
        orm_requests = result.scalars().all()
        return [self._map_orm_to_domain(req) for req in orm_requests if req]

    @staticmethod
    def _map_orm_to_domain(orm_request: GenerationRequestOrm) -> GenerationRequest:
        """Maps a SQLAlchemy ORM object to a GenerationRequest domain model."""
        if not orm_request:
            return None
        return GenerationRequest(
            id=orm_request.id,
            user_id=orm_request.user_id,
            project_id=orm_request.project_id,
            input_prompt=orm_request.input_prompt,
            style_guidance=orm_request.style_guidance,
            input_parameters=orm_request.input_parameters,
            status=orm_request.status,
            error_message=orm_request.error_message,
            error_details=orm_request.error_details,
            sample_asset_infos=orm_request.sample_asset_infos,
            selected_sample_id=orm_request.selected_sample_id,
            final_asset_info=orm_request.final_asset_info,
            credits_cost_sample=float(orm_request.credits_cost_sample) if orm_request.credits_cost_sample is not None else None,
            credits_cost_final=float(orm_request.credits_cost_final) if orm_request.credits_cost_final is not None else None,
            ai_model_used=orm_request.ai_model_used,
            created_at=orm_request.created_at,
            updated_at=orm_request.updated_at,
        )

    @staticmethod
    def _map_domain_to_orm(domain_request: GenerationRequest) -> GenerationRequestOrm:
        """Maps a GenerationRequest domain model to a SQLAlchemy ORM object."""
        if not domain_request:
            return None
        return GenerationRequestOrm(
            id=domain_request.id,
            user_id=domain_request.user_id,
            project_id=domain_request.project_id,
            input_prompt=domain_request.input_prompt,
            style_guidance=domain_request.style_guidance,
            input_parameters=domain_request.input_parameters,
            status=domain_request.status,
            error_message=domain_request.error_message,
            error_details=domain_request.error_details,
            sample_asset_infos=domain_request.sample_asset_infos,
            selected_sample_id=domain_request.selected_sample_id,
            final_asset_info=domain_request.final_asset_info,
            credits_cost_sample=domain_request.credits_cost_sample,
            credits_cost_final=domain_request.credits_cost_final,
            ai_model_used=domain_request.ai_model_used,
            created_at=domain_request.created_at,
            updated_at=domain_request.updated_at,
        )