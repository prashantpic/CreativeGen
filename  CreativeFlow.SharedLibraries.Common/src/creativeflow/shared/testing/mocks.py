"""
Contains common mock objects and test data factories to aid in testing.
"""
import math
from typing import Any, List, Optional, TypeVar

from ..dtos.error_dto import ErrorResponseDTO
from ..dtos.pagination_dto import PaginatedResponseDTO

T = TypeVar("T")


def create_mock_error_response_dto(
    error_code: str = "TEST_ERROR",
    message: str = "A test error occurred.",
    details: Optional[Any] = None,
) -> ErrorResponseDTO:
    """Creates a mock `ErrorResponseDTO` instance for testing."""
    return ErrorResponseDTO(error_code=error_code, message=message, details=details)


def create_mock_paginated_response_dto(
    items: List[T],
    total_items: Optional[int] = None,
    page: int = 1,
    page_size: int = 10,
) -> PaginatedResponseDTO[T]:
    """
    Creates a mock `PaginatedResponseDTO` instance for testing.

    Calculates `total_pages` based on the provided data.
    """
    if total_items is None:
        total_items = len(items)

    if total_items == 0:
        total_pages = 0
        current_page = 0
    elif page_size > 0:
        total_pages = math.ceil(total_items / page_size)
        current_page = page
    else:  # page_size is 0 or negative, which is invalid
        total_pages = 0
        current_page = page

    return PaginatedResponseDTO(
        items=items,
        total_items=total_items,
        page=current_page,
        page_size=page_size,
        total_pages=total_pages,
    )