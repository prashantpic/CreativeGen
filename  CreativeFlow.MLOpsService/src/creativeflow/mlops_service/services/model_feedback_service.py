"""
Service for managing user feedback related to AI models.

This service handles the business logic for collecting, storing, and
retrieving user feedback on AI model outputs, which is vital for the
human-in-the-loop model improvement process.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas import feedback_schemas
from creativeflow.mlops_service.infrastructure.database.orm_models import AIModelFeedbackORM
from creativeflow.mlops_service.infrastructure.database.repositories import (
    feedback_repository
)


class ModelFeedbackService:
    """Handles business logic for model feedback."""

    def __init__(self):
        """Initializes the service with the feedback repository."""
        self.feedback_repo = feedback_repository

    async def submit_feedback(
        self, db: Session, feedback_in: feedback_schemas.ModelFeedbackCreateSchema
    ) -> AIModelFeedbackORM:
        """
        Stores a new feedback submission in the database.

        Args:
            db: The database session.
            feedback_in: The Pydantic schema with feedback creation data.

        Returns:
            The created AIModelFeedbackORM object.
        """
        return await self.feedback_repo.create(db, obj_in=feedback_in)

    async def get_feedback_for_model_version(
        self, db: Session, version_id: UUID, skip: int, limit: int
    ) -> List[AIModelFeedbackORM]:
        """
        Retrieves all feedback for a specific AI Model Version.

        Args:
            db: The database session.
            version_id: The UUID of the model version.
            skip: The number of records to skip for pagination.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelFeedbackORM objects.
        """
        return await self.feedback_repo.list_by_model_version_id(
            db, model_version_id=version_id, skip=skip, limit=limit
        )