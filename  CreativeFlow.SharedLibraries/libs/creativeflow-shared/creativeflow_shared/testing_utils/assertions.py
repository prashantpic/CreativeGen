"""
Defines custom assertion helper functions to simplify common assertion
patterns in tests, making tests more readable and maintainable.

Requirement Mapping: NFR-011 (Testability)
"""

import datetime
from typing import Any

import pydantic


def assert_dtos_equal_ignoring_fields(
    dto1: pydantic.BaseModel, dto2: pydantic.BaseModel, ignore_fields: list[str]
) -> None:
    """
    Asserts that two Pydantic models are equal, ignoring specified fields.

    Args:
        dto1: The first DTO to compare.
        dto2: The second DTO to compare.
        ignore_fields: A list of field names (strings) to exclude from comparison.
    """
    dict1 = dto1.model_dump()
    dict2 = dto2.model_dump()

    for field in ignore_fields:
        dict1.pop(field, None)
        dict2.pop(field, None)

    assert dict1 == dict2


def assert_timestamp_approx_now(
    timestamp: datetime.datetime, tolerance_seconds: int = 5
) -> None:
    """
    Asserts that a given timestamp is approximately now (UTC).

    Args:
        timestamp: The datetime object to check.
        tolerance_seconds: The allowed difference in seconds.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # Ensure the provided timestamp is also timezone-aware for comparison
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
    delta = abs(now_utc - timestamp)
    assert delta < datetime.timedelta(
        seconds=tolerance_seconds
    ), f"Timestamp difference {delta} exceeds tolerance of {tolerance_seconds}s"


def assert_api_error_response(
    response: Any,
    expected_status_code: int,
    expected_error_code: str | None = None,
    expected_message_contains: str | None = None,
) -> None:
    """
    Asserts common properties of a standardized API error response.

    This helper is useful for testing API endpoints that return
    `ErrorResponseDTO`.

    Args:
        response: The HTTP response object (e.g., from FastAPI's TestClient).
        expected_status_code: The expected HTTP status code.
        expected_error_code: The expected internal error code in the response body.
        expected_message_contains: A substring expected to be in the error message.
    """
    assert response.status_code == expected_status_code
    error_data = response.json()

    # The top-level error message or list of details
    detail = error_data.get("detail")
    assert detail is not None

    if expected_message_contains:
        if isinstance(detail, str):
            assert expected_message_contains in detail
        elif isinstance(detail, list) and detail:
            # Check if the message is in any of the detail items
            assert any(expected_message_contains in item.get("message", "") for item in detail)

    if expected_error_code:
        assert isinstance(detail, list) and detail, "Error details list is required for error code check"
        # Check if the code is in any of the detail items
        assert any(item.get("code") == expected_error_code for item in detail)