# Specification

# 1. Files

- **Path:** src/creativeflow/socialpublishing/__init__.py  
**Description:** Makes the 'socialpublishing' directory a Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the socialpublishing Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the main socialpublishing package.
    
**Namespace:** creativeflow.socialpublishing  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/socialpublishing/main.py  
**Description:** Main application file for the FastAPI service. Initializes the FastAPI app, includes routers, and sets up middleware and event handlers.  
**Template:** Python FastAPI Main  
**Dependency Level:** 4  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
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
    - RouterIntegration
    - MiddlewareConfiguration
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Sets up and runs the FastAPI application, configuring routes, middleware, and lifecycle events.  
**Logic Description:** Create FastAPI instance. Include API routers from api.v1.routers. Setup CORS middleware, exception handlers. Define startup (e.g., DB connection check) and shutdown events.  
**Documentation:**
    
    - **Summary:** Entry point for the Social Publishing microservice. Initializes and configures the FastAPI application.
    
**Namespace:** creativeflow.socialpublishing  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/config.py  
**Description:** Configuration settings for the service, loaded from environment variables or .env files using Pydantic BaseSettings.  
**Template:** Python Pydantic Settings  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** config  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** AES_KEY  
**Type:** str  
**Attributes:** public  
    - **Name:** INSTAGRAM_APP_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** INSTAGRAM_APP_SECRET  
**Type:** str  
**Attributes:** public  
    - **Name:** FACEBOOK_APP_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** FACEBOOK_APP_SECRET  
**Type:** str  
**Attributes:** public  
    - **Name:** LINKEDIN_CLIENT_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** LINKEDIN_CLIENT_SECRET  
**Type:** str  
**Attributes:** public  
    - **Name:** TWITTER_API_KEY  
**Type:** str  
**Attributes:** public  
    - **Name:** TWITTER_API_SECRET_KEY  
**Type:** str  
**Attributes:** public  
    - **Name:** PINTEREST_APP_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** PINTEREST_APP_SECRET  
**Type:** str  
**Attributes:** public  
    - **Name:** TIKTOK_CLIENT_KEY  
**Type:** str  
**Attributes:** public|Optional  
    - **Name:** TIKTOK_CLIENT_SECRET  
**Type:** str  
**Attributes:** public|Optional  
    - **Name:** AUTH_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** LOG_LEVEL  
**Type:** str  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static|functools.lru_cache  
    
**Implemented Features:**
    
    - ConfigurationManagement
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines and loads application settings (database URLs, API keys, service endpoints).  
**Logic Description:** Use Pydantic's BaseSettings to define configuration variables. Load values from environment variables or a .env file. Include all necessary API keys and secrets for social platforms and internal services. Provide a cached function to access settings.  
**Documentation:**
    
    - **Summary:** Manages application configuration settings using Pydantic for type validation and environment variable loading.
    
**Namespace:** creativeflow.socialpublishing.config  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/socialpublishing/dependencies.py  
**Description:** FastAPI dependency injection setup. Defines reusable dependencies for database sessions, service clients, etc.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 3  
**Name:** dependencies  
**Type:** DependencyInjection  
**Relative Path:** dependencies  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:** public|async  
    - **Name:** get_token_encryption_service  
**Parameters:**
    
    
**Return Type:** ITokenEncryptionService  
**Attributes:** public  
    - **Name:** get_oauth_orchestration_service  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    - token_svc: ITokenEncryptionService = Depends(get_token_encryption_service)
    
**Return Type:** OAuthOrchestrationService  
**Attributes:** public  
    - **Name:** get_publishing_orchestration_service  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    
**Return Type:** PublishingOrchestrationService  
**Attributes:** public  
    - **Name:** get_insights_aggregation_service  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    
**Return Type:** InsightsAggregationService  
**Attributes:** public  
    - **Name:** get_current_user_id  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** str  
**Attributes:** public|async  
**Notes:** Depends on an oauth2_scheme from REPO-AUTH-SERVICE-001 contract, or a shared utility.  
    
**Implemented Features:**
    
    - DependencyManagement
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides dependencies like database sessions and service instances to FastAPI path operations.  
**Logic Description:** Define functions that provide instances of services or database sessions. Use FastAPI's Depends system. Ensure proper setup and teardown for resources like database sessions (e.g., using try/finally).  
**Documentation:**
    
    - **Summary:** Manages dependency injection for the FastAPI application, providing necessary service instances and database sessions.
    
**Namespace:** creativeflow.socialpublishing.dependencies  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/socialpublishing/api/__init__.py  
**Description:** Initializes the API package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the api Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the API layer package.
    
**Namespace:** creativeflow.socialpublishing.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/__init__.py  
**Description:** Initializes the V1 API package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the v1 API Python package.  
**Logic Description:** Imports and re-exports routers for convenience.  
**Documentation:**
    
    - **Summary:** Initializes the V1 API layer package, aggregating routers.
    
**Namespace:** creativeflow.socialpublishing.api.v1  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/routers/__init__.py  
**Description:** Initializes the API routers package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/routers/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the API routers Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the API routers package.
    
**Namespace:** creativeflow.socialpublishing.api.v1.routers  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/routers/connections_router.py  
**Description:** FastAPI router for managing social media connections (OAuth flows, listing, disconnecting).  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** connections_router  
**Type:** Controller  
**Relative Path:** api/v1/routers/connections_router  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** initiate_oauth_connection  
**Parameters:**
    
    - platform: str
    - current_user_id: str = Depends(get_current_user_id)
    - oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)
    
**Return Type:** RedirectResponse  
**Attributes:** public|async  
**Decorator:** @router.get('/connect/{platform}')  
    - **Name:** handle_oauth_callback  
**Parameters:**
    
    - platform: str
    - request: Request
    - code: Optional[str] = None
    - error: Optional[str] = None
    - oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)
    
**Return Type:** Any  
**Attributes:** public|async  
**Decorator:** @router.get('/connect/{platform}/callback')  
    - **Name:** list_connections  
**Parameters:**
    
    - current_user_id: str = Depends(get_current_user_id)
    - oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)
    
**Return Type:** List[SocialConnectionResponse]  
**Attributes:** public|async  
**Decorator:** @router.get('/connections')  
    - **Name:** disconnect_account  
**Parameters:**
    
    - connection_id: UUID
    - current_user_id: str = Depends(get_current_user_id)
    - oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)
    
**Return Type:** StatusResponse  
**Attributes:** public|async  
**Decorator:** @router.delete('/connections/{connection_id}')  
    
**Implemented Features:**
    
    - OAuthConnectionInitiation
    - OAuthCallbackHandling
    - ListConnections
    - DisconnectAccount
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Handles API requests related to connecting and managing user social media accounts.  
**Logic Description:** Define FastAPI routes for initiating OAuth flows (redirecting to social platforms), handling callbacks (exchanging code for tokens, storing tokens securely), listing connected accounts for the user, and disconnecting accounts (revoking tokens, deleting connection records). Use injected services for business logic.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for managing social media account connections, including OAuth authorization and token handling.
    
**Namespace:** creativeflow.socialpublishing.api.v1.routers.connections_router  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/routers/publishing_router.py  
**Description:** FastAPI router for publishing and scheduling content to social media platforms.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** publishing_router  
**Type:** Controller  
**Relative Path:** api/v1/routers/publishing_router  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** publish_content_now  
**Parameters:**
    
    - payload: PublishRequest
    - current_user_id: str = Depends(get_current_user_id)
    - publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)
    
