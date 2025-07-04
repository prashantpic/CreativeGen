# Software Design Specification (SDS) for CreativeFlow.Service.ApiPlatform

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.Service.ApiPlatform`. This service is a core backend component of the CreativeFlow AI platform, acting as the primary public-facing API for third-party developers and external integrations. It is responsible for secure access control, usage management, and routing requests to internal services.

### 1.2. Scope
The scope of this service includes:
-   Exposing a versioned, RESTful API for creative generation, asset management, and other platform features.
-   Implementing robust, secure API key-based authentication and authorization.
-   Enforcing rate limiting and usage quotas based on developer subscription plans.
-   Tracking API usage for billing and analytics purposes.
-   Managing and dispatching webhook notifications for asynchronous events.
-   Acting as a secure gateway that communicates with internal backend services like the AI Generation Orchestrator and the Odoo Business Service.

### 1.3. Technology Stack
-   **Language:** Python 3.11+
-   **Framework:** FastAPI
-   **Database ORM:** SQLAlchemy (asyncio)
-   **Database Migration:** Alembic
-   **Data Validation:** Pydantic
-   **Messaging:** Pika for RabbitMQ integration
-   **Security:** `passlib[bcrypt]` for hashing, `python-jose` for JWT utilities if needed for internal tokens.
-   **HTTP Client:** `httpx` for asynchronous service-to-service communication.

## 2. System Architecture & Design

The `ApiPlatform` service is a microservice within a larger distributed system. It follows the **API Gateway** pattern for external clients.

### 2.1. Key Architectural Principles
-   **Asynchronous First:** The service will be built using Python's `asyncio` and FastAPI's async capabilities to handle high concurrency.
-   **Statelessness:** The service itself will be stateless, with all state managed in the PostgreSQL database or external services. This facilitates horizontal scaling.
-   **Loose Coupling:** Communication with other services (AI Orchestrator, Odoo) is done via well-defined REST APIs or asynchronously via a message broker (RabbitMQ), ensuring services can evolve independently.
-   **Security by Design:** Security is a primary concern, addressed through secure API key handling, strict input validation, and middleware for authentication and authorization.

### 2.2. Core Data Flows

#### 2.2.1. Authenticated API Request Flow
1.  A third-party developer's application sends an HTTP request to an API endpoint (e.g., `/api/v1/generations`). The request includes an `Authorization` header with the API Key.
2.  FastAPI, via a dependency, extracts the API Key.
3.  The `api_key_service` authenticates the key against the database.
4.  The `quota_service` checks rate limits and usage quotas by communicating with the `Odoo Business Service`.
5.  If authentication and quota checks pass, the request is forwarded to the appropriate internal service client (e.g., `aigen_orchestration_client`).
6.  The internal service processes the request.
7.  A response (e.g., a job ID for an async task) is returned to the `ApiPlatform` service.
8.  The `ApiPlatform` service formats the final response and sends it back to the developer client.

#### 2.2.2. Asynchronous Webhook Notification Flow
1.  An internal service (e.g., AI Orchestrator) completes an asynchronous task initiated by an API user (e.g., `generation.completed`).
2.  The internal service publishes an event message to a RabbitMQ exchange.
3.  The `ApiPlatform`'s webhook management logic (or a dedicated consumer service) listens for these events.
4.  Upon receiving a relevant event, the service retrieves the webhook registrations for the corresponding API client from the database.
5.  For each registered webhook, it constructs a payload, signs it with the webhook's secret, and publishes it to a `webhook_dispatch` queue in RabbitMQ.
6.  A separate pool of workers (potentially within this service or another) consumes from this queue and makes the final HTTP POST request to the developer's registered URL, handling retries on failure.

## 3. Detailed Component Specification

This section details the implementation for each file defined in the repository structure.

### 3.1. Project Configuration

#### 3.1.1. `pyproject.toml`
-   **Purpose:** Manages project dependencies and metadata.
-   **Specification:**
    -   Use `poetry` for dependency management.
    -   Dependencies must include: `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `alembic`, `psycopg2-binary`, `pika`, `pydantic`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `httpx`.
    -   Dev dependencies must include: `pytest`, `pytest-asyncio`, `httpx`.

#### 3.1.2. `alembic.ini`
-   **Purpose:** Configures the Alembic database migration tool.
-   **Specification:**
    -   `sqlalchemy.url` must be configured to load from the `DATABASE_URL` environment variable defined in `core.config`.
    -   `script_location` must point to `src/creativeflow/service/alembic`.

### 3.2. Core Application (`src/creativeflow/service/`)

#### 3.2.1. `main.py`
-   **Purpose:** Application entry point and global configuration.
-   **Specification:**
    -   Initialize a `FastAPI` app instance.
    -   **Middleware:**
        -   Add `CORSMiddleware` to enforce a strict CORS policy as per `SEC-005`. Origins, methods, and headers should be configurable via `core.config`.
        -   Add a global middleware to handle adding a request/correlation ID to all incoming requests for distributed tracing.
    -   **Routers:** Include the main API router from `api.v1.api_router`.
    -   **Event Handlers:**
        -   `@app.on_event("startup")`: Implement an `async` function to initialize resources, e.g., create a RabbitMQ connection pool/producer instance.
        -   `@app.on_event("shutdown")`: Implement an `async` function to gracefully close connections (e.g., RabbitMQ).
    -   **Exception Handling:** Implement a global exception handler to catch unhandled exceptions and return a standardized JSON error response (e.g., `{"detail": "Internal Server Error", "correlation_id": "..."}`).

#### 3.2.2. `core/config.py`
-   **Purpose:** Centralized, type-safe configuration management.
-   **Specification:**
    -   Define a `Settings` class inheriting from `pydantic_settings.BaseSettings`.
    -   Define fields for all required environment variables with type hints:
        -   `PROJECT_NAME: str = "CreativeFlow API Platform"`
        -   `API_V1_STR: str = "/api/v1"`
        -   `DATABASE_URL: PostgresDsn`
        -   `RABBITMQ_URL: str`
        -   `WEBHOOK_EXCHANGE_NAME: str = "webhook_events"`
        -   `AIGEN_ORCH_SERVICE_URL: HttpUrl`
        -   `ODOO_BUSINESS_SERVICE_URL: HttpUrl`
        -   `SECRET_KEY: str` (for internal token signing, if any)
    -   Instantiate a single `settings` object for use throughout the application.

#### 3.2.3. `core/security.py`
-   **Purpose:** Centralize security and cryptographic functions.
-   **Specification:**
    -   Define a `CryptContext` instance: `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`.
    -   `generate_api_key_and_secret() -> tuple[str, str]`: Generates a public `api_key` (e.g., `cf_` + 32 random URL-safe chars) and a `secret` (e.g., 48 random URL-safe chars) using the `secrets` module.
    -   `hash_api_secret(secret: str) -> str`: Uses `pwd_context.hash()` to hash the plain text secret.
    -   `verify_api_secret(plain_secret: str, hashed_secret: str) -> bool`: Uses `pwd_context.verify()` to check a secret against its hash.

### 3.3. Database Layer (`src/creativeflow/service/db/`)

#### 3.3.1. `db/session.py`
-   **Purpose:** Manage database connections and sessions.
-   **Specification:**
    -   Import `create_async_engine` and `async_sessionmaker` from `sqlalchemy.ext.asyncio`.
    -   Create `async_engine` using `settings.DATABASE_URL`.
    -   Create `AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)`.
    -   `get_db_session() -> AsyncGenerator[AsyncSession, None]`: An `async` generator dependency that `yield`s a session from `AsyncSessionLocal` and closes it in a `finally` block.

