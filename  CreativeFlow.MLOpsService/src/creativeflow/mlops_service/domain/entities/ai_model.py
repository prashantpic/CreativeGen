"""
Pydantic model representing an AI Model entity within the MLOps domain.

This class defines the core data structure for an AI Model, which acts as a
container for its various versions.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AIModel(BaseModel):
    """
    Represents an AI Model, a logical grouping for model versions.

    Attributes:
        id: The unique identifier for the AI model.
        name: The user-defined name of the model.
        description: A detailed description of the model's purpose.
        task_type: The type of task the model performs (e.g., 'ImageGeneration').
        owner_id: The ID of the user or team that owns this model.
        created_at: The timestamp when the model was created.
        updated_at: The timestamp of the last update.
    """
    id: UUID
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    task_type: str = Field(..., max_length=50)
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime