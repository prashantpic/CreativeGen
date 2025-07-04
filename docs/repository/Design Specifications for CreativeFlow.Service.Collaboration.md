# Software Design Specification (SDS) for CreativeFlow.Service.Collaboration

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.Service.Collaboration` repository. This service is a core backend component responsible for enabling real-time, multi-user collaborative editing of creative documents. It manages WebSocket connections, synchronizes document states using Conflict-free Replicated Data Types (CRDTs), and handles user presence.

### 1.2. Scope
The scope of this document is limited to the design and implementation of the `CreativeFlow.Service.Collaboration` microservice. This includes:
-   WebSocket server setup and connection management.
-   CRDT-based document state synchronization using the Yjs library.
-   Real-time user presence management.
-   Persistence of document states to a PostgreSQL database.
-   Integration with Redis for presence and session management.
-   Authentication of WebSocket connections via JWT.

### 1.3. Technology Stack
-   **Language:** TypeScript 5.5.2
-   **Runtime:** Node.js 20.15.0
-   **Framework:** Express.js 4.19.2
-   **Real-time Communication:** Socket.IO 4.7.5
-   **CRDT Library:** Yjs 13.6.14
-   **Database Client (PostgreSQL):** `pg`
-   **Cache/PubSub Client (Redis):** `ioredis` 5.4.1
-   **Containerization:** Docker

## 2. Architectural Design

### 2.1. System Architecture
This service follows a **Layered Architecture** within a broader **Microservices** ecosystem. This approach promotes separation of concerns, testability, and maintainability.

-   **Interfaces Layer:** The outermost layer, responsible for handling network protocols. It includes the HTTP server and the Socket.IO adapter that receives events from clients. It translates network requests into application-level commands.
-   **Application Layer:** Contains the application-specific business rules and use cases. It orchestrates the domain layer objects to fulfill requests initiated from the interfaces layer. It is unaware of the underlying database or network specifics.
-   **Domain Layer:** The core of the service. It contains the enterprise-wide business logic and state. This layer includes domain entities (`Participant`), aggregate roots (`CollaborationSession`), and repository interfaces (`ICollaborationSessionRepository`, `IPresenceRepository`). It has no dependencies on other layers.
-   **Infrastructure Layer:** Provides concrete implementations of the interfaces defined in the domain layer (e.g., repositories) and handles communication with external systems like databases (PostgreSQL), caches (Redis), and other services.

### 2.2. Data Flow
1.  A client (web or mobile app) establishes a WebSocket connection with the Collaboration Service, providing a JWT for authentication.
2.  The client emits a `join-session` event with a `documentId`.
3.  The `SocketIoAdapter` receives the event and invokes the `JoinSessionUseCase`.
4.  The use case interacts with the `CollaborationSessionRepository` (PostgreSQL) to load the document's latest state snapshot and the `PresenceRepository` (Redis) to update the user's presence.
5.  A `CollaborationSession` aggregate instance is created or retrieved in memory. The server sends the current document state back to the joining client.
6.  When a client makes a change, it emits a `document-update` event with a CRDT update payload.
7.  The `SocketIoAdapter` routes this to the `ApplyDocumentUpdateUseCase`.
8.  The use case applies the update to the in-memory `CollaborationSession` aggregate.
9.  The `SocketIoAdapter` broadcasts the update to all other participants in the same session.
10. Periodically, or when the last user leaves, the `CollaborationSessionRepository` saves a new snapshot of the document state to PostgreSQL.

## 3. Core Concepts

### 3.1. Collaboration Session
A `CollaborationSession` represents a live, multi-user editing session for a single document. It is managed in memory for high performance and is uniquely identified by the `documentId`. It encapsulates the shared document state.

### 3.2. CRDT (Yjs)
The shared document state is managed by a `Y.Doc` instance from the Yjs library. Yjs ensures that all changes (updates) from different users can be merged automatically and convergently, which is the foundation for handling both real-time and offline edits (`REQ-019.1`).

### 3.3. Presence
Presence refers to the real-time status of users within a session (i.e., who is currently active in which document). This data is volatile and managed in Redis for fast access and automatic expiration of stale connections.

### 3.4. Persistence
To ensure durability, the in-memory state of a `Y.Doc` is periodically saved to a PostgreSQL database as a binary snapshot. This strategy balances real-time performance with data safety, avoiding database writes on every keystroke.

## 4. Component Specification

This section details the design of each file within the repository structure.

---

### `package.json`
-   **Purpose:** To manage project dependencies and define scripts.
-   **Dependencies:**
    -   `express`: Web framework.
    -   `socket.io`: Real-time communication server.
    -   `yjs`: CRDT library for document synchronization.
    -   `ioredis`: High-performance Redis client.
    -   `pg`: PostgreSQL client.
    -   `typescript`: Language transpiler.
    -   `ts-node-dev`: Development server with live reload.
    -   `@types/*`: Type definitions for all libraries.
    -   `jsonwebtoken`, `@types/jsonwebtoken`: For JWT validation.
    -   `dotenv`: For environment variable management.
    -   `jest`, `ts-jest`, `@types/jest`: For unit/integration testing.
-   **Scripts:**
    -   `start`: `node dist/main.js` - Runs the compiled production server.
    -   `dev`: `ts-node-dev --respawn src/main.ts` - Runs the development server.
    -   `build`: `tsc` - Compiles TypeScript to JavaScript.
    -   `test`: `jest` - Runs all tests.

---

### `src/domain/collaborationSession.ts`
-   **Purpose:** Aggregate root representing the shared state of a document.
-   **Dependencies:** `yjs`, `Participant`.
-   **Class: `CollaborationSession`**
    -   **Properties:**
        -   `readonly id: string`: Unique identifier for the session (same as `documentId`).
        -   `private doc: Y.Doc`: The core Yjs document instance holding the shared state.
        -   `private participants: Map<string, Participant>`: A map of connected participants, keyed by `userId`.
    -   **Constructor:** `constructor(id: string, snapshot?: Uint8Array)`
        -   Initializes `id` and `participants`.
        -   Creates a new `Y.Doc` instance.
        -   If a `snapshot` is provided, it applies it to the `doc` using `Y.applyUpdate(this.doc, snapshot)`.
    -   **Methods:**
        -   `addParticipant(participant: Participant): void`: Adds a participant to the `participants` map.
        -   `removeParticipant(userId: string): void`: Removes a participant from the map. Returns the removed participant if found.
        -   `getParticipant(userId: string): Participant | undefined`: Retrieves a participant.
        -   `getParticipantCount(): number`: Returns the number of active participants.
        -   `applyUpdate(update: Uint8Array, transactionOrigin: any): void`: Applies a CRDT update to the internal `Y.Doc` using `Y.applyUpdate`. The `transactionOrigin` is used to identify the source of the update to prevent echoing back to the sender.
        -   `getStateVector(): Uint8Array`: Returns the state vector of the document using `Y.encodeStateVector(this.doc)`.
        -   `getDiff(stateVector: Uint8Array): Uint8Array`: Creates a differential update for a client based on their provided `stateVector`, using `Y.encodeStateAsUpdate(this.doc, stateVector)`.
        -   `getSnapshot(): Uint8Array`: Creates a full snapshot of the document state using `Y.encodeStateAsUpdate(this.doc)`.

---

### `src/domain/participant.ts`
-   **Purpose:** Entity representing a user in a session.
-   **Class: `Participant`**
    -   **Properties:**
        -   `readonly userId: string`: The unique ID of the user.
        -   `readonly socketId: string`: The unique ID of their current WebSocket connection.
        -   `presenceState: Record<string, any>`: An object for cursor position or other presence-related metadata.

---

### `src/domain/repositories/iCollaborationSessionRepository.ts`
-   **Purpose:** Defines the contract for session persistence.
-   **Interface: `ICollaborationSessionRepository`**
    -   **Methods:**
        -   `findSnapshotById(documentId: string): Promise<Uint8Array | null>`: Retrieves the latest document snapshot from persistence.
        -   `save(documentId: string, snapshot: Uint8Array): Promise<void>`: Saves or updates the document snapshot.
        -   `delete(documentId: string): Promise<void>`: Deletes a document session from persistence.

---

### `src/domain/repositories/iPresenceRepository.ts`
-   **Purpose:** Defines the contract for presence management.
-   **Interface: `IPresenceRepository`**
    -   **Methods:**
        -   `setUserPresence(documentId: string, participant: Participant): Promise<void>`: Marks a user as active in a document.
        -   `removeUserPresence(documentId: string, userId: string): Promise<void>`: Removes a user's presence.
        -   `getPresentUsers(documentId: string): Promise<Participant[]>`: Gets all active users in a document.
        -   `findDocumentIdForSocket(socketId: string): Promise<string | null>`: Finds which document a socket is associated with.
        -   `trackSocket(socketId: string, userId: string, documentId: string): Promise<void>`: Associates a socket ID with a user and document for quick lookup on disconnect.
        -   `untrackSocket(socketId: string): Promise<{ userId: string; documentId: string } | null>`: Removes the socket tracking entry.

---

### `src/application/sessionManagerService.ts`
-   **Purpose:** Application service to manage the lifecycle of in-memory `CollaborationSession` instances.
-   **Dependencies:** `ICollaborationSessionRepository`.
-   **Class: `SessionManagerService`**
    -   **Properties:**
        -   `private activeSessions: Map<string, CollaborationSession>`: In-memory cache of active sessions.
        -   `private sessionRepository: ICollaborationSessionRepository`: Persistence repository.
        -   `private persistenceTimers: Map<string, NodeJS.Timeout>`: Timers for debouncing persistence saves.
    -   **Methods:**
        -   `getSession(documentId: string): Promise<CollaborationSession>`: Retrieves a session. If not in memory, loads it from the repository. If not in the repository, creates a new one. Caches it in `activeSessions`.
        -   `applyUpdate(documentId: string, update: Uint8Array, origin: any): Promise<void>`: Gets the session, applies the update, and schedules a persistence save.
        -   `schedulePersistence(documentId: string): void`: Manages a debounced save operation. If a timer for a `documentId` already exists, it resets it. Otherwise, it sets a new timer (e.g., for 10 seconds). When the timer fires, it calls `persistSession`.
        -   `persistSession(documentId: string): Promise<void>`: Retrieves the session from memory, gets its snapshot, and saves it using the repository.
        -   `closeSessionIfEmpty(documentId: string): Promise<void>`: Checks if a session has any participants. If not, it persists the session one last time and removes it from the `activeSessions` map to free up memory.

---

### `src/infrastructure/persistence/postgresql/collaborationSessionRepository.ts`
-   **Purpose:** PostgreSQL implementation for session persistence.
-   **Dependencies:** `pg` (Node-Postgres client), `ICollaborationSessionRepository`.
-   **Class: `PostgresCollaborationSessionRepository`**
    -   Implements `ICollaborationSessionRepository`.
    -   **Methods:**
        -   `findSnapshotById(documentId: string)`: `SELECT document_state FROM collaboration_documents WHERE id = $1`. Returns the `document_state` as a `Uint8Array`.
        -   `save(documentId: string, snapshot: Uint8Array)`: Performs an `INSERT ... ON CONFLICT (id) DO UPDATE SET document_state = EXCLUDED.document_state, updated_at = NOW()`.
        -   `delete(documentId: string)`: `DELETE FROM collaboration_documents WHERE id = $1`.

---

### `src/infrastructure/persistence/redis/presenceRepository.ts`
-   **Purpose:** Redis implementation for presence management.
-   **Dependencies:** `ioredis`, `IPresenceRepository`.
-   **Class: `RedisPresenceRepository`**
    -   Implements `IPresenceRepository`.
    -   Uses Redis Hashes and simple keys with TTLs.
    -   **Methods:**
        -   `setUserPresence`: Uses `HSET` on a key like `presence:${documentId}` with the `userId` as the field and serialized `Participant` data as the value.
        -   `removeUserPresence`: Uses `HDEL` to remove the `userId` field from the hash.
        -   `getPresentUsers`: Uses `HGETALL` on `presence:${documentId}` and deserializes the values.
        -   `findDocumentIdForSocket`: Uses `GET` on a key like `socket:${socketId}`.
        -   `trackSocket`: Uses `SET` on `socket:${socketId}` with a value like `${userId}:${documentId}` and a TTL (e.g., 24 hours).
        -   `untrackSocket`: Uses `GET` and then `DEL` on the `socket:${socketId}` key.

---

### `src/infrastructure/realtime/socketIoAdapter.ts`
-   **Purpose:** Bridge between Socket.IO and the application layer.
-   **Dependencies:** `socket.io`, `http.Server`, `SessionManagerService`, `IPresenceRepository`, and an `AuthService` for JWT validation.
-   **Class: `SocketIoAdapter`**
    -   **Methods:**
        -   `initialize(httpServer, authService, sessionManager, presenceRepo)`: Sets up the Socket.IO server, attaches it to the HTTP server, and configures middleware and event handlers.
        -   **Middleware (`io.use`)**:
            -   Extracts JWT from `socket.handshake.auth.token`.
            -   Calls `authService.verifyToken()` to validate it and get user details (`userId`).
            -   Attaches `userId` to the `socket` object for later use. Rejects connection if auth fails.
        -   **Connection Handler (`io.on('connection', ...)`):**
            -   **`join-session` handler:**
                1.  Receives `{ documentId: string }`.
                2.  Calls `sessionManager.getSession(documentId)`.
                3.  Creates a `Participant` instance.
                4.  Adds participant to the session aggregate.
                5.  Calls `presenceRepo.setUserPresence` and `presenceRepo.trackSocket`.
                6.  Joins the socket to a room named after the `documentId`.
                7.  Emits `session-joined` back to the client with the full document state (`session.getSnapshot()`) and the list of current participants.
                8.  Broadcasts a `user-joined` event to the room (excluding the sender).
            -   **`document-update` handler:**
                1.  Receives `{ documentId: string, update: Uint8Array }`.
                2.  Calls `sessionManager.applyUpdate(documentId, update, socket.id)`.
                3.  Broadcasts the `update` to the room (excluding the sender) using `socket.to(documentId).emit('document-update', update)`.
            -   **`sync-request` handler:**
                1.  Receives `{ documentId: string, stateVector: Uint8Array }`.
                2.  Calls `sessionManager.getSession(documentId)`.
                3.  Calculates the diff using `session.getDiff(stateVector)`.
                4.  Emits `sync-reply` back to the client with the diff.
            -   **`disconnect` handler:**
                1.  Calls `presenceRepo.untrackSocket(socket.id)` to get the `userId` and `documentId`.
                2.  If found, calls `presenceRepo.removeUserPresence`.
                3.  Calls `sessionManager.getSession` and then `session.removeParticipant`.
                4.  Broadcasts a `user-left` event to the room.
                5.  Calls `sessionManager.closeSessionIfEmpty(documentId)`.

---

### `src/interfaces/http/server.ts`
-   **Purpose:** Main server setup.
-   **Dependencies:** `express`, `http`, `SocketIoAdapter`, `dotenv`.
-   **Logic:**
    -   Load environment variables using `dotenv.config()`.
    -   Create an Express application instance.
    -   Define a `/health` GET endpoint that returns `{ status: 'OK' }` with a 200 status code.
    -   Create an `http.Server` from the Express app.
    -   Instantiate and initialize the `SocketIoAdapter`, passing it the `http.Server`.
    -   Start the server listening on `process.env.PORT || 3000`.

---

### `src/main.ts`
-   **Purpose:** Application entry point and Dependency Injection.
-   **Logic (Conceptual):**
    typescript
    // 1. Initialize DB and Redis clients
    const pgClient = new PostgresClient(process.env.POSTGRES_CONNECTION_STRING);
    const redisClient = new RedisClient(process.env.REDIS_URL);

    // 2. Instantiate Infrastructure Repositories
    const sessionRepository = new PostgresCollaborationSessionRepository(pgClient);
    const presenceRepository = new RedisPresenceRepository(redisClient);

    // 3. Instantiate Application Services
    const sessionManager = new SessionManagerService(sessionRepository);
    const authService = new AuthService(process.env.JWT_SECRET); // Mock/Stub for now

    // 4. Instantiate and Start the Server/Adapter
    const httpServer = createHttpServer(); // from server.ts
    const socketAdapter = new SocketIoAdapter();
    socketAdapter.initialize(httpServer, authService, sessionManager, presenceRepository);

    startServer(httpServer);
    

## 5. Real-time Communication Protocol (Socket.IO Events)

### 5.1. Client-to-Server Events
-   **`join-session`**:
    -   **Payload:** `{ documentId: string }`
    -   **Action:** Joins the user to the specified document's session.
-   **`document-update`**:
    -   **Payload:** `{ documentId: string, update: Uint8Array }`
    -   **Action:** Submits a CRDT update from the client.
-   **`sync-request`**:
    -   **Payload:** `{ documentId: string, stateVector: Uint8Array }`
    -   **Action:** Requests a differential update based on the client's current state vector.
-   **`presence-update`**:
    -   **Payload:** `{ documentId: string, presenceState: Record<string, any> }`
    -   **Action:** Updates the user's presence metadata (e.g., cursor position).

### 5.2. Server-to-Client Events
-   **`session-joined`**:
    -   **Payload:** `{ documentState: Uint8Array, participants: Participant[] }`
    -   **Action:** Confirms successful session join and provides the initial document state and participant list. Sent only to the joining client.
-   **`document-update`**:
    -   **Payload:** `Uint8Array` (the update data)
    -   **Action:** Broadcasts a document change to all clients in the room (except the sender).
-   **`sync-reply`**:
    -   **Payload:** `Uint8Array` (the differential update)
    -   **Action:** Sends a diff update to a specific client in response to a `sync-request`.
-   **`user-joined`**:
    -   **Payload:** `Participant`
    -   **Action:** Notifies clients in a room that a new user has joined.
-   **`user-left`**:
    -   **Payload:** `{ userId: string }`
    -   **Action:** Notifies clients in a room that a user has left.
-   **`presence-update`**:
    -   **Payload:** `{ userId: string, presenceState: Record<string, any> }`
    -   **Action:** Broadcasts a change in a user's presence state.
-   **`session-error`**:
    -   **Payload:** `{ message: string, code: string }`
    -   **Action:** Communicates an error (e.g., auth failure, invalid document) to a client.

## 6. Configuration
The service will be configured via environment variables. A `.env.example` file will be provided.
-   `PORT`: The port for the HTTP/Socket.IO server to listen on.
-   `POSTGRES_CONNECTION_STRING`: The connection string for the PostgreSQL database.
-   `REDIS_URL`: The connection URL for the Redis server.
-   `JWT_SECRET`: The secret key for verifying JWTs.
-   `PERSISTENCE_DEBOUNCE_MS`: Debounce time in milliseconds for saving document snapshots (e.g., `10000`).
-   `PRESENCE_TTL_SECONDS`: Time-to-live for user presence entries in Redis (e.g., `60`).