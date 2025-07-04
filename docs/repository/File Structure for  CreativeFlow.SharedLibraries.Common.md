# Specification

# 1. Files

- **Path:** pyproject.toml  
**Description:** Defines project metadata, dependencies, build system configuration (PEP 517/518), and tool configurations (e.g., linters, formatters) for the CreativeFlow.SharedLibraries.Common package. Specifies Python version, Pydantic, python-json-logger, bleach, babel as dependencies.  
**Template:** TOML Configuration File  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** ConfigurationFile  
**Relative Path:** ../../pyproject.toml  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Definition
    - Dependency Management
    - Build Configuration
    - Tool Configuration
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** Standard Python project definition file managing build, dependencies, and tool settings for the shared library.  
**Logic Description:** Configures the project using Poetry or Hatch as the build backend. Lists runtime dependencies like pydantic, python-json-logger, bleach, babel. Configures tools like black for formatting, pylint/flake8 for linting, and pytest for testing (though test execution setup is out of scope for this file generation).  
**Documentation:**
    
    - **Summary:** Core project configuration file for the shared Python libraries. Defines how the package is built, its dependencies, and development tool settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** src/creativeflow/shared/__init__.py  
**Description:** Main package initializer for the creativeflow.shared library. Exports key modules, classes, and functions to provide a clean public API for consumers of this shared library. Manages the public interface of the library.  
**Template:** Python Package Initializer  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Public API Definition
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Makes the 'creativeflow.shared' directory a Python package and controls what is exposed when the package is imported.  
**Logic Description:** Imports and re-exports selected classes, functions, or submodules from .logging, .security, .i18n, .dtos, .exceptions, .utils, and .constants to create a convenient and controlled public API for the library. For example 'from .logging import get_logger'.  
**Documentation:**
    
    - **Summary:** Initializes the creativeflow.shared Python package and exposes its public interface.
    
**Namespace:** creativeflow.shared  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/shared/constants/__init__.py  
**Description:** Initializer for the constants module. Exports constants defined within this module.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** constants/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Constants Export
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'constants' directory a Python sub-package and exports its contents.  
**Logic Description:** Imports specific constants or all constants from modules within the 'constants' directory (e.g., from .general import ...).  
**Documentation:**
    
    - **Summary:** Initializes the constants sub-package and makes its defined constants available.
    
**Namespace:** creativeflow.shared.constants  
**Metadata:**
    
    - **Category:** Utilities
    
- **Path:** src/creativeflow/shared/constants/general.py  
**Description:** Defines general, application-wide constants used across multiple services. This could include default timeouts, common keys, or status codes if not specific to a single domain.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** general  
**Type:** Module  
**Relative Path:** constants/general.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DEFAULT_REQUEST_TIMEOUT_SECONDS  
**Type:** int  
**Attributes:** public|final  
    - **Name:** MAX_USERNAME_LENGTH  
**Type:** int  
**Attributes:** public|final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Constant Definitions
    
**Requirement Ids:**
    
    
**Purpose:** Provides a centralized location for widely used, immutable values within the CreativeFlow AI platform.  
**Logic Description:** Contains simple assignments of constant values. These are typically uppercase variables. Example: DEFAULT_REQUEST_TIMEOUT_SECONDS = 30.  
**Documentation:**
    
    - **Summary:** Defines general constants for use across the CreativeFlow AI platform.
    
**Namespace:** creativeflow.shared.constants  
**Metadata:**
    
    - **Category:** Utilities
    
- **Path:** src/creativeflow/shared/exceptions/__init__.py  
**Description:** Initializer for the exceptions module. Exports custom exception classes.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** exceptions/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Exception Export
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'exceptions' directory a Python sub-package and exports custom exception classes.  
**Logic Description:** Imports and re-exports exception classes from .base, .domain_exceptions, .infra_exceptions. Example: from .base import BaseCreativeFlowError; from .domain_exceptions import ValidationError.  
**Documentation:**
    
    - **Summary:** Initializes the exceptions sub-package and provides access to custom exception types.
    
