"""
Initializes the 'core' submodule, exporting common utilities and constants.
"""
from .constants import (
    CORRELATION_ID_LOG_KEY,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    MAX_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    REQUEST_ID_HEADER,
    STANDARD_DATETIME_FORMAT,
)
from .utils import deep_merge_dicts, generate_unique_id, parse_datetime_string

__all__ = [
    "generate_unique_id",
    "deep_merge_dicts",
    "parse_datetime_string",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "MAX_USERNAME_LENGTH",
    "MIN_PASSWORD_LENGTH",
    "REQUEST_ID_HEADER",
    "CORRELATION_ID_LOG_KEY",
    "STANDARD_DATETIME_FORMAT",
]