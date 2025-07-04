"""
Custom exception classes for the MLOps service.
"""

from fastapi import HTTPException
from starlette import status


class MLOpsServiceException(HTTPException):
    """Base class for all MLOps service-specific exceptions."""
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)


class ModelNotFoundException(MLOpsServiceException):
    """Raised when an AI model is not found in the registry."""
    def __init__(self, model_id: str):
        super().__init__(
            detail=f"Model with ID '{model_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ModelVersionNotFoundException(MLOpsServiceException):
    """Raised when an AI model version is not found."""
    def __init__(self, version_id: str):
        super().__init__(
            detail=f"Model version with ID '{version_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
class DeploymentNotFoundException(MLOpsServiceException):
    """Raised when a deployment is not found."""
    def __init__(self, deployment_id: str):
        super().__init__(
            detail=f"Deployment with ID '{deployment_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class DeploymentFailedException(MLOpsServiceException):
    """Raised when a Kubernetes deployment operation fails."""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class ValidationFailedException(MLOpsServiceException):
    """Raised when a model validation process fails or cannot be completed."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(
            detail=detail,
            status_code=status_code
        )

class ArtifactOperationFailedException(MLOpsServiceException):
    """Raised when an operation on a model artifact (e.g., upload/download) fails."""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            detail=detail,
            status_code=status_code
        )

class InvalidStateTransitionException(MLOpsServiceException):
    """Raised when an invalid status change is attempted on an entity."""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT # 409 Conflict is appropriate here
        )