**Namespace:** creativeflow.shared.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** src/creativeflow/shared/exceptions/base.py  
**Description:** Defines a base custom exception class for all CreativeFlow AI platform-specific exceptions. Allows for common handling and identification of application errors.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** base  
**Type:** Module  
**Relative Path:** exceptions/base.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** error_code  
**Type:** Optional[str]  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - message: str
    - error_code: Optional[str] = None
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Base Custom Exception
    
**Requirement Ids:**
    
    
**Purpose:** Provides a common ancestor for all custom exceptions, facilitating centralized error handling strategies.  
**Logic Description:** Defines a class 'BaseCreativeFlowError' inheriting from Python's built-in 'Exception'. It can include common attributes like an optional error code or context information.  
**Documentation:**
    
    - **Summary:** Base exception class for the CreativeFlow AI application.
    
**Namespace:** creativeflow.shared.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** src/creativeflow/shared/exceptions/domain_exceptions.py  
**Description:** Defines custom exceptions related to business logic and domain rule violations. Examples: ValidationError, ResourceNotFoundError, BusinessRuleViolationError.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** domain_exceptions  
**Type:** Module  
**Relative Path:** exceptions/domain_exceptions.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Domain-Specific Exceptions
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Provides specific exception types for domain-level errors, enhancing error clarity and handling.  
**Logic Description:** Defines classes like 'ValidationError', 'ResourceNotFoundError', 'AuthenticationError', 'AuthorizationError', each inheriting from 'BaseCreativeFlowError'. These may carry specific context related to the domain error.  
**Documentation:**
    
    - **Summary:** Custom exceptions for business logic and domain rule violations.
    
**Namespace:** creativeflow.shared.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** src/creativeflow/shared/exceptions/infra_exceptions.py  
**Description:** Defines custom exceptions related to infrastructure issues or external service failures. Examples: ServiceUnavailableError, ConfigurationError, DatabaseConnectionError.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** infra_exceptions  
**Type:** Module  
**Relative Path:** exceptions/infra_exceptions.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Infrastructure-Related Exceptions
    
**Requirement Ids:**
    
    
**Purpose:** Provides specific exception types for infrastructure or external dependency failures.  
**Logic Description:** Defines classes like 'ServiceUnavailableError', 'ConfigurationError', 'ExternalAPIFailureError', each inheriting from 'BaseCreativeFlowError'. These help in distinguishing operational issues from domain logic errors.  
**Documentation:**
    
    - **Summary:** Custom exceptions for infrastructure and external service interaction problems.
    
**Namespace:** creativeflow.shared.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** src/creativeflow/shared/dtos/__init__.py  
**Description:** Initializer for the DTOs (Data Transfer Objects) module. Exports shared DTO classes.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** dtos/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DTO Export
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Makes the 'dtos' directory a Python sub-package and exports its Pydantic models.  
**Logic Description:** Imports and re-exports DTO classes from .base_dto, .error_dto, .pagination_dto, and any other shared DTO modules. Example: from .base_dto import BaseDTO.  
**Documentation:**
    
    - **Summary:** Initializes the DTOs sub-package, providing standardized data structures for inter-service communication and API contracts.
    
**Namespace:** creativeflow.shared.dtos  
**Metadata:**
    
    - **Category:** DataContracts
    
- **Path:** src/creativeflow/shared/dtos/base_dto.py  
**Description:** Defines a base Pydantic model for all Data Transfer Objects (DTOs). Includes common configurations like ORM mode, alias generation, or custom validation settings.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** base_dto  
**Type:** Module  
**Relative Path:** dtos/base_dto.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base DTO Model
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Provides a common base class for all DTOs, ensuring consistency and reusability of Pydantic configurations.  
**Logic Description:** Defines a class 'BaseDTO' inheriting from 'pydantic.BaseModel'. Common Pydantic 'Config' class settings (e.g., 'orm_mode = True', 'allow_population_by_field_name = True') are defined here.  
**Documentation:**
    
    - **Summary:** Base Pydantic model for shared Data Transfer Objects, enforcing common settings.
    
**Namespace:** creativeflow.shared.dtos  
**Metadata:**
    
    - **Category:** DataContracts
    
- **Path:** src/creativeflow/shared/dtos/error_dto.py  
**Description:** Defines standardized DTOs for error responses across services. Includes fields for error code, message, and optional details.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** error_dto  
**Type:** Module  
**Relative Path:** dtos/error_dto.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** error_code  
**Type:** str  
**Attributes:** public  
    - **Name:** message  
**Type:** str  
**Attributes:** public  
    - **Name:** details  
**Type:** Optional[Any]  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Standard Error Response DTO
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Ensures consistent error response structures from APIs and services.  
**Logic Description:** Defines a Pydantic model class 'ErrorResponseDTO' inheriting from 'BaseDTO'. It includes fields like 'error_code', 'message', and 'details' to structure error information.  
**Documentation:**
    
    - **Summary:** Data Transfer Object for standardized error responses.
    
**Namespace:** creativeflow.shared.dtos  
**Metadata:**
    
    - **Category:** DataContracts
    
- **Path:** src/creativeflow/shared/dtos/pagination_dto.py  
**Description:** Defines standardized DTOs for paginated list responses. Includes fields for items, total count, page number, page size, and next/previous links if applicable.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** pagination_dto  
**Type:** Module  
**Relative Path:** dtos/pagination_dto.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** items  
**Type:** List[T]  
**Attributes:** public  
    - **Name:** total_items  
**Type:** int  
**Attributes:** public  
    - **Name:** page  
**Type:** int  
**Attributes:** public  
    - **Name:** page_size  
**Type:** int  
**Attributes:** public  
    - **Name:** total_pages  
**Type:** int  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Paginated Response DTO
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Provides a consistent structure for API responses that return lists of resources.  
**Logic Description:** Defines a generic Pydantic model class 'PaginatedResponseDTO[T]' inheriting from 'BaseDTO', where T is a type variable. It includes fields like 'items', 'total_items', 'page', 'page_size', 'total_pages'.  
**Documentation:**
    
    - **Summary:** Data Transfer Object for representing paginated API responses.
    
**Namespace:** creativeflow.shared.dtos  
**Metadata:**
    
    - **Category:** DataContracts
    
- **Path:** src/creativeflow/shared/logging/__init__.py  
**Description:** Initializer for the logging module. Exports logging configuration functions and logger retrieval utilities.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** logging/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Logging Utilities Export
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Makes the 'logging' directory a Python sub-package and exports its main functionalities.  
**Logic Description:** Imports and re-exports functions like 'setup_logging' from .config and 'get_logger' from .logger. Example: from .config import setup_logging; from .logger import get_logger.  
**Documentation:**
    
    - **Summary:** Initializes the logging sub-package, providing standardized logging setup and access.
    
**Namespace:** creativeflow.shared.logging  
**Metadata:**
    
    - **Category:** CrossCuttingConcerns
    
- **Path:** src/creativeflow/shared/logging/config.py  
**Description:** Configures standardized logging for the platform. Sets up JSON formatter for structured logging, configures root logger, and defines log levels based on environment variables.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** config  
**Type:** Module  
**Relative Path:** logging/config.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str = 'INFO'
    - service_name: Optional[str] = None
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Standardized JSON Logging Configuration
    - Configurable Log Levels
    - Service Contextualization
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Provides a centralized function to initialize logging with a consistent JSON format across all Python services.  
**Logic Description:** Defines 'setup_logging' function. Uses 'python_json_logger.jsonlogger.JsonFormatter' to format logs as JSON. Reads log level from environment variable (e.g., LOG_LEVEL) or uses default. Adds common fields like timestamp, level, message, service_name, and allows for extra fields. Configures the root logger or a specific application logger.  
**Documentation:**
    
    - **Summary:** Module for configuring standardized JSON logging for CreativeFlow AI services.
    
