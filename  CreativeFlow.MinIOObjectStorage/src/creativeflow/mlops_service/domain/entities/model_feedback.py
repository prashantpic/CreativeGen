"""
Pydantic model for user feedback on AI model performance or output quality.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ModelFeedback(BaseModel):
    """
    Represents user-provided feedback on an AI model or its outputs.

    This Pydantic model defines the structure for capturing user feedback,
    including ratings, comments, and other structured data, linking it to the
    relevant model version and user.
    """
    id: UUID = Field(default_factory=uuid4)
    model_version_id: UUID = Field(..., description="The UUID of the AIModelVersion this feedback pertains to.")
    user_id: Optional[UUID] = Field(None, description="The UUID of the user providing the feedback.")
    generation_request_id: Optional[UUID] = Field(None, description="The UUID of the specific generation request this feedback is about.")
    rating: Optional[int] = Field(None, ge=1, le=5, description="A numerical rating, e.g., from 1 to 5.")
    comment: Optional[str] = Field(None, max_length=2000, description="Free-text comment from the user.")
    feedback_data: Optional[Dict[str, Any]] = Field(None, description="Any additional structured feedback data, e.g., {'was_helpful': true, 'tags': ['blurry', 'off-topic']}.")
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }