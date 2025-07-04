"""
Initializes the storage infrastructure package.

This package contains adapters for interacting with external object storage
systems, such as MinIO, abstracting the specific implementation details
from the service layer.
"""
from .minio_adapter import MinioAdapter

__all__ = ["MinioAdapter"]