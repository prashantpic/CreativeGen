"""
Pydantic model for user feedback on AI model performance or output quality.

This class defines the structure for capturing and storing user feedback,
which is crucial for model improvement and retraining cycles.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ModelFeedback(BaseModel):
    """
    Represents user-provided feedback on an AI model or its outputs.

    Attributes:
        id: The unique identifier for the feedback entry.
        model_version_id: The ID of the AIModelVersion the feedback is for.
        user_id: The ID of the user who submitted the feedback.
        generation_request_id: The ID of the specific generation request, if any.
        rating: A numerical rating, e.g., 1-5.
        comment: Free-text comment from the user.
        feedback_data: Additional structured feedback data.
        submitted_at: The timestamp when the feedback was submitted.
    """
    id: UUID
    model_version_id: UUID
    user_id: Optional[UUID] = None
    generation_request_id: Optional[UUID] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    feedback_data: Optional[Dict[str, Any]] = None
    submitted_at: datetime