from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update

from creativeflow.services.aigeneration.domain.models.generation_request import GenerationRequest
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import GenerationRequestOrm

class PostgresGenerationRequestRepository(IGenerationRequestRepository):
    """
    PostgreSQL implementation of the IGenerationRequestRepository interface.
    It uses SQLAlchemy ORM with an async session to interact with the database.
    """

    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    def _orm_to_domain(self, orm_obj: GenerationRequestOrm) -> GenerationRequest:
        """Maps an ORM object to a domain model."""
        # Unpack input_parameters from JSONB to domain model fields
        input_params = orm_obj.input_parameters or {}
        domain_data = {
            "id": orm_obj.id,
            "user_id": orm_obj.user_id,
            "project_id": orm_obj.project_id,
            "input_prompt": orm_obj.input_prompt,
            "style_guidance": orm_obj.style_guidance,
            "status": orm_obj.status,
            "error_message": orm_obj.error_message,
            "sample_asset_infos": orm_obj.sample_asset_infos,
            "selected_sample_id": orm_obj.selected_sample_id,
            "final_asset_info": orm_obj.final_asset_info,
            "credits_cost_sample": orm_obj.credits_cost_sample,
            "credits_cost_final": orm_obj.credits_cost_final,
            "ai_model_used": orm_obj.ai_model_used,
            "created_at": orm_obj.created_at,
            "updated_at": orm_obj.updated_at,
            **input_params # Unpack the rest of the params
        }
        return GenerationRequest(**domain_data)

    def _domain_to_orm_values(self, domain_obj: GenerationRequest) -> dict:
        """Maps a domain model to a dictionary of values for the ORM."""
        # Group flexible input parameters into the JSONB field
        input_parameters = {
            "output_format": domain_obj.output_format,
            "custom_dimensions": domain_obj.custom_dimensions,
            "brand_kit_id": domain_obj.brand_kit_id,
            "uploaded_image_references": domain_obj.uploaded_image_references,
            "target_platform_hints": domain_obj.target_platform_hints,
            "emotional_tone": domain_obj.emotional_tone,
            "cultural_adaptation_parameters": domain_obj.cultural_adaptation_parameters,
        }
        # Use .dict() to handle Pydantic model serialization correctly, especially for AssetInfo
        orm_values = {
            "id": domain_obj.id,
            "user_id": domain_obj.user_id,
            "project_id": domain_obj.project_id,
            "input_prompt": domain_obj.input_prompt,
            "style_guidance": domain_obj.style_guidance,
            "input_parameters": input_parameters,
            "status": domain_obj.status.value, # Ensure enum value is stored
            "error_message": domain_obj.error_message,
            "sample_asset_infos": [info.dict() for info in domain_obj.sample_asset_infos] if domain_obj.sample_asset_infos else None,
            "selected_sample_id": domain_obj.selected_sample_id,
            "final_asset_info": domain_obj.final_asset_info.dict() if domain_obj.final_asset_info else None,
            "credits_cost_sample": domain_obj.credits_cost_sample,
            "credits_cost_final": domain_obj.credits_cost_final,
            "ai_model_used": domain_obj.ai_model_used,
            "created_at": domain_obj.created_at,
            "updated_at": domain_obj.updated_at,
        }
        return orm_values

    async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]:
        stmt = select(GenerationRequestOrm).where(GenerationRequestOrm.id == request_id)
        result = await self._db.execute(stmt)
        orm_request = result.scalar_one_or_none()
        return self._orm_to_domain(orm_request) if orm_request else None

    async def add(self, generation_request: GenerationRequest) -> None:
        orm_values = self._domain_to_orm_values(generation_request)
        orm_request = GenerationRequestOrm(**orm_values)
        self._db.add(orm_request)
        await self._db.flush() # Flush to assign default values like created_at

    async def update(self, generation_request: GenerationRequest) -> None:
        orm_values = self._domain_to_orm_values(generation_request)
        # We don't want to update the primary key
        orm_values.pop('id', None)
        
        stmt = (
            sqlalchemy_update(GenerationRequestOrm)
            .where(GenerationRequestOrm.id == generation_request.id)
            .values(**orm_values)
        )
        await self._db.execute(stmt)

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
        return [self._orm_to_domain(req) for req in orm_requests]