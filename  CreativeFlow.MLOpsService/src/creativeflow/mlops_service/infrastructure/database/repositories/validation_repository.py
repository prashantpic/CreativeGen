"""
SQLAlchemy repository for ValidationResult entities.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.validation_schemas import (
    ValidationResultResponseSchema, # Placeholder for create/update if needed
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository
)
from creativeflow.mlops_service.infrastructure.database.orm_models.validation_result_orm import (
    AIModelValidationResultORM
)


class ValidationResultRepository(
    BaseRepository[AIModelValidationResultORM, ValidationResultResponseSchema, ValidationResultResponseSchema]
):
    """
    Repository for managing ValidationResult data.
    Note: Create/Update schemas are placeholders as creation is complex.
    """
    async def list_by_model_version_id(
        self, db: Session, *, model_version_id: UUID
    ) -> List[AIModelValidationResultORM]:
        """
        List all validation results for a specific model version.

        Args:
            db: The database session.
            model_version_id: The ID of the model version.

        Returns:
            A list of AIModelValidationResultORM instances.
        """
        return (
            db.query(AIModelValidationResultORM)
            .filter(AIModelValidationResultORM.model_version_id == model_version_id)
            .all()
        )

# Instantiate the repository
validation_repository = ValidationResultRepository(AIModelValidationResultORM)