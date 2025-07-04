"""
SQLAlchemy repository for AIModelVersion entities.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.model_schemas import (
    ModelVersionCreateSchema, ModelVersionUpdateSchema
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository
)
from creativeflow.mlops_service.infrastructure.database.orm_models.ai_model_version_orm import (
    AIModelVersionORM
)


class ModelVersionRepository(
    BaseRepository[AIModelVersionORM, ModelVersionCreateSchema, ModelVersionUpdateSchema]
):
    """
    Repository for managing AIModelVersion data.
    """
    async def get_by_model_id_and_version_string(
        self, db: Session, *, model_id: UUID, version_string: str
    ) -> Optional[AIModelVersionORM]:
        """
        Get a specific model version by its parent model ID and version string.

        Args:
            db: The database session.
            model_id: The ID of the parent model.
            version_string: The version string of the model version.

        Returns:
            The AIModelVersionORM instance or None if not found.
        """
        return (
            db.query(AIModelVersionORM)
            .filter(
                AIModelVersionORM.model_id == model_id,
                AIModelVersionORM.version_string == version_string,
            )
            .first()
        )

    async def list_by_model_id(
        self, db: Session, *, model_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelVersionORM]:
        """
        List all versions for a specific model with pagination.

        Args:
            db: The database session.
            model_id: The ID of the parent model.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelVersionORM instances.
        """
        return (
            db.query(AIModelVersionORM)
            .filter(AIModelVersionORM.model_id == model_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Instantiate the repository
version_repository = ModelVersionRepository(AIModelVersionORM)