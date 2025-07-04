# Specification

# 1. Files

- **Path:** libs/creativeflow-shared/pyproject.toml  
**Description:** Defines the build system requirements (setuptools, wheel) and project metadata (name, version, author, classifiers) for the CreativeFlow.Shared Python package. Specifies project dependencies like pydantic, python-json-logger, bleach. Essential for packaging and distribution.  
**Template:** TOML Configuration Template  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:** ../../pyproject.toml  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Package Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** Specifies build dependencies and core metadata for the Python package.  
**Logic Description:** Contains [build-system] table specifying requires and build-backend. Contains [project] table with name, version, description, authors, license, classifiers, dependencies, and optional-dependencies. Dependencies include pydantic, python-json-logger, bleach, and other common utilities.  
**Documentation:**
    
    - **Summary:** Standard Python packaging project file using TOML format. Defines how the shared library is built and its dependencies.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** libs/creativeflow-shared/setup.cfg  
**Description:** Provides static configuration for setuptools, complementing pyproject.toml. Can specify package details, options for build, and other distribution settings. For modern Python packaging, much of this might be in pyproject.toml, but setup.cfg can still be used for certain configurations.  
**Template:** INI Configuration Template  
**Dependency Level:** 0  
**Name:** setup  
**Type:** Configuration  
**Relative Path:** ../../setup.cfg  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Package Configuration
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** Provides build and distribution configuration for the setuptools build system.  
**Logic Description:** Contains [metadata] section for package information. Contains [options] section for specifying packages, install_requires (often redundant with pyproject.toml), python_requires. May include [options.packages.find] to auto-discover packages.  
**Documentation:**
    
    - **Summary:** Configuration file for setuptools, used in building and distributing the Python shared library.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** libs/creativeflow-shared/MANIFEST.in  
**Description:** Specifies non-code files to be included in the source distribution (sdist) of the Python package, such as licenses, data files, or documentation stubs if any are packaged.  
**Template:** Text File  
**Dependency Level:** 0  
**Name:** MANIFEST  
**Type:** Configuration  
**Relative Path:** ../../MANIFEST.in  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Source Distribution File Inclusion
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** Controls which files are included in the source distribution of the shared library.  
**Logic Description:** Contains commands like 'include LICENSE', 'recursive-include creativeflow_shared/i18n/locales *.mo' (if locale files are packaged), 'graft tests' (if tests are part of sdist for some reason, usually not for libraries).  
**Documentation:**
    
    - **Summary:** Specifies files to be included when creating a source distribution of the Python package.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/__init__.py  
**Description:** Initializes the 'creativeflow_shared' Python package. Exports key classes, functions, or submodules to make them easily accessible when the library is imported. Defines the public API surface of the shared library.  
**Template:** Python Module Template  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    - FacadePattern
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Library Public API Definition
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Makes core components of the shared library available for import.  
**Logic Description:** Contains import statements like 'from .logging.config import get_logger', 'from .error_handling.exceptions import BaseAppException, ValidationError', 'from .datamodels.common import ErrorResponseDTO', 'from .security.validation importvalidate_input'. This file carefully curates what is exposed.  
**Documentation:**
    
    - **Summary:** The main entry point for the creativeflow_shared package, defining its public interface.
    
**Namespace:** CreativeFlow.Shared  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/core/__init__.py  
**Description:** Initializes the 'core' submodule of the shared library. Exports common utilities and constants.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** core/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Core Utilities Module API
    
**Requirement Ids:**
    
    
**Purpose:** Exposes public utilities and constants from the core module.  
**Logic Description:** Contains import statements like 'from .utils import some_utility_function', 'from .constants import SOME_CONSTANT'.  
**Documentation:**
    
    - **Summary:** Initializes the core utilities module, making its functions and constants available.
    
**Namespace:** CreativeFlow.Shared.Core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/core/utils.py  
**Description:** Contains general-purpose utility functions that are shared across different services. Examples: string manipulation, date/time helpers not specific to i18n, collection helpers.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** utils  
**Type:** UtilityModule  
**Relative Path:** core/utils.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** generate_unique_id  
**Parameters:**
    
    - prefix: str = None
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** deep_merge_dicts  
**Parameters:**
    
    - dict1: dict
    - dict2: dict
    
