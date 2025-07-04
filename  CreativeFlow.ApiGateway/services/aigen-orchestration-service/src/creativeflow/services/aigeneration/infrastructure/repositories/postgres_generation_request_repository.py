import logging
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus
from creativeflow.services.aigeneration.domain.models.asset_info import AssetInfo
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestORM

logger = logging.getLogger(__name__)

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """

    PostgreSQL implementation of the IGenerationRequestRepository interface.
    Handles the mapping between the GenerationRequest domain model and the
    GenerationRequestORM SQLAlchemy model.
    """

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    def _map_orm_to_domain(self, orm_obj: GenerationRequestORM) -> GenerationRequest:
        """Maps a SQLAlchemy ORM object to a domain model object."""
        return GenerationRequest(
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            project_id=orm_obj.project_id,
            input_prompt=orm_obj.input_prompt,
            style_guidance=orm_obj.style_guidance,
            input_parameters=orm_obj.input_parameters,
            status=GenerationStatus(orm_obj.status),
            error_message=orm_obj.error_message,
            error_details=orm_obj.error_details,
            sample_asset_infos=[AssetInfo(**info) for info in orm_obj.sample_asset_infos] if orm_obj.sample_asset_infos else [],
            selected_sample_id=orm_obj.selected_sample_id,
            final_asset_info=AssetInfo(**orm_obj.final_asset_info) if orm_obj.final_asset_info else None,
            credits_cost_sample=float(orm_obj.credits_cost_sample) if orm_obj.credits_cost_sample is not None else None,
            credits_cost_final=float(orm_obj.credits_cost_final) if orm_obj.credits_cost_final is not None else None,
            ai_model_used=orm_obj.ai_model_used,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    def _map_domain_to_orm_dict(self, domain_obj: GenerationRequest) -> dict:
        """Maps a domain model object to a dictionary suitable for ORM creation/update."""
        return {
            "id": domain_obj.id,
            "user_id": domain_obj.user_id,
            "project_id": domain_obj.project_id,
            "input_prompt": domain_obj.input_prompt,
            "style_guidance": domain_obj.style_guidance,
            "input_parameters": domain_obj.input_parameters,
            "status": domain_obj.status.value,
            "error_message": domain_obj.error_message,
            "error_details": domain_obj.error_details,
            "sample_asset_infos": [info.dict() for info in domain_obj.sample_asset_infos],
            "selected_sample_id": domain_obj.selected_sample_id,
            "final_asset_info": domain_obj.final_asset_info.dict() if domain_obj.final_asset_info else None,
            "credits_cost_sample": domain_obj.credits_cost_sample,
            "credits_cost_final": domain_obj.credits_cost_final,
            "ai_model_used": domain_obj.ai_model_used,
            "created_at": domain_obj.created_at,
            "updated_at": domain_obj.updated_at,
        }

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        """Retrieves a GenerationRequest by its unique ID."""
        logger.debug(f"Fetching generation request with id: {request_id}")
        stmt = select(GenerationRequestORM).where(GenerationRequestORM.id == request_id)
        result = await self._db_session.execute(stmt)
        orm_request = result.scalar_one_or_none()
        if orm_request:
            return self._map_orm_to_domain(orm_request)
        return None

    async def add(self, generation_request: GenerationRequest) -> None:
        """Adds a new GenerationRequest to the database."""
        logger.info(f"Adding new generation request with id: {generation_request.id}")
        orm_data = self._map_domain_to_orm_dict(generation_request)
        orm_request = GenerationRequestORM(**orm_data)
        self._db_session.add(orm_request)
        await self._db_session.commit()
        await self._db_session.refresh(orm_request)

    async def update(self, generation_request: GenerationRequest) -> None:
        """Updates an existing GenerationRequest in the database."""
        logger.info(f"Updating generation request with id: {generation_request.id}, status: {generation_request.status.value}")
        update_data = self._map_domain_to_orm_dict(generation_request)
        
        # The ORM tracks changes, so we can just update the object if we fetched it first.
        # However, a direct update statement can be more efficient.
        stmt = (
            update(GenerationRequestORM)
            .where(GenerationRequestORM.id == generation_request.id)
            .values(**update_data)
        )
        await self._db_session.execute(stmt)
        await self._db_session.commit()

    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
        """Lists all GenerationRequests for a specific user, with pagination."""
        logger.debug(f"Listing generation requests for user_id: {user_id} with limit {limit}, skip {skip}")
        stmt = (
            select(GenerationRequestORM)
            .where(GenerationRequestORM.user_id == user_id)
            .order_by(GenerationRequestORM.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._db_session.execute(stmt)
        orm_requests = result.scalars().all()
        return [self._map_orm_to_domain(req) for req in orm_requests]