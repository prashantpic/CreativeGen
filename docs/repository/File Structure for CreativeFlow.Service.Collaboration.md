# Specification

# 1. Files

- **Path:** package.json  
**Description:** Defines the project metadata, dependencies, and scripts for the Real-time Collaboration Service. Includes dependencies like Express, Socket.IO, Yjs, Redis client, and PostgreSQL client.  
**Template:** Node.js Package  
**Dependency Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project setup and dependency management
    
**Requirement Ids:**
    
    
**Purpose:** To manage project dependencies and define scripts for running, testing, and building the service.  
**Logic Description:** Contains scripts for 'start', 'dev', 'build', 'test'. Lists dependencies such as 'express', 'socket.io', 'yjs', 'redis', 'pg', 'typescript', '@types/node', 'ts-node-dev', etc.  
**Documentation:**
    
    - **Summary:** Standard Node.js package manifest file. It lists all production and development dependencies required to build and run the collaboration service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** tsconfig.json  
**Description:** TypeScript compiler configuration for the service. Defines compiler options like target ECMAScript version, module system, strict type-checking rules, and output directory.  
**Template:** TypeScript Configuration  
**Dependency Level:** 0  
**Name:** tsconfig  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - TypeScript language configuration
    
**Requirement Ids:**
    
    
**Purpose:** To ensure consistent and strict type-checking and configure the TypeScript compilation process for the project.  
**Logic Description:** Sets 'target' to a modern ES version, 'module' to 'CommonJS', enables 'strict' mode, specifies 'outDir' to './dist', and 'rootDir' to './src'. Includes path aliases for cleaner imports.  
**Documentation:**
    
    - **Summary:** Configuration file for the TypeScript compiler (tsc). Governs how TypeScript files are transpiled into JavaScript.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** Dockerfile  
**Description:** Dockerfile for building a production-ready container image of the Collaboration Service. It defines a multi-stage build to create a small, optimized final image.  
**Template:** Docker Template  
**Dependency Level:** 0  
**Name:** Dockerfile  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization of the service
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To create a standardized, portable, and isolated environment for deploying the collaboration service.  
**Logic Description:** Uses a multi-stage build. The first stage ('builder') installs dependencies and compiles TypeScript to JavaScript. The second, final stage copies only the compiled JavaScript and production node_modules into a slim Node.js base image. Exposes the application port and defines the CMD to start the server.  
**Documentation:**
    
    - **Summary:** Instructions for Docker to build a container image for the application. This ensures consistent deployment across different environments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Deployment
    
- **Path:** src/domain/collaborationSession.ts  
**Description:** The core aggregate root for a real-time collaboration session. Encapsulates the CRDT document state (Y.Doc) and manages the list of active participants. It enforces the business rules of a session.  
**Template:** TypeScript Class  
**Dependency Level:** 1  
**Name:** CollaborationSession  
**Type:** AggregateRoot  
**Relative Path:** domain/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - DDD Aggregate
    - Domain Model
    
**Members:**
    
    - **Name:** id  
**Type:** string  
**Attributes:** private|readonly  
    - **Name:** documentId  
**Type:** string  
**Attributes:** private|readonly  
    - **Name:** doc  
**Type:** Y.Doc  
**Attributes:** private  
    - **Name:** participants  
**Type:** Map<string, Participant>  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** addParticipant  
**Parameters:**
    
    - participant: Participant
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** removeParticipant  
**Parameters:**
    
    - userId: string
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** applyUpdate  
**Parameters:**
    
    - update: Uint8Array
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** getStateVector  
**Parameters:**
    
    
**Return Type:** Uint8Array  
**Attributes:** public  
    - **Name:** getDiff  
**Parameters:**
    
    - stateVector: Uint8Array
    
**Return Type:** Uint8Array  
**Attributes:** public  
    - **Name:** getSnapshot  
**Parameters:**
    
    
**Return Type:** Uint8Array  
**Attributes:** public  
    
**Implemented Features:**
    
    - CRDT State Management
    - Participant Management
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** To represent the state and behavior of a single collaborative document session, acting as the consistency boundary.  
**Logic Description:** This class holds a Y.Doc instance. The applyUpdate method uses Y.applyUpdate to merge changes. The add/remove participant methods manage the internal map of connected users. It provides methods to get the current state vector or a diff based on a client's state vector, essential for synchronization. It's unaware of network protocols.  
**Documentation:**
    
    - **Summary:** This is the central domain model for collaboration. It manages the shared document state using Yjs and tracks participants, enforcing session-specific invariants.
    
