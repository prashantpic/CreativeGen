# Specification

# 1. Files

- **Path:** src/creativeflow/services/userprofile/__init__.py  
**Description:** Initializes the userprofile service Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PackageInitialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'userprofile' directory a Python package.  
**Logic Description:** This file can be empty or can contain package-level imports.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer.
    
**Namespace:** creativeflow.services.userprofile  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/userprofile/main.py  
**Description:** Main application file for the UserProfile Service. Initializes the FastAPI application, includes routers, and sets up middleware and lifespan events.  
**Template:** Python FastAPI Main  
**Dependency Level:** 5  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:**   
    
**Methods:**
    
    - **Name:** startup_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** shutdown_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - ServiceInitialization
    - APIRouting
    - MiddlewareConfiguration
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    
**Purpose:** Sets up and runs the FastAPI application, including routers for user profiles, data privacy, and consent management.  
**Logic Description:** Import FastAPI. Import routers from adapters.api.v1. Create FastAPI app instance. Include routers. Define startup (e.g., DB connection pool) and shutdown events. Configure CORS middleware if necessary. Setup global exception handlers.  
**Documentation:**
    
    - **Summary:** Entry point for the UserProfile microservice. Initializes and configures the FastAPI application.
    
**Namespace:** creativeflow.services.userprofile  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/userprofile/config.py  
**Description:** Handles application configuration using Pydantic's BaseSettings for loading from environment variables or .env files.  
**Template:** Python Pydantic Settings  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** config.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** AUTH_SERVICE_URL  
**Type:** str  
**Attributes:** Optional  
    - **Name:** LOG_LEVEL  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** lru_cache  
    
**Implemented Features:**
    
    - ConfigurationManagement
    
**Requirement Ids:**
    
    
**Purpose:** Defines and loads environment-specific configurations like database URLs and log levels.  
**Logic Description:** Define a Pydantic BaseSettings class. Add fields for all required configurations (e.g., DATABASE_URL, JWT_SECRET_KEY if local validation, LOG_LEVEL). Implement a function to get cached settings instance.  
**Documentation:**
    
    - **Summary:** Manages application settings loaded from environment variables.
    
**Namespace:** creativeflow.services.userprofile  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/userprofile/logging_config.py  
**Description:** Configures structured logging for the application.  
**Template:** Python Logging Configuration  
**Dependency Level:** 0  
**Name:** logging_config  
**Type:** Configuration  
**Relative Path:** logging_config.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - StructuredLogging
    
**Requirement Ids:**
    
    
**Purpose:** Sets up application-wide logging format and level.  
**Logic Description:** Use Python's logging module. Configure a JSON formatter for structured logs. Set log level based on configuration. Optionally integrate with external logging services if needed.  
**Documentation:**
    
    - **Summary:** Configures logging for the UserProfile service.
    
**Namespace:** creativeflow.services.userprofile  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/userprofile/domain/__init__.py  
**Description:** Initializes the domain package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'domain' directory as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for the domain layer package.
    
**Namespace:** creativeflow.services.userprofile.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/models/__init__.py  
**Description:** Initializes the domain models package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/models/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'models' directory within 'domain' as a Python package.  
**Logic Description:** This file can be empty or import key domain models for easier access.  
**Documentation:**
    
    - **Summary:** Initializer for domain model entities and value objects.
    
**Namespace:** creativeflow.services.userprofile.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/models/user_profile.py  
**Description:** Defines the UserProfile, Preferences, and associated Value Objects domain models.  
**Template:** Python Pydantic Domain Model  
**Dependency Level:** 0  
**Name:** user_profile  
**Type:** DomainModel  
**Relative Path:** domain/models/user_profile.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** UserProfile.id  
**Type:** UUID  
**Attributes:**   
    - **Name:** UserProfile.auth_user_id  
**Type:** str  
**Attributes:** Unique identifier from Auth service  
    - **Name:** UserProfile.full_name  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** UserProfile.username  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** UserProfile.profile_picture_url  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** UserProfile.preferences  
**Type:** Preferences  
**Attributes:**   
    - **Name:** UserProfile.created_at  
**Type:** datetime  
**Attributes:**   
    - **Name:** UserProfile.updated_at  
**Type:** datetime  
**Attributes:**   
    - **Name:** Preferences.language_preference  
**Type:** str  
**Attributes:**   
    - **Name:** Preferences.timezone  
**Type:** str  
**Attributes:**   
    - **Name:** Preferences.ui_settings  
**Type:** Optional[dict]  
**Attributes:** JSONB in DB  
    
**Methods:**
    
    - **Name:** UserProfile.update_details  
**Parameters:**
    
    - full_name: Optional[str]
    - username: Optional[str]
    - ...
    
**Return Type:** None  
**Attributes:**   
    - **Name:** UserProfile.update_preferences  
**Parameters:**
    
    - preferences: Preferences
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - UserProfileDefinition
    - UserPreferencesDefinition
    
