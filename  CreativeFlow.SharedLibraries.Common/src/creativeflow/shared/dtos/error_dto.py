"""
Defines a standardized Data Transfer Object (DTO) for error responses.
"""
from typing import Any, Optional

from .base_dto import BaseDTO


class ErrorResponseDTO(BaseDTO):
    """
    A standardized DTO for returning error information in API responses.

    This ensures that all error responses across the platform have a
    consistent and predictable structure.

    Attributes:
        error_code: A unique, machine-readable code for the error.
        message: A human-readable message describing the error.
        details: Optional additional information about the error, which can be
                 a simple string, a dictionary, or a list of validation issues.
    """

    error_code: str
    message: str
    details: Optional[Any] = None