"""
SQLAlchemy repository for Deployment entities.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.deployment_schemas import (
    DeploymentCreateSchema, DeploymentUpdateSchema
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository
)
from creativeflow.mlops_service.infrastructure.database.orm_models.deployment_orm import (
    AIModelDeploymentORM
)


class DeploymentRepository(
    BaseRepository[AIModelDeploymentORM, DeploymentCreateSchema, DeploymentUpdateSchema]
):
    """
    Repository for managing Deployment data.
    """
    async def list_by_model_version_id_and_env(
        self,
        db: Session,
        *,
        model_version_id: UUID,
        environment: Optional[str] = None
    ) -> List[AIModelDeploymentORM]:
        """
        List deployments for a specific model version, optionally filtered by environment.

        Args:
            db: The database session.
            model_version_id: The ID of the model version.
            environment: Optional environment to filter by.

        Returns:
            A list of AIModelDeploymentORM instances.
        """
        query = db.query(AIModelDeploymentORM).filter(
            AIModelDeploymentORM.model_version_id == model_version_id
        )
        if environment:
            query = query.filter(AIModelDeploymentORM.environment == environment)
        return query.all()

# Instantiate the repository
deployment_repository = DeploymentRepository(AIModelDeploymentORM)