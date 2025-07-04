"""
Contains reusable mock objects and classes for external dependencies or complex
internal components. This helps in isolating units under test.

Requirement Mapping: NFR-011 (Testability)
"""
import contextlib
import datetime
from typing import Any, Generator
from unittest.mock import MagicMock, patch


class MockExternalServiceClient:
    """
    A mock class for an external service client.
    Methods can be pre-configured to return specific values or MagicMocks.
    """

    def __init__(self):
        self.perform_action = MagicMock(return_value={"status": "success"})
        self.get_data = MagicMock(return_value={"id": "123", "data": "some_value"})


class MockCacheClient:
    """
    A simple in-memory dictionary-based mock for a Redis-like cache client.
    """

    def __init__(self):
        self._cache = {}
        self.get = MagicMock(side_effect=self._get)
        self.set = MagicMock(side_effect=self._set)
        self.delete = MagicMock(side_effect=self._delete)

    def _get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def _set(self, key: str, value: Any, *args, **kwargs) -> None:
        self._cache[key] = value

    def _delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]


@contextlib.contextmanager
def patch_datetime_now(
    fixed_datetime: datetime.datetime,
) -> Generator[None, None, None]:
    """
    A context manager to patch `datetime.datetime.now()` and `utcnow()`
    to return a fixed datetime object during tests.

    Args:
        fixed_datetime: The datetime object that should be returned by now() and utcnow().
    """
    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_datetime
        mock_dt.utcnow.return_value = fixed_datetime
        # Ensure that other attributes like `strptime` still work
        mock_dt.strptime = datetime.datetime.strptime
        yield