**Return Type:** PublishJobResponse  
**Attributes:** public|async  
**Decorator:** @router.post('/publish')  
    - **Name:** schedule_content  
**Parameters:**
    
    - payload: ScheduleRequest
    - current_user_id: str = Depends(get_current_user_id)
    - publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)
    
**Return Type:** PublishJobResponse  
**Attributes:** public|async  
**Decorator:** @router.post('/schedule')  
    - **Name:** get_publish_job_status  
**Parameters:**
    
    - job_id: UUID
    - current_user_id: str = Depends(get_current_user_id)
    - publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)
    
**Return Type:** PublishJobResponse  
**Attributes:** public|async  
**Decorator:** @router.get('/jobs/{job_id}/status')  
    - **Name:** list_publish_jobs  
**Parameters:**
    
    - current_user_id: str = Depends(get_current_user_id)
    - publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)
    - platform: Optional[str] = None
    - status: Optional[str] = None
    
**Return Type:** List[PublishJobResponse]  
**Attributes:** public|async  
**Decorator:** @router.get('/jobs')  
    
**Implemented Features:**
    
    - DirectPublishing
    - ScheduledPublishing
    - JobStatusTracking
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Handles API requests for publishing and scheduling content to connected social media accounts.  
**Logic Description:** Define FastAPI routes for immediate publishing, scheduling content for later, and retrieving the status of publishing jobs. Validate input payloads and user permissions. Delegate actual publishing/scheduling logic to the PublishingOrchestrationService.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for content publishing and scheduling to various social media platforms.
    
**Namespace:** creativeflow.socialpublishing.api.v1.routers.publishing_router  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/routers/insights_router.py  
**Description:** FastAPI router for fetching platform-specific insights like trending hashtags or best times to post.  
**Template:** Python FastAPI Router  
**Dependency Level:** 4  
**Name:** insights_router  
**Type:** Controller  
**Relative Path:** api/v1/routers/insights_router  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_trending_hashtags  
**Parameters:**
    
    - platform: str
    - request_payload: HashtagRequest
    - current_user_id: str = Depends(get_current_user_id)
    - insights_service: InsightsAggregationService = Depends(get_insights_aggregation_service)
    
**Return Type:** HashtagResponse  
**Attributes:** public|async  
**Decorator:** @router.post('/insights/{platform}/hashtags')  
    - **Name:** get_best_times_to_post  
**Parameters:**
    
    - platform: str
    - connection_id: UUID
    - current_user_id: str = Depends(get_current_user_id)
    - insights_service: InsightsAggregationService = Depends(get_insights_aggregation_service)
    
**Return Type:** BestTimeToPostResponse  
**Attributes:** public|async  
**Decorator:** @router.get('/insights/{platform}/best-times')  
    
**Implemented Features:**
    
    - TrendingHashtagSuggestion
    - BestTimeToPostSuggestion
    
**Requirement Ids:**
    
    - INT-002
    
**Purpose:** Handles API requests for fetching social media platform insights.  
**Logic Description:** Define FastAPI routes for fetching trending hashtags (based on keywords/industry) and best times to post for a given platform and connected account. Delegate fetching and processing logic to the InsightsAggregationService.  
**Documentation:**
    
    - **Summary:** Provides API endpoints for retrieving content optimization insights from social media platforms.
    
**Namespace:** creativeflow.socialpublishing.api.v1.routers.insights_router  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/schemas/__init__.py  
**Description:** Initializes the API schemas package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/schemas/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the API Pydantic schemas Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the API schemas package.
    
**Namespace:** creativeflow.socialpublishing.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/schemas/common_schemas.py  
**Description:** Pydantic schemas for common API responses like status or error messages.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** common_schemas  
**Type:** DataModel  
**Relative Path:** api/v1/schemas/common_schemas  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - StandardizedAPIResponses
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines common Pydantic models for consistent API responses.  
**Logic Description:** Define Pydantic models for `StatusResponse` (e.g., `{"status": "success", "message": "Operation successful"}`) and `ErrorDetail` (e.g., `{"code": "invalid_input", "detail": "Field X is required"}`).  
**Documentation:**
    
    - **Summary:** Contains Pydantic schemas for common API response structures, such as status messages and error details.
    
**Namespace:** creativeflow.socialpublishing.api.v1.schemas.common_schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/schemas/connection_schemas.py  
**Description:** Pydantic schemas for social media connection API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** connection_schemas  
**Type:** DataModel  
**Relative Path:** api/v1/schemas/connection_schemas  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - SocialConnectionAPIModels
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines Pydantic models for social media connection-related API interactions.  
**Logic Description:** Define `SocialConnectionResponse` (id, user_id, platform, external_user_id, display_name, created_at). Define `OAuthCallbackQuery` (code, state, error, error_description). Define `InitiateOAuthResponse` (authorization_url).  
**Documentation:**
    
    - **Summary:** Contains Pydantic schemas for requests and responses related to managing social media account connections.
    
**Namespace:** creativeflow.socialpublishing.api.v1.schemas.connection_schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/schemas/publishing_schemas.py  
**Description:** Pydantic schemas for content publishing and scheduling API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** publishing_schemas  
**Type:** DataModel  
**Relative Path:** api/v1/schemas/publishing_schemas  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PublishingAPIModels
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines Pydantic models for content publishing and scheduling API interactions.  
**Logic Description:** Define `GeneratedAsset` (url, type, metadata). Define `PublishRequest` (connection_id, text_content, assets: List[GeneratedAsset], platform_specific_options: dict). Define `ScheduleRequest` (extends PublishRequest, schedule_time: datetime). Define `PublishJobResponse` (job_id, status, platform, created_at, scheduled_at, published_at, error_message, post_url).  
**Documentation:**
    
    - **Summary:** Contains Pydantic schemas for requests and responses related to publishing and scheduling content.
    
**Namespace:** creativeflow.socialpublishing.api.v1.schemas.publishing_schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/api/v1/schemas/insights_schemas.py  
**Description:** Pydantic schemas for social media insights API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** insights_schemas  
**Type:** DataModel  
**Relative Path:** api/v1/schemas/insights_schemas  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - InsightsAPIModels
    
**Requirement Ids:**
    
    - INT-002
    
**Purpose:** Defines Pydantic models for social media insights API interactions.  
**Logic Description:** Define `HashtagRequest` (keywords: List[str], industry: Optional[str], limit: int). Define `HashtagSuggestion` (tag: str, score: Optional[float]). Define `HashtagResponse` (suggestions: List[HashtagSuggestion]). Define `BestTimeToPostResponse` (suggested_times: List[Dict[str, Any]], confidence: Optional[str]).  
**Documentation:**
    
    - **Summary:** Contains Pydantic schemas for requests and responses related to fetching social media insights like hashtags or optimal posting times.
    
**Namespace:** creativeflow.socialpublishing.api.v1.schemas.insights_schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/socialpublishing/application/__init__.py  
**Description:** Initializes the application layer package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the application layer Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the application layer package containing service logic and use cases.
    
**Namespace:** creativeflow.socialpublishing.application  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/application/services/__init__.py  
**Description:** Initializes the application services package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/services/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the application services Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the application services package.
    
**Namespace:** creativeflow.socialpublishing.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/application/services/oauth_orchestration_service.py  
**Description:** Orchestrates OAuth 2.0 flows for connecting social media accounts. Handles token exchange, storage, and retrieval.  
**Template:** Python Service Class  
**Dependency Level:** 3  
**Name:** oauth_orchestration_service  
**Type:** Service  
**Relative Path:** application/services/oauth_orchestration_service  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** social_connection_repo  
**Type:** ISocialConnectionRepository  
**Attributes:** private  
    - **Name:** token_encryption_service  
**Type:** ITokenEncryptionService  
**Attributes:** private  
    - **Name:** platform_clients  
**Type:** Dict[str, BaseSocialClient]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** initiate_connection  
**Parameters:**
    
    - platform: str
    - user_id: str
    
**Return Type:** str  
**Attributes:** public|async  
**Notes:** Returns authorization URL  
    - **Name:** finalize_connection  
**Parameters:**
    
    - platform: str
    - user_id: str
    - callback_data: OAuthCallbackQuery
    
**Return Type:** SocialConnection  
**Attributes:** public|async  
    - **Name:** get_user_connections  
**Parameters:**
    
    - user_id: str
    
**Return Type:** List[SocialConnection]  
**Attributes:** public|async  
    - **Name:** disconnect  
**Parameters:**
    
    - connection_id: UUID
    - user_id: str
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** get_valid_access_token  
**Parameters:**
    
    - connection_id: UUID
    - user_id: str
    
**Return Type:** str  
**Attributes:** public|async  
**Notes:** Handles token refresh if necessary  
    
**Implemented Features:**
    
    - OAuthFlowManagement
    - TokenStorage
    - TokenRetrieval
    - TokenRefresh
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Manages the entire lifecycle of OAuth connections for different social media platforms.  
**Logic Description:** Coordinate with specific platform clients (from infrastructure.clients) to get authorization URLs. Handle callbacks, exchange authorization codes for access/refresh tokens. Use TokenEncryptionService to encrypt tokens before storing them via SocialConnectionRepository. Implement logic for token refresh if supported by the platform and needed.  
**Documentation:**
    
    - **Summary:** Service responsible for orchestrating OAuth 2.0 authentication flows with various social media platforms, including token management.
    
**Namespace:** creativeflow.socialpublishing.application.services.oauth_orchestration_service  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/application/services/publishing_orchestration_service.py  
**Description:** Orchestrates the publishing and scheduling of content to social media platforms.  
**Template:** Python Service Class  
**Dependency Level:** 3  
**Name:** publishing_orchestration_service  
**Type:** Service  
**Relative Path:** application/services/publishing_orchestration_service  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** social_connection_repo  
**Type:** ISocialConnectionRepository  
**Attributes:** private  
    - **Name:** publish_job_repo  
**Type:** IPublishJobRepository  
**Attributes:** private  
    - **Name:** oauth_service  
**Type:** OAuthOrchestrationService  
**Attributes:** private  
    - **Name:** platform_clients  
**Type:** Dict[str, BaseSocialClient]  
**Attributes:** private  
    - **Name:** platform_policy_validator  
**Type:** PlatformPolicyValidator  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** publish_now  
**Parameters:**
    
    - user_id: str
    - payload: PublishRequest
    
**Return Type:** PublishJob  
**Attributes:** public|async  
    - **Name:** schedule_publish  
**Parameters:**
    
    - user_id: str
    - payload: ScheduleRequest
    
**Return Type:** PublishJob  
**Attributes:** public|async  
    - **Name:** get_job_status  
**Parameters:**
    
    - job_id: UUID
    - user_id: str
    
**Return Type:** PublishJob  
**Attributes:** public|async  
    - **Name:** list_jobs  
**Parameters:**
    
    - user_id: str
    - platform: Optional[str]
    - status: Optional[str]
    
**Return Type:** List[PublishJob]  
**Attributes:** public|async  
    - **Name:** _execute_publish  
**Parameters:**
    
    - job: PublishJob
    - access_token: str
    
**Return Type:** Tuple[bool, Optional[str], Optional[str]]  
**Attributes:** private|async  
**Notes:** Returns success, post_url, error_message  
    
**Implemented Features:**
    
    - ContentPublishing
    - ContentScheduling
    - PublishJobManagement
    
**Requirement Ids:**
    
    - INT-001
    - INT-002
    
**Purpose:** Handles the logic for publishing content immediately or scheduling it for later to various social platforms.  
**Logic Description:** Validate the publish/schedule request. Create a PublishJob record. For immediate publishing, fetch a valid access token using OAuthOrchestrationService, validate content against platform policies using PlatformPolicyValidator, then use the appropriate platform client to publish. Update job status. For scheduled publishing, store the job and a background worker/scheduler (out of scope for this service's files, but this service provides jobs for it) would pick it up. Handle API errors and retries (leveraging client utilities).  
**Documentation:**
    
    - **Summary:** Service responsible for orchestrating content publishing and scheduling workflows across different social media platforms.
    
**Namespace:** creativeflow.socialpublishing.application.services.publishing_orchestration_service  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/application/services/insights_aggregation_service.py  
**Description:** Fetches and aggregates insights like trending hashtags and best times to post from social platforms.  
**Template:** Python Service Class  
**Dependency Level:** 3  
**Name:** insights_aggregation_service  
**Type:** Service  
**Relative Path:** application/services/insights_aggregation_service  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** oauth_service  
**Type:** OAuthOrchestrationService  
**Attributes:** private  
    - **Name:** platform_clients  
**Type:** Dict[str, BaseSocialClient]  
**Attributes:** private  
    - **Name:** insights_cache  
**Type:** PlatformInsightsCache  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_trending_hashtags  
**Parameters:**
    
    - user_id: str
    - platform: str
    - keywords: List[str]
    - industry: Optional[str]
    
**Return Type:** List[HashtagSuggestion]  
**Attributes:** public|async  
    - **Name:** get_best_times_to_post  
**Parameters:**
    
    - user_id: str
    - platform: str
    - connection_id: UUID
    
**Return Type:** List[Dict[str, Any]]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - HashtagSuggestionFetching
    - BestTimeToPostFetching
    
**Requirement Ids:**
    
    - INT-002
    
**Purpose:** Provides content optimization insights by interacting with social media platform APIs.  
**Logic Description:** For a given platform and user context (keywords, connection), fetch a valid access token. Use the appropriate platform client to request hashtag suggestions or account insights (like best engagement times). Process and return the data. Implement caching for insights to avoid excessive API calls (using `PlatformInsightsCache`).  
**Documentation:**
    
    - **Summary:** Service responsible for fetching and processing content optimization insights from social media platforms.
    
**Namespace:** creativeflow.socialpublishing.application.services.insights_aggregation_service  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/application/exceptions.py  
**Description:** Custom exceptions for the application layer.  
**Template:** Python Exceptions  
**Dependency Level:** 1  
**Name:** exceptions  
**Type:** ExceptionHandling  
**Relative Path:** application/exceptions  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - CustomApplicationExceptions
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines custom exceptions specific to the application layer logic.  
**Logic Description:** Define exceptions like `OAuthConnectionError`, `PublishingError`, `InsufficientPermissionsError`, `PlatformApiError`, `TokenEncryptionError`.  
**Documentation:**
    
    - **Summary:** Contains custom exception classes for the application layer.
    
**Namespace:** creativeflow.socialpublishing.application.exceptions  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/socialpublishing/domain/__init__.py  
**Description:** Initializes the domain layer package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the domain layer Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the domain layer package containing core business logic and models.
    
**Namespace:** creativeflow.socialpublishing.domain  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/models/__init__.py  
**Description:** Initializes the domain models package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/models/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the domain models Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the domain models (entities, value objects) package.
    
**Namespace:** creativeflow.socialpublishing.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/models/social_connection.py  
**Description:** Domain entity representing a user's connection to a social media platform.  
**Template:** Python Data Class  
**Dependency Level:** 0  
**Name:** social_connection  
**Type:** Entity  
**Relative Path:** domain/models/social_connection  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** user_id  
**Type:** str  
**Attributes:** public  
    - **Name:** platform  
**Type:** str  
**Attributes:** public  
    - **Name:** external_user_id  
**Type:** str  
**Attributes:** public  
    - **Name:** external_display_name  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** access_token_encrypted  
**Type:** bytes  
**Attributes:** public  
    - **Name:** refresh_token_encrypted  
**Type:** Optional[bytes]  
**Attributes:** public  
    - **Name:** expires_at  
**Type:** Optional[datetime]  
**Attributes:** public  
    - **Name:** scopes  
**Type:** Optional[List[str]]  
**Attributes:** public  
    - **Name:** created_at  
**Type:** datetime  
**Attributes:** public  
    - **Name:** updated_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** is_token_expired  
**Parameters:**
    
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** update_tokens  
**Parameters:**
    
    - new_access_token_encrypted: bytes
    - new_refresh_token_encrypted: Optional[bytes]
    - new_expires_at: Optional[datetime]
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - SocialConnectionState
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Represents a user's authenticated connection to a social media platform, holding encrypted tokens and metadata.  
**Logic Description:** Define a dataclass or Pydantic BaseModel for SocialConnection. Include methods for checking token expiry and updating tokens. Encryption/decryption itself is a domain service concern, this entity holds the encrypted form.  
**Documentation:**
    
    - **Summary:** Domain entity for a social media connection, including encrypted tokens and expiry information.
    
**Namespace:** creativeflow.socialpublishing.domain.models.social_connection  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/models/publish_job.py  
**Description:** Domain entity representing a content publishing or scheduling job.  
**Template:** Python Data Class  
**Dependency Level:** 0  
**Name:** publish_job  
**Type:** Entity  
**Relative Path:** domain/models/publish_job  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** user_id  
**Type:** str  
**Attributes:** public  
    - **Name:** social_connection_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** platform  
**Type:** str  
**Attributes:** public  
    - **Name:** content_text  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** asset_urls  
**Type:** List[str]  
**Attributes:** public  
    - **Name:** platform_specific_options  
**Type:** Optional[Dict[str, Any]]  
**Attributes:** public  
    - **Name:** status  
**Type:** str  
**Attributes:** public  
**Notes:** e.g., Pending, Processing, Published, Scheduled, Failed, ContentRejected  
    - **Name:** scheduled_at  
**Type:** Optional[datetime]  
**Attributes:** public  
    - **Name:** published_at  
**Type:** Optional[datetime]  
**Attributes:** public  
    - **Name:** error_message  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** attempts  
**Type:** int  
**Attributes:** public  
    - **Name:** post_url  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** created_at  
**Type:** datetime  
**Attributes:** public  
    - **Name:** updated_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** mark_as_processing  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** mark_as_published  
**Parameters:**
    
    - post_url: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** mark_as_failed  
**Parameters:**
    
    - error: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** mark_as_content_rejected  
**Parameters:**
    
    - reason: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** increment_attempts  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - PublishJobStateManagement
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Represents a job to publish or schedule content, tracking its state and details.  
**Logic Description:** Define a dataclass or Pydantic BaseModel for PublishJob. Include methods for state transitions (e.g., pending to processing, processing to published/failed). This entity encapsulates all information needed to perform and track a publishing action.  
**Documentation:**
    
    - **Summary:** Domain entity for a publishing job, including content details, target, schedule, and status.
    
**Namespace:** creativeflow.socialpublishing.domain.models.publish_job  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/models/platform_insights.py  
**Description:** Domain value object or entity representing fetched platform insights (e.g., hashtags, best times).  
**Template:** Python Data Class  
**Dependency Level:** 0  
**Name:** platform_insights  
**Type:** ValueObject  
**Relative Path:** domain/models/platform_insights  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - ValueObject
    
**Members:**
    
    - **Name:** platform  
**Type:** str  
**Attributes:** public  
    - **Name:** insight_type  
**Type:** str  
**Attributes:** public  
**Notes:** e.g., 'trending_hashtags', 'best_post_times'  
    - **Name:** data  
**Type:** Any  
**Attributes:** public  
**Notes:** Could be List[HashtagSuggestionVO] or List[TimeSlotVO]  
    - **Name:** generated_at  
**Type:** datetime  
**Attributes:** public  
    - **Name:** context_params  
**Type:** Optional[Dict[str,Any]]  
**Attributes:** public  
**Notes:** Parameters used to generate this insight, e.g. keywords  
    
**Methods:**
    
    
**Implemented Features:**
    
    - PlatformInsightRepresentation
    
**Requirement Ids:**
    
    - INT-002
    
**Purpose:** Represents content optimization insights fetched from social media platforms.  
**Logic Description:** Define a dataclass/Pydantic BaseModel for PlatformInsights. Ensure it's immutable if a Value Object. Can be specialized for `HashtagSuggestion` and `BestPostTime` value objects.  
**Documentation:**
    
    - **Summary:** Domain model for storing and representing social media platform insights.
    
**Namespace:** creativeflow.socialpublishing.domain.models.platform_insights  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/repositories/__init__.py  
**Description:** Initializes the domain repositories interfaces package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/repositories/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the domain repositories Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the domain repository interfaces package.
    
**Namespace:** creativeflow.socialpublishing.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/repositories/social_connection_repository.py  
**Description:** Interface for the SocialConnection repository.  
**Template:** Python ABC Interface  
**Dependency Level:** 1  
**Name:** social_connection_repository  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/social_connection_repository  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - connection_id: UUID
    
**Return Type:** Optional[SocialConnection]  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_by_user_and_platform  
**Parameters:**
    
    - user_id: str
    - platform: str
    
**Return Type:** Optional[SocialConnection]  
**Attributes:** public|abstractmethod|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    
**Return Type:** List[SocialConnection]  
**Attributes:** public|abstractmethod|async  
    - **Name:** save  
**Parameters:**
    
    - connection: SocialConnection
    
**Return Type:** SocialConnection  
**Attributes:** public|abstractmethod|async  
    - **Name:** delete  
**Parameters:**
    
    - connection_id: UUID
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - SocialConnectionPersistenceContract
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines the contract for data access operations related to SocialConnection entities.  
**Logic Description:** Define an abstract base class (ABC) with abstract methods for CRUD operations on SocialConnection entities. This interface will be implemented by the infrastructure layer.  
**Documentation:**
    
    - **Summary:** Abstract interface defining data persistence operations for SocialConnection entities.
    
**Namespace:** creativeflow.socialpublishing.domain.repositories.social_connection_repository  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/repositories/publish_job_repository.py  
**Description:** Interface for the PublishJob repository.  
**Template:** Python ABC Interface  
**Dependency Level:** 1  
**Name:** publish_job_repository  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/publish_job_repository  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - job_id: UUID
    
**Return Type:** Optional[PublishJob]  
**Attributes:** public|abstractmethod|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    - platform: Optional[str]
    - status: Optional[str]
    
**Return Type:** List[PublishJob]  
**Attributes:** public|abstractmethod|async  
    - **Name:** save  
**Parameters:**
    
    - job: PublishJob
    
**Return Type:** PublishJob  
**Attributes:** public|abstractmethod|async  
    - **Name:** find_pending_scheduled_jobs  
**Parameters:**
    
    - limit: int
    
**Return Type:** List[PublishJob]  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - PublishJobPersistenceContract
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines the contract for data access operations related to PublishJob entities.  
**Logic Description:** Define an abstract base class (ABC) with abstract methods for CRUD operations and querying PublishJob entities, including finding jobs due for scheduled publishing.  
**Documentation:**
    
    - **Summary:** Abstract interface defining data persistence operations for PublishJob entities.
    
**Namespace:** creativeflow.socialpublishing.domain.repositories.publish_job_repository  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/services/__init__.py  
**Description:** Initializes the domain services package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/services/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the domain services Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the domain services package.
    
**Namespace:** creativeflow.socialpublishing.domain.services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/services/token_encryption_service.py  
**Description:** Interface for encrypting and decrypting sensitive tokens.  
**Template:** Python ABC Interface  
**Dependency Level:** 1  
**Name:** token_encryption_service  
**Type:** DomainServiceInterface  
**Relative Path:** domain/services/token_encryption_service  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - StrategyPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** encrypt_token  
**Parameters:**
    
    - token: str
    
**Return Type:** bytes  
**Attributes:** public|abstractmethod  
    - **Name:** decrypt_token  
**Parameters:**
    
    - encrypted_token: bytes
    
**Return Type:** str  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - TokenEncryptionContract
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines the contract for encrypting and decrypting OAuth tokens.  
**Logic Description:** Define an abstract base class (ABC) with methods for encryption and decryption. This decouples the domain from specific encryption algorithms.  
**Documentation:**
    
    - **Summary:** Abstract interface for services that handle encryption and decryption of sensitive tokens.
    
**Namespace:** creativeflow.socialpublishing.domain.services.token_encryption_service  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/services/platform_policy_validator.py  
**Description:** Domain service to validate content against platform-specific policies before attempting to publish.  
**Template:** Python Service Class  
**Dependency Level:** 2  
**Name:** platform_policy_validator  
**Type:** DomainService  
**Relative Path:** domain/services/platform_policy_validator  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_content_for_platform  
**Parameters:**
    
    - platform: str
    - content_text: Optional[str]
    - assets: List[GeneratedAsset]
    
**Return Type:** Tuple[bool, Optional[str]]  
**Attributes:** public|async  
**Notes:** Returns (is_valid, error_message)  
    
**Implemented Features:**
    
    - ContentPolicyValidation
    
**Requirement Ids:**
    
    - INT-001
    - INT-002
    
**Purpose:** Encapsulates logic for checking if content adheres to requirements of a specific social media platform.  
**Logic Description:** Implement validation rules based on platform (e.g., character limits for Twitter, image dimensions for Instagram, video length for TikTok). This service might use platform client utilities or hardcoded rules based on public platform guidelines. Logic to check if assets dimensions (from `GeneratedAsset` metadata) are suitable for the target platform and format.  
**Documentation:**
    
    - **Summary:** Domain service responsible for validating content against rules and policies of different social media platforms.
    
**Namespace:** creativeflow.socialpublishing.domain.services.platform_policy_validator  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/domain/exceptions.py  
**Description:** Custom exceptions for the domain layer.  
**Template:** Python Exceptions  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** ExceptionHandling  
**Relative Path:** domain/exceptions  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - CustomDomainExceptions
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines custom exceptions specific to domain logic rules and invariants.  
**Logic Description:** Define exceptions like `InvalidSocialPlatformError`, `TokenExpiredError`, `ContentValidationError`, `JobStateTransitionError`.  
**Documentation:**
    
    - **Summary:** Contains custom exception classes for the domain layer, representing violations of business rules.
    
**Namespace:** creativeflow.socialpublishing.domain.exceptions  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/__init__.py  
**Description:** Initializes the infrastructure layer package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the infrastructure layer Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the infrastructure layer package, containing implementations for external concerns.
    
**Namespace:** creativeflow.socialpublishing.infrastructure  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/__init__.py  
**Description:** Initializes the database infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the database infrastructure Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the database interaction package within infrastructure.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/sqlalchemy_models.py  
**Description:** SQLAlchemy ORM models for database tables.  
**Template:** Python SQLAlchemy Models  
**Dependency Level:** 1  
**Name:** sqlalchemy_models  
**Type:** DataModel  
**Relative Path:** infrastructure/database/sqlalchemy_models  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DatabaseTableDefinitions
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines SQLAlchemy ORM classes that map to database tables (SocialConnection, PublishJob).  
**Logic Description:** Define `SocialConnectionSQL` and `PublishJobSQL` classes inheriting from SQLAlchemy's declarative base. Map attributes from domain models to table columns, including relationships and constraints. These models are used by repository implementations.  
**Documentation:**
    
    - **Summary:** Contains SQLAlchemy ORM model definitions corresponding to the database schema.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.sqlalchemy_models  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/repositories/__init__.py  
**Description:** Initializes the infrastructure repositories package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/repositories/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the repository implementations Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the repository implementations package.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/repositories/sql_social_connection_repository.py  
**Description:** SQLAlchemy implementation of the ISocialConnectionRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sql_social_connection_repository  
**Type:** RepositoryImplementation  
**Relative Path:** infrastructure/database/repositories/sql_social_connection_repository  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - ORM
    
**Members:**
    
    - **Name:** db_session  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - connection_id: UUID
    
**Return Type:** Optional[SocialConnection]  
**Attributes:** public|async  
    - **Name:** get_by_user_and_platform  
**Parameters:**
    
    - user_id: str
    - platform: str
    
**Return Type:** Optional[SocialConnection]  
**Attributes:** public|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    
**Return Type:** List[SocialConnection]  
**Attributes:** public|async  
    - **Name:** save  
**Parameters:**
    
    - connection: SocialConnection
    
**Return Type:** SocialConnection  
**Attributes:** public|async  
    - **Name:** delete  
**Parameters:**
    
    - connection_id: UUID
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** _map_to_domain  
**Parameters:**
    
    - db_conn: SocialConnectionSQL
    
**Return Type:** SocialConnection  
**Attributes:** private|static  
    - **Name:** _map_to_db_model  
**Parameters:**
    
    - domain_conn: SocialConnection
    - db_conn_sql: Optional[SocialConnectionSQL] = None
    
**Return Type:** SocialConnectionSQL  
**Attributes:** private|static  
    
**Implemented Features:**
    
    - SocialConnectionPersistence
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides concrete data access logic for SocialConnection entities using SQLAlchemy and PostgreSQL.  
**Logic Description:** Implement the methods defined in `ISocialConnectionRepository`. Use SQLAlchemy session for database operations. Include mapping functions to convert between domain entities and SQLAlchemy models.  
**Documentation:**
    
    - **Summary:** SQLAlchemy-based implementation for persisting and retrieving SocialConnection domain entities.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.repositories.sql_social_connection_repository  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/repositories/sql_publish_job_repository.py  
**Description:** SQLAlchemy implementation of the IPublishJobRepository interface.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 3  
**Name:** sql_publish_job_repository  
**Type:** RepositoryImplementation  
**Relative Path:** infrastructure/database/repositories/sql_publish_job_repository  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - ORM
    
**Members:**
    
    - **Name:** db_session  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - job_id: UUID
    
**Return Type:** Optional[PublishJob]  
**Attributes:** public|async  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    - platform: Optional[str]
    - status: Optional[str]
    
**Return Type:** List[PublishJob]  
**Attributes:** public|async  
    - **Name:** save  
**Parameters:**
    
    - job: PublishJob
    
**Return Type:** PublishJob  
**Attributes:** public|async  
    - **Name:** find_pending_scheduled_jobs  
**Parameters:**
    
    - limit: int
    
**Return Type:** List[PublishJob]  
**Attributes:** public|async  
    - **Name:** _map_to_domain  
**Parameters:**
    
    - db_job: PublishJobSQL
    
**Return Type:** PublishJob  
**Attributes:** private|static  
    - **Name:** _map_to_db_model  
**Parameters:**
    
    - domain_job: PublishJob
    - db_job_sql: Optional[PublishJobSQL] = None
    
**Return Type:** PublishJobSQL  
**Attributes:** private|static  
    
**Implemented Features:**
    
    - PublishJobPersistence
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides concrete data access logic for PublishJob entities using SQLAlchemy and PostgreSQL.  
**Logic Description:** Implement the methods defined in `IPublishJobRepository`. Use SQLAlchemy session for database operations. Include mapping functions for domain/db model conversion. Method `find_pending_scheduled_jobs` queries for jobs with status 'Scheduled' and `scheduled_at` in the past.  
**Documentation:**
    
    - **Summary:** SQLAlchemy-based implementation for persisting and retrieving PublishJob domain entities.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.repositories.sql_publish_job_repository  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/session_manager.py  
**Description:** Manages SQLAlchemy database sessions and engine creation.  
**Template:** Python SQLAlchemy Session  
**Dependency Level:** 2  
**Name:** session_manager  
**Type:** DatabaseConnector  
**Relative Path:** infrastructure/database/session_manager  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** engine  
**Type:** AsyncEngine  
**Attributes:** private|static  
    - **Name:** AsyncSessionLocal  
**Type:** sessionmaker  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** init_db  
**Parameters:**
    
    - database_url: str
    
**Return Type:** None  
**Attributes:** public|static  
    - **Name:** get_session  
**Parameters:**
    
    
**Return Type:** Generator[AsyncSession, None, None]  
**Attributes:** public|static|async  
    
**Implemented Features:**
    
    - DatabaseConnectionManagement
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Handles creation of database engine and provides sessions for database interaction.  
**Logic Description:** Initialize SQLAlchemy async engine using `DATABASE_URL` from config. Create an `AsyncSessionLocal` session factory. Provide a dependency `get_session` that yields a session and ensures it's closed.  
**Documentation:**
    
    - **Summary:** Provides SQLAlchemy database engine and session management utilities.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.session_manager  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/alembic/__init__.py  
**Description:** Makes the alembic directory a Python package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/alembic/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the Alembic package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the Alembic migrations package.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.alembic  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/alembic/env.py  
**Description:** Alembic environment configuration file.  
**Template:** Python Alembic Env  
**Dependency Level:** 3  
**Name:** env  
**Type:** DatabaseMigrationConfig  
**Relative Path:** infrastructure/database/alembic/env  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** run_migrations_offline  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** do_run_migrations  
**Parameters:**
    
    - connection
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** run_migrations_online  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - AlembicConfiguration
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Configures Alembic for database schema migrations, pointing to SQLAlchemy models and database URL.  
**Logic Description:** Standard Alembic env.py setup. Configure `target_metadata` to point to `sqlalchemy_models.Base.metadata`. Use `DATABASE_URL` from `config.py`. Configure for asynchronous migration runs.  
**Documentation:**
    
    - **Summary:** Alembic environment script for database schema migration management.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.alembic.env  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/alembic/script.py.mako  
**Description:** Alembic migration script template.  
**Template:** Python Alembic Mako  
**Dependency Level:** 3  
**Name:** script.py  
**Type:** DatabaseMigrationTemplate  
**Relative Path:** infrastructure/database/alembic/script.py  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Mako template used by Alembic to generate new migration scripts.  
**Logic Description:** Standard Alembic Mako template. No custom logic usually needed here.  
**Documentation:**
    
    - **Summary:** Mako template for generating Alembic migration scripts.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.alembic  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/database/alembic/versions/__init__.py  
**Description:** Initializes the Alembic versions package.  
**Template:** Python Package Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/alembic/versions/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the Alembic versions directory.  
**Logic Description:** Empty file, standard Python package initializer. Migration scripts will be generated here.  
**Documentation:**
    
    - **Summary:** Package containing individual Alembic migration scripts.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.database.alembic.versions  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/__init__.py  
**Description:** Initializes the external API clients package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/clients/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the external API clients Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the package containing clients for interacting with external social media APIs.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/base_social_client.py  
**Description:** Abstract base class or common utilities for social media API clients.  
**Template:** Python ABC Class  
**Dependency Level:** 2  
**Name:** base_social_client  
**Type:** ExternalServiceClientBase  
**Relative Path:** infrastructure/clients/base_social_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** http_client  
**Type:** httpx.AsyncClient  
**Attributes:** protected  
    - **Name:** config  
**Type:** Settings  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** get_oauth_url  
**Parameters:**
    
    - state: str
    - redirect_uri: str
    
**Return Type:** str  
**Attributes:** public|abstractmethod|async  
    - **Name:** exchange_code_for_token  
**Parameters:**
    
    - code: str
    - redirect_uri: str
    
**Return Type:** Dict[str, Any]  
**Attributes:** public|abstractmethod|async  
**Notes:** Returns access_token, refresh_token, expires_in, etc.  
    - **Name:** refresh_access_token  
**Parameters:**
    
    - refresh_token: str
    
**Return Type:** Dict[str, Any]  
**Attributes:** public|abstractmethod|async  
    - **Name:** publish_content  
**Parameters:**
    
    - access_token: str
    - text: Optional[str]
    - assets: List[GeneratedAsset]
    - options: Optional[Dict[str, Any]]
    
**Return Type:** str  
**Attributes:** public|abstractmethod|async  
**Notes:** Returns post URL or ID  
    - **Name:** get_user_profile  
**Parameters:**
    
    - access_token: str
    
**Return Type:** Dict[str, Any]  
**Attributes:** public|abstractmethod|async  
**Notes:** Returns external user ID, display name  
    - **Name:** get_trending_hashtags  
**Parameters:**
    
    - access_token: Optional[str]
    - keywords: List[str]
    - industry: Optional[str]
    
**Return Type:** List[str]  
**Attributes:** public|abstractmethod|async  
    - **Name:** get_best_post_times  
**Parameters:**
    
    - access_token: str
    
**Return Type:** List[Dict[str, Any]]  
**Attributes:** public|abstractmethod|async  
    - **Name:** _handle_api_error  
**Parameters:**
    
    - response: httpx.Response
    
**Return Type:** None  
**Attributes:** protected|async  
**Notes:** Raises PlatformApiError  
    
**Implemented Features:**
    
    - BaseSocialAPIInteraction
    
**Requirement Ids:**
    
    - INT-001
    - INT-002
    
**Purpose:** Defines a common interface and shared utilities for social media platform API clients.  
**Logic Description:** Use ABC for interface definition. Initialize with httpx.AsyncClient. Implement common error handling, rate limit awareness (using `_client_utils`), and potentially retry logic here or in a utility module used by clients.  
**Documentation:**
    
    - **Summary:** Abstract base class for social media API clients, defining common methods and handling.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.base_social_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/_client_utils.py  
**Description:** Utility functions for social media clients, e.g., retry logic, specific error mapping.  
**Template:** Python Utility Module  
**Dependency Level:** 2  
**Name:** _client_utils  
**Type:** Utility  
**Relative Path:** infrastructure/clients/_client_utils  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - CircuitBreaker
    
**Members:**
    
    
**Methods:**
    
    - **Name:** map_platform_error  
**Parameters:**
    
    - platform_name: str
    - status_code: int
    - response_json: Optional[dict]
    
**Return Type:** ApplicationException  
**Attributes:** public  
    - **Name:** http_retry_decorator  
**Parameters:**
    
    - max_retries: int = 3
    - delay_seconds: float = 1.0
    - backoff_factor: float = 2.0
    
**Return Type:** Callable  
**Attributes:** public  
    
**Implemented Features:**
    
    - ApiClientErrorHandling
    - ApiClientRetry
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides common utilities for social media API clients, such as error mapping and retry mechanisms.  
**Logic Description:** Implement a decorator for retrying HTTP requests with exponential backoff. Create a function to map platform-specific error codes/messages to standardized internal application exceptions (e.g., `PlatformApiError`, `RateLimitError`).  
**Documentation:**
    
    - **Summary:** Contains utility functions shared among different social media API clients, like retry logic and error normalization.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients._client_utils  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/instagram_client.py  
**Description:** Client for interacting with the Instagram Graph API.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** instagram_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/instagram_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** publish_post  
**Parameters:**
    
    - access_token: str
    - image_url: str
    - caption: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    - **Name:** publish_story  
**Parameters:**
    
    - access_token: str
    - media_url: str
    - media_type: str
    
**Return Type:** str  
**Attributes:** public|async  
    - **Name:** publish_reel  
**Parameters:**
    
    - access_token: str
    - video_url: str
    - caption: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - InstagramPublishing
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with Instagram Graph API for publishing posts, stories, and reels.  
**Logic Description:** Inherit from BaseSocialClient. Implement methods specific to Instagram API (e.g., content upload, post creation, story creation). Use `httpx` for API calls. Handle Instagram-specific error codes and rate limits, leveraging `_client_utils`. Use `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET` from config.  
**Documentation:**
    
    - **Summary:** Client for Instagram Graph API, supporting content publishing and other platform-specific interactions.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.instagram_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/facebook_client.py  
**Description:** Client for interacting with the Facebook Graph API.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** facebook_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/facebook_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** publish_to_page  
**Parameters:**
    
    - access_token: str
    - page_id: str
    - message: Optional[str]
    - link: Optional[str]
    - image_url: Optional[str]
    - video_url: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - FacebookPublishing
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with Facebook Graph API for page management and content publishing.  
**Logic Description:** Inherit from BaseSocialClient. Implement methods for publishing to Facebook Pages. Use `httpx` for API calls. Handle Facebook-specific error responses and rate limits. Use `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET` from config.  
**Documentation:**
    
    - **Summary:** Client for Facebook Graph API, supporting content publishing to Pages.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.facebook_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/linkedin_client.py  
**Description:** Client for interacting with the LinkedIn API.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** linkedin_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/linkedin_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** publish_to_company_page  
**Parameters:**
    
    - access_token: str
    - company_urn: str
    - text: str
    - media_asset_urn: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    - **Name:** publish_to_personal_profile  
**Parameters:**
    
    - access_token: str
    - text: str
    
**Return Type:** str  
**Attributes:** public|async  
**Notes:** If API allows  
    
**Implemented Features:**
    
    - LinkedInPublishing
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with LinkedIn API for publishing to company pages and personal profiles (if allowed).  
**Logic Description:** Inherit from BaseSocialClient. Implement methods for publishing. Use `httpx`. Handle LinkedIn-specific errors and rate limits. Use `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET` from config.  
**Documentation:**
    
    - **Summary:** Client for LinkedIn API, supporting content publishing.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.linkedin_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/twitter_client.py  
**Description:** Client for interacting with the Twitter API v2 (X API).  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** twitter_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/twitter_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** post_tweet  
**Parameters:**
    
    - access_token: str
    - text: str
    - media_ids: Optional[List[str]]
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - TwitterPublishing
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with Twitter API v2 for posting tweets.  
**Logic Description:** Inherit from BaseSocialClient. Use `TWITTER_API_KEY`, `TWITTER_API_SECRET_KEY`. Implement tweet posting, possibly media upload as a separate step if required by API v2. Use `httpx`.  
**Documentation:**
    
    - **Summary:** Client for Twitter API v2 (X API), supporting tweet creation.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.twitter_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/pinterest_client.py  
**Description:** Client for interacting with the Pinterest API.  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** pinterest_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/pinterest_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_pin  
**Parameters:**
    
    - access_token: str
    - board_id: str
    - image_url: str
    - title: Optional[str]
    - description: Optional[str]
    - link: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - PinterestPinCreation
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with Pinterest API for creating Pins.  
**Logic Description:** Inherit from BaseSocialClient. Use `PINTEREST_APP_ID`, `PINTEREST_APP_SECRET`. Implement Pin creation. Use `httpx`.  
**Documentation:**
    
    - **Summary:** Client for Pinterest API, supporting Pin creation.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.pinterest_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/clients/tiktok_client.py  
**Description:** Client for interacting with the TikTok API (if available and suitable for direct publishing).  
**Template:** Python HTTP Client  
**Dependency Level:** 3  
**Name:** tiktok_client  
**Type:** ExternalServiceClient  
**Relative Path:** infrastructure/clients/tiktok_client  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** publish_video  
**Parameters:**
    
    - access_token: str
    - video_url: str
    - caption: Optional[str]
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - TikTokPublishing
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Implements methods to interact with TikTok API for video publishing, if supported by the API.  
**Logic Description:** Inherit from BaseSocialClient. Check for official TikTok publishing API availability. If available, implement video upload and posting. Use `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`. Use `httpx`.  
**Documentation:**
    
    - **Summary:** Client for TikTok API, supporting video publishing if and when API capabilities allow.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.clients.tiktok_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/security/__init__.py  
**Description:** Initializes the security infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/security/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the security related infrastructure Python package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the security infrastructure package, e.g., for encryption services.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.security  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/security/aes_gcm_encryption_service.py  
**Description:** Implementation of ITokenEncryptionService using AES-GCM.  
**Template:** Python Cryptography Service  
**Dependency Level:** 2  
**Name:** aes_gcm_encryption_service  
**Type:** EncryptionServiceImplementation  
**Relative Path:** infrastructure/security/aes_gcm_encryption_service  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - StrategyPattern
    
**Members:**
    
    - **Name:** key  
**Type:** bytes  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** encrypt_token  
**Parameters:**
    
    - token: str
    
**Return Type:** bytes  
**Attributes:** public  
    - **Name:** decrypt_token  
**Parameters:**
    
    - encrypted_token: bytes
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - TokenEncryptionAESGCM
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides AES-GCM encryption and decryption for sensitive tokens.  
**Logic Description:** Implement the `ITokenEncryptionService` interface. Use the `cryptography` library for AES-GCM encryption. Load the encryption key securely from configuration (`config.AES_KEY`). Handle padding, nonce generation, and tag verification for GCM.  
**Documentation:**
    
    - **Summary:** Implements token encryption and decryption using AES-GCM algorithm.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.security.aes_gcm_encryption_service  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/logging/__init__.py  
**Description:** Initializes the logging infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/logging/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the logging setup package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the logging configuration package.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.logging  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/logging/config.py  
**Description:** Configuration for structured logging.  
**Template:** Python Logging Config  
**Dependency Level:** 2  
**Name:** config  
**Type:** LoggingConfiguration  
**Relative Path:** infrastructure/logging/config  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str
    
**Return Type:** None  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - StructuredLoggingSetup
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Configures structured logging for the application (e.g., JSON format).  
**Logic Description:** Set up Python's standard `logging` module. Configure a formatter for JSON output. Set log level based on application config. Potentially integrate with external logging services if needed (though that's more CI/CD/Ops concern for agent setup).  
**Documentation:**
    
    - **Summary:** Sets up structured logging for the application, including format and level.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.logging.config  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/caching/__init__.py  
**Description:** Initializes the caching infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/caching/__init__  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the caching mechanisms package.  
**Logic Description:** Empty file, standard Python package initializer.  
**Documentation:**
    
    - **Summary:** Initializes the caching implementation package.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.caching  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/socialpublishing/infrastructure/caching/platform_insights_cache.py  
**Description:** Caching mechanism for platform insights (e.g., hashtags, best times to post) using Redis or an in-memory cache with TTL.  
**Template:** Python Cache Client  
**Dependency Level:** 3  
**Name:** platform_insights_cache  
**Type:** CacheClient  
**Relative Path:** infrastructure/caching/platform_insights_cache  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    - Caching
    
**Members:**
    
    - **Name:** redis_client  
**Type:** Optional[Redis]  
**Attributes:** private  
    - **Name:** ttl_seconds  
**Type:** int  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_insights  
**Parameters:**
    
    - platform: str
    - insight_type: str
    - context_key: str
    
**Return Type:** Optional[Any]  
**Attributes:** public|async  
    - **Name:** set_insights  
**Parameters:**
    
    - platform: str
    - insight_type: str
    - context_key: str
    - data: Any
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - InsightsCaching
    
**Requirement Ids:**
    
    - INT-002
    
**Purpose:** Caches platform insights to reduce API calls to social media platforms and improve response times.  
**Logic Description:** Implement a cache client that can store and retrieve insights data. Use Redis if available (from REPO-SHARED-LIBS-001 or configured directly), otherwise an in-memory cache with Time-To-Live (TTL) could be a simpler start. The key should be composite, e.g., f'{platform}:{insight_type}:{context_key}'.  
**Documentation:**
    
    - **Summary:** Provides caching for social media platform insights to optimize performance and reduce external API calls.
    
