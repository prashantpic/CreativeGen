# Software Design Specification: CreativeFlow.SharedLibraries.Common

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `CreativeFlow.SharedLibraries.Common` repository. This repository provides a collection of shared Python libraries and common utilities intended for use across multiple backend microservices within the CreativeFlow AI platform. The purpose of these shared libraries is to promote code reuse, consistency, adherence to non-functional requirements (NFRs) such as code quality and testability, and to provide standardized solutions for common cross-cutting concerns.

### 1.2 Scope
The scope of this document is limited to the design and implementation of the `CreativeFlow.SharedLibraries.Common` Python package. This includes modules for:
*   Standardized Logging
*   Security Helpers (Input Validation, Output Sanitization)
*   Internationalization (I18n) Utilities
*   Data Transfer Objects (DTOs)
*   Custom Exception Classes
*   General Utility Functions and Decorators
*   Shared Constants
*   Shared Testing Utilities

This document does not cover the design of the services that will consume these libraries, but rather focuses on the internal design of the shared library itself.

### 1.3 Overview of the Shared Library
The `CreativeFlow.SharedLibraries.Common` package is designed to be a foundational library providing robust, well-tested, and reusable components. By centralizing common functionalities, it aims to reduce code duplication, improve maintainability, and ensure a consistent approach to aspects like error handling, logging, and data contracts across the platform.

## 2. General Design Principles

The design and implementation of this shared library will adhere to the following principles:

*   **Code Quality (NFR-008):** All Python code will follow PEP 8 guidelines. Automated linting (e.g., Flake8, Pylint) and formatting (e.g., Black) tools will be used to ensure consistency.
*   **Modularity and Reusability (NFR-009):** The library will be organized into distinct modules with clear responsibilities. Functions and classes will be designed for maximum reusability across different services. Public interfaces will be well-defined.
*   **Testability (NFR-011):** All modules and functions will be designed with testability in mind. Dependencies will be injectable where appropriate, and comprehensive unit tests will be provided.
*   **Clarity and Simplicity:** Code will be written to be clear, understandable, and as simple as possible while meeting requirements. Complex logic will be well-commented.
*   **Dependency Minimization:** External dependencies will be kept to a minimum to reduce the library's footprint and potential for conflicts in consuming services. The specified third-party libraries (Pydantic, python-json-logger, bleach, babel) are core to the library's functionality.
*   **Type Hinting:** Python type hints will be used extensively to improve code clarity, enable static analysis, and enhance developer experience.

## 3. Module Specifications

The `CreativeFlow.SharedLibraries.Common` package will be structured as follows:

### 3.1 Project Configuration (`pyproject.toml`)

*   **File Path:** `pyproject.toml`
*   **Purpose:** Defines project metadata, dependencies, build system configuration (Poetry), and tool configurations for the shared library. (Requirement: NFR-008)
*   **Build System:** Poetry will be used as the build backend and dependency manager.
    toml
    [tool.poetry]
    name = "creativeflow-shared"
    version = "0.1.0"
    description = "Shared libraries for the CreativeFlow AI platform."
    authors = ["CreativeFlow AI Team <dev@creativeflow.ai>"]
    license = "Proprietary" # Or appropriate license
    readme = "README.md"
    packages = [{include = "creativeflow", from = "src"}]

    [tool.poetry.dependencies]
    python = "^3.11"
    pydantic = "^2.7.0" # For DTOs and validation
    python-json-logger = "^2.0.7" # For structured logging
    bleach = "^6.1.0" # For HTML sanitization
    babel = "^2.15.0" # For I18n formatting
    # Add other core dependencies if any

    [tool.poetry.group.dev.dependencies]
    pytest = "^8.0.0"
    pytest-cov = "^5.0.0"
    flake8 = "^7.0.0"
    pylint = "^3.0.0" # Or another linter like ruff
    black = "^24.0.0"
    mypy = "^1.0.0"
    # Add other development dependencies like types-* packages

    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"

    [tool.black]
    line-length = 88
    target-version = ['py311']

    [tool.pylint.'MESSAGES CONTROL']
    disable = "C0330, C0326, R0903, C0114, C0115, C0116" # Example disables

    [tool.pytest.ini_options]
    pythonpath = ["src"]
    testpaths = ["tests"]
    addopts = "--cov=src/creativeflow/shared --cov-report=term-missing --cov-report=xml"

    [tool.mypy]
    python_version = "3.11"
    warn_return_any = true
    warn_unused_configs = true
    ignore_missing_imports = true # Adjust based on project needs
    
*   **Dependencies:**
    *   `python = "^3.11"`
    *   `pydantic = "^2.7.0"`
    *   `python-json-logger = "^2.0.7"`
    *   `bleach = "^6.1.0"`
    *   `babel = "^2.15.0"`
*   **Development Dependencies:**
    *   `pytest`
    *   `pytest-cov`
    *   `flake8` (or `ruff`)
    *   `pylint` (or `ruff`)
    *   `black`
    *   `mypy`
*   **Tool Configuration:**
    *   `black`: For code formatting (e.g., line length 88).
    *   `flake8`/`pylint`: For linting, with appropriate rule configurations.
    *   `pytest`: Test path configurations, coverage reporting.
    *   `mypy`: Type checking configurations.

### 3.2 Main Package Initializer (`src/creativeflow/shared/__init__.py`)

