"""
Adapter for interacting with the Kubernetes API.
"""
import asyncio
import logging
from typing import Any, Dict, Optional

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import (
    V1Deployment,
    V1DeploymentStatus,
    V1Service,
    V1Status,
)

from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.utils.exceptions import DeploymentFailedException

logger = logging.getLogger(__name__)


class KubernetesAdapter:
    """
    Adapter for Kubernetes API interactions.

    Provides an interface to Kubernetes for deploying and managing model serving
    containers. It uses the official Kubernetes Python client library and handles
    API interactions for Deployments, Services, and other resources.
    """

    def __init__(self):
        """
        Initializes the KubernetesAdapter and loads the K8s configuration.
        """
        try:
            settings = get_settings()
            if settings.KUBERNETES_CONFIG_PATH:
                config.load_kube_config(config_file=settings.KUBERNETES_CONFIG_PATH)
                logger.info(f"Loaded Kubernetes config from file: {settings.KUBERNETES_CONFIG_PATH}")
            else:
                config.load_incluster_config()
                logger.info("Loaded in-cluster Kubernetes config.")
            
            self.apps_v1_api = client.AppsV1Api()
            self.core_v1_api = client.CoreV1Api()
            self.custom_objects_api = client.CustomObjectsApi()
        except config.ConfigException as e:
            logger.error(f"Could not configure Kubernetes client: {e}", exc_info=True)
            # This is a critical failure, so we set APIs to None
            self.apps_v1_api = None
            self.core_v1_api = None
            self.custom_objects_api = None

    async def _run_in_thread(self, func, *args, **kwargs):
        """
        Runs a synchronous function in a separate thread to avoid blocking
        the asyncio event loop.
        """
        if not all([self.apps_v1_api, self.core_v1_api, self.custom_objects_api]):
             raise DeploymentFailedException("Kubernetes client is not configured.")
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    async def apply_deployment(self, namespace: str, manifest: Dict[str, Any]) -> V1Deployment:
        """
        Creates or updates a Kubernetes Deployment.

        Args:
            namespace: The Kubernetes namespace for the deployment.
            manifest: A dictionary representing the K8s Deployment manifest.

        Returns:
            The created or updated V1Deployment object.
        
        Raises:
            DeploymentFailedException: If the API call fails.
        """
        name = manifest["metadata"]["name"]
        try:
            # Check if it exists to decide between create and replace/patch
            await self._run_in_thread(self.apps_v1_api.read_namespaced_deployment, name=name, namespace=namespace)
            logger.info(f"Deployment '{name}' exists, replacing...")
            api_response = await self._run_in_thread(
                self.apps_v1_api.replace_namespaced_deployment,
                name=name,
                namespace=namespace,
                body=manifest
            )
        except ApiException as e:
            if e.status == 404:
                logger.info(f"Deployment '{name}' does not exist, creating...")
                api_response = await self._run_in_thread(
                    self.apps_v1_api.create_namespaced_deployment,
                    namespace=namespace,
                    body=manifest
                )
            else:
                logger.error(f"Kubernetes API error applying deployment '{name}': {e.body}", exc_info=True)
                raise DeploymentFailedException(f"Failed to apply deployment '{name}': {e.reason}")
        
        return api_response

    async def delete_deployment(self, namespace: str, name: str) -> V1Status:
        """
        Deletes a Kubernetes Deployment.

        Args:
            namespace: The Kubernetes namespace.
            name: The name of the Deployment to delete.

        Returns:
            A V1Status object confirming the deletion.
        """
        try:
            return await self._run_in_thread(
                self.apps_v1_api.delete_namespaced_deployment,
                name=name,
                namespace=namespace
            )
        except ApiException as e:
            if e.status == 404:
                logger.warning(f"Attempted to delete non-existent deployment '{name}'.")
                return V1Status(status="Success", reason="Already deleted")
            logger.error(f"Kubernetes API error deleting deployment '{name}': {e.body}", exc_info=True)
            raise DeploymentFailedException(f"Failed to delete deployment '{name}': {e.reason}")

    async def get_deployment_status(self, namespace: str, name: str) -> Optional[V1DeploymentStatus]:
        """
        Gets the status of a Kubernetes Deployment.
        """
        try:
            deployment = await self._run_in_thread(
                self.apps_v1_api.read_namespaced_deployment_status,
                name=name,
                namespace=namespace
            )
            return deployment.status
        except ApiException as e:
            if e.status == 404:
                return None
            logger.error(f"Kubernetes API error getting deployment status for '{name}': {e.body}", exc_info=True)
            raise DeploymentFailedException(f"Failed to get status for deployment '{name}': {e.reason}")

    async def apply_service(self, namespace: str, manifest: Dict[str, Any]) -> V1Service:
        """
        Creates or updates a Kubernetes Service.
        """
        name = manifest["metadata"]["name"]
        try:
            await self._run_in_thread(self.core_v1_api.read_namespaced_service, name=name, namespace=namespace)
            logger.info(f"Service '{name}' exists, replacing...")
            api_response = await self._run_in_thread(
                self.core_v1_api.replace_namespaced_service,
                name=name,
                namespace=namespace,
                body=manifest
            )
        except ApiException as e:
            if e.status == 404:
                logger.info(f"Service '{name}' does not exist, creating...")
                api_response = await self._run_in_thread(
                    self.core_v1_api.create_namespaced_service,
                    namespace=namespace,
                    body=manifest
                )
            else:
                logger.error(f"Kubernetes API error applying service '{name}': {e.body}", exc_info=True)
                raise DeploymentFailedException(f"Failed to apply service '{name}': {e.reason}")
        return api_response

    async def delete_service(self, namespace: str, name: str) -> V1Status:
        """
        Deletes a Kubernetes Service.
        """
        try:
            return await self._run_in_thread(
                self.core_v1_api.delete_namespaced_service,
                name=name,
                namespace=namespace
            )
        except ApiException as e:
            if e.status == 404:
                logger.warning(f"Attempted to delete non-existent service '{name}'.")
                return V1Status(status="Success", reason="Already deleted")
            logger.error(f"Kubernetes API error deleting service '{name}': {e.body}", exc_info=True)
            raise DeploymentFailedException(f"Failed to delete service '{name}': {e.reason}")