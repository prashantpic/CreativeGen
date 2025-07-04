# Software Design Specification: CreativeFlow.SocialPublishingService

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.SocialPublishingService`. This microservice is responsible for managing connections to various social media platforms, enabling users to publish and schedule content, and fetching content optimization insights. It serves as a backend component, exposing internal REST APIs for consumption by other services within the CreativeFlow AI platform, primarily the API Gateway or a Backend-for-Frontend (BFF).

### 1.2 Scope
The scope of this service includes:
*   Securely managing user connections to social media platforms (Instagram, Facebook, LinkedIn, Twitter/X, Pinterest, TikTok) via OAuth 2.0.
*   Storing and refreshing OAuth tokens with AES-256 encryption at rest.
*   Providing functionalities for direct publishing and scheduling of creative content to connected social accounts.
*   Handling API errors, rate limits, and permission changes from social media platforms.
*   Fetching platform-specific content optimization insights such as trending hashtags and best times to post, where APIs permit.
*   Validating content against basic platform policies (e.g., character limits, media types) before publishing attempts.

Out of scope for this service are:
*   User interface elements for managing connections or publishing (handled by frontend applications).
*   AI content generation (handled by the AI Generation Orchestration Service).
*   Complex content editing or real-time collaboration on creatives.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **API:** Application Programming Interface
*   **OAuth:** Open Authorization
*   **JWT:** JSON Web Token
*   **CRUD:** Create, Read, Update, Delete
*   **Pydantic:** Python data validation library
*   **SQLAlchemy:** Python SQL toolkit and Object Relational Mapper (ORM)
*   **FastAPI:** Modern, fast (high-performance) web framework for building APIs with Python
*   **Alembic:** Database migration tool for SQLAlchemy
*   **httpx:** A fully featured HTTP client for Python 3, which provides sync and async APIs.
*   **AES-GCM:** Advanced Encryption Standard - Galois/Counter Mode (an authenticated encryption algorithm)
*   **SDK:** Software Development Kit
*   **SDS:** Software Design Specification
*   **CI/CD:** Continuous Integration / Continuous Deployment
*   **DB:** Database
*   **VO:** Value Object
*   **DTO:** Data Transfer Object
*   **TTL:** Time To Live (for cache)
*   **KMS:** Key Management Service (though this service uses a configured key, actual KMS interaction is abstracted)
*   **RDBMS:** Relational Database Management System

## 2. System Overview
The `CreativeFlow.SocialPublishingService` is a Python FastAPI-based microservice. It follows a layered architecture internally:
*   **API Layer:** Handles incoming HTTP requests, request validation (Pydantic), and response formatting. Composed of FastAPI routers.
*   **Application Layer:** Contains service classes that orchestrate business logic, coordinate domain entities, repositories, and external client interactions.
*   **Domain Layer:** Encapsulates core business entities, value objects, repository interfaces, and domain-specific services (e.g., token encryption interface).
*   **Infrastructure Layer:** Implements interfaces defined in the domain layer, handling external concerns such as database interactions (SQLAlchemy), communication with social media platform APIs (HTTP clients/SDKs), encryption, logging, and caching.

It interacts with:
*   **PostgreSQL Database (`REPO-POSTGRES-DB-001`):** For storing social connection details, publishing job statuses, and potentially cached insights.
*   **Authentication Service (`REPO-AUTH-SERVICE-001`):** Implicitly, for validating user identity based on tokens passed by the API Gateway.
*   **Shared Libraries (`REPO-SHARED-LIBS-001`):** For common utilities, potentially including JWT validation helpers or base error types.
*   **External Social Media Platform APIs:** For OAuth flows, publishing content, and fetching insights.

## 3. Configuration (`src/creativeflow/socialpublishing/config.py`)
The service utilizes Pydantic's `BaseSettings` for managing configurations, loaded from environment variables or a `.env` file.

**Class: `Settings(BaseSettings)`**
*   `DATABASE_URL: str`: SQLAlchemy asynchronous database connection string (e.g., `postgresql+asyncpg://user:pass@host:port/db`).
*   `AES_KEY: str`: Secret key for AES-GCM encryption/decryption of OAuth tokens (must be 32 bytes, base64 encoded).
*   `INSTAGRAM_APP_ID: str`
*   `INSTAGRAM_APP_SECRET: str`
*   `FACEBOOK_APP_ID: str`
*   `FACEBOOK_APP_SECRET: str`
*   `LINKEDIN_CLIENT_ID: str`
*   `LINKEDIN_CLIENT_SECRET: str`
*   `TWITTER_API_KEY: str`
*   `TWITTER_API_SECRET_KEY: str`
    *   `TWITTER_ACCESS_TOKEN: Optional[str] = None` (For app-only auth if needed by Tweepy or X API v2)
    *   `TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None` (For app-only auth)
    *   `TWITTER_BEARER_TOKEN: Optional[str] = None` (For X API v2 app-only context)
*   `PINTEREST_APP_ID: str`
*   `PINTEREST_APP_SECRET: str`
*   `TIKTOK_CLIENT_KEY: Optional[str] = None`
*   `TIKTOK_CLIENT_SECRET: Optional[str] = None`
*   `AUTH_SERVICE_URL: str`: URL for the internal authentication service (if direct validation is needed beyond gateway).
*   `LOG_LEVEL: str = "INFO"`: Logging level (e.g., DEBUG, INFO, WARNING, ERROR).
*   `SERVICE_BASE_URL: str`: The base URL of this service itself, used for constructing callback URLs for OAuth.
*   `REDIS_URL: Optional[str] = None`: URL for Redis instance for caching insights.
*   `INSIGHTS_CACHE_TTL_SECONDS: int = 3600`: Default TTL for cached insights.
*   `MAX_API_RETRIES: int = 3`
*   `API_RETRY_DELAY_SECONDS: float = 1.0`
*   `API_RETRY_BACKOFF_FACTOR: float = 2.0`

    python
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    

**Function: `get_settings() -> Settings`**
*   Uses `functools.lru_cache` to load settings once.
*   Returns an instance of `Settings`.

## 4. API Design (Internal REST API - Version 1)

Base path: `/api/v1`

Authentication: Assumes JWT Bearer token provided by API Gateway, containing `user_id`. The `get_current_user_id` dependency will handle token validation and extraction.

### 4.1 Connections Router (`src/creativeflow/socialpublishing/api/v1/routers/connections_router.py`)
Tag: `Social Connections`
Prefix: `/connections`

*   **GET `/connect/{platform}`**
    *   **Operation ID:** `initiate_oauth_connection_connect__platform__get`
    *   **Summary:** Initiates OAuth 2.0 connection flow for a given platform.
    *   **Parameters:**
        *   `platform: str` (Path parameter, e.g., "instagram", "facebook")
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)`
    *   **Responses:**
        *   `307 Temporary Redirect`: Redirects user to the social platform's authorization URL.
        *   `400 Bad Request`: (schemas.ErrorDetail) If platform is unsupported.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `oauth_service.initiate_connection` to get the authorization URL and returns a `RedirectResponse`.

*   **GET `/connect/{platform}/callback`**
    *   **Operation ID:** `handle_oauth_callback_connect__platform__callback_get`
    *   **Summary:** Handles the OAuth 2.0 callback from the social platform.
    *   **Parameters:**
        *   `platform: str` (Path parameter)
        *   `request: Request` (FastAPI Request object to access `current_user_id` if passed in state or derive from session)
        *   `code: Optional[str] = Query(None)` (Authorization code)
        *   `error: Optional[str] = Query(None)` (Error from social platform)
        *   `state: Optional[str] = Query(None)` (State parameter for CSRF protection, should contain user_id or session identifier)
        *   `oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)`
    *   **Responses:**
        *   `200 OK`: (schemas.SocialConnectionResponse) On successful connection.
        *   `400 Bad Request`: (schemas.ErrorDetail) If error in callback or invalid state.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Extracts `user_id` from the `state` parameter (needs secure implementation). Calls `oauth_service.finalize_connection` with the `code` and other relevant data. Returns success or error message.

*   **GET `/`**
    *   **Operation ID:** `list_connections_get`
    *   **Summary:** Lists all active social media connections for the current user.
    *   **Parameters:**
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)`
    *   **Responses:**
        *   `200 OK`: `List[schemas.SocialConnectionResponse]`
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `oauth_service.get_user_connections`.

*   **DELETE `/{connection_id}`**
    *   **Operation ID:** `disconnect_account__connection_id__delete`
    *   **Summary:** Disconnects a social media account.
    *   **Parameters:**
        *   `connection_id: UUID` (Path parameter)
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service)`
    *   **Responses:**
        *   `200 OK`: (schemas.StatusResponse)
        *   `404 Not Found`: (schemas.ErrorDetail) If connection not found or doesn't belong to user.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `oauth_service.disconnect`.

### 4.2 Publishing Router (`src/creativeflow/socialpublishing/api/v1/routers/publishing_router.py`)
Tag: `Content Publishing`
Prefix: `/publishing`

*   **POST `/publish`**
    *   **Operation ID:** `publish_content_now_publish_post`
    *   **Summary:** Publishes content immediately to a connected social account.
    *   **Parameters:**
        *   `payload: schemas.PublishRequest` (Request body)
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)`
    *   **Responses:**
        *   `202 Accepted`: (schemas.PublishJobResponse) Job accepted for processing.
        *   `400 Bad Request`: (schemas.ErrorDetail) Invalid payload or content policy violation.
        *   `404 Not Found`: (schemas.ErrorDetail) Connection ID not found.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `publishing_service.publish_now`.

*   **POST `/schedule`**
    *   **Operation ID:** `schedule_content_schedule_post`
    *   **Summary:** Schedules content for future publishing.
    *   **Parameters:**
        *   `payload: schemas.ScheduleRequest` (Request body)
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)`
    *   **Responses:**
        *   `202 Accepted`: (schemas.PublishJobResponse) Job accepted for scheduling.
        *   `400 Bad Request`: (schemas.ErrorDetail) Invalid payload or schedule time.
        *   `404 Not Found`: (schemas.ErrorDetail) Connection ID not found.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `publishing_service.schedule_publish`.

*   **GET `/jobs/{job_id}/status`**
    *   **Operation ID:** `get_publish_job_status_jobs__job_id__status_get`
    *   **Summary:** Retrieves the status of a specific publishing job.
    *   **Parameters:**
        *   `job_id: UUID` (Path parameter)
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)`
    *   **Responses:**
        *   `200 OK`: (schemas.PublishJobResponse)
        *   `404 Not Found`: (schemas.ErrorDetail) Job not found or doesn't belong to user.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `publishing_service.get_job_status`.

*   **GET `/jobs`**
    *   **Operation ID:** `list_publish_jobs_jobs_get`
    *   **Summary:** Lists publishing jobs for the current user, with optional filters.
    *   **Parameters:**
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `publishing_service: PublishingOrchestrationService = Depends(get_publishing_orchestration_service)`
        *   `platform: Optional[str] = Query(None)`
        *   `status: Optional[str] = Query(None)`
    *   **Responses:**
        *   `200 OK`: `List[schemas.PublishJobResponse]`
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `publishing_service.list_jobs`.

### 4.3 Insights Router (`src/creativeflow/socialpublishing/api/v1/routers/insights_router.py`)
Tag: `Content Insights`
Prefix: `/insights`

*   **POST `/{platform}/hashtags`**
    *   **Operation ID:** `get_trending_hashtags_insights__platform__hashtags_post`
    *   **Summary:** Fetches trending hashtag suggestions for a platform.
    *   **Parameters:**
        *   `platform: str` (Path parameter)
        *   `request_payload: schemas.HashtagRequest` (Request body)
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `insights_service: InsightsAggregationService = Depends(get_insights_aggregation_service)`
    *   **Responses:**
        *   `200 OK`: (schemas.HashtagResponse)
        *   `400 Bad Request`: (schemas.ErrorDetail)
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `insights_service.get_trending_hashtags`.

*   **GET `/{platform}/best-times`**
    *   **Operation ID:** `get_best_times_to_post_insights__platform__best_times_get`
    *   **Summary:** Fetches best times to post for a connected account on a platform.
    *   **Parameters:**
        *   `platform: str` (Path parameter)
        *   `connection_id: UUID = Query(...)`
        *   `current_user_id: str = Depends(get_current_user_id)`
        *   `insights_service: InsightsAggregationService = Depends(get_insights_aggregation_service)`
    *   **Responses:**
        *   `200 OK`: (schemas.BestTimeToPostResponse)
        *   `404 Not Found`: (schemas.ErrorDetail) If connection ID invalid or insights not available.
        *   `500 Internal Server Error`: (schemas.ErrorDetail)
    *   **Logic:** Calls `insights_service.get_best_times_to_post`.

### 4.4 Pydantic Schemas (`src/creativeflow/socialpublishing/api/v1/schemas/`)

*   **`common_schemas.py`**:
    *   `StatusResponse(BaseModel)`: `status: str`, `message: Optional[str] = None`
    *   `ErrorDetail(BaseModel)`: `code: str`, `detail: str`
*   **`connection_schemas.py`**:
    *   `SocialConnectionResponse(BaseModel)`: `id: UUID`, `user_id: str`, `platform: str`, `external_user_id: str`, `external_display_name: Optional[str] = None`, `created_at: datetime`, `expires_at: Optional[datetime] = None`, `scopes: Optional[List[str]] = None`
    *   `OAuthCallbackQuery(BaseModel)`: `code: Optional[str] = None`, `state: Optional[str] = None`, `error: Optional[str] = None`, `error_description: Optional[str] = None`
    *   `InitiateOAuthResponse(BaseModel)`: `authorization_url: str`
*   **`publishing_schemas.py`**:
    *   `GeneratedAsset(BaseModel)`: `url: str` (MinIO path or public URL), `asset_type: str` (e.g., 'image', 'video'), `mime_type: str`, `platform_media_id: Optional[str] = None` (ID after upload to platform if multi-step)
    *   `PublishRequest(BaseModel)`: `connection_id: UUID`, `text_content: Optional[str] = None`, `assets: List[GeneratedAsset] = []`, `platform_specific_options: Optional[Dict[str, Any]] = None` (e.g., Instagram location tag, Facebook link details)
    *   `ScheduleRequest(PublishRequest)`: `schedule_time: datetime`
    *   `PublishJobResponse(BaseModel)`: `job_id: UUID`, `status: str`, `platform: str`, `user_id: str`, `created_at: datetime`, `scheduled_at: Optional[datetime] = None`, `published_at: Optional[datetime] = None`, `error_message: Optional[str] = None`, `post_url: Optional[str] = None`
*   **`insights_schemas.py`**:
    *   `HashtagRequest(BaseModel)`: `keywords: List[str]`, `industry: Optional[str] = None`, `limit: int = 10`
    *   `HashtagSuggestion(BaseModel)`: `tag: str`, `score: Optional[float] = None`
    *   `HashtagResponse(BaseModel)`: `suggestions: List[HashtagSuggestion]`
    *   `BestTimeToPostSuggestion(BaseModel)`: `day_of_week: int` (0-6), `hour_of_day: int` (0-23), `score: Optional[float] = None`
    *   `BestTimeToPostResponse(BaseModel)`: `suggested_times: List[BestTimeToPostSuggestion]`, `confidence: Optional[str] = None` (e.g., "high", "medium")

## 5. Core Modules & Logic

### 5.1 Application Layer (`src/creativeflow/socialpublishing/application/`)

#### 5.1.1 `oauth_orchestration_service.py:OAuthOrchestrationService`
*   **Constructor:**
    *   `db_session: AsyncSession`
    *   `token_encryption_service: ITokenEncryptionService`
    *   `config: Settings`
    *   Initializes platform clients (e.g., `InstagramClient`, `FacebookClient`) from `infrastructure.clients` based on config.
*   **`async def initiate_connection(self, platform: str, user_id: str, request: Request) -> str`**:
    1.  Validate `platform`.
    2.  Get appropriate platform client.
    3.  Construct `redirect_uri` using `config.SERVICE_BASE_URL + f"/api/v1/connections/connect/{platform}/callback"`.
    4.  Generate a secure `state` parameter (e.g., CSRF token, possibly embedding/linking `user_id` if session state is not robustly handled by gateway/frontend).
    5.  Call platform client's `get_oauth_url(state, redirect_uri)`.
    6.  Return authorization URL.
*   **`async def finalize_connection(self, platform: str, user_id_from_state: str, code: str, redirect_uri: str) -> domain.SocialConnection`**:
    1.  Validate `platform`.
    2.  Get appropriate platform client.
    3.  Call platform client's `exchange_code_for_token(code, redirect_uri)`. This returns `access_token`, `refresh_token` (if any), `expires_in`, `scopes`.
    4.  Use the obtained `access_token` to call platform client's `get_user_profile()` to fetch `external_user_id` and `external_display_name`.
    5.  Encrypt `access_token` and `refresh_token` using `token_encryption_service`.
    6.  Calculate `expires_at` datetime.
    7.  Check if a connection already exists for this `user_id_from_state` and `platform`. If so, update it. Otherwise, create a new `domain.SocialConnection` entity.
    8.  Save the entity using `social_connection_repo.save()`.
    9.  Return the domain entity.
*   **`async def get_user_connections(self, user_id: str) -> List[domain.SocialConnection]`**:
    1.  Call `social_connection_repo.list_by_user_id(user_id)`.
    2.  Return the list.
*   **`async def disconnect(self, connection_id: UUID, user_id: str) -> None`**:
    1.  Fetch connection using `social_connection_repo.get_by_id(connection_id)`.
    2.  Verify it belongs to `user_id`. If not, raise `PermissionDeniedError`.
    3.  (Optional but recommended) Attempt to revoke token with the social platform via its client, if API supports.
    4.  Call `social_connection_repo.delete(connection_id)`.
*   **`async def get_valid_access_token(self, connection_id: UUID, user_id: str) -> str`**:
    1.  Fetch connection via `social_connection_repo.get_by_id(connection_id)`.
    2.  Verify ownership by `user_id`.
    3.  Decrypt `access_token_encrypted`.
    4.  If `expires_at` is past and `refresh_token_encrypted` exists:
        a.  Decrypt `refresh_token_encrypted`.
        b.  Get appropriate platform client.
        c.  Call platform client's `refresh_access_token(decrypted_refresh_token)`.
        d.  Update the connection with new encrypted tokens and `expires_at` using `social_connection_repo.save()`.
        e.  Return the new decrypted access token.
    5.  If token is still valid or no refresh mechanism, return decrypted access token.
    6.  If expired and no refresh, raise `TokenExpiredError`.

#### 5.1.2 `publishing_orchestration_service.py:PublishingOrchestrationService`
*   **Constructor:**
    *   `db_session: AsyncSession`
    *   `oauth_service: OAuthOrchestrationService`
    *   `policy_validator: PlatformPolicyValidator`
    *   `config: Settings`
    *   Initializes platform clients.
*   **`async def publish_now(self, user_id: str, payload: schemas.PublishRequest) -> domain.PublishJob`**:
    1.  Validate `payload`.
    2.  Validate content against platform policies using `policy_validator.validate_content_for_platform`. If invalid, raise `ContentValidationError`.
    3.  Create `domain.PublishJob` entity with status 'Processing'. Save via `publish_job_repo.save()`.
    4.  Try to execute:
        a.  Get valid access token using `oauth_service.get_valid_access_token(payload.connection_id, user_id)`.
        b.  Call `self._execute_publish(job, access_token, payload.text_content, payload.assets, payload.platform_specific_options)`.
    5.  Update job status (Published/Failed) and save.
    6.  Return job entity.
*   **`async def schedule_publish(self, user_id: str, payload: schemas.ScheduleRequest) -> domain.PublishJob`**:
    1.  Validate `payload`, ensure `schedule_time` is in the future.
    2.  Validate content against platform policies.
    3.  Create `domain.PublishJob` entity with status 'Scheduled', `scheduled_at = payload.schedule_time`.
    4.  Save via `publish_job_repo.save()`.
    5.  Return job entity. (A separate background worker/scheduler service will pick this up based on `scheduled_at` and status 'Scheduled', then call an internal method similar to `_execute_publish`).
*   **`async def get_job_status(self, job_id: UUID, user_id: str) -> domain.PublishJob`**:
    1.  Fetch job using `publish_job_repo.get_by_id(job_id)`.
    2.  Verify ownership by `user_id`.
    3.  Return job.
*   **`async def list_jobs(self, user_id: str, platform: Optional[str], status: Optional[str]) -> List[domain.PublishJob]`**:
    1.  Call `publish_job_repo.list_by_user_id(user_id, platform, status)`.
    2.  Return list.
*   **`async def _execute_publish(self, job: domain.PublishJob, access_token: str, text: Optional[str], assets: List[schemas.GeneratedAsset], options: Optional[Dict[str, Any]]) -> None`**: (Internal method called by `publish_now` or background scheduler)
    1.  Job status updated to 'Processing' and attempts incremented by `publish_job_repo.save(job)`.
    2.  Get appropriate platform client based on `job.platform`.
    3.  Call platform client's `publish_content(access_token, text, assets, options)`. This might involve multiple steps (e.g., media upload then post creation).
    4.  If successful, update job status to 'Published', set `published_at`, `post_url`.
    5.  If failed (API error, rate limit, content rejection), update job status to 'Failed' or 'ContentRejected', set `error_message`.
    6.  Save job via `publish_job_repo.save(job)`.
    7.  Handle retries for transient errors based on `config.MAX_API_RETRIES` and `job.attempts`.

#### 5.1.3 `insights_aggregation_service.py:InsightsAggregationService`
*   **Constructor:**
    *   `db_session: AsyncSession` (if insights are persisted/logged)
    *   `oauth_service: OAuthOrchestrationService`
    *   `insights_cache: PlatformInsightsCache`
    *   `config: Settings`
    *   Initializes platform clients.
*   **`async def get_trending_hashtags(self, user_id: str, platform: str, request_payload: schemas.HashtagRequest) -> schemas.HashtagResponse`**:
    1.  Generate cache key based on platform, keywords, industry.
    2.  Try fetching from `insights_cache`. If found and not stale, return.
    3.  Get platform client. Some platforms might not require user-specific tokens for public trends. If they do, fetch access token via `oauth_service` (may need a generic app token or a user token if specific to their connections).
    4.  Call platform client's `get_trending_hashtags(access_token_if_needed, request_payload.keywords, request_payload.industry, request_payload.limit)`.
    5.  Transform response to `List[schemas.HashtagSuggestion]`.
    6.  Store in `insights_cache`.
    7.  Return `schemas.HashtagResponse`.
*   **`async def get_best_times_to_post(self, user_id: str, platform: str, connection_id: UUID) -> schemas.BestTimeToPostResponse`**:
    1.  Generate cache key based on platform, connection_id (or external_user_id).
    2.  Try fetching from `insights_cache`. If found and not stale, return.
    3.  Get valid access token using `oauth_service.get_valid_access_token(connection_id, user_id)`.
    4.  Get platform client.
    5.  Call platform client's `get_best_post_times(access_token)`.
    6.  Transform response to `List[schemas.BestTimeToPostSuggestion]`.
    7.  Store in `insights_cache`.
    8.  Return `schemas.BestTimeToPostResponse`.

#### 5.1.4 `application/exceptions.py`
Defines custom exceptions:
*   `SocialPublishingBaseError(Exception)`
*   `OAuthConnectionError(SocialPublishingBaseError)`
*   `PublishingError(SocialPublishingBaseError)`
*   `InsufficientPermissionsError(SocialPublishingBaseError)`
*   `PlatformApiError(SocialPublishingBaseError)`: `platform: str`, `status_code: int`, `details: Any`
*   `RateLimitError(PlatformApiError)`
*   `TokenEncryptionError(SocialPublishingBaseError)`
*   `TokenExpiredError(SocialPublishingBaseError)`
*   `ContentValidationError(SocialPublishingBaseError)`
*   `JobNotFoundError(SocialPublishingBaseError)`

### 5.2 Domain Layer (`src/creativeflow/socialpublishing/domain/`)

#### 5.2.1 Models (`domain/models/`)
*   **`social_connection.py:SocialConnection` (Dataclass/Pydantic Model)**:
    *   Attributes: `id: UUID`, `user_id: str`, `platform: str`, `external_user_id: str`, `external_display_name: Optional[str]`, `access_token_encrypted: bytes`, `refresh_token_encrypted: Optional[bytes]`, `expires_at: Optional[datetime]`, `scopes: Optional[List[str]]`, `created_at: datetime`, `updated_at: datetime`.
    *   Methods: `is_token_expired() -> bool`, `update_tokens(...)`.
*   **`publish_job.py:PublishJob` (Dataclass/Pydantic Model)**:
    *   Attributes: `id: UUID`, `user_id: str`, `social_connection_id: UUID`, `platform: str`, `content_text: Optional[str]`, `asset_urls: List[str]`, `platform_specific_options: Optional[Dict[str, Any]]`, `status: str` (Enum: PENDING, PROCESSING, PUBLISHED, SCHEDULED, FAILED, CONTENT_REJECTED), `scheduled_at: Optional[datetime]`, `published_at: Optional[datetime]`, `error_message: Optional[str]`, `attempts: int = 0`, `post_url: Optional[str]`, `created_at: datetime`, `updated_at: datetime`.
    *   Methods: `mark_as_processing()`, `mark_as_published(post_url: str)`, `mark_as_failed(error: str)`, `mark_as_content_rejected(reason: str)`, `increment_attempts()`.
*   **`platform_insights.py:PlatformInsights, HashtagSuggestionVO, BestPostTimeVO` (Dataclass/Pydantic Models)**:
    *   `HashtagSuggestionVO`: `tag: str`, `score: Optional[float]`
    *   `BestPostTimeVO`: `day_of_week: int`, `hour_of_day: int`, `score: Optional[float]`
    *   `PlatformInsights`: `platform: str`, `insight_type: str` (Enum: HASHTAGS, BEST_TIMES), `data: Union[List[HashtagSuggestionVO], List[BestPostTimeVO]]`, `generated_at: datetime`, `context_params: Optional[Dict[str, Any]]`

#### 5.2.2 Repositories (Interfaces) (`domain/repositories/`)
*   **`social_connection_repository.py:ISocialConnectionRepository(ABC)`**:
    *   `async def get_by_id(self, connection_id: UUID) -> Optional[SocialConnection]`
    *   `async def get_by_user_and_platform(self, user_id: str, platform: str) -> Optional[SocialConnection]`
    *   `async def list_by_user_id(self, user_id: str) -> List[SocialConnection]`
    *   `async def save(self, connection: SocialConnection) -> SocialConnection`
    *   `async def delete(self, connection_id: UUID) -> None`
*   **`publish_job_repository.py:IPublishJobRepository(ABC)`**:
    *   `async def get_by_id(self, job_id: UUID) -> Optional[PublishJob]`
    *   `async def list_by_user_id(self, user_id: str, platform: Optional[str] = None, status: Optional[str] = None) -> List[PublishJob]`
    *   `async def save(self, job: PublishJob) -> PublishJob`
    *   `async def find_pending_scheduled_jobs(self, limit: int = 100) -> List[PublishJob]` (fetches jobs where status is 'Scheduled' and `scheduled_at` <= now)

#### 5.2.3 Domain Services (`domain/services/`)
*   **`token_encryption_service.py:ITokenEncryptionService(ABC)`**:
    *   `def encrypt_token(self, token: str) -> bytes`
    *   `def decrypt_token(self, encrypted_token: bytes) -> str`
*   **`platform_policy_validator.py:PlatformPolicyValidator`**:
    *   **Constructor:** (May load platform-specific rules or have platform client dependencies if validation requires API calls).
    *   `async def validate_content_for_platform(self, platform: str, content_text: Optional[str], assets: List[schemas.GeneratedAsset]) -> Tuple[bool, Optional[str]]`:
        1.  Switch based on `platform`.
        2.  Apply rules: e.g., Twitter character limit, Instagram image aspect ratio/resolution from `assets[i].metadata` (if available in `GeneratedAsset` schema, else fetch if needed), video duration for TikTok/Reels.
        3.  Return `(True, None)` if valid, or `(False, "Error message")` if invalid.

#### 5.2.4 Domain Exceptions (`domain/exceptions.py`)
*   `InvalidSocialPlatformError(ValueError)`
*   `TokenExpiredError(Exception)` (might inherit from a base auth error)
*   `ContentValidationError(ValueError)`
*   `JobStateTransitionError(Exception)`
*   `EntityNotFoundError(Exception)`

### 5.3 Infrastructure Layer (`src/creativeflow/socialpublishing/infrastructure/`)

#### 5.3.1 Database (`infrastructure/database/`)
*   **`sqlalchemy_models.py`**:
    *   `Base = declarative_base()`
    *   `SocialConnectionSQL(Base)`: Maps to `social_connections` table. Columns for all `SocialConnection` domain model attributes. `user_id` indexed. `UniqueConstraint('user_id', 'platform')`.
    *   `PublishJobSQL(Base)`: Maps to `publish_jobs` table. Columns for all `PublishJob` domain model attributes. `ForeignKeyConstraint` to `social_connections.id`. Indexes on `user_id`, `status`, `scheduled_at`.
*   **`repositories/sql_social_connection_repository.py:SQLSocialConnectionRepository`**: Implements `ISocialConnectionRepository` using SQLAlchemy `AsyncSession` and `SocialConnectionSQL`. Includes `_map_to_domain` and `_map_to_db_model` helpers.
*   **`repositories/sql_publish_job_repository.py:SQLPublishJobRepository`**: Implements `IPublishJobRepository` using SQLAlchemy `AsyncSession` and `PublishJobSQL`. Includes mappers. `find_pending_scheduled_jobs` uses `select().where(PublishJobSQL.status == 'Scheduled', PublishJobSQL.scheduled_at <= datetime.utcnow()).limit(limit)`.
*   **`session_manager.py:DBSessionManager`**:
    *   `_engine: Optional[AsyncEngine] = None`
    *   `_SessionLocal: Optional[async_sessionmaker[AsyncSession]] = None`
    *   `init_db(cls, database_url: str)`: Creates `_engine` and `_SessionLocal`.
    *   `async def get_session(cls) -> AsyncGenerator[AsyncSession, None]`: Provides an `AsyncSession` in a context manager.
*   **Alembic setup (`alembic/`, `alembic.ini`)**: Configured for asynchronous migrations targeting `sqlalchemy_models.Base.metadata`. `env.py` will use `config.DATABASE_URL`. Initial migration will create `social_connections` and `publish_jobs` tables.

#### 5.3.2 External API Clients (`infrastructure/clients/`)
*   **`base_social_client.py:BaseSocialClient(ABC)`**:
    *   **Constructor:** `http_client: httpx.AsyncClient`, `config: Settings`, `platform_name: str`.
    *   Abstract methods as defined in file structure.
    *   `async def _handle_api_error(self, response: httpx.Response, platform_name: str)`: Examines `response.status_code` and content. Raises `RateLimitError` or `PlatformApiError` with details. Leverages `_client_utils.map_platform_error`.
*   **`_client_utils.py`**:
    *   `map_platform_error`: Takes platform name, status code, JSON response. Returns specific `PlatformApiError` or general one.
    *   `http_retry_decorator`: Decorator for `httpx` calls in client methods. Uses `config.MAX_API_RETRIES`, `config.API_RETRY_DELAY_SECONDS`, `config.API_RETRY_BACKOFF_FACTOR`. Retries on specific HTTP status codes (e.g., 5xx, 429 if not handled by specific rate limit logic).
*   **Specific Clients (`instagram_client.py`, `facebook_client.py`, etc.)**:
    *   Each inherits from `BaseSocialClient`.
    *   Implement platform-specific API calls for OAuth, publishing, and insights using `self.http_client.request()`.
    *   Use platform-specific app IDs/secrets from `self.config`.
    *   Map platform API responses to standardized internal DTOs or domain model attributes where necessary.
    *   **Instagram Client**:
        *   `get_oauth_url`: Implements Instagram Basic Display or Graph API OAuth.
        *   `exchange_code_for_token`: Completes OAuth.
        *   `publish_post`: Uses content publishing API (image, video if Business Account). Needs logic for container creation and publish.
        *   `publish_story`: Uses story publishing API.
        *   `publish_reel`: Uses reel publishing API (if available).
    *   **Facebook Client**:
        *   `get_oauth_url`: Implements Facebook Login OAuth (`manage_pages`, `publish_pages` permissions).
        *   `exchange_code_for_token`.
        *   `get_user_profile`: Fetches user's pages they manage.
        *   `publish_to_page`: Posts to selected page feed (text, image, video).
    *   **LinkedIn Client**:
        *   OAuth flow, publishing to Company Page, potentially personal profile if API terms allow.
    *   **Twitter Client (X API v2)**:
        *   OAuth 2.0 PKCE flow for user context.
        *   `post_tweet`: Handles text, media uploads (may be multi-step).
    *   **Pinterest Client**:
        *   OAuth flow.
        *   `create_pin`: Creates image/video pins on selected boards.
    *   **TikTok Client**:
        *   Research official API for direct publishing for businesses. If available, implement OAuth and video publishing. If not, this client may be minimal or stubbed, logging unavailability. Relies on `EnableTikTokPublishing` feature toggle.

#### 5.3.3 Security (`infrastructure/security/`)
*   **`aes_gcm_encryption_service.py:AESGCMTokenEncryptionService`**: Implements `ITokenEncryptionService`.
    *   **Constructor:** Takes `aes_key: bytes` (derived from `config.AES_KEY`).
    *   `encrypt_token(self, token: str) -> bytes`: Encodes token to bytes, generates a unique nonce, encrypts using AES-GCM (`cryptography.hazmat.primitives.ciphers.aead.AESGCM`), returns `nonce + ciphertext + tag`.
    *   `decrypt_token(self, encrypted_data: bytes) -> str`: Splits nonce, ciphertext, tag. Decrypts using AES-GCM. Decodes to string. Raises `TokenEncryptionError` on failure.

#### 5.3.4 Logging (`infrastructure/logging/`)
*   **`config.py:setup_logging(log_level: str)`**:
    *   Uses `logging.basicConfig` or custom handlers.
    *   If `python-json-logger` is added:
        python
        import logging
        from pythonjsonlogger import jsonlogger

        def setup_logging(log_level_str: str = "INFO"):
            logger = logging.getLogger("creativeflow.socialpublishing")
            log_level = getattr(logging, log_level_str.upper(), logging.INFO)
            logger.setLevel(log_level)
            log_handler = logging.StreamHandler()
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
            )
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
            logger.propagate = False # To avoid duplicate logs if root logger is also configured

            # Configure uvicorn access logs if desired to be JSON
            # uvicorn_access_logger = logging.getLogger("uvicorn.access")
            # uvicorn_access_logger.handlers = [log_handler]
            # uvicorn_access_logger.propagate = False
        
    *   Called during FastAPI app startup in `main.py`.

#### 5.3.5 Caching (`infrastructure/caching/`)
*   **`platform_insights_cache.py:PlatformInsightsCache`**:
    *   **Constructor:** Takes `redis_client: Optional[aioredis.Redis] = None` (from shared lib or direct setup), `default_ttl_seconds: int`.
    *   `async def get_insights(...)`: Constructs cache key. If `redis_client`, uses `await redis_client.get(key)`. Deserialize if found.
    *   `async def set_insights(...)`: Constructs cache key. If `redis_client`, uses `await redis_client.set(key, serialized_data, ex=self.ttl_seconds)`. Serialize data.
    *   If no `redis_client`, use an in-memory LRU cache with TTL (e.g., from `cachetools` library, but consider async compatibility or a simple dict with expiry checks).

### 5.4 Main Application (`src/creativeflow/socialpublishing/main.py`)
*   Initialize `Settings` using `config.get_settings()`.
*   Call `logging_config.setup_logging(settings.LOG_LEVEL)`.
*   Call `session_manager.DBSessionManager.init_db(settings.DATABASE_URL)`.
*   Create FastAPI app instance: `app = FastAPI(...)`.
*   Include routers: `app.include_router(connections_router.router, prefix="/api/v1/connections", tags=["Social Connections"])`, etc. for publishing and insights.
*   **Middleware:**
    *   CORS (Allow specific origins if BFF/Frontend are on different domains).
    *   Global exception handler to catch custom exceptions and return structured error responses.
*   **Event Handlers:**
    *   `@app.on_event("startup")`: Potentially log service start, initialize any global resources not handled by dependencies.
    *   `@app.on_event("shutdown")`: Cleanly close database engine connections (if `DBSessionManager` doesn't handle this implicitly on engine disposal), close `httpx.AsyncClient` instances if they are global.

### 5.5 Dependencies (`src/creativeflow/socialpublishing/dependencies.py`)
*   `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")` (or similar, assuming token URL is from Auth service if this service validates directly, otherwise token is just passed through).
*   `async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str`:
    1.  This is a placeholder. Actual implementation depends on how user auth is handled platform-wide.
    2.  If this service validates tokens: call Auth Service to validate `token` and get `user_id`.
    3.  If API Gateway validates tokens and passes `user_id` in a header: read header.
    4.  For simplicity in this SDS, assume `jwt-decode` or a shared utility can decode the JWT and extract `user_id` if the token is already validated by an upstream gateway. If this service has to validate, it needs an `httpx.AsyncClient` to call the Auth Service's token introspection endpoint.
    5.  Return `user_id`. Raise `HTTPException(status_code=401, ...)` if invalid.
*   `get_db_session`: Uses `DBSessionManager.get_session()`.
*   `get_token_encryption_service`: Returns `AESGCMTokenEncryptionService(config.get_settings().AES_KEY.encode())`.
*   Service getters (`get_oauth_orchestration_service`, etc.): Instantiate respective application services, injecting their dependencies (db session, other services, config).

## 6. Error Handling Strategy
*   **Platform API Errors:**
    *   Clients in `infrastructure.clients` will use `_client_utils.map_platform_error` to convert platform-specific errors into `PlatformApiError` or `RateLimitError`.
    *   Retry logic with exponential backoff implemented in `_client_utils.http_retry_decorator` for transient network issues or temporary server errors from social platforms.
    *   `OAuthOrchestrationService` and `PublishingOrchestrationService` will catch these exceptions and can:
        *   Log the error.
        *   Update `PublishJob.status` to 'Failed' with error message.
        *   Return appropriate error responses to the API caller.
*   **Token Expiry/Revocation:**
    *   `OAuthOrchestrationService.get_valid_access_token` handles token refresh.
    *   If refresh fails or token is irrevocably invalid, `TokenExpiredError` is raised.
    *   API endpoints will catch this and return a 401/403 response, possibly with a specific error code indicating re-authentication is needed.
*   **Internal Errors:**
    *   Custom exceptions (from `application.exceptions`, `domain.exceptions`) are used to signal specific issues.
    *   A global FastAPI exception handler in `main.py` catches these and maps them to appropriate HTTP status codes and `schemas.ErrorDetail` responses. Unhandled exceptions result in a generic 500 error.
*   **Content Policy Violations:**
    *   `PlatformPolicyValidator` identifies these.
    *   `PublishingOrchestrationService` will mark `PublishJob.status` as 'ContentRejected' and provide reason.

## 7. Security Considerations
*   **Token Encryption:** OAuth access and refresh tokens are encrypted at rest using AES-GCM via `AESGCMTokenEncryptionService`. The `AES_KEY` is a critical secret managed via `config.py`.
*   **API Key Management (for this service's access to social platforms):** Social platform App IDs/Secrets are managed as configuration secrets.
*   **Input Validation:** Pydantic schemas in the API layer validate all incoming request data.
*   **Authentication:** User identity is established via JWTs (assumed validated by an upstream gateway or this service calls Auth Service). `get_current_user_id` is key.
*   **Authorization:** Service logic must check if `current_user_id` owns the `SocialConnection` or `PublishJob` being accessed/modified.
*   **HTTPS:** All external communication with social platforms and internal API calls must use HTTPS. FastAPI will run under Uvicorn, typically behind Nginx for SSL termination.
*   **Rate Limiting (by this service):** While this service primarily *handles* rate limits from external platforms, it can also implement its own rate limits for its exposed APIs if needed, via FastAPI middleware or dependencies (though this is often a Gateway concern).

## 8. Database Schema & Migrations
*   SQLAlchemy models are defined in `infrastructure/database/sqlalchemy_models.py`.
*   Alembic is used for schema migrations. The initial migration will create tables for `SocialConnectionSQL` and `PublishJobSQL`.
*   Refer to section 5.3.1 for model details.

## 9. Testing Strategy (High-Level)
*   **Unit Tests:**
    *   PyTest for application services, domain logic, repository mappings, client utilities.
    *   Mock external dependencies (database, HTTP calls to social platforms, other services).
*   **Integration Tests:**
    *   Test FastAPI routers with `TestClient` or `httpx.AsyncClient`.
    *   Test interactions with a real test database (PostgreSQL).
    *   Test interactions with mocked social media platform APIs to verify client logic.
*   **Contract Tests (Pact - if other services consume this one directly):** Not explicitly detailed but good practice if this service's API is a provider for other internal microservices.

## 10. Deployment (Conceptual)
*   The service is containerized using Docker (Dockerfile to be created).
*   Deployed as a microservice, potentially managed by Kubernetes.
*   Relies on external PostgreSQL and Redis instances.
*   Configuration injected via environment variables.
*   A separate background worker process/service (not part of these files but interacting with `PublishJobRepository`) will be needed to pick up scheduled jobs from the `PublishJob` table (e.g., a Celery worker, or a simple scheduled Python script querying `find_pending_scheduled_jobs`).

This SDS provides a comprehensive plan for developing the `CreativeFlow.SocialPublishingService`.