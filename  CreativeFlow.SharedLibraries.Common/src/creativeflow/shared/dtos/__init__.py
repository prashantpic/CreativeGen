"""
Initializes the DTOs sub-package and exports shared DTO classes.
"""
from .base_dto import BaseDTO
from .error_dto import ErrorResponseDTO
from .pagination_dto import PaginatedResponseDTO, T

__all__ = [
    "BaseDTO",
    "ErrorResponseDTO",
    "PaginatedResponseDTO",
    "T",
]