**Namespace:** CreativeFlow.Collaboration.Domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/domain/participant.ts  
**Description:** Represents a user participating in a collaboration session. Holds user-specific information relevant to the session, like their user ID and presence state.  
**Template:** TypeScript Class  
**Dependency Level:** 1  
**Name:** Participant  
**Type:** Entity  
**Relative Path:** domain/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - DDD Entity
    
**Members:**
    
    - **Name:** userId  
**Type:** string  
**Attributes:** public|readonly  
    - **Name:** socketId  
**Type:** string  
**Attributes:** public  
    - **Name:** presenceState  
**Type:** string  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Participant State
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** To model a user within the context of a collaboration session, tracking their connection and state.  
**Logic Description:** A simple data-holding class representing a user in a session. It is uniquely identified by the userId within the CollaborationSession aggregate.  
**Documentation:**
    
    - **Summary:** A domain entity that captures the identity and session-specific state of a user in a collaborative context.
    
**Namespace:** CreativeFlow.Collaboration.Domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/domain/repositories/iCollaborationSessionRepository.ts  
**Description:** Interface defining the contract for persisting and retrieving CollaborationSession aggregates. This abstracts the data storage mechanism from the domain logic.  
**Template:** TypeScript Interface  
**Dependency Level:** 2  
**Name:** ICollaborationSessionRepository  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - Dependency Inversion
    
**Members:**
    
    
**Methods:**
    
    - **Name:** findById  
**Parameters:**
    
    - documentId: string
    
**Return Type:** Promise<CollaborationSession | null>  
**Attributes:**   
    - **Name:** save  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** Promise<void>  
**Attributes:**   
    - **Name:** create  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** Promise<void>  
**Attributes:**   
    
**Implemented Features:**
    
    - Session Persistence Contract
    
**Requirement Ids:**
    
    - REQ-013
    - REQ-019.1
    
**Purpose:** To define how collaboration sessions are stored and retrieved, decoupling the domain from specific database technologies.  
**Logic Description:** Declares methods for core persistence operations. findById will retrieve a session's state, likely its document snapshot. save will update or persist the current state of a session's document.  
**Documentation:**
    
    - **Summary:** This interface provides the abstraction for data access operations related to the CollaborationSession aggregate, allowing for different persistence implementations.
    
**Namespace:** CreativeFlow.Collaboration.Domain.Repositories  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/domain/repositories/iPresenceRepository.ts  
**Description:** Interface defining the contract for managing user presence information within collaborative sessions, such as which users are active in which documents.  
**Template:** TypeScript Interface  
**Dependency Level:** 2  
**Name:** IPresenceRepository  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setUserPresence  
**Parameters:**
    
    - documentId: string
    - userId: string
    - metadata: object
    
**Return Type:** Promise<void>  
**Attributes:**   
    - **Name:** removeUserPresence  
**Parameters:**
    
    - documentId: string
    - userId: string
    
**Return Type:** Promise<void>  
**Attributes:**   
    - **Name:** getPresentUsers  
**Parameters:**
    
    - documentId: string
    
**Return Type:** Promise<Participant[]>  
**Attributes:**   
    
**Implemented Features:**
    
    - Presence Management Contract
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** To abstract the storage and retrieval of real-time presence data, which is often handled by a fast in-memory store like Redis.  
**Logic Description:** Defines methods to add, remove, and query the list of active users for a specific document. This is crucial for showing collaborator avatars and cursors in the UI.  
**Documentation:**
    
    - **Summary:** This interface outlines the operations for managing the presence state of users in a session, typically backed by a fast, distributed cache.
    
**Namespace:** CreativeFlow.Collaboration.Domain.Repositories  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/application/use-cases/joinSession.ts  
**Description:** Application use case for a user joining a collaboration session. It orchestrates finding or creating a session, adding the participant, and setting their presence.  
**Template:** TypeScript Function/Class  
**Dependency Level:** 3  
**Name:** JoinSessionUseCase  
**Type:** UseCase  
**Relative Path:** application/use-cases/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - Application Service
    - CommandPattern
    
**Members:**
    
    - **Name:** sessionRepo  
**Type:** ICollaborationSessionRepository  
**Attributes:** private|readonly  
    - **Name:** presenceRepo  
**Type:** IPresenceRepository  
**Attributes:** private|readonly  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - command: { documentId: string, userId: string, socketId: string }
    
**Return Type:** Promise<CollaborationSession>  
**Attributes:** public  
    
**Implemented Features:**
    
    - User joining a session
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** To handle the complete business logic flow when a new participant connects to a collaborative session.  
**Logic Description:** The execute method will first try to find an existing session for the documentId using the session repository. If not found, it creates a new CollaborationSession instance. It then creates a new Participant and adds them to the session aggregate. It updates the presence information using the presence repository. Finally, it saves the session state if it's new and returns the session object.  
**Documentation:**
    
    - **Summary:** This use case orchestrates all necessary steps for a user to join a collaborative document session, including loading/creating the session, updating presence, and preparing the state for the new user.
    
**Namespace:** CreativeFlow.Collaboration.Application.UseCases  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/application/use-cases/applyDocumentUpdate.ts  
**Description:** Application use case for applying a document update from a client. It retrieves the session, applies the CRDT update, and implicitly relies on other mechanisms to persist and broadcast the change.  
**Template:** TypeScript Function/Class  
**Dependency Level:** 3  
**Name:** ApplyDocumentUpdateUseCase  
**Type:** UseCase  
**Relative Path:** application/use-cases/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - Application Service
    - CommandPattern
    
**Members:**
    
    - **Name:** sessionRepo  
**Type:** ICollaborationSessionRepository  
**Attributes:** private|readonly  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - command: { documentId: string, update: Uint8Array }
    
**Return Type:** Promise<void>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Real-time document editing
    
**Requirement Ids:**
    
    - REQ-013
    - REQ-019.1
    - Section 5.3.2
    
**Purpose:** To process an incoming CRDT update for a specific document session, ensuring the change is applied to the shared state.  
**Logic Description:** The execute method retrieves the relevant CollaborationSession from the repository. It validates that the session exists. It then calls the applyUpdate method on the session aggregate, passing the CRDT update data. It does not directly save or broadcast; those are separate concerns. This use case is a key part of the real-time editing loop.  
**Documentation:**
    
    - **Summary:** This use case handles the core logic of applying a client's change to a document's shared CRDT state. It acts as the bridge between the network interface and the domain model for edits.
    
**Namespace:** CreativeFlow.Collaboration.Application.UseCases  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** src/infrastructure/persistence/postgresql/collaborationSessionRepository.ts  
**Description:** PostgreSQL implementation of the ICollaborationSessionRepository. Handles storing and retrieving the CRDT document snapshots to/from the database.  
**Template:** TypeScript Class  
**Dependency Level:** 3  
**Name:** PostgresCollaborationSessionRepository  
**Type:** Repository  
**Relative Path:** infrastructure/persistence/postgresql/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** dbClient  
**Type:** PostgresClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** findById  
**Parameters:**
    
    - documentId: string
    
**Return Type:** Promise<CollaborationSession | null>  
**Attributes:** public  
    - **Name:** save  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** Promise<void>  
**Attributes:** public  
    - **Name:** create  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** Promise<void>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Session State Persistence
    
**Requirement Ids:**
    
    - REQ-013
    - REQ-019.1
    
**Purpose:** To provide concrete data access logic for collaboration sessions using a PostgreSQL database.  
**Logic Description:** Implements the ICollaborationSessionRepository interface. The findById method queries the database for a document snapshot. If found, it creates a new Y.Doc, applies the snapshot, and returns a new CollaborationSession instance. The save method gets the latest snapshot from the session's Y.Doc and performs an UPSERT operation into the database table.  
**Documentation:**
    
    - **Summary:** This repository implementation connects the domain's need for session persistence with the technical details of a PostgreSQL database, managing the storage of document snapshots.
    
**Namespace:** CreativeFlow.Collaboration.Infrastructure.Persistence  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/infrastructure/persistence/redis/presenceRepository.ts  
**Description:** Redis implementation of the IPresenceRepository. Uses Redis data structures (like Hashes or Sets) to efficiently manage and query user presence in real-time.  
**Template:** TypeScript Class  
**Dependency Level:** 3  
**Name:** RedisPresenceRepository  
**Type:** Repository  
**Relative Path:** infrastructure/persistence/redis/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** redisClient  
**Type:** RedisClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** setUserPresence  
**Parameters:**
    
    - documentId: string
    - userId: string
    - metadata: object
    
**Return Type:** Promise<void>  
**Attributes:** public  
    - **Name:** removeUserPresence  
**Parameters:**
    
    - documentId: string
    - userId: string
    
**Return Type:** Promise<void>  
**Attributes:** public  
    - **Name:** getPresentUsers  
**Parameters:**
    
    - documentId: string
    
**Return Type:** Promise<Participant[]>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Real-time Presence Management
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** To provide a high-performance implementation for tracking which users are currently active in a given document session.  
**Logic Description:** Implements the IPresenceRepository interface using Redis. `setUserPresence` might use a Redis Hash where the key is the document ID and fields are user IDs. `removeUserPresence` deletes a field from the hash. `getPresentUsers` fetches all fields from the hash. A short TTL is used on each entry to automatically clean up stale presences.  
**Documentation:**
    
    - **Summary:** This class leverages Redis for fast, volatile storage of user presence information, which is critical for real-time UI features like collaborator lists.
    
**Namespace:** CreativeFlow.Collaboration.Infrastructure.Persistence  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/infrastructure/realtime/socketIoAdapter.ts  
**Description:** The main Socket.IO adapter that configures the server, handles connection/disconnection events, and routes incoming socket events to the appropriate application use cases.  
**Template:** TypeScript Class  
**Dependency Level:** 4  
**Name:** SocketIoAdapter  
**Type:** Adapter  
**Relative Path:** infrastructure/realtime/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** io  
**Type:** SocketIOServer  
**Attributes:** private  
    - **Name:** sessionUseCases  
**Type:** CollaborationAppService  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** initialize  
**Parameters:**
    
    - httpServer: http.Server
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** handleConnection  
**Parameters:**
    
    - socket: Socket
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** broadcastUpdate  
**Parameters:**
    
    - documentId: string
    - update: Uint8Array
    - senderSocketId: string
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - WebSocket Connection Management
    - Real-time Event Routing
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** To encapsulate all Socket.IO-specific logic, acting as the primary bridge between the network and the application layer.  
**Logic Description:** Initializes a Socket.IO server attached to the main HTTP server. The `handleConnection` method sets up listeners for events like `join-session`, `document-update`, and `disconnect` on each new socket. These listeners authenticate the request (e.g., JWT in handshake), then invoke the corresponding application use case. It also provides a method to broadcast updates to all clients in a specific room (document session), excluding the sender.  
**Documentation:**
    
    - **Summary:** This adapter manages the real-time communication layer using Socket.IO. It's responsible for handling client connections and routing messages to the application logic for processing.
    
**Namespace:** CreativeFlow.Collaboration.Infrastructure.Realtime  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/interfaces/http/server.ts  
**Description:** Initializes and starts the Express.js HTTP server. This server's primary role is to provide a host for the Socket.IO server and potentially a health check endpoint.  
**Template:** Node.js Server  
**Dependency Level:** 5  
**Name:** server  
**Type:** Server  
**Relative Path:** interfaces/http/  
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** start  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - HTTP Server Initialization
    
**Requirement Ids:**
    
    
**Purpose:** To create the underlying HTTP server that the WebSocket/Socket.IO server will attach to.  
**Logic Description:** Creates an Express app. Creates an HTTP server from the app. Initializes the SocketIoAdapter with the HTTP server instance. Defines a '/health' endpoint that returns a 200 OK status. Starts listening on the configured port.  
**Documentation:**
    
    - **Summary:** This file sets up the main HTTP server. While the service is primarily real-time, an HTTP server is needed as a base for Socket.IO and for standard operational endpoints like health checks.
    
**Namespace:** CreativeFlow.Collaboration.Interfaces.Http  
**Metadata:**
    
    - **Category:** Interface
    
- **Path:** src/main.ts  
**Description:** The main entry point for the Collaboration Service application. Responsible for dependency injection and starting the server.  
**Template:** Node.js Application Entry  
**Dependency Level:** 6  
**Name:** main  
**Type:** Application  
**Relative Path:**   
**Repository Id:** REPO-SERVICE-COLLABORATION-001  
**Pattern Ids:**
    
    - Dependency Injection
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Bootstrap
    
**Requirement Ids:**
    
    
**Purpose:** To initialize all modules, wire up dependencies (DI container), and launch the application.  
**Logic Description:** This file will instantiate concrete repository implementations (Postgres, Redis), instantiate application use cases with the repositories, initialize the Socket.IO adapter with the use cases, and finally, call the start method on the HTTP server. This is where the application's dependency graph is constructed.  
**Documentation:**
    
    - **Summary:** The bootstrap file for the service. It orchestrates the creation and injection of all necessary dependencies before starting the server.
    
**Namespace:** CreativeFlow.Collaboration  
**Metadata:**
    
    - **Category:** Application
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableDetailedPresence
  - enablePersistenceThrottling
  - enableOfflineConflictUI
  
- **Database Configs:**
  
  - POSTGRES_CONNECTION_STRING
  - REDIS_URL
  


---

