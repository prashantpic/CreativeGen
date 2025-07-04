"""
SQLAlchemy repository for AIModelVersion entities.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.model_schemas import (
    ModelVersionCreateSchema,
    ModelVersionUpdateSchema,
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository,
)
from creativeflow.mlops_service.infrastructure.database.orm_models.ai_model_version_orm import (
    AIModelVersionORM,
)


class ModelVersionRepository(
    BaseRepository[AIModelVersionORM, ModelVersionCreateSchema, ModelVersionUpdateSchema]
):
    """
    Repository for managing AIModelVersion data in PostgreSQL.

    This class provides specific data access methods for AIModelVersionORM entities,
    such as finding a version by its model ID and version string, or listing all
    versions for a given model.
    """

    def get_by_model_id_and_version_string(
        self, db: Session, *, model_id: UUID, version_string: str
    ) -> Optional[AIModelVersionORM]:
        """
        Retrieves a model version by its parent model ID and version string.

        Args:
            db: The SQLAlchemy database session.
            model_id: The UUID of the parent model.
            version_string: The version string of the model version.

        Returns:
            The AIModelVersionORM instance if found, otherwise None.
        """
        return (
            db.query(self.model)
            .filter(
                self.model.model_id == model_id,
                self.model.version_string == version_string,
            )
            .first()
        )

    def list_by_model_id(
        self, db: Session, *, model_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelVersionORM]:
        """
        Lists all versions for a specific model with pagination.

        Args:
            db: The SQLAlchemy database session.
            model_id: The UUID of the parent model.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelVersionORM instances.
        """
        return (
            db.query(self.model)
            .filter(self.model.model_id == model_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


version_repo = ModelVersionRepository(AIModelVersionORM)