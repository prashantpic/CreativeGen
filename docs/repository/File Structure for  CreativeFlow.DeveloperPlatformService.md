# Specification

# 1. Files

- **Path:** src/creativeflow/services/developer_platform/__init__.py  
**Description:** Package marker for the developer_platform service.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** __init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'developer_platform' Python package.  
**Logic Description:** Typically empty or may contain package-level imports.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package.
    
**Namespace:** creativeflow.services.developer_platform  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/developer_platform/main.py  
**Description:** Main application file for the FastAPI service. Initializes the FastAPI app, includes routers, middleware, and event handlers.  
**Template:** Python FastAPI Main  
**Dependency Level:** 5  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** create_application  
**Parameters:**
    
    
**Return Type:** FastAPI  
**Attributes:** private  
    - **Name:** startup_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    - **Name:** shutdown_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    
**Implemented Features:**
    
    - ServiceInitialization
    - MiddlewareConfiguration
    - RouterInclusion
    - CORSConfiguration
    - GlobalExceptionHandling
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Sets up and runs the FastAPI application, configuring CORS, exception handlers, and including all API routers.  
**Logic Description:** Instantiate FastAPI. Load configuration using core.config. Configure CORS middleware. Include routers from api.routers. Setup global exception handlers. Define startup (e.g., DB connection pool init, RabbitMQ client init) and shutdown events.  
**Documentation:**
    
    - **Summary:** Entry point for the Developer Platform microservice. Initializes and configures the FastAPI application.
    
**Namespace:** creativeflow.services.developer_platform  
**Metadata:**
    
    - **Category:** ApplicationCore
    
- **Path:** src/creativeflow/services/developer_platform/core/__init__.py  
**Description:** Package marker for core utilities and configurations.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** core/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'core' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for core functionalities.
    
**Namespace:** creativeflow.services.developer_platform.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/developer_platform/core/config.py  
**Description:** Handles application configuration loading using Pydantic for settings management from environment variables or config files.  
**Template:** Python Pydantic Settings  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** core/config  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** RABBITMQ_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** JWT_SECRET_KEY  
**Type:** str  
**Attributes:** public  
    - **Name:** AI_GENERATION_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** ASSET_MANAGEMENT_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** USER_TEAM_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** AUTH_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - ConfigurationLoading
    - EnvironmentVariableParsing
    
**Requirement Ids:**
    
    
**Purpose:** Defines and loads application settings from environment variables or configuration files.  
**Logic Description:** Define a Pydantic BaseModel subclass 'Settings' with fields for all required configurations (database URL, RabbitMQ URL, service URLs, secret keys). Load settings from environment variables. Provide a singleton instance or a getter function.  
**Documentation:**
    
    - **Summary:** Manages application-wide configuration settings.
    
**Namespace:** creativeflow.services.developer_platform.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/developer_platform/core/exceptions.py  
**Description:** Defines custom application-level exceptions and global exception handlers for FastAPI.  
**Template:** Python FastAPI Exceptions  
**Dependency Level:** 1  
**Name:** exceptions  
**Type:** Utility  
**Relative Path:** core/exceptions  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** APIKeyNotFoundError  
**Type:** AppException  
**Attributes:** public  
    - **Name:** WebhookNotFoundError  
**Type:** AppException  
**Attributes:** public  
    - **Name:** InsufficientQuotaError  
**Type:** AppException  
**Attributes:** public  
    - **Name:** RateLimitExceededError  
**Type:** AppException  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** app_exception_handler  
**Parameters:**
    
    - Request request
    - AppException exc
    
**Return Type:** JSONResponse  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - CustomExceptionDefinitions
    - GlobalExceptionHandling
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** Defines custom exceptions for the application and FastAPI exception handlers to return standardized error responses.  
**Logic Description:** Define base AppException and specific exception classes inheriting from it. Create FastAPI exception handlers using '@app.exception_handler' decorator to catch these custom exceptions and return appropriate HTTP responses (e.g., 404, 403, 429).  
**Documentation:**
    
    - **Summary:** Handles custom exceptions and provides global error handling for the API.
    
**Namespace:** creativeflow.services.developer_platform.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/developer_platform/core/logging_config.py  
**Description:** Configures structured logging for the application.  
**Template:** Python Logging Configuration  
**Dependency Level:** 1  
**Name:** logging_config  
**Type:** Configuration  
**Relative Path:** core/logging_config  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str = 'INFO'
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - StructuredLoggingSetup
    
**Requirement Ids:**
    
    
**Purpose:** Sets up application-wide structured logging (e.g., JSON format) to standard output.  
**Logic Description:** Use Python's built-in 'logging' module. Configure formatters for structured logs (e.g., python-json-logger). Set up handlers to output logs to console. Allow log level configuration via environment variable.  
**Documentation:**
    
    - **Summary:** Initializes and configures the logging system for the application.
    
**Namespace:** creativeflow.services.developer_platform.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/developer_platform/api/__init__.py  
**Description:** Package marker for the API layer containing routers, schemas, and dependencies.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** api/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'api' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for API related modules.
    
**Namespace:** creativeflow.services.developer_platform.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/dependencies/__init__.py  
**Description:** Package marker for API dependencies.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** api/dependencies/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'dependencies' Python sub-package for API concerns.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for API dependency injection modules.
    
**Namespace:** creativeflow.services.developer_platform.api.dependencies  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/dependencies/authentication.py  
**Description:** FastAPI dependency for authenticating API clients using API keys.  
**Template:** Python FastAPI Dependency  
**Dependency Level:** 4  
**Name:** authentication  
**Type:** Security  
**Relative Path:** api/dependencies/authentication  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_active_api_client  
**Parameters:**
    
    - api_key_header: str = Security(APIKeyHeader(name='X-API-KEY'))
    - api_key_service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** APIClientDomainModel  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIKeyAuthentication
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    - SEC-005
    
**Purpose:** Provides a FastAPI dependency to authenticate requests based on an API key provided in the 'X-API-KEY' header.  
**Logic Description:** Define an APIKeyHeader security scheme. The 'get_current_active_api_client' dependency extracts the API key from the header, validates it using the APIKeyService, checks if it's active and has necessary permissions for the requested scope (if applicable). Raises HTTP_401_UNAUTHORIZED or HTTP_403_FORBIDDEN if validation fails.  
**Documentation:**
    
    - **Summary:** Handles API key based authentication for FastAPI endpoints.
    
**Namespace:** creativeflow.services.developer_platform.api.dependencies  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/dependencies/common.py  
**Description:** Common FastAPI dependencies, e.g., getting a database session or service instances.  
**Template:** Python FastAPI Dependency  
**Dependency Level:** 3  
**Name:** common  
**Type:** Utility  
**Relative Path:** api/dependencies/common  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Session  
**Attributes:** public  
    - **Name:** get_api_key_service  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    
**Return Type:** APIKeyService  
**Attributes:** public  
    - **Name:** get_webhook_service  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    - webhook_publisher: WebhookPublisher = Depends(get_webhook_publisher)
    
**Return Type:** WebhookService  
**Attributes:** public  
    - **Name:** get_usage_tracking_service  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    
**Return Type:** UsageTrackingService  
**Attributes:** public  
    - **Name:** get_quota_management_service  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    
**Return Type:** QuotaManagementService  
**Attributes:** public  
    - **Name:** get_rate_limiting_service  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    
**Return Type:** RateLimitingService  
**Attributes:** public  
    - **Name:** get_generation_proxy_service  
**Parameters:**
    
    - ai_gen_client: AIGenerationClient = Depends(get_ai_generation_client)
    
**Return Type:** GenerationProxyService  
**Attributes:** public  
    - **Name:** get_webhook_publisher  
