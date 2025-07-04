"""
Pydantic model representing a specific version of an AI Model.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, AnyHttpUrl

from creativeflow.mlops_service.domain.enums import (
    ModelFormatEnum,
    ModelVersionStatusEnum,
    ServingInterfaceEnum,
)


class AIModelVersion(BaseModel):
    """
    Represents a version of an AI Model, linking to its artifacts and metadata.

    This Pydantic model defines the structure for a version of an AI Model,
    including its artifact location, format, status, and associated parameters
    and metrics.
    """
    id: UUID = Field(default_factory=uuid4)
    model_id: UUID = Field(..., description="The UUID of the parent AIModel.")
    version_string: str = Field(..., min_length=1, max_length=50, description="The semantic version string for this model version, e.g., '1.0.0'.")
    description: Optional[str] = Field(None, max_length=500, description="Description of the changes or features in this version.")
    artifact_path: str = Field(..., description="The path to the model artifact in the object storage (e.g., MinIO).")
    model_format: ModelFormatEnum = Field(..., description="The format of the model artifact, e.g., ONNX, TensorFlow SavedModel.")
    interface_type: ServingInterfaceEnum = Field(..., description="The serving interface required for this model, e.g., TensorFlow Serving, Custom FastAPI.")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Key-value pairs of training or inference parameters.")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Key-value pairs of performance or quality metrics from training/evaluation.")
    status: ModelVersionStatusEnum = Field(default=ModelVersionStatusEnum.STAGING, description="The current lifecycle status of the model version.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: Optional[UUID] = Field(None, description="The UUID of the user who created this version.")

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }