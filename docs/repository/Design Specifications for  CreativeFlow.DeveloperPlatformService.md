# Software Design Specification: CreativeFlow.DeveloperPlatformService

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.DeveloperPlatformService`. This microservice is a core component of the CreativeFlow AI platform, dedicated to managing third-party developer access and interactions via the platform's API. Its primary responsibilities include API key management, webhook configuration and event dispatch, API usage tracking, monetization enforcement (rate limiting, quotas), and proxying authenticated API requests to relevant backend services.

### 1.2. Scope
The scope of this document covers the design of the `CreativeFlow.DeveloperPlatformService` including:
-   API endpoint definitions for managing API keys and webhooks.
-   Endpoints for developers to query their API usage and quota status.
-   Proxy endpoints for creative generation, asset management, and user/team management operations initiated by API clients.
-   Internal logic for API key validation, permissioning, rate limiting, and quota enforcement.
-   Integration with the PostgreSQL database for persistence.
-   Integration with RabbitMQ for asynchronous webhook event publishing.
-   Integration with other internal microservices (AI Generation, Asset Management, User/Team Management, Authentication) via HTTP clients.

### 1.3. Definitions, Acronyms, and Abbreviations
-   **API:** Application Programming Interface
-   **CRUD:** Create, Read, Update, Delete
-   **CI/CD:** Continuous Integration/Continuous Deployment
-   **DTO:** Data Transfer Object
-   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
-   **HMAC:** Hash-based Message Authentication Code
-   **HTTP:** Hypertext Transfer Protocol
-   **IaC:** Infrastructure-as-Code
-   **JWT:** JSON Web Token
-   **K8s:** Kubernetes
-   **ORM:** Object-Relational Mapper
-   **PWA:** Progressive Web Application
-   **Pydantic:** Data validation and settings management using Python type annotations.
-   **SQLAlchemy:** SQL toolkit and Object-Relational Mapper for Python.
-   **SDS:** Software Design Specification
-   **VO:** Value Object
-   **SDK:** Software Development Kit

## 2. System Overview

### 2.1. Service Architecture
The `CreativeFlow.DeveloperPlatformService` is a Python-based microservice built using the FastAPI framework. It follows a layered architecture:
-   **API Layer (`api/`):** Handles HTTP requests, request/response validation (Pydantic schemas), and authentication/authorization. Contains routers and dependencies.
-   **Application Layer (`application/`):** Contains service classes that orchestrate business logic, interacting with the domain layer and infrastructure layer.
-   **Domain Layer (`domain/`):** Defines core business entities, value objects, and repository interfaces, encapsulating business rules.
-   **Infrastructure Layer (`infrastructure/`):** Implements data persistence (SQLAlchemy repositories), messaging (RabbitMQ client), and communication with other external/internal services (HTTP clients).

It interacts with:
-   **PostgreSQL Database:** For storing API keys, webhook configurations, usage records, and quotas.
-   **RabbitMQ:** For publishing webhook events asynchronously.
-   **Authentication Service:** For validating user identity when managing API keys or webhooks (if user-scoped).
-   **AI Generation Orchestration Service:** To proxy creative generation requests.
-   **Asset Management Service:** To proxy asset-related requests.
-   **User/Team Management Service:** To proxy user/team-related requests.

### 2.2. Key Features
-   **API Key Management (REQ-017, SEC-001):**
    -   Secure generation of API keys and secrets.
    -   Storage of hashed API secrets.
    -   Revocation and activation/deactivation of API keys.
    -   Assignment of granular permissions/scopes to API keys (future).
-   **Webhook Management (REQ-017):**
    -   Registration and management of webhook endpoints by developers.
    -   Subscription to specific event types (e.g., `generation.completed`).
    -   Secure event dispatch via RabbitMQ, including HMAC signatures for payload verification.
-   **API Monetization & Control (REQ-018):**
    -   Tracking API usage per client/key.
    -   Enforcing rate limits (e.g., requests per second/minute).
    -   Enforcing usage quotas (e.g., generations per month).
    -   Providing endpoints for developers to view their usage and quota status.
-   **API Request Proxying (REQ-017):**
    -   Acting as an authenticated gateway for API clients to access core platform functionalities like:
        -   Initiating creative generation.
        -   Querying generation status.
        -   Retrieving asset details.
        -   Managing user-uploaded source assets.
        -   Performing user/team management operations (scoped).
-   **Security (SEC-005):**
    -   API key-based authentication.
    -   Input validation and sanitization.
    -   Protection against common web vulnerabilities.

## 3. Core Module Design

### 3.1. `main.py` - Application Entrypoint
-   **Purpose:** Initializes and configures the FastAPI application.
-   **`create_application() -> FastAPI`:**
    -   Instantiates `FastAPI` app.
    -   Loads settings from `core.config.Settings`.
    -   Configures CORS middleware (allow specific origins or all for development).
    -   Includes API routers from `api.routers.*`.
    -   Sets up global exception handlers from `core.exceptions`.
    -   Calls `core.logging_config.setup_logging()`.
-   **`startup_event() -> None` (async):**
    -   Attached to `app.on_event("startup")`.
    -   Initialize database engine/connection pool (if not handled by `get_db_session` on first use).
    -   Initialize RabbitMQ client connection (`infrastructure.messaging.rabbitmq_client.connect()`).
    -   Initialize HTTP clients for external services (`infrastructure.external_clients.*.init_client()`).
-   **`shutdown_event() -> None` (async):**
    -   Attached to `app.on_event("shutdown")`.
    -   Close RabbitMQ client connection (`infrastructure.messaging.rabbitmq_client.close()`).
    -   Close HTTP clients for external services (`infrastructure.external_clients.*.close_client()`).
-   **Global Exception Handlers:**
    -   Generic `HTTPException` handler.
    -   Handler for `RequestValidationError` to return 422 with detailed errors.
    -   Custom application exception handlers defined in `core.exceptions`.

### 3.2. `core/` - Core Utilities and Configurations

#### 3.2.1. `core/config.py`
-   **Purpose:** Manages application configuration.
-   **`class Settings(BaseSettings)`:**
    -   `DATABASE_URL: str` (e.g., `postgresql+asyncpg://user:pass@host:port/db`)
    -   `RABBITMQ_URL: str` (e.g., `amqp://guest:guest@localhost:5672/`)
    -   `JWT_SECRET_KEY: str` (For decoding tokens from Auth service, if needed for verifying user actions on API keys/webhooks).
    -   `AI_GENERATION_SERVICE_URL: str` (Base URL for AI Generation Orchestration Service).
    -   `ASSET_MANAGEMENT_SERVICE_URL: str` (Base URL for Asset Management Service).
    -   `USER_TEAM_SERVICE_URL: str` (Base URL for User/Team Management Service).
    -   `AUTH_SERVICE_URL: str` (Base URL for Authentication Service, e.g., for user token validation).
    -   `API_KEY_HEADER_NAME: str = "X-API-KEY"`
    -   `WEBHOOK_HMAC_SECRET_KEY: str` (A global secret for signing webhook payloads, or allow per-webhook secrets).
    -   `LOG_LEVEL: str = "INFO"`
    -   `RABBITMQ_WEBHOOK_EXCHANGE_NAME: str = "webhook_events_exchange"`
    -   `RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX: str = "webhook.event"`
    -   `DEFAULT_RATE_LIMIT_REQUESTS: int = 100`
    -   `DEFAULT_RATE_LIMIT_PERIOD_SECONDS: int = 60`
    -   Model configuration: `model_config = SettingsConfigDict(env_file=".env", extra="ignore")`
-   **`@lru_cache` `def get_settings() -> Settings:`:** Returns a cached instance of `Settings`.

#### 3.2.2. `core/exceptions.py`
-   **Purpose:** Defines custom exceptions and handlers.
-   **`class AppException(HTTPException)`:** Base custom exception.
-   **`class APIKeyNotFoundError(AppException)`:** `status_code=404`, `detail="API Key not found."`
-   **`class APIKeyInactiveError(AppException)`:** `status_code=403`, `detail="API Key is inactive."`
-   **`class APIKeyPermissionDeniedError(AppException)`:** `status_code=403`, `detail="API Key does not have sufficient permissions."`
-   **`class WebhookNotFoundError(AppException)`:** `status_code=404`, `detail="Webhook not found."`
-   **`class InsufficientQuotaError(AppException)`:** `status_code=429`, `detail="API quota exceeded."` (REQ-018)
-   **`class RateLimitExceededError(AppException)`:** `status_code=429`, `detail="Rate limit exceeded."` (REQ-018)
-   **`class InvalidUserInputError(AppException)`:** `status_code=400`, `detail="Invalid user input."`
-   **`class ExternalServiceError(AppException)`:** `status_code=502`, `detail="Error communicating with an external service."`
-   **FastAPI Exception Handlers:**
    -   `async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:`
    -   `async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:` (Logs error, returns generic 500)
    -   `async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:` (Logs error, returns generic 500)

#### 3.2.3. `core/logging_config.py`
-   **Purpose:** Configures structured logging.
-   **`def setup_logging(log_level: str = "INFO") -> None:`:**
    -   Uses `logging.config.dictConfig` or direct logger configuration.
    -   Configures `python-json-logger.JSONFormatter` if chosen.
    -   Includes timestamp, level, message, module, function name, line number, and correlation ID (if available via middleware).
    -   Sets root logger level based on `log_level` from config.

### 3.3. `api/` - API Layer

