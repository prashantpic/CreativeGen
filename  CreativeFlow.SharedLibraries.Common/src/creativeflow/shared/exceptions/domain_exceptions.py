"""
Defines custom exceptions for business logic and domain rule violations.
"""
from typing import Any, Optional

from .base import BaseCreativeFlowError


class ValidationError(BaseCreativeFlowError):
    """
    Exception raised for input data validation failures.

    Typically used when incoming data (e.g., from an API request) does not
    conform to the expected schema or rules. The `details` attribute often
    contains structured information about which fields failed validation.
    """

    def __init__(
        self,
        message: str = "Input validation failed",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, error_code=error_code, details=details)


class ResourceNotFoundError(BaseCreativeFlowError):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        resource_name: str,
        resource_id: Any,
        error_code: str = "RESOURCE_NOT_FOUND",
    ) -> None:
        message = f"{resource_name} with ID '{resource_id}' not found."
        details = {"resource_name": resource_name, "resource_id": resource_id}
        super().__init__(message, error_code=error_code, details=details)


class AuthenticationError(BaseCreativeFlowError):
    """Exception raised for failed authentication attempts."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_FAILURE",
    ) -> None:
        super().__init__(message, error_code=error_code)


class AuthorizationError(BaseCreativeFlowError):
    """Exception raised when an authenticated user lacks permission for an action."""

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "AUTHORIZATION_FAILURE",
    ) -> None:
        super().__init__(message, error_code=error_code)


class BusinessRuleViolationError(BaseCreativeFlowError):
    """

    Exception raised for violations of specific business rules that are not
    covered by other standard exceptions. For example, trying to create a
    duplicate resource that must be unique.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "BUSINESS_RULE_VIOLATION",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, error_code=error_code, details=details)