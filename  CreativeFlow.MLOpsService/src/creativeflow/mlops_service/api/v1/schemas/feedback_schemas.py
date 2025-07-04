"""
Pydantic schemas for Model Feedback API requests and responses.

These schemas define the data structures for interacting with the `/feedback`
API endpoints, allowing users to submit feedback and admins to retrieve it.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_config


class ModelFeedbackBaseSchema(BaseModel):
    """Base schema for model feedback attributes."""
    model_version_id: UUID
    generation_request_id: Optional[UUID] = None
    rating: Optional[int] = Field(None, ge=1, le=5, description="A numerical rating, e.g., 1-5.")
    comment: Optional[str] = Field(None, description="Free-text comment from the user.")
    feedback_data: Optional[Dict[str, Any]] = Field(None, description="Additional structured feedback.")


class ModelFeedbackCreateSchema(ModelFeedbackBaseSchema):
    """Schema for submitting new model feedback."""
    user_id: Optional[UUID] = Field(None, description="ID of the user providing feedback (if available).")


class ModelFeedbackResponseSchema(ModelFeedbackBaseSchema):
    """Schema for API responses containing model feedback data."""
    id: UUID
    user_id: Optional[UUID] = None
    submitted_at: datetime

    @model_config
    class Config:
        from_attributes = True