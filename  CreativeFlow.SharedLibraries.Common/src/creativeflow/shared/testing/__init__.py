"""
Initializes the shared testing utilities sub-package.
"""
from .mocks import create_mock_error_response_dto, create_mock_paginated_response_dto

__all__ = [
    "create_mock_error_response_dto",
    "create_mock_paginated_response_dto",
]