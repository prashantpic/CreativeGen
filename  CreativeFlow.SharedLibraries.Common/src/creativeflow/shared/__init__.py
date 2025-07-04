"""
Main package initializer for the creativeflow.shared library.

This file exports key modules, classes, and functions to provide a clean
public API for consumers of this shared library, managing its public interface.
"""
from .constants.general import (
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    EMAIL_REGEX,
    MAX_FULL_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
    UUID_REGEX,
)
from .dtos.base_dto import BaseDTO
from .dtos.error_dto import ErrorResponseDTO
from .dtos.pagination_dto import PaginatedResponseDTO
from .exceptions.base import BaseCreativeFlowError
from .exceptions.domain_exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessRuleViolationError,
    ResourceNotFoundError,
    ValidationError,
)
from .exceptions.infra_exceptions import (
    ConfigurationError,
    DatabaseConnectionError,
    ExternalAPIFailureError,
    ServiceUnavailableError,
)
from .i18n.formatters import (
    format_currency_localized,
    format_date_localized,
    format_datetime_localized,
    format_number_localized,
    format_time_localized,
)
from .i18n.utils import get_timezone_aware_datetime, get_user_locale
from .logging.config import setup_logging
from .logging.logger import get_logger
from .security.sanitization import sanitize_html_output
from .security.validation import is_valid_email, is_valid_uuid, validate_payload
from .utils.collections import chunk_list, deep_merge_dicts
from .utils.decorators import memoize, timed

__all__ = [
    # Constants
    "DEFAULT_REQUEST_TIMEOUT_SECONDS",
    "MAX_USERNAME_LENGTH",
    "MAX_FULL_NAME_LENGTH",
    "EMAIL_REGEX",
    "UUID_REGEX",
    # Exceptions
    "BaseCreativeFlowError",
    "ValidationError",
    "ResourceNotFoundError",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessRuleViolationError",
    "ServiceUnavailableError",
    "ConfigurationError",
    "ExternalAPIFailureError",
    "DatabaseConnectionError",
    # DTOs
    "BaseDTO",
    "ErrorResponseDTO",
    "PaginatedResponseDTO",
    # Logging
    "setup_logging",
    "get_logger",
    # Security
    "validate_payload",
    "is_valid_email",
    "is_valid_uuid",
    "sanitize_html_output",
    # I18n
    "format_datetime_localized",
    "format_date_localized",
    "format_time_localized",
    "format_number_localized",
    "format_currency_localized",
    "get_user_locale",
    "get_timezone_aware_datetime",
    # Utils
    "chunk_list",
    "deep_merge_dicts",
    "timed",
    "memoize",
]