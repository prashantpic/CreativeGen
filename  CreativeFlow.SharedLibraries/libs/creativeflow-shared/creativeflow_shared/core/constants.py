"""
Defines shared constants used across various parts of the CreativeFlow AI platform.
Centralizing constants here ensures consistency and eases maintenance.

Requirement Mapping: NFR-008 (Code Quality)
"""

# Pagination
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100

# User Model Constraints
MAX_USERNAME_LENGTH: int = 50
MIN_PASSWORD_LENGTH: int = 12

# HTTP Headers and Logging Keys
REQUEST_ID_HEADER: str = "X-Request-ID"
CORRELATION_ID_LOG_KEY: str = "correlation_id"

# Date/Time Formats
STANDARD_DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"