**Namespace:** creativeflow.socialpublishing.infrastructure.caching.platform_insights_cache  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** pyproject.toml  
**Description:** Python project configuration file using PEP 518. Defines project metadata, dependencies, and build system (e.g., Poetry, Flit, or Hatch).  
**Template:** Python Pyproject.toml  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** BuildConfiguration  
**Relative Path:** ../pyproject  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - ProjectDefinition
    - DependencyManagement
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Defines the project structure, dependencies, and build tool configuration for the Python application.  
**Logic Description:** Specify project name, version, authors. List dependencies: fastapi, uvicorn[standard], pydantic, sqlalchemy[asyncpg], psycopg2-binary, httpx, cryptography, alembic. Configure build tool (e.g., poetry). Define scripts for running the app, tests, migrations.  
**Documentation:**
    
    - **Summary:** Project configuration file defining metadata, dependencies, and build system details.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment file showing required environment variables.  
**Template:** Environment Example  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** ConfigurationTemplate  
**Relative Path:** ../.env.example  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Provides a template for developers to create their local .env file with necessary configurations.  
**Logic Description:** List all environment variables defined in config.py with placeholder or example values. E.g., DATABASE_URL=postgresql+asyncpg://user:pass@host/db, AES_KEY=your_secret_aes_key_here, INSTAGRAM_APP_ID=...  
**Documentation:**
    
    - **Summary:** Example environment variable file to guide developers in setting up their local development environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** alembic.ini  