**Return Type:** dict  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Common Utility Functions
    
**Requirement Ids:**
    
    
**Purpose:** Provides a collection of reusable, general-purpose utility functions.  
**Logic Description:** Implements helper functions that are frequently needed but don't belong to a specific domain like logging or security. Functions are stateless and deterministic where possible.  
**Documentation:**
    
    - **Summary:** A module for common, miscellaneous utility functions.
    
**Namespace:** CreativeFlow.Shared.Core  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/core/constants.py  
**Description:** Defines shared constants used across various parts of the CreativeFlow AI platform. Examples: default pagination sizes, common keys, status codes.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** constants  
**Type:** Configuration  
**Relative Path:** core/constants.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DEFAULT_PAGE_SIZE  
**Type:** int  
**Attributes:** public static  
    - **Name:** MAX_USERNAME_LENGTH  
**Type:** int  
**Attributes:** public static  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Constants Definition
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** Centralizes common constants to ensure consistency and maintainability.  
**Logic Description:** Contains definitions of constants like 'DEFAULT_API_TIMEOUT_SECONDS = 30', 'STANDARD_DATE_FORMAT = "%Y-%m-%d"'. No dynamic logic, only static definitions.  
**Documentation:**
    
    - **Summary:** A module for storing globally used constant values.
    
**Namespace:** CreativeFlow.Shared.Core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/datamodels/__init__.py  
**Description:** Initializes the 'datamodels' submodule. Exports base DTO models and common DTOs used for inter-service communication or API contracts.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** datamodels/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DataModels Module API
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Exposes base data models and common DTOs for use by other services.  
**Logic Description:** Contains import statements like 'from .base import SharedBaseModel', 'from .common import UserContextDTO, PaginatedResponseDTO'.  
**Documentation:**
    
    - **Summary:** Initializes the datamodels module, providing access to shared data structures.
    
**Namespace:** CreativeFlow.Shared.DataModels  
**Metadata:**
    
    - **Category:** DataModel
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/datamodels/base.py  
**Description:** Defines a base Pydantic model with common configurations (e.g., ORM mode, alias generation) to be inherited by other DTOs. Ensures consistency in data model definitions.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** base  
**Type:** Model  
**Relative Path:** datamodels/base.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base Data Transfer Object Definition
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Provides a consistent base class for all shared Pydantic data models.  
**Logic Description:** Defines 'SharedBaseModel(BaseModel)' with 'class Config: orm_mode = True; alias_generator = to_camel_case; allow_population_by_field_name = True'. Includes helper functions like 'to_camel_case'.  
**Documentation:**
    
    - **Summary:** A base Pydantic model providing shared configuration for DTOs.
    
**Namespace:** CreativeFlow.Shared.DataModels  
**Metadata:**
    
    - **Category:** DataModel
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/datamodels/common.py  
**Description:** Contains definitions for commonly used Data Transfer Objects (DTOs) like ErrorResponse, UserContext, Pagination structures. These are built using Pydantic and inherit from the base model.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** common  
**Type:** Model  
**Relative Path:** datamodels/common.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Common DTO Definitions
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Defines standard DTOs for consistent data exchange across services.  
**Logic Description:** Defines Pydantic models like 'ErrorDetail(SharedBaseModel)', 'ErrorResponseDTO(SharedBaseModel)', 'UserContextDTO(SharedBaseModel)', 'PaginationInfo(SharedBaseModel)', 'PaginatedResponseDTO(GenericModel, Generic[T], SharedBaseModel)'. These models include type hints and validation.  
**Documentation:**
    
    - **Summary:** A module defining common DTOs used for API responses and inter-service communication.
    
**Namespace:** CreativeFlow.Shared.DataModels  
**Metadata:**
    
    - **Category:** DataModel
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/error_handling/__init__.py  
**Description:** Initializes the 'error_handling' submodule. Exports custom exception classes and error handling utilities.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** error_handling/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Error Handling Module API
    
**Requirement Ids:**
    
    
**Purpose:** Exposes common exception classes and error handling utilities.  
**Logic Description:** Contains import statements like 'from .exceptions import BaseAppException, AuthenticationError, AuthorizationError, NotFoundError, ValidationError'.  
**Documentation:**
    
    - **Summary:** Initializes the error handling module, providing custom exceptions and utilities.
    
