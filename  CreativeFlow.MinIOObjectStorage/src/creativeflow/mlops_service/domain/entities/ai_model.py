"""
Pydantic model representing an AI Model entity within the MLOps domain.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from creativeflow.mlops_service.domain.enums import ModelTaskTypeEnum


class AIModel(BaseModel):
    """
    Represents an AI Model entity, including its core metadata.

    This is a Pydantic model used for internal data representation within the
    service layer, distinct from the database ORM model.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=100, description="The unique name of the AI model.")
    description: Optional[str] = Field(None, max_length=500, description="A detailed description of the model's purpose and capabilities.")
    task_type: ModelTaskTypeEnum = Field(..., description="The primary task the model is designed for, e.g., ImageGeneration.")
    owner_id: Optional[UUID] = Field(None, description="The UUID of the user or team that owns this model.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        from_attributes = True  # Allows creating Pydantic models from ORM objects.
        json_encoders = {
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }