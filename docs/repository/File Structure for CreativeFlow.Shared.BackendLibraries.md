# Specification

# 1. Files

- **Path:** pyproject.toml  
**Description:** Defines the project metadata, dependencies, and build system configuration according to PEP 621. Specifies project name, version, authors, and tools for linting, formatting, and testing like Black, Flake8, MyPy, and PyTest.  
**Template:** Python Library Template  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:** pyproject.toml  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Packaging
    - Dependency Management
    - Tool Configuration
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** To manage the Python project's build and dependency ecosystem, ensuring consistency and adherence to modern Python packaging standards.  
**Logic Description:** This file will contain sections for [tool.poetry] or [project] to define metadata. It will list dependencies like 'pydantic' and 'fastapi'. It will also configure tools such as [tool.black], [tool.isort], [tool.mypy], and [tool.pytest.ini_options] to enforce code quality and style standards (NFR-008).  
**Documentation:**
    
    - **Summary:** Configuration file for the shared backend libraries Python package. It manages project dependencies, build configurations, and settings for integrated development tools.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/creativeflow/shared/__init__.py  
**Description:** Initializes the 'creativeflow.shared' Python package, making its submodules importable. Can be used to define package-level metadata or expose key components at the top level.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Package Definition
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** To mark the directory as a Python package, enabling modular imports and organizing the shared library structure.  
**Logic Description:** This file will be largely empty but is essential for the Python import system. It might contain a `__version__` attribute to track the library's version. It establishes the root of the shared library's namespace.  
**Documentation:**
    
    - **Summary:** The root initializer for the CreativeFlow shared backend libraries package.
    
**Namespace:** creativeflow.shared  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/shared/core/exceptions.py  
**Description:** Defines a hierarchy of custom exception classes for standardized error handling across all backend services. This ensures consistent API error responses.  
**Template:** Python Module Template  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** ExceptionFramework  
**Relative Path:** core/exceptions.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    - ExceptionHierarchy
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Standardized Error Handling
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** To provide a common set of exceptions that services can raise, allowing the API Gateway or a middleware to catch them and generate standardized HTTP error responses.  
**Logic Description:** Define a base class 'BaseAPIException' inheriting from Python's Exception. Create specific subclasses like 'NotFoundException' (HTTP 404), 'ValidationException' (HTTP 422), 'AuthenticationException' (HTTP 401), 'PermissionDeniedException' (HTTP 403), and 'ConflictException' (HTTP 409). Each exception will have attributes for status_code, detail message, and optional error-specific data.  
**Documentation:**
    
    - **Summary:** This module contains the custom exception classes used throughout the backend microservices to ensure consistent and predictable error handling and API responses.
    
**Namespace:** creativeflow.shared.core  
**Metadata:**
    
    - **Category:** CrossCuttingConcern
    
- **Path:** src/creativeflow/shared/core/logging.py  
**Description:** Provides a standardized logging configuration utility for all backend services to ensure consistent, structured (JSON) logging practices.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** logging  
**Type:** Utility  
**Relative Path:** core/logging.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** configure_logging  
**Parameters:**
    
    - service_name: str
    - log_level: str = 'INFO'
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Structured Logging
    - Correlation ID Handling
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** To abstract logging setup, ensuring all services output logs in a machine-readable JSON format with consistent fields like timestamp, log level, service name, and correlation ID.  
**Logic Description:** The `configure_logging` function will use Python's standard `logging` library. It will remove any existing handlers, add a new `StreamHandler`, and attach a formatter that outputs JSON. The formatter will include standard fields and be able to extract and include a correlation ID from a context variable (e.g., from middleware).  
**Documentation:**
    
    - **Summary:** A utility module for setting up standardized JSON logging across all backend services. This ensures logs are consistent and easily parsable by the centralized logging system (ELK/Loki).
    
**Namespace:** creativeflow.shared.core  
**Metadata:**
    
    - **Category:** CrossCuttingConcern
    
- **Path:** src/creativeflow/shared/api/dtos/base.py  
**Description:** Defines base Pydantic models and configurations to be inherited by all other DTOs. Includes common fields and settings like ORM mode.  
**Template:** Python Pydantic Template  
**Dependency Level:** 1  
**Name:** base  
**Type:** Model  
**Relative Path:** api/dtos/base.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** created_at  
**Type:** datetime  
**Attributes:** public  
    - **Name:** updated_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base DTO Definition
    
**Requirement Ids:**
    
    - Section 7
    - NFR-009
    
**Purpose:** To create a common foundation for all data transfer objects, promoting consistency and reducing code duplication in DTO definitions.  
**Logic Description:** Create a `BaseModel` class inheriting from `pydantic.BaseModel`. Configure it with `class Config: orm_mode = True` to allow easy creation from ORM objects. Define common fields like `id`, `created_at`, `updated_at` which are present in many database entities. Other DTOs will inherit from this base model.  
**Documentation:**
    
    - **Summary:** Provides the base Pydantic models for all DTOs, including common fields and configuration settings like ORM mode.
    
**Namespace:** creativeflow.shared.api.dtos  
**Metadata:**
    
    - **Category:** DataContract
    
- **Path:** src/creativeflow/shared/api/dtos/user.py  
**Description:** Contains Pydantic DTOs related to User Account and Profile Management. Used for API requests and responses.  
**Template:** Python Pydantic Template  
**Dependency Level:** 2  
**Name:** user  
**Type:** Model  
**Relative Path:** api/dtos/user.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Data Contracts
    
**Requirement Ids:**
    
    - Section 7
    
**Purpose:** To define the data structures for creating, updating, and retrieving user information, ensuring a consistent contract for the user management service's API.  
**Logic Description:** Define several Pydantic classes inheriting from the shared `BaseModel`. `UserCreate` will have fields for registration (email, password). `UserUpdate` will contain optional fields for profile updates. `UserResponse` will define the structure of the user object returned by the API, excluding sensitive fields like password hashes. `TokenResponse` will define the structure for returning JWTs.  
**Documentation:**
    
    - **Summary:** Defines the Data Transfer Objects (DTOs) for user-related API operations, such as registration, profile updates, and authentication responses.
    
**Namespace:** creativeflow.shared.api.dtos  
**Metadata:**
    
    - **Category:** DataContract
    
- **Path:** src/creativeflow/shared/api/dtos/project.py  
**Description:** Contains Pydantic DTOs for Workbench, Project, and Asset Management.  
**Template:** Python Pydantic Template  
**Dependency Level:** 2  
**Name:** project  
**Type:** Model  
**Relative Path:** api/dtos/project.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Management Data Contracts
    
**Requirement Ids:**
    
    - Section 7
    
**Purpose:** To define the data structures for managing the creative workflow, including workbenches, projects, assets, and brand kits.  
**Logic Description:** Define Pydantic models for `BrandKitCreate`, `BrandKitResponse`, `WorkbenchCreate`, `WorkbenchResponse`, `ProjectCreate`, `ProjectResponse`, and `AssetResponse`. These models will reflect the database schemas but will be tailored for API interaction, ensuring a stable contract for the Creative Management Service.  
**Documentation:**
    
    - **Summary:** Defines the Data Transfer Objects (DTOs) for creative project management, including workbenches, projects, assets, and brand kits.
    
**Namespace:** creativeflow.shared.api.dtos  
**Metadata:**
    
    - **Category:** DataContract
    
- **Path:** src/creativeflow/shared/api/dtos/generation.py  
**Description:** Contains Pydantic DTOs for AI Creative Generation requests and responses.  
**Template:** Python Pydantic Template  
**Dependency Level:** 2  
**Name:** generation  
**Type:** Model  
**Relative Path:** api/dtos/generation.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Generation Data Contracts
    
**Requirement Ids:**
    
    - Section 7
    
**Purpose:** To define the data structures for initiating and tracking AI generation tasks, ensuring a clear contract for the AI Generation Orchestration Service.  
**Logic Description:** Define `GenerationRequestCreate` with fields like `input_prompt`, `style_guidance`, and `input_parameters`. Create `GenerationStatusResponse` to return the status of a job, including links to sample assets. Define `GenerationResultResponse` for the final completed job.  
**Documentation:**
    
    - **Summary:** Defines the Data Transfer Objects (DTOs) for initiating and monitoring AI creative generation requests.
    
**Namespace:** creativeflow.shared.api.dtos  
**Metadata:**
    
    - **Category:** DataContract
    
- **Path:** src/creativeflow/shared/messaging/events.py  
**Description:** Contains Pydantic models that define the schemas for events published to and consumed from RabbitMQ.  
**Template:** Python Pydantic Template  
**Dependency Level:** 2  
**Name:** events  
**Type:** Model  
**Relative Path:** messaging/events.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    - DomainEvent
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asynchronous Event Contracts
    
**Requirement Ids:**
    
    - NFR-009
    
**Purpose:** To establish a strict, versioned contract for all asynchronous communication between microservices, ensuring reliability and decoupling.  
**Logic Description:** Define a `BaseEvent` model with common fields like `event_id`, `event_type`, `timestamp`, and `correlation_id`. Create specific event models inheriting from it, such as `UserRegisteredEvent`, `GenerationCompletedEvent`, `PaymentSucceededEvent`, and `WebhookDispatchEvent`. These schemas are the source of truth for message formats.  
**Documentation:**
    
    - **Summary:** Defines the Pydantic schemas for all asynchronous domain events used in RabbitMQ, creating a clear and enforceable contract between services.
    
**Namespace:** creativeflow.shared.messaging  
**Metadata:**
    
    - **Category:** DataContract
    
- **Path:** src/creativeflow/shared/security/auth.py  
**Description:** Provides shared security utilities, such as JWT decoding or permission checking helpers, to be used by various backend services.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** auth  
**Type:** Utility  
**Relative Path:** security/auth.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_user_from_token  
**Parameters:**
    
    - token: str
    
**Return Type:** UserDTO  
**Attributes:** public  
    - **Name:** require_role  
**Parameters:**
    
    - required_role: str
    
**Return Type:** Callable  
**Attributes:** public  
    
**Implemented Features:**
    
    - JWT Handling
    - Permission Decorators
    
**Requirement Ids:**
    
    - Section 8
    
**Purpose:** To centralize common security-related logic that can be reused by any service sitting behind the API Gateway, reducing code duplication.  
**Logic Description:** The `get_current_user_from_token` function would use a JWT library to decode a token and return a user DTO. The `require_role` function would be a decorator for FastAPI routes that checks the token payload for the required role, raising a `PermissionDeniedException` if the check fails. This standardizes authorization logic.  
**Documentation:**
    
    - **Summary:** A collection of shared utilities for handling authentication and authorization tasks, such as decoding JWTs and providing route decorators for role-based access control.
    
**Namespace:** creativeflow.shared.security  
**Metadata:**
    
    - **Category:** CrossCuttingConcern
    
- **Path:** src/creativeflow/shared/validation/validators.py  
**Description:** Contains reusable Pydantic field validators for common data validation tasks like password complexity, specific ID formats, or other business rules.  
**Template:** Python Module Template  
**Dependency Level:** 1  
**Name:** validators  
**Type:** Utility  
**Relative Path:** validation/validators.py  
**Repository Id:** REPO-SHARED-BACKEND-LIBS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_password_complexity  
**Parameters:**
    
    - password: str
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** validate_username_format  
**Parameters:**
    
    - username: str
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - Custom Data Validation
    
**Requirement Ids:**
    
    - NFR-008
    
**Purpose:** To provide a centralized library of custom validation logic that can be easily applied to Pydantic DTO models across multiple services.  
**Logic Description:** Implement functions that can be used with Pydantic's `@validator` decorator. For example, `validate_password_complexity` will use regex to check for length, uppercase, lowercase, number, and special character requirements, raising a `ValueError` if the checks fail. These functions can then be imported and used in the DTO definitions.  
**Documentation:**
    
    - **Summary:** Provides a set of reusable, common validator functions for use within Pydantic models to enforce data integrity and business rules consistently.
    
**Namespace:** creativeflow.shared.validation  
**Metadata:**
    
    - **Category:** Utility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

