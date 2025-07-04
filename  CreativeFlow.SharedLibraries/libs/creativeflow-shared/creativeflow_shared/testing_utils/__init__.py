"""
Initializes the 'testing_utils' submodule.

Exports shared test fixtures, mock objects, and assertion helpers to
promote consistent and efficient testing across services.

Requirement Mapping: NFR-011 (Testability)
"""

from .assertions import (
    assert_api_error_response,
    assert_dtos_equal_ignoring_fields,
    assert_timestamp_approx_now,
)
from .fixtures import mock_db_session, sample_user_dto, test_correlation_id
from .mocks import MockCacheClient, MockExternalServiceClient, patch_datetime_now

__all__ = [
    # fixtures
    "mock_db_session",
    "sample_user_dto",
    "test_correlation_id",
    # mocks
    "MockExternalServiceClient",
    "patch_datetime_now",
    "MockCacheClient",
    # assertions
    "assert_dtos_equal_ignoring_fields",
    "assert_timestamp_approx_now",
    "assert_api_error_response",
]