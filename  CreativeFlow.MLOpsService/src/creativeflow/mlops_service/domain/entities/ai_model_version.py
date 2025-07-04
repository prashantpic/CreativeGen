"""
Pydantic model representing a specific version of an AI Model.

This class holds all metadata related to a particular iteration of a model,
including its artifact location, format, status, and performance metrics.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from creativeflow.mlops_service.domain.enums import (
    ModelFormatEnum, ModelVersionStatusEnum, ServingInterfaceEnum
)


class AIModelVersion(BaseModel):
    """
    Represents a specific version of an AI Model.

    Attributes:
        id: The unique identifier for this model version.
        model_id: The ID of the parent AIModel.
        version_string: The semantic version string (e.g., '1.0.0', '2023-10-26').
        description: A description of the changes in this version.
        artifact_path: The path to the model artifact in object storage (MinIO).
        model_format: The format of the model artifact (e.g., ONNX, TorchScript).
        interface_type: The serving interface required to run the model.
        parameters: Training or inference parameters associated with this version.
        metrics: Performance metrics from training or validation (e.g., accuracy).
        status: The current lifecycle status of the version.
        created_at: The timestamp when this version was created.
        created_by_user_id: The ID of the user who created this version.
    """
    id: UUID
    model_id: UUID
    version_string: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    artifact_path: str
    model_format: ModelFormatEnum
    interface_type: ServingInterfaceEnum
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    status: ModelVersionStatusEnum
    created_at: datetime
    created_by_user_id: Optional[UUID] = None