**Requirement Ids:**
    
    - REQ-004
    - Section 3.1.2
    - Section 7.1.1
    
**Purpose:** Represents the user's profile information and their UI preferences. Enforces domain invariants.  
**Logic Description:** Use Pydantic BaseModel for UserProfile and Preferences. Define fields as per Section 7.1.1 (full_name, username, profile_picture_url, language_preference, timezone, preferences JSONB). Include methods for updating profile details and preferences while ensuring validity.  
**Documentation:**
    
    - **Summary:** Domain model for user profile attributes and preferences.
    
**Namespace:** creativeflow.services.userprofile.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/models/consent.py  
**Description:** Defines the Consent domain model for managing user consents.  
**Template:** Python Pydantic Domain Model  
**Dependency Level:** 0  
**Name:** consent  
**Type:** DomainModel  
**Relative Path:** domain/models/consent.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** Consent.id  
**Type:** UUID  
**Attributes:**   
    - **Name:** Consent.auth_user_id  
**Type:** str  
**Attributes:**   
    - **Name:** Consent.consent_type  
**Type:** str  
**Attributes:** e.g., marketing_emails, data_analytics  
    - **Name:** Consent.is_granted  
**Type:** bool  
**Attributes:**   
    - **Name:** Consent.version  
**Type:** str  
**Attributes:** Version of privacy policy/terms for this consent  
    - **Name:** Consent.timestamp  
**Type:** datetime  
**Attributes:**   
    
**Methods:**
    
    - **Name:** Consent.grant  
**Parameters:**
    
    - version: str
    
**Return Type:** None  
**Attributes:**   
    - **Name:** Consent.withdraw  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - ConsentDefinition
    - ConsentStateManagement
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Represents a user's consent for a specific data processing activity.  
**Logic Description:** Use Pydantic BaseModel. Define fields for consent type, status (granted/denied), version of policy consented to, and timestamp. Methods to grant and withdraw consent.  
**Documentation:**
    
    - **Summary:** Domain model for user consents related to data processing.
    
**Namespace:** creativeflow.services.userprofile.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/models/data_privacy.py  
**Description:** Defines domain models related to data privacy requests (GDPR/CCPA) and retention rules.  
**Template:** Python Pydantic Domain Model  
**Dependency Level:** 0  
**Name:** data_privacy  
**Type:** DomainModel  
**Relative Path:** domain/models/data_privacy.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** DataPrivacyRequest.id  
**Type:** UUID  
**Attributes:**   
    - **Name:** DataPrivacyRequest.auth_user_id  
**Type:** str  
**Attributes:**   
    - **Name:** DataPrivacyRequest.request_type  
**Type:** str  
**Attributes:** e.g., access, portability, deletion  
    - **Name:** DataPrivacyRequest.status  
**Type:** str  
**Attributes:** e.g., pending, processing, completed, failed  
    - **Name:** DataPrivacyRequest.created_at  
**Type:** datetime  
**Attributes:**   
    - **Name:** DataPrivacyRequest.processed_at  
**Type:** Optional[datetime]  
**Attributes:**   
    - **Name:** DataPrivacyRequest.details  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** RetentionRule.data_category  
**Type:** str  
**Attributes:**   
    - **Name:** RetentionRule.duration_days  
**Type:** int  
**Attributes:**   
    - **Name:** RetentionRule.action  
**Type:** str  
**Attributes:** e.g., delete, anonymize  
    
**Methods:**
    
    - **Name:** DataPrivacyRequest.mark_completed  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - DataPrivacyRequestDefinition
    - RetentionRuleDefinition
    
**Requirement Ids:**
    
    - SEC-004
    - Section 7.5
    
**Purpose:** Represents user requests under GDPR/CCPA and defines data retention rules.  
**Logic Description:** Use Pydantic BaseModel. DataPrivacyRequest tracks requests. RetentionRule defines parameters for data retention policies.  
**Documentation:**
    
    - **Summary:** Domain models for handling data privacy requests and retention policies.
    
**Namespace:** creativeflow.services.userprofile.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/repositories.py  
**Description:** Defines abstract repository interfaces for domain entities.  
**Template:** Python Abstract Repository  
**Dependency Level:** 0  
**Name:** repositories  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - DependencyInversionPrinciple
    
**Members:**
    
    
**Methods:**
    
    - **Name:** IUserProfileRepository.get_by_auth_id  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** Optional[UserProfile]  
**Attributes:** abstractmethod  
    - **Name:** IUserProfileRepository.save  
**Parameters:**
    
    - user_profile: UserProfile
    
**Return Type:** None  
**Attributes:** abstractmethod  
    - **Name:** IUserProfileRepository.delete_by_auth_id  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** None  
**Attributes:** abstractmethod  
    - **Name:** IConsentRepository.get_by_user_and_type  