*   **File Path:** `src/creativeflow/shared/__init__.py`
*   **Purpose:** Initializes the `creativeflow.shared` Python package and defines its public API by exporting selected members from submodules. (Requirement: NFR-009)
*   **Logic:**
    *   Import and re-export key classes and functions from submodules:
        python
        from .constants.general import (
            DEFAULT_REQUEST_TIMEOUT_SECONDS,
            MAX_USERNAME_LENGTH,
            # Add other general constants here
        )
        from .exceptions.base import BaseCreativeFlowError
        from .exceptions.domain_exceptions import (
            ValidationError,
            ResourceNotFoundError,
            AuthenticationError,
            AuthorizationError,
            BusinessRuleViolationError, # Added for completeness
        )
        from .exceptions.infra_exceptions import (
            ServiceUnavailableError,
            ConfigurationError,
            ExternalAPIFailureError,
            DatabaseConnectionError, # Added for completeness
        )
        from .dtos.base_dto import BaseDTO
        from .dtos.error_dto import ErrorResponseDTO
        from .dtos.pagination_dto import PaginatedResponseDTO
        from .logging.config import setup_logging
        from .logging.logger import get_logger
        from .security.validation import validate_payload, is_valid_email
        from .security.sanitization import sanitize_html_output
        from .i18n.formatters import (
            format_datetime_localized,
            format_number_localized,
            format_currency_localized,
        )
        from .i18n.utils import get_user_locale, get_timezone_aware_datetime
        from .utils.collections import chunk_list, deep_merge_dicts
        from .utils.decorators import timed, memoize

        __all__ = [
            # Constants
            "DEFAULT_REQUEST_TIMEOUT_SECONDS",
            "MAX_USERNAME_LENGTH",
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
            "sanitize_html_output",
            # I18n
            "format_datetime_localized",
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
        

### 3.3 Constants Module (`src/creativeflow/shared/constants/`)

#### 3.3.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/constants/__init__.py`
*   **Purpose:** Initializes the `constants` sub-package.
*   **Logic:**
    python
    from .general import (
        DEFAULT_REQUEST_TIMEOUT_SECONDS,
        MAX_USERNAME_LENGTH,
        # Add other general constants to export
    )
    # Example: If there were other constant files like 'api_keys.py'
    # from .api_keys import THIRD_PARTY_SERVICE_KEY_NAME

    __all__ = [
        "DEFAULT_REQUEST_TIMEOUT_SECONDS",
        "MAX_USERNAME_LENGTH",
        # "THIRD_PARTY_SERVICE_KEY_NAME",
    ]
    

#### 3.3.2 `general.py`

*   **File Path:** `src/creativeflow/shared/constants/general.py`
*   **Purpose:** Defines general, application-wide constants.
*   **Members:**
    *   `DEFAULT_REQUEST_TIMEOUT_SECONDS: int = 30`
    *   `MAX_USERNAME_LENGTH: int = 50`
    *   `MAX_FULL_NAME_LENGTH: int = 100`
    *   `EMAIL_REGEX: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"` (Example common regex)
    *   `UUID_REGEX: str = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"`
    *   Add other widely used constants as identified.

### 3.4 Exceptions Module (`src/creativeflow/shared/exceptions/`)

#### 3.4.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/exceptions/__init__.py`
*   **Purpose:** Initializes the `exceptions` sub-package.
*   **Logic:**
    python
    from .base import BaseCreativeFlowError
    from .domain_exceptions import (
        ValidationError,
        ResourceNotFoundError,
        AuthenticationError,
        AuthorizationError,
        BusinessRuleViolationError,
    )
    from .infra_exceptions import (
        ServiceUnavailableError,
        ConfigurationError,
        ExternalAPIFailureError,
        DatabaseConnectionError,
    )

    __all__ = [
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
    ]
    

#### 3.4.2 `base.py`

*   **File Path:** `src/creativeflow/shared/exceptions/base.py`
*   **Purpose:** Defines the base custom exception class.
*   **Class: `BaseCreativeFlowError(Exception)`**
    *   **Attributes:**
        *   `message: str` (inherited from `Exception`)
        *   `error_code: Optional[str]`
        *   `details: Optional[Any]` (to hold additional context)
    *   **Methods:**
        *   `__init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None)`:
            *   Calls `super().__init__(message)`.
            *   Sets `self.error_code = error_code`.
            *   Sets `self.details = details`.
        *   `__str__(self) -> str`:
            *   Returns a string representation including `message` and `error_code` if present.

#### 3.4.3 `domain_exceptions.py`

*   **File Path:** `src/creativeflow/shared/exceptions/domain_exceptions.py`
*   **Purpose:** Defines custom exceptions for business logic and domain rule violations. (Requirement: SEC-005 context)
*   **Classes (all inherit from `BaseCreativeFlowError`):**
    *   **`ValidationError(BaseCreativeFlowError)`**: For input data validation failures.
        *   `__init__(self, message: str = "Input validation failed", error_code: str = "VALIDATION_ERROR", details: Optional[Any] = None)`
    *   **`ResourceNotFoundError(BaseCreativeFlowError)`**: When a requested resource is not found.
        *   `__init__(self, resource_name: str, resource_id: Any, error_code: str = "RESOURCE_NOT_FOUND")`
        *   Stores `resource_name` and `resource_id` in `details`.
    *   **`AuthenticationError(BaseCreativeFlowError)`**: For failed authentication attempts.
        *   `__init__(self, message: str = "Authentication failed", error_code: str = "AUTHENTICATION_FAILURE")`
    *   **`AuthorizationError(BaseCreativeFlowError)`**: When an authenticated user lacks permission.
        *   `__init__(self, message: str = "Permission denied", error_code: str = "AUTHORIZATION_FAILURE")`
    *   **`BusinessRuleViolationError(BaseCreativeFlowError)`**: For violations of specific business rules.
        *   `__init__(self, message: str, error_code: str = "BUSINESS_RULE_VIOLATION", details: Optional[Any] = None)`

#### 3.4.4 `infra_exceptions.py`

*   **File Path:** `src/creativeflow/shared/exceptions/infra_exceptions.py`
*   **Purpose:** Defines custom exceptions for infrastructure or external service failures.
*   **Classes (all inherit from `BaseCreativeFlowError`):**
    *   **`ServiceUnavailableError(BaseCreativeFlowError)`**: When a dependent service is unavailable.
        *   `__init__(self, service_name: str, error_code: str = "SERVICE_UNAVAILABLE")`
        *   Stores `service_name` in `details`.
    *   **`ConfigurationError(BaseCreativeFlowError)`**: For errors related to system configuration.
        *   `__init__(self, message: str, error_code: str = "CONFIGURATION_ERROR")`
    *   **`ExternalAPIFailureError(BaseCreativeFlowError)`**: When an external API call fails.
        *   `__init__(self, service_name: str, original_error: Optional[Exception] = None, error_code: str = "EXTERNAL_API_FAILURE")`
        *   Stores `service_name` and potentially `original_error` details.
    *   **`DatabaseConnectionError(BaseCreativeFlowError)`**: For failures in connecting to the database.
        *   `__init__(self, message: str = "Database connection failed", error_code: str = "DB_CONNECTION_ERROR")`

### 3.5 Data Transfer Objects (DTOs) Module (`src/creativeflow/shared/dtos/`)

#### 3.5.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/dtos/__init__.py`
*   **Purpose:** Initializes the `dtos` sub-package.
*   **Logic:**
    python
    from .base_dto import BaseDTO
    from .error_dto import ErrorResponseDTO
    from .pagination_dto import PaginatedResponseDTO, T # Expose TypeVar T if needed

    __all__ = [
        "BaseDTO",
        "ErrorResponseDTO",
        "PaginatedResponseDTO",
        "T",
    ]
    

#### 3.5.2 `base_dto.py`

*   **File Path:** `src/creativeflow/shared/dtos/base_dto.py`
*   **Purpose:** Defines a base Pydantic model for all DTOs. (Requirement: NFR-009)
*   **Class: `BaseDTO(pydantic.BaseModel)`**
    *   **Pydantic Configuration (`model_config`):**
        python
        from pydantic import BaseModel, ConfigDict

        class BaseDTO(BaseModel):
            model_config = ConfigDict(
                from_attributes=True,  # was orm_mode
                populate_by_name=True, # was allow_population_by_field_name
                # Add other common configurations like alias generators if needed
                # e.g., alias_generator=to_camel_case
            )
        
    *   Optionally, include common helper methods if applicable (e.g., `to_dict_cleaned()`).

#### 3.5.3 `error_dto.py`

*   **File Path:** `src/creativeflow/shared/dtos/error_dto.py`
*   **Purpose:** Defines standardized DTOs for error responses. (Requirement: NFR-009)
*   **Class: `ErrorResponseDTO(BaseDTO)`**
    *   **Fields:**
        *   `error_code: str`
        *   `message: str`
        *   `details: Optional[Any] = None`
    *   Example usage for API responses:
        python
        # Example from pydantic import Field, Any
        # from typing import Optional
        # from .base_dto import BaseDTO

        # class ErrorDetail(BaseDTO):
        #     field: Optional[str] = None
        #     issue: str

        # class ErrorResponseDTO(BaseDTO):
        #     error_code: str = Field(..., description="A unique code for the error.")
        #     message: str = Field(..., description="A human-readable error message.")
        #     details: Optional[List[ErrorDetail]] = Field(None, description="Optional further details about the error, e.g., validation issues.")
        
        (Note: The `ErrorDetail` example adds more structure if needed for validation errors). For simplicity, using `Optional[Any]` as per file structure definition.

#### 3.5.4 `pagination_dto.py`

*   **File Path:** `src/creativeflow/shared/dtos/pagination_dto.py`
*   **Purpose:** Defines standardized DTOs for paginated list responses. (Requirement: NFR-009)
*   **Class: `PaginatedResponseDTO[T](BaseDTO, Generic[T])`**
    *   **Fields:**
        *   `items: List[T]`
        *   `total_items: int`
        *   `page: int` (current page number, 1-indexed)
        *   `page_size: int`
        *   `total_pages: int`
    *   **Logic:**
        python
        from typing import List, TypeVar, Generic, Optional
        from pydantic import Field
        from .base_dto import BaseDTO

        T = TypeVar('T')

        class PaginatedResponseDTO(BaseDTO, Generic[T]):
            items: List[T] = Field(..., description="List of items for the current page.")
            total_items: int = Field(..., ge=0, description="Total number of items available.")
            page: int = Field(..., gt=0, description="Current page number.")
            page_size: int = Field(..., gt=0, description="Number of items per page.")
            total_pages: int = Field(..., ge=0, description="Total number of pages.")
            # Optional next/prev links if needed
            # next_page_url: Optional[str] = None
            # prev_page_url: Optional[str] = None
        

### 3.6 Logging Module (`src/creativeflow/shared/logging/`)

#### 3.6.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/logging/__init__.py`
*   **Purpose:** Initializes the `logging` sub-package.
*   **Logic:**
    python
    from .config import setup_logging
    from .logger import get_logger

    __all__ = [
        "setup_logging",
        "get_logger",
    ]
    

#### 3.6.2 `config.py`

*   **File Path:** `src/creativeflow/shared/logging/config.py`
*   **Purpose:** Configures standardized JSON logging. (Requirement: DEP-005)
*   **Function: `setup_logging(log_level: str = 'INFO', service_name: Optional[str] = None, environment: Optional[str] = None) -> None`**
    *   **Parameters:**
        *   `log_level`: Logging level string (e.g., "DEBUG", "INFO", "WARNING", "ERROR"). Defaults to "INFO". Can be overridden by `LOG_LEVEL` environment variable.
        *   `service_name`: Name of the service using the logger. Can be overridden by `SERVICE_NAME` environment variable.
        *   `environment`: Deployment environment (e.g., "dev", "staging", "prod"). Can be overridden by `ENVIRONMENT` environment variable.
    *   **Logic:**
        1.  Determine effective log level from parameter or `os.getenv("LOG_LEVEL", log_level)`.
        2.  Determine effective service name from parameter or `os.getenv("SERVICE_NAME", service_name or "unknown_service")`.
        3.  Determine effective environment from parameter or `os.getenv("ENVIRONMENT", environment or "unknown_env")`.
        4.  Create a `python_json_logger.jsonlogger.JsonFormatter`.
            *   Define a format string or use `rename_fields` to include standard fields: `timestamp` (asctime), `levelname`, `message`, `name` (logger name), `funcName`, `lineno`.
            *   Add custom static fields: `service_name`, `environment`.
        5.  Get the root logger (`logging.getLogger()`).
        6.  Remove any existing handlers from the root logger to prevent duplicate logs if `setup_logging` is called multiple times (or use a flag to ensure it's run once).
        7.  Create a `logging.StreamHandler()` (for stdout).
        8.  Set the `JsonFormatter` on the handler.
        9.  Add the handler to the root logger.
        10. Set the root logger's level to the effective log level.
        11. Optionally, log a message indicating logging has been configured.
        python
        import logging
        import os
        from typing import Optional
        from python_json_logger import jsonlogger

        _logging_configured = False

        def setup_logging(
            log_level: str = "INFO",
            service_name: Optional[str] = None,
            environment: Optional[str] = None,
        ) -> None:
            """
            Configures structured JSON logging for the application.
            Can be called multiple times, but will only configure once.
            """
            global _logging_configured
            if _logging_configured:
                # logging.getLogger(__name__).debug("Logging already configured.")
                return

            effective_log_level_str = os.getenv("LOG_LEVEL", log_level).upper()
            effective_log_level = getattr(logging, effective_log_level_str, logging.INFO)

            effective_service_name = os.getenv(
                "SERVICE_NAME", service_name or "creativeflow-service"
            )
            effective_environment = os.getenv(
                "ENVIRONMENT", environment or "development"
            )

            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s",
                rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
                datefmt="%Y-%m-%dT%H:%M:%S.%fZ" # ISO 8601 format
            )
            
            # Add static fields to all log messages
            jsonlogger.BASIC_FIELDS.update({
                "service_name": effective_service_name,
                "environment": effective_environment,
            })
            # Or if you want them as part of the formatter's static fields directly
            # for handler in logging.root.handlers:
            #    if isinstance(handler.formatter, jsonlogger.JsonFormatter):
            #        handler.formatter.static_fields = {
            #            "service_name": effective_service_name,
            #            "environment": effective_environment,
            #        }


            log_handler = logging.StreamHandler() # Defaults to sys.stderr
            log_handler.setFormatter(formatter)

            root_logger = logging.getLogger()
            
            # Clear existing handlers to avoid duplicate logs if re-called
            if root_logger.hasHandlers():
                root_logger.handlers.clear()
                
            root_logger.addHandler(log_handler)
            root_logger.setLevel(effective_log_level)

            _logging_configured = True
            # logging.getLogger(__name__).info(
            #     f"Logging configured for service '{effective_service_name}' in '{effective_environment}' environment "
            #     f"at level '{effective_log_level_str}'."
            # )
        

#### 3.6.3 `logger.py`

*   **File Path:** `src/creativeflow/shared/logging/logger.py`
*   **Purpose:** Provides a utility to obtain a pre-configured logger. (Requirement: DEP-005)
*   **Function: `get_logger(name: str) -> logging.Logger`**
    *   **Parameters:**
        *   `name`: The name of the logger, typically `__name__` of the calling module.
    *   **Logic:**
        1.  Ensure `setup_logging()` from `config.py` has been called (can be done implicitly if `setup_logging` is called at application startup by services using this library, or add a check here as well for robustness, though `setup_logging` itself has a guard).
        2.  Return `logging.getLogger(name)`.
        python
        import logging
        # from .config import setup_logging # Call if not guaranteed to be called elsewhere

        def get_logger(name: str) -> logging.Logger:
            """
            Retrieves a logger instance with the specified name.
            Assumes setup_logging() has been called at application startup.
            """
            # Optionally, ensure setup_logging is called if it's not a firm guarantee
            # from .config import _logging_configured, setup_logging
            # if not _logging_configured:
            #     setup_logging() # Call with defaults or from env vars
            return logging.getLogger(name)
        

### 3.7 Security Module (`src/creativeflow/shared/security/`)

#### 3.7.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/security/__init__.py`
*   **Purpose:** Initializes the `security` sub-package.
*   **Logic:**
    python
    from .validation import validate_payload, is_valid_email, is_valid_uuid # Added is_valid_uuid
    from .sanitization import sanitize_html_output

    __all__ = [
        "validate_payload",
        "is_valid_email",
        "is_valid_uuid",
        "sanitize_html_output",
    ]
    

#### 3.7.2 `validation.py`

*   **File Path:** `src/creativeflow/shared/security/validation.py`
*   **Purpose:** Provides input validation utilities. (Requirement: SEC-005)
*   **Functions:**
    *   **`validate_payload(payload: Any, model_cls: Type[BaseDTO]) -> BaseDTO`**:
        *   **Parameters:**
            *   `payload`: The data to validate (e.g., a dictionary from a request).
            *   `model_cls`: The Pydantic model class to validate against.
        *   **Returns:** An instance of `model_cls` if validation succeeds.
        *   **Raises:** `ValidationError` (from `creativeflow.shared.exceptions`) if validation fails, including Pydantic's validation error details.
        *   **Logic:**
            python
            from typing import Type, Any
            from pydantic import ValidationError as PydanticValidationError
            from ..dtos.base_dto import BaseDTO # Relative import
            from ..exceptions.domain_exceptions import ValidationError # Relative import

            def validate_payload(payload: Any, model_cls: Type[BaseDTO]) -> BaseDTO:
                try:
                    return model_cls.model_validate(payload) # Pydantic v2
                except PydanticValidationError as e:
                    # Transform Pydantic's error into our custom ValidationError
                    # You might want to format e.errors() into a more structured detail
                    error_details = e.errors() 
                    raise ValidationError(
                        message="Payload validation failed.", 
                        details=error_details
                    ) from e
            
    *   **`is_valid_email(email_string: str) -> bool`**:
        *   **Logic:** Use a robust regex (e.g., from `creativeflow.shared.constants.general.EMAIL_REGEX`) or a dedicated email validation library if more complex validation (like MX record checks) are needed (though typically out of scope for a simple shared validator).
            python
            import re
            from ..constants.general import EMAIL_REGEX # Relative import

            def is_valid_email(email_string: str) -> bool:
                if not email_string or not isinstance(email_string, str):
                    return False
                return bool(re.fullmatch(EMAIL_REGEX, email_string))
            
    *   **`is_valid_uuid(uuid_string: str) -> bool`**:
        *   **Logic:** Use regex (e.g., from `creativeflow.shared.constants.general.UUID_REGEX`) or attempt to cast to `uuid.UUID`.
            python
            import re
            import uuid
            from ..constants.general import UUID_REGEX # Relative import

            def is_valid_uuid(uuid_string: str) -> bool:
                if not uuid_string or not isinstance(uuid_string, str):
                    return False
                # Regex check first for format
                if not re.fullmatch(UUID_REGEX, uuid_string):
                    return False
                # Then try to parse to ensure it's a valid UUID value (optional stricter check)
                try:
                    uuid.UUID(uuid_string)
                    return True
                except ValueError:
                    return False
            

#### 3.7.3 `sanitization.py`

*   **File Path:** `src/creativeflow/shared/security/sanitization.py`
*   **Purpose:** Provides output sanitization utilities. (Requirement: SEC-005)
*   **Function: `sanitize_html_output(html_string: str, allowed_tags: Optional[List[str]] = None, allowed_attributes: Optional[Dict[str, List[str]]] = None, strip_comments: bool = True) -> str`**
    *   **Parameters:**
        *   `html_string`: The HTML string to sanitize.
        *   `allowed_tags`: Optional list of allowed HTML tags. If None, use a safe default set.
        *   `allowed_attributes`: Optional dictionary of allowed attributes per tag. If None, use safe defaults.
        *   `strip_comments`: Whether to strip HTML comments. Defaults to True.
    *   **Logic:**
        1.  Define default safe allowed tags (e.g., `p, br, b, i, u, strong, em, a[href,title], ul, ol, li, blockquote, code, pre`).
        2.  Define default safe allowed attributes (e.g., `a: ['href', 'title']`).
        3.  Use `bleach.clean()` with the provided or default settings.
        python
        from typing import Optional, List, Dict
        import bleach

        DEFAULT_ALLOWED_TAGS = [
            "p", "br", "b", "i", "u", "strong", "em", "a", "ul", "ol", "li", 
            "blockquote", "code", "pre", "h1", "h2", "h3", "h4", "h5", "h6",
            "img", "span", "div" # Add more as needed, carefully
        ]

        DEFAULT_ALLOWED_ATTRIBUTES = {
            "a": ["href", "title", "target"],
            "img": ["src", "alt", "title", "width", "height"],
            "*": ["class", "id", "style"] # Be very careful with 'style'
        }
        # More restrictive style attribute values if 'style' is allowed:
        # DEFAULT_ALLOWED_STYLES = ['color', 'font-weight', 'text-align']

        def sanitize_html_output(
            html_string: str,
            custom_allowed_tags: Optional[List[str]] = None,
            custom_allowed_attributes: Optional[Dict[str, List[str]]] = None,
            # custom_allowed_styles: Optional[List[str]] = None, # If finer control over style needed
            strip_comments: bool = True,
        ) -> str:
            if not html_string or not isinstance(html_string, str):
                return ""

            tags_to_allow = custom_allowed_tags if custom_allowed_tags is not None else DEFAULT_ALLOWED_TAGS
            attrs_to_allow = custom_allowed_attributes if custom_allowed_attributes is not None else DEFAULT_ALLOWED_ATTRIBUTES
            # styles_to_allow = custom_allowed_styles if custom_allowed_styles is not None else DEFAULT_ALLOWED_STYLES
            
            return bleach.clean(
                html_string,
                tags=tags_to_allow,
                attributes=attrs_to_allow,
                # styles=styles_to_allow, # Only if style attribute is allowed and needs restriction
                strip=True, # Strips disallowed tags entirely
                strip_comments=strip_comments,
            )
        

### 3.8 Internationalization (I18n) Module (`src/creativeflow/shared/i18n/`)

#### 3.8.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/i18n/__init__.py`
*   **Purpose:** Initializes the `i18n` sub-package.
*   **Logic:**
    python
    from .formatters import (
        format_datetime_localized,
        format_number_localized,
        format_currency_localized,
    )
    from .utils import get_user_locale, get_timezone_aware_datetime

    __all__ = [
        "format_datetime_localized",
        "format_number_localized",
        "format_currency_localized",
        "get_user_locale",
        "get_timezone_aware_datetime",
    ]
    

#### 3.8.2 `formatters.py`

*   **File Path:** `src/creativeflow/shared/i18n/formatters.py`
*   **Purpose:** Provides locale-aware formatting functions using Babel. (Requirement: UI-006)
*   **Functions (using `babel`):**
    *   **`format_datetime_localized(dt: datetime, locale_identifier: str, format_type: str = 'medium', timezone: Optional[str] = None) -> str`**:
        *   Converts `dt` to the specified `timezone` if provided, then formats.
        *   Uses `babel.dates.format_datetime(dt, format=format_type, locale=locale_identifier, tzinfo=pytz.timezone(timezone) if timezone else None)`.
    *   **`format_date_localized(d: date, locale_identifier: str, format_type: str = 'medium') -> str`**:
        *   Uses `babel.dates.format_date(d, format=format_type, locale=locale_identifier)`.
    *   **`format_time_localized(t: time, locale_identifier: str, format_type: str = 'medium', timezone: Optional[str] = None) -> str`**:
        *   Uses `babel.dates.format_time(t, format=format_type, locale=locale_identifier, tzinfo=pytz.timezone(timezone) if timezone else None)`.
    *   **`format_number_localized(number: Union[int, float, Decimal], locale_identifier: str) -> str`**:
        *   Uses `babel.numbers.format_decimal(Decimal(str(number)), locale=locale_identifier)`. Ensures input is Decimal for consistent formatting.
    *   **`format_currency_localized(amount: Union[int, float, Decimal], currency_code: str, locale_identifier: str) -> str`**:
        *   Uses `babel.numbers.format_currency(Decimal(str(amount)), currency_code, locale=locale_identifier)`.
    python
    from datetime import datetime, date, time
    from decimal import Decimal
    from typing import Union, Optional
    import babel.dates
    import babel.numbers
    import pytz # For timezone handling with Babel if dt is naive

    # Helper to ensure datetime is timezone-aware if tz is provided
    def _make_aware_if_needed(dt_obj: Union[datetime, time], timezone_str: Optional[str]) -> Union[datetime, time]:
        if timezone_str:
            tz = pytz.timezone(timezone_str)
            if isinstance(dt_obj, datetime) and dt_obj.tzinfo is None:
                return tz.localize(dt_obj)
            elif isinstance(dt_obj, datetime) and dt_obj.tzinfo is not None:
                 return dt_obj.astimezone(tz) # Convert to target timezone
            # For time objects, Babel handles tzinfo directly if passed
        return dt_obj


    def format_datetime_localized(
        dt: datetime,
        locale_identifier: str,
        format_type: str = "medium",
        timezone: Optional[str] = None,
    ) -> str:
        aware_dt = _make_aware_if_needed(dt, timezone)
        tz_info_for_babel = pytz.timezone(timezone) if timezone else None
        if isinstance(aware_dt, datetime) and aware_dt.tzinfo is None and tz_info_for_babel:
             # If still naive but timezone was given, make it aware for Babel
             aware_dt = tz_info_for_babel.localize(aware_dt)

        return babel.dates.format_datetime(
            aware_dt, format=format_type, locale=locale_identifier, tzinfo=tz_info_for_babel if isinstance(aware_dt, datetime) else None
        )

    def format_date_localized(
        d: date, locale_identifier: str, format_type: str = "medium"
    ) -> str:
        return babel.dates.format_date(d, format=format_type, locale=locale_identifier)

    def format_time_localized(
        t: time,
        locale_identifier: str,
        format_type: str = "medium",
        timezone: Optional[str] = None,
    ) -> str:
        tz_info_for_babel = pytz.timezone(timezone) if timezone else None
        return babel.dates.format_time(t, format=format_type, locale=locale_identifier, tzinfo=tz_info_for_babel)


    def format_number_localized(
        number: Union[int, float, Decimal], locale_identifier: str
    ) -> str:
        # Ensure number is Decimal for consistent formatting by Babel
        if not isinstance(number, Decimal):
            number = Decimal(str(number))
        return babel.numbers.format_decimal(number, locale=locale_identifier)


    def format_currency_localized(
        amount: Union[int, float, Decimal], currency_code: str, locale_identifier: str
    ) -> str:
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        return babel.numbers.format_currency(
            amount, currency_code, locale=locale_identifier
        )
    

#### 3.8.3 `utils.py`

*   **File Path:** `src/creativeflow/shared/i18n/utils.py`
*   **Purpose:** I18n utility functions. (Requirement: UI-006)
*   **Functions:**
    *   **`get_user_locale(user_preference: Optional[str], request_headers: Optional[dict], supported_locales: List[str], default_locale: str = 'en_US') -> str`**:
        *   **Logic:**
            1.  If `user_preference` is provided and is in `supported_locales`, return it.
            2.  If `request_headers` contains 'Accept-Language', parse it (using `babel.negotiate_locale` or simple parsing) to find the best match in `supported_locales`.
            3.  Return `default_locale` if no match is found.
    *   **`get_timezone_aware_datetime(dt: datetime, target_timezone_str: str, source_timezone_str: Optional[str] = None) -> datetime`**:
        *   **Logic:** Use `pytz` or Python 3.9+ `zoneinfo`. If `dt` is naive and `source_timezone_str` is provided, localize it. Then convert to `target_timezone_str`. If `dt` is already aware, convert it directly.
    python
    from typing import Optional, Dict, List
    from datetime import datetime
    import pytz # Or from zoneinfo import ZoneInfo for Python 3.9+
    from babel import Locale, negotiate_locale

    DEFAULT_SUPPORTED_LOCALES = ['en_US', 'en_GB', 'es_ES', 'es_MX', 'fr_FR', 'de_DE']
    DEFAULT_LOCALE = 'en_US'

    def get_user_locale(
        user_preference: Optional[str] = None,
        accept_language_header: Optional[str] = None,
        supported_locales: List[str] = DEFAULT_SUPPORTED_LOCALES,
        default_locale: str = DEFAULT_LOCALE,
    ) -> str:
        """
        Determines the best locale to use based on user preference,
        Accept-Language header, supported locales, and a default.
        """
        if user_preference and user_preference in supported_locales:
            return user_preference
        
        if accept_language_header:
            # Babel's negotiate_locale is robust for this
            preferred_locales = [str(Locale.parse(lang.split(';')[0].strip())) for lang in accept_language_header.split(',')]
            negotiated = negotiate_locale(preferred_locales, supported_locales)
            if negotiated:
                return negotiated
        
        return default_locale

    def get_timezone_aware_datetime(
        dt_object: datetime,
        target_timezone_str: str,
        source_timezone_str: Optional[str] = None,
    ) -> datetime:
        """
        Converts a datetime object to a target timezone.
        If dt_object is naive and source_timezone_str is provided, it's localized first.
        If dt_object is naive and no source_timezone_str, it's assumed to be UTC.
        """
        target_tz = pytz.timezone(target_timezone_str)

        if dt_object.tzinfo is None: # Naive datetime
            if source_timezone_str:
                source_tz = pytz.timezone(source_timezone_str)
                dt_object = source_tz.localize(dt_object)
            else: # Assume UTC if naive and no source timezone
                dt_object = pytz.utc.localize(dt_object)
        
        return dt_object.astimezone(target_tz)
    

### 3.9 General Utilities Module (`src/creativeflow/shared/utils/`)

#### 3.9.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/utils/__init__.py`
*   **Purpose:** Initializes the `utils` sub-package.
*   **Logic:**
    python
    from .collections import chunk_list, deep_merge_dicts
    from .decorators import timed, memoize
    # Add other utility modules if created, e.g., from .string_utils import ...

    __all__ = [
        "chunk_list",
        "deep_merge_dicts",
        "timed",
        "memoize",
    ]
    

#### 3.9.2 `collections.py`

*   **File Path:** `src/creativeflow/shared/utils/collections.py`
*   **Purpose:** Common utility functions for Python collections.
*   **Functions:**
    *   **`chunk_list(data: List[Any], size: int) -> Generator[List[Any], None, None]`**:
        *   **Logic:** Yield successive `size`-sized chunks from `data`.
    *   **`deep_merge_dicts(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]`**:
        *   **Logic:** Recursively merges `dict2` into `dict1`. For conflicting keys, if both values are dictionaries, merges them recursively. Otherwise, `dict2`'s value overwrites `dict1`'s. Returns a new dictionary.
    python
    from typing import List, Dict, Any, Generator, TypeVar
    import collections.abc

    T_co = TypeVar('T_co', covariant=True)

    def chunk_list(data: List[T_co], size: int) -> Generator[List[T_co], None, None]:
        """Yield successive n-sized chunks from list."""
        if size <= 0:
            raise ValueError("Chunk size must be positive.")
        for i in range(0, len(data), size):
            yield data[i : i + size]

    def deep_merge_dicts(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Recursively merges dict2 into dict1.
        If keys conflict and both values are dicts, they are merged.
        Otherwise, dict2's value overwrites dict1's.
        Returns a new dictionary, dict1 and dict2 are not modified.
        """
        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged:
                if isinstance(merged[key], dict) and isinstance(value, collections.abc.Mapping):
                    merged[key] = deep_merge_dicts(merged[key], value)
                else:
                    merged[key] = value
            else:
                merged[key] = value
        return merged
    

#### 3.9.3 `decorators.py`

*   **File Path:** `src/creativeflow/shared/utils/decorators.py`
*   **Purpose:** Common, reusable decorators.
*   **Decorators:**
    *   **`@timed(logger: Optional[logging.Logger] = None)`**:
        *   **Logic:** A decorator that measures the execution time of a function. If a logger is provided, it logs the function name and execution time.
    *   **`@memoize(maxsize: int = 128)`**:
        *   **Logic:** A simple memoization decorator using `functools.lru_cache` or a custom dictionary-based cache to store results of function calls based on arguments.
    python
    import time
    import functools
    import logging
    from typing import Callable, Any, Optional

    def timed(logger: Optional[logging.Logger] = None) -> Callable:
        """
        Decorator that logs the execution time of the wrapped function.
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                elapsed_time_ms = (end_time - start_time) * 1000
                
                log_target = logger if logger else logging.getLogger(func.__module__)
                log_target.debug(
                    f"Function '{func.__name__}' executed in {elapsed_time_ms:.4f} ms"
                )
                return result
            return wrapper
        return decorator

    def memoize(maxsize: int = 128, typed: bool = False) -> Callable:
        """
        Simple memoization decorator using functools.lru_cache.
        """
        def decorator(func: Callable) -> Callable:
            return functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        return decorator
    

### 3.10 Shared Testing Utilities (`src/creativeflow/shared/testing/`)

#### 3.10.1 `__init__.py`

*   **File Path:** `src/creativeflow/shared/testing/__init__.py`
*   **Purpose:** Initializes the `testing` sub-package. (Requirement: NFR-011)
*   **Logic:**
    python
    from .mocks import create_mock_error_response_dto, create_mock_paginated_response_dto
    # from .fixtures import mock_config_fixture (if defined)
    # Add other mock/fixture exports

    __all__ = [
        "create_mock_error_response_dto",
        "create_mock_paginated_response_dto",
        # "mock_config_fixture",
    ]
    

#### 3.10.2 `mocks.py`

*   **File Path:** `src/creativeflow/shared/testing/mocks.py`
*   **Purpose:** Contains common mock objects and test data factories. (Requirement: NFR-011)
*   **Factory Functions:**
    *   `create_mock_error_response_dto(error_code: str = "TEST_ERROR", message: str = "A test error occurred.", details: Optional[Any] = None) -> ErrorResponseDTO`: Creates an `ErrorResponseDTO` instance.
    *   `create_mock_paginated_response_dto(items: List[T], total_items: Optional[int] = None, page: int = 1, page_size: int = 10) -> PaginatedResponseDTO[T]`: Creates a `PaginatedResponseDTO` instance. Calculates `total_pages` if `total_items` is provided.
    python
    from typing import List, Optional, Any, TypeVar
    from ..dtos.error_dto import ErrorResponseDTO
    from ..dtos.pagination_dto import PaginatedResponseDTO

    T = TypeVar('T')

    def create_mock_error_response_dto(
        error_code: str = "TEST_ERROR",
        message: str = "A test error occurred.",
        details: Optional[Any] = None
    ) -> ErrorResponseDTO:
        return ErrorResponseDTO(error_code=error_code, message=message, details=details)

    def create_mock_paginated_response_dto(
        items: List[T],
        total_items: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> PaginatedResponseDTO[T]:
        if total_items is None:
            total_items = len(items)
        
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
        if total_items == 0 : # handles case of 0 items
             total_pages = 0
             page = 0 # if page is 1 and total_items is 0, page should be 0

        return PaginatedResponseDTO(
            items=items,
            total_items=total_items,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    

#### 3.10.3 `fixtures.py`

*   **File Path:** `src/creativeflow/shared/testing/fixtures.py`
*   **Purpose:** Contains shared PyTest fixtures. (Requirement: NFR-011)
*   **Example Fixture:**
    *   **`@pytest.fixture def mock_shared_logger() -> MagicMock`**:
        *   **Logic:** Returns a `unittest.mock.MagicMock` instance that can be used to patch `get_logger` or a logger instance in tests to assert logging calls.
    python
    import pytest
    from unittest.mock import MagicMock
    import logging

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

    # Example fixture to ensure logging is setup for tests that might use it
    @pytest.fixture(scope="session", autouse=True)
    def ensure_logging_configured_for_tests():
        from ..logging.config import setup_logging, _logging_configured
        if not _logging_configured:
            setup_logging(log_level="DEBUG", service_name="pytest-shared-lib")
    

## 4. Error Handling Strategy

*   **Custom Exceptions:** Services consuming this library should catch specific exceptions defined in `creativeflow.shared.exceptions` (e.g., `ValidationError`, `ResourceNotFoundError`) to handle errors appropriately.
*   **Standardized Error DTOs:** When services build API responses for errors, they should utilize `ErrorResponseDTO` from `creativeflow.shared.dtos` to ensure a consistent error structure across the platform, if this library's DTOs are adopted for external API contracts.
*   **Logging:** All exceptions should be logged with sufficient context using the standardized logging mechanism provided by `creativeflow.shared.logging`.

## 5. Testing Strategy

*   **Unit Tests:** Each module and utility function within this shared library will be accompanied by comprehensive unit tests using `pytest`.
*   **Coverage:** Aim for high code coverage (target >= 90% for most modules, especially critical ones like security, logging, DTOs).
*   **Shared Utilities:** The `creativeflow.shared.testing` submodule will provide mocks and fixtures to aid in testing this library itself and to be potentially reused by services that consume this library for mocking shared components.
*   **CI Integration:** All tests will be executed automatically as part of the CI/CD pipeline.

## 6. Integration with Other Services

*   **Import and Usage:** Backend microservices (primarily Python-based) will include `creativeflow-shared` as a dependency in their `pyproject.toml` (or `requirements.txt`). They can then import and use the exposed classes and functions.
    python
    # Example in a consuming service:
    from creativeflow.shared import get_logger, ValidationError, validate_payload, UserRequestDTO # Assuming UserRequestDTO is defined in shared DTOs or consuming service
    
    logger = get_logger(__name__)
    
    def process_user_request(data: dict):
        try:
            validated_data: UserRequestDTO = validate_payload(data, UserRequestDTO)
            logger.info(f"Processing request for user: {validated_data.user_id}")
            # ... business logic ...
        except ValidationError as e:
            logger.error(f"Validation failed: {e.details}")
            raise # Or handle specific to service
        except Exception as e:
            logger.exception("An unexpected error occurred.") # Logs with stack trace
            raise
    
*   **Versioning:** The shared library will follow semantic versioning (SemVer). Consuming services should pin to compatible versions to avoid unexpected breaking changes.

## 7. Future Considerations (Out of Scope for Initial Implementation but relevant to design)
*   **Async Support:** While current utilities are synchronous, future needs might require async versions of some utilities (e.g., for I/O bound operations). The design should not preclude adding `async` counterparts later.
*   **Configuration Management Utilities:** Helpers for loading and validating service configurations could be added if a common pattern emerges.
*   **More Sophisticated Decorators:** For aspects like circuit breaking (if generic enough) or more advanced caching strategies.

This SDS provides a detailed plan for the `CreativeFlow.SharedLibraries.Common` repository, ensuring it meets the specified requirements and serves as a robust foundation for other backend services.