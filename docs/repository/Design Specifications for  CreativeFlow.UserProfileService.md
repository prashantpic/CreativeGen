# Software Design Specification: CreativeFlow.UserProfileService

## 1. Introduction

This document outlines the software design for the `CreativeFlow.UserProfileService`, a microservice responsible for managing user profiles, preferences, consent, and data privacy compliance features within the CreativeFlow AI platform. It interacts with other services and a PostgreSQL database.

### 1.1. Purpose

The UserProfileService provides a centralized way to manage detailed user information beyond basic authentication, enabling personalized experiences and ensuring compliance with data privacy regulations like GDPR and CCPA.

### 1.2. Scope

This service is responsible for:
*   Creating, reading, updating, and deleting user profile data (e.g., full name, username, profile picture URL).
*   Managing user preferences (e.g., language, timezone, UI settings).
*   Handling user consent for various data processing activities.
*   Implementing data subject rights requests (access, portability, erasure).
*   Orchestrating data retention policies for user profile data.
*   Exposing internal REST APIs for these functionalities.

This service does **not** handle:
*   User authentication (passwords, MFA, social login connections - handled by Auth Service).
*   Subscription or billing management (handled by Odoo/Billing Service, though it might display some related info).
*   Brand Kit management, Project/Asset management (handled by Creative Management Service).

### 1.3. Acronyms and Abbreviations

*   **API**: Application Programming Interface
*   **CRUD**: Create, Read, Update, Delete
*   **DB**: Database
*   **DTO**: Data Transfer Object
*   **GDPR**: General Data Protection Regulation
*   **CCPA**: California Consumer Privacy Act
*   **CPRA**: California Privacy Rights Act
*   **HTTP**: Hypertext Transfer Protocol
*   **JWT**: JSON Web Token
*   **ORM**: Object-Relational Mapping
*   **PWA**: Progressive Web Application
*   **SDS**: Software Design Specification
*   **SRS**: Software Requirements Specification
*   **TS**: TypeScript
*   **UUID**: Universally Unique Identifier

## 2. System Overview

The UserProfileService is a Python FastAPI-based microservice. It follows a layered architecture (Domain, Application, Adapters/Infrastructure). It persists data in a PostgreSQL database using SQLAlchemy and interacts with other services as needed (e.g., potentially an Auth service for user ID validation or an event bus for inter-service communication).

**Key Dependencies:**
*   `REPO-POSTGRES-DB-001`: For storing profile, consent, and privacy request data.
*   `REPO-AUTH-SERVICE-001`: Relies on `auth_user_id` provided by the Auth service after user authentication. May subscribe to user deletion events.
*   `REPO-SHARED-LIBS-001`: For common utilities, base classes, or shared DTOs/schemas if applicable.

## 3. Design Considerations

*   **Data Privacy by Design:** All functionalities handling personal data are designed with GDPR/CCPA principles in mind.
*   **Scalability:** The service is designed to be scalable, leveraging FastAPI's asynchronous capabilities and efficient database interaction.
*   **Maintainability:** A layered architecture with clear separation of concerns is used.
*   **Testability:** Design emphasizes dependency injection and abstract repositories to facilitate unit and integration testing.
*   **Security:** Sensitive data is handled with care, and interactions are secured. This service assumes an `auth_user_id` from a validated JWT, typically handled by an API Gateway or Auth Service.

## 4. Detailed Component Design

This section details the design for each file defined in the repository's file structure.

---

### 4.1. `src/creativeflow/services/userprofile/__init__.py`
*   **Purpose:** Initializes the `creativeflow.services.userprofile` Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** This file will be empty or may contain top-level imports for convenience if needed by other modules importing from this package.
    python
    # creativeflow/services/userprofile/__init__.py
    # This file can be left empty or used for package-level imports.
    
*   **ImplementedFeatures:** PackageInitialization

---

### 4.2. `src/creativeflow/services/userprofile/main.py`
*   **Purpose:** Main application file. Initializes the FastAPI application, includes routers, and sets up middleware and lifespan events.
*   **Type:** ApplicationEntrypoint
*   **Key Components:**
    *   `app: FastAPI`: The main FastAPI application instance.
*   **Methods:**
    *   `startup_event()`: `async def startup_event():`
        *   **Logic:** Establishes database connection pool (e.g., using `database.init_db()`). Sets up logging. Initializes any other resources needed at startup.
    *   `shutdown_event()`: `async def shutdown_event():`
        *   **Logic:** Closes database connection pool. Cleans up any other resources.
    *   `create_application() -> FastAPI`: (Helper function to encapsulate app creation logic)
        *   **Logic:**
            1.  Instantiate `FastAPI()`.
            2.  Set up CORS middleware if requests are expected directly from browsers not via a gateway handling CORS.
                python
                from fastapi.middleware.cors import CORSMiddleware
                # ... origins list ...
                app.add_middleware(
                    CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                
            3.  Include API routers from `adapters.api.v1.routers`.
                python
                from .adapters.api.v1.routers import user_profiles_router, data_privacy_router, consent_router
                app.include_router(user_profiles_router.router, prefix="/api/v1/userprofiles", tags=["User Profiles"])
                app.include_router(data_privacy_router.router, prefix="/api/v1/privacy", tags=["Data Privacy"])
                app.include_router(consent_router.router, prefix="/api/v1/consents", tags=["User Consents"])
                
            4.  Register `startup_event` and `shutdown_event` lifespan events.
            5.  Set up global exception handlers (e.g., for custom domain or application exceptions, mapping them to appropriate HTTP responses).
                python
                from fastapi import Request, status
                from fastapi.responses import JSONResponse
                from .domain.exceptions import ProfileNotFoundError # Example

                @app.exception_handler(ProfileNotFoundError)
                async def profile_not_found_exception_handler(request: Request, exc: ProfileNotFoundError):
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={"message": str(exc)},
                    )
                
            6.  Return the `app` instance.
*   **LogicDescription:**
    *   Import `FastAPI`.
    *   Import routers from `creativeflow.services.userprofile.adapters.api.v1.routers`.
    *   Import `logging_config` and call `setup_logging`.
    *   Import database setup from `creativeflow.services.userprofile.adapters.db.database`.
    *   The main execution block (`if __name__ == "__main__":`) will use `uvicorn` to run the app (typically for local development).
*   **ImplementedFeatures:** ServiceInitialization, APIRouting, MiddlewareConfiguration
*   **RequirementIds:** `REQ-004`, `SEC-004`

---

### 4.3. `src/creativeflow/services/userprofile/config.py`
*   **Purpose:** Defines and loads environment-specific configurations.
*   **Type:** Configuration
*   **Key Components:**
    *   `Settings(BaseSettings)`: Pydantic class for settings.
        *   `DATABASE_URL: str` (e.g., `postgresql+asyncpg://user:pass@host:port/db`)
        *   `AUTH_SERVICE_URL: Optional[str] = None` (If direct calls to Auth service are needed for user validation)
        *   `LOG_LEVEL: str = "INFO"`
        *   `ENVIRONMENT: str = "development"`
        *   `API_V1_STR: str = "/api/v1"`
        *   `PROJECT_NAME: str = "UserProfile Service"`
        *   (Other settings as needed, e.g., secrets for external service calls, though preferably managed by a secrets manager)
    *   `get_settings() -> Settings`: Cached function to retrieve settings.
        python
        from functools import lru_cache
        from pydantic_settings import BaseSettings, SettingsConfigDict

        class Settings(BaseSettings):
            DATABASE_URL: str
            AUTH_SERVICE_URL: str | None = None
            LOG_LEVEL: str = "INFO"
            ENVIRONMENT: str = "development"
            API_V1_STR: str = "/api/v1"
            PROJECT_NAME: str = "UserProfile Service"

            model_config = SettingsConfigDict(env_file=".env", extra="ignore")

        @lru_cache()
        def get_settings() -> Settings:
            return Settings()
        
*   **ImplementedFeatures:** ConfigurationManagement

---

### 4.4. `src/creativeflow/services/userprofile/logging_config.py`
*   **Purpose:** Sets up application-wide structured logging.
*   **Type:** Configuration
*   **Methods:**
    *   `setup_logging(log_level: str)`:
        *   **Logic:**
            *   Use Python's `logging` module.
            *   Configure a JSON formatter (e.g., using `python-json-logger`) to output logs in a structured format suitable for centralized log aggregation.
            *   Include standard fields like timestamp, level, message, logger name, and allow for extra fields (e.g., `correlation_id`).
            *   Set the root logger level based on `log_level` from config.
            *   Example basic setup:
            python
            import logging
            import sys
            # from pythonjsonlogger import jsonlogger # If using python-json-logger

            def setup_logging(log_level: str = "INFO"):
                # For structured logging, a more robust setup would use python-json-logger
                # For simplicity, a basic configuration:
                logging.basicConfig(
                    level=getattr(logging, log_level.upper(), logging.INFO),
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    stream=sys.stdout,
                )
                # Example with python-json-logger:
                # logger = logging.getLogger()
                # log_handler = logging.StreamHandler()
                # formatter = jsonlogger.JsonFormatter(
                #     fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
                # )
                # log_handler.setFormatter(formatter)
                # logger.addHandler(log_handler)
                # logger.setLevel(log_level.upper())
                logging.info(f"Logging configured with level: {log_level}")
            
*   **ImplementedFeatures:** StructuredLogging

---

### 4.5. Domain Layer (`src/creativeflow/services/userprofile/domain/`)

#### 4.5.1. `domain/__init__.py`
*   **Purpose:** Marks the `domain` directory as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

#### 4.5.2. `domain/models/__init__.py`
*   **Purpose:** Marks the `models` directory as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** May import key domain models for easier access from other domain modules.
    python
    # creativeflow/services/userprofile/domain/models/__init__.py
    from .user_profile import UserProfile, Preferences
    from .consent import Consent
    from .data_privacy import DataPrivacyRequest, RetentionRule

    __all__ = ["UserProfile", "Preferences", "Consent", "DataPrivacyRequest", "RetentionRule"]
    

#### 4.5.3. `domain/models/user_profile.py`
*   **Purpose:** Defines the UserProfile and Preferences domain models.
*   **Type:** DomainModel (Entity and Value Object)
*   **Key Components:**
    *   `Preferences(BaseModel)`: (Value Object)
        *   `language_preference: str = Field(default="en-US", max_length=10)`
        *   `timezone: str = Field(default="UTC", max_length=50)`
        *   `ui_settings: dict = Field(default_factory=dict)` (For UI settings like default formats, potentially validated with a more specific Pydantic model if structure is complex)
    *   `UserProfile(BaseModel)`: (Entity)
        *   `id: UUID = Field(default_factory=uuid.uuid4)`
        *   `auth_user_id: str = Field(..., description="Identifier from Auth service, unique")`
        *   `full_name: Optional[str] = Field(None, max_length=100)`
        *   `username: Optional[str] = Field(None, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")`
        *   `profile_picture_url: Optional[HttpUrl] = None`
        *   `preferences: Preferences = Field(default_factory=Preferences)`
        *   `created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))`
        *   `updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))`
        *   `last_activity_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))` (For retention policy)
        *   `is_anonymized: bool = False`
*   **Methods (within `UserProfile`):**
    *   `update_details(self, full_name: Optional[str] = None, username: Optional[str] = None, profile_picture_url: Optional[HttpUrl] = None)`:
        *   **Logic:** Updates profile fields if new values are provided. Sets `updated_at`.
    *   `update_preferences(self, language_preference: Optional[str] = None, timezone: Optional[str] = None, ui_settings: Optional[dict] = None)`:
        *   **Logic:** Updates preference fields. Sets `updated_at`.
    *   `anonymize(self)`:
        *   **Logic:** Sets PII fields (full_name, username, profile_picture_url, specific preferences if PII) to placeholder values (e.g., "ANONYMIZED_USER"). Sets `is_anonymized = True`. Sets `updated_at`.
    *   `record_activity(self)`:
        *   **Logic:** Updates `last_activity_at` to current UTC time. Sets `updated_at`.
*   **ImplementedFeatures:** UserProfileDefinition, UserPreferencesDefinition
*   **RequirementIds:** `REQ-004`, `Section 3.1.2`, `Section 7.1.1`

#### 4.5.4. `domain/models/consent.py`
*   **Purpose:** Defines the Consent domain model.
*   **Type:** DomainModel (Entity)
*   **Key Components:**
    *   `ConsentType(str, Enum)`:
        *   `MARKETING_EMAILS = "marketing_emails"`
        *   `DATA_ANALYTICS = "data_analytics"`
        *   `BETA_PROGRAM = "beta_program"`
        *   (Add other consent types as needed)
    *   `Consent(BaseModel)`: (Entity)
        *   `id: UUID = Field(default_factory=uuid.uuid4)`
        *   `auth_user_id: str`
        *   `consent_type: ConsentType`
        *   `is_granted: bool = False`
        *   `version: str` (e.g., "privacy_policy_v1.2", "terms_v2.0")
        *   `timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))`
*   **Methods (within `Consent`):**
    *   `grant(self, version: str)`:
        *   **Logic:** Sets `is_granted = True`, `version = version`, `timestamp = datetime.now(timezone.utc)`.
    *   `withdraw(self)`:
        *   **Logic:** Sets `is_granted = False`, `timestamp = datetime.now(timezone.utc)`.
*   **ImplementedFeatures:** ConsentDefinition, ConsentStateManagement
*   **RequirementIds:** `SEC-004` (UAPM-1-009)

#### 4.5.5. `domain/models/data_privacy.py`
*   **Purpose:** Defines domain models for data privacy requests and retention.
*   **Type:** DomainModel (Entity, Value Object)
*   **Key Components:**
    *   `DataPrivacyRequestType(str, Enum)`:
        *   `ACCESS = "access"`
        *   `PORTABILITY = "portability"`
        *   `DELETION = "deletion"`
        *   `RECTIFICATION = "rectification"`
    *   `DataPrivacyRequestStatus(str, Enum)`:
        *   `PENDING = "pending"`
        *   `PROCESSING = "processing"`
        *   `COMPLETED = "completed"`
        *   `FAILED = "failed"`
        *   `CANCELLED = "cancelled"`
    *   `DataPrivacyRequest(BaseModel)`: (Entity)
        *   `id: UUID = Field(default_factory=uuid.uuid4)`
        *   `auth_user_id: str`
        *   `request_type: DataPrivacyRequestType`
        *   `status: DataPrivacyRequestStatus = DataPrivacyRequestStatus.PENDING`
        *   `details: Optional[str] = None` (e.g., specific data for rectification)
        *   `created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))`
        *   `updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))`
        *   `processed_at: Optional[datetime] = None`
        *   `response_data_path: Optional[str] = None` (e.g., MinIO path for portability export)
    *   `RetentionRuleAction(str, Enum)`:
        *   `DELETE = "delete"`
        *   `ANONYMIZE = "anonymize"`
    *   `RetentionRule(BaseModel)`: (Value Object, or could be configured elsewhere)
        *   `data_category: str` (e.g., "inactive_free_user_profile", "consent_log")
        *   `retention_period_days: int`
        *   `action: RetentionRuleAction`
        *   `basis: str` (e.g., "last_activity", "consent_revoked_date")
*   **Methods (within `DataPrivacyRequest`):**
    *   `mark_as_processing(self)`
    *   `mark_as_completed(self, response_data_path: Optional[str] = None)`
    *   `mark_as_failed(self, reason: str)`
*   **ImplementedFeatures:** DataPrivacyRequestDefinition, RetentionRuleDefinition
*   **RequirementIds:** `SEC-004` (UAPM-1-007), `Section 7.5`

#### 4.5.6. `domain/repositories.py`
*   **Purpose:** Defines abstract repository interfaces.
*   **Type:** RepositoryInterface
*   **Key Components (Interfaces using `abc.ABC` and `abc.abstractmethod`):**
    *   `IUserProfileRepository(ABC)`:
        *   `get_by_auth_id(self, auth_user_id: str) -> Awaitable[Optional[UserProfile]]`
        *   `save(self, user_profile: UserProfile) -> Awaitable[UserProfile]`
        *   `delete_by_auth_id(self, auth_user_id: str) -> Awaitable[None]` (Soft delete or hard delete depending on policy)
        *   `get_profiles_for_retention_check(self, last_activity_before: datetime, is_anonymized: bool = False) -> Awaitable[List[UserProfile]]`
    *   `IConsentRepository(ABC)`:
        *   `get_by_user_and_type(self, auth_user_id: str, consent_type: ConsentType) -> Awaitable[Optional[Consent]]`
        *   `get_all_by_user(self, auth_user_id: str) -> Awaitable[List[Consent]]`
        *   `save(self, consent: Consent) -> Awaitable[Consent]`
        *   `delete_by_user_and_type(self, auth_user_id: str, consent_type: ConsentType) -> Awaitable[None]`
    *   `IDataPrivacyRequestRepository(ABC)`:
        *   `save(self, request: DataPrivacyRequest) -> Awaitable[DataPrivacyRequest]`
        *   `get_by_id(self, request_id: UUID) -> Awaitable[Optional[DataPrivacyRequest]]`
        *   `get_by_user_and_type(self, auth_user_id: str, request_type: DataPrivacyRequestType, status: Optional[DataPrivacyRequestStatus] = None) -> Awaitable[List[DataPrivacyRequest]]`
        *   `update(self, request: DataPrivacyRequest) -> Awaitable[DataPrivacyRequest]`
*   **ImplementedFeatures:** RepositoryAbstractions
*   **RequirementIds:** `REQ-004`, `SEC-004`, `Section 7.5`

#### 4.5.7. `domain/services.py`
*   **Purpose:** Contains domain services with business logic spanning multiple entities or complex rules.
*   **Type:** DomainService
*   **Key Components:**
    *   `DataRetentionPolicyService`:
        *   `__init__(self, user_profile_repo: IUserProfileRepository)`
        *   `apply_policy_to_profile(self, user_profile: UserProfile, rules: List[RetentionRule]) -> Awaitable[bool]`:
            *   **Logic:** Iterates through `rules`. For a given `user_profile`, checks if any rule applies (e.g., based on `user_profile.last_activity_at` and `rule.retention_period_days`). If a rule applies, performs the `rule.action` (e.g., calls `user_profile.anonymize()` and then `user_profile_repo.save(user_profile)` or flags for deletion). Returns `True` if an action was taken.
*   **ImplementedFeatures:** DataRetentionLogic
*   **RequirementIds:** `Section 7.5`

#### 4.5.8. `domain/exceptions.py`
*   **Purpose:** Custom domain-specific exceptions.
*   **Type:** Exception
*   **Key Components:**
    *   `UserProfileDomainError(Exception)` (Base class)
    *   `ProfileNotFoundError(UserProfileDomainError)`
    *   `InvalidPreferenceError(UserProfileDomainError)`
    *   `ConsentNotFoundError(UserProfileDomainError)`
    *   `ConsentAlreadyExistsError(UserProfileDomainError)`
    *   `DataPrivacyRequestError(UserProfileDomainError)`
*   **ImplementedFeatures:** DomainErrorHandling

---

### 4.6. Application Layer (`src/creativeflow/services/userprofile/application/`)

#### 4.6.1. `application/__init__.py`
*   **Purpose:** Marks `application` as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

#### 4.6.2. `application/services/__init__.py`
*   **Purpose:** Marks `services` directory within `application` as a package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty or import application service classes.

#### 4.6.3. `application/services/user_profile_service.py`
*   **Purpose:** Application service for managing user profiles and preferences.
*   **Type:** ApplicationService
*   **Key Components:**
    *   `UserProfileService`:
        *   `__init__(self, user_profile_repo: IUserProfileRepository)`
        *   `get_user_profile(self, auth_user_id: str) -> Awaitable[UserProfileSchema]`:
            *   **Logic:** Fetch `UserProfile` from `user_profile_repo`. If not found, raise `ProfileNotFoundError`. Record user activity. Convert domain model to `UserProfileSchema` (application DTO).
        *   `create_or_get_user_profile(self, auth_user_id: str, initial_preferences: Optional[PreferencesSchema] = None) -> Awaitable[UserProfileSchema]`:
            *   **Logic:** Attempt to fetch. If not found, create a new `UserProfile` domain entity with `auth_user_id` and default or provided `initial_preferences`. Save via repo. Convert to `UserProfileSchema`.
        *   `update_user_profile(self, auth_user_id: str, profile_update_data: UserProfileUpdateSchema) -> Awaitable[UserProfileSchema]`:
            *   **Logic:** Fetch `UserProfile`. If not found, raise error or consider creating (depends on desired behavior, usually update implies exists). Call domain model's `update_details` and/or `update_preferences`. Save. Record activity. Convert to `UserProfileSchema`. This handles progressive profiling.
*   **ImplementedFeatures:** UserProfileCRUD, PreferencesManagement, ProgressiveProfilingSupport
*   **RequirementIds:** `REQ-004`, `Section 3.1.2`, `Section 7.1.1`

#### 4.6.4. `application/services/data_privacy_service.py`
*   **Purpose:** Application service for GDPR/CCPA requests.
*   **Type:** ApplicationService
*   **Key Components:**
    *   `DataPrivacyService`:
        *   `__init__(self, user_profile_repo: IUserProfileRepository, privacy_request_repo: IDataPrivacyRequestRepository)`
        *   `request_data_access(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]`:
            *   **Logic:** Create `DataPrivacyRequest` domain entity (type ACCESS). Save via repo. Potentially trigger an async task to compile data. Return DTO.
        *   `request_data_portability(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]`:
            *   **Logic:** Similar to access, but resulting data should be in a portable format. Create `DataPrivacyRequest` (type PORTABILITY). Save. Trigger async task. Return DTO.
        *   `request_account_deletion(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]`:
            *   **Logic:** Create `DataPrivacyRequest` (type DELETION). Save. Trigger anonymization/deletion process (can be async or part of a batch job). Return DTO. Profile service is responsible for its data; coordinating deletion across services might involve events.
        *   `fulfill_data_access_request(self, request_id: UUID) -> Awaitable[UserProfileDataExportSchema]`: (Potentially internal or admin-triggered)
            *   **Logic:** Fetch request. Fetch user profile. Format data for export (e.g., JSON). Store export (e.g., temp MinIO location or return directly if small). Update request status.
        *   `process_pending_deletion_requests_internal(self) -> Awaitable[None]`: (Internal, perhaps scheduled)
            *   **Logic:** Fetch pending deletion requests. For each, fetch `UserProfile`. Call `user_profile.anonymize()` or `user_profile_repo.delete_by_auth_id()`. Update `DataPrivacyRequest` status.
*   **ImplementedFeatures:** GDPRDataAccess, GDPRDataPortability, GDPRDataDeletion, CCPARequestHandling
*   **RequirementIds:** `SEC-004` (UAPM-1-007), `NFR-006`

#### 4.6.5. `application/services/consent_service.py`
*   **Purpose:** Application service for managing user consents.
*   **Type:** ApplicationService
*   **Key Components:**
    *   `ConsentService`:
        *   `__init__(self, consent_repo: IConsentRepository)`
        *   `get_user_consents(self, auth_user_id: str) -> Awaitable[List[ConsentSchema]]`:
            *   **Logic:** Fetch all `Consent` entities for user from repo. Convert to list of `ConsentSchema` DTOs.
        *   `update_user_consent(self, auth_user_id: str, consent_update: ConsentUpdateSchema) -> Awaitable[ConsentSchema]`:
            *   **Logic:** Fetch existing consent by user and type. If not found, create new. Update grant status and version using domain model methods. Save. Convert to `ConsentSchema`.
*   **ImplementedFeatures:** ConsentRetrieval, ConsentUpdate
*   **RequirementIds:** `SEC-004` (UAPM-1-009)

#### 4.6.6. `application/services/data_retention_orchestrator_service.py`
*   **Purpose:** Orchestrates application of data retention policies.
*   **Type:** ApplicationService
*   **Key Components:**
    *   `DataRetentionOrchestratorService`:
        *   `__init__(self, user_profile_repo: IUserProfileRepository, retention_policy_service: DataRetentionPolicyService)`
        *   `apply_retention_policies_globally(self) -> Awaitable[None]`: (Likely triggered by a scheduler, not a direct API call)
            *   **Logic:**
                1.  Define or fetch `RetentionRule`s (these might be hardcoded, from config, or a DB table not yet defined). Example rule for inactive free users: "inactive_free_user_profile", 730 days (24 months), "anonymize", "last_activity_at".
                2.  Fetch eligible profiles from `user_profile_repo.get_profiles_for_retention_check()` based on criteria like `last_activity_before`.
                3.  For each profile, call `retention_policy_service.apply_policy_to_profile(profile, rules)`.
                4.  Log actions taken.
*   **ImplementedFeatures:** DataRetentionExecution
*   **RequirementIds:** `Section 7.5`

#### 4.6.7. `application/schemas.py`
*   **Purpose:** Pydantic schemas for application layer DTOs (internal use).
*   **Type:** DTO
*   **Key Components (Pydantic BaseModels):**
    *   `UserProfileSchema` (Matches domain model UserProfile, for service layer outputs if different from API response)
    *   `PreferencesSchema` (Matches domain model Preferences)
    *   `ConsentSchema` (Matches domain model Consent)
    *   `DataPrivacyRequestSchema` (Matches domain model DataPrivacyRequest)
    *   `UserProfileDataExportSchema` (Structure for data access/portability output, e.g., JSON with profile and links to assets)
        *   `profile: UserProfileSchema`
        *   `consents: List[ConsentSchema]`
        *   (Potentially links to assets or other data this service can provide directly)
    *   Input schemas for service methods if they differ from API schemas (e.g., `UserProfileCreateInternalSchema`, `UserProfileUpdateInternalSchema`). Often, API schemas are directly used by services if simple.
*   **ImplementedFeatures:** InternalDataContracts
*   **RequirementIds:** `REQ-004`, `SEC-004`

#### 4.6.8. `application/exceptions.py`
*   **Purpose:** Custom application-level exceptions.
*   **Type:** Exception
*   **Key Components:**
    *   `UserProfileApplicationError(Exception)` (Base class)
    *   `ProfileUpdateFailedError(UserProfileApplicationError)`
    *   `DataPrivacyRequestProcessingError(UserProfileApplicationError)`
    *   `ConsentManagementError(UserProfileApplicationError)`
*   **ImplementedFeatures:** ApplicationErrorHandling

---

### 4.7. Adapters Layer (`src/creativeflow/services/userprofile/adapters/`)

#### 4.7.1. `adapters/__init__.py`
*   **Purpose:** Marks `adapters` as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

#### 4.7.2. API Adapters (`adapters/api/`)
##### 4.7.2.1. `adapters/api/__init__.py`
*   **Purpose:** Marks `api` directory as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

##### 4.7.2.2. `adapters/api/v1/__init__.py`
*   **Purpose:** Marks `v1` directory as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

##### 4.7.2.3. `adapters/api/v1/routers/__init__.py`
*   **Purpose:** Marks `routers` directory as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:**
    python
    # creativeflow/services/userprofile/adapters/api/v1/routers/__init__.py
    from .user_profiles_router import router as user_profiles_api_router
    from .data_privacy_router import router as data_privacy_api_router
    from .consent_router import router as consent_api_router

    # Optionally, a main router to include all of them
    from fastapi import APIRouter
    api_v1_router = APIRouter()
    api_v1_router.include_router(user_profiles_api_router, prefix="/profiles", tags=["User Profiles"])
    api_v1_router.include_router(data_privacy_api_router, prefix="/privacy-requests", tags=["Data Privacy Requests"])
    api_v1_router.include_router(consent_api_router, prefix="/consents", tags=["User Consents"])

    __all__ = ["api_v1_router"]
    

##### 4.7.2.4. `adapters/api/v1/routers/user_profiles_router.py`
*   **Purpose:** FastAPI router for user profile related HTTP endpoints.
*   **Type:** Controller
*   **Key Components:**
    *   `router = APIRouter()`
*   **Methods (Endpoints):**
    *   `get_user_profile_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), service: UserProfileService = Depends(get_user_profile_service)) -> UserProfileResponseSchema`: `@router.get("/{auth_user_id}")`
        *   **Logic:** Calls `service.get_user_profile(auth_user_id)`. Handles `ProfileNotFoundError` specifically.
    *   `update_user_profile_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), profile_in: UserProfileUpdateRequestSchema, service: UserProfileService = Depends(get_user_profile_service)) -> UserProfileResponseSchema`: `@router.put("/{auth_user_id}")` (PUT for full update)
        *   **Logic:** Calls `service.update_user_profile(auth_user_id, profile_in)`.
    *   `patch_user_profile_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), profile_patch: UserProfilePatchRequestSchema, service: UserProfileService = Depends(get_user_profile_service)) -> UserProfileResponseSchema`: `@router.patch("/{auth_user_id}")` (PATCH for partial update - progressive profiling)
        *   **Logic:** Calls `service.update_user_profile(auth_user_id, profile_patch)` (service method needs to handle partial updates based on `exclude_unset=True` from Pydantic model).
    *   `create_user_profile_on_first_interaction_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), initial_profile_data: Optional[InitialProfileDataSchema] = None, service: UserProfileService = Depends(get_user_profile_service)) -> UserProfileResponseSchema`: `@router.post("/{auth_user_id}")` (If explicit creation is needed, or handled by `get_user_profile` with create-if-not-exists logic)
        *   **Logic:** Calls `service.create_or_get_user_profile(auth_user_id, initial_profile_data)`.
*   **Dependencies:** `UserProfileService`, API Schemas (`UserProfileResponseSchema`, `UserProfileUpdateRequestSchema`, `UserProfilePatchRequestSchema`).
*   **ImplementedFeatures:** UserProfileAPIEndpoints
*   **RequirementIds:** `REQ-004`, `Section 3.1.2`, `Section 7.1.1`

##### 4.7.2.5. `adapters/api/v1/routers/data_privacy_router.py`
*   **Purpose:** FastAPI router for data privacy related HTTP endpoints.
*   **Type:** Controller
*   **Key Components:**
    *   `router = APIRouter()`
*   **Methods (Endpoints):**
    *   `submit_data_access_request_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), service: DataPrivacyService = Depends(get_data_privacy_service)) -> DataPrivacyRequestResponseSchema`: `@router.post("/{auth_user_id}/access-request")`
    *   `submit_data_portability_request_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), service: DataPrivacyService = Depends(get_data_privacy_service)) -> DataPrivacyRequestResponseSchema`: `@router.post("/{auth_user_id}/portability-request")`
    *   `submit_account_deletion_request_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), service: DataPrivacyService = Depends(get_data_privacy_service)) -> DataPrivacyRequestResponseSchema`: `@router.post("/{auth_user_id}/deletion-request")`
    *   `get_data_privacy_request_status_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), request_id: UUID, service: DataPrivacyService = Depends(get_data_privacy_service)) -> DataPrivacyRequestResponseSchema`: `@router.get("/{auth_user_id}/requests/{request_id}")`
*   **Dependencies:** `DataPrivacyService`, API Schemas.
*   **ImplementedFeatures:** DataPrivacyAPIEndpoints
*   **RequirementIds:** `SEC-004` (UAPM-1-007)

##### 4.7.2.6. `adapters/api/v1/routers/consent_router.py`
*   **Purpose:** FastAPI router for user consent management HTTP endpoints.
*   **Type:** Controller
*   **Key Components:**
    *   `router = APIRouter()`
*   **Methods (Endpoints):**
    *   `get_user_consents_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), service: ConsentService = Depends(get_consent_service)) -> List[ConsentResponseSchema]`: `@router.get("/{auth_user_id}/consents")`
    *   `update_user_consent_endpoint(auth_user_id: str = Path(..., description="Authenticated User ID"), consent_type: str = Path(..., description="Type of consent to update"), consent_in: ConsentUpdateRequestSchema, service: ConsentService = Depends(get_consent_service)) -> ConsentResponseSchema`: `@router.put("/{auth_user_id}/consents/{consent_type}")`
*   **Dependencies:** `ConsentService`, API Schemas.
*   **ImplementedFeatures:** ConsentAPIEndpoints
*   **RequirementIds:** `SEC-004` (UAPM-1-009)

##### 4.7.2.7. `adapters/api/v1/schemas.py`
*   **Purpose:** Pydantic schemas for API request and response DTOs.
*   **Type:** DTO
*   **Key Components (Pydantic `BaseModel` classes):**
    *   `PreferencesRequestSchema`: Fields from domain `Preferences` (all optional for updates).
    *   `PreferencesResponseSchema`: Fields from domain `Preferences`.
    *   `UserProfileBaseSchema`: Common fields for user profile.
    *   `UserProfileCreateRequestSchema(UserProfileBaseSchema)`: Schema for profile creation (if needed separately).
    *   `UserProfileUpdateRequestSchema(UserProfileBaseSchema)`: All fields optional for PUT.
        *   `full_name: Optional[str] = None`
        *   `username: Optional[str] = None`
        *   `profile_picture_url: Optional[HttpUrl] = None`
        *   `preferences: Optional[PreferencesRequestSchema] = None`
    *   `UserProfilePatchRequestSchema(BaseModel)`: Similar to Update, but explicitly for PATCH, ensuring Pydantic handles partial updates correctly.
        *   `full_name: Optional[str] = Field(None, description="User's full name")`
        *   `username: Optional[str] = Field(None, description="User's chosen username")`
        *   `profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")`
        *   `language_preference: Optional[str] = Field(None, description="Preferred UI language (e.g., en-US)")`
        *   `timezone: Optional[str] = Field(None, description="User's preferred timezone (e.g., America/New_York)")`
        *   `ui_settings: Optional[dict] = Field(None, description="JSONB for UI settings")`
    *   `UserProfileResponseSchema(UserProfileBaseSchema)`: Includes all relevant fields for response.
        *   `auth_user_id: str`
        *   `full_name: Optional[str]`
        *   `username: Optional[str]`
        *   `profile_picture_url: Optional[HttpUrl]`
        *   `preferences: PreferencesResponseSchema`
        *   `created_at: datetime`
        *   `updated_at: datetime`
    *   `InitialProfileDataSchema(BaseModel)`: For initial profile creation.
        *   `language_preference: Optional[str] = None`
        *   `timezone: Optional[str] = None`
    *   `ConsentTypeEnum(str, Enum)`: Replicates `domain.models.consent.ConsentType` for API schema.
    *   `ConsentUpdateRequestSchema(BaseModel)`:
        *   `is_granted: bool`
        *   `version: str` (e.g., privacy policy version)
    *   `ConsentResponseSchema(BaseModel)`:
        *   `consent_type: ConsentTypeEnum`
        *   `is_granted: bool`
        *   `version: str`
        *   `timestamp: datetime`
    *   `DataPrivacyRequestTypeEnum(str, Enum)`: Replicates domain enum.
    *   `DataPrivacyRequestStatusEnum(str, Enum)`: Replicates domain enum.
    *   `DataPrivacyRequestResponseSchema(BaseModel)`:
        *   `id: UUID`
        *   `auth_user_id: str`
        *   `request_type: DataPrivacyRequestTypeEnum`
        *   `status: DataPrivacyRequestStatusEnum`
        *   `details: Optional[str]`
        *   `created_at: datetime`
        *   `processed_at: Optional[datetime]`
        *   `response_data_url: Optional[HttpUrl] = None` (Link to exported data if applicable)
*   **ImplementedFeatures:** APIDataContracts
*   **RequirementIds:** `REQ-004`, `SEC-004`, `Section 7.1.1`

##### 4.7.2.8. `adapters/api/v1/dependencies.py`
*   **Purpose:** Common FastAPI dependencies for API endpoints.
*   **Type:** DependencyProvider
*   **Key Components:**
    *   `async def get_db_session(session: AsyncSession = Depends(get_async_db_session_local)) -> AsyncGenerator[AsyncSession, None]:`
        *   **Logic:** Yields an SQLAlchemy `AsyncSession` from `database.get_async_db_session_local()`.
    *   `def get_user_profile_service(db_session: AsyncSession = Depends(get_db_session)) -> UserProfileService:`
        *   **Logic:** Initializes and returns `UserProfileService` with `SQLAlchemyUserProfileRepository(db_session)`.
    *   `def get_data_privacy_service(...) -> DataPrivacyService:` (Similar for other services)
    *   `def get_consent_service(...) -> ConsentService:` (Similar)
    *   `async def get_current_auth_user_id(request: Request) -> str:`
        *   **Logic:** Extracts `auth_user_id` from the request, typically from a header set by an API Gateway after validating a JWT from the Auth service. If direct token validation is needed here (less ideal for microservices), it would involve:
            *   `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="dummy_token_url_not_used_here")`
            *   `token: str = Depends(oauth2_scheme)`
            *   Decode and validate JWT (potentially calling Auth service's `/validate` endpoint or using shared public key). For this service, assume `auth_user_id` is passed in a trusted header like `X-User-ID` by the gateway.
            *   Example for trusted header:
            python
            from fastapi import Header, HTTPException, status
            async def get_current_auth_user_id(x_user_id: str | None = Header(None)) -> str:
                if x_user_id is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User ID not provided in headers",
                    )
                return x_user_id
            
*   **ImplementedFeatures:** DatabaseSessionDependency, ServiceInstantiationDependency, UserAuthenticationContextDependency (via header)

---

#### 4.7.3. Database Adapters (`adapters/db/`)
##### 4.7.3.1. `adapters/db/__init__.py`
*   **Purpose:** Marks `db` as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

##### 4.7.3.2. `adapters/db/sqlalchemy_models.py`
*   **Purpose:** SQLAlchemy ORM models.
*   **Type:** ORMModel
*   **Key Components (SQLAlchemy `Base` subclasses):**
    *   `UserProfileSQL(Base)`:
        *   `__tablename__ = "user_profiles"`
        *   `id: Mapped[UUID] = mapped_column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4)`
        *   `auth_user_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)`
        *   `full_name: Mapped[Optional[str]] = mapped_column(String(100))`
        *   `username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)`
        *   `profile_picture_url: Mapped[Optional[str]] = mapped_column(String(1024))`
        *   `language_preference: Mapped[str] = mapped_column(String(10), default="en-US", nullable=False)`
        *   `timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)`
        *   `ui_settings_json: Mapped[Optional[dict]] = mapped_column(JSON, name="ui_settings")`
        *   `created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `is_anonymized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)`
    *   `ConsentSQL(Base)`:
        *   `__tablename__ = "user_consents"`
        *   `id: Mapped[UUID] = mapped_column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4)`
        *   `auth_user_id: Mapped[str] = mapped_column(String(255), ForeignKey("user_profiles.auth_user_id"), index=True, nullable=False)`
        *   `consent_type: Mapped[str] = mapped_column(String(50), nullable=False)` (Store enum value)
        *   `is_granted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)`
        *   `version: Mapped[str] = mapped_column(String(50), nullable=False)`
        *   `timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `UniqueConstraint('auth_user_id', 'consent_type', name='uq_user_consent_type')`
    *   `DataPrivacyRequestSQL(Base)`:
        *   `__tablename__ = "data_privacy_requests"`
        *   `id: Mapped[UUID] = mapped_column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4)`
        *   `auth_user_id: Mapped[str] = mapped_column(String(255), ForeignKey("user_profiles.auth_user_id"), index=True, nullable=False)`
        *   `request_type: Mapped[str] = mapped_column(String(50), nullable=False)`
        *   `status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)`
        *   `details: Mapped[Optional[str]] = mapped_column(Text)`
        *   `created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)`
        *   `processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))`
        *   `response_data_path: Mapped[Optional[str]] = mapped_column(String(1024))`
*   **ImplementedFeatures:** UserProfileTableSchema, ConsentTableSchema, DataPrivacyRequestTableSchema
*   **RequirementIds:** `REQ-004`, `SEC-004`, `Section 7.1.1`

##### 4.7.3.3. `adapters/db/repositories/__init__.py`
*   **Purpose:** Marks `repositories` as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

##### 4.7.3.4. `adapters/db/repositories/user_profile_repository.py`
*   **Purpose:** SQLAlchemy implementation of `IUserProfileRepository`.
*   **Type:** Repository
*   **Key Components:**
    *   `SQLAlchemyUserProfileRepository(IUserProfileRepository)`:
        *   `__init__(self, db_session: AsyncSession)`
        *   `async def get_by_auth_id(self, auth_user_id: str) -> Optional[UserProfile]`:
            *   **Logic:** Query `UserProfileSQL` by `auth_user_id`. Map result to `UserProfile` domain model.
        *   `async def save(self, user_profile: UserProfile) -> UserProfile`:
            *   **Logic:** Check if exists. If yes, update. If no, create. Map `UserProfile` domain model to `UserProfileSQL`. Add and commit. Return mapped domain model.
        *   `async def delete_by_auth_id(self, auth_user_id: str) -> None`:
            *   **Logic:** Find `UserProfileSQL`. If soft delete, update `deleted_at` or `is_anonymized`. If hard delete, `session.delete()`. Commit.
        *   `async def get_profiles_for_retention_check(self, last_activity_before: datetime, is_anonymized: bool = False) -> List[UserProfile]`:
            *   **Logic:** Query `UserProfileSQL` where `last_activity_at < last_activity_before` and `is_anonymized == is_anonymized`. Map results to `UserProfile` domain models.
*   **ImplementedFeatures:** UserProfilePersistence
*   **RequirementIds:** `REQ-004`, `SEC-004`, `Section 7.1.1`, `Section 7.5`

##### 4.7.3.5. `adapters/db/repositories/consent_repository.py`
*   **Purpose:** SQLAlchemy implementation of `IConsentRepository`.
*   **Type:** Repository
*   **Key Components:**
    *   `SQLAlchemyConsentRepository(IConsentRepository)`:
        *   `__init__(self, db_session: AsyncSession)`
        *   `async def get_by_user_and_type(self, auth_user_id: str, consent_type: ConsentType) -> Optional[Consent]`: Map to/from `ConsentSQL`.
        *   `async def get_all_by_user(self, auth_user_id: str) -> List[Consent]`: Map to/from `ConsentSQL`.
        *   `async def save(self, consent: Consent) -> Consent`: Map to/from `ConsentSQL`.
        *   `async def delete_by_user_and_type(self, auth_user_id: str, consent_type: ConsentType) -> None`: (Likely not hard delete, maybe mark inactive or rely on `is_granted=False`)
*   **ImplementedFeatures:** ConsentPersistence
*   **RequirementIds:** `SEC-004`

##### 4.7.3.6. `adapters/db/repositories/data_privacy_request_repository.py`
*   **Purpose:** SQLAlchemy implementation of `IDataPrivacyRequestRepository`.
*   **Type:** Repository
*   **Key Components:**
    *   `SQLAlchemyDataPrivacyRequestRepository(IDataPrivacyRequestRepository)`:
        *   `__init__(self, db_session: AsyncSession)`
        *   `async def save(self, request: DataPrivacyRequest) -> DataPrivacyRequest`: Map to/from `DataPrivacyRequestSQL`.
        *   `async def get_by_id(self, request_id: UUID) -> Optional[DataPrivacyRequest]`: Map to/from `DataPrivacyRequestSQL`.
        *   `async def get_by_user_and_type(...) -> List[DataPrivacyRequest]`: Map to/from `DataPrivacyRequestSQL`.
        *   `async def update(self, request: DataPrivacyRequest) -> DataPrivacyRequest`: Map to/from `DataPrivacyRequestSQL`, update existing.
*   **ImplementedFeatures:** DataPrivacyRequestPersistence
*   **RequirementIds:** `SEC-004`

##### 4.7.3.7. `adapters/db/database.py`
*   **Purpose:** SQLAlchemy database engine and session management for asynchronous operations.
*   **Type:** DatabaseConnector
*   **Key Components:**
    *   `SQLALCHEMY_DATABASE_URL: str` (from `config.py`)
    *   `engine: AsyncEngine` (using `create_async_engine` from `sqlalchemy.ext.asyncio`)
    *   `AsyncSessionLocal: async_sessionmaker` (from `sqlalchemy.ext.asyncio`)
    *   `Base = declarative_base()`
    *   `async def get_async_db_session_local() -> AsyncGenerator[AsyncSession, None]:` FastAPI dependency provider for async sessions.
    *   `async def init_db():` (Optional, if using Alembic for migrations this might not be needed here, or just to create tables for dev if not using migrations initially)
        *   **Logic:** `async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)`
    python
    # creativeflow/services/userprofile/adapters/db/database.py
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    from sqlalchemy.orm import declarative_base
    from typing import AsyncGenerator

    from ....config import get_settings

    settings = get_settings()
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.ENVIRONMENT == "development") # echo based on env
    AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    Base = declarative_base()

    async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            yield session

    async def create_db_and_tables(): # For initial setup or testing
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    
*   **ImplementedFeatures:** DatabaseConnection, SessionManagement (async)

---

#### 4.7.4. Event Handlers (`adapters/event_handlers/`)
##### 4.7.4.1. `adapters/event_handlers/__init__.py`
*   **Purpose:** Marks `event_handlers` as a Python package.
*   **Type:** PackageInitializer
*   **LogicDescription:** Empty.

##### 4.7.4.2. `adapters/event_handlers/user_events_handler.py`
*   **Purpose:** Handles asynchronous events related to users from other services.
*   **Type:** EventHandler
*   **Key Components:**
    *   `UserEventsHandler`: (Could be a class with methods, or standalone functions if simple)
        *   `__init__(self, data_privacy_service: DataPrivacyService)` (or UserProfileService if direct deletion action is there)
        *   `async def handle_user_deleted_event(self, event_data: dict)`:
            *   **Logic:**
                1.  Parse `event_data` to get `auth_user_id`.
                2.  Call `data_privacy_service.request_account_deletion(auth_user_id)` to initiate the standard deletion workflow, or directly call a method in `UserProfileService` to mark the profile for deletion/anonymization according to policy. This ensures data retention rules are respected even for externally triggered deletions.
                3.  Log the event and action taken.
    *   This handler would be registered as a consumer for a specific message queue (e.g., RabbitMQ topic/queue for `user.deleted` events). The setup for consuming messages would typically be in `main.py` during startup or in a separate worker process.
*   **ImplementedFeatures:** CrossServiceEventConsistency (for user deletion)
*   **RequirementIds:** `SEC-004` (related to ensuring data is handled correctly upon account deletion signaled by Auth service).

---

### 4.8. Build and Configuration Files

#### 4.8.1. `pyproject.toml`
*   **Purpose:** Python project configuration using Poetry.
*   **Type:** BuildConfiguration
*   **Key Sections:**
    *   `[tool.poetry]`: name, version, description, authors, license, readme.
    *   `[tool.poetry.dependencies]`:
        *   `python = "^3.11"`
        *   `fastapi = "^0.111.0"` (or latest compatible)
        *   `uvicorn = {extras = ["standard"], version = "^0.29.0"}`
        *   `sqlalchemy = {extras = ["asyncio"], version = "^2.0.30"}`
        *   `asyncpg = "^0.29.0"` (PostgreSQL async driver)
        *   `pydantic = {extras = ["email"], version = "^2.7.4"}`
        *   `pydantic-settings = "^2.3.4"`
        *   `python-jose = {extras = ["cryptography"], version = "^3.3.0"}` (If JWT validation is done locally for some reason)
        *   `python-multipart = "^0.0.9"` (For FastAPI file uploads, if profile picture is uploaded via this service directly)
        *   `python-json-logger = "^2.0.7"` (For structured logging)
        *   `uuid = "^1.30"` (Though `uuid` is in stdlib, explicitly for clarity if specific version features were needed)
    *   `[tool.poetry.group.dev.dependencies]`:
        *   `pytest = "^8.0.0"`
        *   `pytest-asyncio = "^0.23.0"`
        *   `httpx = "^0.27.0"` (For testing FastAPI endpoints)
        *   `flake8 = "^7.0.0"`
        *   `mypy = "^1.10.0"`
        *   `black = "^24.0.0"`
        *   `isort = "^5.0.0"`
    *   `[build-system]`: Standard Poetry build system requirements.
*   **ImplementedFeatures:** DependencyManagement, ProjectBuild

#### 4.8.2. `poetry.lock`
*   **Purpose:** Lock file generated by Poetry for deterministic builds.
*   **Type:** DependencyLockfile
*   **LogicDescription:** Auto-generated by Poetry. Not manually edited.
*   **ImplementedFeatures:** DeterministicBuilds

---

### 4.9. Configuration Variables
*   **`DATABASE_URL`**: PostgreSQL connection string (e.g., `postgresql+asyncpg://user:pass@host:port/dbname`).
*   **`AUTH_SERVICE_URL`**: URL of the Authentication Service (if needed for direct validation).
*   **`LOG_LEVEL`**: Logging level (e.g., `INFO`, `DEBUG`, `WARNING`, `ERROR`).
*   **`ENVIRONMENT`**: Runtime environment (e.g., `development`, `staging`, `production`).
*   **Feature Toggles:**
    *   `ENABLE_PROGRESSIVE_PROFILING_PROMPT: bool = True` (Example, though prompting logic usually in frontend)
    *   `ENABLE_ANONYMIZATION_ON_DELETION: bool = True` (Determines if deletion anonymizes or hard deletes based on request)

---

## 5. Data Models (Summary)

This service will manage the following primary data entities in PostgreSQL, represented by SQLAlchemy ORM models and Pydantic domain models:

*   **UserProfile**: Stores user-specific profile information (name, username, picture, preferences) linked to an `auth_user_id`.
*   **Consent**: Stores user consent status for different processing activities.
*   **DataPrivacyRequest**: Tracks user requests related to GDPR/CCPA (access, portability, deletion).

Detailed schemas are described in sections 4.5.3, 4.5.4, 4.5.5 (Domain Models) and 4.7.3.2 (SQLAlchemy ORM Models).

## 6. API Design

Internal REST APIs will be exposed by this service.

### 6.1. User Profiles API (`/api/v1/userprofiles`)
*   **`POST /{auth_user_id}`**: Create a new user profile (or get existing).
    *   Request Body: `InitialProfileDataSchema` (optional)
    *   Response: `UserProfileResponseSchema`
*   **`GET /{auth_user_id}`**: Retrieve a user's profile.
    *   Response: `UserProfileResponseSchema`
*   **`PUT /{auth_user_id}`**: Update a user's entire profile (idempotent).
    *   Request Body: `UserProfileUpdateRequestSchema`
    *   Response: `UserProfileResponseSchema`
*   **`PATCH /{auth_user_id}`**: Partially update a user's profile (for progressive profiling).
    *   Request Body: `UserProfilePatchRequestSchema`
    *   Response: `UserProfileResponseSchema`

### 6.2. Data Privacy API (`/api/v1/privacy-requests`)
*   **`POST /{auth_user_id}/access-request`**: Submit a data access request.
    *   Response: `DataPrivacyRequestResponseSchema`
*   **`POST /{auth_user_id}/portability-request`**: Submit a data portability request.
    *   Response: `DataPrivacyRequestResponseSchema`
*   **`POST /{auth_user_id}/deletion-request`**: Submit an account/data deletion request.
    *   Response: `DataPrivacyRequestResponseSchema`
*   **`GET /{auth_user_id}/requests/{request_id}`**: Get status of a specific privacy request.
    *   Response: `DataPrivacyRequestResponseSchema`

### 6.3. User Consents API (`/api/v1/consents`)
*   **`GET /{auth_user_id}/consents`**: Retrieve all consents for a user.
    *   Response: `List[ConsentResponseSchema]`
*   **`PUT /{auth_user_id}/consents/{consent_type}`**: Update (grant/withdraw) a specific consent.
    *   Path Parameter: `consent_type` (e.g., "marketing_emails")
    *   Request Body: `ConsentUpdateRequestSchema`
    *   Response: `ConsentResponseSchema`

Authentication for these APIs is assumed to be handled by an upstream API Gateway, which validates a JWT and passes the `auth_user_id` (e.g., via a trusted header like `X-User-ID`). The `get_current_auth_user_id` dependency will extract this.

## 7. Error Handling

*   **Domain Exceptions:** Custom exceptions (e.g., `ProfileNotFoundError`) raised from the domain layer.
*   **Application Exceptions:** Custom exceptions (e.g., `ProfileUpdateFailedError`) raised from the application layer.
*   **API Error Responses:** FastAPI exception handlers in `main.py` will catch custom exceptions and standard FastAPI/Pydantic validation errors, returning appropriate HTTP status codes and JSON error messages (e.g., 400, 404, 500).
    *   400 Bad Request: Invalid input, Pydantic validation errors.
    *   401 Unauthorized: If `auth_user_id` is missing (handled by dependency).
    *   403 Forbidden: If user is not authorized for an action (though most authz might be implicit if `auth_user_id` matches resource).
    *   404 Not Found: Resource (e.g., profile) not found.
    *   500 Internal Server Error: Unhandled exceptions.
*   **Logging:** All errors and exceptions will be logged with context (correlation ID, user ID if available, stack trace).

## 8. Data Retention and Deletion

*   **Deletion Requests:** Handled via `DataPrivacyService`. The actual data removal or anonymization will be performed by repository methods.
*   **Anonymization:** The `UserProfile.anonymize()` method will be used.
*   **Automated Retention:** `DataRetentionOrchestratorService` will periodically invoke `DataRetentionPolicyService` (domain service) to apply rules from `Section 7.5` (e.g., anonymize/delete inactive free user profiles after 24 months). `IUserProfileRepository.get_profiles_for_retention_check` will be used to find eligible profiles.

## 9. Security Considerations

*   **Input Validation:** Pydantic schemas at the API layer provide input validation.
*   **Authentication:** Relies on upstream API Gateway / Auth Service for JWT validation and `auth_user_id` provision.
*   **Authorization:** Primarily based on `auth_user_id` matching the resource being accessed. More complex authorization, if needed, would be handled in application services.
*   **Data Encryption:** NFR-006 states data at rest encryption. This is typically handled at the PostgreSQL database level (e.g., Transparent Data Encryption - TDE if supported and configured, or filesystem encryption) and MinIO level. Application-level encryption for specific sensitive fields is not explicitly designed here but could be added if required by encrypting data before sending to SQLAlchemy models. For this service, the critical part is that it doesn't store raw passwords or overly sensitive data beyond what's defined for profiles and consents.
*   **Dependencies:** Secure communication with PostgreSQL and other internal services (TLS).

## 10. Scalability and Performance

*   **Async Operations:** FastAPI and SQLAlchemy with an async driver (`asyncpg`) enable non-blocking I/O.
*   **Database Optimizations:** Proper indexing on `auth_user_id` and other queried fields. Connection pooling.
*   **Stateless Service:** The service itself aims to be stateless, allowing for horizontal scaling. Session information (if any beyond JWT) would be in Redis.

## 11. Testing Strategy

*   **Unit Tests:** Pytest for domain logic, application services, and repository method logic (using in-memory SQLite or mocked DB for speed if appropriate). Focus on business rules and individual functions.
*   **Integration Tests:** Pytest with `httpx` to test FastAPI endpoints, including interaction with a test database instance. Test service-to-repository interactions.
*   **Contract Tests:** (If applicable) Ensure API contracts are met.
*   Test coverage targets as per `QA-001` (e.g., 90% for critical modules).

This SDS provides a detailed plan for developing the UserProfileService, aligning with the given requirements and file structure.