**Parameters:**
    
    - rabbitmq_client: RabbitMQClient = Depends(get_rabbitmq_client)
    
**Return Type:** WebhookPublisher  
**Attributes:** public  
    - **Name:** get_rabbitmq_client  
**Parameters:**
    
    
**Return Type:** RabbitMQClient  
**Attributes:** public  
    - **Name:** get_ai_generation_client  
**Parameters:**
    
    
**Return Type:** AIGenerationClient  
**Attributes:** public  
    - **Name:** get_asset_management_client  
**Parameters:**
    
    
**Return Type:** AssetManagementClient  
**Attributes:** public  
    - **Name:** get_user_team_client  
**Parameters:**
    
    
**Return Type:** UserTeamClient  
**Attributes:** public  
    
**Implemented Features:**
    
    - DependencyInjectionSetup
    
**Requirement Ids:**
    
    
**Purpose:** Provides FastAPI dependencies for injecting database sessions and application service instances into route handlers.  
**Logic Description:** Define functions that yield database sessions from infrastructure.database.session. Define functions that instantiate and return application service instances, injecting their own dependencies (like repositories).  
**Documentation:**
    
    - **Summary:** Manages common dependency injections for FastAPI request handlers.
    
**Namespace:** creativeflow.services.developer_platform.api.dependencies  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/routers/__init__.py  
**Description:** Package marker for API routers.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** api/routers/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'routers' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for API route definitions.
    
**Namespace:** creativeflow.services.developer_platform.api.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/routers/api_keys_router.py  
**Description:** FastAPI router for managing API keys (CRUD operations).  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** api_keys_router  
**Type:** Controller  
**Relative Path:** api/routers/api_keys_router  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** create_api_key  
**Parameters:**
    
    - payload: APIKeyCreateSchema
    - user_id: UUID
    - service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** APIKeyResponseSchema  
**Attributes:** public|async|post  
    - **Name:** list_api_keys  
**Parameters:**
    
    - user_id: UUID
    - service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** List[APIKeyResponseSchema]  
**Attributes:** public|async|get  
    - **Name:** get_api_key  
**Parameters:**
    
    - api_key_id: UUID
    - user_id: UUID
    - service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** APIKeyResponseSchema  
**Attributes:** public|async|get  
    - **Name:** update_api_key_permissions  
**Parameters:**
    
    - api_key_id: UUID
    - payload: APIKeyUpdateSchema
    - user_id: UUID
    - service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** APIKeyResponseSchema  
**Attributes:** public|async|put  
    - **Name:** revoke_api_key  
**Parameters:**
    
    - api_key_id: UUID
    - user_id: UUID
    - service: APIKeyService = Depends(get_api_key_service)
    
**Return Type:** StatusResponseSchema  
**Attributes:** public|async|delete  
    
**Implemented Features:**
    
    - APIKeyManagementEndpoints
    
**Requirement Ids:**
    
    - REQ-017
    - SEC-001 (API key management part)
    
**Purpose:** Exposes HTTP endpoints for API key creation, listing, retrieval, permission updates, and revocation for authenticated users (developers).  
**Logic Description:** Define FastAPI routes for API key operations. Each route will depend on an authenticated user (likely from another service or JWT) and the APIKeyService. Use Pydantic schemas for request validation and response formatting. Ensure proper authorization checks (user owns the API key).  
**Documentation:**
    
    - **Summary:** Provides API endpoints for developers to manage their API keys.
    
**Namespace:** creativeflow.services.developer_platform.api.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/routers/webhooks_router.py  
**Description:** FastAPI router for managing webhooks (CRUD operations).  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** webhooks_router  
**Type:** Controller  
**Relative Path:** api/routers/webhooks_router  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** register_webhook  
**Parameters:**
    
    - payload: WebhookCreateSchema
    - user_id: UUID
    - service: WebhookService = Depends(get_webhook_service)
    
**Return Type:** WebhookResponseSchema  
**Attributes:** public|async|post  
    - **Name:** list_webhooks  
**Parameters:**
    
    - user_id: UUID
    - service: WebhookService = Depends(get_webhook_service)
    
**Return Type:** List[WebhookResponseSchema]  
**Attributes:** public|async|get  
    - **Name:** get_webhook  
**Parameters:**
    
    - webhook_id: UUID
    - user_id: UUID
    - service: WebhookService = Depends(get_webhook_service)
    
**Return Type:** WebhookResponseSchema  
**Attributes:** public|async|get  
    - **Name:** update_webhook  
**Parameters:**
    
    - webhook_id: UUID
    - payload: WebhookUpdateSchema
    - user_id: UUID
    - service: WebhookService = Depends(get_webhook_service)
    
**Return Type:** WebhookResponseSchema  
**Attributes:** public|async|put  
    - **Name:** delete_webhook  
**Parameters:**
    
    - webhook_id: UUID
    - user_id: UUID
    - service: WebhookService = Depends(get_webhook_service)
    
**Return Type:** StatusResponseSchema  
**Attributes:** public|async|delete  
    
**Implemented Features:**
    
    - WebhookManagementEndpoints
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Exposes HTTP endpoints for developers to register, list, retrieve, update, and delete their webhook configurations.  
**Logic Description:** Define FastAPI routes for webhook CRUD operations. Authenticate requests (likely via API key or user session). Use WebhookService to interact with the domain and persistence layers. Validate request payloads using Pydantic schemas. Ensure users can only manage their own webhooks.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for developers to manage their webhook subscriptions.
    
**Namespace:** creativeflow.services.developer_platform.api.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/routers/usage_router.py  
**Description:** FastAPI router for developers to query their API usage and quota status.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** usage_router  
**Type:** Controller  
**Relative Path:** api/routers/usage_router  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_api_usage_summary  
**Parameters:**
    
    - api_client: APIClientDomainModel = Depends(get_current_active_api_client)
    - usage_service: UsageTrackingService = Depends(get_usage_tracking_service)
    
**Return Type:** UsageSummaryResponseSchema  
**Attributes:** public|async|get  
    - **Name:** get_current_quota_status  
**Parameters:**
    
    - api_client: APIClientDomainModel = Depends(get_current_active_api_client)
    - quota_service: QuotaManagementService = Depends(get_quota_management_service)
    
**Return Type:** QuotaStatusResponseSchema  
**Attributes:** public|async|get  
    
**Implemented Features:**
    
    - APIUsageQueryEndpoints
    - QuotaStatusEndpoints
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Provides endpoints for API clients (developers) to check their current API usage, associated costs, and quota status.  
**Logic Description:** Define FastAPI routes that depend on an authenticated API client. Use UsageTrackingService and QuotaManagementService to fetch relevant data. Return data formatted according to Pydantic response schemas.  
**Documentation:**
    
    - **Summary:** API endpoints for developers to monitor their API consumption and quota limits.
    
**Namespace:** creativeflow.services.developer_platform.api.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/routers/generation_proxy_router.py  
**Description:** FastAPI router for proxying creative generation, asset, and user/team management requests from API clients.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** generation_proxy_router  
**Type:** Controller  
**Relative Path:** api/routers/generation_proxy_router  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** initiate_creative_generation_proxy  
**Parameters:**
    
    - payload: GenerationCreateSchema
    - api_client: APIClientDomainModel = Depends(get_current_active_api_client)
    - proxy_service: GenerationProxyService = Depends(get_generation_proxy_service)
    
**Return Type:** GenerationStatusResponseSchema  
**Attributes:** public|async|post  
    - **Name:** get_generation_status_proxy  
**Parameters:**
    
    - generation_id: UUID
    - api_client: APIClientDomainModel = Depends(get_current_active_api_client)
    - proxy_service: GenerationProxyService = Depends(get_generation_proxy_service)
    
**Return Type:** GenerationStatusResponseSchema  
**Attributes:** public|async|get  
    - **Name:** retrieve_asset_details_proxy  
**Parameters:**
    
    - asset_id: UUID
    - api_client: APIClientDomainModel = Depends(get_current_active_api_client)
    - proxy_service: GenerationProxyService = Depends(get_generation_proxy_service)
    
**Return Type:** AssetDetailResponseSchema  
**Attributes:** public|async|get  
    
**Implemented Features:**
    
    - ProxiedCreativeGenerationAPI
    - ProxiedAssetManagementAPI
    - ProxiedUserTeamManagementAPI
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Acts as an authenticated gateway for API clients to access creative generation, asset, and user/team management functionalities provided by other backend services.  
**Logic Description:** Define FastAPI routes for the specified operations. Authenticate requests using API keys via 'get_current_active_api_client'. Check API client's permissions for the requested action. Use the GenerationProxyService (which internally uses external clients for AI Gen Orch, Asset Mgmt, User/Team Mgmt services) to forward the request. Track usage via UsageTrackingService. Implement rate limiting and quota checks.  
**Documentation:**
    
    - **Summary:** Exposes core platform functionalities (generation, assets, user/team management) to API developers, acting as an authenticated proxy.
    
**Namespace:** creativeflow.services.developer_platform.api.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/__init__.py  
**Description:** Package marker for API request/response Pydantic schemas.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** api/schemas/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'schemas' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for Pydantic schema definitions used in API request/response validation and serialization.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/api_key_schemas.py  
**Description:** Pydantic schemas for API key related requests and responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** api_key_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/api_key_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** APIKeyBase  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** APIKeyCreateSchema  
**Type:** APIKeyBase  
**Attributes:**   
    - **Name:** APIKeyUpdateSchema  
**Type:** APIKeyBase  
**Attributes:**   
    - **Name:** APIKeyResponseSchema  
**Type:** APIKeyBase  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIKeyDataContracts
    
**Requirement Ids:**
    
    - REQ-017
    - SEC-001 (API key management part)
    
**Purpose:** Defines data structures for creating, updating, and responding with API key information.  
**Logic Description:** Define Pydantic models: APIKeyBase (common fields like name, permissions), APIKeyCreateSchema (for key creation request), APIKeyUpdateSchema (for updating permissions), APIKeyResponseSchema (for API responses, including the key value - to be shown only on creation - and its ID, name, permissions, status).  
**Documentation:**
    
    - **Summary:** Pydantic models for API key request and response data transfer objects.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/webhook_schemas.py  
**Description:** Pydantic schemas for webhook related requests and responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** webhook_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/webhook_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** WebhookBase  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** WebhookCreateSchema  
**Type:** WebhookBase  
**Attributes:**   
    - **Name:** WebhookUpdateSchema  
**Type:** WebhookBase  
**Attributes:**   
    - **Name:** WebhookResponseSchema  
**Type:** WebhookBase  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - WebhookDataContracts
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines data structures for creating, updating, and responding with webhook information.  
**Logic Description:** Define Pydantic models: WebhookBase (common fields like target_url, event_types, secret), WebhookCreateSchema, WebhookUpdateSchema, WebhookResponseSchema (including ID, URL, events, status).  
**Documentation:**
    
    - **Summary:** Pydantic models for webhook request and response data transfer objects.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/usage_schemas.py  
**Description:** Pydantic schemas for API usage and quota related responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** usage_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/usage_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** UsageSummaryResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** QuotaStatusResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIUsageDataContracts
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines data structures for responding with API usage summaries and current quota status.  
**Logic Description:** Define Pydantic models: UsageSummaryResponseSchema (fields like generations_used_current_period, total_cost_current_period, period_start_date, period_end_date). QuotaStatusResponseSchema (fields like quota_limit, quota_remaining, quota_reset_date, rate_limit_per_second).  
**Documentation:**
    
    - **Summary:** Pydantic models for API usage and quota status response data transfer objects.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/generation_schemas.py  
**Description:** Pydantic schemas for proxying creative generation requests and responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** generation_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/generation_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** GenerationCreateSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** GenerationStatusResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - ProxiedGenerationDataContracts
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines data structures for requests to initiate creative generation and responses for generation status, via the developer API proxy.  
**Logic Description:** Define Pydantic models: GenerationCreateSchema (fields like prompt, output_format, style_preferences, etc., mirroring what the AI Generation Orchestration service expects). GenerationStatusResponseSchema (fields like generation_id, status, progress, result_url_if_completed, error_message_if_failed).  
**Documentation:**
    
    - **Summary:** Pydantic models for proxied creative generation request and response DTOs.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/asset_schemas.py  
**Description:** Pydantic schemas for proxying asset management requests and responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** asset_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/asset_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** AssetDetailResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** AssetUploadSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - ProxiedAssetDataContracts
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines data structures for requests to manage assets (e.g., upload) and responses for asset details, via the developer API proxy.  
**Logic Description:** Define Pydantic models: AssetDetailResponseSchema (fields like asset_id, name, type, download_url, metadata). AssetUploadSchema (potentially for multipart file uploads if directly handled, or parameters for asset creation).  
**Documentation:**
    
    - **Summary:** Pydantic models for proxied asset management request and response DTOs.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/user_team_schemas.py  
**Description:** Pydantic schemas for proxying user and team management requests and responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** user_team_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/user_team_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** UserDetailResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    - **Name:** TeamDetailResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - ProxiedUserTeamDataContracts
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines data structures for requests and responses related to user and team management operations, via the developer API proxy.  
**Logic Description:** Define Pydantic models based on the capabilities exposed by the underlying User/Team management service. This might include schemas for listing users in a team, user details, team details etc., accessible to an API client with appropriate permissions.  
**Documentation:**
    
    - **Summary:** Pydantic models for proxied user and team management request and response DTOs.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/api/schemas/base_schemas.py  
**Description:** Common base Pydantic schemas, e.g., for status responses.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** base_schemas  
**Type:** DTO  
**Relative Path:** api/schemas/base_schemas  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** StatusResponseSchema  
**Type:** BaseModel  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - CommonResponseContracts
    
**Requirement Ids:**
    
    
**Purpose:** Defines common response structures used across multiple API endpoints.  
**Logic Description:** Define Pydantic models like StatusResponseSchema (fields: status: str, message: Optional[str]).  
**Documentation:**
    
    - **Summary:** Pydantic models for common API response structures.
    
**Namespace:** creativeflow.services.developer_platform.api.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/developer_platform/application/__init__.py  
**Description:** Package marker for the application layer containing services and use cases.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** application/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'application' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for application logic and services.
    
**Namespace:** creativeflow.services.developer_platform.application  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/__init__.py  
**Description:** Package marker for application services.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** application/services/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'services' Python sub-package within application layer.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for application service implementations.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/api_key_service.py  
**Description:** Application service for managing API keys. Orchestrates domain logic and repository interactions.  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** api_key_service  
**Type:** Service  
**Relative Path:** application/services/api_key_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** api_key_repo  
**Type:** IApiKeyRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** generate_key  
**Parameters:**
    
    - user_id: UUID
    - name: str
    - permissions: Optional[dict]
    
**Return Type:** Tuple[APIKeyDomainModel, str]  
**Attributes:** public|async  
    - **Name:** revoke_key  
**Parameters:**
    
    - api_key_id: UUID
    - user_id: UUID
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** validate_key  
**Parameters:**
    
    - key_value: str
    
