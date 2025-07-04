"""
Custom exception classes for the MLOps service.

This module defines specific exception types that can be raised by the service
layers and caught by FastAPI exception handlers to return appropriate HTTP
responses with clear error messages.
"""
from fastapi import HTTPException, status

class MLOpsServiceException(HTTPException):
    """Base exception for all MLOps service errors."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ModelNotFoundException(MLOpsServiceException):
    """Raised when an AI Model is not found in the registry."""
    def __init__(self, model_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with ID '{model_id}' not found."
        )


class ModelVersionNotFoundException(MLOpsServiceException):
    """Raised when an AI Model Version is not found."""
    def __init__(self, version_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model Version with ID '{version_id}' not found."
        )


class DeploymentFailedException(MLOpsServiceException):
    """Raised when a model deployment to Kubernetes fails."""
    def __init__(self, detail: str = "Model deployment failed."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ValidationFailedException(MLOpsServiceException):
    """Raised when a model validation process fails."""
    def __init__(self, detail: str = "Model validation failed."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ArtifactUploadFailedException(MLOpsServiceException):
    """Raised when an artifact upload to storage fails."""
    def __init__(self, detail: str = "Model artifact upload failed."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class InvalidStateTransitionException(MLOpsServiceException):
    """Raised when a model version status update is invalid."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )