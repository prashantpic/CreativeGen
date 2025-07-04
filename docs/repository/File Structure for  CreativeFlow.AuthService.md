# Specification

# 1. Files

- **Path:** services/auth-service/pyproject.toml  
**Description:** Python project configuration file using Poetry. Defines project metadata, dependencies, scripts, and tool configurations (e.g., for linters, testers).  
**Template:** Python Poetry Project File  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DependencyManagement
    - ProjectMetadata
    
**Requirement Ids:**
    
    
**Purpose:** Defines project structure, dependencies (FastAPI, SQLAlchemy, Pydantic, python-jose, passlib, Redis, etc.), and build/tooling configurations.  
**Logic Description:** Specifies Python version (3.11+). Lists all runtime and development dependencies. Configures linters (e.g., Flake8, Black) and test runners (e.g., PyTest).  
**Documentation:**
    
    - **Summary:** Core project definition file for managing dependencies and development environment settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** services/auth-service/.env.example  
**Description:** Example environment variables file. Provides a template for required environment variables such as database connection strings, Redis URL, JWT secrets, social login API keys, email service credentials, etc. Actual values are not stored here.  
**Template:** Environment Variables Template  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - ConfigurationTemplate
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-002
    
**Purpose:** Serves as a template for developers to set up their local environment variables and for CI/CD to configure deployment environments.  
**Logic Description:** Lists all environment variables required by the application, with placeholder or example values. Includes DATABASE_URL, REDIS_URL, JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SOCIAL_GOOGLE_CLIENT_ID, SOCIAL_GOOGLE_CLIENT_SECRET, EMAIL_HOST, EMAIL_PORT, etc.  
**Documentation:**
    
    - **Summary:** Template for environment-specific configuration variables. Actual secrets are managed externally.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** services/auth-service/alembic.ini  
**Description:** Configuration file for Alembic, the database migration tool for SQLAlchemy.  
**Template:** Alembic Configuration  
**Dependency Level:** 0  
**Name:** alembic  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DatabaseMigrationConfiguration
    
**Requirement Ids:**
    
    
**Purpose:** Configures Alembic settings, including database connection URL (sourced from env), migration script location, and other migration parameters.  
**Logic Description:** Points to the database connection string. Specifies the directory for migration scripts (`src/creativeflow/authservice/infrastructure/database/alembic/versions`). Defines how migration environment is set up.  
**Documentation:**
    
    - **Summary:** Main configuration file for Alembic database migrations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Database
    
- **Path:** services/auth-service/src/creativeflow/authservice/__init__.py  
**Description:** Initializes the authservice Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:**   
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package, allowing modules within it to be imported.  
**Logic Description:** This file is typically empty or may contain package-level initializations or imports if necessary.  
**Documentation:**
    
    - **Summary:** Package initializer for the authservice.
    
**Namespace:** CreativeFlow.Services.Auth  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/auth-service/src/creativeflow/authservice/config.py  
**Description:** Application configuration settings using Pydantic. Loads settings from environment variables.  
**Template:** Python Pydantic Settings  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** REDIS_URL  
**Type:** str  
**Attributes:**   
    - **Name:** JWT_SECRET_KEY  
**Type:** str  
**Attributes:**   
    - **Name:** JWT_ALGORITHM  
**Type:** str  
**Attributes:**   
    - **Name:** ACCESS_TOKEN_EXPIRE_MINUTES  
**Type:** int  
**Attributes:**   
    - **Name:** REFRESH_TOKEN_EXPIRE_DAYS  
**Type:** int  
**Attributes:**   
    - **Name:** EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS  
**Type:** int  
**Attributes:**   
    - **Name:** PASSWORD_RESET_TOKEN_EXPIRE_HOURS  
**Type:** int  
**Attributes:**   
    - **Name:** MFA_OTP_EXPIRE_SECONDS  
**Type:** int  
**Attributes:**   
    - **Name:** SOCIAL_GOOGLE_CLIENT_ID  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** SOCIAL_GOOGLE_CLIENT_SECRET  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** EMAIL_HOST  
**Type:** str  
**Attributes:**   
    - **Name:** EMAIL_PORT  
**Type:** int  
**Attributes:**   
    - **Name:** EMAIL_USERNAME  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** EMAIL_PASSWORD  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** EMAIL_FROM_ADDRESS  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - ConfigurationManagement
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-002
    - REQ-001
    - REQ-002
    
**Purpose:** Defines and loads all application settings from environment variables, ensuring type safety and central configuration access.  
**Logic Description:** Uses Pydantic's `BaseSettings` to define settings. Environment variables are loaded automatically. Provides a cached `get_settings` function for global access.  
**Documentation:**
    
    - **Summary:** Manages application-wide configuration settings loaded from environment variables.
    
**Namespace:** CreativeFlow.Services.Auth.Config  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/auth-service/src/creativeflow/authservice/main.py  
**Description:** Main FastAPI application entry point. Initializes the FastAPI app, includes routers, and sets up middleware.  
**Template:** Python FastAPI Main  
**Dependency Level:** 0  
**Name:** main  
**Type:** Application  
**Relative Path:**   
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - ApplicationInitialization
    - APIRouting
    - MiddlewareSetup
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the FastAPI application, configures global middleware (e.g., CORS, error handling), and includes all API routers.  
**Logic Description:** Creates a FastAPI instance. Includes routers from `api.v1.routers`. Sets up CORS middleware, global exception handlers, and any other application-level middleware (e.g., for setting secure cookie flags indirectly via responses).  
**Documentation:**
    
    - **Summary:** The main entry point for the FastAPI application, responsible for app setup and routing.
    
**Namespace:** CreativeFlow.Services.Auth  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/auth-service/src/creativeflow/authservice/utils/__init__.py  
**Description:** Initializes the utils Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for utility modules.
    
**Namespace:** CreativeFlow.Services.Auth.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** services/auth-service/src/creativeflow/authservice/utils/token_generator.py  
**Description:** Utility functions for generating various secure tokens (e.g., email verification, password reset).  
**Template:** Python Utility Module  
**Dependency Level:** 0  
**Name:** token_generator  
**Type:** Utility  
**Relative Path:** utils  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** generate_secure_token  
**Parameters:**
    
    - length: int = 32
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** generate_otp_code  
**Parameters:**
    
    - length: int = 6
    
**Return Type:** str  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - SecureTokenGeneration
    - OTPGeneration
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-002
    
**Purpose:** Provides functions to generate cryptographically secure random strings for use as verification tokens, OTPs, etc.  
**Logic Description:** Uses `secrets.token_urlsafe` for secure random string generation. For OTPs, generates a string of digits.  
**Documentation:**
    
    - **Summary:** Utility for generating secure random tokens and OTP codes.
    
**Namespace:** CreativeFlow.Services.Auth.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** services/auth-service/src/creativeflow/authservice/utils/time_utils.py  
**Description:** Utility functions for time and timezone operations.  
**Template:** Python Utility Module  
**Dependency Level:** 0  
**Name:** time_utils  
**Type:** Utility  
**Relative Path:** utils  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_utc_time  
**Parameters:**
    
    
**Return Type:** datetime  
**Attributes:** public|static  
    - **Name:** is_token_expired  
**Parameters:**
    
    - expires_at: datetime
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - TimeManipulation
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-002
    
**Purpose:** Provides helper functions for common time-related operations, ensuring UTC is used for consistency.  
**Logic Description:** Uses `datetime.datetime.utcnow()` for current UTC time. Compares expiration timestamps against current UTC time.  
**Documentation:**
    
    - **Summary:** Utility functions for handling date and time operations, primarily focusing on UTC.
    
**Namespace:** CreativeFlow.Services.Auth.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/enums.py  
**Description:** Defines domain-specific enumerations.  
**Template:** Python Enum Module  
**Dependency Level:** 0  
**Name:** enums  
**Type:** Domain  
**Relative Path:** core/domain  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SocialProvider  
**Type:** Enum  
**Attributes:**   
    - **Name:** MFAMethod  
**Type:** Enum  
**Attributes:**   
    - **Name:** UserRole  
**Type:** Enum  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - DomainEnumerations
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-002
    - REQ-003
    
**Purpose:** Provides enumerations for concepts like social login providers (Google, Facebook, Apple), MFA methods (SMS, TOTP, Email), and user roles.  
**Logic Description:** Defines Python `Enum` classes for SocialProvider (GOOGLE, FACEBOOK, APPLE), MFAMethod (SMS, TOTP, EMAIL), and UserRole (OWNER, ADMIN, EDITOR, VIEWER).  
**Documentation:**
    
    - **Summary:** Contains enumerations used throughout the authentication domain.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Enums  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/exceptions.py  
**Description:** Custom domain-specific exceptions for the authentication service.  
**Template:** Python Exception Module  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** Domain  
**Relative Path:** core/domain  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** AuthServiceException  
**Type:** class (BaseException)  
**Attributes:**   
    - **Name:** UserNotFoundException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** InvalidCredentialsException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** TokenExpiredException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** InvalidTokenException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** MFAChallengeRequiredException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** MFAInvalidCodeException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** EmailAlreadyExistsException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    - **Name:** EmailNotVerifiedException  
**Type:** class (AuthServiceException)  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - CustomExceptionHandling
    
**Requirement Ids:**
    
    
**Purpose:** Defines custom exceptions to represent specific error conditions within the authentication domain, allowing for more granular error handling.  
**Logic Description:** Each exception class inherits from a base `AuthServiceException` or standard Python exceptions. They may carry additional context.  
**Documentation:**
    
    - **Summary:** Provides custom exceptions for clear and specific error handling within the authentication service.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Exceptions  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/notifications/interface.py  
**Description:** Defines the interface for notification services (email, SMS).  
**Template:** Python Interface Module  
**Dependency Level:** 0  
**Name:** interface  
**Type:** Interface  
**Relative Path:** infrastructure/notifications  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInversion
    
**Members:**
    
    
**Methods:**
    
    - **Name:** send_email  
**Parameters:**
    
    - to_email: str
    - subject: str
    - html_content: str
    
**Return Type:** Awaitable[None]  
**Attributes:** public|abstractmethod  
    - **Name:** send_sms  
**Parameters:**
    
    - to_phone: str
    - message: str
    
**Return Type:** Awaitable[None]  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - NotificationServiceAbstraction
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-002
    
**Purpose:** Abstracts the sending of notifications, allowing different implementations (e.g., actual email/SMS service, mock service for tests).  
**Logic Description:** Defines an abstract base class `NotificationService` with methods like `send_email` and `send_sms`. Core services will depend on this interface.  
**Documentation:**
    
    - **Summary:** Interface for notification sending services, decoupling core logic from specific notification providers.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Notifications  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/__init__.py  
**Description:** Initializes the domain models Python package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for domain model modules.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/user_model.py  
**Description:** SQLAlchemy model representing a user in the system.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** user_model  
**Type:** Model  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** primary_key|index  
    - **Name:** email  
**Type:** String  
**Attributes:** unique|index|nullable=False  
    - **Name:** hashed_password  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** full_name  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** default=True  
    - **Name:** is_verified  
**Type:** Boolean  
**Attributes:** default=False  
    - **Name:** verification_token  
**Type:** String  
**Attributes:** nullable=True|index  
    - **Name:** verification_token_expires_at  
**Type:** DateTime  
**Attributes:** nullable=True  
    - **Name:** password_reset_token  
**Type:** String  
**Attributes:** nullable=True|index  
    - **Name:** password_reset_token_expires_at  
**Type:** DateTime  
**Attributes:** nullable=True  
    - **Name:** social_provider  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** social_provider_id  
**Type:** String  
**Attributes:** nullable=True|index  
    - **Name:** last_login_at  
**Type:** DateTime  
**Attributes:** nullable=True  
    - **Name:** created_at  
**Type:** DateTime  
**Attributes:** default=func.now()  
    - **Name:** updated_at  
**Type:** DateTime  
**Attributes:** default=func.now()|onupdate=func.now()  
    - **Name:** mfa_factors  
**Type:** relationship  
**Attributes:** back_populates='user'  
    - **Name:** recovery_codes  
**Type:** relationship  
**Attributes:** back_populates='user'  
    - **Name:** roles  
**Type:** relationship  
**Attributes:** secondary=user_roles_table|back_populates='users'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - UserEntityDefinition
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-002
    - REQ-003
    - NFR-006
    
**Purpose:** Defines the database schema for the `users` table using SQLAlchemy ORM.  
**Logic Description:** Includes fields for ID, email, hashed password, verification status/token, password reset status/token, social login details, MFA links, roles, and timestamps. Ensures unique constraints on email and social provider ID. Uses `Base` from `database.base`.  
**Documentation:**
    
    - **Summary:** SQLAlchemy model for user accounts, storing essential authentication and profile information.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/mfa_model.py  
**Description:** SQLAlchemy model representing MFA factors for a user.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** mfa_model  
**Type:** Model  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** primary_key|index  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** ForeignKey('users.id')|nullable=False  
    - **Name:** method  
**Type:** String  
**Attributes:** nullable=False  
    - **Name:** secret_key_encrypted  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** phone_number_encrypted  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** email_address  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** is_enabled  
**Type:** Boolean  
**Attributes:** default=False  
    - **Name:** created_at  
**Type:** DateTime  
**Attributes:** default=func.now()  
    - **Name:** user  
**Type:** relationship  
**Attributes:** back_populates='mfa_factors'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - MFAFactorEntityDefinition
    
**Requirement Ids:**
    
    - REQ-002
    - NFR-006
    
**Purpose:** Defines the database schema for storing user's MFA configurations (e.g., TOTP secret, verified phone for SMS).  
**Logic Description:** Includes fields for user ID, MFA method type (TOTP, SMS, EMAIL), encrypted secret/phone, status, and timestamps. Uses `Base`.  
**Documentation:**
    
    - **Summary:** SQLAlchemy model for user Multi-Factor Authentication methods and their configurations.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/role_model.py  
**Description:** SQLAlchemy model representing user roles.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** role_model  
**Type:** Model  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** Integer  
**Attributes:** primary_key|autoincrement=True  
    - **Name:** name  
**Type:** String  
**Attributes:** unique|index|nullable=False  
    - **Name:** description  
**Type:** String  
**Attributes:** nullable=True  
    - **Name:** users  
**Type:** relationship  
**Attributes:** secondary=user_roles_table|back_populates='roles'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - RoleEntityDefinition
    
**Requirement Ids:**
    
    - REQ-003
    
**Purpose:** Defines the database schema for user roles (e.g., Owner, Admin, Editor, Viewer). `user_roles_table` will be an association table.  
**Logic Description:** Includes fields for role ID, name (unique), and description. Defines `user_roles_table` as `Table('user_roles', Base.metadata, Column('user_id', UUID, ForeignKey('users.id')), Column('role_id', Integer, ForeignKey('roles.id')))`.  
**Documentation:**
    
    - **Summary:** SQLAlchemy model for defining user roles within the system.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/recovery_code_model.py  
**Description:** SQLAlchemy model for storing hashed MFA recovery codes.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** recovery_code_model  
**Type:** Model  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** primary_key|index  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** ForeignKey('users.id')|nullable=False  
    - **Name:** hashed_code  
**Type:** String  
**Attributes:** nullable=False  
    - **Name:** is_used  
**Type:** Boolean  
**Attributes:** default=False  
    - **Name:** created_at  
**Type:** DateTime  
**Attributes:** default=func.now()  
    - **Name:** user  
**Type:** relationship  
**Attributes:** back_populates='recovery_codes'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - RecoveryCodeEntityDefinition
    
**Requirement Ids:**
    
    - REQ-002
    - NFR-006
    
**Purpose:** Defines the database schema for storing hashed MFA recovery codes for users.  
**Logic Description:** Includes fields for user ID, hashed recovery code, used status, and timestamp. Uses `Base`.  
**Documentation:**
    
    - **Summary:** SQLAlchemy model for MFA recovery codes, ensuring they are stored securely.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/domain/models/token_revocation_model.py  
**Description:** SQLAlchemy model for storing revoked JWTs (e.g., JTI - JWT ID).  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** token_revocation_model  
**Type:** Model  
**Relative Path:** core/domain/models  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** jti  
**Type:** String  
**Attributes:** primary_key|index  
    - **Name:** expires_at  
**Type:** DateTime  
**Attributes:** nullable=False|index  
    
**Methods:**
    
    
**Implemented Features:**
    
    - TokenRevocationStorage
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Defines a schema for storing identifiers of revoked JWTs to prevent their reuse, typically used for refresh tokens or if immediate access token revocation is needed beyond expiry. Could also be handled purely in Redis.  
**Logic Description:** Stores the JWT ID (jti) and its original expiry time to allow for cleanup. Uses `Base`. An alternative implementation could use Redis directly with TTL.  
**Documentation:**
    
    - **Summary:** SQLAlchemy model for persisting revoked JWT identifiers, aiding in token lifecycle management.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Domain.Models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/security/__init__.py  
**Description:** Initializes the security core Python package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** core/security  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for security-related core modules.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/security/password_manager.py  
**Description:** Handles password hashing and verification using passlib/bcrypt.  
**Template:** Python Security Module  
**Dependency Level:** 1  
**Name:** password_manager  
**Type:** Security  
**Relative Path:** core/security  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** pwd_context  
**Type:** CryptContext  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** get_password_hash  
**Parameters:**
    
    - password: str
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** verify_password  
**Parameters:**
    
    - plain_password: str
    - hashed_password: str
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - PasswordHashing
    - PasswordVerification
    
**Requirement Ids:**
    
    - NFR-006
    - SEC-001
    
**Purpose:** Provides secure password hashing using bcrypt via passlib and verification of plain passwords against stored hashes.  
**Logic Description:** Initializes `CryptContext` with bcrypt scheme. `get_password_hash` hashes the password. `verify_password` checks a plain password against a hash.  
**Documentation:**
    
    - **Summary:** Manages secure hashing and verification of user passwords.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/security/jwt_manager.py  
**Description:** Handles JWT generation, signing, and validation using python-jose.  
**Template:** Python Security Module  
**Dependency Level:** 1  
**Name:** jwt_manager  
**Type:** Security  
**Relative Path:** core/security  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SECRET_KEY  
**Type:** str  
**Attributes:** private  
    - **Name:** ALGORITHM  
**Type:** str  
**Attributes:** private  
    - **Name:** ACCESS_TOKEN_EXPIRE_MINUTES  
**Type:** int  
**Attributes:** private  
    - **Name:** REFRESH_TOKEN_EXPIRE_DAYS  
**Type:** int  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_access_token  
**Parameters:**
    
    - data: dict
    - expires_delta: Optional[timedelta] = None
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** create_refresh_token  
**Parameters:**
    
    - data: dict
    - expires_delta: Optional[timedelta] = None
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** decode_token  
**Parameters:**
    
    - token: str
    
**Return Type:** Optional[dict]  
**Attributes:** public  
    - **Name:** generate_jti  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:** private|static  
    
**Implemented Features:**
    
    - JWTGeneration
    - JWTValidation
    - RefreshTokenManagement
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Manages the lifecycle of JSON Web Tokens (JWTs), including creation of access and refresh tokens, and decoding/validating tokens.  
**Logic Description:** Loads secret key, algorithm, and expiry times from config. `create_access_token` and `create_refresh_token` encode data (subject, claims, expiry, JTI) into JWTs. `decode_token` validates and decodes a JWT, handling expiry and signature errors. Includes JTI generation.  
**Documentation:**
    
    - **Summary:** Provides functionalities for creating, signing, and validating JWTs for authentication.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/security/permissions.py  
**Description:** FastAPI dependency functions for checking user roles and permissions.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 1  
**Name:** permissions  
**Type:** Security  
**Relative Path:** core/security  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_active_user  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** User  
**Attributes:** public  
    - **Name:** require_role  
**Parameters:**
    
    - required_role: UserRole
    
**Return Type:** Callable  
**Attributes:** public  
    
**Implemented Features:**
    
    - RBACEnforcement
    - AuthenticatedUserProvider
    
**Requirement Ids:**
    
    - REQ-003
    - SEC-001
    
**Purpose:** Provides FastAPI dependencies to get the currently authenticated user and to enforce role-based access control on specific endpoints.  
**Logic Description:** `oauth2_scheme` is an instance of `OAuth2PasswordBearer`. `get_current_active_user` decodes the JWT from the Authorization header, retrieves the user from the database, and checks if active. `require_role` is a factory function that returns a dependency checking if the current user has the specified role.  
**Documentation:**
    
    - **Summary:** Defines FastAPI dependencies for user authentication and role-based authorization.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/security/totp_handler.py  
**Description:** Handles Time-based One-Time Password (TOTP) generation and verification for MFA.  
**Template:** Python Security Module  
**Dependency Level:** 1  
**Name:** totp_handler  
**Type:** Security  
**Relative Path:** core/security  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** generate_totp_secret  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** get_totp_uri  
**Parameters:**
    
    - secret: str
    - issuer_name: str
    - account_name: str
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** verify_totp_code  
**Parameters:**
    
    - secret: str
    - code: str
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - TOTPGeneration
    - TOTPVerification
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Provides functionalities for generating TOTP secrets, creating provisioning URIs for authenticator apps, and verifying TOTP codes.  
**Logic Description:** Uses a library like `pyotp`. `generate_totp_secret` creates a base32 encoded secret. `get_totp_uri` formats a provisioning URI. `verify_totp_code` checks if a given code is valid for the secret.  
**Documentation:**
    
    - **Summary:** Manages Time-based One-Time Password (TOTP) operations for multi-factor authentication.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/__init__.py  
**Description:** Initializes the database infrastructure Python package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for database configuration and access modules.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/db_config.py  
**Description:** SQLAlchemy database engine and session management setup.  
**Template:** Python SQLAlchemy Config  
**Dependency Level:** 1  
**Name:** db_config  
**Type:** Configuration  
**Relative Path:** infrastructure/database  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SQLALCHEMY_DATABASE_URL  
**Type:** str  
**Attributes:** private  
    - **Name:** engine  
**Type:** Engine  
**Attributes:** public  
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Iterator[Session]  
**Attributes:** public  
    
**Implemented Features:**
    
    - DatabaseConnection
    - SessionManagement
    
**Requirement Ids:**
    
    
**Purpose:** Configures the SQLAlchemy database engine using the DATABASE_URL from settings and provides a session factory (`SessionLocal`) and a FastAPI dependency (`get_db`) for database sessions.  
**Logic Description:** Reads `DATABASE_URL` from `config.settings`. Creates `engine` using `create_engine`. Creates `SessionLocal` using `sessionmaker`. `get_db` is a generator function for FastAPI dependency injection, ensuring session is closed after request.  
**Documentation:**
    
    - **Summary:** Sets up SQLAlchemy database connection and session management.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/base.py  
**Description:** SQLAlchemy declarative base for ORM models.  
**Template:** Python SQLAlchemy Base  
**Dependency Level:** 1  
**Name:** base  
**Type:** Model  
**Relative Path:** infrastructure/database  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** Base  
**Type:** DeclarativeMeta  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - ORMBaseDefinition
    
**Requirement Ids:**
    
    
**Purpose:** Provides the declarative base class that all SQLAlchemy ORM models in the application will inherit from.  
**Logic Description:** Imports `declarative_base` from `sqlalchemy.orm` and assigns it to `Base`. This file will also import all model files (e.g., `from ..core.domain.models.user_model import User`) so that Alembic can discover them.  
**Documentation:**
    
    - **Summary:** Defines the base for SQLAlchemy ORM models and ensures models are discoverable by Alembic.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/redis_config.py  
**Description:** Redis client connection setup.  
**Template:** Python Redis Config  
**Dependency Level:** 1  
**Name:** redis_config  
**Type:** Configuration  
**Relative Path:** infrastructure/database  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** redis_client  
**Type:** Redis  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_redis_client  
**Parameters:**
    
    
**Return Type:** Redis  
**Attributes:** public  
    
**Implemented Features:**
    
    - RedisConnection
    
**Requirement Ids:**
    
    - SEC-002
    
**Purpose:** Initializes and configures the Redis client instance for connecting to the Redis server.  
**Logic Description:** Reads `REDIS_URL` from `config.settings`. Creates a Redis client instance using the `redis` library. Provides a `get_redis_client` function for dependency injection or global access.  
**Documentation:**
    
    - **Summary:** Manages Redis client connection and configuration.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/alembic/env.py  
**Description:** Alembic environment configuration script.  
**Template:** Alembic Environment Script  
**Dependency Level:** 1  
**Name:** env  
**Type:** Configuration  
**Relative Path:** infrastructure/database/alembic  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DatabaseMigrationEnvironment
    
**Requirement Ids:**
    
    
**Purpose:** Configures the Alembic migration environment, including database connection details and metadata target for autogenerate.  
**Logic Description:** Imports `Base` from `infrastructure.database.base` and sets `target_metadata = Base.metadata`. Configures database URL from application settings (`config.py`). Defines online and offline migration run procedures.  
**Documentation:**
    
    - **Summary:** Alembic script that defines how database migrations are run and configured.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Database
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/database/alembic/script.py.mako  
**Description:** Mako template for generating new Alembic migration scripts.  
**Template:** Alembic Migration Template  
**Dependency Level:** 1  
**Name:** script.py  
**Type:** Template  
**Relative Path:** infrastructure/database/alembic  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DatabaseMigrationScriptTemplate
    
**Requirement Ids:**
    
    
**Purpose:** Provides the template used by Alembic when creating new migration files.  
**Logic Description:** Standard Alembic Mako template containing placeholders for revision IDs, downgrade revision, imports, and `upgrade()` and `downgrade()` functions.  
**Documentation:**
    
    - **Summary:** Template file for Alembic migration scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Database
    
- **Path:** services/auth-service/src/creativeflow/authservice/dependencies.py  
**Description:** Common FastAPI dependency injection functions.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 1  
**Name:** dependencies  
**Type:** Utility  
**Relative Path:**   
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Iterator[Session]  
**Attributes:** public  
    - **Name:** get_redis_client  
**Parameters:**
    
    
**Return Type:** Redis  
**Attributes:** public  
    - **Name:** get_current_user  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** UserSchema  
**Attributes:** public  
    - **Name:** get_notification_service  
**Parameters:**
    
    
**Return Type:** NotificationService  
**Attributes:** public  
    
**Implemented Features:**
    
    - DependencyProvision
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable FastAPI dependencies for database sessions, Redis client, current authenticated user, and other services.  
**Logic Description:** Imports `get_db` from `infrastructure.database.db_config`, `get_redis_client` from `infrastructure.database.redis_config`. `get_current_user` uses `core.security.permissions.get_current_active_user`. `get_notification_service` instantiates a notification service implementation.  
**Documentation:**
    
    - **Summary:** Centralizes common dependencies used across FastAPI route handlers.
    
**Namespace:** CreativeFlow.Services.Auth.Dependencies  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/__init__.py  
**Description:** Initializes the API schemas Python package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for API Pydantic schema modules.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/common_schemas.py  
**Description:** Pydantic schemas for common API responses like success/error messages.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** common_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** MessageResponse  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** ErrorDetail  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** ErrorResponse  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - StandardAPIResponses
    
**Requirement Ids:**
    
    
**Purpose:** Defines common Pydantic models for standardized API responses, such as a generic message or error details.  
**Logic Description:** `MessageResponse` contains a `message: str`. `ErrorDetail` contains `loc: List[str]`, `msg: str`, `type: str`. `ErrorResponse` contains `detail: Union[str, List[ErrorDetail]]`.  
**Documentation:**
    
    - **Summary:** Pydantic models for common API response structures.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/user_schemas.py  
**Description:** Pydantic schemas for user registration, profile, and related operations.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** user_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** UserCreateSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** UserResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** EmailVerificationRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** SocialLoginRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - UserAPIModels
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Defines Pydantic models for user-related API requests (e.g., registration) and responses (e.g., user profile).  
**Logic Description:** `UserCreateSchema` includes email, password. `UserResponseSchema` includes id, email, full_name, is_verified. `EmailVerificationRequestSchema` includes token. `SocialLoginRequestSchema` includes provider, token.  
**Documentation:**
    
    - **Summary:** Pydantic models for user data transfer in API requests and responses.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/token_schemas.py  
**Description:** Pydantic schemas for token-related API responses.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** token_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** TokenResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** RefreshTokenRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - TokenAPIModels
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Defines Pydantic models for API responses containing access and refresh tokens, and requests for token refresh.  
**Logic Description:** `TokenResponseSchema` includes `access_token: str`, `refresh_token: str`, `token_type: str`. `RefreshTokenRequestSchema` includes `refresh_token: str`.  
**Documentation:**
    
    - **Summary:** Pydantic models for JWT access and refresh token responses.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/mfa_schemas.py  
**Description:** Pydantic schemas for MFA setup and verification.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** mfa_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** MFASetupRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** MFASetupResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** MFAVerifyRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** RecoveryCodesResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - MFA_APIModels
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Defines Pydantic models for MFA related API requests (e.g., setup method, verify code) and responses (e.g., TOTP URI, recovery codes).  
**Logic Description:** `MFASetupRequestSchema` includes method (TOTP, SMS, EMAIL). `MFASetupResponseSchema` includes `otp_uri` for TOTP. `MFAVerifyRequestSchema` includes `method`, `code`. `RecoveryCodesResponseSchema` includes `recovery_codes: List[str]`.  
**Documentation:**
    
    - **Summary:** Pydantic models for multi-factor authentication API operations.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/password_schemas.py  
**Description:** Pydantic schemas for password management operations.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** password_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ForgotPasswordRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** ResetPasswordRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** ChangePasswordRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - PasswordManagementAPIModels
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Defines Pydantic models for password reset requests, forgot password initiation, and changing current password.  
**Logic Description:** `ForgotPasswordRequestSchema` includes `email: str`. `ResetPasswordRequestSchema` includes `token: str`, `new_password: str`. `ChangePasswordRequestSchema` includes `current_password: str`, `new_password: str`.  
**Documentation:**
    
    - **Summary:** Pydantic models for user password management API operations.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/session_schemas.py  
**Description:** Pydantic schemas for session management operations.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** session_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SessionResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** ActiveSessionListResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - SessionAPIModels
    
**Requirement Ids:**
    
    - SEC-002
    
**Purpose:** Defines Pydantic models for responses related to active user sessions, e.g., listing active sessions.  
**Logic Description:** `SessionResponseSchema` includes `id: str`, `device_info: str`, `ip_address: str`, `last_activity: datetime`. `ActiveSessionListResponseSchema` includes `sessions: List[SessionResponseSchema]`.  
**Documentation:**
    
    - **Summary:** Pydantic models for API responses related to user session management.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/schemas/auth_schemas.py  
**Description:** Pydantic schemas specific to authentication requests.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 1  
**Name:** auth_schemas  
**Type:** Schema  
**Relative Path:** api/v1/schemas  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** LoginRequestSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** MFAChallengeResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - AuthAPIModels
    
**Requirement Ids:**
    
    - SEC-001
    - REQ-002
    
**Purpose:** Defines Pydantic models for authentication requests, such as login credentials.  
**Logic Description:** `LoginRequestSchema` could inherit from FastAPI's `OAuth2PasswordRequestForm` or define `username` (email) and `password`. `MFAChallengeResponseSchema` might indicate MFA is required and list available methods, or return a temporary token to proceed with MFA verification.  
**Documentation:**
    
    - **Summary:** Pydantic models for user login and MFA challenge responses.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/__init__.py  
**Description:** Initializes the core services Python package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for core application service modules.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/auth_service.py  
**Description:** Core authentication service logic for user login and token handling.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** auth_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** _password_manager  
**Type:** PasswordManager  
**Attributes:** private  
    - **Name:** _token_service  
**Type:** TokenService  
**Attributes:** private  
    - **Name:** _session_service  
**Type:** SessionService  
**Attributes:** private  
    - **Name:** _mfa_service  
**Type:** MFAService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** authenticate_user  
**Parameters:**
    
    - email: str
    - password: str
    - ip_address: str
    - user_agent: str
    
**Return Type:** Tuple[str, str, Optional[User]]  
    - **Name:** logout_user  
**Parameters:**
    
    - refresh_token: str
    - session_id: Optional[str]
    
**Return Type:** None  
    - **Name:** verify_mfa_and_login  
**Parameters:**
    
    - user: User
    - mfa_code: str
    - mfa_method: MFAMethod
    - ip_address: str
    - user_agent: str
    
**Return Type:** Tuple[str, str]  
    
**Implemented Features:**
    
    - UserLogin
    - UserLogout
    - MFAVerificationLogin
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-002
    - REQ-002
    
**Purpose:** Handles user authentication, MFA challenges during login, session creation, and token issuance.  
**Logic Description:** `authenticate_user` fetches user by email, verifies password, checks MFA status. If MFA enabled, raises `MFAChallengeRequiredException`. If not, creates session, generates tokens. `logout_user` revokes refresh token and session. `verify_mfa_and_login` verifies MFA code then proceeds with session and token creation.  
**Documentation:**
    
    - **Summary:** Orchestrates user authentication, MFA handling, and session management during login/logout.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/registration_service.py  
**Description:** Handles user registration, email verification, and social login integration.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** registration_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** _password_manager  
**Type:** PasswordManager  
**Attributes:** private  
    - **Name:** _notification_service  
**Type:** NotificationService  
**Attributes:** private  
    - **Name:** _oauth_service  
**Type:** OAuthService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** register_new_user  
**Parameters:**
    
    - user_create_data: UserCreateSchema
    
**Return Type:** User  
    - **Name:** verify_email_address  
**Parameters:**
    
    - token: str
    
**Return Type:** User  
    - **Name:** resend_verification_email  
**Parameters:**
    
    - email: str
    
**Return Type:** None  
    - **Name:** handle_social_login  
**Parameters:**
    
    - provider: SocialProvider
    - auth_code_or_token: str
    - ip_address: str
    - user_agent: str
    
**Return Type:** Tuple[str, str, User]  
    
**Implemented Features:**
    
    - EmailRegistration
    - SocialLogin
    - EmailVerification
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Manages new user creation via email/password or social providers, and handles the email verification flow.  
**Logic Description:** `register_new_user` checks for existing email, hashes password, creates user, generates verification token, sends verification email. `verify_email_address` validates token and marks user as verified. `handle_social_login` uses `_oauth_service` to get user info from provider, then creates or logs in the user, returning tokens and user object.  
**Documentation:**
    
    - **Summary:** Provides services for user registration through various methods and email verification.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/token_service.py  
**Description:** Service for generating, validating, and refreshing JWTs.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** token_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _jwt_manager  
**Type:** JWTManager  
**Attributes:** private  
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** _token_revocation_repo  
**Type:** TokenRevocationRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** generate_auth_tokens  
**Parameters:**
    
    - user_id: UUID
    - roles: List[str]
    
**Return Type:** Tuple[str, str]  
    - **Name:** refresh_access_token  
**Parameters:**
    
    - refresh_token_str: str
    
**Return Type:** str  
    - **Name:** validate_token_and_get_user  
**Parameters:**
    
    - token_str: str
    
**Return Type:** User  
    - **Name:** revoke_refresh_token  
**Parameters:**
    
    - refresh_token_str: str
    
**Return Type:** None  
    
**Implemented Features:**
    
    - TokenGeneration
    - TokenRefresh
    - TokenValidation
    - TokenRevocation
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Centralizes logic for JWT lifecycle management, including creation, validation, and refresh with rotation strategy.  
**Logic Description:** `generate_auth_tokens` creates access and refresh tokens with user ID and roles. `refresh_access_token` validates the refresh token, checks if revoked, generates a new access token (and potentially a new refresh token for rotation, revoking the old one). `validate_token_and_get_user` decodes token and fetches user. `revoke_refresh_token` adds JTI to blacklist.  
**Documentation:**
    
    - **Summary:** Manages the creation, validation, and refreshing of JWT access and refresh tokens.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/mfa_service.py  
**Description:** Service for managing Multi-Factor Authentication (MFA).  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** mfa_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** _mfa_repo  
**Type:** MFARepository  
**Attributes:** private  
    - **Name:** _otp_service  
**Type:** OTPService  
**Attributes:** private  
    - **Name:** _totp_handler  
**Type:** TOTPHandler  
**Attributes:** private  
    - **Name:** _notification_service  
**Type:** NotificationService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** setup_mfa_method  
**Parameters:**
    
    - user_id: UUID
    - method: MFAMethod
    - value: Optional[str] = None
    
**Return Type:** Union[str, List[str]]  
    - **Name:** verify_mfa_code  
**Parameters:**
    
    - user_id: UUID
    - method: MFAMethod
    - code: str
    
**Return Type:** bool  
    - **Name:** disable_mfa_method  
**Parameters:**
    
    - user_id: UUID
    - method: MFAMethod
    
**Return Type:** None  
    - **Name:** generate_recovery_codes  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[str]  
    - **Name:** verify_recovery_code  
**Parameters:**
    
    - user_id: UUID
    - code: str
    
**Return Type:** bool  
    - **Name:** get_user_mfa_status  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** dict  
    
**Implemented Features:**
    
    - MFASetup
    - MFAVerification
    - RecoveryCodeManagement
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Handles all logic related to MFA: enabling/disabling methods, generating secrets/codes, validating user-provided codes, and managing recovery codes.  
**Logic Description:** `setup_mfa_method` initiates setup for TOTP (returns URI/secret), SMS/Email (sends OTP). `verify_mfa_code` validates OTP for the given method. `generate_recovery_codes` creates and stores hashed recovery codes. `verify_recovery_code` checks a code against stored hashes. `get_user_mfa_status` returns user's configured MFA methods.  
**Documentation:**
    
    - **Summary:** Manages the setup, verification, and recovery processes for multi-factor authentication.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/password_service.py  
**Description:** Service for password management operations like reset and change.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** password_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** _password_manager  
**Type:** PasswordManager  
**Attributes:** private  
    - **Name:** _notification_service  
**Type:** NotificationService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** request_password_reset  
**Parameters:**
    
    - email: str
    
**Return Type:** None  
    - **Name:** reset_password  
**Parameters:**
    
    - token: str
    - new_password: str
    
**Return Type:** None  
    - **Name:** change_password  
**Parameters:**
    
    - user_id: UUID
    - current_password: str
    - new_password: str
    
**Return Type:** None  
    
**Implemented Features:**
    
    - PasswordReset
    - PasswordChange
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Handles password reset requests, validation of reset tokens, and secure changing of user passwords.  
**Logic Description:** `request_password_reset` generates a reset token, stores it with expiry, and sends reset email. `reset_password` validates token, updates user's password. `change_password` verifies current password then updates to new password.  
**Documentation:**
    
    - **Summary:** Provides services for user password reset and change functionalities.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/session_service.py  
**Description:** Manages user sessions, including creation, validation, revocation, and device tracking, using Redis.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** session_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _session_repo  
**Type:** SessionRepository  
**Attributes:** private  
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    - **Name:** SESSION_TTL_SECONDS  
**Type:** int  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_session  
**Parameters:**
    
    - user_id: UUID
    - ip_address: str
    - user_agent: str
    
**Return Type:** str  
    - **Name:** get_session_data  
**Parameters:**
    
    - session_id: str
    
**Return Type:** Optional[dict]  
    - **Name:** revoke_session  
**Parameters:**
    
    - session_id: str
    
**Return Type:** None  
    - **Name:** revoke_all_user_sessions  
**Parameters:**
    
    - user_id: UUID
    - except_session_id: Optional[str] = None
    
**Return Type:** None  
    - **Name:** list_user_sessions  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[dict]  
    - **Name:** update_session_activity  
**Parameters:**
    
    - session_id: str
    
**Return Type:** None  
    
**Implemented Features:**
    
    - SessionManagement
    - DeviceTracking
    - ConcurrentSessionControl
    
**Requirement Ids:**
    
    - SEC-002
    
**Purpose:** Handles the lifecycle of user sessions stored in Redis, including tracking active devices and supporting revocation.  
**Logic Description:** `create_session` generates a session ID, stores session data in Redis with TTL. `get_session_data` retrieves session. `revoke_session` deletes session from Redis. `revoke_all_user_sessions` iterates and deletes. `list_user_sessions` fetches all active sessions for a user. Implements concurrent session limits by checking count before creating a new one.  
**Documentation:**
    
    - **Summary:** Manages user sessions stored in Redis, providing creation, validation, and revocation capabilities.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/user_service.py  
**Description:** Service for user-related operations not directly tied to authentication flows (e.g., fetching profile data).  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** user_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _user_repo  
**Type:** UserRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_user_by_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** Optional[User]  
    - **Name:** get_user_by_email  
**Parameters:**
    
    - email: str
    
**Return Type:** Optional[User]  
    - **Name:** update_user_last_login  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** None  
    
**Implemented Features:**
    
    - UserLookup
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Provides methods to retrieve and update user information relevant to the authentication service context.  
**Logic Description:** Wrapper around `UserRepository` methods. `get_user_by_id` and `get_user_by_email` fetch user details. `update_user_last_login` updates the last login timestamp.  
**Documentation:**
    
    - **Summary:** Handles retrieval and basic updates of user data needed by the authentication service.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/otp_service.py  
**Description:** Service for generating and verifying One-Time Passwords (OTPs).  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** otp_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _redis_client  
**Type:** Redis  
**Attributes:** private  
    - **Name:** OTP_TTL_SECONDS  
**Type:** int  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** generate_and_store_otp  
**Parameters:**
    
    - key_prefix: str
    - identifier: str
    
**Return Type:** str  
    - **Name:** verify_otp  
**Parameters:**
    
    - key_prefix: str
    - identifier: str
    - otp_code: str
    
**Return Type:** bool  
    
**Implemented Features:**
    
    - OTPGeneration
    - OTPVerification
    - OTPStorage
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Manages the lifecycle of OTPs used for email or SMS MFA, including generation, temporary storage (in Redis), and verification.  
**Logic Description:** `generate_and_store_otp` uses `token_generator.generate_otp_code`, stores it in Redis with a specific key (e.g., `otp:email_mfa:<user_id>`) and TTL. `verify_otp` retrieves OTP from Redis, compares with user input, and deletes if matched.  
**Documentation:**
    
    - **Summary:** Provides services for generating, storing, and verifying One-Time Passwords.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/core/services/oauth_service.py  
**Description:** Service for handling OAuth 2.0/OpenID Connect social logins.  
**Template:** Python Service Module  
**Dependency Level:** 2  
**Name:** oauth_service  
**Type:** Service  
**Relative Path:** core/services  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    - AdapterPattern
    
**Members:**
    
    - **Name:** _http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_social_user_info  
**Parameters:**
    
    - provider: SocialProvider
    - token_or_code: str
    
**Return Type:** dict  
    
**Implemented Features:**
    
    - SocialUserInfoRetrieval
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Interacts with social identity providers (Google, Facebook, Apple) to exchange authorization codes/tokens for user information.  
**Logic Description:** `get_social_user_info` takes provider and token/code. Based on provider, it calls the respective IdP's user info endpoint (e.g., Google's People API) using `httpx` to fetch user details (email, name, provider ID). Handles IdP-specific logic and error responses. Uses client IDs/secrets from config.  
**Documentation:**
    
    - **Summary:** Handles communication with external OAuth2/OIDC providers to retrieve user information for social logins.
    
**Namespace:** CreativeFlow.Services.Auth.Core.Services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/repositories/__init__.py  
**Description:** Initializes the repositories Python package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/repositories  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for data repository implementation modules.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/repositories/user_repository.py  
**Description:** SQLAlchemy repository implementation for user data.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** user_repository  
**Type:** Repository  
**Relative Path:** infrastructure/repositories  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _db  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_user  
**Parameters:**
    
    - user_data: UserCreateSchema
    
**Return Type:** User  
    - **Name:** get_user_by_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** Optional[User]  
    - **Name:** get_user_by_email  
**Parameters:**
    
    - email: str
    
**Return Type:** Optional[User]  
    - **Name:** get_user_by_social_id  
**Parameters:**
    
    - provider: SocialProvider
    - social_id: str
    
**Return Type:** Optional[User]  
    - **Name:** update_user  
**Parameters:**
    
    - user: User
    - update_data: dict
    
**Return Type:** User  
    - **Name:** add_role_to_user  
**Parameters:**
    
    - user: User
    - role_name: str
    
**Return Type:** None  
    
**Implemented Features:**
    
    - UserCRUD
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-003
    - NFR-006
    
**Purpose:** Implements data access logic for `User` entities using SQLAlchemy, interacting with the PostgreSQL database.  
**Logic Description:** Uses SQLAlchemy session (`_db`) to perform CRUD operations on `UserModel`. Handles querying by ID, email, social ID. `update_user` applies changes and commits. `add_role_to_user` finds or creates role and associates it. Manages relationships like roles, MFA factors.  
**Documentation:**
    
    - **Summary:** Provides database interaction methods for user account data.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/repositories/mfa_repository.py  
**Description:** SQLAlchemy repository for MFA factor and recovery code data.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** mfa_repository  
**Type:** Repository  
**Relative Path:** infrastructure/repositories  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _db  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** add_mfa_factor  
**Parameters:**
    
    - user_id: UUID
    - method: MFAMethod
    - data: dict
    
**Return Type:** MFAModel  
    - **Name:** get_mfa_factors_for_user  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[MFAModel]  
    - **Name:** get_mfa_factor_by_method  
**Parameters:**
    
    - user_id: UUID
    - method: MFAMethod
    
**Return Type:** Optional[MFAModel]  
    - **Name:** update_mfa_factor  
**Parameters:**
    
    - mfa_factor: MFAModel
    - update_data: dict
    
**Return Type:** MFAModel  
    - **Name:** add_recovery_codes  
**Parameters:**
    
    - user_id: UUID
    - hashed_codes: List[str]
    
**Return Type:** None  
    - **Name:** find_and_use_recovery_code  
**Parameters:**
    
    - user_id: UUID
    - hashed_code_attempt: str
    
**Return Type:** bool  
    
**Implemented Features:**
    
    - MFACRUD
    - RecoveryCodeCRUD
    
**Requirement Ids:**
    
    - REQ-002
    - NFR-006
    
**Purpose:** Manages persistence of MFA configurations and recovery codes in the database.  
**Logic Description:** Uses SQLAlchemy session for CRUD operations on `MFAModel` and `RecoveryCodeModel`. Handles storing encrypted secrets/phone numbers. `find_and_use_recovery_code` searches for a hashed code and marks it as used if found.  
**Documentation:**
    
    - **Summary:** Data access layer for MFA factors and recovery codes.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/repositories/session_repository.py  
**Description:** Redis repository for managing user sessions.  
**Template:** Python Redis Repository  
**Dependency Level:** 2  
**Name:** session_repository  
**Type:** Repository  
**Relative Path:** infrastructure/repositories  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _redis  
**Type:** Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** store_session  
**Parameters:**
    
    - session_id: str
    - user_id: UUID
    - data: dict
    - ttl_seconds: int
    
**Return Type:** None  
    - **Name:** get_session  
**Parameters:**
    
    - session_id: str
    
**Return Type:** Optional[dict]  
    - **Name:** delete_session  
**Parameters:**
    
    - session_id: str
    
**Return Type:** None  
    - **Name:** get_user_sessions  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[dict]  
    - **Name:** update_session_ttl  
**Parameters:**
    
    - session_id: str
    - ttl_seconds: int
    
**Return Type:** None  
    
**Implemented Features:**
    
    - SessionStorageRedis
    
**Requirement Ids:**
    
    - SEC-002
    
**Purpose:** Implements session storage and retrieval using Redis, including TTL management for session expiry.  
**Logic Description:** Uses Redis client to store session data (e.g., user_id, device_info, ip_address) keyed by session ID, with an expiry time. `get_user_sessions` might use a secondary index in Redis (e.g., a set of session IDs per user) or scan keys (less ideal).  
**Documentation:**
    
    - **Summary:** Provides Redis-backed storage for user session data.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/repositories/token_revocation_repository.py  
**Description:** Repository for managing revoked tokens (e.g., refresh tokens, blacklisted access tokens).  
**Template:** Python Redis/DB Repository  
**Dependency Level:** 2  
**Name:** token_revocation_repository  
**Type:** Repository  
**Relative Path:** infrastructure/repositories  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _redis  
**Type:** Optional[Redis]  
**Attributes:** private  
    - **Name:** _db  
**Type:** Optional[Session]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** add_to_blacklist  
**Parameters:**
    
    - jti: str
    - expires_at: datetime
    
**Return Type:** None  
    - **Name:** is_blacklisted  
**Parameters:**
    
    - jti: str
    
**Return Type:** bool  
    
**Implemented Features:**
    
    - TokenBlacklisting
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Manages a blacklist of revoked token identifiers (JTIs) to prevent their reuse, primarily using Redis for performance with TTL.  
**Logic Description:** `add_to_blacklist` stores the JTI in Redis with a TTL equal to the original token's remaining validity. `is_blacklisted` checks if JTI exists in Redis. Could also use a DB table (`TokenRevocationModel`) for longer-term storage if Redis is volatile, but Redis is preferred for speed.  
**Documentation:**
    
    - **Summary:** Handles storage and checking of revoked token identifiers.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/notifications/__init__.py  
**Description:** Initializes the notifications infrastructure Python package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/notifications  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for notification service implementations.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Notifications  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/notifications/email_service.py  
**Description:** Concrete implementation for sending emails (e.g., via SMTP or an email API).  
**Template:** Python Service Implementation  
**Dependency Level:** 2  
**Name:** email_service  
**Type:** ServiceImplementation  
**Relative Path:** infrastructure/notifications  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _settings  
**Type:** Settings  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send_email  
**Parameters:**
    
    - to_email: str
    - subject: str
    - html_content: str
    
**Return Type:** Awaitable[None]  
**Attributes:** public  
    
**Implemented Features:**
    
    - EmailSending
    
**Requirement Ids:**
    
    - REQ-001
    - REQ-002
    
**Purpose:** Implements the `NotificationService` interface for sending emails. Uses settings from `config.py` for SMTP server details or email API keys.  
**Logic Description:** Implements `send_email` method from `NotificationService` interface. Uses `smtplib` for SMTP or a third-party library like `httpx` to call an email API service (e.g., SendGrid, Mailgun) based on configuration.  
**Documentation:**
    
    - **Summary:** Provides email sending functionality, implementing the NotificationService interface.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Notifications  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** services/auth-service/src/creativeflow/authservice/infrastructure/notifications/sms_service.py  
**Description:** Concrete implementation for sending SMS messages (e.g., via Twilio).  
**Template:** Python Service Implementation  
**Dependency Level:** 2  
**Name:** sms_service  
**Type:** ServiceImplementation  
**Relative Path:** infrastructure/notifications  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _settings  
**Type:** Settings  
**Attributes:** private  
    - **Name:** _twilio_client  
**Type:** Optional[TwilioClient]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send_sms  
**Parameters:**
    
    - to_phone: str
    - message: str
    
**Return Type:** Awaitable[None]  
**Attributes:** public  
    
**Implemented Features:**
    
    - SMSSending
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Implements the `NotificationService` interface for sending SMS messages. Uses settings for SMS provider credentials.  
**Logic Description:** Implements `send_sms` method from `NotificationService` interface. Uses a third-party SMS gateway library (e.g., Twilio Python SDK) and credentials from `config.py`.  
**Documentation:**
    
    - **Summary:** Provides SMS sending functionality, implementing the NotificationService interface.
    
**Namespace:** CreativeFlow.Services.Auth.Infrastructure.Notifications  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/__init__.py  
**Description:** Initializes the API Python package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for API related modules.
    
**Namespace:** CreativeFlow.Services.Auth.API  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/__init__.py  
**Description:** Initializes the API v1 Python package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for API version 1.  
**Logic Description:** Empty file. May import all routers for easier inclusion in `main.py`.  
**Documentation:**
    
    - **Summary:** Package initializer for version 1 of the API.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/__init__.py  
**Description:** Initializes the API routers Python package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Empty file.  
**Documentation:**
    
    - **Summary:** Package initializer for FastAPI router modules.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/auth_router.py  
**Description:** FastAPI router for authentication endpoints (login, logout, refresh token).  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** auth_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    - MVCPattern (Controller)
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** login_for_access_token  
**Parameters:**
    
    - form_data: OAuth2PasswordRequestForm = Depends()
    - db: Session = Depends(get_db_session)
    - redis: Redis = Depends(get_redis_client)
    - request: Request
    
**Return Type:** TokenResponseSchema  
**Attributes:** public|async  
    - **Name:** refresh_token  
**Parameters:**
    
    - refresh_token_data: RefreshTokenRequestSchema
    - db: Session = Depends(get_db_session)
    - redis: Redis = Depends(get_redis_client)
    
**Return Type:** TokenResponseSchema  
**Attributes:** public|async  
    - **Name:** logout  
**Parameters:**
    
    - refresh_token_data: RefreshTokenRequestSchema
    - db: Session = Depends(get_db_session)
    - redis: Redis = Depends(get_redis_client)
    - request: Request
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - UserLoginAPI
    - TokenRefreshAPI
    - UserLogoutAPI
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-002
    
