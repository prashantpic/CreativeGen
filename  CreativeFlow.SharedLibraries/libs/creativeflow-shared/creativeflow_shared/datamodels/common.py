"""
Contains definitions for commonly used Data Transfer Objects (DTOs).
These are built using Pydantic and inherit from the shared base model
to ensure consistency in data exchange across services.

Requirement Mapping: NFR-009 (Modularity)
"""
import enum
import uuid
from typing import Generic, TypeVar

import pydantic

from .base import SharedBaseModel


# --- Error DTOs ---
class ErrorDetailDTO(SharedBaseModel):
    """
    Represents a detailed error message, often used for validation failures.
    """

    field: str | None = None
    message: str
    code: str | None = None


class ErrorResponseDTO(SharedBaseModel):
    """
    Standardized error response structure for APIs.
    """

    detail: str | list[ErrorDetailDTO]
    request_id: str | None = None


# --- User and Context DTOs ---
class UserContextDTO(SharedBaseModel):
    """
    Represents the user context passed between services or embedded in tokens.
    """

    user_id: uuid.UUID
    email: pydantic.EmailStr
    roles: list[str] = pydantic.Field(default_factory=list)
    permissions: list[str] = pydantic.Field(default_factory=list)
    subscription_tier: str | None = None


# --- Pagination DTOs ---
class PaginationInfoDTO(SharedBaseModel):
    """
    Contains metadata for a paginated list of items.
    """

    total_items: int
    total_pages: int
    current_page: int
    page_size: int


T = TypeVar("T")


class PaginatedResponseDTO(SharedBaseModel, Generic[T]):
    """
    A generic DTO for returning a paginated list of any item type.
    """

    items: list[T]
    pagination: PaginationInfoDTO


# --- Common Enums ---
class SortOrderEnum(str, enum.Enum):
    """
    Defines standard sort orders.
    """

    ASC = "asc"
    DESC = "desc"