"""
Contains shared PyTest fixtures that can be used across test suites.
"""
import logging
from unittest.mock import MagicMock

import pytest

from ..logging.config import _logging_configured, setup_logging


@pytest.fixture
def mock_shared_logger() -> MagicMock:
    """
    Provides a MagicMock object that can be used to mock a logger instance.

    Example usage in a test:

    @patch('your_service_module.logger', new_callable=mock_shared_logger)
    def test_something_that_logs(mock_logger_instance):
        your_function_that_logs()
        mock_logger_instance.info.assert_called_with("Expected log message")
    """
    return MagicMock(spec=logging.Logger)


@pytest.fixture(scope="session", autouse=True)
def ensure_logging_configured_for_tests() -> None:
    """
    A session-scoped, auto-used fixture to ensure logging is configured once
    for the entire test suite. This prevents errors in utilities that rely on
    the logger being set up.
    """
    if not _logging_configured:
        setup_logging(log_level="DEBUG", service_name="pytest-shared-lib-tests")