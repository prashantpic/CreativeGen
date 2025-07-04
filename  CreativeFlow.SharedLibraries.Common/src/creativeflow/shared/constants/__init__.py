"""
Initializes the constants sub-package and exports its defined constants.
"""
from .general import (
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    EMAIL_REGEX,
    MAX_FULL_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
    UUID_REGEX,
)

__all__ = [
    "DEFAULT_REQUEST_TIMEOUT_SECONDS",
    "EMAIL_REGEX",
    "MAX_FULL_NAME_LENGTH",
    "MAX_USERNAME_LENGTH",
    "UUID_REGEX",
]