**Namespace:** creativeflow.shared.logging  
**Metadata:**
    
    - **Category:** CrossCuttingConcerns
    
- **Path:** src/creativeflow/shared/logging/logger.py  
**Description:** Provides a factory function or utility to obtain a pre-configured logger instance. Ensures all parts of the application use the standardized logging setup.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** logger  
**Type:** Module  
**Relative Path:** logging/logger.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_logger  
**Parameters:**
    
    - name: str
    
**Return Type:** logging.Logger  
**Attributes:** public  
    
**Implemented Features:**
    
    - Logger Factory
    - Contextual Logging Access
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Offers a simple way for services to get a logger instance that adheres to the platform's logging standards.  
**Logic Description:** Defines 'get_logger' function. Takes a module name as input. Returns a 'logging.Logger' instance. Ensures that 'setup_logging' from 'config.py' has been called (e.g., by checking a global flag or implicitly by design).  
**Documentation:**
    
    - **Summary:** Provides a utility function to retrieve configured logger instances.
    
**Namespace:** creativeflow.shared.logging  
**Metadata:**
    
    - **Category:** CrossCuttingConcerns
    
- **Path:** src/creativeflow/shared/security/__init__.py  
**Description:** Initializer for the security module. Exports security helper functions and classes.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** security/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Security Utilities Export
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Makes the 'security' directory a Python sub-package and exports its utilities.  
**Logic Description:** Imports and re-exports functions/classes from .validation and .sanitization. Example: from .validation import validate_input; from .sanitization import sanitize_html_output.  
**Documentation:**
    
    - **Summary:** Initializes the security sub-package, providing common security-related utilities.
    
**Namespace:** creativeflow.shared.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** src/creativeflow/shared/security/validation.py  
**Description:** Provides input validation utilities, potentially leveraging Pydantic models for request/data validation. Includes common validation rules or helpers.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** validation  
**Type:** Module  
**Relative Path:** security/validation.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_payload  
**Parameters:**
    
    - payload: dict
    - model: Type[BaseDTO]
    
**Return Type:** BaseDTO  
**Attributes:** public  
    - **Name:** is_valid_email  
**Parameters:**
    
    - email_string: str
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Input Data Validation
    - Pydantic Model Validation Helper
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Offers reusable functions for validating input data against defined schemas or rules.  
**Logic Description:** Defines functions like 'validate_payload' which takes a dictionary and a Pydantic model type, attempts to parse and validate, and raises a shared 'ValidationError' on failure. May include specific validators for common patterns like email, UUIDs, etc., if not covered by Pydantic directly for all cases or if custom logic is needed.  
**Documentation:**
    
    - **Summary:** Module for input data validation, often using Pydantic models.
    
**Namespace:** creativeflow.shared.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** src/creativeflow/shared/security/sanitization.py  
**Description:** Provides output sanitization utilities, especially for HTML content to prevent XSS, using libraries like Bleach. Includes functions to clean user-generated content before display.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** sanitization  
**Type:** Module  
**Relative Path:** security/sanitization.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** sanitize_html_output  
**Parameters:**
    
    - html_string: str
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - HTML Sanitization
    - XSS Prevention Utilities
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Offers functions to sanitize potentially unsafe content before it's rendered or outputted, focusing on XSS prevention.  
**Logic Description:** Defines functions like 'sanitize_html_output'. Uses the 'bleach' library with a pre-defined set of allowed tags, attributes, and styles to clean HTML strings. Ensures that any user-provided content that might be rendered as HTML is safe.  
**Documentation:**
    
    - **Summary:** Module for sanitizing output data, particularly HTML, to prevent XSS attacks.
    
**Namespace:** creativeflow.shared.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** src/creativeflow/shared/i18n/__init__.py  
**Description:** Initializer for the i18n (internationalization) module. Exports formatting utilities and locale management functions.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** i18n/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - I18n Utilities Export
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Makes the 'i18n' directory a Python sub-package and exports its functionalities.  
**Logic Description:** Imports and re-exports functions/classes from .formatters and .utils. Example: from .formatters import format_datetime_localized; from .utils import get_current_locale.  
**Documentation:**
    
    - **Summary:** Initializes the i18n sub-package, providing tools for internationalization and localization.
    