**Description:** Configuration file for Alembic database migrations.  
**Template:** Alembic Ini  
**Dependency Level:** 1  
**Name:** alembic  
**Type:** DatabaseMigrationConfig  
**Relative Path:** ../alembic  
**Repository Id:** REPO-SOCIALPUB-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AlembicSetup
    
**Requirement Ids:**
    
    - INT-001
    
**Purpose:** Main configuration file for Alembic, pointing to the script location and database URL.  
**Logic Description:** Set `script_location` to `src/creativeflow/socialpublishing/infrastructure/database/alembic`. Configure `sqlalchemy.url` to be read from the application's config (e.g., via an environment variable or a helper script).  
**Documentation:**
    
    - **Summary:** Configuration file for the Alembic database migration tool.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Infrastructure
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableTikTokPublishing
  - EnableLinkedInPersonalProfilePublishing
  - EnableAdvancedInsightsFetching
  
- **Database Configs:**
  
  - DATABASE_URL
  - DB_ECHO_LOG
  
- **Api Keys:**
  
  - INSTAGRAM_APP_ID
  - INSTAGRAM_APP_SECRET
  - FACEBOOK_APP_ID
  - FACEBOOK_APP_SECRET
  - LINKEDIN_CLIENT_ID
  - LINKEDIN_CLIENT_SECRET
  - TWITTER_API_KEY
  - TWITTER_API_SECRET_KEY
  - TWITTER_ACCESS_TOKEN
  - TWITTER_ACCESS_TOKEN_SECRET
  - PINTEREST_APP_ID
  - PINTEREST_APP_SECRET
  - TIKTOK_CLIENT_KEY
  - TIKTOK_CLIENT_SECRET
  
- **Encryption Keys:**
  
  - AES_ENCRYPTION_KEY
  
- **Service Endpoints:**
  
  - AUTH_SERVICE_URL
  
- **Cache Configs:**
  
  - REDIS_URL
  - INSIGHTS_CACHE_TTL_SECONDS
  


---