**Parameters:**
    
    - auth_user_id: str
    - consent_type: str
    
**Return Type:** Optional[Consent]  
**Attributes:** abstractmethod  
    - **Name:** IConsentRepository.save  
**Parameters:**
    
    - consent: Consent
    
**Return Type:** None  
**Attributes:** abstractmethod  
    - **Name:** IConsentRepository.get_all_by_user  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** List[Consent]  
**Attributes:** abstractmethod  
    - **Name:** IDataPrivacyRequestRepository.save  
**Parameters:**
    
    - request: DataPrivacyRequest
    
**Return Type:** None  
**Attributes:** abstractmethod  
    - **Name:** IDataPrivacyRequestRepository.get_by_id  
**Parameters:**
    
    - request_id: UUID
    
**Return Type:** Optional[DataPrivacyRequest]  
**Attributes:** abstractmethod  
    - **Name:** IDataPrivacyRequestRepository.get_pending_deletion_profiles  
**Parameters:**
    
    - retention_period_days: int
    
**Return Type:** List[UserProfile]  
**Attributes:** abstractmethod  
    
**Implemented Features:**
    
    - RepositoryAbstractions
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    - Section 7.5
    
**Purpose:** Provides contracts for data persistence operations, decoupling domain logic from specific database implementations.  
**Logic Description:** Use abc.ABC and abc.abstractmethod to define interfaces for UserProfileRepository, ConsentRepository, and DataPrivacyRequestRepository. Include methods for CRUD operations and specific queries needed by application services.  
**Documentation:**
    
    - **Summary:** Abstract interfaces for data repositories for UserProfile entities.
    
**Namespace:** creativeflow.services.userprofile.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/services.py  
**Description:** Contains domain services with business logic that doesn't naturally fit within a single entity.  
**Template:** Python Domain Service  
**Dependency Level:** 1  
**Name:** services  
**Type:** DomainService  
**Relative Path:** domain/services.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** DataRetentionPolicyService.apply_retention_to_profile  
**Parameters:**
    
    - user_profile: UserProfile
    - rules: List[RetentionRule]
    
**Return Type:** bool  
**Attributes:** Determines if a profile needs action based on rules  
    
**Implemented Features:**
    
    - DataRetentionLogic
    
**Requirement Ids:**
    
    - Section 7.5
    
**Purpose:** Encapsulates complex domain logic, such as evaluating data retention policies against a user profile.  
**Logic Description:** Implement DataRetentionPolicyService. This service would take a user profile and a set of retention rules, and determine if the profile should be anonymized or marked for deletion based on inactivity or other criteria from Section 7.5.  
**Documentation:**
    
    - **Summary:** Domain services for UserProfile-related business logic.
    
**Namespace:** creativeflow.services.userprofile.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/domain/exceptions.py  
**Description:** Custom domain-specific exceptions.  
**Template:** Python Custom Exceptions  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** Exception  
**Relative Path:** domain/exceptions.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DomainErrorHandling
    
**Requirement Ids:**
    
    
**Purpose:** Defines custom exceptions for the domain layer to provide specific error context.  
**Logic Description:** Define custom exception classes inheriting from Python's base Exception (e.g., ProfileNotFoundError, InvalidPreferenceError, ConsentAlreadyExistsError).  
**Documentation:**
    
    - **Summary:** Custom exceptions for the user profile domain.
    
**Namespace:** creativeflow.services.userprofile.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/services/userprofile/application/__init__.py  
**Description:** Initializes the application package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'application' directory as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for the application layer package.
    
**Namespace:** creativeflow.services.userprofile.application  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/services/__init__.py  
**Description:** Initializes the application services package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/services/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'services' directory within 'application' as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for application services (use cases).
    
**Namespace:** creativeflow.services.userprofile.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/services/user_profile_service.py  
**Description:** Application service for managing user profiles and preferences.  
**Template:** Python Application Service  
**Dependency Level:** 3  
**Name:** user_profile_service  
**Type:** ApplicationService  
**Relative Path:** application/services/user_profile_service.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** user_profile_repo  
**Type:** IUserProfileRepository  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_user_profile  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** Optional[UserProfileSchema]  
**Attributes:** async  
    - **Name:** create_user_profile  
**Parameters:**
    
    - auth_user_id: str
    - profile_data: UserProfileCreateSchema
    
**Return Type:** UserProfileSchema  
**Attributes:** async  
    - **Name:** update_user_profile  
**Parameters:**
    
    - auth_user_id: str
    - profile_update_data: UserProfileUpdateSchema
    
**Return Type:** UserProfileSchema  
**Attributes:** async  
    - **Name:** update_user_preferences  
**Parameters:**
    
    - auth_user_id: str
    - preferences_data: PreferencesUpdateSchema
    
**Return Type:** PreferencesSchema  
**Attributes:** async  
    
**Implemented Features:**
    
    - UserProfileCRUD
    - PreferencesManagement
    - ProgressiveProfilingSupport
    
