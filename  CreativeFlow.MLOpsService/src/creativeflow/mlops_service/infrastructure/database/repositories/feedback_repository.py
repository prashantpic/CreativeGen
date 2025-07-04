"""
SQLAlchemy repository for ModelFeedback entities.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.feedback_schemas import (
    ModelFeedbackCreateSchema, # Placeholder for update if needed
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository
)
from creativeflow.mlops_service.infrastructure.database.orm_models.model_feedback_orm import (
    AIModelFeedbackORM
)


class ModelFeedbackRepository(
    BaseRepository[AIModelFeedbackORM, ModelFeedbackCreateSchema, ModelFeedbackCreateSchema]
):
    """
    Repository for managing ModelFeedback data.
    """
    async def list_by_model_version_id(
        self, db: Session, *, model_version_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelFeedbackORM]:
        """
        List all feedback for a specific model version with pagination.

        Args:
            db: The database session.
            model_version_id: The ID of the model version.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelFeedbackORM instances.
        """
        return (
            db.query(AIModelFeedbackORM)
            .filter(AIModelFeedbackORM.model_version_id == model_version_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Instantiate the repository
feedback_repository = ModelFeedbackRepository(AIModelFeedbackORM)