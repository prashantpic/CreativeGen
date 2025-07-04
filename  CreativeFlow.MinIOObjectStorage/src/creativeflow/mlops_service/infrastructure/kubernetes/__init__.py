"""
Initializes the Kubernetes infrastructure package.

This package contains adapters for interacting with the Kubernetes API,
abstracting the complexities of deploying and managing model serving
containers from the core application logic.
"""
from .k8s_adapter import KubernetesAdapter

__all__ = ["KubernetesAdapter"]