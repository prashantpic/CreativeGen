"""
Adapter for interacting with the Kubernetes API.

This class provides an asynchronous interface for deploying and managing
model serving containers within the Kubernetes cluster, abstracting the
details of the Kubernetes Python client.
"""
import asyncio
from typing import Dict, Any, Optional

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from creativeflow.mlops_service.core.config import Settings
from creativeflow.mlops_service.utils.exceptions import DeploymentFailedException


class KubernetesAdapter:
    """Provides an interface to Kubernetes for managing model services."""

    def __init__(self, settings: Settings):
        """
        Initializes the KubernetesAdapter.
        
        Loads Kubernetes configuration either from a specified file or from
        within a cluster.
        """
        try:
            if settings.KUBERNETES_CONFIG_PATH:
                config.load_kube_config(config_file=settings.KUBERNETES_CONFIG_PATH)
            else:
                config.load_incluster_config()
            
            self.apps_v1 = client.AppsV1Api()
            self.core_v1 = client.CoreV1Api()
        except config.ConfigException as e:
            # This is a critical failure, the service cannot operate without K8s access
            raise RuntimeError(f"Could not configure Kubernetes client: {e}")

    async def _run_in_thread(self, func, *args, **kwargs):
        """Runs a synchronous function in a separate thread."""
        return await asyncio.to_thread(func, *args, **kwargs)

    async def apply_deployment(self, namespace: str, manifest: Dict[str, Any]) -> client.V1Deployment:
        """
        Creates or updates a Kubernetes Deployment.

        Args:
            namespace: The target namespace.
            manifest: The deployment manifest as a dictionary.

        Returns:
            The created or updated V1Deployment object.

        Raises:
            DeploymentFailedException: If the API call fails.
        """
        try:
            name = manifest["metadata"]["name"]
            # Check if deployment exists to decide between create and replace/patch
            try:
                await self._run_in_thread(self.apps_v1.read_namespaced_deployment, name=name, namespace=namespace)
                api_response = await self._run_in_thread(
                    self.apps_v1.patch_namespaced_deployment, name=name, namespace=namespace, body=manifest
                )
            except ApiException as e:
                if e.status == 404: # Not found, so create
                    api_response = await self._run_in_thread(
                        self.apps_v1.create_namespaced_deployment, namespace=namespace, body=manifest
                    )
                else:
                    raise
            return api_response
        except ApiException as e:
            raise DeploymentFailedException(f"Failed to apply K8s deployment: {e.reason}")

    async def delete_deployment(self, namespace: str, name: str) -> client.V1Status:
        """
        Deletes a Kubernetes Deployment.

        Args:
            namespace: The deployment's namespace.
            name: The name of the deployment.

        Returns:
            The V1Status object from the delete call.

        Raises:
            DeploymentFailedException: If the API call fails.
        """
        try:
            return await self._run_in_thread(
                self.apps_v1.delete_namespaced_deployment, name=name, namespace=namespace
            )
        except ApiException as e:
            if e.status == 404: # Already deleted, which is fine
                return client.V1Status(status="Success", reason="Already deleted")
            raise DeploymentFailedException(f"Failed to delete K8s deployment: {e.reason}")

    async def get_deployment_status(self, namespace: str, name: str) -> Optional[client.V1DeploymentStatus]:
        """
        Gets the status of a specific Kubernetes Deployment.

        Args:
            namespace: The deployment's namespace.
            name: The name of the deployment.

        Returns:
            The V1DeploymentStatus object or None if not found.
        """
        try:
            deployment = await self._run_in_thread(self.apps_v1.read_namespaced_deployment_status, name=name, namespace=namespace)
            return deployment.status
        except ApiException as e:
            if e.status == 404:
                return None
            raise DeploymentFailedException(f"Failed to get K8s deployment status: {e.reason}")

    async def apply_service(self, namespace: str, manifest: Dict[str, Any]) -> client.V1Service:
        """
        Creates or updates a Kubernetes Service.

        Args:
            namespace: The target namespace.
            manifest: The service manifest as a dictionary.

        Returns:
            The created or updated V1Service object.

        Raises:
            DeploymentFailedException: If the API call fails.
        """
        try:
            name = manifest["metadata"]["name"]
            try:
                await self._run_in_thread(self.core_v1.read_namespaced_service, name=name, namespace=namespace)
                api_response = await self._run_in_thread(
                    self.core_v1.patch_namespaced_service, name=name, namespace=namespace, body=manifest
                )
            except ApiException as e:
                if e.status == 404:
                    api_response = await self._run_in_thread(
                        self.core_v1.create_namespaced_service, namespace=namespace, body=manifest
                    )
                else:
                    raise
            return api_response
        except ApiException as e:
            raise DeploymentFailedException(f"Failed to apply K8s service: {e.reason}")

    async def delete_service(self, namespace: str, name: str) -> client.V1Status:
        """
        Deletes a Kubernetes Service.

        Args:
            namespace: The service's namespace.
            name: The name of the service.

        Returns:
            The V1Status object from the delete call.

        Raises:
            DeploymentFailedException: If the API call fails.
        """
        try:
            return await self._run_in_thread(
                self.core_v1.delete_namespaced_service, name=name, namespace=namespace
            )
        except ApiException as e:
            if e.status == 404:
                return client.V1Status(status="Success", reason="Already deleted")
            raise DeploymentFailedException(f"Failed to delete K8s service: {e.reason}")

    async def get_pod_logs(self, namespace: str, pod_name: str, container_name: Optional[str] = None) -> str:
        """
        Retrieves logs from a specific pod.

        Args:
            namespace: The pod's namespace.
            pod_name: The name of the pod.
            container_name: The name of the container within the pod (optional).

        Returns:
            The logs as a string.
        """
        try:
            return await self._run_in_thread(
                self.core_v1.read_namespaced_pod_log,
                name=pod_name,
                namespace=namespace,
                container=container_name
            )
        except ApiException as e:
            raise DeploymentFailedException(f"Failed to get pod logs: {e.reason}")