#### 3.3.1. `api/dependencies/authentication.py`
-   **Purpose:** Handles API key authentication.
-   **`api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=True)`**
-   **`async def get_current_active_api_client(`**
    -   **`api_key_header_val: str = Security(api_key_header),`**
    -   **`api_key_service: APIKeyService = Depends(get_api_key_service)`**
    -   **`) -> APIKeyDomainModel:`** (REQ-017, SEC-001, SEC-005)
        -   Extract API key value from header.
        -   Call `api_key_service.validate_key(key_value=api_key_header_val)` which should check both the key format and the hashed secret.
            -   *Correction:* The header should contain the full API key (prefix + secret part). The service then splits it, finds the APIKey by prefix, and verifies the secret part against the stored hash.
        -   If `api_key_domain_model` is None or not `api_key_domain_model.is_active`, raise `HTTPException(status_code=401, detail="Invalid or inactive API Key")`.
        -   Return `api_key_domain_model`.
        -   *Note: Permission checks based on scope should be done within individual route handlers or a separate permission dependency, using the returned `api_key_domain_model.permissions`.*

#### 3.3.2. `api/dependencies/common.py`
-   **Purpose:** Provides common dependencies for injection.
-   **`async def get_db_session() -> AsyncGenerator[AsyncSession, None]:`** Yields an `AsyncSession` from `infrastructure.database.session.AsyncSessionLocal`.
-   **`async def get_rabbitmq_client() -> RabbitMQClient:`:** Returns an initialized `RabbitMQClient` instance (singleton or managed).
-   **`async def get_ai_generation_client() -> AIGenerationClient:`:** Returns an initialized `AIGenerationClient`.
-   **`async def get_asset_management_client() -> AssetManagementClient:`:** Returns an initialized `AssetManagementClient`.
-   **`async def get_user_team_client() -> UserTeamClient:`:** Returns an initialized `UserTeamClient`.
-   **`async def get_webhook_publisher(rabbitmq_client: RabbitMQClient = Depends(get_rabbitmq_client)) -> WebhookPublisher:`:** Instantiates and returns `WebhookPublisher`.
-   **`def get_api_key_service(db_session: AsyncSession = Depends(get_db_session)) -> APIKeyService:`:** Instantiates and returns `APIKeyService` with `SqlAlchemyApiKeyRepository`.
-   **`def get_webhook_service(db_session: AsyncSession = Depends(get_db_session), webhook_publisher: WebhookPublisher = Depends(get_webhook_publisher)) -> WebhookService:`:** Instantiates `WebhookService`.
-   **`def get_usage_tracking_service(db_session: AsyncSession = Depends(get_db_session)) -> UsageTrackingService:`:** Instantiates `UsageTrackingService`.
-   **`def get_quota_management_service(db_session: AsyncSession = Depends(get_db_session), usage_service: UsageTrackingService = Depends(get_usage_tracking_service)) -> QuotaManagementService:`:** Instantiates `QuotaManagementService`.
-   **`def get_rate_limiting_service(redis_client = Depends(get_redis_client_dependency)) -> RateLimitingService:`:** Instantiates `RateLimitingService`. (Requires a Redis client dependency, to be added).
-   **`def get_generation_proxy_service(`**
    -   **`ai_gen_client: AIGenerationClient = Depends(get_ai_generation_client),`**
    -   **`asset_mgmt_client: AssetManagementClient = Depends(get_asset_management_client),`**
    -   **`user_team_client: UserTeamClient = Depends(get_user_team_client),`**
    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**
    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service),`**
    -   **`rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service)`**
    -   **`) -> GenerationProxyService:`** Instantiates `GenerationProxyService`.

#### 3.3.3. `api/routers/api_keys_router.py` (REQ-017, SEC-001)
-   `router = APIRouter(prefix="/api-keys", tags=["API Keys"], dependencies=[Depends(get_current_active_api_client)])`
    -   *Correction*: The base router dependency should be a user authentication check (e.g. JWT from web app session) for managing keys. Individual API calls using the key will use `get_current_active_api_client`. For this router, let's assume a `get_current_authenticated_user` dependency that provides a `user_id`.
-   **`POST /` `async def create_api_key(`**
    -   **`payload: APIKeyCreateSchema,`**
    -   **`user: AuthenticatedUser = Depends(get_current_authenticated_user),`** (*Assuming this dependency provides `user.id`*)
    -   **`service: APIKeyService = Depends(get_api_key_service)`**
    -   **`) -> APIKeyCreateResponseSchema:`** (Returns key value only once)
        -   Call `service.generate_key(user_id=user.id, name=payload.name, permissions=payload.permissions)`.
        -   Map domain model to `APIKeyCreateResponseSchema` (includes the one-time secret).
-   **`GET /` `async def list_api_keys(`**
    -   **`user: AuthenticatedUser = Depends(get_current_authenticated_user),`**
    -   **`service: APIKeyService = Depends(get_api_key_service)`**
    -   **`) -> List[APIKeyResponseSchema]:`**
        -   Call `service.list_keys_for_user(user_id=user.id)`.
        -   Map list of domain models to `APIKeyResponseSchema` (excluding secret).
-   **`GET /{api_key_id}` `async def get_api_key(...) -> APIKeyResponseSchema:`**
    -   Ensure user owns the key via `service.get_key_by_id(api_key_id, user_id=user.id)`.
-   **`PUT /{api_key_id}` `async def update_api_key_permissions(...) -> APIKeyResponseSchema:`**
    -   Ensure user owns the key.
    -   Call `service.update_key_permissions(...)`.
-   **`DELETE /{api_key_id}` `async def revoke_api_key(...) -> StatusResponseSchema:`**
    -   Ensure user owns the key.
    -   Call `service.revoke_key(...)`.

#### 3.3.4. `api/routers/webhooks_router.py` (REQ-017)
-   `router = APIRouter(prefix="/webhooks", tags=["Webhooks"], dependencies=[Depends(get_current_authenticated_user)])` (*User auth for management*)
-   **`POST /` `async def register_webhook(...) -> WebhookResponseSchema:`**
    -   Call `service.register_webhook(...)`.
-   **`GET /` `async def list_webhooks(...) -> List[WebhookResponseSchema]:`**
-   **`GET /{webhook_id}` `async def get_webhook(...) -> WebhookResponseSchema:`**
-   **`PUT /{webhook_id}` `async def update_webhook(...) -> WebhookResponseSchema:`**
-   **`DELETE /{webhook_id}` `async def delete_webhook(...) -> StatusResponseSchema:`**

#### 3.3.5. `api/routers/usage_router.py` (REQ-018)
-   `router = APIRouter(prefix="/usage", tags=["API Usage"], dependencies=[Depends(get_current_active_api_client)])` (*API Key auth for usage queries*)
-   **`GET /summary` `async def get_api_usage_summary(`**
    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**
    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**
    -   **`start_date: date = Query(...), end_date: date = Query(...)`**
    -   **`) -> UsageSummaryResponseSchema:`**
        -   Call `usage_service.get_usage_summary(api_client_id=api_client.id, user_id=api_client.user_id, start_date, end_date)`.
-   **`GET /quota` `async def get_current_quota_status(`**
    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**
    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service)`**
    -   **`) -> QuotaStatusResponseSchema:`**
        -   Call `quota_service.get_quota_status(api_client_id=api_client.id, user_id=api_client.user_id)`.

#### 3.3.6. `api/routers/generation_proxy_router.py` (REQ-017)
-   `router = APIRouter(prefix="/proxy/v1", tags=["Platform API Proxy"], dependencies=[Depends(get_current_active_api_client)])`
-   **`POST /generations` `async def initiate_creative_generation_proxy(`**
    -   **`payload: GenerationCreateRequestSchema,`** (*from schemas/generation_schemas.py*)
    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**
    -   **`proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),`**
    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**
    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service),`**
    -   **`rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service)`**
    -   **`) -> GenerationStatusResponseSchema:`**
        -   Check rate limits: `if await rate_limit_service.is_rate_limited(...) raise RateLimitExceededError()`.
        -   Check quotas: `can_proceed = await quota_service.check_and_decrement_quota(...) if not can_proceed: raise InsufficientQuotaError()`.
        -   Call `proxy_service.proxy_initiate_generation(api_client=api_client, payload=payload)`.
        -   Record usage: `await usage_service.record_api_call(...)`.
-   **`GET /generations/{generation_id}` `async def get_generation_status_proxy(...) -> GenerationStatusResponseSchema:`**
    -   Similar rate limit, quota checks (maybe quota not applicable for GETs, or lower cost).
    -   Call `proxy_service.proxy_get_generation_status(...)`.
    -   Record usage.
-   **`GET /assets/{asset_id}` `async def retrieve_asset_details_proxy(...) -> AssetDetailResponseSchema:`**
    -   Similar checks.
    -   Call `proxy_service.proxy_retrieve_asset_details(...)`.
    -   Record usage.
-   *(Further endpoints for asset management and user/team management would follow this pattern, proxying to respective services)*

#### 3.3.7. `api/schemas/` - Pydantic Schemas

##### `api_key_schemas.py`
-   `APIKeyBase(BaseModel)`: `name: str`, `permissions: Optional[Dict[str, bool]] = None`
-   `APIKeyCreateSchema(APIKeyBase)`: `pass`
-   `APIKeyCreateResponseSchema(APIKeyBase)`: `id: UUID`, `key_prefix: str`, `api_key: str` (full key shown once), `is_active: bool`, `created_at: datetime`
-   `APIKeyUpdateSchema(BaseModel)`: `name: Optional[str] = None`, `permissions: Optional[Dict[str, bool]] = None`, `is_active: Optional[bool] = None`
-   `APIKeyResponseSchema(APIKeyBase)`: `id: UUID`, `key_prefix: str`, `is_active: bool`, `created_at: datetime`, `revoked_at: Optional[datetime] = None`

##### `webhook_schemas.py`
-   `WebhookBase(BaseModel)`: `target_url: HttpUrl`, `event_types: List[str]`, `secret: Optional[str] = None` (for HMAC signature)
-   `WebhookCreateSchema(WebhookBase)`: `pass`
-   `WebhookUpdateSchema(BaseModel)`: `target_url: Optional[HttpUrl] = None`, `event_types: Optional[List[str]] = None`, `secret: Optional[str] = None`, `is_active: Optional[bool] = None`
-   `WebhookResponseSchema(WebhookBase)`: `id: UUID`, `user_id: UUID`, `is_active: bool`, `created_at: datetime`

##### `usage_schemas.py`
-   `UsageSummaryDataPoint(BaseModel)`: `endpoint: str`, `call_count: int`, `cost: Optional[Decimal] = None`
-   `UsageSummaryResponseSchema(BaseModel)`: `api_client_id: UUID`, `user_id: UUID`, `period_start: date`, `period_end: date`, `total_calls: int`, `total_cost: Optional[Decimal] = None`, `detailed_usage: List[UsageSummaryDataPoint]`
-   `QuotaStatusResponseSchema(BaseModel)`: `api_client_id: UUID`, `user_id: UUID`, `quota_type: str` (e.g., "generations"), `limit: int`, `remaining: int`, `period: str` (e.g., "monthly"), `resets_at: Optional[datetime] = None`
-   `RateLimitStatusResponseSchema(BaseModel)`: `allowed: bool`, `remaining_requests: Optional[int] = None`, `retry_after_seconds: Optional[int] = None`

##### `generation_schemas.py`
-   `GenerationCreateRequestSchema(BaseModel)`: `prompt: str`, `output_format: str = "png"`, `num_samples: int = 4`, `project_id: Optional[UUID] = None`, `style_preferences: Optional[Dict[str, Any]] = None`, `custom_dimensions: Optional[Tuple[int, int]] = None` (mirroring AI Gen Orch service)
-   `GenerationStatusResponseSchema(BaseModel)`: `generation_id: UUID`, `status: str`, `progress: Optional[int] = None`, `sample_urls: Optional[List[HttpUrl]] = None`, `result_url: Optional[HttpUrl] = None`, `error_message: Optional[str] = None`, `credits_cost_sample: Optional[Decimal] = None`, `credits_cost_final: Optional[Decimal] = None`, `created_at: datetime`, `updated_at: datetime`

##### `asset_schemas.py`
-   `AssetDetailResponseSchema(BaseModel)`: `asset_id: UUID`, `name: str`, `type: str`, `mime_type: str`, `download_url: HttpUrl`, `metadata: Optional[Dict[str, Any]] = None`, `created_at: datetime`
-   *(Other schemas as needed for proxied asset management, e.g., AssetUploadSchema, AssetUpdateSchema)*

##### `user_team_schemas.py`
-   *(Schemas for proxied user/team info, e.g., UserDetailResponseSchema, TeamListResponseSchema)*

##### `base_schemas.py`
-   `StatusResponseSchema(BaseModel)`: `status: str = "success"`, `message: Optional[str] = None`

### 3.4. `application/services/` - Application Services

#### `api_key_service.py`
-   `generate_key(...)`:
    -   Generate a unique prefix (e.g., `cf_dev_`) and a cryptographically secure secret.
    -   Hash the secret using `infrastructure.security.hashing.hash_secret()`.
    -   Create `APIKeyDomainModel` instance.
    -   Call `api_key_repo.add()`.
    -   Return domain model and the *original plain text secret* (to be displayed once).
-   `validate_key(key_value: str) -> Optional[APIKeyDomainModel]`:
    -   Split `key_value` into prefix and plain_secret.
    -   `key_domain = await self.api_key_repo.get_by_key_prefix(key_prefix=prefix)`.
    -   If `key_domain` and `key_domain.is_active` and `hashing.verify_secret(plain_secret, key_domain.secret_hash)`: return `key_domain`.
    -   Else return `None`.
-   Other methods: Straightforward CRUD and business logic using the repository.

#### `webhook_service.py`
-   `register_webhook(...)`:
    -   If `secret` is provided, hash it using `hashing.hash_secret()`.
    -   Create `WebhookDomainModel`.
    -   Call `webhook_repo.add()`.
-   `trigger_event_for_user_webhooks(user_id, event_type, payload)`:
    -   `webhooks = await self.webhook_repo.list_by_user_id_and_event_type(user_id, event_type)`.
    -   For each webhook:
        -   `await self.webhook_publisher.publish_webhook_event(webhook, event_type, payload)`.

#### `usage_tracking_service.py`
-   `record_api_call(...)`: Create `APIUsageRecordDomainModel` and call `usage_repo.add_record()`.
-   `get_usage_summary(...)`: Call `usage_repo.get_summary_for_client()`. Process into DTO.

#### `quota_management_service.py`
-   `check_and_decrement_quota(...)`:
    -   `quota_config = await self.quota_repo.get_quota_by_client_id(...)`.
    -   If no specific quota, use default or tier-based quota (needs integration with user/subscription service or API key permissions).
    -   `current_usage = await self.usage_repo.get_count_for_period(api_client_id, period_start=quota_config.last_reset_at, action_type="generation")` (or similar).
    -   If `current_usage + action_cost <= quota_config.limit_amount`: return True.
    -   Else: raise `InsufficientQuotaError`.
    -   *Note: Decrementing is implicit via `UsageTrackingService.record_api_call`.*
-   `get_quota_status(...)`: Fetch quota config and current usage, calculate remaining.

#### `rate_limiting_service.py`
-   `is_rate_limited(...)`:
    -   Use Redis (via `cache_client`) with a sliding window or token bucket algorithm.
    -   Key could be `f"rate_limit:{api_client_id}:{endpoint_key}"`.
    -   Increment counter. If counter exceeds limit within window, return `True`. Set TTL on keys.

#### `generation_proxy_service.py`
-   `proxy_initiate_generation(...)`:
    -   (Rate limiting and quota checks should be done in the router *before* calling this service, or as a first step here).
    -   Construct request for `ai_gen_client.initiate_generation(payload, auth_token=api_client.internal_auth_token)`. (*Needs a way to get an internal service token for the API client/user*).
    -   Return response.
-   Similar logic for other proxy methods, calling respective clients.

### 3.5. `domain/models/` - Domain Models

#### `api_key.py`
-   **`APIKeyPermissions(BaseModel)`:** Fields for scopes (e.g., `can_generate_creative: bool`, `can_read_assets: bool`).
-   **`APIKey(BaseModel)`:** `id: UUID`, `user_id: UUID`, `name: str`, `key_prefix: str` (e.g., first 8 chars of API key value), `secret_hash: str`, `permissions: APIKeyPermissions`, `is_active: bool = True`, `created_at: datetime = Field(default_factory=datetime.utcnow)`, `revoked_at: Optional[datetime] = None`.
    -   `revoke()`: Sets `is_active = False`, `revoked_at = datetime.utcnow()`.

#### `webhook.py`
-   **`WebhookEvent(str, Enum)`:** e.g., `GENERATION_COMPLETED = "generation.completed"`, `GENERATION_FAILED = "generation.failed"`.
-   **`Webhook(BaseModel)`:** `id: UUID`, `user_id: UUID`, `target_url: HttpUrl`, `event_types: List[WebhookEvent]`, `hashed_secret: Optional[str] = None`, `is_active: bool = True`, `created_at: datetime = Field(default_factory=datetime.utcnow)`.
    -   `generate_signature(payload_body: str) -> Optional[str]`: If `hashed_secret` (actually, the plain secret should be used for signing, then discarded if not stored), calculate HMAC-SHA256. *Correction: Service layer will handle signing using plain secret obtained at creation/update, domain model should not store plain secret.*

#### `usage.py`
-   **`APIUsageRecord(BaseModel)`:** `id: UUID`, `api_client_id: UUID`, `user_id: UUID`, `timestamp: datetime`, `endpoint: str`, `cost: Optional[Decimal] = None`, `is_successful: bool`.
-   **`QuotaPeriod(str, Enum)`:** `DAILY = "daily"`, `MONTHLY = "monthly"`.
-   **`Quota(BaseModel)`:** `id: UUID`, `api_client_id: UUID`, `user_id: UUID`, `limit_amount: int`, `period: QuotaPeriod`, `last_reset_at: datetime`.

### 3.6. `domain/repositories/` - Repository Interfaces
-   Define abstract methods for CRUD operations and specific queries for each domain aggregate/entity, using domain model types in signatures.

### 3.7. `infrastructure/` - Infrastructure Layer

#### `database/session.py`
-   As per file structure: `AsyncEngine`, `async_sessionmaker`, `get_async_db_session` generator.

#### `database/models/`
-   SQLAlchemy ORM models (`APIKeyModel`, `WebhookModel`, `UsageRecordModel`, `QuotaModel`) mirroring domain models and database table structures defined in the "Database Design" input. Ensure appropriate `ForeignKey` constraints and indexing.

#### `database/repositories/`
-   Implementations of repository interfaces using SQLAlchemy `AsyncSession` and ORM models.
-   **`SqlAlchemyApiKeyRepository`**:
    -   `get_by_key_prefix`: Query `APIKeyModel` where `key_prefix` matches.
-   **`SqlAlchemyWebhookRepository`**:
    -   `list_by_user_id_and_event_type`: Query `WebhookModel` where `user_id` matches and `event_types` array contains the given event.
-   **`SqlAlchemyUsageRepository`**:
    -   `get_summary_for_client`: Query `UsageRecordModel`, aggregate data.
-   **`SqlAlchemyQuotaRepository`**:
    -   `get_current_usage_for_quota_period`: This might be complex. It would query `UsageRecordModel` table to count relevant actions since `quota.last_reset_at`.

#### `database/migrations/env.py`
-   Standard Alembic setup, ensuring `target_metadata` points to `infrastructure.database.models.base.Base.metadata`.

#### `messaging/rabbitmq_client.py`
-   **`class RabbitMQClient`:**
    -   `connect()`: `aio_pika.connect_robust(...)`.
    -   `get_channel()`: `await self.connection.channel()`.
    -   `close()`: `await self.connection.close()`.

#### `messaging/webhook_publisher.py`
-   **`class WebhookPublisher(IWebhookPublisher)`:** (*Define IWebhookPublisher interface first*)
    -   `__init__(rabbitmq_client: RabbitMQClient, exchange_name: str)`
    -   `publish_webhook_event(webhook: WebhookDomainModel, event_type: str, payload: dict)`:
        -   `channel = await self.rabbitmq_client.get_channel()`.
        -   `exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True)`.
        -   Prepare message body (JSON string): `{"target_url": webhook.target_url, "payload": payload, "secret": webhook.secret_for_signing, "event_type": event_type}`. *Correction: The publisher should send details so a separate worker can do the HTTP POST and signing. The WebhookDomainModel likely won't have the plain secret. The service layer retrieving the webhook could pass the plain secret if it's temporarily decrypted/retrieved for this purpose, or the signature is generated here by the service and passed in the message.* Let's assume the service layer handles the secret part and passes the raw payload and signature instructions.
        -   Message structure for worker: `{"webhook_id": webhook.id, "target_url": webhook.target_url, "raw_payload": json.dumps(payload), "event_type": event_type, "signature_secret_ref": webhook.id}` (worker retrieves secret from Vault using webhook.id as ref).
        -   `routing_key = f"{settings.RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX}.{event_type}.{webhook.user_id}"`.
        -   `await exchange.publish(aio_pika.Message(body=message_body.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT), routing_key=routing_key)`.

#### `security/hashing.py`
-   Use `passlib.context.CryptContext` with `bcrypt` or `argon2`.
    -   `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`
    -   `hash_secret(secret: str) -> str: return pwd_context.hash(secret)`
    -   `verify_secret(plain_secret: str, hashed_secret: str) -> bool: return pwd_context.verify(plain_secret, hashed_secret)`

#### `external_clients/`
-   **Base Client (Conceptual):**
    -   `__init__(base_url: str, timeout: int = 5)`: `self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)`
    -   `async def _request(method, endpoint, headers=None, json=None, data=None, params=None) -> httpx.Response:`
        -   Implement retry logic (e.g., using `tenacity` library) for transient errors (5xx, network errors).
        -   Implement circuit breaker (e.g., using `pybreaker` or custom logic with Redis).
        -   Make request: `await self.client.request(...)`.
        -   Handle HTTP errors (4xx, 5xx) and raise `ExternalServiceError`.
    -   `async def close_client(): await self.client.aclose()`
-   **`AIGenerationClient`**: Methods map to AI Gen Orch Service endpoints.
-   **`AssetManagementClient`**: Methods map to Asset Mgmt Service endpoints.
-   **`UserTeamClient`**: Methods map to User/Team Mgmt Service endpoints.

## 4. Data Design
The database design for this service will primarily involve the following tables, as described in the "Database Design" input and relevant to this service's scope:
-   `APIClient` (renamed to `api_keys` in ORM model `APIKeyModel` for clarity)
-   `Webhook` (ORM model `WebhookModel`)
-   `APIUsageRecord` (ORM model `UsageRecordModel`)
-   `Quota` (ORM model `QuotaModel`)

Relationships:
-   `APIKeyModel` has a `user_id` (foreign key to a conceptual `users` table, managed by User Management service).
-   `WebhookModel` has a `user_id`.
-   `UsageRecordModel` has `api_client_db_id` (FK to `api_keys.id`) and `user_id`.
-   `QuotaModel` has `api_client_db_id` (FK to `api_keys.id`) and `user_id`.

Data types and constraints will follow the Pydantic domain models and SQLAlchemy ORM definitions.

## 5. API Design
The public-facing API for developers will be defined in `api/openapi.yaml` following OpenAPI 3.x specification.
Key endpoint groups:
-   `/api-keys`: CRUD operations for API keys.
-   `/webhooks`: CRUD operations for webhooks.
-   `/usage`: Endpoints for querying API usage and quota status.
-   `/proxy/v1/*`: Endpoints for proxying requests to internal services:
    -   `/proxy/v1/generations`: Initiate, get status.
    -   `/proxy/v1/assets`: Retrieve details, manage.
    -   `/proxy/v1/users`, `/proxy/v1/teams`: Manage user/team resources (scoped).

Authentication:
-   Management endpoints (`/api-keys`, `/webhooks` when managed by a user for themselves) would typically be authenticated via user session JWT from the main web application or a dedicated developer portal session.
-   Proxied API endpoints (`/proxy/v1/*`) and usage queries (`/usage`) are authenticated via `X-API-KEY` header.

## 6. Security Considerations (REQ-018, SEC-001, SEC-005)
-   **API Key Security:**
    -   Secrets are hashed using bcrypt/Argon2.
    -   Plaintext secret displayed only once upon creation.
    -   Keys can be revoked.
    -   Permissions/scopes to limit key capabilities.
-   **Webhook Security:**
    -   Optional shared secret for HMAC-SHA256 signature verification of webhook payloads. The service generating the event to be sent via webhook (e.g., Generation Orchestration service after a generation completes) will be responsible for using the webhook's secret to sign the payload *before* it's put on the RabbitMQ queue for the `WebhookPublisher` in *this* service to then send out. *Correction:* The `WebhookPublisher` in this service should be responsible for retrieving the secret (e.g. from Vault, or if stored encrypted in DB with WebhookModel) and generating the signature before dispatching the HTTP POST request to the `target_url`. The RabbitMQ message to the worker/publisher should contain enough info to retrieve the secret.
-   **Input Validation:** Pydantic schemas enforce strict input validation for all API requests.
-   **Output Encoding:** FastAPI handles JSON response encoding, mitigating common XSS vectors for API consumers.
-   **Rate Limiting & Quotas:** Implemented to prevent abuse and manage resource consumption.
-   **Authentication:** All sensitive endpoints require authentication.
-   **Authorization:** Permissions check for API key operations and proxied requests.
-   **Dependencies:** Secure communication (HTTPS) with external and internal services.
-   **Secret Management:** Application secrets (DB URL, RabbitMQ URL, HMAC keys) managed via `core.config` (environment variables) and not hardcoded. For production, these should be injected by a secure deployment system (e.g., K8s secrets, HashiCorp Vault).

## 7. Deployment Considerations
-   The service will be containerized using Docker.
-   `requirements.txt` and `pyproject.toml` define dependencies.
-   Database migrations managed by Alembic, integrated into CI/CD.
-   Environment variables for configuration.
-   Deployed as part of the microservices architecture, likely behind an API Gateway/Load Balancer for external traffic.

## 8. Error Handling and Logging
-   Custom exceptions defined in `core.exceptions` are handled by global FastAPI exception handlers to return standardized JSON error responses.
-   Structured JSON logging configured via `core.logging_config`, including correlation IDs where possible (e.g., passed via headers or generated per request).
-   Detailed error information logged for debugging, while user-facing messages are kept generic and informative.
-   Errors from external service calls are caught and wrapped in `ExternalServiceError` or more specific custom exceptions.

## 9. Testing Strategy (as per QA-001)
-   **Unit Tests (PyTest):**
    -   Domain model logic.
    -   Application service business logic (with mocked repositories/clients).
    -   Utility functions (hashing, config loading).
-   **Integration Tests (PyTest with `httpx.AsyncClient` for FastAPI's `TestClient`, and actual DB/RabbitMQ instances in test environment):**
    -   API endpoint request/response validation and behavior.
    -   Service interactions with real database repositories.
    -   Webhook publishing to RabbitMQ and verification of message content/routing.
    -   Interaction with mocked external service clients.
-   **Contract Tests (Pact or similar):** For interactions with AI Generation Service, Asset Management Service, User/Team Service to ensure API compatibility. (This would be part of their respective test suites and this service's client tests).

This SDS provides a comprehensive blueprint for developing the `CreativeFlow.DeveloperPlatformService`. It details the structure, functionality, and interactions necessary to fulfill its requirements within the CreativeFlow AI ecosystem.json
{
  "sds": "# Software Design Specification: CreativeFlow.DeveloperPlatformService\n\n## 1. Introduction\n\n### 1.1. Purpose\nThis document provides a detailed software design specification for the `CreativeFlow.DeveloperPlatformService`. This microservice is a core component of the CreativeFlow AI platform, dedicated to managing third-party developer access and interactions via the platform's API. Its primary responsibilities include API key management, webhook configuration and event dispatch, API usage tracking, monetization enforcement (rate limiting, quotas), and proxying authenticated API requests to relevant backend services.\n\n### 1.2. Scope\nThe scope of this document covers the design of the `CreativeFlow.DeveloperPlatformService` including:\n-   API endpoint definitions for managing API keys and webhooks.\n-   Endpoints for developers to query their API usage and quota status.\n-   Proxy endpoints for creative generation, asset management, and user/team management operations initiated by API clients.\n-   Internal logic for API key validation, permissioning, rate limiting, and quota enforcement.\n-   Integration with the PostgreSQL database for persistence.\n-   Integration with RabbitMQ for asynchronous webhook event publishing.\n-   Integration with other internal microservices (AI Generation, Asset Management, User/Team Management, Authentication) via HTTP clients.\n\n### 1.3. Definitions, Acronyms, and Abbreviations\n-   **API:** Application Programming Interface\n-   **CRUD:** Create, Read, Update, Delete\n-   **CI/CD:** Continuous Integration/Continuous Deployment\n-   **DTO:** Data Transfer Object\n-   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.\n-   **HMAC:** Hash-based Message Authentication Code\n-   **HTTP:** Hypertext Transfer Protocol\n-   **IaC:** Infrastructure-as-Code\n-   **JWT:** JSON Web Token\n-   **K8s:** Kubernetes\n-   **ORM:** Object-Relational Mapper\n-   **PWA:** Progressive Web Application\n-   **Pydantic:** Data validation and settings management using Python type annotations.\n-   **SQLAlchemy:** SQL toolkit and Object-Relational Mapper for Python.\n-   **SDS:** Software Design Specification\n-   **VO:** Value Object\n-   **SDK:** Software Development Kit\n\n## 2. System Overview\n\n### 2.1. Service Architecture\nThe `CreativeFlow.DeveloperPlatformService` is a Python-based microservice built using the FastAPI framework. It follows a layered architecture:\n-   **API Layer (`api/`):** Handles HTTP requests, request/response validation (Pydantic schemas), and authentication/authorization. Contains routers and dependencies.\n-   **Application Layer (`application/`):** Contains service classes that orchestrate business logic, interacting with the domain layer and infrastructure layer.\n-   **Domain Layer (`domain/`):** Defines core business entities, value objects, and repository interfaces, encapsulating business rules.\n-   **Infrastructure Layer (`infrastructure/`):** Implements data persistence (SQLAlchemy repositories), messaging (RabbitMQ client), and communication with other external/internal services (HTTP clients).\n\nIt interacts with:\n-   **PostgreSQL Database:** For storing API keys, webhook configurations, usage records, and quotas.\n-   **RabbitMQ:** For publishing webhook events asynchronously.\n-   **Authentication Service:** For validating user identity when managing API keys or webhooks (if user-scoped).\n-   **AI Generation Orchestration Service:** To proxy creative generation requests.\n-   **Asset Management Service:** To proxy asset-related requests.\n-   **User/Team Management Service:** To proxy user/team-related requests.\n\n### 2.2. Key Features\n-   **API Key Management (REQ-017, SEC-001):**\n    -   Secure generation of API keys and secrets.\n    -   Storage of hashed API secrets.\n    -   Revocation and activation/deactivation of API keys.\n    -   Assignment of granular permissions/scopes to API keys (future).\n-   **Webhook Management (REQ-017):**\n    -   Registration and management of webhook endpoints by developers.\n    -   Subscription to specific event types (e.g., `generation.completed`).\n    -   Secure event dispatch via RabbitMQ, including HMAC signatures for payload verification.\n-   **API Monetization & Control (REQ-018):**\n    -   Tracking API usage per client/key.\n    -   Enforcing rate limits (e.g., requests per second/minute).\n    -   Enforcing usage quotas (e.g., generations per month).\n    -   Providing endpoints for developers to view their usage and quota status.\n-   **API Request Proxying (REQ-017):**\n    -   Acting as an authenticated gateway for API clients to access core platform functionalities like:\n        -   Initiating creative generation.\n        -   Querying generation status.\n        -   Retrieving asset details.\n        -   Managing user-uploaded source assets.\n        -   Performing user/team management operations (scoped).\n-   **Security (SEC-005):**\n    -   API key-based authentication.\n    -   Input validation and sanitization.\n    -   Protection against common web vulnerabilities.\n\n## 3. Core Module Design\n\n### 3.1. `main.py` - Application Entrypoint\n-   **Purpose:** Initializes and configures the FastAPI application.\n-   **`create_application() -> FastAPI`:**\n    -   Instantiates `FastAPI` app.\n    -   Loads settings from `core.config.Settings`.\n    -   Configures CORS middleware (allow specific origins or all for development).\n    -   Includes API routers from `api.routers.*`.\n    -   Sets up global exception handlers from `core.exceptions`.\n    -   Calls `core.logging_config.setup_logging()`.\n-   **`startup_event() -> None` (async):**\n    -   Attached to `app.on_event(\"startup\")`.\n    -   Initialize database engine/connection pool (if not handled by `get_db_session` on first use).\n    -   Initialize RabbitMQ client connection (`infrastructure.messaging.rabbitmq_client.connect()`).\n    -   Initialize HTTP clients for external services (`infrastructure.external_clients.*.init_client()`).\n-   **`shutdown_event() -> None` (async):**\n    -   Attached to `app.on_event(\"shutdown\")`.\n    -   Close RabbitMQ client connection (`infrastructure.messaging.rabbitmq_client.close()`).\n    -   Close HTTP clients for external services (`infrastructure.external_clients.*.close_client()`).\n-   **Global Exception Handlers:**\n    -   Generic `HTTPException` handler.\n    -   Handler for `RequestValidationError` to return 422 with detailed errors.\n    -   Custom application exception handlers defined in `core.exceptions`.\n\n### 3.2. `core/` - Core Utilities and Configurations\n\n#### 3.2.1. `core/config.py`\n-   **Purpose:** Manages application configuration.\n-   **`class Settings(BaseSettings)`:**\n    -   `DATABASE_URL: str` (e.g., `postgresql+asyncpg://user:pass@host:port/db`)\n    -   `RABBITMQ_URL: str` (e.g., `amqp://guest:guest@localhost:5672/`)\n    -   `JWT_SECRET_KEY: str` (For decoding tokens from Auth service, if needed for verifying user actions on API keys/webhooks).\n    -   `AI_GENERATION_SERVICE_URL: str` (Base URL for AI Generation Orchestration Service).\n    -   `ASSET_MANAGEMENT_SERVICE_URL: str` (Base URL for Asset Management Service).\n    -   `USER_TEAM_SERVICE_URL: str` (Base URL for User/Team Management Service).\n    -   `AUTH_SERVICE_URL: str` (Base URL for Authentication Service, e.g., for user token validation).\n    -   `API_KEY_HEADER_NAME: str = \"X-API-KEY\"`\n    -   `WEBHOOK_HMAC_SECRET_KEY: str` (A global secret for signing webhook payloads, or allow per-webhook secrets).\n    -   `LOG_LEVEL: str = \"INFO\"`\n    -   `RABBITMQ_WEBHOOK_EXCHANGE_NAME: str = \"webhook_events_exchange\"`\n    -   `RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX: str = \"webhook.event\"`\n    -   `DEFAULT_RATE_LIMIT_REQUESTS: int = 100`\n    -   `DEFAULT_RATE_LIMIT_PERIOD_SECONDS: int = 60`\n    -   Model configuration: `model_config = SettingsConfigDict(env_file=\".env\", extra=\"ignore\")`\n-   **`@lru_cache` `def get_settings() -> Settings:`:** Returns a cached instance of `Settings`.\n\n#### 3.2.2. `core/exceptions.py`\n-   **Purpose:** Defines custom exceptions and handlers.\n-   **`class AppException(HTTPException)`:** Base custom exception.\n-   **`class APIKeyNotFoundError(AppException)`:** `status_code=404`, `detail=\"API Key not found.\"`\n-   **`class APIKeyInactiveError(AppException)`:** `status_code=403`, `detail=\"API Key is inactive.\"`\n-   **`class APIKeyPermissionDeniedError(AppException)`:** `status_code=403`, `detail=\"API Key does not have sufficient permissions.\"`\n-   **`class WebhookNotFoundError(AppException)`:** `status_code=404`, `detail=\"Webhook not found.\"`\n-   **`class InsufficientQuotaError(AppException)`:** `status_code=429`, `detail=\"API quota exceeded.\"` (REQ-018)\n-   **`class RateLimitExceededError(AppException)`:** `status_code=429`, `detail=\"Rate limit exceeded.\"` (REQ-018)\n-   **`class InvalidUserInputError(AppException)`:** `status_code=400`, `detail=\"Invalid user input.\"`\n-   **`class ExternalServiceError(AppException)`:** `status_code=502`, `detail=\"Error communicating with an external service.\"`\n-   **FastAPI Exception Handlers:**\n    -   `async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:`\n    -   `async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:` (Logs error, returns generic 500)\n    -   `async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:` (Logs error, returns generic 500)\n\n#### 3.2.3. `core/logging_config.py`\n-   **Purpose:** Configures structured logging.\n-   **`def setup_logging(log_level: str = \"INFO\") -> None:`:**\n    -   Uses `logging.config.dictConfig` or direct logger configuration.\n    -   Configures `python-json-logger.JSONFormatter` if chosen.\n    -   Includes timestamp, level, message, module, function name, line number, and correlation ID (if available via middleware).\n    -   Sets root logger level based on `log_level` from config.\n\n### 3.3. `api/` - API Layer\n\n#### 3.3.1. `api/dependencies/authentication.py`\n-   **Purpose:** Handles API key authentication.\n-   **`api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=True)`**\n-   **`async def get_current_active_api_client(`**\n    -   **`api_key_header_val: str = Security(api_key_header),`**\n    -   **`api_key_service: APIKeyService = Depends(get_api_key_service)`**\n    -   **`) -> APIKeyDomainModel:`** (REQ-017, SEC-001, SEC-005)\n        -   Extract API key value from header.\n        -   Call `api_key_service.validate_key(key_value=api_key_header_val)` which should check both the key format and the hashed secret.\n            -   *Correction:* The header should contain the full API key (prefix + secret part). The service then splits it, finds the APIKey by prefix, and verifies the secret part against the stored hash.\n        -   If `api_key_domain_model` is None or not `api_key_domain_model.is_active`, raise `HTTPException(status_code=401, detail=\"Invalid or inactive API Key\")`.\n        -   Return `api_key_domain_model`.\n        -   *Note: Permission checks based on scope should be done within individual route handlers or a separate permission dependency, using the returned `api_key_domain_model.permissions`.*\n\n#### 3.3.2. `api/dependencies/common.py`\n-   **Purpose:** Provides common dependencies for injection.\n-   **`async def get_db_session() -> AsyncGenerator[AsyncSession, None]:`** Yields an `AsyncSession` from `infrastructure.database.session.AsyncSessionLocal`.\n-   **`async def get_rabbitmq_client() -> RabbitMQClient:`:** Returns an initialized `RabbitMQClient` instance (singleton or managed).\n-   **`async def get_ai_generation_client() -> AIGenerationClient:`:** Returns an initialized `AIGenerationClient`.\n-   **`async def get_asset_management_client() -> AssetManagementClient:`:** Returns an initialized `AssetManagementClient`.\n-   **`async def get_user_team_client() -> UserTeamClient:`:** Returns an initialized `UserTeamClient`.\n-   **`async def get_webhook_publisher(rabbitmq_client: RabbitMQClient = Depends(get_rabbitmq_client)) -> WebhookPublisher:`:** Instantiates and returns `WebhookPublisher`.\n-   **`def get_api_key_service(db_session: AsyncSession = Depends(get_db_session)) -> APIKeyService:`:** Instantiates and returns `APIKeyService` with `SqlAlchemyApiKeyRepository`.\n-   **`def get_webhook_service(db_session: AsyncSession = Depends(get_db_session), webhook_publisher: WebhookPublisher = Depends(get_webhook_publisher)) -> WebhookService:`:** Instantiates `WebhookService`.\n-   **`def get_usage_tracking_service(db_session: AsyncSession = Depends(get_db_session)) -> UsageTrackingService:`:** Instantiates `UsageTrackingService`.\n-   **`def get_quota_management_service(db_session: AsyncSession = Depends(get_db_session), usage_service: UsageTrackingService = Depends(get_usage_tracking_service)) -> QuotaManagementService:`:** Instantiates `QuotaManagementService`.\n-   **`def get_rate_limiting_service(redis_client = Depends(get_redis_client_dependency)) -> RateLimitingService:`:** Instantiates `RateLimitingService`. (Requires a Redis client dependency, to be added).\n-   **`def get_generation_proxy_service(`**\n    -   **`ai_gen_client: AIGenerationClient = Depends(get_ai_generation_client),`**\n    -   **`asset_mgmt_client: AssetManagementClient = Depends(get_asset_management_client),`**\n    -   **`user_team_client: UserTeamClient = Depends(get_user_team_client),`**\n    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**\n    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service),`**\n    -   **`rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service)`**\n    -   **`) -> GenerationProxyService:`** Instantiates `GenerationProxyService`.\n\n#### 3.3.3. `api/routers/api_keys_router.py` (REQ-017, SEC-001)\n-   `router = APIRouter(prefix=\"/api-keys\", tags=[\"API Keys\"], dependencies=[Depends(get_current_active_api_client)])`\n    -   *Correction*: The base router dependency should be a user authentication check (e.g. JWT from web app session) for managing keys. Individual API calls using the key will use `get_current_active_api_client`. For this router, let's assume a `get_current_authenticated_user` dependency that provides a `user_id`.\n-   **`POST /` `async def create_api_key(`**\n    -   **`payload: APIKeyCreateSchema,`**\n    -   **`user: AuthenticatedUser = Depends(get_current_authenticated_user),`** (*Assuming this dependency provides `user.id`*)\n    -   **`service: APIKeyService = Depends(get_api_key_service)`**\n    -   **`) -> APIKeyCreateResponseSchema:`** (Returns key value only once)\n        -   Call `service.generate_key(user_id=user.id, name=payload.name, permissions=payload.permissions)`.\n        -   Map domain model to `APIKeyCreateResponseSchema` (includes the one-time secret).\n-   **`GET /` `async def list_api_keys(`**\n    -   **`user: AuthenticatedUser = Depends(get_current_authenticated_user),`**\n    -   **`service: APIKeyService = Depends(get_api_key_service)`**\n    -   **`) -> List[APIKeyResponseSchema]:`**\n        -   Call `service.list_keys_for_user(user_id=user.id)`.\n        -   Map list of domain models to `APIKeyResponseSchema` (excluding secret).\n-   **`GET /{api_key_id}` `async def get_api_key(...) -> APIKeyResponseSchema:`**\n    -   Ensure user owns the key via `service.get_key_by_id(api_key_id, user_id=user.id)`.\n-   **`PUT /{api_key_id}` `async def update_api_key_permissions(...) -> APIKeyResponseSchema:`**\n    -   Ensure user owns the key.\n    -   Call `service.update_key_permissions(...)`.\n-   **`DELETE /{api_key_id}` `async def revoke_api_key(...) -> StatusResponseSchema:`**\n    -   Ensure user owns the key.\n    -   Call `service.revoke_key(...)`.\n\n#### 3.3.4. `api/routers/webhooks_router.py` (REQ-017)\n-   `router = APIRouter(prefix=\"/webhooks\", tags=[\"Webhooks\"], dependencies=[Depends(get_current_authenticated_user)])` (*User auth for management*)\n-   **`POST /` `async def register_webhook(...) -> WebhookResponseSchema:`**\n    -   Call `service.register_webhook(...)`.\n-   **`GET /` `async def list_webhooks(...) -> List[WebhookResponseSchema]:`**\n-   **`GET /{webhook_id}` `async def get_webhook(...) -> WebhookResponseSchema:`**\n-   **`PUT /{webhook_id}` `async def update_webhook(...) -> WebhookResponseSchema:`**\n-   **`DELETE /{webhook_id}` `async def delete_webhook(...) -> StatusResponseSchema:`**\n\n#### 3.3.5. `api/routers/usage_router.py` (REQ-018)\n-   `router = APIRouter(prefix=\"/usage\", tags=[\"API Usage\"], dependencies=[Depends(get_current_active_api_client)])` (*API Key auth for usage queries*)\n-   **`GET /summary` `async def get_api_usage_summary(`**\n    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**\n    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**\n    -   **`start_date: date = Query(...), end_date: date = Query(...)`**\n    -   **`) -> UsageSummaryResponseSchema:`**\n        -   Call `usage_service.get_usage_summary(api_client_id=api_client.id, user_id=api_client.user_id, start_date, end_date)`.\n-   **`GET /quota` `async def get_current_quota_status(`**\n    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**\n    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service)`**\n    -   **`) -> QuotaStatusResponseSchema:`**\n        -   Call `quota_service.get_quota_status(api_client_id=api_client.id, user_id=api_client.user_id)`.\n\n#### 3.3.6. `api/routers/generation_proxy_router.py` (REQ-017)\n-   `router = APIRouter(prefix=\"/proxy/v1\", tags=[\"Platform API Proxy\"], dependencies=[Depends(get_current_active_api_client)])`\n-   **`POST /generations` `async def initiate_creative_generation_proxy(`**\n    -   **`payload: GenerationCreateRequestSchema,`** (*from schemas/generation_schemas.py*)\n    -   **`api_client: APIKeyDomainModel = Depends(get_current_active_api_client),`**\n    -   **`proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),`**\n    -   **`usage_service: UsageTrackingService = Depends(get_usage_tracking_service),`**\n    -   **`quota_service: QuotaManagementService = Depends(get_quota_management_service),`**\n    -   **`rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service)`**\n    -   **`) -> GenerationStatusResponseSchema:`**\n        -   Check rate limits: `if await rate_limit_service.is_rate_limited(...) raise RateLimitExceededError()`.\n        -   Check quotas: `can_proceed = await quota_service.check_and_decrement_quota(...) if not can_proceed: raise InsufficientQuotaError()`.\n        -   Call `proxy_service.proxy_initiate_generation(api_client=api_client, payload=payload)`.\n        -   Record usage: `await usage_service.record_api_call(...)`.\n-   **`GET /generations/{generation_id}` `async def get_generation_status_proxy(...) -> GenerationStatusResponseSchema:`**\n    -   Similar rate limit, quota checks (maybe quota not applicable for GETs, or lower cost).\n    -   Call `proxy_service.proxy_get_generation_status(...)`.\n    -   Record usage.\n-   **`GET /assets/{asset_id}` `async def retrieve_asset_details_proxy(...) -> AssetDetailResponseSchema:`**\n    -   Similar checks.\n    -   Call `proxy_service.proxy_retrieve_asset_details(...)`.\n    -   Record usage.\n-   *(Further endpoints for asset management and user/team management would follow this pattern, proxying to respective services)*\n\n#### 3.3.7. `api/schemas/` - Pydantic Schemas\n\n##### `api_key_schemas.py`\n-   `APIKeyBase(BaseModel)`: `name: str`, `permissions: Optional[Dict[str, bool]] = None`\n-   `APIKeyCreateSchema(APIKeyBase)`: `pass`\n-   `APIKeyCreateResponseSchema(APIKeyBase)`: `id: UUID`, `key_prefix: str`, `api_key: str` (full key shown once), `is_active: bool`, `created_at: datetime`\n-   `APIKeyUpdateSchema(BaseModel)`: `name: Optional[str] = None`, `permissions: Optional[Dict[str, bool]] = None`, `is_active: Optional[bool] = None`\n-   `APIKeyResponseSchema(APIKeyBase)`: `id: UUID`, `key_prefix: str`, `is_active: bool`, `created_at: datetime`, `revoked_at: Optional[datetime] = None`\n\n##### `webhook_schemas.py`\n-   `WebhookBase(BaseModel)`: `target_url: HttpUrl`, `event_types: List[str]`, `secret: Optional[str] = None` (for HMAC signature)\n-   `WebhookCreateSchema(WebhookBase)`: `pass`\n-   `WebhookUpdateSchema(BaseModel)`: `target_url: Optional[HttpUrl] = None`, `event_types: Optional[List[str]] = None`, `secret: Optional[str] = None`, `is_active: Optional[bool] = None`\n-   `WebhookResponseSchema(WebhookBase)`: `id: UUID`, `user_id: UUID`, `is_active: bool`, `created_at: datetime`\n\n##### `usage_schemas.py`\n-   `UsageSummaryDataPoint(BaseModel)`: `endpoint: str`, `call_count: int`, `cost: Optional[Decimal] = None`\n-   `UsageSummaryResponseSchema(BaseModel)`: `api_client_id: UUID`, `user_id: UUID`, `period_start: date`, `period_end: date`, `total_calls: int`, `total_cost: Optional[Decimal] = None`, `detailed_usage: List[UsageSummaryDataPoint]`\n-   `QuotaStatusResponseSchema(BaseModel)`: `api_client_id: UUID`, `user_id: UUID`, `quota_type: str` (e.g., \"generations\"), `limit: int`, `remaining: int`, `period: str` (e.g., \"monthly\"), `resets_at: Optional[datetime] = None`\n-   `RateLimitStatusResponseSchema(BaseModel)`: `allowed: bool`, `remaining_requests: Optional[int] = None`, `retry_after_seconds: Optional[int] = None`\n\n##### `generation_schemas.py`\n-   `GenerationCreateRequestSchema(BaseModel)`: `prompt: str`, `output_format: str = \"png\"`, `num_samples: int = 4`, `project_id: Optional[UUID] = None`, `style_preferences: Optional[Dict[str, Any]] = None`, `custom_dimensions: Optional[Tuple[int, int]] = None` (mirroring AI Gen Orch service)\n-   `GenerationStatusResponseSchema(BaseModel)`: `generation_id: UUID`, `status: str`, `progress: Optional[int] = None`, `sample_urls: Optional[List[HttpUrl]] = None`, `result_url: Optional[HttpUrl] = None`, `error_message: Optional[str] = None`, `credits_cost_sample: Optional[Decimal] = None`, `credits_cost_final: Optional[Decimal] = None`, `created_at: datetime`, `updated_at: datetime`\n\n##### `asset_schemas.py`\n-   `AssetDetailResponseSchema(BaseModel)`: `asset_id: UUID`, `name: str`, `type: str`, `mime_type: str`, `download_url: HttpUrl`, `metadata: Optional[Dict[str, Any]] = None`, `created_at: datetime`\n-   *(Other schemas as needed for proxied asset management, e.g., AssetUploadSchema, AssetUpdateSchema)*\n\n##### `user_team_schemas.py`\n-   *(Schemas for proxied user/team info, e.g., UserDetailResponseSchema, TeamListResponseSchema)*\n\n##### `base_schemas.py`\n-   `StatusResponseSchema(BaseModel)`: `status: str = \"success\"`, `message: Optional[str] = None`\n\n### 3.4. `application/services/` - Application Services\n\n#### `api_key_service.py`\n-   `generate_key(...)`:\n    -   Generate a unique prefix (e.g., `cf_dev_`) and a cryptographically secure secret.\n    -   Hash the secret using `infrastructure.security.hashing.hash_secret()`.\n    -   Create `APIKeyDomainModel` instance.\n    -   Call `api_key_repo.add()`.\n    -   Return domain model and the *original plain text secret* (to be displayed once).\n-   `validate_key(key_value: str) -> Optional[APIKeyDomainModel]`:\n    -   Split `key_value` into prefix and plain_secret.\n    -   `key_domain = await self.api_key_repo.get_by_key_prefix(key_prefix=prefix)`.\n    -   If `key_domain` and `key_domain.is_active` and `hashing.verify_secret(plain_secret, key_domain.secret_hash)`: return `key_domain`.\n    -   Else return `None`.\n-   Other methods: Straightforward CRUD and business logic using the repository.\n\n#### `webhook_service.py`\n-   `register_webhook(...)`:\n    -   If `secret` is provided, hash it using `hashing.hash_secret()`.\n    -   Create `WebhookDomainModel`.\n    -   Call `webhook_repo.add()`.\n-   `trigger_event_for_user_webhooks(user_id, event_type, payload)`:\n    -   `webhooks = await self.webhook_repo.list_by_user_id_and_event_type(user_id, event_type)`.\n    -   For each webhook:\n        -   `await self.webhook_publisher.publish_webhook_event(webhook, event_type, payload)`.\n\n#### `usage_tracking_service.py`\n-   `record_api_call(...)`: Create `APIUsageRecordDomainModel` and call `usage_repo.add_record()`.\n-   `get_usage_summary(...)`: Call `usage_repo.get_summary_for_client()`. Process into DTO.\n\n#### `quota_management_service.py`\n-   `check_and_decrement_quota(...)`:\n    -   `quota_config = await self.quota_repo.get_quota_by_client_id(...)`.\n    -   If no specific quota, use default or tier-based quota (needs integration with user/subscription service or API key permissions).\n    -   `current_usage = await self.usage_repo.get_count_for_period(api_client_id, period_start=quota_config.last_reset_at, action_type=\"generation\")` (or similar).\n    -   If `current_usage + action_cost <= quota_config.limit_amount`: return True.\n    -   Else: raise `InsufficientQuotaError`.\n    -   *Note: Decrementing is implicit via `UsageTrackingService.record_api_call`.*\n-   `get_quota_status(...)`: Fetch quota config and current usage, calculate remaining.\n\n#### `rate_limiting_service.py`\n-   `is_rate_limited(...)`:\n    -   Use Redis (via `cache_client`) with a sliding window or token bucket algorithm.\n    -   Key could be `f\"rate_limit:{api_client_id}:{endpoint_key}\"`.\n    -   Increment counter. If counter exceeds limit within window, return `True`. Set TTL on keys.\n\n#### `generation_proxy_service.py`\n-   `proxy_initiate_generation(...)`:\n    -   (Rate limiting and quota checks should be done in the router *before* calling this service, or as a first step here).\n    -   Construct request for `ai_gen_client.initiate_generation(payload, auth_token=api_client.internal_auth_token)`. (*Needs a way to get an internal service token for the API client/user*).\n    -   Return response.\n-   Similar logic for other proxy methods, calling respective clients.\n\n### 3.5. `domain/models/` - Domain Models\n\n#### `api_key.py`\n-   **`APIKeyPermissions(BaseModel)`:** Fields for scopes (e.g., `can_generate_creative: bool`, `can_read_assets: bool`).\n-   **`APIKey(BaseModel)`:** `id: UUID`, `user_id: UUID`, `name: str`, `key_prefix: str` (e.g., first 8 chars of API key value), `secret_hash: str`, `permissions: APIKeyPermissions`, `is_active: bool = True`, `created_at: datetime = Field(default_factory=datetime.utcnow)`, `revoked_at: Optional[datetime] = None`.\n    -   `revoke()`: Sets `is_active = False`, `revoked_at = datetime.utcnow()`.\n\n#### `webhook.py`\n-   **`WebhookEvent(str, Enum)`:** e.g., `GENERATION_COMPLETED = \"generation.completed\"`, `GENERATION_FAILED = \"generation.failed\"`.\n-   **`Webhook(BaseModel)`:** `id: UUID`, `user_id: UUID`, `target_url: HttpUrl`, `event_types: List[WebhookEvent]`, `hashed_secret: Optional[str] = None`, `is_active: bool = True`, `created_at: datetime = Field(default_factory=datetime.utcnow)`.\n    -   `generate_signature(payload_body: str) -> Optional[str]`: If `hashed_secret` (actually, the plain secret should be used for signing, then discarded if not stored), calculate HMAC-SHA256. *Correction: Service layer will handle signing using plain secret obtained at creation/update, domain model should not store plain secret.*\n\n#### `usage.py`\n-   **`APIUsageRecord(BaseModel)`:** `id: UUID`, `api_client_id: UUID`, `user_id: UUID`, `timestamp: datetime`, `endpoint: str`, `cost: Optional[Decimal] = None`, `is_successful: bool`.\n-   **`QuotaPeriod(str, Enum)`:** `DAILY = \"daily\"`, `MONTHLY = \"monthly\"`.\n-   **`Quota(BaseModel)`:** `id: UUID`, `api_client_id: UUID`, `user_id: UUID`, `limit_amount: int`, `period: QuotaPeriod`, `last_reset_at: datetime`.\n\n### 3.6. `domain/repositories/` - Repository Interfaces\n-   Define abstract methods for CRUD operations and specific queries for each domain aggregate/entity, using domain model types in signatures.\n\n### 3.7. `infrastructure/` - Infrastructure Layer\n\n#### `database/session.py`\n-   As per file structure: `AsyncEngine`, `async_sessionmaker`, `get_async_db_session` generator.\n\n#### `database/models/`\n-   SQLAlchemy ORM models (`APIKeyModel`, `WebhookModel`, `UsageRecordModel`, `QuotaModel`) mirroring domain models and database table structures defined in the \"Database Design\" input. Ensure appropriate `ForeignKey` constraints and indexing.\n\n#### `database/repositories/`\n-   Implementations of repository interfaces using SQLAlchemy `AsyncSession` and ORM models.\n-   **`SqlAlchemyApiKeyRepository`**:\n    -   `get_by_key_prefix`: Query `APIKeyModel` where `key_prefix` matches.\n-   **`SqlAlchemyWebhookRepository`**:\n    -   `list_by_user_id_and_event_type`: Query `WebhookModel` where `user_id` matches and `event_types` array contains the given event.\n-   **`SqlAlchemyUsageRepository`**:\n    -   `get_summary_for_client`: Query `UsageRecordModel`, aggregate data.\n-   **`SqlAlchemyQuotaRepository`**:\n    -   `get_current_usage_for_quota_period`: This might be complex. It would query `UsageRecordModel` table to count relevant actions since `quota.last_reset_at`.\n\n#### `database/migrations/env.py`\n-   Standard Alembic setup, ensuring `target_metadata` points to `infrastructure.database.models.base.Base.metadata`.\n\n#### `messaging/rabbitmq_client.py`\n-   **`class RabbitMQClient`:**\n    -   `connect()`: `aio_pika.connect_robust(...)`.\n    -   `get_channel()`: `await self.connection.channel()`.\n    -   `close()`: `await self.connection.close()`.\n\n#### `messaging/webhook_publisher.py`\n-   **`class WebhookPublisher(IWebhookPublisher)`:** (*Define IWebhookPublisher interface first*)\n    -   `__init__(rabbitmq_client: RabbitMQClient, exchange_name: str)`\n    -   `publish_webhook_event(webhook: WebhookDomainModel, event_type: str, payload: dict)`:\n        -   `channel = await self.rabbitmq_client.get_channel()`.\n        -   `exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True)`.\n        -   Prepare message body (JSON string): `{\"target_url\": webhook.target_url, \"payload\": payload, \"secret\": webhook.secret_for_signing, \"event_type\": event_type}`. *Correction: The publisher should send details so a separate worker can do the HTTP POST and signing. The WebhookDomainModel likely won't have the plain secret. The service layer retrieving the webhook could pass the plain secret if it's temporarily decrypted/retrieved for this purpose, or the signature is generated here by the service and passed in the message.* Let's assume the service layer handles the secret part and passes the raw payload and signature instructions.\n        -   Message structure for worker: `{\"webhook_id\": webhook.id, \"target_url\": webhook.target_url, \"raw_payload\": json.dumps(payload), \"event_type\": event_type, \"signature_secret_ref\": webhook.id}` (worker retrieves secret from Vault using webhook.id as ref).\n        -   `routing_key = f\"{settings.RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX}.{event_type}.{webhook.user_id}\"`.\n        -   `await exchange.publish(aio_pika.Message(body=message_body.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT), routing_key=routing_key)`.\n\n#### `security/hashing.py`\n-   Use `passlib.context.CryptContext` with `bcrypt` or `argon2`.\n    -   `pwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")`\n    -   `hash_secret(secret: str) -> str: return pwd_context.hash(secret)`\n    -   `verify_secret(plain_secret: str, hashed_secret: str) -> bool: return pwd_context.verify(plain_secret, hashed_secret)`\n\n#### `external_clients/`\n-   **Base Client (Conceptual):**\n    -   `__init__(base_url: str, timeout: int = 5)`: `self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)`\n    -   `async def _request(method, endpoint, headers=None, json=None, data=None, params=None) -> httpx.Response:`\n        -   Implement retry logic (e.g., using `tenacity` library) for transient errors (5xx, network errors).\n        -   Implement circuit breaker (e.g., using `pybreaker` or custom logic with Redis).\n        -   Make request: `await self.client.request(...)`.\n        -   Handle HTTP errors (4xx, 5xx) and raise `ExternalServiceError`.\n    -   `async def close_client(): await self.client.aclose()`\n-   **`AIGenerationClient`**: Methods map to AI Gen Orch Service endpoints.\n-   **`AssetManagementClient`**: Methods map to Asset Mgmt Service endpoints.\n-   **`UserTeamClient`**: Methods map to User/Team Mgmt Service endpoints.\n\n## 4. Data Design\nThe database design for this service will primarily involve the following tables, as described in the \"Database Design\" input and relevant to this service's scope:\n-   `APIClient` (renamed to `api_keys` in ORM model `APIKeyModel` for clarity)\n-   `Webhook` (ORM model `WebhookModel`)\n-   `APIUsageRecord` (ORM model `UsageRecordModel`)\n-   `Quota` (ORM model `QuotaModel`)\n\nRelationships:\n-   `APIKeyModel` has a `user_id` (foreign key to a conceptual `users` table, managed by User Management service).\n-   `WebhookModel` has a `user_id`.\n-   `UsageRecordModel` has `api_client_db_id` (FK to `api_keys.id`) and `user_id`.\n-   `QuotaModel` has `api_client_db_id` (FK to `api_keys.id`) and `user_id`.\n\nData types and constraints will follow the Pydantic domain models and SQLAlchemy ORM definitions.\n\n## 5. API Design\nThe public-facing API for developers will be defined in `api/openapi.yaml` following OpenAPI 3.x specification.\nKey endpoint groups:\n-   `/api-keys`: CRUD operations for API keys.\n-   `/webhooks`: CRUD operations for webhooks.\n-   `/usage`: Endpoints for querying API usage and quota status.\n-   `/proxy/v1/*`: Endpoints for proxying requests to internal services:\n    -   `/proxy/v1/generations`: Initiate, get status.\n    -   `/proxy/v1/assets`: Retrieve details, manage.\n    -   `/proxy/v1/users`, `/proxy/v1/teams`: Manage user/team resources (scoped).\n\nAuthentication:\n-   Management endpoints (`/api-keys`, `/webhooks` when managed by a user for themselves) would typically be authenticated via user session JWT from the main web application or a dedicated developer portal session.\n-   Proxied API endpoints (`/proxy/v1/*`) and usage queries (`/usage`) are authenticated via `X-API-KEY` header.\n\n## 6. Security Considerations (REQ-018, SEC-001, SEC-005)\n-   **API Key Security:**\n    -   Secrets are hashed using bcrypt/Argon2.\n    -   Plaintext secret displayed only once upon creation.\n    -   Keys can be revoked.\n    -   Permissions/scopes to limit key capabilities.\n-   **Webhook Security:**\n    -   Optional shared secret for HMAC-SHA256 signature verification of webhook payloads. The service generating the event to be sent via webhook (e.g., Generation Orchestration service after a generation completes) will be responsible for using the webhook's secret to sign the payload *before* it's put on the RabbitMQ queue for the `WebhookPublisher` in *this* service to then send out. *Correction:* The `WebhookPublisher` in this service should be responsible for retrieving the secret (e.g. from Vault, or if stored encrypted in DB with WebhookModel) and generating the signature before dispatching the HTTP POST request to the `target_url`. The RabbitMQ message to the worker/publisher should contain enough info to retrieve the secret.\n-   **Input Validation:** Pydantic schemas enforce strict input validation for all API requests.\n-   **Output Encoding:** FastAPI handles JSON response encoding, mitigating common XSS vectors for API consumers.\n-   **Rate Limiting & Quotas:** Implemented to prevent abuse and manage resource consumption.\n-   **Authentication:** All sensitive endpoints require authentication.\n-   **Authorization:** Permissions check for API key operations and proxied requests.\n-   **Dependencies:** Secure communication (HTTPS) with external and internal services.\n-   **Secret Management:** Application secrets (DB URL, RabbitMQ URL, HMAC keys) managed via `core.config` (environment variables) and not hardcoded. For production, these should be injected by a secure deployment system (e.g., K8s secrets, HashiCorp Vault).\n\n## 7. Deployment Considerations\n-   The service will be containerized using Docker.\n-   `requirements.txt` and `pyproject.toml` define dependencies.\n-   Database migrations managed by Alembic, integrated into CI/CD.\n-   Environment variables for configuration.\n-   Deployed as part of the microservices architecture, likely behind an API Gateway/Load Balancer for external traffic.\n\n## 8. Error Handling and Logging\n-   Custom exceptions defined in `core.exceptions` are handled by global FastAPI exception handlers to return standardized JSON error responses.\n-   Structured JSON logging configured via `core.logging_config`, including correlation IDs where possible (e.g., passed via headers or generated per request).\n-   Detailed error information logged for debugging, while user-facing messages are kept generic and informative.\n-   Errors from external service calls are caught and wrapped in `ExternalServiceError` or more specific custom exceptions.\n\n## 9. Testing Strategy (as per QA-001)\n-   **Unit Tests (PyTest):**\n    -   Domain model logic.\n    -   Application service business logic (with mocked repositories/clients).\n    -   Utility functions (hashing, config loading).\n-   **Integration Tests (PyTest with `httpx.AsyncClient` for FastAPI's `TestClient`, and actual DB/RabbitMQ instances in test environment):**\n    -   API endpoint request/response validation and behavior.\n    -   Service interactions with real database repositories.\n    -   Webhook publishing to RabbitMQ and verification of message content/routing.\n    -   Interaction with mocked external service clients.\n-   **Contract Tests (Pact or similar):** For interactions with AI Generation Service, Asset Management Service, User/Team Service to ensure API compatibility. (This would be part of their respective test suites and this service's client tests).\n\nThis SDS provides a comprehensive blueprint for developing the `CreativeFlow.DeveloperPlatformService`. It details the structure, functionality, and interactions necessary to fulfill its requirements within the CreativeFlow AI ecosystem.\n"
}
