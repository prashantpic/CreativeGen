# Software Design Specification: CreativeFlow.CollaborationService

## 1. Introduction

### 1.1 Purpose
This document details the design for the `CreativeFlow.CollaborationService`, a microservice responsible for enabling real-time collaborative editing of creative projects within the CreativeFlow AI platform. It manages WebSocket connections, synchronizes document changes using Conflict-free Replicated Data Types (CRDTs), handles presence information, and supports merging of offline edits for collaborative projects.

### 1.2 Scope
The scope of this document covers the design of the `CreativeFlow.CollaborationService`, including:
*   WebSocket API for client communication.
*   Core collaboration logic using Yjs (via `y-py`).
*   Integration with Redis for session state and presence management.
*   Interaction with the Authentication & Authorization Service for user token validation.
*   Domain models, application services, and infrastructure components.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **SDS**: Software Design Specification
*   **API**: Application Programming Interface
*   **CRDT**: Conflict-free Replicated Data Type
*   **Yjs**: A CRDT framework for building collaborative applications.
*   **`y-py`**: Python bindings for Yjs.
*   **WebSocket**: A communication protocol providing full-duplex communication channels over a single TCP connection.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pydantic**: Data validation and settings management using Python type annotations.
*   **Redis**: In-memory data structure store, used as a database, cache, and message broker.
*   **DTO**: Data Transfer Object
*   **VO**: Value Object
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **REQ-XXX**: Requirement ID from the Software Requirements Specification (SRS).
*   **UAPM-XXX**: User Account & Profile Management requirement ID.

### 1.4 References
*   CreativeFlow AI Software Requirements Specification (SRS)
    *   REQ-013: Real-time collaborative editing
    *   REQ-019.1: Offline Data Synchronization and Conflict Resolution (Collaborative project conflict resolution part)
    *   Section 2.2: Product Functions (Real-time collaborative editing function)
    *   Section 5.3.2: System Architecture (Collaboration Flow implementation)