**Purpose:** Defines API endpoints for user login, token refresh, and logout. Interacts with `AuthService` and `TokenService`.  
**Logic Description:** `/login` endpoint takes username/password, calls `AuthService.authenticate_user`, sets secure cookies for tokens. `/refresh` takes refresh token, calls `TokenService.refresh_access_token`. `/logout` calls `AuthService.logout_user`, clears cookies.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for user authentication, token management, and logout.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/registration_router.py  
**Description:** FastAPI router for user registration and email verification endpoints.  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** registration_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** register_user  
**Parameters:**
    
    - user_in: UserCreateSchema
    - db: Session = Depends(get_db_session)
    
**Return Type:** UserResponseSchema  
**Attributes:** public|async  
    - **Name:** verify_email  
**Parameters:**
    
    - token_data: EmailVerificationRequestSchema
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** resend_verification_email_endpoint  
**Parameters:**
    
    - email_data: dict
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** social_login_endpoint  
**Parameters:**
    
    - provider: str
    - social_data: SocialLoginRequestSchema
    - db: Session = Depends(get_db_session)
    - redis: Redis = Depends(get_redis_client)
    - request: Request
    
**Return Type:** TokenResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - UserRegistrationAPI
    - EmailVerificationAPI
    - SocialLoginAPI
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Defines API endpoints for new user registration (email/social) and email verification processes. Uses `RegistrationService`.  
**Logic Description:** `/register` takes user data, calls `RegistrationService.register_new_user`. `/verify-email` takes token, calls `RegistrationService.verify_email_address`. `/social-login/{provider}` handles social login callback/token, calls `RegistrationService.handle_social_login`.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for user registration and email verification flows.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/mfa_router.py  
**Description:** FastAPI router for MFA setup, verification, and recovery code management.  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** mfa_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** setup_mfa  
**Parameters:**
    
    - mfa_setup_data: MFASetupRequestSchema
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** MFASetupResponseSchema  
**Attributes:** public|async  
    - **Name:** verify_mfa_setup  
**Parameters:**
    
    - mfa_verify_data: MFAVerifyRequestSchema
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** disable_mfa  
**Parameters:**
    
    - mfa_method_data: dict
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** get_recovery_codes  
**Parameters:**
    
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** RecoveryCodesResponseSchema  
**Attributes:** public|async  
    - **Name:** verify_mfa_login_challenge  
**Parameters:**
    
    - mfa_verify_data: MFAVerifyRequestSchema
    - temp_auth_token: str
    - db: Session = Depends(get_db_session)
    - redis: Redis = Depends(get_redis_client)
    - request: Request
    
**Return Type:** TokenResponseSchema  
**Attributes:** public|async  
    - **Name:** get_mfa_status  
**Parameters:**
    
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - MFASetupAPI
    - MFAVerificationAPI
    - RecoveryCodeAPI
    
**Requirement Ids:**
    
    - REQ-002
    
**Purpose:** Defines API endpoints for users to manage their MFA settings. Uses `MFAService`.  
**Logic Description:** Endpoints for setting up MFA methods (e.g., `/mfa/setup/totp`), verifying codes (`/mfa/verify`), disabling methods, and retrieving/generating recovery codes. Endpoints are protected by `get_current_user` dependency.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for managing multi-factor authentication settings.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/password_router.py  
**Description:** FastAPI router for password management (forgot password, reset password, change password).  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** password_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** forgot_password  
**Parameters:**
    
    - forgot_password_data: ForgotPasswordRequestSchema
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** reset_password_with_token  
**Parameters:**
    
    - reset_password_data: ResetPasswordRequestSchema
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** change_current_password  
**Parameters:**
    
    - change_password_data: ChangePasswordRequestSchema
    - current_user: User = Depends(get_current_user)
    - db: Session = Depends(get_db_session)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - PasswordManagementAPI
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** Defines API endpoints for user password management flows. Uses `PasswordService`.  
**Logic Description:** `/password/forgot` initiates password reset. `/password/reset` allows setting new password with token. `/password/change` allows authenticated user to change their password.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for user password management functionalities.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/session_router.py  
**Description:** FastAPI router for managing user sessions (list active sessions, revoke sessions).  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** session_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** list_active_sessions  
**Parameters:**
    
    - current_user: User = Depends(get_current_user)
    - redis: Redis = Depends(get_redis_client)
    
**Return Type:** ActiveSessionListResponseSchema  
**Attributes:** public|async  
    - **Name:** revoke_session_by_id  
**Parameters:**
    
    - session_id: str
    - current_user: User = Depends(get_current_user)
    - redis: Redis = Depends(get_redis_client)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    - **Name:** revoke_all_other_sessions  
**Parameters:**
    
    - current_user: User = Depends(get_current_user)
    - request: Request
    - redis: Redis = Depends(get_redis_client)
    
**Return Type:** MessageResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - SessionManagementAPI
    - DeviceTrackingAPI
    
**Requirement Ids:**
    
    - SEC-002
    
**Purpose:** Defines API endpoints for users to view and manage their active sessions. Uses `SessionService`.  
**Logic Description:** `/sessions` (GET) lists active sessions. `/sessions/{session_id}` (DELETE) revokes a specific session. `/sessions/revoke-all-others` (POST) revokes all sessions except the current one. Protected by `get_current_user`.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for viewing and managing active user sessions.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/auth-service/src/creativeflow/authservice/api/v1/routers/user_router.py  
**Description:** FastAPI router for fetching current user information.  
**Template:** Python FastAPI Router  
**Dependency Level:** 3  
**Name:** user_router  
**Type:** Controller  
**Relative Path:** api/v1/routers  
**Repository Id:** REPO-AUTH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** read_users_me  
**Parameters:**
    
    - current_user: UserResponseSchema = Depends(get_current_user)
    
**Return Type:** UserResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - CurrentUserAPI
    
**Requirement Ids:**
    
    - REQ-001
    
**Purpose:** Defines API endpoint for authenticated users to retrieve their own profile information.  
**Logic Description:** `/users/me` endpoint, protected by `get_current_user` dependency, returns the current authenticated user's details.  
**Documentation:**
    
    - **Summary:** Provides an API endpoint for authenticated users to fetch their own information.
    
**Namespace:** CreativeFlow.Services.Auth.API.v1.Routers  
**Metadata:**
    
    - **Category:** API
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableSocialLoginGoogle
  - EnableSocialLoginFacebook
  - EnableSocialLoginApple
  - EnableMFA_SMS
  - EnableMFA_AuthenticatorApp
  - EnableMFA_EmailOTP
  - EnableProgressiveProfilingTrigger
  
- **Database Configs:**
  
  - DATABASE_URL
  - REDIS_URL
  - JWT_SECRET_KEY
  - JWT_ALGORITHM
  - ACCESS_TOKEN_EXPIRE_MINUTES
  - REFRESH_TOKEN_EXPIRE_DAYS
  - EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS
  - PASSWORD_RESET_TOKEN_EXPIRE_HOURS
  - MFA_OTP_EXPIRE_SECONDS
  - TOTP_ISSUER_NAME
  - CONCURRENT_SESSION_LIMIT
  - SOCIAL_GOOGLE_CLIENT_ID
  - SOCIAL_GOOGLE_CLIENT_SECRET
  - SOCIAL_GOOGLE_REDIRECT_URI
  - SOCIAL_FACEBOOK_CLIENT_ID
  - SOCIAL_FACEBOOK_CLIENT_SECRET
  - SOCIAL_FACEBOOK_REDIRECT_URI
  - SOCIAL_APPLE_CLIENT_ID
  - SOCIAL_APPLE_TEAM_ID
  - SOCIAL_APPLE_KEY_ID
  - SOCIAL_APPLE_PRIVATE_KEY
  - EMAIL_HOST
  - EMAIL_PORT
  - EMAIL_USERNAME
  - EMAIL_PASSWORD
  - EMAIL_USE_TLS
  - EMAIL_FROM_ADDRESS
  - SMS_PROVIDER_API_KEY
  - SMS_PROVIDER_SENDER_ID
  


---

