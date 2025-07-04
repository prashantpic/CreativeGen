"""
The concrete implementation of the IGenerationRepository interface using SQLAlchemy.
It handles all database operations for the GenerationRequest entity.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...app.interfaces import IGenerationRepository
from ...domain.models.generation_request import GenerationRequest, GenerationStatus
from ..models import GenerationRequestORM


class SqlAlchemyGenerationRepository(IGenerationRepository):
    """
    Provides a persistence mechanism for GenerationRequest domain objects
    using SQLAlchemy for asynchronous database interactions.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, generation_request: GenerationRequest) -> None:
        """
        Converts the domain entity to a SQLAlchemy ORM model and adds it
        to the current database session for insertion.
        """
        orm_instance = self._map_domain_to_orm(generation_request)
        self._session.add(orm_instance)
        await self._session.flush([orm_instance])

    async def get_by_id(self, id: UUID) -> Optional[GenerationRequest]:
        """
        Queries the database for a GenerationRequest by its ID, retrieves the
        ORM object, and maps it back to a domain entity.
        """
        stmt = select(GenerationRequestORM).where(GenerationRequestORM.id == id)
        result = await self._session.execute(stmt)
        orm_instance = result.scalar_one_or_none()
        return self._map_orm_to_domain(orm_instance) if orm_instance else None

    async def update(self, generation_request: GenerationRequest) -> None:
        """
        Updates an existing ORM model in the session with new data from the
        domain model. SQLAlchemy's unit of work will handle the UPDATE statement
        upon commit.
        """
        # Fetch the existing ORM object to update it in the session
        orm_instance = await self._session.get(GenerationRequestORM, generation_request.id)
        if orm_instance:
            # Update fields from the domain model
            orm_instance.status = generation_request.status
            orm_instance.errorMessage = generation_request.errorMessage
            orm_instance.sampleAssets = generation_request.sampleAssets
            orm_instance.selectedSampleId = generation_request.selectedSampleId
            orm_instance.finalAssetId = generation_request.finalAssetId
            orm_instance.updatedAt = generation_request.updatedAt
            await self._session.flush([orm_instance])


    def _map_orm_to_domain(self, orm_instance: GenerationRequestORM) -> GenerationRequest:
        """Maps a SQLAlchemy ORM object to a GenerationRequest domain entity."""
        return GenerationRequest(
            id=orm_instance.id,
            userId=orm_instance.userId,
            projectId=orm_instance.projectId,
            inputPrompt=orm_instance.inputPrompt,
            styleGuidance=orm_instance.styleGuidance,
            inputParameters=orm_instance.inputParameters,
            status=GenerationStatus(orm_instance.status),
            errorMessage=orm_instance.errorMessage,
            sampleAssets=orm_instance.sampleAssets,
            selectedSampleId=orm_instance.selectedSampleId,
            finalAssetId=orm_instance.finalAssetId,
            creditsCostSample=orm_instance.creditsCostSample,
            creditsCostFinal=orm_instance.creditsCostFinal,
            aiModelUsed=orm_instance.aiModelUsed,
            createdAt=orm_instance.createdAt,
            updatedAt=orm_instance.updatedAt,
        )

    def _map_domain_to_orm(self, domain_entity: GenerationRequest) -> GenerationRequestORM:
        """Maps a GenerationRequest domain entity to a SQLAlchemy ORM object."""
        return GenerationRequestORM(
            id=domain_entity.id,
            userId=domain_entity.userId,
            projectId=domain_entity.projectId,
            inputPrompt=domain_entity.inputPrompt,
            styleGuidance=domain_entity.styleGuidance,
            inputParameters=domain_entity.inputParameters,
            status=domain_entity.status,
            errorMessage=domain_entity.errorMessage,
            sampleAssets=domain_entity.sampleAssets,
            selectedSampleId=domain_entity.selectedSampleId,
            finalAssetId=domain_entity.finalAssetId,
            creditsCostSample=domain_entity.creditsCostSample,
            creditsCostFinal=domain_entity.creditsCostFinal,
            aiModelUsed=domain_entity.aiModelUsed,
            createdAt=domain_entity.createdAt,
            updatedAt=domain_entity.updatedAt,
        )