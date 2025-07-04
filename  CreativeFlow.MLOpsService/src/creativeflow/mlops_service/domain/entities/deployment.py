"""
Pydantic model representing a deployment instance of an AI Model Version.

This class tracks the state of a model version deployed to a specific
environment, including its configuration and status.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from creativeflow.mlops_service.domain.enums import DeploymentStatusEnum


class Deployment(BaseModel):
    """
    Represents the deployment of a model version to an environment.

    Attributes:
        id: The unique identifier for the deployment.
        model_version_id: The ID of the AIModelVersion being deployed.
        environment: The target environment (e.g., 'staging', 'production').
        status: The current status of the deployment.
        deployment_strategy: The strategy used (e.g., 'blue_green', 'canary').
        endpoint_url: The URL where the deployed model can be accessed.
        replicas: The number of pod replicas for this deployment.
        config: Additional configuration details (e.g., K8s manifest snippets).
        deployed_at: The timestamp when the deployment was initiated.
        deployed_by_user_id: The ID of the user who initiated the deployment.
    """
    id: UUID
    model_version_id: UUID
    environment: str = Field(..., max_length=50)
    status: DeploymentStatusEnum
    deployment_strategy: Optional[str] = Field(None, max_length=50)
    endpoint_url: Optional[str] = None
    replicas: Optional[int] = Field(None, ge=0)
    config: Optional[Dict[str, Any]] = None
    deployed_at: datetime
    deployed_by_user_id: Optional[UUID] = None