#
# CreativeFlow.SharedLibraries - Main Package Initializer
#
# This file defines the public API for the `creativeflow_shared` library.
# It acts as a facade, exporting the most commonly used components from
# its submodules. This simplifies imports for consuming services and
# establishes a clear, curated interface for the library.
#
# Requirement Mapping: NFR-009 (Modularity)
#

# Logging
from .logging.config import get_logger, setup_logging
from .logging.middleware import FastAPILoggingMiddleware

# Error Handling
from .error_handling.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BaseAppException,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    RateLimitExceededError,
    UnprocessableEntityError,
    ValidationError,
)
from .error_handling.error_reporter import init_error_tracking, report_exception

# Data Models
from .datamodels.base import SharedBaseModel
from .datamodels.common import (
    ErrorDetailDTO,
    ErrorResponseDTO,
    PaginatedResponseDTO,
    PaginationInfoDTO,
    SortOrderEnum,
    UserContextDTO,
)

# Security
from .security.sanitization import (
    clean_filename,
    encode_for_html_attribute,
    sanitize_html_input,
)
from .security.validation import is_strong_password, is_valid_uuid, validate_request_payload

# Internationalization (i18n)
from .i18n.formatting import (
    format_currency_localized,
    format_datetime_localized,
    format_number_localized,
)
from .i18n.translation import get_translator, init_translations, translate_message

# Core Utilities
from .core.constants import (
    CORRELATION_ID_LOG_KEY,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    MAX_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    REQUEST_ID_HEADER,
    STANDARD_DATETIME_FORMAT,
)
from .core.utils import deep_merge_dicts, generate_unique_id, parse_datetime_string

# Configuration Management
from .config_management.loader import load_app_config
from .config_management.schemas import (
    BaseConfigSchema,
    DatabaseConfigSchema,
    LoggingConfigSchema,
    RabbitMQConfigSchema,
    RedisConfigSchema,
    SentryConfigSchema,
    ServiceEndpointSchema,
    ThirdPartyServiceConfigSchema,
)

__all__ = [
    # Logging
    "setup_logging",
    "get_logger",
    "FastAPILoggingMiddleware",
    # Error Handling
    "BaseAppException",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "ExternalServiceError",
    "ConflictError",
    "RateLimitExceededError",
    "UnprocessableEntityError",
    "init_error_tracking",
    "report_exception",
    # Data Models
    "SharedBaseModel",
    "ErrorDetailDTO",
    "ErrorResponseDTO",
    "UserContextDTO",
    "PaginationInfoDTO",
    "PaginatedResponseDTO",
    "SortOrderEnum",
    # Security
    "sanitize_html_input",
    "encode_for_html_attribute",
    "clean_filename",
    "validate_request_payload",
    "is_strong_password",
    "is_valid_uuid",
    # Internationalization (i18n)
    "format_datetime_localized",
    "format_number_localized",
    "format_currency_localized",
    "get_translator",
    "translate_message",
    "init_translations",
    # Core Utilities
    "generate_unique_id",
    "deep_merge_dicts",
    "parse_datetime_string",
    # Core Constants
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "MAX_USERNAME_LENGTH",
    "MIN_PASSWORD_LENGTH",
    "REQUEST_ID_HEADER",
    "CORRELATION_ID_LOG_KEY",
    "STANDARD_DATETIME_FORMAT",
    # Configuration Management
    "load_app_config",
    "BaseConfigSchema",
    "DatabaseConfigSchema",
    "RedisConfigSchema",
    "RabbitMQConfigSchema",
    "ServiceEndpointSchema",
    "ThirdPartyServiceConfigSchema",
    "LoggingConfigSchema",
    "SentryConfigSchema",
]