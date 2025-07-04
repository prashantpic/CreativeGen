"""
Initializes the 'datamodels' submodule.

Exports base Pydantic models and common DTOs used for inter-service
communication or as standardized API contracts.

Requirement Mapping: NFR-009 (Modularity)
"""
from .base import SharedBaseModel, to_camel_case
from .common import (
    ErrorDetailDTO,
    ErrorResponseDTO,
    PaginatedResponseDTO,
    PaginationInfoDTO,
    SortOrderEnum,
    UserContextDTO,
)

__all__ = [
    "SharedBaseModel",
    "to_camel_case",
    "ErrorDetailDTO",
    "ErrorResponseDTO",
    "UserContextDTO",
    "PaginationInfoDTO",
    "PaginatedResponseDTO",
    "SortOrderEnum",
]