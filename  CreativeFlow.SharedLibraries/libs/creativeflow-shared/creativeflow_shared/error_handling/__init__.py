"""
Initializes the 'error_handling' submodule.

Exports custom exception classes and error reporting utilities to provide
a standardized error management framework.
"""
from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    BaseAppException,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    RateLimitExceededError,
    UnprocessableEntityError,
    ValidationError,
)
from .error_reporter import init_error_tracking, report_exception

__all__ = [
    "BaseAppException",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "UnprocessableEntityError",
    "ExternalServiceError",
    "RateLimitExceededError",
    "init_error_tracking",
    "report_exception",
]