**Requirement Ids:**
    
    - REQ-004
    - Section 3.1.2
    - Section 7.1.1
    
**Purpose:** Orchestrates operations related to user profiles, such as creation, retrieval, updates, and preferences management.  
**Logic Description:** Inject IUserProfileRepository. Implement methods to get, create, and update user profiles and their preferences. Use application-layer DTOs/schemas for input/output. Convert to/from domain models. Handle progressive profiling by allowing partial updates.  
**Documentation:**
    
    - **Summary:** Service layer for handling user profile operations.
    
**Namespace:** creativeflow.services.userprofile.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/services/data_privacy_service.py  
**Description:** Application service for handling GDPR/CCPA data privacy requests.  
**Template:** Python Application Service  
**Dependency Level:** 3  
**Name:** data_privacy_service  
**Type:** ApplicationService  
**Relative Path:** application/services/data_privacy_service.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** user_profile_repo  
**Type:** IUserProfileRepository  
**Attributes:**   
    - **Name:** privacy_request_repo  
**Type:** IDataPrivacyRequestRepository  
**Attributes:**   
    
**Methods:**
    
    - **Name:** request_data_access  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** UserProfileDataExportSchema  
**Attributes:** async  
    - **Name:** request_data_portability  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** UserProfileDataExportSchema  
**Attributes:** async  
    - **Name:** request_data_deletion  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** DataPrivacyRequestSchema  
**Attributes:** async  
    - **Name:** process_pending_deletions  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - GDPRDataAccess
    - GDPRDataPortability
    - GDPRDataDeletion
    - CCPARequestHandling
    
**Requirement Ids:**
    
    - SEC-004
    - NFR-006
    
**Purpose:** Manages data subject requests for access, portability, and deletion of personal data. Orchestrates data deletion/anonymization.  
**Logic Description:** Inject IUserProfileRepository and IDataPrivacyRequestRepository. Implement methods to create and track privacy requests. For deletion, fetch profile, anonymize/delete data via repository, update request status. For access/portability, fetch data and format it.  
**Documentation:**
    
    - **Summary:** Service layer for managing data privacy requests (GDPR/CCPA).
    
**Namespace:** creativeflow.services.userprofile.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/services/consent_service.py  
**Description:** Application service for managing user consents.  
**Template:** Python Application Service  
**Dependency Level:** 3  
**Name:** consent_service  
**Type:** ApplicationService  
**Relative Path:** application/services/consent_service.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** consent_repo  
**Type:** IConsentRepository  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_user_consents  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** List[ConsentSchema]  
**Attributes:** async  
    - **Name:** update_user_consent  
**Parameters:**
    
    - auth_user_id: str
    - consent_update: ConsentUpdateSchema
    
**Return Type:** ConsentSchema  
**Attributes:** async  
    
**Implemented Features:**
    
    - ConsentRetrieval
    - ConsentUpdate
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Handles retrieval and updates of user consents for various processing activities.  
**Logic Description:** Inject IConsentRepository. Implement method to get all consents for a user. Implement method to update a specific consent (grant/withdraw), creating new or updating existing consent records.  
**Documentation:**
    
    - **Summary:** Service layer for managing user consents.
    
**Namespace:** creativeflow.services.userprofile.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/services/data_retention_orchestrator_service.py  
**Description:** Application service for orchestrating data retention policies.  
**Template:** Python Application Service  
**Dependency Level:** 3  
**Name:** data_retention_orchestrator_service  
**Type:** ApplicationService  
**Relative Path:** application/services/data_retention_orchestrator_service.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** user_profile_repo  
**Type:** IUserProfileRepository  
**Attributes:**   
    - **Name:** retention_policy_service  
**Type:** DataRetentionPolicyService  
**Attributes:** Domain Service  
    
**Methods:**
    
    - **Name:** apply_retention_policies_to_all_eligible_profiles  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - DataRetentionExecution
    
**Requirement Ids:**
    
    - Section 7.5
    
**Purpose:** Periodically (e.g., via a scheduled job) applies data retention policies to user profiles.  
**Logic Description:** Inject IUserProfileRepository and DataRetentionPolicyService (domain service). This service might be triggered by a scheduler. It would fetch profiles eligible for retention checks, use the domain service to evaluate policies, and instruct the repository to take action (delete/anonymize).  
**Documentation:**
    
    - **Summary:** Orchestrates the application of data retention policies to user profiles.
    
**Namespace:** creativeflow.services.userprofile.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/schemas.py  
**Description:** Pydantic schemas for application layer Data Transfer Objects (DTOs). These are internal representations used by application services.  
**Template:** Python Pydantic Application DTO  
**Dependency Level:** 1  
**Name:** schemas  
**Type:** DTO  
**Relative Path:** application/schemas.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - DTO
    
**Members:**
    
    - **Name:** UserProfileInternalView.auth_user_id  
**Type:** str  
**Attributes:**   
    - **Name:** UserProfileInternalView.full_name  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** DataPrivacyRequestDetails.request_id  
**Type:** UUID  
**Attributes:**   
    - **Name:** ConsentDetails.consent_type  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - InternalDataContracts
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    
**Purpose:** Defines data structures for internal use within the application layer, distinct from API schemas.  
**Logic Description:** Define Pydantic BaseModels for internal data transfer between application service methods and potentially for mapping from/to domain entities. E.g., schemas for representing a processed profile or a privacy request summary.  
**Documentation:**
    
    - **Summary:** Internal DTOs for the application layer.
    
**Namespace:** creativeflow.services.userprofile.application  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/application/exceptions.py  
**Description:** Custom application-level exceptions.  
**Template:** Python Custom Exceptions  
**Dependency Level:** 1  
**Name:** exceptions  
**Type:** Exception  
**Relative Path:** application/exceptions.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - ApplicationErrorHandling
    
**Requirement Ids:**
    
    
**Purpose:** Defines custom exceptions for the application layer for issues like service-level validation errors or orchestration failures.  
**Logic Description:** Define custom exception classes inheriting from Python's base Exception (e.g., UserProfileProcessingError, DataPrivacyRequestFailedError).  
**Documentation:**
    
    - **Summary:** Custom exceptions for the application layer of UserProfile service.
    
**Namespace:** creativeflow.services.userprofile.application  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/creativeflow/services/userprofile/adapters/__init__.py  
**Description:** Initializes the adapters package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'adapters' directory as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for the adapters (infrastructure) layer package.
    
**Namespace:** creativeflow.services.userprofile.adapters  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/__init__.py  
**Description:** Initializes the API adapters package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/api/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'api' directory as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for the API (HTTP) adapters package.
    
**Namespace:** creativeflow.services.userprofile.adapters.api  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/__init__.py  
**Description:** Initializes the v1 API package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/api/v1/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'v1' directory (for API version 1) as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for version 1 of the UserProfile API.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/routers/__init__.py  
**Description:** Initializes the API routers package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/api/v1/routers/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'routers' directory as a Python package.  
**Logic Description:** This file can be empty or import router instances for inclusion in main.py.  
**Documentation:**
    
    - **Summary:** Initializer for the API routers package.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1.routers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/routers/user_profiles_router.py  
**Description:** FastAPI router for user profile related HTTP endpoints.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** user_profiles_router  
**Type:** Controller  
**Relative Path:** adapters/api/v1/routers/user_profiles_router.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - APIGatewayRouteHandler
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_user_profile_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - service: UserProfileService = Depends()
    
**Return Type:** UserProfileResponseSchema  
**Attributes:** async|@router.get('/{auth_user_id}')  
    - **Name:** update_user_profile_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - profile_in: UserProfileUpdateSchema
    - service: UserProfileService = Depends()
    
**Return Type:** UserProfileResponseSchema  
**Attributes:** async|@router.put('/{auth_user_id}')  
    - **Name:** patch_user_profile_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - profile_patch: UserProfilePatchSchema
    - service: UserProfileService = Depends()
    
**Return Type:** UserProfileResponseSchema  
**Attributes:** async|@router.patch('/{auth_user_id}')  
    
**Implemented Features:**
    
    - UserProfileAPIEndpoints
    
**Requirement Ids:**
    
    - REQ-004
    - Section 3.1.2
    - Section 7.1.1
    
**Purpose:** Defines HTTP endpoints for creating, retrieving, and updating user profiles and preferences.  
**Logic Description:** Import APIRouter from FastAPI, UserProfileService, and API Pydantic schemas. Create router instance. Define GET, PUT, PATCH endpoints for /profiles/{auth_user_id}. Inject UserProfileService. Call service methods, handle exceptions, return responses.  
**Documentation:**
    
    - **Summary:** HTTP endpoints for user profile management.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1.routers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/routers/data_privacy_router.py  
**Description:** FastAPI router for data privacy related HTTP endpoints (GDPR/CCPA).  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** data_privacy_router  
**Type:** Controller  
**Relative Path:** adapters/api/v1/routers/data_privacy_router.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - APIGatewayRouteHandler
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** submit_data_access_request_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - service: DataPrivacyService = Depends()
    
**Return Type:** DataPrivacyRequestResponseSchema  
**Attributes:** async|@router.post('/{auth_user_id}/access')  
    - **Name:** submit_data_portability_request_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - service: DataPrivacyService = Depends()
    
**Return Type:** DataPrivacyRequestResponseSchema  
**Attributes:** async|@router.post('/{auth_user_id}/portability')  
    - **Name:** submit_data_deletion_request_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - service: DataPrivacyService = Depends()
    
**Return Type:** DataPrivacyRequestResponseSchema  
**Attributes:** async|@router.post('/{auth_user_id}/deletion')  
    
**Implemented Features:**
    
    - DataPrivacyAPIEndpoints
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Defines HTTP endpoints for users to submit data access, portability, and deletion requests.  
**Logic Description:** Import APIRouter, DataPrivacyService, API Pydantic schemas. Create router instance. Define POST endpoints for /privacy-requests/{auth_user_id}/access, /portability, /deletion. Inject DataPrivacyService. Call service methods, return responses.  
**Documentation:**
    
    - **Summary:** HTTP endpoints for managing GDPR/CCPA data privacy requests.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1.routers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/routers/consent_router.py  
**Description:** FastAPI router for user consent management HTTP endpoints.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** consent_router  
**Type:** Controller  
**Relative Path:** adapters/api/v1/routers/consent_router.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - APIGatewayRouteHandler
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_user_consents_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - service: ConsentService = Depends()
    
**Return Type:** List[ConsentResponseSchema]  
**Attributes:** async|@router.get('/{auth_user_id}/consents')  
    - **Name:** update_user_consent_endpoint  
**Parameters:**
    
    - auth_user_id: str
    - consent_in: ConsentUpdateSchema
    - service: ConsentService = Depends()
    
**Return Type:** ConsentResponseSchema  
**Attributes:** async|@router.put('/{auth_user_id}/consents/{consent_type}')  
    
**Implemented Features:**
    
    - ConsentAPIEndpoints
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Defines HTTP endpoints for retrieving and updating user consents.  
**Logic Description:** Import APIRouter, ConsentService, API Pydantic schemas. Create router instance. Define GET and PUT endpoints for managing consents. Inject ConsentService. Call service methods, return responses.  
**Documentation:**
    
    - **Summary:** HTTP endpoints for user consent management.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1.routers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/schemas.py  
**Description:** Pydantic schemas for API request and response DTOs (Data Transfer Objects).  
**Template:** Python Pydantic API DTO  
**Dependency Level:** 3  
**Name:** schemas  
**Type:** DTO  
**Relative Path:** adapters/api/v1/schemas.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - DTO
    
**Members:**
    
    - **Name:** UserProfileResponseSchema.auth_user_id  
**Type:** str  
**Attributes:**   
    - **Name:** UserProfileResponseSchema.full_name  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** UserProfileUpdateSchema.full_name  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** PreferencesResponseSchema.language_preference  
**Type:** str  
**Attributes:**   
    - **Name:** PreferencesUpdateSchema.language_preference  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** DataPrivacyRequestSchema.request_type  
**Type:** str  
**Attributes:**   
    - **Name:** DataPrivacyRequestResponseSchema.id  
**Type:** UUID  
**Attributes:**   
    - **Name:** ConsentResponseSchema.consent_type  
**Type:** str  
**Attributes:**   
    - **Name:** ConsentUpdateSchema.is_granted  
**Type:** bool  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIDataContracts
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    - Section 7.1.1
    
**Purpose:** Defines the data structures for HTTP API requests and responses, ensuring data validation and serialization.  
**Logic Description:** Define Pydantic BaseModels for each API endpoint's request body and response payload. Include necessary fields, types, and validation (e.g., email format, string lengths). Separate schemas for creation, update, and response.  
**Documentation:**
    
    - **Summary:** Pydantic schemas for API request/response validation and serialization.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/api/v1/dependencies.py  
**Description:** Common FastAPI dependencies for API endpoints.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 2  
**Name:** dependencies  
**Type:** DependencyProvider  
**Relative Path:** adapters/api/v1/dependencies.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[SessionLocal, None, None]  
**Attributes:**   
    - **Name:** get_current_user_auth_id  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** str  
**Attributes:** Validates token and extracts auth_user_id  
    
**Implemented Features:**
    
    - DatabaseSessionDependency
    - UserAuthenticationDependency
    
**Requirement Ids:**
    
    
**Purpose:** Provides common dependencies to be injected into API endpoint handlers, like database sessions or authenticated user information.  
**Logic Description:** Define functions that FastAPI can use as dependencies. E.g., a dependency to provide a SQLAlchemy session. A dependency to validate an auth token (from Auth service or gateway) and extract user ID.  
**Documentation:**
    
    - **Summary:** FastAPI dependencies for database sessions and user authentication.
    
**Namespace:** creativeflow.services.userprofile.adapters.api.v1  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/__init__.py  
**Description:** Initializes the database adapters package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/db/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'db' directory as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for the database persistence adapters package.
    
**Namespace:** creativeflow.services.userprofile.adapters.db  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/sqlalchemy_models.py  
**Description:** SQLAlchemy ORM models representing database tables for user profiles, preferences, consents, and privacy requests.  
**Template:** Python SQLAlchemy ORM Model  
**Dependency Level:** 1  
**Name:** sqlalchemy_models  
**Type:** ORMModel  
**Relative Path:** adapters/db/sqlalchemy_models.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** UserProfileSQL.id  
**Type:** Column(UUIDType, primary_key=True)  
**Attributes:**   
    - **Name:** UserProfileSQL.auth_user_id  
