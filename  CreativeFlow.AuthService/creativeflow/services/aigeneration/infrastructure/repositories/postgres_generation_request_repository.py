import logging
from typing import Optional, List
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
    Uses SQLAlchemy ORM with an async session for database operations.
    """

    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    def _to_domain(self, orm_obj: GenerationRequestOrm) -> GenerationRequest:
        """Maps an ORM object to a domain model."""
        data = orm_obj.__dict__
        
        # Combine flat input parameters back into the domain model's structure
        input_params = data.get('input_parameters', {}) or {}
        
        domain_data = {
            "id": data['id'],
            "user_id": data['user_id'],
            "project_id": data['project_id'],
            "input_prompt": data['input_prompt'],
            "style_guidance": data['style_guidance'],
            "status": data['status'],
            "error_message": data['error_message'],
            "error_details": data['error_details'],
            "sample_asset_infos": data['sample_asset_infos'],
            "selected_sample_id": data['selected_sample_id'],
            "final_asset_info": data['final_asset_info'],
            "credits_cost_sample": float(data['credits_cost_sample']) if data.get('credits_cost_sample') is not None else None,
            "credits_cost_final": float(data['credits_cost_final']) if data.get('credits_cost_final') is not None else None,
            "ai_model_used": data['ai_model_used'],
            "created_at": data['created_at'],
            "updated_at": data['updated_at'],
            **input_params  # Unpack format, dimensions, etc.
        }
        return GenerationRequest(**domain_data)
        
    def _to_orm_values(self, domain_obj: GenerationRequest) -> dict:
        """Maps a domain model to a dictionary of ORM values, separating input params."""
        orm_values = {
            "id": domain_obj.id,
            "user_id": domain_obj.user_id,
            "project_id": domain_obj.project_id,
            "input_prompt": domain_obj.input_prompt,
            "style_guidance": domain_obj.style_guidance,
            "status": domain_obj.status.value,
            "error_message": domain_obj.error_message,
            "error_details": domain_obj.error_details,
            "sample_asset_infos": domain_obj.sample_asset_infos,
            "selected_sample_id": domain_obj.selected_sample_id,
            "final_asset_info": domain_obj.final_asset_info,
            "credits_cost_sample": domain_obj.credits_cost_sample,
            "credits_cost_final": domain_obj.credits_cost_final,
            "ai_model_used": domain_obj.ai_model_used,
            "created_at": domain_obj.created_at,
            "updated_at": domain_obj.updated_at,
        }
        # Group other input parameters into the JSONB column
        orm_values["input_parameters"] = {
            "output_format": domain_obj.output_format,
            "custom_dimensions": domain_obj.custom_dimensions,
            "brand_kit_id": domain_obj.brand_kit_id,
            "uploaded_image_references": domain_obj.uploaded_image_references,
            "target_platform_hints": domain_obj.target_platform_hints,
            "emotional_tone": domain_obj.emotional_tone,
            "cultural_adaptation_parameters": domain_obj.cultural_adaptation_parameters,
        }
        return orm_values


    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        stmt = select(GenerationRequestOrm).where(GenerationRequestOrm.id == request_id)
        result = await self._db.execute(stmt)
        orm_request = result.scalar_one_or_none()
        return self._to_domain(orm_request) if orm_request else None

    async def add(self, generation_request: GenerationRequest) -> None:
        orm_values = self._to_orm_values(generation_request)
        orm_request = GenerationRequestOrm(**orm_values)
        self._db.add(orm_request)
        await self._db.commit()
        await self._db.refresh(orm_request)
        logger.info(f"Added generation request {generation_request.id} to DB.")

    async def update(self, generation_request: GenerationRequest) -> None:
        orm_values = self._to_orm_values(generation_request)
        stmt = (
            update(GenerationRequestOrm)
            .where(GenerationRequestOrm.id == generation_request.id)
            .values(**orm_values)
        )
        await self._db.execute(stmt)
        await self._db.commit()
        logger.debug(f"Updated generation request {generation_request.id} in DB.")

    async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]:
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