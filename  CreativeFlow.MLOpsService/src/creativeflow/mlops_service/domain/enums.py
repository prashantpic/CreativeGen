"""
Defines various enumerations used throughout the MLOps domain.

These enums provide a standardized and consistent way to represent states,
types, and formats, preventing errors from magic strings and improving
code readability.
"""
from enum import Enum


class ModelVersionStatusEnum(str, Enum):
    """Enumeration for the status of an AI Model Version."""
    STAGING = "STAGING"
    PENDING_VALIDATION = "PENDING_VALIDATION"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATED = "VALIDATED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class DeploymentStatusEnum(str, Enum):
    """Enumeration for the status of a model deployment."""
    REQUESTED = "REQUESTED"
    DEPLOYING = "DEPLOYING"
    ACTIVE = "ACTIVE"
    INACTIVE_BLUEGREEN = "INACTIVE_BLUEGREEN"
    ROLLING_OUT_CANARY = "ROLLING_OUT_CANARY"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    DELETED = "DELETED"


class ValidationStatusEnum(str, Enum):
    """Enumeration for the status of a validation process."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class ModelFormatEnum(str, Enum):
    """Enumeration for the format of a model artifact."""
    ONNX = "ONNX"
    TENSORFLOW_SAVEDMODEL = "TENSORFLOW_SAVEDMODEL"
    PYTORCH_TORCHSCRIPT = "PYTORCH_TORCHSCRIPT"
    CUSTOM_PYTHON_CONTAINER = "CUSTOM_PYTHON_CONTAINER"
    OTHER = "OTHER"


class ServingInterfaceEnum(str, Enum):
    """Enumeration for the model serving interface/framework."""
    TENSORFLOW_SERVING = "TENSORFLOW_SERVING"
    TORCHSERVE = "TORCHSERVE"
    TRITON_INFERENCE_SERVER = "TRITON_INFERENCE_SERVER"
    CUSTOM_FASTAPI = "CUSTOM_FASTAPI"
    CUSTOM_FLASK = "CUSTOM_FLASK"