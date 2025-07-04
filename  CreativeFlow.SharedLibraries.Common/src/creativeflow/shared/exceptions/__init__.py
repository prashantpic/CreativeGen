"""
Initializes the exceptions sub-package and exports custom exception classes.
"""
from .base import BaseCreativeFlowError
from .domain_exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessRuleViolationError,
    ResourceNotFoundError,
    ValidationError,
)
from .infra_exceptions import (
    ConfigurationError,
    DatabaseConnectionError,
    ExternalAPIFailureError,
    ServiceUnavailableError,
)

__all__ = [
    # Base Exception
    "BaseCreativeFlowError",
    # Domain Exceptions
    "ValidationError",
    "ResourceNotFoundError",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessRuleViolationError",
    # Infrastructure Exceptions
    "ServiceUnavailableError",
    "ConfigurationError",
    "ExternalAPIFailureError",
    "DatabaseConnectionError",
]