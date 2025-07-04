"""
Defines a standardized Data Transfer Object (DTO) for paginated list responses.
"""
from typing import Generic, List, TypeVar

from pydantic import Field

from .base_dto import BaseDTO

T = TypeVar("T")


class PaginatedResponseDTO(BaseDTO, Generic[T]):
    """
    A generic DTO for representing paginated API responses.

    This provides a consistent structure for any API endpoint that returns a
    list of items, making it easy for clients to handle pagination.

    Attributes:
        items: The list of items for the current page.
        total_items: The total number of items available across all pages.
        page: The current page number (1-indexed).
        page_size: The number of items per page.
        total_pages: The total number of pages available.
    """

    items: List[T] = Field(..., description="List of items for the current page.")
    total_items: int = Field(
        ..., ge=0, description="Total number of items available."
    )
    page: int = Field(..., gt=0, description="Current page number.")
    page_size: int = Field(..., gt=0, description="Number of items per page.")
    total_pages: int = Field(..., ge=0, description="Total number of pages.")