"""
Defines various enumerations used throughout the MLOps domain.

This module provides standardized Enum classes for managing states, types, and
strategies consistently across the service, from the domain layer to the API.
"""
from enum import Enum


class ModelVersionStatusEnum(str, Enum):
    """Enumeration for the lifecycle status of an AI Model Version."""
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
    INACTIVE_BLUEGREEN = "INACTIVE_BLUEGREEN"  # In blue-green, the inactive deployment
    ROLLING_OUT_CANARY = "ROLLING_OUT_CANARY"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    DELETED = "DELETED"
    
class DeploymentStrategyEnum(str, Enum):
    """Enumeration for deployment strategies."""
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING_UPDATE = "rolling_update"

class DeploymentEnvironmentEnum(str, Enum):
    """Enumeration for deployment environments."""
    STAGING = "staging"
    PRODUCTION = "production"

class ValidationStatusEnum(str, Enum):
    """Enumeration for the status of a validation process."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"  # For non-critical issues
    SKIPPED = "SKIPPED"
    
class ValidationScanTypeEnum(str, Enum):
    """Enumeration for different types of validation scans."""
    SECURITY_CONTAINER = "security_container"
    SECURITY_ARTIFACT = "security_artifact"
    FUNCTIONAL_IO = "functional_io"
    PERFORMANCE_BENCHMARK = "performance_benchmark"
    CONTENT_SAFETY = "content_safety"


class ModelFormatEnum(str, Enum):
    """Enumeration for the format of a model artifact."""
    ONNX = "ONNX"
    TENSORFLOW_SAVEDMODEL = "TENSORFLOW_SAVEDMODEL"
    PYTORCH_TORCHSCRIPT = "PYTORCH_TORCHSCRIPT"
    CUSTOM_PYTHON_CONTAINER = "CUSTOM_PYTHON_CONTAINER"
    OTHER = "OTHER"


class ServingInterfaceEnum(str, Enum):
    """Enumeration for the serving interface/framework for a model."""
    TENSORFLOW_SERVING = "TENSORFLOW_SERVING"
    TORCHSERVE = "TORCHSERVE"
    TRITON_INFERENCE_SERVER = "TRITON_INFERENCE_SERVER"
    CUSTOM_FASTAPI = "CUSTOM_FASTAPI"
    CUSTOM_FLASK = "CUSTOM_FLASK"


class ModelTaskTypeEnum(str, Enum):
    """Enumeration for the primary task of an AI Model."""
    IMAGE_GENERATION = "ImageGeneration"
    TEXT_GENERATION = "TextGeneration"
    IMAGE_TRANSFORMATION = "ImageTransformation"
    STYLE_TRANSFER = "StyleTransfer"
    CONTENT_SAFETY = "ContentSafety"
    OTHER = "Other"