**Namespace:** creativeflow.shared.i18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** src/creativeflow/shared/i18n/formatters.py  
**Description:** Provides functions for formatting dates, times, numbers, and currencies according to locale settings, using the Babel library.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** formatters  
**Type:** Module  
**Relative Path:** i18n/formatters.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** format_datetime_localized  
**Parameters:**
    
    - dt: datetime
    - locale_identifier: str
    - format_type: str = 'medium'
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** format_number_localized  
**Parameters:**
    
    - number: Union[int, float, Decimal]
    - locale_identifier: str
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** format_currency_localized  
**Parameters:**
    
    - amount: Union[int, float, Decimal]
    - currency_code: str
    - locale_identifier: str
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - Localized Date/Time Formatting
    - Localized Number Formatting
    - Localized Currency Formatting
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Ensures consistent and locale-aware formatting of data for display in user interfaces.  
**Logic Description:** Defines functions that wrap Babel's formatting capabilities. For example, 'format_datetime_localized' uses 'babel.dates.format_datetime'. Functions take a value and a locale identifier (e.g., 'en_US', 'de_DE') to produce a localized string representation.  
**Documentation:**
    
    - **Summary:** Module for formatting dates, times, numbers, and currencies based on locale using Babel.
    
**Namespace:** creativeflow.shared.i18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** src/creativeflow/shared/i18n/utils.py  
**Description:** Contains utility functions for internationalization, such as locale negotiation, timezone handling, or helpers for managing translation strings if not handled by a dedicated framework elsewhere.  
**Template:** Python Module  
**Dependency Level:** 1  
**Name:** utils  
**Type:** Module  
**Relative Path:** i18n/utils.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_user_locale  
**Parameters:**
    
    - user_preference: Optional[str]
    - request_headers: Optional[dict]
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** get_timezone_aware_datetime  
**Parameters:**
    
    - dt: datetime
    - timezone_str: str
    
**Return Type:** datetime  
**Attributes:** public  
    
**Implemented Features:**
    
    - Locale Detection/Resolution
    - Timezone Conversion Utilities
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Provides helper utilities for managing locale and timezone information within applications.  
**Logic Description:** Defines functions like 'get_user_locale' to determine the appropriate locale based on user settings or request information. 'get_timezone_aware_datetime' helps convert naive datetimes to timezone-aware ones or convert between timezones using 'pytz' or Python's built-in 'zoneinfo'.  
**Documentation:**
    
    - **Summary:** Utility functions supporting internationalization, including locale and timezone management.
    
**Namespace:** creativeflow.shared.i18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** src/creativeflow/shared/utils/__init__.py  
**Description:** Initializer for the general utilities module. Exports various helper functions and classes.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - General Utilities Export
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'utils' directory a Python sub-package and exports its utility functions.  
**Logic Description:** Imports and re-exports utilities from modules like .collections, .decorators. Example: from .collections import chunk_list.  
**Documentation:**
    
    - **Summary:** Initializes the general utilities sub-package.
    
**Namespace:** creativeflow.shared.utils  
**Metadata:**
    
    - **Category:** Utilities
    
- **Path:** src/creativeflow/shared/utils/collections.py  
**Description:** Contains common utility functions for working with Python collections (lists, dictionaries, sets) that are not specific to any single domain.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** collections  
**Type:** Module  
**Relative Path:** utils/collections.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** chunk_list  
**Parameters:**
    
    - data: list
    - size: int
    
**Return Type:** Generator[list, None, None]  
**Attributes:** public  
    - **Name:** deep_merge_dicts  
**Parameters:**
    
    - dict1: dict
    - dict2: dict
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - List Chunking Utility
    - Dictionary Deep Merge Utility
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable helper functions for common operations on collections.  
**Logic Description:** Defines functions like 'chunk_list' to split a list into smaller chunks of a specified size, and 'deep_merge_dicts' to recursively merge two dictionaries.  
**Documentation:**
    
    - **Summary:** Utility functions for manipulating Python collections.
    
