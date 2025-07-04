"""
Pydantic model representing a deployment instance of an AI Model Version.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, AnyHttpUrl

from creativeflow.mlops_service.domain.enums import (
    DeploymentStatusEnum,
    DeploymentStrategyEnum,
    DeploymentEnvironmentEnum
)


class Deployment(BaseModel):
    """
    Represents a deployment of a specific AI model version.

    This Pydantic model defines the data structure for tracking the deployment
    of a model version to a specific environment, including its status, strategy,
    and configuration details.
    """
    id: UUID = Field(default_factory=uuid4)
    model_version_id: UUID = Field(..., description="The UUID of the AIModelVersion being deployed.")
    environment: DeploymentEnvironmentEnum = Field(..., description="The target environment for the deployment, e.g., 'staging', 'production'.")
    status: DeploymentStatusEnum = Field(default=DeploymentStatusEnum.REQUESTED, description="The current status of the deployment.")
    deployment_strategy: Optional[DeploymentStrategyEnum] = Field(None, description="The strategy used for this deployment, e.g., 'blue_green', 'canary'.")
    endpoint_url: Optional[AnyHttpUrl] = Field(None, description="The publicly or internally accessible URL for the deployed model service.")
    replicas: Optional[int] = Field(None, ge=0, description="The number of replicas for this deployment.")
    config: Optional[Dict[str, Any]] = Field(None, description="Specific configuration for the deployment, e.g., K8s manifest details, A/B test traffic split.")
    deployed_at: Optional[datetime] = Field(None, description="The timestamp when the deployment became active.")
    deployed_by_user_id: Optional[UUID] = Field(None, description="The UUID of the user who initiated the deployment.")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat() if v else None
        }