**Return Type:** Optional[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** get_key_by_id  
**Parameters:**
    
    - api_key_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** list_keys_for_user  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** update_key_permissions  
**Parameters:**
    
    - api_key_id: UUID
    - user_id: UUID
    - new_permissions: dict
    
**Return Type:** APIKeyDomainModel  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIKeyLifecycleManagement
    - APIKeyValidation
    
**Requirement Ids:**
    
    - REQ-017
    - SEC-001 (API key management part)
    
**Purpose:** Handles business logic for API key generation, validation, revocation, and permission management.  
**Logic Description:** Uses IApiKeyRepository for persistence. Generate_key creates a new APIKey domain object, generates a secure secret, hashes it, saves to DB, and returns the key and original secret (once). Validate_key checks the provided key against stored hashes. Revoke_key updates key status. Other methods manage permissions and listing.  
**Documentation:**
    
    - **Summary:** Orchestrates operations related to API key management.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/webhook_service.py  
**Description:** Application service for managing webhooks. Orchestrates domain logic and repository/publisher interactions.  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** webhook_service  
**Type:** Service  
**Relative Path:** application/services/webhook_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** webhook_repo  
**Type:** IWebhookRepository  
**Attributes:** private  
    - **Name:** webhook_publisher  
**Type:** IWebhookPublisher  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** register_webhook  
**Parameters:**
    
    - user_id: UUID
    - target_url: str
    - event_types: List[str]
    - secret: Optional[str]
    
**Return Type:** WebhookDomainModel  
**Attributes:** public|async  
    - **Name:** update_webhook  
**Parameters:**
    
    - webhook_id: UUID
    - user_id: UUID
    - target_url: Optional[str]
    - event_types: Optional[List[str]]
    - secret: Optional[str]
    
**Return Type:** WebhookDomainModel  
**Attributes:** public|async  
    - **Name:** delete_webhook  
**Parameters:**
    
    - webhook_id: UUID
    - user_id: UUID
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_webhook_by_id  
**Parameters:**
    
    - webhook_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[WebhookDomainModel]  
**Attributes:** public|async  
    - **Name:** list_webhooks_for_user  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[WebhookDomainModel]  
**Attributes:** public|async  
    - **Name:** trigger_event_for_user_webhooks  
**Parameters:**
    
    - user_id: UUID
    - event_type: str
    - payload: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - WebhookLifecycleManagement
    - WebhookEventDispatch
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Handles business logic for webhook registration, management, and triggering event notifications.  
**Logic Description:** Uses IWebhookRepository for persistence and IWebhookPublisher to send events. Register_webhook creates and saves a Webhook domain object. Trigger_event fetches relevant webhooks for a user and event_type, then uses the publisher to send the payload, including HMAC signature if secret is configured.  
**Documentation:**
    
    - **Summary:** Orchestrates operations related to webhook management and event publishing.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/usage_tracking_service.py  
**Description:** Application service for tracking API usage.  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** usage_tracking_service  
**Type:** Service  
**Relative Path:** application/services/usage_tracking_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** usage_repo  
**Type:** IUsageRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** record_api_call  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - endpoint: str
    - cost: Optional[Decimal]
    - is_successful: bool
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_usage_summary  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - start_date: datetime
    - end_date: datetime
    
**Return Type:** UsageSummaryDTO  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIUsageRecording
    - APIUsageReporting
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Handles business logic for recording API calls and generating usage summaries for developers.  
**Logic Description:** Uses IUsageRepository to persist usage records. Record_api_call creates a new UsageRecord. Get_usage_summary aggregates records for a given client/user and time period.  
**Documentation:**
    
    - **Summary:** Manages tracking and reporting of API usage.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/quota_management_service.py  
**Description:** Application service for managing and enforcing API quotas.  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** quota_management_service  
**Type:** Service  
**Relative Path:** application/services/quota_management_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** quota_repo  
**Type:** IQuotaRepository  
**Attributes:** private  
    - **Name:** usage_repo  
**Type:** IUsageRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** check_and_decrement_quota  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - action_cost: int = 1
    
**Return Type:** bool  
**Attributes:** public|async  
    - **Name:** get_quota_status  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    
**Return Type:** QuotaStatusDTO  
**Attributes:** public|async  
    - **Name:** set_quota_for_client  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - limit: int
    - period: str
    
**Return Type:** None  
**Attributes:** public|async|admin_only  
    
**Implemented Features:**
    
    - APIQuotaEnforcement
    - APIQuotaConfiguration
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Handles logic for checking, decrementing, and managing API usage quotas.  
**Logic Description:** Uses IQuotaRepository to manage quota definitions and IUsageRepository to get current usage. Check_and_decrement_quota verifies if the client is within their quota for the current period before allowing an action and updates usage. Get_quota_status returns current usage vs limit.  
**Documentation:**
    
    - **Summary:** Manages API usage quotas for developers.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/rate_limiting_service.py  
**Description:** Application service for managing and enforcing API rate limits. (Could use Redis for counters).  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** rate_limiting_service  
**Type:** Service  
**Relative Path:** application/services/rate_limiting_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** cache_client  
**Type:** RedisClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** is_rate_limited  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - endpoint_key: str
    
**Return Type:** bool  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIRateLimitEnforcement
    
**Requirement Ids:**
    
    - REQ-018
    - SEC-005
    
**Purpose:** Handles logic for checking if an API client has exceeded their rate limits.  
**Logic Description:** Uses a caching client (e.g., Redis, not directly a DB repo for this) to implement a sliding window or token bucket algorithm for rate limiting per API client or user, per endpoint group. Returns true if the request should be blocked.  
**Documentation:**
    
    - **Summary:** Manages API rate limiting for developers.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/application/services/generation_proxy_service.py  
**Description:** Application service for proxying requests from API clients to internal generation, asset, and user/team services.  
**Template:** Python Application Service  
**Dependency Level:** 2  
**Name:** generation_proxy_service  
**Type:** Service  
**Relative Path:** application/services/generation_proxy_service  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** ai_gen_client  
**Type:** AIGenerationClient  
**Attributes:** private  
    - **Name:** asset_mgmt_client  
**Type:** AssetManagementClient  
**Attributes:** private  
    - **Name:** user_team_client  
**Type:** UserTeamClient  
**Attributes:** private  
    - **Name:** usage_tracking_service  
**Type:** UsageTrackingService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** proxy_initiate_generation  
**Parameters:**
    
    - api_client: APIClientDomainModel
    - payload: GenerationCreateSchema
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** proxy_get_generation_status  
**Parameters:**
    
    - api_client: APIClientDomainModel
    - generation_id: UUID
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** proxy_retrieve_asset_details  
**Parameters:**
    
    - api_client: APIClientDomainModel
    - asset_id: UUID
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIRequestProxying
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Orchestrates calls to internal services on behalf of an authenticated API client, handling permissions and usage tracking.  
**Logic Description:** Receives requests from the generation_proxy_router. Verifies API client permissions for the action (if applicable). Calls the appropriate external client (e.g., AIGenerationClient). Records the API call using UsageTrackingService. Handles responses and errors from internal services and translates them for the API client.  
**Documentation:**
    
    - **Summary:** Proxies API client requests to appropriate backend services for generation, assets, and user/team management.
    
**Namespace:** creativeflow.services.developer_platform.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/developer_platform/domain/__init__.py  
**Description:** Package marker for the domain layer.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** domain/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'domain' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for core domain logic and models.
    
**Namespace:** creativeflow.services.developer_platform.domain  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/models/__init__.py  
**Description:** Package marker for domain models.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package  
**Relative Path:** domain/models/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'models' Python sub-package for domain entities and value objects.  
**Logic Description:** Empty file to mark directory as a package. May import key domain models for easier access.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for domain model definitions (Aggregates, Entities, Value Objects).
    
**Namespace:** creativeflow.services.developer_platform.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/models/api_key.py  
**Description:** Domain model for APIKey aggregate and related value objects.  
**Template:** Python Domain Model  
**Dependency Level:** 0  
**Name:** api_key  
**Type:** DomainModel  
**Relative Path:** domain/models/api_key  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - ValueObject
    
**Members:**
    
    - **Name:** APIKeyPermissions (VO)  
**Type:** Pydantic BaseModel  
**Attributes:** public  
    - **Name:** APIKey (Aggregate Root)  
**Type:** Pydantic BaseModel  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** APIKey.create  
**Parameters:**
    
    - user_id: UUID
    - name: str
    - key_value: str
    - secret_hash: str
    - permissions: APIKeyPermissions
    
**Return Type:** APIKey  
**Attributes:** public|static  
    - **Name:** APIKey.revoke  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** APIKey.update_permissions  
**Parameters:**
    
    - new_permissions: APIKeyPermissions
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** APIKey.is_active  
**Parameters:**
    
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - APIKeyEntity
    - APIKeyPermissionsValueObject
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    
**Purpose:** Defines the structure and behavior of an API Key, including its permissions and lifecycle.  
**Logic Description:** APIKeyPermissions: Pydantic model for permissions (e.g., {'can_generate_creative': True, 'can_manage_assets': False}). APIKey: Pydantic model with id, user_id, name, key_prefix, secret_hash, permissions (APIKeyPermissions), is_active, created_at, revoked_at. Methods to manage state (revoke, update_permissions). Factory method for creation. Business logic like ensuring key prefixes are consistent.  
**Documentation:**
    
    - **Summary:** Represents an API Key aggregate root and its associated permissions value object. Encapsulates API key properties and business rules.
    
**Namespace:** creativeflow.services.developer_platform.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/models/webhook.py  
**Description:** Domain model for Webhook entity and related value objects.  
**Template:** Python Domain Model  
**Dependency Level:** 0  
**Name:** webhook  
**Type:** DomainModel  
**Relative Path:** domain/models/webhook  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** WebhookEvent (VO)  
**Type:** Enum  
**Attributes:** public  
    - **Name:** Webhook (Entity)  
**Type:** Pydantic BaseModel  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** Webhook.create  
**Parameters:**
    
    - user_id: UUID
    - target_url: str
    - event_types: List[WebhookEvent]
    - secret: Optional[str]
    
**Return Type:** Webhook  
**Attributes:** public|static  
    - **Name:** Webhook.update_details  
**Parameters:**
    
    - target_url: Optional[str]
    - event_types: Optional[List[WebhookEvent]]
    - secret: Optional[str]
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** Webhook.is_active  
**Parameters:**
    
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** Webhook.generate_signature  
**Parameters:**
    
    - payload: str
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - WebhookEntity
    - WebhookEventValueObject
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines the structure and behavior of a Webhook subscription.  
**Logic Description:** WebhookEvent: Enum for supported event types (e.g., 'generation.completed', 'asset.created'). Webhook: Pydantic model with id, user_id, target_url, subscribed_events (List[WebhookEvent]), hashed_secret, is_active, created_at. Methods for creation, update, and signature generation (HMAC-SHA256) if secret is present.  
**Documentation:**
    
    - **Summary:** Represents a Webhook entity. Encapsulates webhook properties, subscribed events, and security mechanisms like signature generation.
    
**Namespace:** creativeflow.services.developer_platform.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/models/usage.py  
**Description:** Domain models for API usage records, quotas, and rate limit rules.  
**Template:** Python Domain Model  
**Dependency Level:** 0  
**Name:** usage  
**Type:** DomainModel  
**Relative Path:** domain/models/usage  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** UsagePeriod (VO)  
**Type:** Enum  
**Attributes:** public  
    - **Name:** Quota (Entity)  
**Type:** Pydantic BaseModel  
**Attributes:** public  
    - **Name:** APIUsageRecord (Entity)  
**Type:** Pydantic BaseModel  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** Quota.is_exceeded  
**Parameters:**
    
    - current_usage: int
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** Quota.get_remaining  
**Parameters:**
    
    - current_usage: int
    
**Return Type:** int  
**Attributes:** public  
    
**Implemented Features:**
    
    - APIUsageRecordEntity
    - QuotaEntity
    - RateLimitRuleValueObject
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines structures for tracking API usage, managing quotas, and defining rate limits.  
**Logic Description:** UsagePeriod: Enum (e.g., 'DAILY', 'MONTHLY'). Quota: Pydantic model with id, api_client_id, user_id, limit_amount, period (UsagePeriod), current_usage (transient or calculated), last_reset_at. APIUsageRecord: Pydantic model with id, api_client_id, user_id, timestamp, endpoint_called, cost_incurred, status_code. RateLimitRule could be a VO defining requests per time window for specific endpoints/clients.  
**Documentation:**
    
    - **Summary:** Represents entities and value objects related to API usage tracking, quotas, and rate limiting policies.
    
**Namespace:** creativeflow.services.developer_platform.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/repositories/__init__.py  
**Description:** Package marker for domain repository interfaces.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** domain/repositories/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'repositories' Python sub-package for domain repository interfaces.  
**Logic Description:** Empty file to mark directory as a package. May import repository interfaces for easier access from application layer.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for defining abstract repository interfaces.
    
**Namespace:** creativeflow.services.developer_platform.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/repositories/api_key_repository_interface.py  
**Description:** Interface for APIKey repository defining data access methods.  
**Template:** Python Repository Interface  
**Dependency Level:** 1  
**Name:** api_key_repository_interface  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/api_key_repository_interface  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** add  
**Parameters:**
    
    - api_key: APIKey
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_by_id  
**Parameters:**
    
    - api_key_id: UUID
    
**Return Type:** Optional[APIKey]  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_by_key_value  
**Parameters:**
    
    - key_value_prefix: str
    
**Return Type:** Optional[APIKey]  
**Attributes:** public|abstractmethod|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[APIKey]  
**Attributes:** public|abstractmethod|async  
    - **Name:** update  
**Parameters:**
    
    - api_key: APIKey
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - APIKeyDataAccessContract
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    
**Purpose:** Defines the contract for data persistence operations related to APIKey aggregates.  
**Logic Description:** Abstract base class (ABC) or Protocol defining methods for creating, retrieving (by ID, by key value/prefix), listing by user, and updating APIKey domain objects in the data store.  
**Documentation:**
    
    - **Summary:** Abstract interface for APIKey data access operations.
    
**Namespace:** creativeflow.services.developer_platform.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/repositories/webhook_repository_interface.py  
**Description:** Interface for Webhook repository defining data access methods.  
**Template:** Python Repository Interface  
**Dependency Level:** 1  
**Name:** webhook_repository_interface  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/webhook_repository_interface  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** add  
**Parameters:**
    
    - webhook: Webhook
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_by_id  
**Parameters:**
    
    - webhook_id: UUID
    
**Return Type:** Optional[Webhook]  
**Attributes:** public|abstractmethod|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[Webhook]  
**Attributes:** public|abstractmethod|async  
    - **Name:** list_by_user_id_and_event_type  
**Parameters:**
    
    - user_id: UUID
    - event_type: WebhookEvent
    
**Return Type:** List[Webhook]  
**Attributes:** public|abstractmethod|async  
    - **Name:** update  
**Parameters:**
    
    - webhook: Webhook
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    - **Name:** delete  
**Parameters:**
    
    - webhook_id: UUID
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - WebhookDataAccessContract
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines the contract for data persistence operations related to Webhook entities.  
**Logic Description:** Abstract base class (ABC) or Protocol defining methods for CRUD operations on Webhook domain objects, and listing by user/event type.  
**Documentation:**
    
    - **Summary:** Abstract interface for Webhook data access operations.
    
**Namespace:** creativeflow.services.developer_platform.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/repositories/usage_repository_interface.py  
**Description:** Interface for APIUsageRecord repository defining data access methods.  
**Template:** Python Repository Interface  
**Dependency Level:** 1  
**Name:** usage_repository_interface  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/usage_repository_interface  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** add_record  
**Parameters:**
    
    - usage_record: APIUsageRecord
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_summary_for_client  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - start_date: datetime
    - end_date: datetime
    
**Return Type:** List[APIUsageRecord]  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - APIUsageDataAccessContract
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines the contract for persisting and retrieving API usage records.  
**Logic Description:** Abstract base class (ABC) or Protocol defining methods for adding usage records and retrieving aggregated summaries for specific clients/users within a time period.  
**Documentation:**
    
    - **Summary:** Abstract interface for API usage record data access operations.
    
**Namespace:** creativeflow.services.developer_platform.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/domain/repositories/quota_repository_interface.py  
**Description:** Interface for Quota repository defining data access methods.  
**Template:** Python Repository Interface  
**Dependency Level:** 1  
**Name:** quota_repository_interface  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/quota_repository_interface  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** save_quota  
**Parameters:**
    
    - quota: Quota
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_quota_by_client_id  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[Quota]  
**Attributes:** public|abstractmethod|async  
    - **Name:** update_quota_usage  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - new_usage: int
    - last_reset_at: Optional[datetime]
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - QuotaDataAccessContract
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines the contract for managing API quota persistence.  
**Logic Description:** Abstract base class (ABC) or Protocol defining methods for saving/updating quota entities, retrieving quotas for a client, and updating their current usage count.  
**Documentation:**
    
    - **Summary:** Abstract interface for API Quota data access operations.
    
**Namespace:** creativeflow.services.developer_platform.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/__init__.py  
**Description:** Package marker for the infrastructure layer.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'infrastructure' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for infrastructure concerns like database access, messaging, and external clients.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/__init__.py  
**Description:** Package marker for database related modules.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/database/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'database' Python sub-package for database interactions.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for database models, repositories, and session management.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/session.py  
**Description:** SQLAlchemy database session management and engine setup.  
**Template:** Python SQLAlchemy Session  
**Dependency Level:** 2  
**Name:** session  
**Type:** DatabaseConnector  
**Relative Path:** infrastructure/database/session  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** engine  
**Type:** AsyncEngine  
**Attributes:** private  
    - **Name:** AsyncSessionLocal  
**Type:** async_sessionmaker  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_async_db_session  
**Parameters:**
    
    
**Return Type:** AsyncGenerator[AsyncSession, None]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - DatabaseConnectionManagement
    - SessionHandling
    
**Requirement Ids:**
    
    
**Purpose:** Configures the SQLAlchemy database engine and provides asynchronous session management for database interactions.  
**Logic Description:** Initialize SQLAlchemy async engine using DATABASE_URL from config. Create an async_sessionmaker. Define a dependency 'get_async_db_session' for FastAPI routes to yield a database session and ensure it's closed after the request.  
**Documentation:**
    
    - **Summary:** Manages SQLAlchemy database engine and session creation.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/__init__.py  
**Description:** Package marker for SQLAlchemy ORM models.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/database/models/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'models' Python sub-package for SQLAlchemy ORM definitions.  
**Logic Description:** Empty file to mark directory as a package. Imports all ORM model classes and the Base for Alembic migrations.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for SQLAlchemy ORM model classes.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/base.py  
**Description:** SQLAlchemy declarative base for ORM models.  
**Template:** Python SQLAlchemy Base  
**Dependency Level:** 1  
**Name:** base  
**Type:** ORMBase  
**Relative Path:** infrastructure/database/models/base  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** Base  
**Type:** DeclarativeMeta  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - SQLAlchemyDeclarativeBase
    
**Requirement Ids:**
    
    
**Purpose:** Provides the base class for all SQLAlchemy ORM models.  
**Logic Description:** Define 'Base = declarative_base()' from SQLAlchemy. All ORM models will inherit from this Base.  
**Documentation:**
    
    - **Summary:** SQLAlchemy declarative base class for defining ORM models.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/api_key_model.py  
**Description:** SQLAlchemy ORM model for APIKey entities.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** api_key_model  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/models/api_key_model  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** Column|primary_key  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey  
    - **Name:** name  
**Type:** String  
**Attributes:** Column  
    - **Name:** key_prefix  
**Type:** String  
**Attributes:** Column|unique  
    - **Name:** secret_hash  
**Type:** String  
**Attributes:** Column  
    - **Name:** permissions  
**Type:** JSONB  
**Attributes:** Column  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** Column  
    - **Name:** created_at  
**Type:** DateTime  
**Attributes:** Column  
    - **Name:** revoked_at  
**Type:** DateTime  
**Attributes:** Column|nullable  
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIKeyPersistenceModel
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    
**Purpose:** Defines the database table structure for storing API keys using SQLAlchemy ORM.  
**Logic Description:** Define a class 'APIKeyModel' inheriting from Base. Map attributes from the APIKey domain model to SQLAlchemy columns (String, UUID, Boolean, DateTime, JSONB for permissions). Define relationships if any.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model representing the 'api_keys' table in the database.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/webhook_model.py  
**Description:** SQLAlchemy ORM model for Webhook entities.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** webhook_model  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/models/webhook_model  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** Column|primary_key  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey  
    - **Name:** target_url  
**Type:** String  
**Attributes:** Column  
    - **Name:** event_types  
**Type:** ARRAY(String)  
**Attributes:** Column  
    - **Name:** hashed_secret  
**Type:** String  
**Attributes:** Column|nullable  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** Column  
    - **Name:** created_at  
**Type:** DateTime  
**Attributes:** Column  
    
**Methods:**
    
    
**Implemented Features:**
    
    - WebhookPersistenceModel
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Defines the database table structure for storing webhook subscriptions.  
**Logic Description:** Define a class 'WebhookModel' inheriting from Base. Map attributes from the Webhook domain model to SQLAlchemy columns (String for URL/secret, ARRAY(String) for event_types, UUID, Boolean, DateTime).  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model representing the 'webhooks' table.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/usage_record_model.py  
**Description:** SQLAlchemy ORM model for APIUsageRecord entities.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** usage_record_model  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/models/usage_record_model  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** Column|primary_key  
    - **Name:** api_client_db_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey('api_keys.id')  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey('users.id')  
    - **Name:** timestamp  
**Type:** DateTime  
**Attributes:** Column  
    - **Name:** endpoint  
**Type:** String  
**Attributes:** Column  
    - **Name:** cost  
**Type:** Numeric  
**Attributes:** Column|nullable  
    - **Name:** is_successful  
**Type:** Boolean  
**Attributes:** Column  
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIUsageRecordPersistenceModel
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines the database table structure for storing API usage records.  
**Logic Description:** Define a class 'UsageRecordModel' inheriting from Base. Map attributes to SQLAlchemy columns. 'api_client_db_id' refers to the primary key of the APIKeyModel, not the APIKey value itself.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model representing the 'api_usage_records' table.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/models/quota_model.py  
**Description:** SQLAlchemy ORM model for Quota entities.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** quota_model  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/models/quota_model  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** Column|primary_key  
    - **Name:** api_client_db_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey('api_keys.id')  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** Column|ForeignKey('users.id')  
    - **Name:** limit_amount  
**Type:** Integer  
**Attributes:** Column  
    - **Name:** period  
**Type:** String  
**Attributes:** Column  
    - **Name:** last_reset_at  
**Type:** DateTime  
**Attributes:** Column  
    
**Methods:**
    
    
**Implemented Features:**
    
    - QuotaPersistenceModel
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Defines the database table structure for storing API quotas.  
**Logic Description:** Define a class 'QuotaModel' inheriting from Base. Stores quota limits and reset information per API client/user.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model representing the 'api_quotas' table.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/repositories/__init__.py  
**Description:** Package marker for SQLAlchemy repository implementations.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/database/repositories/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'repositories' Python sub-package for data access implementations.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for SQLAlchemy repository implementations.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/repositories/sqlalchemy_api_key_repository.py  
**Description:** SQLAlchemy implementation of the IApiKeyRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sqlalchemy_api_key_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/sqlalchemy_api_key_repository  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** AsyncSession  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** add  
**Parameters:**
    
    - api_key_domain: APIKeyDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_by_id  
**Parameters:**
    
    - api_key_id: UUID
    
**Return Type:** Optional[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** get_by_key_prefix  
**Parameters:**
    
    - key_prefix: str
    
**Return Type:** Optional[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[APIKeyDomainModel]  
**Attributes:** public|async  
    - **Name:** update  
**Parameters:**
    
    - api_key_domain: APIKeyDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIKeyPersistence
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    
**Purpose:** Provides concrete data access methods for APIKey entities using SQLAlchemy and PostgreSQL.  
**Logic Description:** Implement methods defined in IApiKeyRepository. Use db_session (AsyncSession from SQLAlchemy) to execute queries. Map between APIKeyModel (ORM) and APIKey (domain model). Handle database exceptions. For 'get_by_key_value', query by 'key_prefix'.  
**Documentation:**
    
    - **Summary:** SQLAlchemy implementation for APIKey data persistence.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/repositories/sqlalchemy_webhook_repository.py  
**Description:** SQLAlchemy implementation of the IWebhookRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sqlalchemy_webhook_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/sqlalchemy_webhook_repository  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** AsyncSession  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** add  
**Parameters:**
    
    - webhook_domain: WebhookDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_by_id  
**Parameters:**
    
    - webhook_id: UUID
    
**Return Type:** Optional[WebhookDomainModel]  
**Attributes:** public|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[WebhookDomainModel]  
**Attributes:** public|async  
    - **Name:** list_by_user_id_and_event_type  
**Parameters:**
    
    - user_id: UUID
    - event_type_str: str
    
**Return Type:** List[WebhookDomainModel]  
**Attributes:** public|async  
    - **Name:** update  
**Parameters:**
    
    - webhook_domain: WebhookDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** delete  
**Parameters:**
    
    - webhook_id: UUID
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - WebhookPersistence
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Provides concrete data access methods for Webhook entities using SQLAlchemy.  
**Logic Description:** Implement methods defined in IWebhookRepository. Use db_session to interact with WebhookModel. Map between ORM and domain models.  
**Documentation:**
    
    - **Summary:** SQLAlchemy implementation for Webhook data persistence.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/repositories/sqlalchemy_usage_repository.py  
**Description:** SQLAlchemy implementation of the IUsageRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sqlalchemy_usage_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/sqlalchemy_usage_repository  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** AsyncSession  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** add_record  
**Parameters:**
    
    - usage_record_domain: APIUsageRecordDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_summary_for_client  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - start_date: datetime
    - end_date: datetime
    
**Return Type:** List[APIUsageRecordDomainModel]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APIUsageRecordPersistence
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Provides concrete data access methods for APIUsageRecord entities.  
**Logic Description:** Implement methods from IUsageRepository using UsageRecordModel and SQLAlchemy.  
**Documentation:**
    
    - **Summary:** SQLAlchemy implementation for API usage record persistence.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/repositories/sqlalchemy_quota_repository.py  
**Description:** SQLAlchemy implementation of the IQuotaRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sqlalchemy_quota_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/sqlalchemy_quota_repository  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db_session  
**Type:** AsyncSession  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** save_quota  
**Parameters:**
    
    - quota_domain: QuotaDomainModel
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_quota_by_client_id  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[QuotaDomainModel]  
**Attributes:** public|async  
    - **Name:** get_current_usage_for_quota_period  
**Parameters:**
    
    - api_client_id: UUID
    - user_id: UUID
    - period_start: datetime
    
**Return Type:** int  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - QuotaPersistence
    
**Requirement Ids:**
    
    - REQ-018
    
**Purpose:** Provides concrete data access methods for Quota entities. Note: QuotaModel itself doesn't store current_usage; this repo will need to query UsageRecordModel to calculate it.  
**Logic Description:** Implement methods from IQuotaRepository. Save_quota and get_quota_by_client_id interact with QuotaModel. Get_current_usage_for_quota_period will query UsageRecordModel to sum up usage since the quota's last_reset_at.  
**Documentation:**
    
    - **Summary:** SQLAlchemy implementation for API quota persistence and usage calculation.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/migrations/__init__.py  
**Description:** Alembic migrations package marker.  
**Template:** Python Alembic Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/database/migrations/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the Alembic migrations directory.  
**Logic Description:** Standard Alembic __init__.py.  
**Documentation:**
    
    - **Summary:** Marks the directory for Alembic database migrations.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.migrations  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/database/migrations/env.py  
**Description:** Alembic environment configuration script.  
**Template:** Python Alembic Env  
**Dependency Level:** 2  
**Name:** env  
**Type:** MigrationScript  
**Relative Path:** infrastructure/database/migrations/env  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** run_migrations_offline  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** run_migrations_online  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - DatabaseMigrationConfiguration
    
**Requirement Ids:**
    
    
**Purpose:** Configures Alembic for online and offline database migrations.  
**Logic Description:** Standard Alembic env.py. Sets up target_metadata (from database.models.base.Base), database URL from config, and logic for running migrations.  
**Documentation:**
    
    - **Summary:** Alembic script to configure and run database schema migrations.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.database.migrations  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/messaging/__init__.py  
**Description:** Package marker for messaging related modules.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/messaging/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'messaging' Python sub-package for message queue interactions.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for messaging components (e.g., RabbitMQ clients).
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.messaging  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/messaging/rabbitmq_client.py  
**Description:** RabbitMQ client setup and connection management.  
**Template:** Python RabbitMQ Client  
**Dependency Level:** 2  
**Name:** rabbitmq_client  
**Type:** MessagingClient  
**Relative Path:** infrastructure/messaging/rabbitmq_client  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** connection  
**Type:** aio_pika.RobustConnection  
**Attributes:** private  
    - **Name:** channel  
**Type:** aio_pika.Channel  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** close  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_channel  
**Parameters:**
    
    
**Return Type:** aio_pika.Channel  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - RabbitMQConnectionManagement
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Manages the connection and channel to the RabbitMQ broker.  
**Logic Description:** Uses 'aio_pika' library. The class handles establishing a robust connection to RabbitMQ using URL from config. Provides methods to get a channel for publishing/consuming. Implements connect on startup and close on shutdown.  
**Documentation:**
    
    - **Summary:** Provides RabbitMQ connection and channel management.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.messaging  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/messaging/webhook_publisher.py  
**Description:** Publishes webhook events to RabbitMQ.  
**Template:** Python RabbitMQ Publisher  
**Dependency Level:** 3  
**Name:** webhook_publisher  
**Type:** MessagePublisher  
**Relative Path:** infrastructure/messaging/webhook_publisher  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** rabbitmq_client  
**Type:** RabbitMQClient  
**Attributes:** private  
    - **Name:** exchange_name  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** publish_webhook_event  
**Parameters:**
    
    - webhook: WebhookDomainModel
    - event_type: str
    - payload: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - WebhookEventPublishing
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Sends webhook event data to a RabbitMQ exchange for asynchronous processing and delivery.  
**Logic Description:** Uses RabbitMQClient to get a channel. Declares an exchange (e.g., 'webhook_events_exchange'). Constructs a message containing webhook details (URL, secret if any), event type, and payload. Publishes the message to the exchange with a routing key indicating the event type or user.  
**Documentation:**
    
    - **Summary:** Publishes webhook notification tasks to RabbitMQ.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.messaging  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/security/__init__.py  
**Description:** Package marker for security-related infrastructure utilities.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/security/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'security' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for security utilities like hashing.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.security  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/security/hashing.py  
**Description:** Utility functions for hashing and verifying secrets (e.g., API key secrets).  
**Template:** Python Hashing Utility  
**Dependency Level:** 2  
**Name:** hashing  
**Type:** Utility  
**Relative Path:** infrastructure/security/hashing  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** hash_secret  
**Parameters:**
    
    - secret: str
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** verify_secret  
**Parameters:**
    
    - plain_secret: str
    - hashed_secret: str
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - SecretHashing
    - SecretVerification
    
**Requirement Ids:**
    
    - SEC-001 (API key management part)
    
**Purpose:** Provides functions for securely hashing API key secrets and verifying them.  
**Logic Description:** Use a strong hashing algorithm like bcrypt or Argon2. Hash_secret generates a hash. Verify_secret compares a plain secret against a stored hash.  
**Documentation:**
    
    - **Summary:** Utility for hashing and verifying sensitive strings.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.security  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/external_clients/__init__.py  
**Description:** Package marker for clients that interact with other internal microservices.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** Package  
**Relative Path:** infrastructure/external_clients/__init__  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'external_clients' Python sub-package.  
**Logic Description:** Empty file to mark directory as a package.  
**Documentation:**
    
    - **Summary:** Marks the directory as a Python package for HTTP clients interacting with other services.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.external_clients  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/external_clients/ai_generation_client.py  
**Description:** HTTP client for interacting with the AI Generation Orchestration Service.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** ai_generation_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/external_clients/ai_generation_client  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - CircuitBreaker
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** initiate_generation  
**Parameters:**
    
    - payload: dict
    - auth_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** get_generation_status  
**Parameters:**
    
    - generation_id: UUID
    - auth_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - AIOrchestrationServiceInteraction
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Provides methods to call endpoints on the AI Generation Orchestration Service.  
**Logic Description:** Uses httpx.AsyncClient for making asynchronous HTTP requests. Base URL from config. Methods for initiating generation and getting status. Includes error handling, retries, and potentially circuit breaker logic for calls to the external service.  
**Documentation:**
    
    - **Summary:** Client for communicating with the AI Generation Orchestration Service.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.external_clients  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/external_clients/asset_management_client.py  
**Description:** HTTP client for interacting with an internal Asset Management Service (if one exists separately).  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** asset_management_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/external_clients/asset_management_client  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - CircuitBreaker
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_asset_details  
**Parameters:**
    
    - asset_id: UUID
    - auth_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** upload_asset_proxy  
**Parameters:**
    
    - file_data: bytes
    - metadata: dict
    - auth_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - AssetManagementServiceInteraction
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Provides methods to call endpoints on an internal Asset Management Service if it's distinct from the AI Gen Orch service.  
**Logic Description:** Uses httpx.AsyncClient. Base URL from config. Methods for getting asset details or proxying uploads. Includes error handling, retries, circuit breaker.  
**Documentation:**
    
    - **Summary:** Client for communicating with an internal Asset Management Service.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.external_clients  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/developer_platform/infrastructure/external_clients/user_team_client.py  
**Description:** HTTP client for interacting with an internal User/Team Management Service.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** user_team_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/external_clients/user_team_client  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    - CircuitBreaker
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_user_details_proxy  
**Parameters:**
    
    - user_id_to_query: UUID
    - requesting_user_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** get_team_details_proxy  
**Parameters:**
    
    - team_id_to_query: UUID
    - requesting_user_token: str
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - UserTeamServiceInteraction
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** Provides methods to call endpoints on an internal User/Team Management Service.  
**Logic Description:** Uses httpx.AsyncClient. Base URL from config. Methods for proxied requests to user/team management functionalities. Includes error handling, retries, circuit breaker.  
**Documentation:**
    
    - **Summary:** Client for communicating with an internal User/Team Management Service.
    
**Namespace:** creativeflow.services.developer_platform.infrastructure.external_clients  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** api/openapi.yaml  
**Description:** OpenAPI 3.x specification file for the Developer Platform Service's public-facing API endpoints.  
**Template:** OpenAPI Specification  
**Dependency Level:** 0  
**Name:** openapi  
**Type:** APISpecification  
**Relative Path:** ../../api/openapi  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - APIDocumentation
    
**Requirement Ids:**
    
    - REQ-017
    - REQ-018
    
**Purpose:** Provides a machine-readable definition of the service's API, including endpoints, request/response schemas, and authentication methods.  
**Logic Description:** YAML or JSON file following OpenAPI 3.x schema. Define paths for /api-keys, /webhooks, /usage, /generation-proxy, etc. Specify request bodies and response schemas using references to Pydantic models (or their structure). Detail security schemes (X-API-KEY).  
**Documentation:**
    
    - **Summary:** Formal specification of the API exposed by the Developer Platform Service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** requirements.txt  
**Description:** Lists Python package dependencies for the service.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyFile  
**Relative Path:** ../../requirements  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DependencyManagement
    
**Requirement Ids:**
    
    
**Purpose:** Specifies all external Python libraries required by the service and their versions.  
**Logic Description:** Plain text file listing packages like fastapi, uvicorn, pydantic, sqlalchemy, psycopg2-binary, aio-pika, httpx, python-jose[cryptography], passlib[bcrypt], python-json-logger. Specify versions for reproducible builds (e.g., fastapi==0.100.0).  
**Documentation:**
    
    - **Summary:** Defines project dependencies for pip installation.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** pyproject.toml  
**Description:** Python project configuration file (e.g., for Poetry or Hatch).  
**Template:** Python Pyproject TOML  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** BuildConfiguration  
**Relative Path:** ../../pyproject  
**Repository Id:** REPO-DEVPLATFORM-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - ProjectMetadata
    - BuildSystemConfig
    - DependencyManagement
    
**Requirement Ids:**
    
    
**Purpose:** Defines project metadata, build system (e.g., poetry, hatch), dependencies, and tool configurations (e.g., black, ruff, pytest).  
**Logic Description:** TOML file. [tool.poetry] or [project] section with name, version, description, authors, dependencies. [tool.poetry.dependencies] or [project.dependencies] lists runtime dependencies. [tool.poetry.group.dev.dependencies] or [project.optional-dependencies] for dev/test dependencies. Configuration for linters, formatters, test runners.  
**Documentation:**
    
    - **Summary:** Standard Python project configuration file defining dependencies, build tools, and project metadata.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_advanced_api_key_permissions
  - enable_detailed_usage_cost_breakdown
  - enable_specific_webhook_event_types
  
- **Database Configs:**
  
  - SQLALCHEMY_DATABASE_URL
  - ALEMBIC_SCRIPT_LOCATION
  
- **Message Queue Configs:**
  
  - RABBITMQ_URL
  - RABBITMQ_WEBHOOK_EXCHANGE_NAME
  - RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX
  
- **Apisecurity Configs:**
  
  - API_KEY_HEADER_NAME
  - JWT_ALGORITHM (if used for internal user auth before issuing API key)
  - ACCESS_TOKEN_EXPIRE_MINUTES (for any dev portal sessions)
  
- **Service Urls:**
  
  - AI_GENERATION_ORCH_SERVICE_URL
  - ASSET_MANAGEMENT_SERVICE_URL
  - USER_TEAM_MANAGEMENT_SERVICE_URL
  - AUTH_SERVICE_URL
  
- **Rate Limiting Configs:**
  
  - DEFAULT_RATE_LIMIT_REQUESTS
  - DEFAULT_RATE_LIMIT_PERIOD_SECONDS
  


---