**Namespace:** CreativeFlow.Shared.ErrorHandling  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/error_handling/exceptions.py  
**Description:** Defines a hierarchy of custom exception classes for the application. This allows for standardized error handling and reporting across services.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** Exception  
**Relative Path:** error_handling/exceptions.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Exception Hierarchy
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** Provides standardized exception types for consistent error management.  
**Logic Description:** Defines classes like 'BaseAppException(Exception)', 'NotFoundError(BaseAppException)', 'ValidationError(BaseAppException)', 'AuthenticationError(BaseAppException)', 'AuthorizationError(BaseAppException)', 'ExternalServiceError(BaseAppException)'. Each exception can carry relevant context.  
**Documentation:**
    
    - **Summary:** A module defining custom exceptions used throughout the CreativeFlow platform.
    
**Namespace:** CreativeFlow.Shared.ErrorHandling  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/error_handling/error_reporter.py  
**Description:** Provides utilities for reporting exceptions to external error tracking services (e.g., Sentry, Rollbar). This is a shared component to ensure consistent error reporting.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** error_reporter  
**Type:** UtilityModule  
**Relative Path:** error_handling/error_reporter.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** init_error_tracking  
**Parameters:**
    
    - dsn: str
    - environment: str
    - release_version: str
    
**Return Type:** None  
**Attributes:** public static  
    - **Name:** report_exception  
**Parameters:**
    
    - exc: Exception
    - context: Optional[dict] = None
    
**Return Type:** None  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Centralized Exception Reporting
    
**Requirement Ids:**
    
    
**Purpose:** Offers a standardized way to report exceptions to monitoring systems.  
**Logic Description:** Contains functions to initialize an error tracking SDK (e.g., Sentry SDK) and to capture and send exceptions. It may include logic to add common context (like user ID, request ID) to error reports.  
**Documentation:**
    
    - **Summary:** A utility module for configuring and sending error reports to external tracking services.
    
**Namespace:** CreativeFlow.Shared.ErrorHandling  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/i18n/__init__.py  
**Description:** Initializes the 'i18n' (internationalization) submodule. Exports utilities for formatting and localization.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** i18n/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - I18n Module API
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Exposes internationalization and localization utilities.  
**Logic Description:** Contains import statements like 'from .formatting import format_datetime_localized, format_number_localized', 'from .translation import get_translator'.  
**Documentation:**
    
    - **Summary:** Initializes the i18n module, providing access to localization and formatting tools.
    
**Namespace:** CreativeFlow.Shared.I18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/i18n/formatting.py  
**Description:** Contains utilities for locale-aware formatting of dates, times, numbers, and currencies. Ensures consistent presentation of data according to user's locale.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** formatting  
**Type:** UtilityModule  
**Relative Path:** i18n/formatting.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** format_datetime_localized  
**Parameters:**
    
    - dt: datetime
    - locale: str
    - format_name: str = 'medium'
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** format_number_localized  
**Parameters:**
    
    - number: Union[int, float]
    - locale: str
    - pattern: Optional[str] = None
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** format_currency_localized  
**Parameters:**
    
    - amount: Decimal
    - currency_code: str
    - locale: str
    
**Return Type:** str  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Locale-Aware Data Formatting
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Provides standardized functions for formatting data according to locale.  
**Logic Description:** Implements functions that use libraries like 'babel' or standard library features (if sufficient) to format dates, times, numbers, and currencies based on a given locale string (e.g., 'en_US', 'de_DE').  
**Documentation:**
    
    - **Summary:** A module for formatting dates, times, numbers, and currencies in a locale-sensitive manner.
    
**Namespace:** CreativeFlow.Shared.I18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/i18n/translation.py  
**Description:** Provides utilities for message localization. This may include functions to load translation files (e.g., .po, .mo, .json) and retrieve translated strings based on a key and locale.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** translation  
**Type:** UtilityModule  
**Relative Path:** i18n/translation.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** load_translations  
**Parameters:**
    
    - locale_dir: str
    
**Return Type:** None  
**Attributes:** public static  
    - **Name:** get_translator  
**Parameters:**
    
    - locale: str
    
**Return Type:** Callable[[str], str]  
**Attributes:** public static  
    - **Name:** translate_message  
