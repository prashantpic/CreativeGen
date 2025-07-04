"""
Defines a hierarchy of custom exception classes for the application.
This allows for standardized error handling and reporting across services.

Requirement Mapping: NFR-009 (Modularity)
"""
from typing import Any

from ..datamodels.common import ErrorDetailDTO


class BaseAppException(Exception):
    """Base exception for all application-specific errors."""

    status_code: int = 500
    message: str = "An unexpected error occurred."
    error_code: str | None = "INTERNAL_SERVER_ERROR"
    details: list[ErrorDetailDTO] | None = None

    def __init__(
        self,
        message: str | None = None,
        status_code: int | None = None,
        error_code: str | None = None,
        details: list[ErrorDetailDTO] | None = None,
        **kwargs: Any,
    ):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.details = details or self.details
        # Allow extra context to be passed
        self.extra_context = kwargs
        super().__init__(self.message)


class NotFoundError(BaseAppException):
    """Raised when a requested resource is not found."""

    status_code = 404
    message = "Resource not found."
    error_code = "RESOURCE_NOT_FOUND"


class ValidationError(BaseAppException):
    """Raised for input validation failures (e.g., from Pydantic)."""

    status_code = 422
    message = "Input validation failed."
    error_code = "VALIDATION_ERROR"


class AuthenticationError(BaseAppException):
    """Raised for authentication failures (e.g., invalid credentials, bad token)."""

    status_code = 401
    message = "Authentication failed."
    error_code = "AUTHENTICATION_FAILURE"


class AuthorizationError(BaseAppException):
    """Raised when an authenticated user lacks permission for an action."""

    status_code = 403
    message = "Permission denied."
    error_code = "AUTHORIZATION_FAILURE"


class ConflictError(BaseAppException):
    """Raised when an action cannot be completed due to a conflict with the current state of the resource."""

    status_code = 409
    message = "Resource conflict."
    error_code = "CONFLICT_ERROR"


class UnprocessableEntityError(BaseAppException):
    """Raised for business logic errors on semantically correct but invalid data."""

    status_code = 422
    message = "Unprocessable entity."
    error_code = "UNPROCESSABLE_ENTITY"


class ExternalServiceError(BaseAppException):
    """Raised for errors when communicating with a downstream or external service."""

    status_code = 502  # Bad Gateway is a common choice
    message = "Error communicating with an external service."
    error_code = "EXTERNAL_SERVICE_ERROR"

    def __init__(self, service_name: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_name = service_name
        if service_name:
            self.message = f"Error communicating with the '{service_name}' service."


class RateLimitExceededError(BaseAppException):
    """Raised when a user or client exceeds their allowed request rate."""

    status_code = 429
    message = "Rate limit exceeded."
    error_code = "RATE_LIMIT_EXCEEDED"

    def __init__(self, retry_after: int | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after