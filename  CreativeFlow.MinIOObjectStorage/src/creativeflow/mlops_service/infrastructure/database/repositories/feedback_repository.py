"""
SQLAlchemy repository for ModelFeedback entities.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.feedback_schemas import (
    ModelFeedbackCreateSchema,
    ModelFeedbackResponseSchema, # Placeholder for update schema
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository,
)
from creativeflow.mlops_service.infrastructure.database.orm_models.model_feedback_orm import (
    AIModelFeedbackORM,
)


class ModelFeedbackRepository(
    BaseRepository[AIModelFeedbackORM, ModelFeedbackCreateSchema, ModelFeedbackResponseSchema]
):
    """
    Repository for managing ModelFeedback data in PostgreSQL.

    Provides specific data access methods for AIModelFeedbackORM entities,
    such as listing all feedback entries for a given model version.
    """

    def list_by_model_version_id(
        self, db: Session, *, model_version_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelFeedbackORM]:
        """
        Lists all feedback entries for a specific model version.

        Args:
            db: The SQLAlchemy database session.
            model_version_id: The UUID of the model version.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelFeedbackORM instances.
        """
        return (
            db.query(self.model)
            .filter(self.model.model_version_id == model_version_id)
            .order_by(self.model.submitted_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


feedback_repo = ModelFeedbackRepository(AIModelFeedbackORM)