**Parameters:**
    
    - message_key: str
    - locale: str
    - **kwargs
    
**Return Type:** str  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Message Localization Utilities
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Offers functions to manage and retrieve translated UI messages.  
**Logic Description:** Implements functions to initialize and use a translation system (e.g., Python's 'gettext' or a custom dictionary-based loader). 'get_translator' would return a function that takes a message key and returns the translated string for the given locale. It might integrate with a TMS.  
**Documentation:**
    
    - **Summary:** A module for handling message translation and localization.
    
**Namespace:** CreativeFlow.Shared.I18n  
**Metadata:**
    
    - **Category:** Internationalization
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/logging/__init__.py  
**Description:** Initializes the 'logging' submodule. Exports the primary logging configuration function or logger instance.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** logging/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Logging Module API
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Exposes standardized logging setup and utilities.  
**Logic Description:** Contains import statements like 'from .config import setup_logging, get_logger'.  
**Documentation:**
    
    - **Summary:** Initializes the logging module, providing access to configured loggers.
    
**Namespace:** CreativeFlow.Shared.Logging  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/logging/config.py  
**Description:** Provides standardized logging configuration for all Python services, using 'python-json-logger' to output logs in a structured JSON format. Includes correlation ID handling.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** logging/config.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - service_name: str
    - log_level: str = 'INFO'
    - environment: str = 'development'
    
**Return Type:** None  
**Attributes:** public static  
    - **Name:** get_logger  
**Parameters:**
    
    - name: str
    
**Return Type:** logging.Logger  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Standardized JSON Logging
    - Correlation ID Logging
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Establishes a consistent, structured logging format across all services.  
**Logic Description:** Configures the Python 'logging' module to use 'python_json_logger.JsonFormatter'. Adds fields like 'timestamp', 'level', 'message', 'service_name', 'correlation_id', and other relevant context. 'setup_logging' is called once at application startup. 'get_logger' returns a configured logger instance.  
**Documentation:**
    
    - **Summary:** A module for setting up standardized JSON-based logging for Python applications.
    
**Namespace:** CreativeFlow.Shared.Logging  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/logging/middleware.py  
**Description:** Contains optional logging middleware for common Python web frameworks (e.g., FastAPI, Flask) to automatically log request/response details and manage correlation IDs.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** middleware  
**Type:** Middleware  
**Relative Path:** logging/middleware.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** FastAPILoggingMiddleware  
**Parameters:**
    
    - app: ASGIApp
    
**Return Type:** ASGIApp  
**Attributes:** public class  
    - **Name:** FlaskLoggingMiddleware  
**Parameters:**
    
    - app: WSGIApp
    
**Return Type:** WSGIApp  
**Attributes:** public class  
    
**Implemented Features:**
    
    - Automated Request/Response Logging
    - Correlation ID Propagation
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Provides middleware to simplify request logging and correlation ID handling in web services.  
**Logic Description:** Implements ASGI/WSGI middleware that intercepts requests and responses. It extracts/generates a correlation ID, logs request details (path, method, headers), logs response details (status code, latency), and ensures the correlation ID is available for subsequent logging within the request context.  
**Documentation:**
    
    - **Summary:** Middleware components for integrating standardized logging into web applications.
    
**Namespace:** CreativeFlow.Shared.Logging  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/security/__init__.py  
**Description:** Initializes the 'security' submodule. Exports utilities for input/output sanitization and validation.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** security/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Security Utilities Module API
    
**Requirement Ids:**
    
    
**Purpose:** Exposes common security helper functions.  
**Logic Description:** Contains import statements like 'from .sanitization import sanitize_html_input', 'from .validation import validate_request_payload'.  
**Documentation:**
    
    - **Summary:** Initializes the security module, providing access to sanitization and validation utilities.
    
**Namespace:** CreativeFlow.Shared.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/security/sanitization.py  
**Description:** Contains utilities for sanitizing user inputs and encoding outputs to prevent common vulnerabilities like XSS. Utilizes libraries like 'bleach' for HTML sanitization.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** sanitization  
**Type:** UtilityModule  
**Relative Path:** security/sanitization.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** sanitize_html_input  
**Parameters:**
    
    - html_string: str
    - allowed_tags: Optional[list] = None
    - allowed_attributes: Optional[dict] = None
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** encode_for_html_attribute  
**Parameters:**
    
    - text: str
    
**Return Type:** str  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Input Sanitization
    - Output Encoding
    
**Requirement Ids:**
    
    
**Purpose:** Provides functions to clean inputs and safely encode outputs.  
**Logic Description:** Implements 'sanitize_html_input' using 'bleach.clean()' with configurable allowed tags and attributes. Implements output encoding functions for different contexts (HTML body, HTML attributes, JavaScript).  
**Documentation:**
    
    - **Summary:** A module for sanitizing inputs and encoding outputs to mitigate security risks like XSS.
    
**Namespace:** CreativeFlow.Shared.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/security/validation.py  
**Description:** Provides common validation utilities, potentially using Pydantic for data validation within API request/response cycles, or custom validation functions for specific security checks (e.g., password strength, input format).  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** validation  
**Type:** UtilityModule  
**Relative Path:** security/validation.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_request_payload  
**Parameters:**
    
    - payload: dict
    - schema: Type[BaseModel]
    
**Return Type:** BaseModel  
**Attributes:** public static  
    - **Name:** is_strong_password  
**Parameters:**
    
    - password: str
    
**Return Type:** bool  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Data Validation Utilities
    - Security-Specific Validations
    
**Requirement Ids:**
    
    
**Purpose:** Offers reusable functions for validating data structures and specific security-related inputs.  
**Logic Description:** 'validate_request_payload' uses a Pydantic schema to validate an input dictionary, raising a shared ValidationError on failure. 'is_strong_password' implements password complexity checks.  
**Documentation:**
    
    - **Summary:** A module containing utilities for data validation, especially for API inputs and security checks.
    
**Namespace:** CreativeFlow.Shared.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/testing_utils/__init__.py  
**Description:** Initializes the 'testing_utils' submodule. Exports shared test fixtures, mock objects, and assertion helpers to promote consistent and efficient testing across services.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** testing_utils/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Testing Utilities Module API
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Exposes common utilities and fixtures for writing tests.  
**Logic Description:** Contains import statements like 'from .fixtures import db_session_mock, user_fixture', 'from .mocks import MockRedisClient', 'from .assertions import assert_dto_matches_dict'.  
**Documentation:**
    
    - **Summary:** Initializes the testing utilities module, providing tools for test development.
    
**Namespace:** CreativeFlow.Shared.TestingUtils  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/testing_utils/fixtures.py  
**Description:** Defines reusable pytest fixtures for setting up common test scenarios, such as database sessions, mock service clients, or pre-populated data models.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** fixtures  
**Type:** TestUtility  
**Relative Path:** testing_utils/fixtures.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** mock_db_session  
**Parameters:**
    
    
**Return Type:** MagicMock  
**Attributes:** public pytest.fixture  
    - **Name:** sample_user_dto  
**Parameters:**
    
    
**Return Type:** UserContextDTO  
**Attributes:** public pytest.fixture  
    
**Implemented Features:**
    
    - Shared Pytest Fixtures
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Provides common, reusable fixtures to simplify test setup.  
**Logic Description:** Contains pytest fixture definitions. For example, a fixture to mock a database session, or a fixture to provide a default User DTO instance. Uses libraries like 'pytest' and 'unittest.mock'.  
**Documentation:**
    
    - **Summary:** A module defining shared pytest fixtures for test setup and data generation.
    
**Namespace:** CreativeFlow.Shared.TestingUtils  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/testing_utils/mocks.py  
**Description:** Contains reusable mock objects or classes for external dependencies or complex internal components. This helps in isolating units under test.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** mocks  
**Type:** TestUtility  
**Relative Path:** testing_utils/mocks.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** MockExternalServiceClient  
**Parameters:**
    
    
**Return Type:** MagicMock  
**Attributes:** public class  
    - **Name:** patch_datetime_now  
**Parameters:**
    
    - fixed_datetime: datetime
    
**Return Type:** ContextManager  
**Attributes:** public contextmanager  
    
**Implemented Features:**
    
    - Reusable Mock Objects
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Provides common mock implementations for dependencies.  
**Logic Description:** Defines classes or functions that return mock objects (e.g., using 'unittest.mock.MagicMock') configured for common scenarios. Includes context managers for patching specific functionalities during tests (e.g., 'datetime.now').  
**Documentation:**
    
    - **Summary:** A module containing mock classes and utilities for isolating components during testing.
    
**Namespace:** CreativeFlow.Shared.TestingUtils  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/testing_utils/assertions.py  
**Description:** Defines custom assertion helper functions to simplify common assertion patterns in tests, making tests more readable and maintainable.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** assertions  
**Type:** TestUtility  
**Relative Path:** testing_utils/assertions.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** assert_dtos_equal_ignoring_fields  
**Parameters:**
    
    - dto1: BaseModel
    - dto2: BaseModel
    - ignore_fields: List[str]
    
**Return Type:** None  
**Attributes:** public static  
    - **Name:** assert_timestamp_approx_now  
**Parameters:**
    
    - timestamp: datetime
    - tolerance_seconds: int = 5
    
**Return Type:** None  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Custom Test Assertions
    
**Requirement Ids:**
    
    - NFR-011
    
**Purpose:** Provides tailored assertion functions for common testing needs.  
**Logic Description:** Implements functions that perform complex or repetitive assertions. For example, comparing two Pydantic models while ignoring certain fields, or asserting a datetime is close to the current time within a tolerance.  
**Documentation:**
    
    - **Summary:** A module for custom assertion helpers to make tests cleaner and more expressive.
    
**Namespace:** CreativeFlow.Shared.TestingUtils  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/config_management/__init__.py  
**Description:** Initializes the 'config_management' submodule. Exports utilities for loading and validating shared configurations.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInitializer  
**Relative Path:** config_management/__init__.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Management Module API
    
**Requirement Ids:**
    
    
**Purpose:** Exposes utilities for managing application configurations.  
**Logic Description:** Contains import statements like 'from .loader import load_app_config', 'from .schemas import AppConfigSchema'.  
**Documentation:**
    
    - **Summary:** Initializes the configuration management module.
    
**Namespace:** CreativeFlow.Shared.ConfigManagement  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/config_management/loader.py  
**Description:** Provides utilities for loading configurations from various sources (e.g., environment variables, config files) and populating Pydantic models for validation and type-safe access.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** loader  
**Type:** UtilityModule  
**Relative Path:** config_management/loader.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** load_app_config  
**Parameters:**
    
    - config_schema: Type[BaseModel]
    - env_prefix: str = 'APP_'
    
**Return Type:** BaseModel  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Configuration Loading
    - Configuration Validation
    
**Requirement Ids:**
    
    
**Purpose:** Offers a standardized way to load and validate application configurations.  
**Logic Description:** Implements a function that loads configuration settings from environment variables (potentially with a prefix) and/or config files (e.g., YAML, .env). Uses a Pydantic schema for validation and to provide a typed config object.  
**Documentation:**
    
    - **Summary:** A module for loading application configurations from environment or files and validating them.
    
**Namespace:** CreativeFlow.Shared.ConfigManagement  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** libs/creativeflow-shared/creativeflow_shared/config_management/schemas.py  
**Description:** Defines Pydantic schemas for shared configuration structures. This allows for validation and type hinting of configuration objects used by services.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** schemas  
**Type:** Model  
**Relative Path:** config_management/schemas.py  
**Repository Id:** REPO-SHARED-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Schema Definitions
    
**Requirement Ids:**
    
    
**Purpose:** Provides Pydantic models for validating and accessing configuration data.  
**Logic Description:** Defines Pydantic models representing expected configuration structures. For example, 'DatabaseConfig(BaseModel)', 'RedisConfig(BaseModel)', 'ServiceEndpointsConfig(BaseModel)'. These schemas define types and validation rules for configuration parameters.  
**Documentation:**
    
    - **Summary:** A module containing Pydantic schemas for application configuration structures.
    
**Namespace:** CreativeFlow.Shared.ConfigManagement  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - LOG_STRUCTURED_JSON_ENABLED
  - SANITIZE_HTML_INPUT_STRICT_MODE
  - I18N_DEFAULT_LOCALE_FALLBACK_ENABLED
  - ERROR_REPORTING_VERBOSE_CONTEXT
  
- **Database Configs:**
  
  


---