#### 3.3.2. `db/models/`
-   **Purpose:** Define SQLAlchemy ORM models. All models should inherit from a common `Base` class.
-   **`api_client.py`:**
    -   **Class `APIClient`**:
        -   `id`: `UUID(as_uuid=True)`, primary key, default `uuid.uuid4`.
        -   `user_id`: `UUID(as_uuid=True)`, `ForeignKey("user.id")`, indexed. (Note: `user` table is in another service's domain, so this is just a logical reference).
        -   `name`: `String(100)`.
        -   `api_key`: `String(100)`, unique, indexed.
        -   `secret_hash`: `String(255)`.
        -   `permissions`: `JSONB`, nullable.
        -   `is_active`: `Boolean`, default `True`.
        -   `created_at`, `updated_at`: `DateTime` with server defaults.
-   **`webhook.py`:**
    -   **Class `Webhook`**:
        -   `id`: `UUID(as_uuid=True)`, primary key, default `uuid.uuid4`.
        -   `api_client_id`: `UUID(as_uuid=True)`, `ForeignKey("api_client.id")`, indexed.
        -   `target_url`: `String(2048)`.
        -   `event_type`: `String(100)`, indexed. (e.g., 'generation.completed', 'generation.failed').
        -   `secret_hash`: `String(255)`, nullable. (For signing payloads).
        -   `is_active`: `Boolean`, default `True`.

#### 3.3.3. `db/repository/api_client_repository.py`
-   **Purpose:** Encapsulate database access logic for `APIClient`.
-   **Specification:**
    -   **Class `APIClientRepository`**:
        -   `async def get_by_api_key(self, db: AsyncSession, *, api_key: str) -> APIClient | None`: Queries for an `APIClient` by its `api_key`.
        -   `async def create(self, db: AsyncSession, *, obj_in: APIClientCreateSchema, user_id: UUID) -> APIClient`: Creates and commits a new `APIClient`.
        -   `async def revoke(self, db: AsyncSession, *, db_obj: APIClient) -> APIClient`: Sets `is_active` to `False` on a given `APIClient` instance and commits.

### 3.4. API Layer (`src/creativeflow/service/api/`)

#### 3.4.1. `api/v1/dependencies.py`
-   **Purpose:** Define reusable FastAPI dependencies.
-   **Specification:**
    -   Define `api_key_scheme = APIKeyHeader(name="Authorization")`.
    -   `async def get_current_api_client(api_key: str = Security(api_key_scheme), db: AsyncSession = Depends(get_db_session)) -> APIClient`:
        1.  Checks if `api_key` is provided. If not, raise `HTTPException(status_code=401, detail="API Key required")`.
        2.  Use `api_client_repository.get_by_api_key` to fetch the client.
        3.  If no client is found or `client.is_active` is `False`, raise `HTTPException(status_code=403, detail="Invalid or inactive API Key")`.
        4.  Return the `APIClient` object.
    -   `async def verify_usage_quota(api_client: APIClient = Depends(get_current_api_client), quota_service: QuotaService = Depends())`:
        1.  Calls `quota_service.check_and_log_usage(api_client=api_client, ...)`.
        2.  The `quota_service` will raise exceptions on failure, which will be propagated.
        3.  Returns the `api_client` if successful.

#### 3.4.2. `api/v1/endpoints/`
-   **Purpose:** Expose RESTful endpoints for different resources.
-   **`api_keys.py`:**
    -   Create `router = APIRouter()`.
    -   `POST /`: Depends on an authenticated *user* (e.g., via a JWT from the main web app's login). Creates a new API key for that user using the `api_key_service`. Returns the new key and secret *once*.
    -   `GET /`: Depends on an authenticated user. Lists all active API keys for that user (without the secret).
    -   `DELETE /{key_id}`: Depends on an authenticated user. Revokes an API key belonging to that user.
-   **`generations.py`:**
    -   Create `router = APIRouter()`.
    -   `POST /`: Depends on `get_current_api_client` and `verify_usage_quota`.
        1.  Accepts a `GenerationRequestSchema`.
        2.  Calls the `aigen_orchestration_client.initiate_generation`, passing the request data.
        3.  Returns a `GenerationResponseSchema` with the `job_id`.
    -   `GET /{job_id}`: Depends on `get_current_api_client`.
        1.  Calls `aigen_orchestration_client.get_generation_status`.
        2.  Returns the status.

### 3.5. Service Layer (`src/creativeflow/service/service/`)

#### 3.5.1. `api_key_service.py`
-   **Purpose:** Business logic for API key lifecycle.
-   **Specification:**
    -   **Class `APIKeyService`**:
        -   `async def create_new_api_key(...)`: Coordinates `security.generate_api_key_and_secret`, `security.hash_api_secret`, and `api_client_repository.create`.
        -   `async def revoke_api_key(...)`: Fetches the key, verifies ownership, and calls `api_client_repository.revoke`.

#### 3.5.2. `quota_service.py`
-   **Purpose:** Enforce usage quotas and rate limits.
-   **Specification:**
    -   **Class `QuotaService`**:
        -   Requires integration clients for Redis (for rate limiting) and the Odoo service.
        -   `async def check_and_log_usage(...)`:
            1.  Implement a rate-limiting check (e.g., token bucket algorithm using Redis). If exceeded, raise `HTTPException(429)`.
            2.  Call the `OdooBusinessClient` to check the user's current credit/quota balance. If insufficient, raise `HTTPException(402, detail="Insufficient credits or quota")`.
            3.  If all checks pass, call the `OdooBusinessClient` again to log the usage/deduct credit.

### 3.6. Messaging Layer (`src/creativeflow/service/messaging/`)

#### 3.6.1. `producer.py`
-   **Purpose:** Publish messages to RabbitMQ for webhook dispatch.
-   **Specification:**
    -   **Class `WebhookEventProducer`**:
        -   `__init__`: Takes `RABBITMQ_URL`.
        -   `async def connect()`: Establishes a connection and channel. Declares the `webhook_events` exchange (type: topic).
        -   `async def publish_event(self, event_type: str, payload: dict)`:
            1.  Serializes payload to JSON.
            2.  Publishes the message to the `webhook_events` exchange with the `event_type` as the routing key.
            3.  Use publisher confirms for delivery guarantee.

### 3.7. Integrations (`src/creativeflow/service/integrations/`)

#### 3.7.1. `aigen_orchestration_client.py`
-   **Purpose:** Client to communicate with the AI Generation Orchestration Service.
-   **Specification:**
    -   **Class `AIGenOrchClient`**:
        -   Use `httpx.AsyncClient` for requests.
        -   `async def initiate_generation(...)`: Sends a `POST` request to the service's endpoint. Implements a retry policy (e.g., 3 retries with exponential backoff) for transient network errors or 5xx responses.
        -   `async def get_generation_status(...)`: Sends a `GET` request.

#### 3.7.2. `odoo_business_client.py` (New File)
-   **Purpose:** Client to communicate with the Odoo Business Service.
-   **Specification:**
    -   **Class `OdooBusinessClient`**:
        -   Use `httpx.AsyncClient`.
        -   `async def check_user_quota(self, user_id: UUID) -> dict`: Sends a request to the Odoo service to get quota/credit info for a given user.
        -   `async def log_api_usage(self, user_id: UUID, usage_details: dict)`: Sends a request to log usage and deduct credits.

## 4. Database Migrations

-   **Tool:** Alembic
-   **Directory:** `src/creativeflow/service/alembic/versions/`
-   **Process:**
    1.  Modify SQLAlchemy models in `src/creativeflow/service/db/models/`.
    2.  Run `alembic revision --autogenerate -m "Description of change"` to create a new migration script.
    3.  Review and manually adjust the generated script if necessary.
    4.  Run `alembic upgrade head` to apply migrations, which will be part of the deployment pipeline.