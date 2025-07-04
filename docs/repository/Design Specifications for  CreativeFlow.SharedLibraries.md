# Software Design Specification: CreativeFlow.SharedLibraries

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.SharedLibraries` repository. This repository serves as a centralized collection of common utilities, modules, and configurations designed to be reused across multiple backend microservices within the CreativeFlow AI platform. Its primary goal is to promote code reuse, maintain consistency, and improve the development efficiency and quality of the overall system.

### 1.2 Scope
The scope of this document is limited to the design and implementation of the shared libraries contained within the `CreativeFlow.SharedLibraries` repository. This includes:
*   Core utilities and constants.
*   Standardized Data Transfer Objects (DTOs).
*   A common error handling framework with custom exceptions.
*   Internationalization (i18n) utilities for formatting and translation.
*   Standardized logging configuration and utilities.
*   Security helper functions for sanitization and validation.
*   Shared testing utilities (fixtures, mocks, assertions).
*   Configuration management utilities.

This document will primarily focus on the Python implementation, as detailed in the repository's file structure. Node.js shared libraries, if required for Node.js services, would follow similar principles but are not detailed herein due to lack of specific file structure information for them.

### 1.3 References
This SDS is based on and should be consistent with:
*   System Requirements Specification (SRS) for CreativeFlow AI, particularly sections related to:
    *   Non-Functional Requirements: NFR-008 (Code Quality), NFR-009 (Modularity), NFR-011 (Testability).
    *   Deployment and Operations: DEP-005 (Monitoring and Logging - Standardized Log Format).
    *   User Interface: UI-006 (Multilingual Support - Backend Aspects).
*   CreativeFlow AI Architecture Design Document.
*   Repository definition for `REPO-SHARED-LIBS-001`.

## 2. Overall Design & Architecture

### 2.1 Repository Purpose
`CreativeFlow.SharedLibraries` aims to provide a robust set of reusable components to support various backend services. By centralizing common functionalities, it ensures:
*   **Consistency:** Uniform logging, error handling, data structures, and security practices across the platform.
*   **Reusability:** Reduces code duplication, saving development time and effort.
*   **Maintainability:** Changes to common logic are made in one place.
*   **Testability:** Provides shared utilities to facilitate easier and more consistent testing.

### 2.2 Primary Language and Technologies
*   **Primary Language:** Python 3.11.9
*   **Key Technologies & Libraries (Python):**
    *   **Pydantic (v2.7.4):** For data validation, serialization, and settings management (DTOs, configuration schemas).
    *   **python-json-logger:** For structured JSON logging.
    *   **bleach:** For HTML sanitization.
    *   Python Standard Library (logging, datetime, collections, etc.)
*   **Node.js (Optional):** If Node.js services require shared libraries, equivalent functionalities would be implemented using the Node.js ecosystem (e.g., Winston/Pino for logging, Zod/Joi for validation). This SDS focuses on the Python part due to the provided detailed file structure.

### 2.3 Architectural Principles
*   **Modularity (NFR-009):** Libraries are organized into distinct modules (core, datamodels, error_handling, i18n, logging, security, testing_utils, config_management) with clear responsibilities.
*   **Loose Coupling & High Cohesion:** Modules are designed to be self-contained with well-defined interfaces.
*   **Testability (NFR-011):** Design facilitates unit testing, and shared testing utilities are provided.
*   **Code Quality (NFR-008):** Adherence to PEP 8 and other best practices, enforced by linting and static analysis.
*   **Standardization:** Promotes standard ways of performing common tasks like logging, error handling, and data exchange.

## 3. Packaging and Distribution (Python)

The Python shared library will be packaged using modern Python packaging standards.

### 3.1 `pyproject.toml`
*   **File Path:** `libs/creativeflow-shared/pyproject.toml`
*   **Purpose:** Defines build system requirements, project metadata, and dependencies.
*   **Key Sections & Logic:**
    *   `[build-system]`:
        *   `requires = ["setuptools>=61.0", "wheel"]`
        *   `build-backend = "setuptools.build_meta"`
        *   `backend-path = ["."]` (if `_build_meta.py` is used, otherwise default)
    *   `[project]`:
        *   `name = "creativeflow_shared"`
        *   `version = "0.1.0"` (or dynamically set via CI/CD)
        *   `description = "Shared libraries for the CreativeFlow AI platform."`
        *   `authors = [{ name = "CreativeFlow AI Team", email = "dev@creativeflow.ai" }]`
        *   `license = { file = "LICENSE" }` (assuming a LICENSE file exists)
        *   `readme = "README.md"`
        *   `requires-python = ">=3.11"`
        *   `classifiers = [...]` (e.g., "Programming Language :: Python :: 3.11")
        *   `dependencies = [`
            *   `"pydantic>=2.7.4,<3.0.0"`,
            *   `"python-json-logger>=2.0.0,<3.0.0"`,
            *   `"bleach>=6.0.0,<7.0.0"`,
            *   `"babel>=2.9.0,<3.0.0"` (for i18n formatting)
            *   `# Other common utilities as identified`
            *   `]`
    *   `[project.optional-dependencies]`:
        *   `test = ["pytest", "pytest-cov", "unittest.mock"]`
    *   `[tool.setuptools.packages.find]`:
        *   `where = ["."] `
        *   `include = ["creativeflow_shared*"]`
        *   `exclude = ["tests*"]` (unless tests are intentionally packaged)
*   **Requirement Mapping:** NFR-008

### 3.2 `setup.cfg`
*   **File Path:** `libs/creativeflow-shared/setup.cfg`
*   **Purpose:** Provides static configuration for setuptools, largely superseded by `pyproject.toml` for modern projects but can contain specific options.
*   **Key Sections & Logic:** (Much of this may be redundant if fully utilizing `pyproject.toml`)
    *   `[metadata]`:
        *   Could hold metadata if not fully in `pyproject.toml`.
    *   `[options]`:
        *   `zip_safe = False`
        *   `include_package_data = True`
*   **Requirement Mapping:** NFR-008

### 3.3 `MANIFEST.in`
*   **File Path:** `libs/creativeflow-shared/MANIFEST.in`
*   **Purpose:** Specifies non-code files to include in the source distribution.
*   **Key Sections & Logic:**
    *   `include LICENSE`
    *   `include README.md`
    *   `recursive-include creativeflow_shared/i18n/locales *.mo` (if compiled .mo files are directly packaged)
    *   `# Add other non-Python files that need to be part of the sdist`
*   **Requirement Mapping:** NFR-008

## 4. Module Design Specifications (Python)

### 4.1 Package Initializer: `creativeflow_shared`

*   **File Path:** `libs/creativeflow-shared/creativeflow_shared/__init__.py`
*   **Purpose:** Initializes the main `creativeflow_shared` package and defines its public API by exporting key components from submodules.
*   **Key Features/Responsibilities:**
    *   Provide a clean and curated public interface for the shared library.
    *   Simplify import paths for consumers of the library.
*   **Exported Symbols (Illustrative):**
    python
    # Logging
    from .logging.config import setup_logging, get_logger

    # Error Handling
    from .error_handling.exceptions import (
        BaseAppException,
        AuthenticationError,
        AuthorizationError,
        NotFoundError,
        ValidationError,
        ExternalServiceError,
        ConflictError # Added for common conflict scenarios
    )
    from .error_handling.error_reporter import init_error_tracking, report_exception

    # Data Models
    from .datamodels.base import SharedBaseModel
    from .datamodels.common import (
        ErrorDetailDTO, # Renamed for clarity
        ErrorResponseDTO,
        UserContextDTO, # Define actual fields based on inter-service needs
        PaginationInfoDTO, # Renamed for clarity
        PaginatedResponseDTO
    )

    # Security
    from .security.sanitization import sanitize_html_input, encode_for_html_attribute
    from .security.validation import validate_request_payload, is_strong_password

    # Internationalization (i18n)
    from .i18n.formatting import (
        format_datetime_localized,
        format_number_localized,
        format_currency_localized
    )
    from .i18n.translation import get_translator, translate_message # load_translations might be internal

    # Core Utilities
    from .core.utils import generate_unique_id, deep_merge_dicts
    from .core.constants import DEFAULT_PAGE_SIZE, MAX_USERNAME_LENGTH # Add more as defined

    # Configuration Management
    from .config_management.loader import load_app_config
    from .config_management.schemas import ( # Example config schemas
        BaseConfigSchema,
        DatabaseConfigSchema,
        RedisConfigSchema,
        ServiceEndpointSchema,
        ThirdPartyServiceConfigSchema
    )

    __all__ = [
        "setup_logging", "get_logger",
        "BaseAppException", "AuthenticationError", "AuthorizationError", "NotFoundError", "ValidationError", "ExternalServiceError", "ConflictError",
        "init_error_tracking", "report_exception",
        "SharedBaseModel", "ErrorDetailDTO", "ErrorResponseDTO", "UserContextDTO", "PaginationInfoDTO", "PaginatedResponseDTO",
        "sanitize_html_input", "encode_for_html_attribute",
        "validate_request_payload", "is_strong_password",
        "format_datetime_localized", "format_number_localized", "format_currency_localized",
        "get_translator", "translate_message",
        "generate_unique_id", "deep_merge_dicts",
        "DEFAULT_PAGE_SIZE", "MAX_USERNAME_LENGTH",
        "load_app_config", "BaseConfigSchema", "DatabaseConfigSchema", "RedisConfigSchema", "ServiceEndpointSchema", "ThirdPartyServiceConfigSchema"
    ]
    
*   **Requirement Mapping:** NFR-009

### 4.2 Submodule: `creativeflow_shared.core`

#### 4.2.1 `creativeflow_shared.core.__init__.py`
*   **Purpose:** Initializes the `core` submodule.
*   **Exported Symbols:**
    python
    from .utils import generate_unique_id, deep_merge_dicts, parse_datetime_string # Added parse_datetime
    from .constants import (
        DEFAULT_PAGE_SIZE, MAX_USERNAME_LENGTH,
        REQUEST_ID_HEADER, # Common header for correlation ID
        # Add other shared constants
    )

    __all__ = [
        "generate_unique_id", "deep_merge_dicts", "parse_datetime_string",
        "DEFAULT_PAGE_SIZE", "MAX_USERNAME_LENGTH", "REQUEST_ID_HEADER"
    ]
    

#### 4.2.2 `creativeflow_shared.core.utils.py`
*   **Purpose:** General-purpose utility functions.
*   **Functions:**
    *   `generate_unique_id(prefix: str = None) -> str`:
        *   **Logic:** Generates a UUID v4 string. If a prefix is provided, prepends it to the UUID string (e.g., `f"{prefix}_{uuid.uuid4()}"`).
    *   `deep_merge_dicts(dict1: dict, dict2: dict) -> dict`:
        *   **Logic:** Recursively merges `dict2` into `dict1`. If keys conflict and values are dictionaries, it merges them; otherwise, `dict2`'s value overwrites `dict1`'s. Returns a new dictionary.
    *   `parse_datetime_string(dt_string: str, formats: list[str] = None) -> datetime | None`:
        *   **Logic:** Attempts to parse a datetime string using a list of provided formats or a default set of common ISO formats. Returns a datetime object or None if parsing fails. Handles timezone awareness if present in the string.

#### 4.2.3 `creativeflow_shared.core.constants.py`
*   **Purpose:** Defines shared constants.
*   **Constants:**
    *   `DEFAULT_PAGE_SIZE: int = 20`
    *   `MAX_PAGE_SIZE: int = 100`
    *   `MAX_USERNAME_LENGTH: int = 50`
    *   `MIN_PASSWORD_LENGTH: int = 12`
    *   `REQUEST_ID_HEADER: str = "X-Request-ID"`
    *   `CORRELATION_ID_LOG_KEY: str = "correlation_id"`
    *   `STANDARD_DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"` (ISO 8601 UTC)
    *   `# Add other relevant constants for API versions, timeouts, common enum-like values if not suited for Pydantic Enums in datamodels`
*   **Requirement Mapping:** NFR-008

### 4.3 Submodule: `creativeflow_shared.datamodels`

#### 4.3.1 `creativeflow_shared.datamodels.__init__.py`
*   **Purpose:** Initializes the `datamodels` submodule.
*   **Exported Symbols:**
    python
    from .base import SharedBaseModel, to_camel_case # Expose helper if needed by services
    from .common import (
        ErrorDetailDTO,
        ErrorResponseDTO,
        UserContextDTO,
        PaginationInfoDTO,
        PaginatedResponseDTO,
        SortOrderEnum # Added
    )

    __all__ = [
        "SharedBaseModel", "to_camel_case",
        "ErrorDetailDTO", "ErrorResponseDTO", "UserContextDTO",
        "PaginationInfoDTO", "PaginatedResponseDTO", "SortOrderEnum"
    ]
    
*   **Requirement Mapping:** NFR-009

#### 4.3.2 `creativeflow_shared.datamodels.base.py`
*   **Purpose:** Base Pydantic model with common configurations.
*   **Classes:**
    *   `SharedBaseModel(pydantic.BaseModel)`:
        *   **Configuration (`ConfigDict` for Pydantic v2):**
            *   `model_config = pydantic.ConfigDict(populate_by_name=True, from_attributes=True, alias_generator=to_camel_case)`
            *   `# orm_mode = True` for Pydantic v1 compatibility is `from_attributes=True` in v2.
        *   **Methods:**
            *   `def to_dict_by_alias(self, **kwargs) -> dict:` (Helper to convert model to dict using aliases)
*   **Helper Functions:**
    *   `to_camel_case(snake_str: str) -> str`:
        *   **Logic:** Converts a snake_case string to camelCase. Handles leading underscores if necessary.
*   **Requirement Mapping:** NFR-009

#### 4.3.3 `creativeflow_shared.datamodels.common.py`
*   **Purpose:** Common Data Transfer Objects (DTOs).
*   **Models:**
    *   `ErrorDetailDTO(SharedBaseModel)`:
        *   `field: str | None = None` (Field causing the error, optional)
        *   `message: str` (Error message)
        *   `code: str | None = None` (Optional error code)
    *   `ErrorResponseDTO(SharedBaseModel)`:
        *   `detail: str | list[ErrorDetailDTO]` (Can be a single message or list of detailed errors)
        *   `request_id: str | None = None` (Correlation ID)
    *   `UserContextDTO(SharedBaseModel)`:
        *   `user_id: uuid.UUID`
        *   `email: pydantic.EmailStr`
        *   `roles: list[str] = []` (e.g., ['admin', 'pro_user'])
        *   `permissions: list[str] = []`
        *   `subscription_tier: str | None = None`
    *   `PaginationInfoDTO(SharedBaseModel)`:
        *   `total_items: int`
        *   `total_pages: int`
        *   `current_page: int`
        *   `page_size: int`
    *   `from typing import TypeVar, Generic`
    *   `T = TypeVar('T')`
    *   `PaginatedResponseDTO(SharedBaseModel, Generic[T])`:
        *   `items: list[T]`
        *   `pagination: PaginationInfoDTO`
    *   `import enum`
    *   `class SortOrderEnum(str, enum.Enum):`:
        *   `ASC = "asc"`
        *   `DESC = "desc"`
*   **Requirement Mapping:** NFR-009

### 4.4 Submodule: `creativeflow_shared.error_handling`

#### 4.4.1 `creativeflow_shared.error_handling.__init__.py`
*   **Purpose:** Initializes the `error_handling` submodule.
*   **Exported Symbols:**
    python
    from .exceptions import (
        BaseAppException,
        AuthenticationError,
        AuthorizationError,
        NotFoundError,
        ValidationError,
        ConflictError, # e.g., resource already exists
        UnprocessableEntityError, # For semantic errors in valid data
        ExternalServiceError,
        RateLimitExceededError # Added
    )
    from .error_reporter import init_error_tracking, report_exception

    __all__ = [
        "BaseAppException", "AuthenticationError", "AuthorizationError",
        "NotFoundError", "ValidationError", "ConflictError", "UnprocessableEntityError",
        "ExternalServiceError", "RateLimitExceededError",
        "init_error_tracking", "report_exception"
    ]
    

#### 4.4.2 `creativeflow_shared.error_handling.exceptions.py`
*   **Purpose:** Defines a hierarchy of custom exception classes.
*   **Classes:**
    *   `BaseAppException(Exception)`:
        *   `status_code: int = 500` (Default HTTP status code)
        *   `message: str = "An unexpected error occurred."`
        *   `error_code: str | None = None` (Optional internal error code)
        *   `details: list[ErrorDetailDTO] | None = None`
        *   `__init__(self, message: str | None = None, status_code: int | None = None, error_code: str | None = None, details: list[ErrorDetailDTO] | None = None, **kwargs)`: Initializes attributes.
    *   `NotFoundError(BaseAppException)`:
        *   `status_code: int = 404`
        *   `message: str = "Resource not found."`
        *   `error_code: str = "RESOURCE_NOT_FOUND"`
    *   `ValidationError(BaseAppException)`:
        *   `status_code: int = 422` (Unprocessable Entity, common for validation)
        *   `message: str = "Input validation failed."`
        *   `error_code: str = "VALIDATION_ERROR"`
    *   `AuthenticationError(BaseAppException)`:
        *   `status_code: int = 401`
        *   `message: str = "Authentication failed."`
        *   `error_code: str = "AUTHENTICATION_FAILURE"`
    *   `AuthorizationError(BaseAppException)`:
        *   `status_code: int = 403`
        *   `message: str = "Permission denied."`
        *   `error_code: str = "AUTHORIZATION_FAILURE"`
    *   `ConflictError(BaseAppException)`:
        *   `status_code: int = 409`
        *   `message: str = "Resource conflict."`
        *   `error_code: str = "CONFLICT_ERROR"`
    *   `UnprocessableEntityError(BaseAppException)`:
        *   `status_code: int = 422`
        *   `message: str = "Unprocessable entity."` # For business logic errors on valid data
        *   `error_code: str = "UNPROCESSABLE_ENTITY"`
    *   `ExternalServiceError(BaseAppException)`:
        *   `status_code: int = 502` (Bad Gateway, if we act as a proxy) or `503` (Service Unavailable)
        *   `message: str = "Error communicating with an external service."`
        *   `error_code: str = "EXTERNAL_SERVICE_ERROR"`
        *   `service_name: str | None = None`
    *   `RateLimitExceededError(BaseAppException)`:
        *   `status_code: int = 429`
        *   `message: str = "Rate limit exceeded."`
        *   `error_code: str = "RATE_LIMIT_EXCEEDED"`
        *   `retry_after: int | None = None` (Optional seconds to wait)
*   **Requirement Mapping:** NFR-009

#### 4.4.3 `creativeflow_shared.error_handling.error_reporter.py`
*   **Purpose:** Utilities for reporting exceptions to external services (e.g., Sentry).
*   **Functions:**
    *   `init_error_tracking(dsn: str, environment: str, release_version: str) -> None`:
        *   **Logic:** Initializes the Sentry SDK (or chosen error tracking SDK) with the provided DSN, environment, and release version. Sets global tags/context.
        *   **Example (Sentry):**
            python
            import sentry_sdk
            def init_error_tracking(dsn: str, environment: str, release_version: str):
                sentry_sdk.init(
                    dsn=dsn,
                    environment=environment,
                    release=release_version,
                    # traces_sample_rate=1.0 # if performance tracing is also used
                )
            
    *   `report_exception(exc: Exception, context: dict | None = None) -> None`:
        *   **Logic:** Captures and sends the given exception to the configured error tracking service. Adds any provided `context` (e.g., user_id, request_id) to the error report.
        *   **Example (Sentry):**
            python
            import sentry_sdk
            def report_exception(exc: Exception, context: dict | None = None):
                if context:
                    with sentry_sdk.push_scope() as scope:
                        for key, value in context.items():
                            scope.set_extra(key, value)
                        sentry_sdk.capture_exception(exc)
                else:
                    sentry_sdk.capture_exception(exc)
            

### 4.5 Submodule: `creativeflow_shared.i18n`

#### 4.5.1 `creativeflow_shared.i18n.__init__.py`
*   **Purpose:** Initializes the `i18n` submodule.
*   **Exported Symbols:**
    python
    from .formatting import (
        format_datetime_localized,
        format_number_localized,
        format_currency_localized
    )
    from .translation import get_translator, translate_message, init_translations

    __all__ = [
        "format_datetime_localized", "format_number_localized", "format_currency_localized",
        "get_translator", "translate_message", "init_translations"
    ]
    
*   **Requirement Mapping:** UI-006

#### 4.5.2 `creativeflow_shared.i18n.formatting.py`
*   **Purpose:** Locale-aware formatting of dates, times, numbers, currencies.
*   **Dependencies:** `babel`
*   **Functions:**
    *   `format_datetime_localized(dt: datetime.datetime, locale: str, format_name: str = 'medium') -> str`:
        *   **Logic:** Uses `babel.dates.format_datetime(dt, format=format_name, locale=locale)` to format. Handles potential errors if locale or format is invalid.
    *   `format_number_localized(number: int | float | decimal.Decimal, locale: str, pattern: str | None = None) -> str`:
        *   **Logic:** Uses `babel.numbers.format_decimal(number, format=pattern, locale=locale)`.
    *   `format_currency_localized(amount: decimal.Decimal, currency_code: str, locale: str) -> str`:
        *   **Logic:** Uses `babel.numbers.format_currency(amount, currency_code, locale=locale)`.
*   **Requirement Mapping:** UI-006

#### 4.5.3 `creativeflow_shared.i18n.translation.py`
*   **Purpose:** Message localization utilities.
*   **Dependencies:** Standard library `gettext`, `os`.
*   **Global Variables (internal):**
    *   `_translations: dict = {}` (To cache loaded translation objects)
    *   `_locale_dir: str | None = None`
*   **Functions:**
    *   `init_translations(locale_dir: str, domain: str = "messages") -> None`:
        *   **Logic:** Sets the global `_locale_dir`. Iterates through subdirectories in `locale_dir` (expected to be language codes like 'en_US', 'es_ES'). For each language, attempts to load translations using `gettext.translation(domain, localedir=locale_dir, languages=[lang_code])`. Caches the translation object in `_translations`.
        *   **Note:** Assumes standard `gettext` directory structure: `locale_dir/<lang_code>/LC_MESSAGES/<domain>.mo`.
    *   `get_translator(locale: str) -> Callable[[str], str]`:
        *   **Logic:** Retrieves the cached translation object for the given `locale` from `_translations`. Returns its `gettext` method (or `ugettext` for older Python versions if needed). If translations for the locale are not found, it could default to a null translator (returns the key itself) or raise an error, or fallback to a default language.
        *   **Fallback Strategy:** Implement a fallback (e.g., to 'en_US') if specific locale translations are missing.
    *   `translate_message(message_key: str, locale: str, **kwargs) -> str`:
        *   **Logic:** Uses `get_translator(locale)` to get the translation function. Calls it with `message_key`. If `kwargs` are provided, formats the translated string using `translated_string.format(**kwargs)` for placeholder replacement.
*   **Requirement Mapping:** UI-006

### 4.6 Submodule: `creativeflow_shared.logging`

#### 4.6.1 `creativeflow_shared.logging.__init__.py`
*   **Purpose:** Initializes the `logging` submodule.
*   **Exported Symbols:**
    python
    from .config import setup_logging, get_logger, add_correlation_id, get_correlation_id
    from .middleware import FastAPILoggingMiddleware # , FlaskLoggingMiddleware (if Flask is used)

    __all__ = [
        "setup_logging", "get_logger", "add_correlation_id", "get_correlation_id",
        "FastAPILoggingMiddleware" # , "FlaskLoggingMiddleware"
    ]
    
*   **Requirement Mapping:** DEP-005

#### 4.6.2 `creativeflow_shared.logging.config.py`
*   **Purpose:** Standardized JSON logging configuration using `python-json-logger`.
*   **Dependencies:** `logging`, `python_json_logger.core`, `python_json_logger.formatter`, `contextvars` (for correlation ID).
*   **Global Variables (internal):**
    *   `_correlation_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("correlation_id", default=None)`
*   **Functions:**
    *   `add_correlation_id(correlation_id: str) -> contextvars.Token`:
        *   **Logic:** Sets the `_correlation_id_var` for the current context. Returns the token to reset it later if needed.
    *   `get_correlation_id() -> str | None`:
        *   **Logic:** Returns the current value of `_correlation_id_var`.
    *   `setup_logging(service_name: str, log_level: str = 'INFO', environment: str = 'development') -> None`:
        *   **Logic:**
            *   Gets the root logger.
            *   Sets the overall log level (e.g., `logging.getLevelName(log_level.upper())`).
            *   Creates a `JsonFormatter` instance from `python_json_logger.formatter`.
            *   The formatter should include standard fields: `timestamp`, `levelname`, `message`, `module`, `funcName`, `lineno`.
            *   Custom fields to add: `service_name` (passed as arg), `environment` (passed as arg), `correlation_id` (retrieved using `get_correlation_id`).
            *   Example `JsonFormatter` format string: `"%(asctime)s %(levelname)s %(service_name)s %(environment)s %(module)s %(funcName)s %(lineno)d %(correlation_id)s %(message)s"` (Note: `asctime` and `levelname` are standard, others need to be added to record factory or via `rename_fields` if supported, or as extra).
            *   A better approach is to customize `python_json_logger.core.Json додатково`:
                python
                class CustomJsonFormatter(python_json_logger.formatter.JsonFormatter):
                    def add_fields(self, log_record, record, message_dict):
                        super().add_fields(log_record, record, message_dict)
                        log_record['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        log_record['level'] = record.levelname
                        log_record['service'] = service_name # From setup_logging closure
                        log_record['env'] = environment     # From setup_logging closure
                        log_record['correlation_id'] = get_correlation_id()
                        # Remove default fields if they are redundant
                        if 'asctime' in log_record: del log_record['asctime']
                        if 'levelname' in log_record: del log_record['levelname']

                formatter = CustomJsonFormatter()
                
            *   Creates a `logging.StreamHandler` (for console output, common in containerized environments).
            *   Sets the formatter on the handler.
            *   Adds the handler to the root logger.
            *   Disables propagation from other loggers if necessary, or configures specific loggers.
    *   `get_logger(name: str) -> logging.Logger`:
        *   **Logic:** Returns `logging.getLogger(name)`. Assumes `setup_logging` has been called.
*   **Requirement Mapping:** DEP-005

#### 4.6.3 `creativeflow_shared.logging.middleware.py`
*   **Purpose:** Optional logging middleware for web frameworks.
*   **Dependencies:** Framework-specific types (e.g., `starlette.types.ASGIApp` for FastAPI), `uuid`, `time`.
*   **Classes:**
    *   `FastAPILoggingMiddleware`: (Example for FastAPI)
        *   **`__init__(self, app: ASGIApp, logger: logging.Logger)`**
        *   **`async def __call__(self, scope: Scope, receive: Receive, send: Send)`:**
            *   **Logic:**
                *   If `scope["type"] == "http"`:
                    *   Extract or generate a correlation ID (e.g., from `REQUEST_ID_HEADER` or `uuid.uuid4()`).
                    *   Call `add_correlation_id()` with this ID.
                    *   Log incoming request details (method, path, client IP, relevant headers).
                    *   `start_time = time.perf_counter()`
                    *   Call `await self.app(scope, receive, send_wrapper)` (where `send_wrapper` captures response status).
                    *   `duration = time.perf_counter() - start_time`
                    *   Log outgoing response details (status code, duration).
                    *   Ensure correlation ID is cleared/reset if `add_correlation_id` returned a token.
                *   Else: `await self.app(scope, receive, send)`
*   **Requirement Mapping:** DEP-005

### 4.7 Submodule: `creativeflow_shared.security`

#### 4.7.1 `creativeflow_shared.security.__init__.py`
*   **Purpose:** Initializes the `security` submodule.
*   **Exported Symbols:**
    python
    from .sanitization import sanitize_html_input, encode_for_html_attribute, clean_filename # Added clean_filename
    from .validation import validate_request_payload, is_strong_password, is_valid_uuid # Added is_valid_uuid

    __all__ = [
        "sanitize_html_input", "encode_for_html_attribute", "clean_filename",
        "validate_request_payload", "is_strong_password", "is_valid_uuid"
    ]
    

#### 4.7.2 `creativeflow_shared.security.sanitization.py`
*   **Purpose:** Input sanitization and output encoding utilities.
*   **Dependencies:** `bleach`, `html` (standard library).
*   **Functions:**
    *   `sanitize_html_input(html_string: str, allowed_tags: list | None = None, allowed_attributes: dict | None = None, strip_comments: bool = True) -> str`:
        *   **Logic:** Uses `bleach.clean()` with sensible defaults for `allowed_tags` and `allowed_attributes` if not provided (e.g., very restrictive set for general input, more permissive for rich text editor content if that's a use case).
    *   `encode_for_html_attribute(text: str) -> str`:
        *   **Logic:** Uses `html.escape(text, quote=True)` to encode text for safe inclusion in HTML attributes.
    *   `clean_filename(filename: str) -> str`:
        *   **Logic:** Removes or replaces characters that are unsafe or problematic in filenames (e.g., `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, control characters). May also limit length and handle path traversal sequences like `../`.
*   **Requirement Mapping:** Implicitly NFR-008 (Security best practices).

#### 4.7.3 `creativeflow_shared.security.validation.py`
*   **Purpose:** Data validation and security-specific input checks.
*   **Dependencies:** `pydantic`, `re`, `uuid`.
*   **Functions:**
    *   `validate_request_payload(payload: dict, schema: type[pydantic.BaseModel]) -> pydantic.BaseModel`:
        *   **Logic:** Attempts to parse `payload` using `schema.model_validate(payload)`. If `pydantic.ValidationError` occurs, re-raises it as a shared `ValidationError` (from `creativeflow_shared.error_handling.exceptions`) potentially transforming Pydantic's error details into `ErrorDetailDTO` format.
    *   `is_strong_password(password: str, min_length: int = MIN_PASSWORD_LENGTH, require_uppercase: bool = True, require_lowercase: bool = True, require_digit: bool = True, require_special_char: bool = True) -> bool`:
        *   **Logic:** Checks if the password meets complexity criteria: min_length, presence of uppercase, lowercase, digit, and special character (configurable). Uses regex or character set checks.
    *   `is_valid_uuid(uuid_string: str) -> bool`:
        *   **Logic:** Attempts to create a `uuid.UUID` object from the string. Returns `True` if successful, `False` otherwise.
*   **Requirement Mapping:** Implicitly NFR-008.

### 4.8 Submodule: `creativeflow_shared.testing_utils`

#### 4.8.1 `creativeflow_shared.testing_utils.__init__.py`
*   **Purpose:** Initializes `testing_utils` submodule.
*   **Exported Symbols:**
    python
    from .fixtures import mock_db_session, sample_user_dto # Add more specific fixtures
    from .mocks import MockExternalServiceClient, patch_datetime_now, MockCacheClient # Added MockCacheClient
    from .assertions import assert_dtos_equal_ignoring_fields, assert_timestamp_approx_now, assert_api_error_response # Added assert_api_error

    __all__ = [
        "mock_db_session", "sample_user_dto",
        "MockExternalServiceClient", "patch_datetime_now", "MockCacheClient",
        "assert_dtos_equal_ignoring_fields", "assert_timestamp_approx_now", "assert_api_error_response"
    ]
    
*   **Requirement Mapping:** NFR-011

#### 4.8.2 `creativeflow_shared.testing_utils.fixtures.py`
*   **Purpose:** Reusable pytest fixtures.
*   **Dependencies:** `pytest`, `unittest.mock`, relevant DTOs from `.datamodels`.
*   **Fixtures (examples):**
    *   `@pytest.fixture\ndef mock_db_session() -> unittest.mock.MagicMock:`
        *   **Logic:** Returns a `MagicMock` instance, suitable for mocking a database session/connection.
    *   `@pytest.fixture\ndef sample_user_dto() -> UserContextDTO:`
        *   **Logic:** Returns a pre-populated `UserContextDTO` instance with default valid data.
    *   `@pytest.fixture\ndef test_correlation_id() -> str:`
        *   **Logic:** Generates and returns a unique correlation ID string for use in tests.
*   **Requirement Mapping:** NFR-011

#### 4.8.3 `creativeflow_shared.testing_utils.mocks.py`
*   **Purpose:** Reusable mock objects.
*   **Dependencies:** `unittest.mock`, `datetime`.
*   **Classes/Functions (examples):**
    *   `class MockExternalServiceClient:`
        *   **Logic:** A class that can be instantiated to mock an external service client. Methods return `MagicMock` or pre-configured responses.
    *   `class MockCacheClient:`
        *   **Logic:** A simple in-memory dictionary-based mock for a Redis-like cache client (get, set, delete methods).
    *   `@contextlib.contextmanager\ndef patch_datetime_now(fixed_datetime: datetime.datetime) -> Generator[None, None, None]:`
        *   **Logic:** Uses `unittest.mock.patch` to temporarily replace `datetime.datetime.now()` (and `.utcnow()`) to return `fixed_datetime`.
*   **Requirement Mapping:** NFR-011

#### 4.8.4 `creativeflow_shared.testing_utils.assertions.py`
*   **Purpose:** Custom assertion helpers.
*   **Dependencies:** Pydantic models, `datetime`.
*   **Functions (examples):**
    *   `assert_dtos_equal_ignoring_fields(dto1: pydantic.BaseModel, dto2: pydantic.BaseModel, ignore_fields: list[str]) -> None`:
        *   **Logic:** Compares two Pydantic models, excluding specified fields from comparison. Asserts that other fields are equal.
    *   `assert_timestamp_approx_now(timestamp: datetime.datetime, tolerance_seconds: int = 5) -> None`:
        *   **Logic:** Asserts that `timestamp` is within `tolerance_seconds` of `datetime.datetime.now(datetime.timezone.utc)`.
    *   `assert_api_error_response(response: Any, expected_status_code: int, expected_error_code: str | None = None, expected_message_contains: str | None = None) -> None`:
        *   **Logic:** Helper to assert common properties of an API error response (e.g., from FastAPI test client). Checks status code, and optionally `error_code` and if message contains a substring from the `ErrorResponseDTO`.
*   **Requirement Mapping:** NFR-011

### 4.9 Submodule: `creativeflow_shared.config_management`

#### 4.9.1 `creativeflow_shared.config_management.__init__.py`
*   **Purpose:** Initializes `config_management` submodule.
*   **Exported Symbols:**
    python
    from .loader import load_app_config
    from .schemas import (
        BaseConfigSchema,
        DatabaseConfigSchema,
        RedisConfigSchema,
        RabbitMQConfigSchema, # Added
        ServiceEndpointSchema,
        ThirdPartyServiceConfigSchema,
        LoggingConfigSchema, # Added
        SentryConfigSchema # Added for error reporting
    )

    __all__ = [
        "load_app_config",
        "BaseConfigSchema", "DatabaseConfigSchema", "RedisConfigSchema", "RabbitMQConfigSchema",
        "ServiceEndpointSchema", "ThirdPartyServiceConfigSchema", "LoggingConfigSchema", "SentryConfigSchema"
    ]
    

#### 4.9.2 `creativeflow_shared.config_management.loader.py`
*   **Purpose:** Utilities for loading and validating configurations.
*   **Dependencies:** `pydantic`, `os`, `dotenv` (optional, for .env file support).
*   **Functions:**
    *   `load_app_config(config_schema: type[pydantic.BaseModel], env_prefix: str = "APP_", dotenv_path: str | None = None) -> pydantic.BaseModel`:
        *   **Logic:**
            *   If `dotenv_path` is provided, loads environment variables from the `.env` file using `python-dotenv`.
            *   Collects environment variables starting with `env_prefix`.
            *   Maps these environment variables to the fields of `config_schema` (e.g., `APP_DATABASE_URL` maps to `database_url`). Handles nested models if Pydantic supports it via env var naming conventions (e.g., `APP_DATABASE__URL`).
            *   Instantiates `config_schema` with the loaded values, triggering Pydantic's validation.
            *   Raises `ValidationError` from `creativeflow_shared.error_handling` if validation fails.
            *   Returns the validated config object.

#### 4.9.3 `creativeflow_shared.config_management.schemas.py`
*   **Purpose:** Pydantic schemas for shared configuration structures.
*   **Dependencies:** `pydantic`.
*   **Models:**
    *   `class BaseConfigSchema(pydantic.BaseModel):`:
        *   `environment: str = "development"` (e.g., dev, staging, prod)
        *   `model_config = pydantic.ConfigDict(extra='ignore')`
    *   `class DatabaseConfigSchema(BaseConfigSchema):`:
        *   `url: pydantic.PostgresDsn`
        *   `pool_size: int = 5`
        *   `max_overflow: int = 10`
    *   `class RedisConfigSchema(BaseConfigSchema):`:
        *   `host: str`
        *   `port: int = 6379`
        *   `password: pydantic.SecretStr | None = None`
        *   `db: int = 0`
    *   `class RabbitMQConfigSchema(BaseConfigSchema):`:
        *   `url: pydantic.AmqpDsn` # e.g., amqp://user:pass@host:port/vhost
    *   `class ServiceEndpointSchema(pydantic.BaseModel):`:
        *   `url: pydantic.HttpUrl`
        *   `timeout_seconds: int = 30`
    *   `class ThirdPartyServiceConfigSchema(BaseConfigSchema):`:
        *   `api_key: pydantic.SecretStr`
        *   `base_url: pydantic.HttpUrl`
        *   `# other specific configs`
    *   `class LoggingConfigSchema(BaseConfigSchema):`
        *   `level: str = "INFO"`
        *   `service_name: str` # To be set by each service
    *   `class SentryConfigSchema(BaseConfigSchema):`
        *   `dsn: pydantic.HttpUrl | None = None`
        *   `release_version: str | None = None`

## 5. Node.js Shared Libraries (Conceptual)

While the detailed file structure focuses on Python, if Node.js services are part of the CreativeFlow AI backend, a parallel `creativeflow-shared-node` library would be beneficial. It would provide:

*   **Structured Logging:** Using libraries like Winston or Pino, configured for JSON output with correlation IDs.
*   **Error Handling:** A hierarchy of custom error classes (`BaseAppError`, `NotFoundError`, etc.) and integration with error reporting services (e.g., Sentry Node.js SDK).
*   **Data Validation/DTOs:** Using libraries like Zod, Joi, or class-validator for defining and validating data structures.
*   **Configuration Management:** Utilities to load configuration from environment variables or files, possibly using a schema validation library.
*   **Common Utilities:** Similar to the Python `core.utils`.
*   **I18n Utilities:** Using libraries like `i18next` for message translation and `Intl` (built-in) or `moment-timezone`/`date-fns-tz` for locale-aware formatting.
*   **Testing Utilities:** Shared mocks, fixtures, and helpers for Jest or Mocha.

The structure would likely mirror the Python library's modularity (e.g., `logging/`, `errors/`, `dtos/`, `utils/`).

## 6. Non-Functional Requirements Adherence

*   **NFR-008 (Code Quality):** Enforced by adherence to PEP 8/ESLint/Effective Dart, use of linters in CI, well-commented code, and static analysis. Constants are centralized.
*   **NFR-009 (Modularity):** Achieved through the modular structure of the shared library itself, and by providing well-defined DTOs and exception classes that act as clear interfaces between services.
*   **NFR-011 (Testability):** Supported by the `testing_utils` module, which provides shared fixtures, mocks, and assertion helpers to facilitate consistent and efficient testing across consuming services.
*   **DEP-005 (Standardized Log Format):** Directly implemented by `creativeflow_shared.logging.config` which mandates structured JSON logging with correlation IDs.
*   **UI-006 (Multilingual Support - Backend Aspects):** Supported by `creativeflow_shared.i18n` for message translation and locale-aware data formatting, ensuring backend services can provide localized data and messages.

This shared library forms a foundational layer for building robust, consistent, and maintainable microservices within the CreativeFlow AI platform.