**Type:** Column(String, unique=True, index=True)  
**Attributes:**   
    - **Name:** UserProfileSQL.full_name  
**Type:** Column(String, nullable=True)  
**Attributes:**   
    - **Name:** UserProfileSQL.preferences_json  
**Type:** Column(JSON)  
**Attributes:**   
    - **Name:** ConsentSQL.id  
**Type:** Column(UUIDType, primary_key=True)  
**Attributes:**   
    - **Name:** DataPrivacyRequestSQL.id  
**Type:** Column(UUIDType, primary_key=True)  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - UserProfileTableSchema
    - PreferencesTableSchema
    - ConsentTableSchema
    - DataPrivacyRequestTableSchema
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    - Section 7.1.1
    
**Purpose:** Defines the database table structures using SQLAlchemy ORM, mapping to PostgreSQL tables.  
**Logic Description:** Import Base from database.py, Column, String, JSON, etc. from SQLAlchemy. Define classes for UserProfileSQL, ConsentSQL, DataPrivacyRequestSQL inheriting from Base. Specify table names and columns as per Section 7.1.1 (profile related fields) and new entities.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM models for UserProfile service data.
    
**Namespace:** creativeflow.services.userprofile.adapters.db  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/repositories/__init__.py  
**Description:** Initializes the database repositories package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/db/repositories/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'repositories' directory within 'db' as a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for concrete repository implementations.
    
**Namespace:** creativeflow.services.userprofile.adapters.db.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/repositories/user_profile_repository.py  
**Description:** SQLAlchemy implementation of the IUserProfileRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** user_profile_repository  
**Type:** Repository  
**Relative Path:** adapters/db/repositories/user_profile_repository.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** Session  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_by_auth_id  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** Optional[UserProfile]  
**Attributes:** async  
    - **Name:** save  
**Parameters:**
    
    - user_profile: UserProfile
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** delete_by_auth_id  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** get_profiles_for_retention_check  
**Parameters:**
    
    - last_activity_threshold: datetime
    
**Return Type:** List[UserProfile]  
**Attributes:** async  
    
**Implemented Features:**
    
    - UserProfilePersistence
    
**Requirement Ids:**
    
    - REQ-004
    - SEC-004
    - Section 7.1.1
    - Section 7.5
    
**Purpose:** Handles database operations (CRUD) for UserProfile domain entities using SQLAlchemy.  
**Logic Description:** Implement IUserProfileRepository. Inject SQLAlchemy Session. Map domain UserProfile to/from UserProfileSQL. Implement methods for creating, finding, updating, and deleting user profile records. Add method to find inactive profiles for retention.  
**Documentation:**
    
    - **Summary:** SQLAlchemy repository for UserProfile data.
    
**Namespace:** creativeflow.services.userprofile.adapters.db.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/repositories/consent_repository.py  
**Description:** SQLAlchemy implementation of the IConsentRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** consent_repository  
**Type:** Repository  
**Relative Path:** adapters/db/repositories/consent_repository.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** Session  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_by_user_and_type  
**Parameters:**
    
    - auth_user_id: str
    - consent_type: str
    
**Return Type:** Optional[Consent]  
**Attributes:** async  
    - **Name:** save  
**Parameters:**
    
    - consent: Consent
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** get_all_by_user  
**Parameters:**
    
    - auth_user_id: str
    
**Return Type:** List[Consent]  
**Attributes:** async  
    
**Implemented Features:**
    
    - ConsentPersistence
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Handles database operations for Consent domain entities.  
**Logic Description:** Implement IConsentRepository. Inject SQLAlchemy Session. Map domain Consent to/from ConsentSQL. Implement methods for saving and retrieving consent records.  
**Documentation:**
    
    - **Summary:** SQLAlchemy repository for Consent data.
    
**Namespace:** creativeflow.services.userprofile.adapters.db.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/repositories/data_privacy_request_repository.py  
**Description:** SQLAlchemy implementation of the IDataPrivacyRequestRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** data_privacy_request_repository  
**Type:** Repository  
**Relative Path:** adapters/db/repositories/data_privacy_request_repository.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** Session  
**Attributes:**   
    
**Methods:**
    
    - **Name:** save  
**Parameters:**
    
    - request: DataPrivacyRequest
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** get_by_id  
**Parameters:**
    
    - request_id: UUID
    
**Return Type:** Optional[DataPrivacyRequest]  
**Attributes:** async  
    - **Name:** update_status  
