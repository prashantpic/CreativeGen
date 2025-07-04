"""
SQLAlchemy repository for ValidationResult entities.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.validation_schemas import (
    ValidationRequestSchema,  # Assuming a create schema might be similar
    ValidationResultResponseSchema,  # Assuming an update schema might be similar
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository,
)
from creativeflow.mlops_service.infrastructure.database.orm_models.validation_result_orm import (
    AIModelValidationResultORM,
)


class ValidationResultRepository(
    BaseRepository[
        AIModelValidationResultORM, ValidationRequestSchema, ValidationResultResponseSchema
    ]
):
    """
    Repository for managing ValidationResult data in PostgreSQL.

    Provides specific data access methods for AIModelValidationResultORM entities,
    such as listing all validation results for a given model version.
    """

    def list_by_model_version_id(
        self, db: Session, *, model_version_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelValidationResultORM]:
        """
        Lists all validation results for a specific model version.

        Args:
            db: The SQLAlchemy database session.
            model_version_id: The UUID of the model version.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelValidationResultORM instances.
        """
        return (
            db.query(self.model)
            .filter(self.model.model_version_id == model_version_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


validation_repo = ValidationResultRepository(AIModelValidationResultORM)