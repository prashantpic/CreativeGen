"""
Defines the base custom exception class for all platform-specific exceptions.
"""
from typing import Any, Optional


class BaseCreativeFlowError(Exception):
    """
    Base exception class for the CreativeFlow AI application.

    All custom exceptions in the application should inherit from this class.
    This allows for a single except block to catch all application-specific
    errors.

    Attributes:
        message (str): The human-readable error message.
        error_code (Optional[str]): A unique, machine-readable code for the error.
        details (Optional[Any]): Additional details or context about the error.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        """
        Initializes the BaseCreativeFlowError.

        Args:
            message: The human-readable error message.
            error_code: A unique code for the error.
            details: Additional context about the error.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details

    def __str__(self) -> str:
        """Returns the string representation of the error."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message