**Namespace:** creativeflow.shared.utils  
**Metadata:**
    
    - **Category:** Utilities
    
- **Path:** src/creativeflow/shared/utils/decorators.py  
**Description:** Contains common decorators that can be applied across different services, e.g., for timing function execution, memoization, or simple retry logic if generic.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** decorators  
**Type:** Module  
**Relative Path:** utils/decorators.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** timed  
**Parameters:**
    
    - func: Callable
    
**Return Type:** Callable  
**Attributes:** public  
    - **Name:** memoize  
**Parameters:**
    
    - func: Callable
    
**Return Type:** Callable  
**Attributes:** public  
    
**Implemented Features:**
    
    - Execution Timing Decorator
    - Memoization Decorator
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable decorators for common cross-cutting concerns in function execution.  
**Logic Description:** Defines decorators such as '@timed' which logs the execution time of the decorated function, and '@memoize' for caching function results based on their arguments (simple implementation).  
**Documentation:**
    
    - **Summary:** A collection of general-purpose decorators.
    
**Namespace:** creativeflow.shared.utils  
**Metadata:**
    
    - **Category:** Utilities
    
- **Path:** src/creativeflow/shared/testing/__init__.py  
**Description:** Initializer for the shared testing utilities module. Exports mock objects, factories, and reusable test fixtures.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** testing/__init__.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Testing Utilities Export
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Makes the 'testing' directory a Python sub-package and exports its utilities to aid in testing services that consume this shared library.  
**Logic Description:** Imports and re-exports utilities from modules like .mocks, .fixtures. Example: from .mocks import MockExternalService.  
**Documentation:**
    
    - **Summary:** Initializes the shared testing utilities sub-package.
    
**Namespace:** creativeflow.shared.testing  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** src/creativeflow/shared/testing/mocks.py  
**Description:** Contains common mock objects or factories for external services or complex dependencies that consuming services might need to mock during their unit/integration tests.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** mocks  
**Type:** Module  
**Relative Path:** testing/mocks.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_mock_user_dto  
**Parameters:**
    
    - id: Optional[str] = None
    - email: Optional[str] = None
    
**Return Type:** Dict[str, Any]  
**Attributes:** public  
    
**Implemented Features:**
    
    - Shared Mock Objects
    - Test Data Factories
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Provides reusable mock implementations and test data generation utilities to simplify testing for services that depend on these shared components.  
**Logic Description:** Defines classes or factory functions that create mock instances of shared DTOs or simulate behavior of shared utilities. For example, 'create_mock_user_dto' might return a dictionary representing a UserDTO with default or specified values.  
**Documentation:**
    
    - **Summary:** Utilities for creating mock objects and test data for shared components.
    
**Namespace:** creativeflow.shared.testing  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** src/creativeflow/shared/testing/fixtures.py  
**Description:** Contains shared PyTest fixtures that can be used by consuming services in their test suites. For example, fixtures for setting up a mock logging configuration or a common test database setup (if applicable and general enough).  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** fixtures  
**Type:** Module  
**Relative Path:** testing/fixtures.py  
**Repository Id:** REPO-SHAREDLIBS-COMMON-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** mock_logger_fixture  
**Parameters:**
    
    
**Return Type:** logging.Logger  
**Attributes:** pytest.fixture  
    
**Implemented Features:**
    
    - Shared PyTest Fixtures
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Provides reusable PyTest fixtures to standardize test setups for services using this shared library.  
**Logic Description:** Defines PyTest fixtures using the '@pytest.fixture' decorator. For instance, a 'mock_logger_fixture' could set up and return a logger instance configured to write to a buffer for easy assertion of log messages during tests.  
**Documentation:**
    
    - **Summary:** Collection of shared PyTest fixtures for common test setups.
    
**Namespace:** creativeflow.shared.testing  
**Metadata:**
    
    - **Category:** Testing
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

