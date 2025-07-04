"""
Pydantic schemas for AI Model and Model Version API requests and responses.

These schemas define the data structures and validation rules for the
data exchanged through the `/models` API endpoints. They separate the API
data contracts from the internal domain models and database ORM models.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_config

from creativeflow.mlops_service.domain.enums import (
    ModelFormatEnum, ModelVersionStatusEnum, ServingInterfaceEnum
)

# AIModel Schemas
class ModelBaseSchema(BaseModel):
    """Base schema for AI Model attributes."""
    name: str = Field(..., min_length=3, max_length=100, description="The name of the AI Model.")
    description: Optional[str] = Field(None, max_length=500, description="A description of the model's purpose.")
    task_type: str = Field(..., max_length=50, description="The task type, e.g., 'ImageGeneration'.")


class ModelCreateSchema(ModelBaseSchema):
    """Schema for creating a new AI Model entry."""
    owner_id: Optional[UUID] = Field(None, description="The ID of the user or team owning the model.")


class ModelUpdateSchema(BaseModel):
    """Schema for updating an existing AI Model entry."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    task_type: Optional[str] = Field(None, max_length=50)


class ModelResponseSchema(ModelBaseSchema):
    """Schema for API responses containing AI Model data."""
    id: UUID
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    @model_config
    class Config:
        from_attributes = True


# AIModelVersion Schemas
class ModelVersionBaseSchema(BaseModel):
    """Base schema for AI Model Version attributes."""
    version_string: str = Field(..., max_length=50, description="Semantic version for the model, e.g., '1.0.0'.")
    description: Optional[str] = Field(None, max_length=500, description="Description of changes in this version.")
    model_format: ModelFormatEnum
    interface_type: ServingInterfaceEnum
    parameters: Optional[Dict[str, Any]] = Field(None, description="Training or inference parameters.")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics from training/validation.")


class ModelVersionCreateSchema(ModelVersionBaseSchema):
    """Schema for creating a new Model Version. Used as form data."""
    pass


class ModelVersionUpdateSchema(BaseModel):
    """Schema for updating a Model Version."""
    description: Optional[str] = Field(None, max_length=500)
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None


class ModelVersionResponseSchema(ModelVersionBaseSchema):
    """Schema for API responses containing Model Version data."""
    id: UUID
    model_id: UUID
    artifact_path: str
    status: ModelVersionStatusEnum
    created_at: datetime
    created_by_user_id: Optional[UUID] = None

    @model_config
    class Config:
        from_attributes = True


class ModelVersionStatusUpdateSchema(BaseModel):
    """Schema for updating the status of a Model Version."""
    new_status: ModelVersionStatusEnum