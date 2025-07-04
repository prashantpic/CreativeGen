"""
Service for managing AI model deployments to Kubernetes.

This service handles the logic for deploying validated models to the Kubernetes
cluster, managing deployment strategies (e.g., blue-green, canary),
configuring A/B tests, and tracking deployment state in the database.
"""
import logging
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas import deployment_schemas
from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.domain.enums import DeploymentStatusEnum, ModelVersionStatusEnum
from creativeflow.mlops_service.infrastructure.database.orm_models import (
    AIModelDeploymentORM, AIModelVersionORM
)
from creativeflow.mlops_service.infrastructure.database.repositories import (
    deployment_repository, version_repository
)
from creativeflow.mlops_service.infrastructure.kubernetes.k8s_adapter import KubernetesAdapter
from creativeflow.mlops_service.utils.exceptions import (
    DeploymentFailedException, InvalidStateTransitionException, ModelVersionNotFoundException
)

logger = logging.getLogger(__name__)


class ModelDeploymentService:
    """Handles business logic for model deployment to Kubernetes."""

    def __init__(self):
        settings = get_settings()
        self.k8s_adapter = KubernetesAdapter(settings)
        self.deployment_repo = deployment_repository
        self.version_repo = version_repository
        self.namespace = settings.KUBERNETES_NAMESPACE_MODELS

    def _construct_k8s_manifests(self, model_version: AIModelVersionORM, config: deployment_schemas.DeploymentCreateSchema) -> tuple[dict, dict]:
        """Constructs Kubernetes Deployment and Service manifests."""
        deployment_name = f"model-{model_version.model.name.lower().replace('_', '-')}-{model_version.id.hex[:8]}"
        labels = {
            "app": deployment_name,
            "model_id": str(model_version.model_id),
            "version_id": str(model_version.id)
        }
        
        # This is a highly simplified example. A real implementation would have templates
        # based on `model_version.interface_type`.
        container_image = f"your-container-registry/model-server-{model_version.interface_type.lower()}:latest"

        deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": deployment_name, "labels": labels},
            "spec": {
                "replicas": config.replicas,
                "selector": {"matchLabels": labels},
                "template": {
                    "metadata": {"labels": labels},
                    "spec": {
                        "containers": [{
                            "name": "model-server",
                            "image": container_image,
                            "ports": [{"containerPort": 8080}],
                            # Add resource requests/limits, env vars etc. here
                        }]
                    },
                },
            },
        }

        service_manifest = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": deployment_name},
            "spec": {
                "selector": labels,
                "ports": [{"protocol": "TCP", "port": 80, "targetPort": 8080}],
                "type": "ClusterIP",
            },
        }
        return deployment_manifest, service_manifest

    async def deploy_model_version(
        self,
        db: Session,
        deployment_config: deployment_schemas.DeploymentCreateSchema,
        user_id: Optional[UUID],
    ) -> AIModelDeploymentORM:
        """
        Deploys a validated model version to Kubernetes.

        Args:
            db: The database session.
            deployment_config: Pydantic schema with deployment configuration.
            user_id: The ID of the user initiating the deployment.

        Returns:
            The created AIModelDeploymentORM object.
        """
        version_id = deployment_config.model_version_id
        model_version = await self.version_repo.get(db, id=version_id)
        if not model_version:
            raise ModelVersionNotFoundException(str(version_id))

        if model_version.status not in [ModelVersionStatusEnum.VALIDATED, ModelVersionStatusEnum.PRODUCTION]:
            raise InvalidStateTransitionException(
                f"Cannot deploy model version from status '{model_version.status}'. Must be VALIDATED or PRODUCTION."
            )

        deployment_manifest, service_manifest = self._construct_k8s_manifests(model_version, deployment_config)
        deployment_name = deployment_manifest["metadata"]["name"]

        # Create record in DB first
        deployment_record = AIModelDeploymentORM(
            model_version_id=version_id,
            environment=deployment_config.environment,
            status=DeploymentStatusEnum.REQUESTED,
            deployment_strategy=deployment_config.deployment_strategy,
            replicas=deployment_config.replicas,
            config=deployment_config.config,
            deployed_by_user_id=user_id,
        )
        db.add(deployment_record)
        db.commit()
        db.refresh(deployment_record)

        try:
            logger.info(f"Applying K8s deployment '{deployment_name}' in namespace '{self.namespace}'")
            await self.k8s_adapter.apply_deployment(self.namespace, deployment_manifest)
            
            logger.info(f"Applying K8s service '{deployment_name}' in namespace '{self.namespace}'")
            service = await self.k8s_adapter.apply_service(self.namespace, service_manifest)
            
            endpoint_url = f"http://{service.metadata.name}.{self.namespace}.svc.cluster.local"
            
            update_data = {"status": DeploymentStatusEnum.ACTIVE, "endpoint_url": endpoint_url}
            return await self.deployment_repo.update(db, db_obj=deployment_record, obj_in=update_data)

        except DeploymentFailedException as e:
            logger.error(f"Deployment failed for version {version_id}: {e}")
            await self.deployment_repo.update(db, db_obj=deployment_record, obj_in={"status": DeploymentStatusEnum.FAILED})
            # Attempt to clean up K8s resources
            await self.delete_deployment(db, deployment_id=deployment_record.id, user_id=None)
            raise

    async def get_deployment_by_id(self, db: Session, deployment_id: UUID) -> Optional[AIModelDeploymentORM]:
        """Retrieves deployment details from the database."""
        return await self.deployment_repo.get(db, id=deployment_id)
    
    async def list_deployments(self, db: Session, skip: int, limit: int) -> List[AIModelDeploymentORM]:
        """Lists all deployments."""
        return await self.deployment_repo.get_multi(db, skip=skip, limit=limit)

    async def update_deployment(
        self, db: Session, deployment_id: UUID, deployment_update: deployment_schemas.DeploymentUpdateSchema, user_id: Optional[UUID]
    ) -> AIModelDeploymentORM:
        """Updates an existing deployment (e.g., scales replicas)."""
        # Placeholder for more complex updates like canary traffic shifting
        deployment_record = await self.deployment_repo.get(db, id=deployment_id)
        if not deployment_record:
            raise DeploymentFailedException(f"Deployment with ID {deployment_id} not found.")

        # Update K8s resources
        # ... logic to patch k8s deployment ...

        # Update DB
        return await self.deployment_repo.update(db, db_obj=deployment_record, obj_in=deployment_update)

    async def delete_deployment(self, db: Session, deployment_id: UUID, user_id: Optional[UUID]) -> None:
        """Deletes/undeploys a model from Kubernetes."""
        deployment_record = await self.deployment_repo.get(db, id=deployment_id)
        if not deployment_record:
            return # Idempotent delete

        model_version = deployment_record.model_version
        deployment_name = f"model-{model_version.model.name.lower().replace('_', '-')}-{model_version.id.hex[:8]}"

        try:
            logger.info(f"Deleting K8s deployment and service '{deployment_name}' in namespace '{self.namespace}'")
            await self.k8s_adapter.delete_deployment(self.namespace, deployment_name)
            await self.k8s_adapter.delete_service(self.namespace, deployment_name)
            
            await self.deployment_repo.update(db, db_obj=deployment_record, obj_in={"status": DeploymentStatusEnum.DELETED})
        except DeploymentFailedException as e:
            logger.error(f"Failed to delete K8s resources for deployment {deployment_id}: {e}")
            await self.deployment_repo.update(db, db_obj=deployment_record, obj_in={"status": DeploymentStatusEnum.FAILED})
            raise