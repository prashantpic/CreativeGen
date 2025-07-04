"""
This module defines a standardized hierarchy of custom exceptions for consistent
error handling across all backend services. This allows middleware in the API
Gateway or individual services to catch specific exceptions and generate
predictable HTTP responses.
"""

from typing import Any, Dict, Optional, Mapping


class BaseAPIException(Exception):
    """Base class for all custom API exceptions in the CreativeFlow platform."""
    status_code: int = 500
    detail: str = "An internal server error occurred."

    def __init__(self, detail: Optional[str] = None, **kwargs: Any) -> None:
        """
        Initializes the exception.

        Args:
            detail: A specific error message to override the default.
            **kwargs: Any additional key-value pairs to include in the response.
        """
        self.detail = detail or self.detail
        self.extra_info = kwargs
        super().__init__(self.detail)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the exception details to a dictionary for API responses."""
        response = {"detail": self.detail}
        if self.extra_info:
            response.update(self.extra_info)
        return response


class NotFoundException(BaseAPIException):
    """Raised when a requested resource is not found (HTTP 404)."""
    status_code = 404
    detail = "Resource not found."


class ValidationException(BaseAPIException):
    """Raised for data validation errors (HTTP 422)."""
    status_code = 422
    detail = "Validation error."

    def __init__(self, errors: Any, detail: Optional[str] = None) -> None:
        """
        Initializes the validation exception.

        Args:
            errors: The detailed validation errors, typically from Pydantic.
            detail: An optional summary message.
        """
        super().__init__(detail=detail or self.detail, errors=errors)


class AuthenticationException(BaseAPIException):
    """Raised for authentication failures (HTTP 401)."""
    status_code = 401
    detail = "Authentication failed."
    headers: Mapping[str, str] = {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(detail, **kwargs)


class PermissionDeniedException(BaseAPIException):
    """Raised when an authenticated user lacks permissions for an action (HTTP 403)."""
    status_code = 403
    detail = "Permission denied."


class ConflictException(BaseAPIException):
    """Raised when an action conflicts with the current state of a resource (HTTP 409)."""
    status_code = 409
    detail = "Conflict with existing resource."


class ServiceUnavailableException(BaseAPIException):
    """Raised when a required downstream service is unavailable (HTTP 503)."""
    status_code = 503
    detail = "A required downstream service is currently unavailable."