*   CreativeFlow AI Architecture Design Document
*   CreativeFlow AI Sequence Diagrams (especially SD-CF-001 for context, though not directly implementing user registration)
*   Repository Definition: `REPO-COLLABORATION-SERVICE-001`
*   Technology Stack: Python 3.11+, FastAPI, `websockets` (FastAPI's underlying library), `y-py`, `redis` (async client).

## 2. System Overview
The `CreativeFlow.CollaborationService` is a backend microservice designed to facilitate real-time multi-user collaboration on creative documents. It establishes persistent WebSocket connections with clients (web and mobile frontends). When a user joins a collaborative session for a specific document, the service manages their connection and presence.

Document changes made by one user are sent to the service, processed using Yjs CRDTs to ensure consistency, and then broadcasted to all other connected participants in the same session. The service utilizes Redis to store active session information, participant presence, and potentially snapshots of Yjs document states for quick loading or recovery. Authentication for WebSocket connections is handled by validating tokens against the `CreativeFlow.AuthService`.

The service is designed to be scalable and resilient, with considerations for handling concurrent connections and efficiently managing CRDT operations. It also plays a role in merging offline edits for collaborative projects when users reconnect.

## 3. Functional Requirements

The Collaboration Service will implement the following functionalities based on the SRS:

*   **REQ-013: Real-time collaborative editing**
    *   **FR-CS-001**: The service shall accept WebSocket connections from authenticated clients for specific document IDs.
    *   **FR-CS-002**: The service shall manage participant lists for each active collaboration session.
    *   **FR-CS-003**: The service shall receive document change updates (Yjs updates) from connected clients.
    *   **FR-CS-004**: The service shall apply received Yjs updates to the server-side representation of the shared document state.
    *   **FR-CS-005**: The service shall broadcast Yjs updates (or diffs) to all other connected clients in the same session, excluding the originator of the update.
    *   **FR-CS-006**: The service shall maintain and broadcast user presence information (e.g., who is currently in the session, cursor positions if supported by client messages).
    *   **FR-CS-007**: Upon a new user joining a session, the service shall provide them with the current state of the shared document.
*   **REQ-019.1: Offline Data Synchronization and Conflict Resolution (Collaborative project conflict resolution part)**
    *   **FR-CS-008**: The service shall accept a batch of offline changes (Yjs updates) from a reconnecting client for a collaborative project.
    *   **FR-CS-009**: The service shall merge these offline changes into the current server-side document state using Yjs CRDT mechanisms.
    *   **FR-CS-010**: If Yjs automatic merging results in a resolvable state, the service shall update the server-side document and broadcast the merged changes to all connected clients.
    *   **FR-CS-011**: (Future consideration, if Yjs auto-merge is insufficient) The service shall flag complex conflicts that cannot be automatically resolved by Yjs and notify involved users, potentially versioning conflicting changes. (Initial scope relies on Yjs's strong merging capabilities).
*   **Section 5.3.2: Collaboration Flow**
    *   **FR-CS-012**: The service shall authenticate WebSocket connections by validating a token (passed during handshake) with the `CreativeFlow.AuthService`.
    *   **FR-CS-013**: The service shall store and retrieve active collaboration session information (e.g., document ID, participant list, Yjs document state) using Redis.

## 4. Non-Functional Requirements

*   **NFR-CS-001 (Performance - Latency)**: Document update propagation (from server receiving an update to other clients receiving it) should ideally be under 200ms (P95) over a stable connection, excluding network latency between client and server. (Derived from REQ-5-001's 2-second end-to-end requirement, this service must be significantly faster).
*   **NFR-CS-002 (Scalability)**: The service should be designed to handle a significant number of concurrent WebSocket connections and collaborative sessions. (Specific numbers to be derived from overall system NFRs like NFR-002). Horizontal scaling of service instances should be possible.
*   **NFR-CS-003 (Reliability)**: The service should be resilient to individual instance failures. If scaled, disconnections should be handled gracefully, and users should be able to reconnect to other instances. Redis HA (Sentinel/Cluster) is crucial.
*   **NFR-CS-004 (Security)**: WebSocket connections must be secure (WSS). User authentication must be enforced before allowing participation in a session. Input validation for messages is required.
*   **NFR-CS-005 (Maintainability)**: Code should be modular, well-documented, and testable. Adherence to Python/FastAPI best practices.
*   **NFR-CS-006 (Data Consistency)**: CRDTs (Yjs) are key to ensuring eventual consistency of the shared document across all participants.

## 5. System Architecture

### 5.1 Architectural Style
The Collaboration Service is a microservice within the larger CreativeFlow AI platform, which follows a Microservices architecture. Internally, it will adopt a layered architecture (API, Application, Domain, Infrastructure).

### 5.2 Key Components
*   **WebSocket Connection Manager**: Handles WebSocket lifecycles, tracks active connections per session.
*   **Message Handler**: Parses incoming WebSocket messages, validates them, and routes them to appropriate application services.
*   **Authentication Middleware/Dependency**: Verifies user identity for WebSocket connections.
*   **Collaboration Application Service**: Orchestrates use cases (join, leave, update document, update presence).
*   **Domain Model**:
    *   `CollaborationSession` Aggregate: Manages participants and document state for a session.
    *   `SharedDocument` Aggregate: Encapsulates the Yjs document and its operations.
    *   `Presence` Entity: Represents user presence.
*   **CRDT Service (Domain Service)**: Wraps `y-py` library for Yjs operations.
*   **Conflict Resolution Service (Domain Service)**: Handles merging offline edits (REQ-019.1).
*   **Repositories (Infrastructure)**: Implementations for storing/retrieving session and presence data from Redis.
*   **WebSocket Broadcaster (Infrastructure)**: Sends messages to connected clients in a session.
*   **Auth Service Client (Infrastructure)**: Communicates with the `CreativeFlow.AuthService`.
*   **Redis Client (Infrastructure)**: Manages connections to Redis.

### 5.3 Technology Stack
*   **Language**: Python 3.11+
*   **Framework**: FastAPI (with `websockets` library for WebSocket handling)
*   **CRDT Library**: `y-py` (Python bindings for Yjs)
*   **Caching/State Store**: Redis (using `redis.asyncio` client)
*   **Data Validation/Serialization**: Pydantic
*   **Configuration**: Pydantic `BaseSettings`
*   **ASGI Server**: Uvicorn

### 5.4 Interfaces
*   **Primary Interface**: WebSocket API
    *   Endpoint: `/ws/document/{document_id}?token={jwt_token}`
    *   Purpose: Real-time bi-directional communication for collaboration.
*   **Internal Interfaces**:
    *   HTTP client calls to `CreativeFlow.AuthService` (for token validation).
    *   Redis client communication for session and presence data.
    *   (Potentially) Redis Pub/Sub for scaling WebSocket broadcasts across multiple service instances.

## 6. Detailed Design

This section details the design for each file specified in the repository structure.

---

**File: `src/creativeflow/collaboration/__init__.py`**
*   **Purpose**: Makes the `collaboration` directory a Python package.
*   **Contents**:
    python
    # This file can be empty or used for package-level imports if needed.
    # For example:
    # from .main import app
    
*   **Logic Description**: Initializes the `creativeflow.collaboration` package.

---

**File: `src/creativeflow/collaboration/main.py`**
*   **Purpose**: Main FastAPI application setup, entry point for the service.
*   **Key Classes/Modules**:
    *   `app: FastAPI`: The main FastAPI application instance.
*   **Methods/Functions**:
    *   `create_application() -> FastAPI`:
        *   **Logic**: Creates and configures the FastAPI application instance.
            *   Instantiates `FastAPI()`.
            *   Includes the WebSocket router from `api.websocket_router`.
            *   Registers `startup_event` and `shutdown_event` handlers.
            *   Optionally adds global exception handlers or middleware (e.g., for logging requests if needed beyond ASGI server logs, basic CORS if this service ever exposes HTTP endpoints directly).
        *   **Returns**: Configured FastAPI application instance.
    *   `startup_event()`:
        *   **Signature**: `async def startup_event():`
        *   **Logic**:
            *   Loads configuration using `core.config.settings`.
            *   Initializes the Redis connection pool using `infrastructure.redis.connection.init_redis_pool(settings.REDIS_URL)`.
            *   Initializes any other global resources or clients (e.g., `AuthServiceClient` instance if managed globally).
            *   Logs a message indicating successful startup.
        *   **Error Handling**: Logs errors if Redis connection fails.
    *   `shutdown_event()`:
        *   **Signature**: `async def shutdown_event():`
        *   **Logic**:
            *   Closes the Redis connection pool using `infrastructure.redis.connection.close_redis_pool()`.
            *   Cleans up any other global resources.
            *   Logs a message indicating graceful shutdown.
*   **Entry Point Logic**:
    python
    # At the bottom of the file, if run directly (though uvicorn will usually import 'app')
    # if __name__ == "__main__":
    #     import uvicorn
    #     from creativeflow.collaboration.core.config import settings
    #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG_MODE) 
    # (Actual uvicorn run command will be in Dockerfile or deployment scripts)

    app = create_application() 
    
*   **Documentation**: "Entry point for the Collaboration Service. Initializes and configures the FastAPI application, including WebSocket routing and lifecycle event handlers."

---

**File: `src/creativeflow/collaboration/core/__init__.py`**
*   **Purpose**: Initializes the `core` sub-package.
*   **Contents**: Empty or package-level imports.

---

**File: `src/creativeflow/collaboration/core/config.py`**
*   **Purpose**: Handles application configuration.
*   **Key Classes/Modules**:
    *   `Settings(BaseSettings)` from Pydantic:
        *   **Attributes**:
            *   `REDIS_URL: str = "redis://localhost:6379/0"`
            *   `REDIS_PASSWORD: Optional[str] = None`
            *   `AUTH_SERVICE_URL: str = "http://auth-service:8000/api/v1/auth"` (Example URL)
            *   `JWT_SECRET_KEY: str` (For decoding, though validation primarily by Auth Service. If this service needs to *sign* anything, it would need its own secret, but it likely only *validates* tokens via Auth Service.)
            *   `LOG_LEVEL: str = "INFO"`
            *   `YJS_GC_ENABLED: bool = True` (Yjs garbage collection setting)
            *   `YJS_DOC_TTL_SECONDS: int = 3600` (Time-to-live for Yjs docs in Redis if not active)
            *   `MAX_WEBSOCKET_MESSAGE_SIZE: int = 4 * 1024 * 1024` (e.g., 4MB)
            *   `WEBSOCKET_SESSION_TIMEOUT_SECONDS: int = 60 * 60` (e.g., 1 hour idle timeout)
            *   `DEBUG_MODE: bool = False`
        *   **Pydantic Config**: `model_config = SettingsConfigDict(env_file=".env", extra="ignore")`
*   **Global Instance**:
    python
    settings = Settings()
    
*   **Logic Description**: Uses Pydantic `BaseSettings` to load configuration from environment variables, with defaults. The `.env` file is used for local development.
*   **Security**: `JWT_SECRET_KEY` if used directly by this service, and `REDIS_PASSWORD` should be loaded securely from environment variables, ideally injected by a secrets manager in production.
*   **Documentation**: "Manages all application-level configurations. Loads settings from environment variables (e.g., `.env` file for local development) using Pydantic."

---

**File: `src/creativeflow/collaboration/core/dependencies.py`**
*   **Purpose**: Defines reusable FastAPI dependencies.
*   **Key Classes/Modules**:
    *   `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")` (Dummy `tokenUrl` as actual token generation is by Auth Service. This is mainly for FastAPI to extract the token from the header/query param during HTTP upgrade for WebSockets if needed, or from query params directly for WebSocket connection).
*   **Methods/Functions**:
    *   `get_collaboration_app_service(redis_client: Redis = Depends(get_redis_client), auth_service_client: AuthServiceClient = Depends(get_auth_service_client)) -> CollaborationAppService`:
        *   **Signature**: `async def get_collaboration_app_service(...) -> CollaborationAppService:`
        *   **Logic**:
            *   Instantiates `RedisCollaborationSessionRepositoryImpl` and `RedisPresenceRepositoryImpl` with `redis_client`.
            *   Instantiates `CRDTService` and `ConflictResolutionService`.
            *   Instantiates `ConnectionManager` (singleton or request-scoped as appropriate).
            *   Instantiates `WebsocketBroadcaster` with the `ConnectionManager` (and potentially `RedisPubSubManager`).
            *   Instantiates `CollaborationAppService` with the repositories, domain services, and broadcaster.
        *   **Returns**: An instance of `CollaborationAppService`.
    *   `get_current_user(token: str = Query(...), auth_client: AuthServiceClient = Depends(get_auth_service_client)) -> UserSchema`:
        *   **Signature**: `async def get_current_user(token: str = Query(...), ...) -> UserSchema:`
        *   **Logic**:
            *   Receives the token from WebSocket query parameters.
            *   Calls `auth_client.validate_token(token)`.
            *   If token is invalid or validation fails, raises `HTTPException(status_code=401, detail="Invalid authentication credentials")` or a specific WebSocket close code.
            *   If valid, returns `UserSchema` (a Pydantic model representing user data, e.g., `user_id`, `email`).
        *   **Error Handling**: Handles exceptions from `AuthServiceClient` (e.g., connection errors, invalid token).
    *   `get_redis_client() -> Redis`:
        *   **Signature**: `async def get_redis_client() -> redis.asyncio.Redis:`
        *   **Logic**: Returns a Redis client instance from `infrastructure.redis.connection.get_redis_client()`.
    *   `get_auth_service_client() -> AuthServiceClient`:
        *   **Signature**: `async def get_auth_service_client() -> AuthServiceClient:`
        *   **Logic**: Instantiates and returns an `AuthServiceClient` using `settings.AUTH_SERVICE_URL`. Could be a singleton.
*   **Documentation**: "Contains FastAPI dependency functions for injecting application services, database connections, and handling user authentication for WebSocket endpoints."

---

**File: `src/creativeflow/collaboration/domain/__init__.py`**
*   **Purpose**: Initializes the `domain` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/aggregates/__init__.py`**
*   **Purpose**: Initializes the `aggregates` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/aggregates/collaboration_session.py`**
*   **Purpose**: Models a real-time collaboration session.
*   **Key Classes/Modules**:
    *   `SessionId(UUID)`: Value object for session identifier.
    *   `UserId(str)`: Value object for user identifier. (Could be UUID if users have UUIDs).
    *   `DocumentId(str)`: Value object for document identifier. (Could be UUID).
    *   `Participant(BaseModel)` from Pydantic:
        *   `user_id: UserId`
        *   `websocket_id: str` (Unique ID for the WebSocket connection, e.g., client-generated or server-assigned on connect)
        *   `joined_at: datetime`
        *   `presence_status: str = "online"` (e.g., 'online', 'idle')
        *   `cursor_position: Optional[dict] = None` (If cursor sharing is implemented)
    *   `CollaborationSession(BaseModel)` from Pydantic (representing the state, not a full aggregate root with behavior here if Redis is the source of truth for active sessions. If it is an aggregate root, it would have methods.):
        *   `id: SessionId = Field(default_factory=uuid.uuid4)`
        *   `document_id: DocumentId`
        *   `participants: Dict[UserId, Participant] = Field(default_factory=dict)` (Mapping UserId to Participant object)
        *   `y_doc_state: bytes` (Serialized Yjs document state)
        *   `created_at: datetime = Field(default_factory=datetime.utcnow)`
        *   `last_activity_at: datetime = Field(default_factory=datetime.utcnow)`
*   **Methods/Functions (if `CollaborationSession` is a true aggregate with behavior, otherwise this logic is in `CollaborationAppService` or Redis repo)**:
    *   `add_participant(self, user_id: UserId, websocket_id: str) -> None`:
        *   Adds participant if not already present. Updates `last_activity_at`. Raises `ParticipantJoinedEvent`.
    *   `remove_participant(self, user_id: UserId) -> None`:
        *   Removes participant. Updates `last_activity_at`. Raises `ParticipantLeftEvent`.
    *   `is_participant(self, user_id: UserId) -> bool`: Checks if user is a participant.
    *   `update_participant_presence(self, user_id: UserId, status: str, cursor_position: Optional[dict]) -> None`: Updates presence details.
    *   `update_ydoc_state(self, new_state: bytes) -> None`: Updates the Yjs document state and `last_activity_at`.
    *   `get_ydoc_state(self) -> bytes`: Returns current Yjs document state.
*   **Logic Description**: `CollaborationSession` primarily acts as a data container for session state stored in Redis. Logic for managing participants and YDoc state updates will largely reside in the application service, which loads, modifies, and saves this session state to/from Redis.
*   **Documentation**: "Defines data structures for representing a collaboration session, its participants, and the associated shared document's CRDT state. Primarily used for structuring data in Redis."

---

**File: `src/creativeflow/collaboration/domain/aggregates/shared_document.py`**
*   **Purpose**: Manages the CRDT state of a shared document using Yjs.
*   **Key Classes/Modules**:
    *   `SharedYDoc`: (Not a separate DB entity, but a conceptual wrapper around a `y_py.YDoc` instance, managed per session, typically held by `CollaborationSession` or in application service memory for an active session, backed by `y_doc_state` in Redis).
*   **Methods/Functions (These would be part of `CRDTService` or directly use `y_py` in `CollaborationAppService`)**:
    *   The methods listed in the file structure (`SharedDocument.apply_update`, `get_document_state`, `get_diff`) are conceptually what needs to be done with a `YDoc` instance. The actual implementation will use `y_py` methods.
*   **Logic Description**: This file might mostly contain type aliases (`DocumentId`, `UserId`) if the Yjs document itself is managed directly within the `CollaborationSession` state or by the `CRDTService`. The core idea is that each active session (`CollaborationSession`) will have an associated Yjs document instance (`YDoc`).
*   **Documentation**: "Conceptually represents a shared document whose state is managed by Yjs. Actual Yjs document instances (`YDoc`) are typically associated with active `CollaborationSession` states."

---

**File: `src/creativeflow/collaboration/domain/entities/__init__.py`**
*   **Purpose**: Initializes the `entities` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/entities/presence.py`**
*   **Purpose**: Models a user's presence status.
*   **Key Classes/Modules**:
    *   `UserId(str)`: (Re-export or define if not globally available from `shared_document.py` or similar).
    *   `SessionId(UUID)`: (Re-export or define).
    *   `PresenceStatus(str, Enum)` from `enum`:
        *   `ONLINE = "online"`
        *   `AWAY = "away"` (Example, could be 'idle')
        *   `OFFLINE = "offline"`
    *   `Presence(BaseModel)` from Pydantic:
        *   `user_id: UserId`
        *   `session_id: SessionId`
        *   `status: PresenceStatus`
        *   `last_seen_at: datetime`
        *   `cursor_position: Optional[dict] = None` (If cursor sharing is implemented)
*   **Logic Description**: A DTO representing presence information, primarily stored and retrieved via `RedisPresenceRepositoryImpl`.
*   **Documentation**: "Represents a user's presence information (status, last seen) within a specific collaboration session."

---

**File: `src/creativeflow/collaboration/domain/events/__init__.py`**
*   **Purpose**: Initializes the `events` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/events/collaboration_events.py`**
*   **Purpose**: Defines domain events.
*   **Key Classes/Modules (Pydantic models)**:
    *   `BaseEvent(BaseModel)`:
        *   `event_id: UUID = Field(default_factory=uuid.uuid4)`
        *   `timestamp: datetime = Field(default_factory=datetime.utcnow)`
    *   `SessionStartedEvent(BaseEvent)`:
        *   `session_id: SessionId`
        *   `document_id: DocumentId`
        *   `user_id: UserId`
    *   `ParticipantJoinedEvent(BaseEvent)`:
        *   `session_id: SessionId`
        *   `user_id: UserId`
        *   `participant_details: Participant` (from `collaboration_session.py`)
    *   `ParticipantLeftEvent(BaseEvent)`:
        *   `session_id: SessionId`
        *   `user_id: UserId`
    *   `DocumentUpdatedEvent(BaseEvent)`:
        *   `session_id: SessionId`
        *   `document_id: DocumentId`
        *   `yjs_update: bytes` (The binary update/diff)
        *   `originator_websocket_id: str` (To avoid sending update back to sender if broadcaster handles it)
    *   `PresenceChangedEvent(BaseEvent)`:
        *   `session_id: SessionId`
        *   `user_id: UserId`
        *   `status: PresenceStatus`
        *   `cursor_position: Optional[dict]`
*   **Logic Description**: Simple data containers for events. These are not directly dispatched via a message bus in this service usually; rather, they inform what messages the `WebsocketBroadcaster` should construct and send.
*   **Documentation**: "Defines data structures for events that occur within the collaboration domain, used internally to trigger appropriate actions like broadcasting messages."

---

**File: `src/creativeflow/collaboration/domain/services/__init__.py`**
*   **Purpose**: Initializes the `services` (domain services) sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/services/crdt_service.py`**
*   **Purpose**: Abstraction for CRDT operations using `y-py`.
*   **Key Classes/Modules**:
    *   `CRDTService`:
*   **Methods/Functions**:
    *   `initialize_document() -> YDoc`:
        *   **Signature**: `def initialize_document() -> YDoc:` (Static method or instance method)
        *   **Logic**: `return YDoc()`
    *   `apply_update_to_document(ydoc: YDoc, update_payload: bytes) -> None`:
        *   **Signature**: `def apply_update_to_document(ydoc: YDoc, update_payload: bytes) -> None:`
        *   **Logic**: `ydoc.apply_update(update_payload)`
        *   **Error Handling**: Catches `y_py` exceptions if any, re-raises as domain-specific exceptions if needed.
    *   `encode_state_vector(ydoc: YDoc) -> bytes`:
        *   **Signature**: `def encode_state_vector(ydoc: YDoc) -> bytes:`
        *   **Logic**: `return ydoc.get_state_vector()`
    *   `encode_state_as_update(ydoc: YDoc, encoded_target_state_vector: Optional[bytes] = None) -> bytes`:
        *   **Signature**: `def encode_state_as_update(...) -> bytes:`
        *   **Logic**: `return ydoc.get_update(encoded_target_state_vector)`
    *   `merge_updates(ydoc: YDoc, updates: List[bytes]) -> None`: (Less common for Yjs, as updates are applied sequentially)
        *   **Signature**: `def merge_updates(ydoc: YDoc, updates: List[bytes]) -> None:`
        *   **Logic**: Iteratively calls `ydoc.apply_update(u)` for each update in the list.
*   **Documentation**: "Service layer providing stateless CRDT (Yjs/`y-py`) document manipulations, such as applying updates and generating state vectors or diffs."

---

**File: `src/creativeflow/collaboration/domain/services/conflict_resolution_service.py`**
*   **Purpose**: Handles conflict resolution for offline edits (REQ-019.1).
*   **Key Classes/Modules**:
    *   `ConflictResolutionService`:
*   **Methods/Functions**:
    *   `resolve_offline_edits(self, current_ydoc_state: bytes, offline_changes_payloads: List[bytes]) -> bytes`:
        *   **Signature**: `async def resolve_offline_edits(...) -> bytes:` (Could be sync if no I/O)
        *   **Logic**:
            1.  Create a new `YDoc` instance.
            2.  Apply `current_ydoc_state` to it.
            3.  Iterate through `offline_changes_payloads` (which are Yjs updates) and apply each one to the `YDoc` using `crdt_service.apply_update_to_document`. Yjs is designed to merge concurrent changes correctly.
            4.  Return the new merged state: `crdt_service.encode_state_as_update(ydoc_instance)`.
            5.  For REQ-019.1, this service primarily leverages Yjs's merging. If "complex changes" require user prompting, this service would identify such scenarios (though Yjs aims to avoid this) and signal the application layer to initiate UI prompts. For the initial scope, direct Yjs merging is assumed.
        *   **Returns**: The merged Yjs document state as bytes.
*   **Documentation**: "Handles the merging of offline edits into the current document state using Yjs CRDT capabilities, as per REQ-019.1."

---

**File: `src/creativeflow/collaboration/domain/repositories/__init__.py`**
*   **Purpose**: Initializes the `repositories` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/domain/repositories/collaboration_repository.py`**
*   **Purpose**: Defines repository interfaces for collaboration data.
*   **Key Classes/Modules (Protocols or ABCs)**:
    *   `ICollaborationSessionRepository(Protocol)`:
        *   `get_by_document_id(self, document_id: DocumentId) -> Awaitable[Optional[CollaborationSession]]` (Sessions are usually per document)
        *   `save(self, session: CollaborationSession) -> Awaitable[None]`
        *   `delete_by_document_id(self, document_id: DocumentId) -> Awaitable[None]`
        *   `add_participant_to_session(self, document_id: DocumentId, participant: Participant) -> Awaitable[None]`
        *   `remove_participant_from_session(self, document_id: DocumentId, user_id: UserId) -> Awaitable[None]`
        *   `update_session_ydoc_state(self, document_id: DocumentId, ydoc_state: bytes, last_activity_at: datetime) -> Awaitable[None]`
        *   `update_session_last_activity(self, document_id: DocumentId, last_activity_at: datetime) -> Awaitable[None]`

    *   `IPresenceRepository(Protocol)`:
        *   `get_presence(self, document_id: DocumentId, user_id: UserId) -> Awaitable[Optional[Presence]]`
        *   `save_presence(self, presence: Presence) -> Awaitable[None]`
        *   `delete_presence(self, document_id: DocumentId, user_id: UserId) -> Awaitable[None]`
        *   `get_all_in_session(self, document_id: DocumentId) -> Awaitable[List[Presence]]`
*   **Documentation**: "Interfaces (protocols) for persisting and retrieving collaboration-related domain data like sessions and presence."

---

**File: `src/creativeflow/collaboration/application/__init__.py`**
*   **Purpose**: Initializes the `application` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/application/services/__init__.py`**
*   **Purpose**: Initializes the `services` (application services) sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/application/services/collaboration_app_service.py`**
*   **Purpose**: Orchestrates collaboration use cases.
*   **Key Classes/Modules**:
    *   `CollaborationAppService`:
        *   **Constructor**: `__init__(self, session_repo: ICollaborationSessionRepository, presence_repo: IPresenceRepository, crdt_service: CRDTService, conflict_resolver: ConflictResolutionService, broadcaster: WebsocketBroadcaster, connection_manager: ConnectionManager)`
*   **Methods/Functions**:
    *   `handle_join_session(self, user: UserSchema, document_id: DocumentId, websocket_id: str) -> Tuple[bytes, List[Participant]]`:
        *   **Logic**:
            1.  Fetch `CollaborationSession` for `document_id` from `session_repo`.
            2.  If not found, create a new one with an initial empty Yjs document state from `crdt_service.initialize_document()`.
            3.  Create `Participant` object for the user.
            4.  Add participant to session: `session_repo.add_participant_to_session(document_id, participant)`.
            5.  Update/save user presence: `presence_repo.save_presence(...)`.
            6.  Load current `y_doc_state` from session.
            7.  Broadcast `ParticipantJoinedEvent` or equivalent message via `broadcaster` to other participants in the session.
            8.  Return initial Yjs document state and list of current participants.
        *   **Error Handling**: If session cannot be loaded/created.
    *   `handle_leave_session(self, user_id: UserId, document_id: DocumentId, websocket_id: str) -> None`:
        *   **Logic**:
            1.  Remove participant from `session_repo`.
            2.  Delete presence from `presence_repo`.
            3.  Broadcast `ParticipantLeftEvent` or equivalent message via `broadcaster`.
            4.  If no participants left, consider session cleanup logic (e.g., persist final YDoc state if needed, remove from active Redis sessions after TTL).
    *   `handle_apply_document_change(self, user_id: UserId, document_id: DocumentId, yjs_update: bytes, originator_websocket_id: str) -> None`:
        *   **Logic**:
            1.  Fetch current `CollaborationSession` (primarily its `y_doc_state`) for `document_id` from `session_repo`.
            2.  Create a `YDoc` instance and apply the current state to it.
            3.  Apply the incoming `yjs_update` using `crdt_service.apply_update_to_document(ydoc_instance, yjs_update)`.
            4.  Get the new full state or a diff: `new_state_or_diff = crdt_service.encode_state_as_update(ydoc_instance, client_state_vector_if_provided)`.
            5.  Persist the new `ydoc_instance.get_state_vector()` to `session_repo.update_session_ydoc_state(...)`.
            6.  Broadcast `DocumentUpdatedEvent` (containing `new_state_or_diff` and `originator_websocket_id`) via `broadcaster` to all participants in the session.
    *   `handle_presence_update(self, user_id: UserId, document_id: DocumentId, status: PresenceStatus, cursor_position: Optional[dict]) -> None`:
        *   **Logic**:
            1.  Create/Update `Presence` object.
            2.  Save to `presence_repo`.
            3.  Broadcast `PresenceChangedEvent` via `broadcaster`.
    *   `handle_offline_changes(self, user_id: UserId, document_id: DocumentId, offline_yjs_updates: List[bytes]) -> None` (REQ-019.1):
        *   **Logic**:
            1.  Fetch current `CollaborationSession` (its `y_doc_state`) for `document_id`.
            2.  Use `conflict_resolution_service.resolve_offline_edits(current_ydoc_state, offline_yjs_updates)` to get the merged document state.
            3.  Persist the new merged state via `session_repo.update_session_ydoc_state(...)`.
            4.  Broadcast the new state/diff to all connected clients in the session.
*   **Documentation**: "Application service orchestrating collaboration use cases like joining sessions, applying document changes, managing presence, and handling offline edits. Interacts with domain services and repositories."

---

**File: `src/creativeflow/collaboration/application/commands/__init__.py`**
*   **Purpose**: Initializes the `commands` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/application/commands/collaboration_commands.py`**
*   **Purpose**: DTOs for collaboration actions.
*   **Key Classes/Modules (Pydantic models)**:
    *   `BaseCommand(BaseModel)`
    *   `JoinSessionCommand(BaseCommand)`:
        *   `user: UserSchema` (Contains authenticated user details like `user_id`)
        *   `document_id: str` (or `DocumentId`)
        *   `websocket_id: str`
    *   `ApplyDocumentChangeCommand(BaseCommand)`:
        *   `user_id: str` (or `UserId`)
        *   `document_id: str` (or `DocumentId`)
        *   `yjs_update: bytes`
        *   `originator_websocket_id: str`
    *   `UpdatePresenceCommand(BaseCommand)`:
        *   `user_id: str` (or `UserId`)
        *   `document_id: str` (or `DocumentId`)
        *   `status: str` (or `PresenceStatus`)
        *   `cursor_position: Optional[dict] = None`
    *   `ProcessOfflineChangesCommand(BaseCommand)`:
        *   `user_id: str`
        *   `document_id: str`
        *   `offline_yjs_updates: List[bytes]`
*   **Documentation**: "Data Transfer Objects (Pydantic models) representing commands for the collaboration application service, typically derived from incoming WebSocket messages."

---

**File: `src/creativeflow/collaboration/application/schemas/__init__.py`**
*   **Purpose**: Initializes the `schemas` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/application/schemas/message_schemas.py`**
*   **Purpose**: Pydantic schemas for WebSocket messages.
*   **Key Classes/Modules (Pydantic models)**:
    *   `ClientMessageType(str, Enum)`:
        *   `JOIN_SESSION = "join_session"`
        *   `LEAVE_SESSION = "leave_session"`
        *   `DOC_UPDATE = "doc_update"`
        *   `PRESENCE_UPDATE = "presence_update"`
        *   `SYNC_OFFLINE_CHANGES = "sync_offline_changes"`
    *   `ServerMessageType(str, Enum)`:
        *   `SESSION_STATE = "session_state"` (Initial state on join)
        *   `PARTICIPANT_JOINED = "participant_joined"`
        *   `PARTICIPANT_LEFT = "participant_left"`
        *   `DOC_UPDATE_BROADCAST = "doc_update_broadcast"`
        *   `PRESENCE_UPDATE_BROADCAST = "presence_update_broadcast"`
        *   `ERROR_MESSAGE = "error_message"`
        *   `SYNC_CONFIRMATION = "sync_confirmation"`
    *   `BaseIncomingMessage(BaseModel)`:
        *   `type: ClientMessageType`
        *   `payload: dict` (Generic payload, specific message types will define it)
    *   `IncomingJoinSessionPayload(BaseModel)`:
        *   `document_id: str`
    *   `IncomingDocUpdatePayload(BaseModel)`:
        *   `yjs_update: bytes` (or base64 encoded string if JSON is strictly used for transport)
    *   `IncomingPresenceUpdatePayload(BaseModel)`:
        *   `status: str`
        *   `cursor_position: Optional[dict] = None`
    *   `IncomingSyncOfflineChangesPayload(BaseModel)`:
        *   `document_id: str`
        *   `updates: List[bytes]` (or List[str] if base64)

    *   `BaseOutgoingMessage(BaseModel)`:
        *   `type: ServerMessageType`
        *   `payload: dict`
    *   `OutgoingSessionStatePayload(BaseModel)`:
        *   `document_id: str`
        *   `ydoc_state: bytes` (or base64 string)
        *   `participants: List[dict]` (List of Participant schemas)
    *   `OutgoingParticipantJoinedPayload(BaseModel)`:
        *   `user_id: str`
        *   `participant_details: dict` (Participant schema)
    *   `OutgoingDocUpdateBroadcastPayload(BaseModel)`:
        *   `yjs_update: bytes` (or base64 string)
        *   `originator_websocket_id: str`
    *   `OutgoingErrorMessagePayload(BaseModel)`:
        *   `message: str`
        *   `code: Optional[str] = None`
*   **Documentation**: "Pydantic models defining the structure (schemas) for messages exchanged over WebSockets between clients and the collaboration server."

---

**File: `src/creativeflow/collaboration/application/event_handlers/__init__.py`**
*   **Purpose**: Initializes the `event_handlers` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/application/event_handlers/domain_event_handlers.py`**
*   **Purpose**: Handles domain events, often by triggering broadcasts.
*   **Key Classes/Modules**:
    *   `DomainEventHandlers`: (May not be a class, could be individual functions registered to an event bus if one existed, or directly called by `CollaborationAppService` before/after `broadcaster` calls).
    *   For simplicity, this logic is often embedded within the `CollaborationAppService` itself, right before it calls the `WebsocketBroadcaster`. If a true event bus was used, these handlers would subscribe to it.
*   **Methods/Functions**:
    *   (Example if using an event bus) `handle_document_updated_event(event: DocumentUpdatedEvent, broadcaster: WebsocketBroadcaster)`:
        *   **Logic**: Constructs appropriate `OutgoingDocUpdateBroadcastMessage` from `event` and calls `broadcaster.broadcast_to_session(...)`.
*   **Logic Description**: In the current design, these "handlers" are implicitly part of `CollaborationAppService` methods that interact with the `WebsocketBroadcaster`. The broadcaster itself takes domain-like information and constructs the actual `message_schemas` payload to send.
*   **Documentation**: "Conceptually, these handlers would react to domain events. In this implementation, such logic is typically integrated within the `CollaborationAppService` before broadcasting messages."

---

**File: `src/creativeflow/collaboration/infrastructure/__init__.py`**
*   **Purpose**: Initializes the `infrastructure` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/infrastructure/redis/__init__.py`**
*   **Purpose**: Initializes the `redis` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/infrastructure/redis/connection.py`**
*   **Purpose**: Manages Redis connection.
*   **Key Classes/Modules**: None (module-level functions and variable).
*   **Global Variable**: `_redis_pool: Optional[redis.asyncio.ConnectionPool] = None`
*   **Methods/Functions**:
    *   `init_redis_pool(redis_url: str, redis_password: Optional[str] = None) -> None`:
        *   **Signature**: `async def init_redis_pool(...) -> None:`
        *   **Logic**: Creates `redis.asyncio.ConnectionPool.from_url(redis_url, password=redis_password, max_connections=...)` and assigns to `_redis_pool`. Logs success or failure.
    *   `get_redis_client() -> redis.asyncio.Redis`:
        *   **Signature**: `def get_redis_client() -> redis.asyncio.Redis:`
        *   **Logic**: If `_redis_pool` is None, raises Exception. Returns `redis.asyncio.Redis(connection_pool=_redis_pool)`.
    *   `close_redis_pool() -> None`:
        *   **Signature**: `async def close_redis_pool() -> None:`
        *   **Logic**: If `_redis_pool` is not None, calls `await _redis_pool.disconnect()`.
*   **Documentation**: "Manages the connection pool for interacting with the Redis server. Provides functions to initialize, retrieve, and close connections."

---

**File: `src/creativeflow/collaboration/infrastructure/redis/repositories/__init__.py`**
*   **Purpose**: Initializes Redis repositories.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/infrastructure/redis/repositories/redis_collaboration_repository.py`**
*   **Purpose**: Redis implementation of collaboration repositories.
*   **Key Classes/Modules**:
    *   `RedisCollaborationSessionRepositoryImpl(ICollaborationSessionRepository)`:
        *   **Constructor**: `__init__(self, redis_client: redis.asyncio.Redis)`
        *   **Redis Key Strategy**:
            *   Session data (YDoc state, participants): `session:{document_id}` (Hash)
                *   Field `ydoc_state`: `bytes`
                *   Field `participants_json`: JSON string of `Dict[UserId, Participant]`
                *   Field `last_activity_at`: ISO datetime string
            *   Active participants in session (Set for quick lookup): `session:{document_id}:users` (Set of UserIds)
    *   `RedisPresenceRepositoryImpl(IPresenceRepository)`:
        *   **Constructor**: `__init__(self, redis_client: redis.asyncio.Redis)`
        *   **Redis Key Strategy**:
            *   User presence in session: `presence:{document_id}:{user_id}` (Hash)
                *   Field `status`: `str`
                *   Field `last_seen_at`: ISO datetime string
                *   Field `cursor_position_json`: JSON string of cursor dict
*   **Methods/Functions**:
    *   Implement all methods from `ICollaborationSessionRepository` and `IPresenceRepository` using `self.redis_client` async methods (e.g., `hget`, `hset`, `sadd`, `srem`, `smembers`, `delete`).
    *   Serialization/Deserialization: Use Pydantic's `.model_dump_json()` and `.model_validate_json()` for complex objects stored as JSON strings in Redis hashes. YDoc state is stored as `bytes`.
    *   Session TTL: When saving/updating session data, set an expiry (e.g., using `settings.YJS_DOC_TTL_SECONDS`) to automatically clean up inactive sessions.
*   **Documentation**: "Implements `ICollaborationSessionRepository` and `IPresenceRepository` using Redis. Stores session YDoc states, participant lists, and user presence information. Manages Redis key structures and data serialization."

---

**File: `src/creativeflow/collaboration/infrastructure/redis/pubsub_manager.py`**
*   **Purpose**: Manages Redis Pub/Sub for multi-instance WebSocket scaling (Optional for initial single-instance, but good for design).
*   **Key Classes/Modules**:
    *   `RedisPubSubManager`:
        *   **Constructor**: `__init__(self, redis_client: redis.asyncio.Redis)`
*   **Methods/Functions**:
    *   `publish_message(self, channel: str, message_payload: str) -> None`:
        *   **Signature**: `async def publish_message(self, channel: str, message_payload: str) -> None:`
        *   **Logic**: `await self.redis_client.publish(channel, message_payload)` (message_payload should be JSON string of the message to broadcast).
    *   `subscribe_to_channel(self, channel_pattern: str, callback: Callable[[str, str], Awaitable[None]]) -> None`:
        *   **Signature**: `async def subscribe_to_channel(self, channel_pattern: str, callback: Callable[[str, str], Awaitable[None]]) -> None:` (callback takes channel and message)
        *   **Logic**: Uses `redis_client.pubsub()` and `psubscribe` or `subscribe`. Listens in a separate task/coroutine and invokes `callback` with received messages.
*   **Documentation**: "Manages publishing and subscribing to messages using Redis Pub/Sub. This is intended for scaling WebSocket message broadcasting across multiple service instances by relaying messages."

---

**File: `src/creativeflow/collaboration/infrastructure/websocket/__init__.py`**
*   **Purpose**: Initializes the `websocket` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/infrastructure/websocket/connection_manager.py`**
*   **Purpose**: Manages active WebSocket connections.
*   **Key Classes/Modules**:
    *   `ConnectionManager`:
        *   **Attributes**:
            *   `active_connections_by_session: DefaultDict[DocumentId, Dict[str, WebSocket]] = defaultdict(dict)`
                (Maps `document_id` to a dict of `websocket_id` to `WebSocket` object)
            *   `websocket_to_user_map: Dict[WebSocket, Tuple[UserId, DocumentId, str]] = {}`
                (Maps `WebSocket` object to `(user_id, document_id, websocket_id)`)
        *   **Methods**:
            *   `connect(self, websocket: WebSocket, document_id: DocumentId, user_id: UserId, websocket_id: str) -> None`:
                *   Adds `websocket` to `active_connections_by_session[document_id][websocket_id]`.
                *   Adds mapping to `websocket_to_user_map`.
            *   `disconnect(self, websocket: WebSocket) -> Optional[Tuple[UserId, DocumentId, str]]`:
                *   Retrieves `user_id, document_id, websocket_id` from `websocket_to_user_map`.
                *   Removes from both dictionaries.
                *   Returns the tuple if found, else None.
            *   `get_connections_for_session(self, document_id: DocumentId) -> List[WebSocket]`:
                *   Returns `list(self.active_connections_by_session.get(document_id, {}).values())`.
            *   `get_user_details_for_connection(self, websocket: WebSocket) -> Optional[Tuple[UserId, DocumentId, str]]`:
                *   Returns entry from `websocket_to_user_map.get(websocket)`.
            *   `get_websocket_by_id(self, document_id: DocumentId, websocket_id: str) -> Optional[WebSocket]`:
                *   Returns `self.active_connections_by_session.get(document_id, {}).get(websocket_id)`.
*   **Singleton**: This class should typically be a singleton instance managed by the DI system or globally.
*   **Thread Safety**: If not using asyncio tasks correctly, locking might be needed, but FastAPI + asyncio usually handles concurrency per request/connection.
*   **Documentation**: "Manages active WebSocket connections, tracking them per session and user. Provides methods to connect, disconnect, and retrieve connection information."

---

**File: `src/creativeflow/collaboration/infrastructure/websocket/broadcaster.py`**
*   **Purpose**: Broadcasts messages to WebSocket clients.
*   **Key Classes/Modules**:
    *   `WebsocketBroadcaster`:
        *   **Constructor**: `__init__(self, connection_manager: ConnectionManager, pubsub_manager: Optional[RedisPubSubManager] = None)`
*   **Methods/Functions**:
    *   `broadcast_to_session(self, document_id: DocumentId, message: BaseOutgoingMessage, originator_websocket_id: Optional[str] = None) -> None`:
        *   **Signature**: `async def broadcast_to_session(...) -> None:`
        *   **Logic**:
            1.  Serialize `message` to JSON string: `message_json = message.model_dump_json()`.
            2.  If `self.pubsub_manager` is configured (for multi-instance scaling):
                *   `await self.pubsub_manager.publish_message(f"session:{document_id}", message_json)`
            3.  Else (single instance or this instance also handles local broadcast from pubsub):
                *   Get connections: `connections = self.connection_manager.get_connections_for_session(document_id)`.
                *   Iterate `connections`:
                    *   Retrieve `ws_user_id, ws_doc_id, ws_websocket_id` using `connection_manager.get_user_details_for_connection(ws)`.
                    *   If `ws_websocket_id == originator_websocket_id`, skip (don't send back to sender).
                    *   `await ws.send_text(message_json)`.
                    *   Handle `ConnectionClosed` exceptions gracefully (log, attempt to remove from `ConnectionManager` if not already handled).
*   **Pub/Sub Integration (for scaling)**: If `RedisPubSubManager` is used, each service instance would also subscribe to relevant channels (e.g., `session:*`). When a message is received from Pub/Sub, it would then broadcast to its locally managed WebSockets for that session. The `originator_websocket_id` helps prevent Pub/Sub messages from being sent back to the original sender if the publishing instance also subscribes.
*   **Documentation**: "Handles broadcasting messages to clients within a specific collaboration session, potentially using Redis Pub/Sub for multi-instance scaling."

---

**File: `src/creativeflow/collaboration/infrastructure/external_services/__init__.py`**
*   **Purpose**: Initializes the `external_services` sub-package.
*   **Contents**: Empty.

---

**File: `src/creativeflow/collaboration/infrastructure/external_services/auth_service_client.py`**
*   **Purpose**: HTTP client for Auth Service.
*   **Key Classes/Modules**:
    *   `UserSchema(BaseModel)`: Pydantic model matching the expected user data structure from Auth Service.
        *   `id: str` (or `UserId`)
        *   `email: str`
        *   `roles: List[str]` (Example)
    *   `AuthServiceClient`:
        *   **Constructor**: `__init__(self, base_url: str, timeout: int = 5)`
        *   **Methods**:
            *   `validate_token(self, token: str) -> Optional[UserSchema]`:
                *   **Signature**: `async def validate_token(self, token: str) -> Optional[UserSchema]:`
                *   **Logic**:
                    1.  Uses `httpx.AsyncClient()`.
                    2.  Makes a GET or POST request to `self.base_url}/validate_token` (or similar endpoint defined by Auth Service) with the token (e.g., in Authorization header).
                    3.  Handles successful response (200 OK): parse JSON response into `UserSchema`.
                    4.  Handles error responses (401, 403, 5xx): log error, return `None` or raise specific exception.
                    5.  Handles connection errors/timeouts: log error, return `None` or raise.
                *   **Error Handling**: `HTTPStatusError`, `RequestError` from `httpx`.
*   **Documentation**: "HTTP client for interacting with the `CreativeFlow.AuthService` to validate user JWTs provided during WebSocket connection establishment."

---

**File: `src/creativeflow/collaboration/api/__init__.py`**
*   **Purpose**: Initializes the `api` sub-package.
*   **Contents**:
    python
    from fastapi import APIRouter
    from .websocket_router import router as websocket_router

    api_router = APIRouter()
    api_router.include_router(websocket_router, prefix="/ws", tags=["collaboration"]) 
    # Prefix might be handled by main app if this router is included there.
    # If this service is standalone, /ws is fine.
    

---

**File: `src/creativeflow/collaboration/api/websocket_router.py`**
*   **Purpose**: Defines FastAPI WebSocket endpoints.
*   **Key Classes/Modules**:
    *   `router = APIRouter()`
*   **Methods/Functions**:
    *   `collaboration_websocket_endpoint(websocket: WebSocket, document_id: str, token: Optional[str] = Query(None), current_user: UserSchema = Depends(dependencies.get_current_user), app_service: CollaborationAppService = Depends(dependencies.get_collaboration_app_service), conn_manager: ConnectionManager = Depends(provide_connection_manager_singleton))`:
        *   **Signature**: `@router.websocket("/document/{document_id}")\nasync def collaboration_websocket_endpoint(...)`
        *   **Logic**:
            1.  `websocket_id = str(uuid.uuid4())` (Generate a unique ID for this connection).
            2.  `await conn_manager.connect(websocket, document_id, current_user.id, websocket_id)`
            3.  Call `app_service.handle_join_session(current_user, document_id, websocket_id)`. Send initial state (`OutgoingSessionStateMessage`) to the connected `websocket`.
            4.  **Message Loop**:
                python
                try:
                    while True:
                        data = await websocket.receive_text() # Or receive_bytes if sending binary Yjs updates directly
                        # Deserialize 'data' into a BaseIncomingMessage or specific type
                        # e.g., incoming_msg = BaseIncomingMessage.model_validate_json(data)
                        # Based on incoming_msg.type:
                        #   if ClientMessageType.DOC_UPDATE:
                        #       payload = IncomingDocUpdatePayload.model_validate(incoming_msg.payload)
                        #       await app_service.handle_apply_document_change(
                        #           user_id=current_user.id, 
                        #           document_id=document_id, 
                        #           yjs_update=payload.yjs_update,
                        #           originator_websocket_id=websocket_id
                        #       )
                        #   elif ClientMessageType.PRESENCE_UPDATE:
                        #       # ... call app_service.handle_presence_update
                        #   elif ClientMessageType.SYNC_OFFLINE_CHANGES:
                        #       # ... call app_service.handle_offline_changes
                        #   # etc.
                except WebSocketDisconnect:
                    logger.info(f"WebSocket disconnected for user {current_user.id} on doc {document_id}")
                except Exception as e:
                    logger.error(f"Error in WebSocket for user {current_user.id}: {e}")
                    # Optionally send an error message to the client before closing
                    # await websocket.send_text(OutgoingErrorMessage(message="Internal server error").model_dump_json())
                finally:
                    conn_manager.disconnect(websocket)
                    await app_service.handle_leave_session(current_user.id, document_id, websocket_id)
                
        *   **Dependency**: `provide_connection_manager_singleton` would be a dependency that returns the singleton instance of `ConnectionManager`.
*   **Authentication**: Handled by `Depends(dependencies.get_current_user)`. If auth fails, the dependency raises an exception and FastAPI closes the WebSocket connection appropriately before this handler fully executes.
*   **Error Handling**: `WebSocketDisconnect` is handled gracefully. Other exceptions should be logged, and potentially a generic error message sent to client before closing connection.
*   **Documentation**: "Defines the primary WebSocket endpoint (`/ws/document/{document_id}`) for real-time collaboration. Handles connection lifecycle, authentication, message parsing, and dispatching actions to the `CollaborationAppService`."

---

**File: `requirements.txt`**
*   **Purpose**: Lists Python dependencies.
*   **Contents**:
    
    fastapi==0.110.0  # Or latest compatible
    uvicorn[standard]==0.29.0 # Or latest
    websockets==12.0 # FastAPI uses this
    y-py==0.7.0 # Or latest compatible
    redis[hiredis]==5.0.3 # Or latest async compatible
    httpx==0.27.0 # Or latest
    pydantic==2.6.4 # Or latest
    python-dotenv==1.0.1 # For .env loading
    # Add any other direct dependencies
    
*   **Note**: Versions are examples and should be updated to latest stable compatible versions.

---

**File: `.env.example`**
*   **Purpose**: Example environment variables template.
*   **Contents**:
    env
    REDIS_URL="redis://localhost:6379/0"
    # REDIS_PASSWORD="your_redis_password" # Uncomment if password protected
    AUTH_SERVICE_URL="http://localhost:8001/api/v1/auth" # Adjust port if Auth service runs elsewhere
    JWT_SECRET_KEY="your-very-secret-jwt-key-for-auth-service-communication-if-needed" # Ideally, Auth service validates its own tokens
    LOG_LEVEL="INFO"
    YJS_GC_ENABLED="True"
    YJS_DOC_TTL_SECONDS="3600"
    MAX_WEBSOCKET_MESSAGE_SIZE="4194304"
    WEBSOCKET_SESSION_TIMEOUT_SECONDS="3600"
    DEBUG_MODE="False"
    
*   **Note**: For production, these would be set in the environment, not an `.env` file, and sensitive values like `JWT_SECRET_KEY` or `REDIS_PASSWORD` managed by a secrets manager.

---

**File: `Dockerfile`**
*   **Purpose**: Builds the service container image.
*   **Contents**:
    dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.11-slim

    # Set the working directory in the container
    WORKDIR /app

    # Install system dependencies if any (e.g., for hiredis or other C extensions)
    # RUN apt-get update && apt-get install -y --no-install-recommends \
    #     # build-essential \ # if needed for some dependencies
    #     && rm -rf /var/lib/apt/lists/*

    # Copy the requirements file into the container
    COPY requirements.txt .

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of the application code into the container
    COPY ./src/creativeflow/collaboration /app/creativeflow/collaboration
    COPY ./src/creativeflow/__init__.py /app/creativeflow/__init__.py # If top-level __init__.py exists
    
    # Ensure the entrypoint script can find the main module
    ENV PYTHONPATH=/app

    # Expose the port the app runs on
    EXPOSE 8000

    # Define the command to run the application
    # Assumes main.py has 'app = FastAPI()' at the global scope or a factory function
    CMD ["uvicorn", "creativeflow.collaboration.main:app", "--host", "0.0.0.0", "--port", "8000"]
    
*   **Note**: Adjust Python version to match project. Ensure correct paths for `COPY`. The `PYTHONPATH` might be needed if the `creativeflow` top-level package is not directly in `/app`.

## 7. Data Design (Redis Specifics)

*   **Collaboration Session State (`session:{document_id}` - Redis Hash)**
    *   `ydoc_state`: (bytes) Serialized Yjs document state.
    *   `participants_json`: (string) JSON representation of `Dict[UserId, ParticipantSchema]`.
    *   `created_at`: (string) ISO 8601 datetime.
    *   `last_activity_at`: (string) ISO 8601 datetime.
    *   TTL: Set using `settings.YJS_DOC_TTL_SECONDS` to clean up inactive sessions. Updated on activity.
*   **Session Participants Set (`session:{document_id}:users` - Redis Set)**
    *   Members: `UserId` strings.
    *   Purpose: Quickly check who is in a session without parsing the full participants JSON.
    *   TTL: Should align with the main session hash TTL.
*   **User Presence in Session (`presence:{document_id}:{user_id}` - Redis Hash)**
    *   `status`: (string) e.g., "online", "away".
    *   `last_seen_at`: (string) ISO 8601 datetime.
    *   `cursor_position_json`: (string) JSON representation of cursor data, if implemented.
    *   `websocket_id`: (string) The ID of the WebSocket connection for this user in this session.
    *   TTL: Shorter TTL, refreshed frequently by client presence pings or activity. E.g., 5 minutes.
*   **(Optional for Scaling) Redis Pub/Sub Channels**:
    *   `session_broadcast:{document_id}`: Channel for broadcasting messages (e.g., document updates, presence changes) to all instances handling connections for a specific document.

## 8. Deployment Considerations

*   The service will be containerized using Docker (as per `Dockerfile`).
*   Deployed as a scalable set of instances behind a load balancer that supports WebSocket sticky sessions (if stateful connection management within a single instance is preferred over fully distributed state via Redis Pub/Sub for broadcasts) or stateless instances if using Redis Pub/Sub for broadcasting.
*   Configuration will be managed via environment variables.
*   Requires network connectivity to Redis and the Authentication Service.

## 9. Configuration Management

Configuration is managed via `src/creativeflow/collaboration/core/config.py` using Pydantic's `BaseSettings`.
Environment variables are loaded from an `.env` file during local development and injected into the container environment in staging/production.
The `.env.example` file provides a template for required variables. Key configurable items include Redis connection details, Auth service URL, logging level, and Yjs/WebSocket operational parameters.

## 10. Error Handling and Logging

*   **WebSocket Errors**:
    *   Authentication failures during handshake will result in connection closure (e.g., HTTP 401/403 during upgrade, or WebSocket close code).
    *   Invalid message formats or payloads will be logged, and an error message (using `OutgoingErrorMessagePayload`) may be sent to the client.
    *   `WebSocketDisconnect` exceptions will be caught to handle client disconnections gracefully (cleanup).
    *   Unexpected server-side errors during message processing will be logged comprehensively. A generic error message might be sent to the client, and the connection may be closed.
*   **Logging**:
    *   Standard Python `logging` module, configured by Uvicorn/FastAPI settings.
    *   Log level configurable via `LOG_LEVEL` environment variable.
    *   Key events to log: WebSocket connection/disconnection, message receipt/broadcast (potentially at DEBUG level), authentication success/failure, errors during CRDT operations, errors interacting with Redis or Auth Service.
    *   Include contextual information like `document_id`, `user_id`, `websocket_id` in logs.
*   **External Service Errors**:
    *   Errors from `AuthServiceClient` (e.g., network issues, auth service down) will be caught, logged, and result in WebSocket connection denial or termination.
    *   Errors from Redis (e.g., connection issues) will be logged; depending on severity, it might impact session operations or lead to service unavailability for specific sessions. Robust retry mechanisms for Redis operations should be considered if transient network issues are common.

## 11. Security Considerations

*   **Authentication**: All WebSocket connections must be authenticated. The `token` passed in the query parameter during connection establishment is validated against the `CreativeFlow.AuthService`. Unauthorized connections are rejected.
*   **Authorization**: Once authenticated, further authorization (e.g., can this user edit this document?) might be implicitly handled by the fact they can join the session (assuming document access is managed by another service). This service primarily focuses on syncing changes for users already authorized to be in the session. If finer-grained per-operation authorization is needed within the collaboration context, it would require additional checks.
*   **Data Validation**: Incoming WebSocket messages (payloads) must be validated using Pydantic schemas (`message_schemas.py`) to prevent malformed data issues.
*   **Secure Communication**: WSS (WebSocket Secure) must be used in production, handled by the reverse proxy/load balancer terminating SSL.
*   **Rate Limiting**: If applicable at the WebSocket level (e.g., too many messages per second from one client), it might be handled by FastAPI middleware or the reverse proxy.
*   **Input Sanitization**: While Yjs updates are binary, any textual data within presence updates or other messages should be treated with care if displayed to other users, though direct XSS from Yjs content is unlikely if clients render it correctly.
*   **Denial of Service**: Max WebSocket message size (`MAX_WEBSOCKET_MESSAGE_SIZE`) should be configured to prevent overly large messages. Connection limits might be enforced by the ASGI server or reverse proxy.
*   **Redis Security**: If Redis is password-protected, the password must be securely managed (`settings.REDIS_PASSWORD`). Network access to Redis should be restricted.

This SDS provides a comprehensive design for the `CreativeFlow.CollaborationService`.