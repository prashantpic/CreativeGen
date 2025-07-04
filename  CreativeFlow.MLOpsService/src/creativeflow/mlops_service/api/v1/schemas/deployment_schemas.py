"""
Pydantic schemas for Model Deployment API requests and responses.

These schemas define the data structures for interacting with the `/deployments`
API endpoints, managing the lifecycle of model deployments.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_config

from creativeflow.mlops_service.domain.enums import DeploymentStatusEnum


class DeploymentBaseSchema(BaseModel):
    """Base schema for model deployment attributes."""
    model_version_id: UUID
    environment: str = Field(..., max_length=50, description="Target environment, e.g., 'staging', 'production'.")
    deployment_strategy: Optional[str] = Field(None, max_length=50, description="Deployment strategy, e.g., 'blue_green', 'canary'.")
    replicas: Optional[int] = Field(1, ge=1, description="Number of replicas for the deployment.")
    config: Optional[Dict[str, Any]] = Field(None, description="Advanced config, e.g., A/B test traffic split.")


class DeploymentCreateSchema(DeploymentBaseSchema):
    """Schema for creating a new model deployment."""
    pass


class DeploymentUpdateSchema(BaseModel):
    """Schema for updating an existing deployment (e.g., scaling, traffic split)."""
    replicas: Optional[int] = Field(None, ge=1)
    config: Optional[Dict[str, Any]] = None


class DeploymentResponseSchema(DeploymentBaseSchema):
    """Schema for API responses containing deployment data."""
    id: UUID
    status: DeploymentStatusEnum
    endpoint_url: Optional[str] = None
    deployed_at: datetime
    deployed_by_user_id: Optional[UUID] = None
    
    @model_config
    class Config:
        from_attributes = True