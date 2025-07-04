"""
SQLAlchemy repository for Deployment entities.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.deployment_schemas import (
    DeploymentCreateSchema,
    DeploymentUpdateSchema,
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository,
)
from creativeflow.mlops_service.infrastructure.database.orm_models.deployment_orm import (
    AIModelDeploymentORM,
)


class DeploymentRepository(
    BaseRepository[AIModelDeploymentORM, DeploymentCreateSchema, DeploymentUpdateSchema]
):
    """
    Repository for managing Deployment data in PostgreSQL.

    Provides specific data access methods for AIModelDeploymentORM entities,
    such as listing deployments by model version or environment.
    """

    def list_by_model_version_id(
        self, db: Session, *, model_version_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[AIModelDeploymentORM]:
        """
        Lists all deployments for a specific model version.

        Args:
            db: The SQLAlchemy database session.
            model_version_id: The UUID of the model version.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelDeploymentORM instances.
        """
        return (
            db.query(self.model)
            .filter(self.model.model_version_id == model_version_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_environment(
        self, db: Session, *, environment: str, skip: int = 0, limit: int = 100
    ) -> List[AIModelDeploymentORM]:
        """
        Lists all deployments in a specific environment.

        Args:
            db: The SQLAlchemy database session.
            environment: The name of the deployment environment.
            skip: The number of records to skip.
            limit: The maximum number of records to return.

        Returns:
            A list of AIModelDeploymentORM instances.
        """
        return (
            db.query(self.model)
            .filter(self.model.environment == environment)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


deployment_repo = DeploymentRepository(AIModelDeploymentORM)