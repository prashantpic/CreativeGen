"""
Defines custom exceptions for infrastructure or external service failures.
"""
from typing import Optional

from .base import BaseCreativeFlowError


class ServiceUnavailableError(BaseCreativeFlowError):
    """Exception raised when a dependent service is unavailable."""

    def __init__(
        self, service_name: str, error_code: str = "SERVICE_UNAVAILABLE"
    ) -> None:
        message = f"The service '{service_name}' is currently unavailable."
        details = {"service_name": service_name}
        super().__init__(message, error_code=error_code, details=details)


class ConfigurationError(BaseCreativeFlowError):
    """Exception raised for errors related to system configuration."""

    def __init__(
        self, message: str, error_code: str = "CONFIGURATION_ERROR"
    ) -> None:
        super().__init__(message, error_code=error_code)


class ExternalAPIFailureError(BaseCreativeFlowError):
    """Exception raised when an external API call fails."""

    def __init__(
        self,
        service_name: str,
        original_error: Optional[Exception] = None,
        error_code: str = "EXTERNAL_API_FAILURE",
    ) -> None:
        message = f"An error occurred while communicating with '{service_name}'."
        details = {
            "service_name": service_name,
            "original_error": str(original_error) if original_error else None,
        }
        super().__init__(message, error_code=error_code, details=details)


class DatabaseConnectionError(BaseCreativeFlowError):
    """Exception raised for failures in connecting to the database."""

    def __init__(
        self,
        message: str = "Database connection failed",
        error_code: str = "DB_CONNECTION_ERROR",
    ) -> None:
        super().__init__(message, error_code=error_code)