**Parameters:**
    
    - request_id: UUID
    - status: str
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - DataPrivacyRequestPersistence
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Handles database operations for DataPrivacyRequest domain entities.  
**Logic Description:** Implement IDataPrivacyRequestRepository. Inject SQLAlchemy Session. Map domain DataPrivacyRequest to/from DataPrivacyRequestSQL. Implement methods for saving, retrieving, and updating privacy requests.  
**Documentation:**
    
    - **Summary:** SQLAlchemy repository for DataPrivacyRequest data.
    
**Namespace:** creativeflow.services.userprofile.adapters.db.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/db/database.py  
**Description:** SQLAlchemy database engine and session management setup.  
**Template:** Python SQLAlchemy Database Setup  
**Dependency Level:** 1  
**Name:** database  
**Type:** DatabaseConnector  
**Relative Path:** adapters/db/database.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SQLALCHEMY_DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** engine  
**Type:** Engine  
**Attributes:**   
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:**   
    - **Name:** Base  
**Type:** declarative_base()  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:**   
    
**Implemented Features:**
    
    - DatabaseConnection
    - SessionManagement
    
**Requirement Ids:**
    
    
**Purpose:** Configures the SQLAlchemy database engine, session maker, and provides a dependency for database sessions.  
**Logic Description:** Import create_engine, sessionmaker, declarative_base from SQLAlchemy. Get DATABASE_URL from config. Create engine and SessionLocal. Define Base for ORM models to inherit. Provide a get_db dependency function for FastAPI.  
**Documentation:**
    
    - **Summary:** SQLAlchemy database connection and session management.
    
**Namespace:** creativeflow.services.userprofile.adapters.db  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/event_handlers/__init__.py  
**Description:** Initializes the event handlers package, if external events are consumed.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/event_handlers/__init__.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'event_handlers' directory as a Python package for consuming external events.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Initializer for event consumer adapters.
    
**Namespace:** creativeflow.services.userprofile.adapters.event_handlers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/userprofile/adapters/event_handlers/user_events_handler.py  
**Description:** Handles asynchronous events related to users, e.g., from an Auth service if a user is deleted.  
**Template:** Python Event Handler  
**Dependency Level:** 3  
**Name:** user_events_handler  
**Type:** EventHandler  
**Relative Path:** adapters/event_handlers/user_events_handler.py  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    - MessageConsumer
    
**Members:**
    
    - **Name:** user_profile_service  
**Type:** UserProfileService  
**Attributes:**   
    
**Methods:**
    
    - **Name:** handle_user_deleted_event  
**Parameters:**
    
    - event_data: dict
    
**Return Type:** None  
**Attributes:** async|Consumes UserDeletedEvent  
    
**Implemented Features:**
    
    - CrossServiceEventConsistency
    
**Requirement Ids:**
    
    - SEC-004
    
**Purpose:** Listens to events from other services (e.g., UserDeleted from Auth service) and triggers corresponding actions in this service, like deleting profile data.  
**Logic Description:** This module would consume messages from a message queue (e.g., RabbitMQ) or an event bus. When a 'UserDeletedEvent' is received, it would call the user_profile_service to delete the corresponding user profile data, respecting data retention policies for certain auditable data.  
**Documentation:**
    
    - **Summary:** Handles incoming user-related events from other microservices.
    
**Namespace:** creativeflow.services.userprofile.adapters.event_handlers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** pyproject.toml  
**Description:** Python project configuration file using Poetry. Defines dependencies, project metadata, and build settings.  
**Template:** Python Poetry pyproject.toml  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** BuildConfiguration  
**Relative Path:** ../../pyproject.toml  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DependencyManagement
    - ProjectBuild
    
**Requirement Ids:**
    
    
**Purpose:** Manages project dependencies and build configurations for the UserProfile service.  
**Logic Description:** Define project metadata (name, version, description). List dependencies: fastapi, uvicorn, sqlalchemy, psycopg2-binary, pydantic, python-jose[cryptography] (for potential local JWT utilities if not fully gateway-handled), python-multipart (for form data/uploads if needed by profile picture, though usually direct to S3). Specify Python version.  
**Documentation:**
    
    - **Summary:** Poetry project file for managing dependencies and build information.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** poetry.lock  
**Description:** Lock file generated by Poetry, ensuring deterministic builds by pinning exact versions of all dependencies.  
**Template:** Python Poetry Lock File  
**Dependency Level:** 0  
**Name:** poetry.lock  
**Type:** DependencyLockfile  
**Relative Path:** ../../poetry.lock  
**Repository Id:** REPO-USERPROFILE-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DeterministicBuilds
    
**Requirement Ids:**
    
    
**Purpose:** Ensures reproducible builds by locking dependency versions.  
**Logic Description:** This file is auto-generated by 'poetry lock' or 'poetry install/update'. It should not be manually edited.  
**Documentation:**
    
    - **Summary:** Poetry lock file for precise dependency versioning.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableProgressiveProfilingPrompt
  - EnableAnonymizationOnDeletion
  
- **Database Configs:**
  
  - DATABASE_URL
  - DB_ECHO_LOG
  


---

