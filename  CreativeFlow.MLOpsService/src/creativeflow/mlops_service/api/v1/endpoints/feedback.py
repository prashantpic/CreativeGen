"""
FastAPI router for collecting and retrieving user feedback on AI models.

This module defines the API endpoints that allow users to submit feedback
on model outputs and for administrators to retrieve this valuable data.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1 import schemas
from creativeflow.mlops_service.core.security import verify_api_key
from creativeflow.mlops_service.database import get_db
from creativeflow.mlops_service.services.model_feedback_service import ModelFeedbackService

router = APIRouter()
model_feedback_service = ModelFeedbackService()

@router.post(
    "/",
    response_model=schemas.ModelFeedbackResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback for an AI Model Version",
    dependencies=[Depends(verify_api_key)],
)
async def submit_model_feedback(
    feedback_in: schemas.ModelFeedbackCreateSchema,
    db: Session = Depends(get_db),
):
    """
    Submit feedback for a model, such as a rating, comment, or structured data,
    to help improve future model versions.
    """
    return await model_feedback_service.submit_feedback(db, feedback_in=feedback_in)


@router.get(
    "/versions/{version_id}",
    response_model=List[schemas.ModelFeedbackResponseSchema],
    summary="Retrieve all feedback for a specific AI Model Version",
    dependencies=[Depends(verify_api_key)],
)
async def get_feedback_for_model_version(
    version_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of all feedback submissions for a specific
    model version.
    """
    return await model_feedback_service.get_feedback_for_model_version(
        db, version_id=version_id, skip=skip, limit=limit
    )