# Specification

# 1. Files

- **Path:** src/creativeflow/collaboration/__init__.py  
**Description:** Makes the 'collaboration' directory a Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:**   
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the collaboration service Python package.  
**Logic Description:** This file can be empty or contain package-level imports.  
**Documentation:**
    
    - **Summary:** Package initializer for the collaboration service.
    
**Namespace:** creativeflow.collaboration  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/collaboration/main.py  
**Description:** Main FastAPI application setup. Initializes the FastAPI app, mounts routers (WebSocket endpoints), and includes global middleware or exception handlers. This is the entry point for the service.  
**Template:** Python FastAPI Main  
**Dependency Level:** 5  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:**   
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - APIGatewayPattern (WebSocket specific)
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** startup_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|private  
**Notes:** Handles application startup logic e.g. initializing Redis connection.  
    - **Name:** shutdown_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|private  
**Notes:** Handles application shutdown logic e.g. closing Redis connection.  
    
**Implemented Features:**
    
    - WebSocket Server Setup
    - Application Lifecycle Management
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Sets up and runs the FastAPI application for the collaboration service, including WebSocket endpoints.  
**Logic Description:** Instantiate FastAPI. Register WebSocket routers from api.websocket_router. Define startup/shutdown event handlers for resource initialization/cleanup (e.g., Redis connection pool). Potentially add global exception handlers or middleware for logging/tracing.  
**Documentation:**
    
    - **Summary:** Entry point for the Collaboration Service. Initializes and configures the FastAPI application, including WebSocket routing.
    
**Namespace:** creativeflow.collaboration  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/core/__init__.py  
**Description:** Initializes the 'core' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** core  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'core' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for the core configuration and dependencies package.
    
**Namespace:** creativeflow.collaboration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/collaboration/core/config.py  
**Description:** Handles application configuration using environment variables or configuration files. Defines settings for Redis, JWT secrets (for auth client), log levels, Yjs parameters.  
**Template:** Python Configuration  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** core  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - ConfigurationProvider
    
**Members:**
    
    - **Name:** REDIS_URL  
**Type:** str  
**Attributes:** public|static  
    - **Name:** AUTH_SERVICE_URL  
**Type:** str  
**Attributes:** public|static  
    - **Name:** JWT_SECRET_KEY  
**Type:** str  
**Attributes:** public|static  
**Notes:** Or mechanism to fetch from secrets manager  
    - **Name:** LOG_LEVEL  
**Type:** str  
**Attributes:** public|static  
    - **Name:** YJS_GC_ENABLED  
**Type:** bool  
**Attributes:** public|static  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** Provides access to application settings and environment variables.  
**Logic Description:** Use Pydantic BaseSettings or a similar library to load configuration from environment variables. Define default values where appropriate. Ensure sensitive information is handled securely, potentially integrating with a secrets manager.  
**Documentation:**
    
    - **Summary:** Manages all application-level configurations, loading them from environment variables or configuration files.
    
**Namespace:** creativeflow.collaboration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/collaboration/core/dependencies.py  
**Description:** Defines reusable FastAPI dependencies, such as for authenticating users via the Auth Service or providing database sessions.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 3  
**Name:** dependencies  
**Type:** Utility  
**Relative Path:** core  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_collaboration_app_service  
**Parameters:**
    
    
**Return Type:** CollaborationAppService  
**Attributes:** async|public  
**Notes:** Provides an instance of CollaborationAppService.  
    - **Name:** get_current_user  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** UserSchema  
**Attributes:** async|public  
**Notes:** Dependency to authenticate user token with Auth Service Client.  
    
**Implemented Features:**
    
    - Dependency Injection for Services
    - User Authentication Hook
    
**Requirement Ids:**
    
    - Section 5.3.2
    
**Purpose:** Provides injectable dependencies for FastAPI route handlers, primarily for service instances and authentication.  
**Logic Description:** Define functions that can be used with FastAPI's `Depends` system. The `get_current_user` dependency will use the `AuthServiceClient` to validate an incoming token (e.g., from WebSocket handshake query params or initial HTTP upgrade request) and return user details. Other dependencies will instantiate and return service classes.  
**Documentation:**
    
    - **Summary:** Contains FastAPI dependency functions for injecting services and handling authentication in route handlers.
    
**Namespace:** creativeflow.collaboration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/collaboration/domain/__init__.py  
**Description:** Initializes the 'domain' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'domain' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for the domain logic package.
    
**Namespace:** creativeflow.collaboration.domain  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/aggregates/__init__.py  
**Description:** Initializes the 'aggregates' sub-package within domain.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/aggregates  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'aggregates' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for domain aggregates.
    
**Namespace:** creativeflow.collaboration.domain.aggregates  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/aggregates/collaboration_session.py  
**Description:** Defines the CollaborationSession aggregate root, SessionId VO, and Participant entity. Manages participants and links to a shared document.  
**Template:** Python Domain Aggregate  
**Dependency Level:** 1  
**Name:** collaboration_session  
**Type:** DomainModel  
**Relative Path:** domain/aggregates  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** SessionId (VO)  
**Type:** UUID  
**Attributes:**   
    - **Name:** Participant (Entity)  
**Type:** object  
**Attributes:**   
**Fields:** user_id: UserId, joined_at: datetime, presence_status: str  
    - **Name:** CollaborationSession (Aggregate)  
**Type:** object  
**Attributes:**   
**Fields:** id: SessionId, document_id: DocumentId, participants: List[Participant], created_at: datetime, ydoc_state: bytes  
    
**Methods:**
    
    - **Name:** CollaborationSession.add_participant  
**Parameters:**
    
    - user_id: UserId
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** CollaborationSession.remove_participant  
**Parameters:**
    
    - user_id: UserId
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** CollaborationSession.is_participant  
**Parameters:**
    
    - user_id: UserId
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** CollaborationSession.update_ydoc_state  
**Parameters:**
    
    - new_state: bytes
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** CollaborationSession.get_ydoc_state  
**Parameters:**
    
    
**Return Type:** bytes  
**Attributes:** public  
    
**Implemented Features:**
    
    - Session Management
    - Participant Tracking
    - CRDT State Persistence (within session)
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Models a real-time collaboration session, its participants, and the associated document's CRDT state.  
**Logic Description:** SessionId is an immutable identifier. Participant tracks user involvement. CollaborationSession is the aggregate root, managing lifecycle of participants and holding the serialized Yjs document state for the session. Methods enforce invariants, e.g., a user cannot be added twice. Raises domain events like ParticipantJoinedEvent, ParticipantLeftEvent.  
**Documentation:**
    
    - **Summary:** Defines the CollaborationSession aggregate, responsible for managing participants and the shared state of a document within a session.
    
**Namespace:** creativeflow.collaboration.domain.aggregates  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/aggregates/shared_document.py  
**Description:** Defines the SharedDocument concept, representing the collaborative document state typically managed by Yjs. Includes DocumentId VO, DocumentChange entity, and ChangeOperation VO for CRDT updates.  
**Template:** Python Domain Model  
**Dependency Level:** 1  
**Name:** shared_document  
**Type:** DomainModel  
**Relative Path:** domain/aggregates  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    - ValueObject
    - CRDTWrapper
    
**Members:**
    
    - **Name:** DocumentId (VO)  
**Type:** UUID  
**Attributes:**   
    - **Name:** ChangeOperation (VO)  
**Type:** object  
**Attributes:**   
**Fields:** type: str, payload: Any  
    - **Name:** DocumentChange (Entity)  
**Type:** object  
**Attributes:**   
**Fields:** user_id: UserId, timestamp: datetime, operations: List[ChangeOperation], yjs_update: bytes  
    - **Name:** SharedDocument (Aggregate)  
**Type:** object  
**Attributes:**   
**Fields:** id: DocumentId, y_doc: YDoc (from y_py), version: int  
    
**Methods:**
    
    - **Name:** SharedDocument.apply_update  
**Parameters:**
    
    - update_payload: bytes
    - originator_id: UserId
    
**Return Type:** bytes  
**Attributes:** public  
**Notes:** Applies a Yjs update and returns the new state or diff.  
    - **Name:** SharedDocument.get_document_state  
**Parameters:**
    
    
**Return Type:** bytes  
**Attributes:** public  
**Notes:** Returns the full Yjs document state.  
    - **Name:** SharedDocument.get_diff  
**Parameters:**
    
    - vector: bytes
    
**Return Type:** bytes  
**Attributes:** public  
**Notes:** Returns Yjs diff from a given state vector.  
    
**Implemented Features:**
    
    - CRDT State Management
    - Change Application
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Manages the CRDT state of a shared document using Yjs, allowing updates and retrieval of state.  
**Logic Description:** SharedDocument encapsulates a Yjs document (`YDoc`). `apply_update` applies a binary Yjs update. `get_document_state` serializes the current YDoc. `get_diff` provides updates based on a client's state vector. Raises DocumentUpdatedEvent. DocumentChange could be used to log specific semantic changes if needed beyond raw Yjs updates.  
**Documentation:**
    
    - **Summary:** Manages the collaborative document state using Yjs. Applies updates and provides current state or diffs.
    
**Namespace:** creativeflow.collaboration.domain.aggregates  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/entities/__init__.py  
**Description:** Initializes the 'entities' sub-package if used separately.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/entities  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'entities' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for domain entities (if not directly within aggregates).
    
**Namespace:** creativeflow.collaboration.domain.entities  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/entities/presence.py  
**Description:** Defines the Presence entity and related value objects like UserId. Manages user presence status within a session.  
**Template:** Python Domain Entity  
**Dependency Level:** 1  
**Name:** presence  
**Type:** DomainModel  
**Relative Path:** domain/entities  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** UserId (VO)  
**Type:** str  
**Attributes:**   
    - **Name:** PresenceStatus (Enum/VO)  
**Type:** str  
**Attributes:**   
**Values:** ['online', 'offline', 'idle']  
    - **Name:** Presence (Entity)  
**Type:** object  
**Attributes:**   
**Fields:** user_id: UserId, session_id: SessionId, status: PresenceStatus, last_seen_at: datetime  
    
**Methods:**
    
    - **Name:** Presence.update_status  
**Parameters:**
    
    - new_status: PresenceStatus
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - User Presence Tracking
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** Models a user's presence status within a specific collaboration session.  
**Logic Description:** The Presence entity tracks the current status (online, offline, idle) of a user within a session. `update_status` changes the status and updates `last_seen_at`. Raises PresenceChangedEvent.  
**Documentation:**
    
    - **Summary:** Represents a user's presence information within a collaboration session.
    
**Namespace:** creativeflow.collaboration.domain.entities  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/events/__init__.py  
**Description:** Initializes the 'events' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/events  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'events' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for domain events package.
    
**Namespace:** creativeflow.collaboration.domain.events  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/events/collaboration_events.py  
**Description:** Defines domain events related to collaboration, such as SessionStarted, ParticipantJoined, DocumentUpdated, PresenceChanged.  
**Template:** Python Domain Events  
**Dependency Level:** 1  
**Name:** collaboration_events  
**Type:** DomainEvent  
**Relative Path:** domain/events  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - DomainEvent
    
**Members:**
    
    - **Name:** BaseEvent  
**Type:** class  
**Attributes:**   
    - **Name:** SessionStartedEvent(BaseEvent)  
**Type:** class  
**Attributes:**   
**Fields:** session_id: SessionId, document_id: DocumentId, user_id: UserId  
    - **Name:** ParticipantJoinedEvent(BaseEvent)  
**Type:** class  
**Attributes:**   
**Fields:** session_id: SessionId, user_id: UserId  
    - **Name:** ParticipantLeftEvent(BaseEvent)  
**Type:** class  
**Attributes:**   
**Fields:** session_id: SessionId, user_id: UserId  
    - **Name:** DocumentUpdatedEvent(BaseEvent)  
**Type:** class  
**Attributes:**   
**Fields:** session_id: SessionId, document_id: DocumentId, update_payload: bytes, originator_id: UserId  
    - **Name:** PresenceChangedEvent(BaseEvent)  
**Type:** class  
**Attributes:**   
**Fields:** session_id: SessionId, user_id: UserId, status: PresenceStatus  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Domain Event Definitions
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Defines data structures for events that occur within the collaboration domain.  
**Logic Description:** Each event class will be a simple data container (e.g., Pydantic model or dataclass) holding relevant information about the event. These events are raised by domain aggregates/services and handled by application event handlers.  
**Documentation:**
    
    - **Summary:** Contains definitions for all domain events specific to the collaboration context.
    
**Namespace:** creativeflow.collaboration.domain.events  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/services/__init__.py  
**Description:** Initializes the 'services' sub-package within domain.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'services' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for domain services.
    
**Namespace:** creativeflow.collaboration.domain.services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/services/crdt_service.py  
**Description:** Domain service for CRDT operations, abstracting y-py library specifics if needed. Handles applying updates to YDocs and generating diffs.  
**Template:** Python Domain Service  
**Dependency Level:** 2  
**Name:** crdt_service  
**Type:** DomainService  
**Relative Path:** domain/services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - DomainService
    - CRDT
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initialize_document  
**Parameters:**
    
    
**Return Type:** YDoc  
**Attributes:** public|static  
    - **Name:** apply_update_to_document  
**Parameters:**
    
    - ydoc: YDoc
    - update_payload: bytes
    
**Return Type:** None  
**Attributes:** public|static  
    - **Name:** encode_state_vector  
**Parameters:**
    
    - ydoc: YDoc
    
**Return Type:** bytes  
**Attributes:** public|static  
    - **Name:** encode_state_as_update  
**Parameters:**
    
    - ydoc: YDoc
    - encoded_target_state_vector: bytes = None
    
**Return Type:** bytes  
**Attributes:** public|static  
    - **Name:** merge_updates  
**Parameters:**
    
    - ydoc: YDoc
    - updates: List[bytes]
    
**Return Type:** None  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - CRDT Operations Abstraction
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Provides a higher-level interface for interacting with the Yjs (y-py) library for CRDT operations.  
**Logic Description:** Wraps y-py functionalities. `initialize_document` creates a new YDoc. `apply_update_to_document` applies a received binary update. `encode_state_vector` gets the current state vector. `encode_state_as_update` gets the full document or a diff based on a target state vector. `merge_updates` applies multiple updates.  
**Documentation:**
    
    - **Summary:** Service layer for CRDT (Yjs) document manipulations, such as applying updates and generating state vectors or diffs.
    
**Namespace:** creativeflow.collaboration.domain.services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/services/conflict_resolution_service.py  
**Description:** Domain service responsible for handling conflict resolution, particularly for merging offline edits as per REQ-019.1. This might involve specific strategies if CRDT auto-merging is insufficient for certain complex changes or business rules.  
**Template:** Python Domain Service  
**Dependency Level:** 2  
**Name:** conflict_resolution_service  
**Type:** DomainService  
**Relative Path:** domain/services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** resolve_offline_edits  
**Parameters:**
    
    - session: CollaborationSession
    - offline_changes: List[DocumentChange]
    
**Return Type:** Tuple[YDoc, List[ResolvedConflict]]  
**Attributes:** public  
**Notes:** Applies offline changes to a session's YDoc, attempting to resolve conflicts.  
    
**Implemented Features:**
    
    - Offline Edit Conflict Resolution
    
**Requirement Ids:**
    
    - REQ-019.1
    
**Purpose:** Implements strategies for resolving conflicts arising from concurrent or offline edits if not automatically handled by CRDTs.  
**Logic Description:** This service takes a current Yjs document state (from CollaborationSession) and a list of offline changes (DocumentChange entities). It attempts to merge these changes. If Yjs handles most conflicts, this service might focus on UI prompts for users if manual intervention is needed, or applying specific business rules for conflict resolution. For REQ-019.1, it ensures offline changes are correctly merged using Yjs principles.  
**Documentation:**
    
    - **Summary:** Handles conflict resolution for collaborative edits, particularly for merging changes made offline by users.
    
**Namespace:** creativeflow.collaboration.domain.services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/repositories/__init__.py  
**Description:** Initializes the 'repositories' sub-package within domain.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/repositories  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'repositories' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for domain repository interfaces.
    
**Namespace:** creativeflow.collaboration.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/domain/repositories/collaboration_repository.py  
**Description:** Defines interfaces for repositories related to collaboration, such as ICollaborationSessionRepository, ISharedDocumentStateRepository, IPresenceRepository.  
**Template:** Python Repository Interface  
**Dependency Level:** 2  
**Name:** collaboration_repository  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** ICollaborationSessionRepository.get_by_id  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** Optional[CollaborationSession]  
**Attributes:** public|abstractmethod  
    - **Name:** ICollaborationSessionRepository.save  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** None  
**Attributes:** public|abstractmethod  
    - **Name:** ICollaborationSessionRepository.delete  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** None  
**Attributes:** public|abstractmethod  
    - **Name:** IPresenceRepository.get_presence  
**Parameters:**
    
    - session_id: SessionId
    - user_id: UserId
    
**Return Type:** Optional[Presence]  
**Attributes:** public|abstractmethod  
    - **Name:** IPresenceRepository.save_presence  
**Parameters:**
    
    - presence: Presence
    
**Return Type:** None  
**Attributes:** public|abstractmethod  
    - **Name:** IPresenceRepository.get_all_in_session  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** List[Presence]  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - Repository Interface Definitions
    
**Requirement Ids:**
    
    - REQ-013
    
**Purpose:** Declares contracts for data access operations related to collaboration sessions, document states, and presence.  
**Logic Description:** Define abstract base classes (ABCs) or protocols for repository interfaces. These specify methods for CRUD operations on CollaborationSession aggregates, SharedDocument states (potentially storing snapshots or full YDoc states if persisted beyond Redis), and Presence entities.  
**Documentation:**
    
    - **Summary:** Interfaces for persisting and retrieving collaboration-related domain aggregates and entities.
    
**Namespace:** creativeflow.collaboration.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/collaboration/application/__init__.py  
**Description:** Initializes the 'application' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'application' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for the application services package.
    
**Namespace:** creativeflow.collaboration.application  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/services/__init__.py  
**Description:** Initializes the 'services' sub-package within application.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'services' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for application services.
    
**Namespace:** creativeflow.collaboration.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/services/collaboration_app_service.py  
**Description:** Application service for handling collaboration use cases. Orchestrates domain logic, interacts with repositories, and dispatches events.  
**Template:** Python Application Service  
**Dependency Level:** 3  
**Name:** collaboration_app_service  
**Type:** ApplicationService  
**Relative Path:** application/services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** session_repo  
**Type:** ICollaborationSessionRepository  
**Attributes:** private  
    - **Name:** presence_repo  
**Type:** IPresenceRepository  
**Attributes:** private  
    - **Name:** crdt_service  
**Type:** CRDTService  
**Attributes:** private  
    - **Name:** conflict_resolver  
**Type:** ConflictResolutionService  
**Attributes:** private  
    - **Name:** broadcaster  
**Type:** WebsocketBroadcaster  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** handle_join_session  
**Parameters:**
    
    - cmd: JoinSessionCommand
    
**Return Type:** SessionStateSchema  
**Attributes:** async|public  
    - **Name:** handle_leave_session  
**Parameters:**
    
    - user_id: UserId
    - session_id: SessionId
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** handle_apply_document_change  
**Parameters:**
    
    - cmd: ApplyDocumentChangeCommand
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** handle_presence_update  
**Parameters:**
    
    - cmd: UpdatePresenceCommand
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** handle_offline_changes  
**Parameters:**
    
    - session_id: SessionId
    - user_id: UserId
    - offline_changes: List[DocumentChangeSchema]
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Related to REQ-019.1  
    
**Implemented Features:**
    
    - Session Joining
    - Change Application
    - Presence Updates
    - Offline Edit Handling
    
**Requirement Ids:**
    
    - REQ-013
    - REQ-019.1
    - Section 5.3.2
    
**Purpose:** Orchestrates use cases like joining a session, applying document changes, and updating presence.  
**Logic Description:** Receives commands. Fetches aggregates from repositories (e.g., CollaborationSession). Invokes domain service methods (e.g., CRDTService, ConflictResolutionService). Saves modified aggregates. Dispatches domain events or directly uses the broadcaster to notify clients. For `handle_join_session`, it might load or create a session, add participant, and return current document state. For `handle_apply_document_change`, it applies Yjs update to the shared document and broadcasts the new state/diff.  
**Documentation:**
    
    - **Summary:** Coordinates collaboration-related operations, acting as a bridge between interface adapters (WebSocket handlers) and the domain layer.
    
**Namespace:** creativeflow.collaboration.application.services  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/commands/__init__.py  
**Description:** Initializes the 'commands' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/commands  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'commands' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for application command DTOs.
    
**Namespace:** creativeflow.collaboration.application.commands  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/commands/collaboration_commands.py  
**Description:** Defines command objects/DTOs for collaboration actions, e.g., JoinSessionCommand, ApplyDocumentChangeCommand.  
**Template:** Python Command DTOs  
**Dependency Level:** 1  
**Name:** collaboration_commands  
**Type:** DTO  
**Relative Path:** application/commands  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - CommandPattern
    - DTO
    
**Members:**
    
    - **Name:** JoinSessionCommand  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** user_id: str, document_id: str  
    - **Name:** ApplyDocumentChangeCommand  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** session_id: str, user_id: str, yjs_update: bytes  
    - **Name:** UpdatePresenceCommand  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** session_id: str, user_id: str, status: str  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Command Definitions
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Represents data for initiating collaboration actions within the application layer.  
**Logic Description:** Simple Pydantic models or dataclasses to carry data for application service methods. These are typically created from incoming WebSocket messages or API requests.  
**Documentation:**
    
    - **Summary:** Data Transfer Objects representing commands for the collaboration application service.
    
**Namespace:** creativeflow.collaboration.application.commands  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/schemas/__init__.py  
**Description:** Initializes the 'schemas' sub-package for Pydantic models.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/schemas  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'schemas' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for Pydantic schemas (DTOs).
    
**Namespace:** creativeflow.collaboration.application.schemas  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/schemas/message_schemas.py  
**Description:** Pydantic schemas for WebSocket message structures (incoming client messages and outgoing server messages).  
**Template:** Python Pydantic Schemas  
**Dependency Level:** 1  
**Name:** message_schemas  
**Type:** DTO  
**Relative Path:** application/schemas  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - DTO
    
**Members:**
    
    - **Name:** ClientMessageType (Enum)  
**Type:** str  
**Attributes:**   
    - **Name:** ServerMessageType (Enum)  
**Type:** str  
**Attributes:**   
    - **Name:** BaseMessage  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** type: str, payload: Any  
    - **Name:** ClientJoinSessionMessage  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** document_id: str  
    - **Name:** ClientDocumentUpdateMessage  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** yjs_update: bytes  
    - **Name:** ServerSessionStateMessage  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** document_state: bytes, participants: List[dict]  
    - **Name:** ServerDocumentUpdateBroadcastMessage  
**Type:** PydanticBaseModel  
**Attributes:**   
**Fields:** yjs_update: bytes, originator_id: str  
    
**Methods:**
    
    
**Implemented Features:**
    
    - WebSocket Message Contracts
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Defines the structure of messages exchanged over WebSockets between clients and the server.  
**Logic Description:** Use Pydantic models for strict validation and serialization/deserialization of WebSocket messages. Define different schemas for various message types (e.g., join, leave, document update, presence update, error).  
**Documentation:**
    
    - **Summary:** Contains Pydantic models defining the schemas for messages sent and received via WebSockets.
    
**Namespace:** creativeflow.collaboration.application.schemas  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/event_handlers/__init__.py  
**Description:** Initializes the 'event_handlers' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** application/event_handlers  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'event_handlers' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for application-level domain event handlers.
    
**Namespace:** creativeflow.collaboration.application.event_handlers  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/application/event_handlers/domain_event_handlers.py  
**Description:** Contains handlers for domain events. These handlers might trigger broadcasting messages to clients or other application logic.  
**Template:** Python Event Handlers  
**Dependency Level:** 3  
**Name:** domain_event_handlers  
**Type:** EventHandler  
**Relative Path:** application/event_handlers  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - ObserverPattern
    - EventHandler
    
**Members:**
    
    - **Name:** broadcaster  
**Type:** WebsocketBroadcaster  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** handle_document_updated_event  
**Parameters:**
    
    - event: DocumentUpdatedEvent
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** handle_participant_joined_event  
**Parameters:**
    
    - event: ParticipantJoinedEvent
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** handle_participant_left_event  
**Parameters:**
    
    - event: ParticipantLeftEvent
    
**Return Type:** None  
**Attributes:** async|public  
    
**Implemented Features:**
    
    - Domain Event Processing
    - Client Notification Triggering
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Listens to domain events and orchestrates responses, such as broadcasting changes to connected clients.  
**Logic Description:** Functions or classes that subscribe to specific domain events. Upon receiving an event (e.g., `DocumentUpdatedEvent`), the handler would use the `WebsocketBroadcaster` to send the relevant update (e.g., new Yjs diff) to all clients in the session, excluding the originator.  
**Documentation:**
    
    - **Summary:** Handles domain events raised by the collaboration service, often by broadcasting information to clients.
    
**Namespace:** creativeflow.collaboration.application.event_handlers  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/collaboration/infrastructure/__init__.py  
**Description:** Initializes the 'infrastructure' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'infrastructure' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for the infrastructure implementations package.
    
**Namespace:** creativeflow.collaboration.infrastructure  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/redis/__init__.py  
**Description:** Initializes the 'redis' sub-package for Redis related infrastructure code.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/redis  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'redis' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for Redis infrastructure components (comp.datastore.redis).
    
**Namespace:** creativeflow.collaboration.infrastructure.redis  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/redis/connection.py  
**Description:** Manages Redis connection pooling and client setup. Provides a way to get a Redis client instance.  
**Template:** Python Redis Connection  
**Dependency Level:** 1  
**Name:** connection  
**Type:** InfrastructureComponent  
**Relative Path:** infrastructure/redis  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - ConnectionPool
    
**Members:**
    
    - **Name:** redis_pool  
**Type:** redis.asyncio.ConnectionPool  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** init_redis_pool  
**Parameters:**
    
    - redis_url: str
    
**Return Type:** None  
**Attributes:** async|public|static  
    - **Name:** get_redis_client  
**Parameters:**
    
    
**Return Type:** redis.asyncio.Redis  
**Attributes:** public|static  
    - **Name:** close_redis_pool  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|public|static  
    
**Implemented Features:**
    
    - Redis Connection Management
    
**Requirement Ids:**
    
    - comp.datastore.redis
    
**Purpose:** Establishes and manages connections to the Redis server.  
**Logic Description:** Use the `redis.asyncio` library. `init_redis_pool` creates a connection pool during application startup using the URL from config. `get_redis_client` returns a client instance from the pool. `close_redis_pool` closes the pool on application shutdown.  
**Documentation:**
    
    - **Summary:** Provides functionality for managing connections to the Redis datastore.
    
**Namespace:** creativeflow.collaboration.infrastructure.redis  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/redis/repositories/__init__.py  
**Description:** Initializes the Redis repositories sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/redis/repositories  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the Redis repository implementations directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for Redis-backed repository implementations.
    
**Namespace:** creativeflow.collaboration.infrastructure.redis.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/redis/repositories/redis_collaboration_repository.py  
**Description:** Concrete implementation of ICollaborationSessionRepository and IPresenceRepository using Redis. Stores session state (including serialized YDoc), and presence information.  
**Template:** Python Redis Repository  
**Dependency Level:** 3  
**Name:** redis_collaboration_repository  
**Type:** RepositoryImplementation  
**Relative Path:** infrastructure/redis/repositories  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.asyncio.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** RedisCollaborationSessionRepositoryImpl.get_by_id  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** Optional[CollaborationSession]  
**Attributes:** async|public  
    - **Name:** RedisCollaborationSessionRepositoryImpl.save  
**Parameters:**
    
    - session: CollaborationSession
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** RedisCollaborationSessionRepositoryImpl.delete  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** RedisPresenceRepositoryImpl.get_presence  
**Parameters:**
    
    - session_id: SessionId
    - user_id: UserId
    
**Return Type:** Optional[Presence]  
**Attributes:** async|public  
    - **Name:** RedisPresenceRepositoryImpl.save_presence  
**Parameters:**
    
    - presence: Presence
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** RedisPresenceRepositoryImpl.get_all_in_session  
**Parameters:**
    
    - session_id: SessionId
    
**Return Type:** List[Presence]  
**Attributes:** async|public  
    
**Implemented Features:**
    
    - Session State Persistence
    - Presence Persistence
    
**Requirement Ids:**
    
    - REQ-013
    - comp.datastore.redis
    
**Purpose:** Persists and retrieves collaboration session data and user presence information using Redis.  
**Logic Description:** Implements the domain repository interfaces. `save` for CollaborationSession would serialize the YDoc state and participant list and store it in Redis (e.g., using HSET or JSON). `get_by_id` retrieves and deserializes this data. Presence information might be stored in a separate key structure. Use appropriate Redis data structures (hashes, sets) for efficient storage and retrieval. Define keying strategy.  
**Documentation:**
    
    - **Summary:** Implements data access for collaboration sessions and presence using Redis as the backing store.
    
**Namespace:** creativeflow.collaboration.infrastructure.redis.repositories  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/redis/pubsub_manager.py  
**Description:** Manages Redis Pub/Sub functionalities if used for broadcasting messages across multiple service instances to ensure all WebSocket connections receive updates.  
**Template:** Python Redis PubSub  
**Dependency Level:** 2  
**Name:** pubsub_manager  
**Type:** InfrastructureComponent  
**Relative Path:** infrastructure/redis  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - PublishSubscribe
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.asyncio.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** publish_message  
**Parameters:**
    
    - channel: str
    - message: str
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** subscribe_to_channel  
**Parameters:**
    
    - channel: str
    - callback: Callable
    
**Return Type:** None  
**Attributes:** async|public  
    
**Implemented Features:**
    
    - Distributed Message Broadcasting via Redis
    
**Requirement Ids:**
    
    - comp.datastore.redis
    - REQ-013
    
**Purpose:** Provides an abstraction for using Redis Pub/Sub for inter-instance communication, often for scaling WebSocket broadcasts.  
**Logic Description:** Wraps Redis Pub/Sub commands. `publish_message` sends a message to a specific Redis channel. `subscribe_to_channel` listens to a channel and invokes a callback for received messages. This is an optional component if a simpler, single-instance WebSocket manager is sufficient initially, or if another message broker is used for this specific task.  
**Documentation:**
    
    - **Summary:** Manages publishing and subscribing to messages using Redis Pub/Sub for inter-service instance communication.
    
**Namespace:** creativeflow.collaboration.infrastructure.redis  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/websocket/__init__.py  
**Description:** Initializes the 'websocket' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/websocket  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'websocket' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for WebSocket related infrastructure components.
    
**Namespace:** creativeflow.collaboration.infrastructure.websocket  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/websocket/connection_manager.py  
**Description:** Manages active WebSocket connections. Tracks connections per session/document, handles connect/disconnect events.  
**Template:** Python WebSocket Connection Manager  
**Dependency Level:** 2  
**Name:** connection_manager  
**Type:** InfrastructureComponent  
**Relative Path:** infrastructure/websocket  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** active_connections  
**Type:** Dict[str, Dict[str, WebSocket]]  
**Attributes:** private  
**Notes:** e.g., {session_id: {connection_id/user_id: websocket_instance}}  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    - websocket: WebSocket
    - session_id: str
    - user_id: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** disconnect  
**Parameters:**
    
    - websocket: WebSocket
    - session_id: str
    - user_id: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** get_connections_for_session  
**Parameters:**
    
    - session_id: str
    
**Return Type:** List[WebSocket]  
**Attributes:** public  
    - **Name:** get_user_id_for_connection  
**Parameters:**
    
    - websocket: WebSocket
    
**Return Type:** Optional[str]  
**Attributes:** public  
    
**Implemented Features:**
    
    - WebSocket Connection Tracking
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Maintains a registry of active WebSocket connections, mapping them to users and collaboration sessions.  
**Logic Description:** Provides methods to add a new connection, remove a connection, and retrieve all connections for a given session. This is crucial for broadcasting messages. If scaling across multiple instances, this manager might need to coordinate with a distributed store (like Redis) for connection information or rely on a Pub/Sub mechanism.  
**Documentation:**
    
    - **Summary:** Manages the lifecycle of active WebSocket connections for collaboration sessions.
    
**Namespace:** creativeflow.collaboration.infrastructure.websocket  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/websocket/broadcaster.py  
**Description:** Handles broadcasting messages (e.g., document updates, presence changes) to relevant WebSocket clients within a session.  
**Template:** Python WebSocket Broadcaster  
**Dependency Level:** 3  
**Name:** broadcaster  
**Type:** InfrastructureComponent  
**Relative Path:** infrastructure/websocket  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - PublishSubscribe
    
**Members:**
    
    - **Name:** connection_manager  
**Type:** ConnectionManager  
**Attributes:** private  
    - **Name:** pubsub_manager  
**Type:** RedisPubSubManager  
**Attributes:** private  
**Notes:** Optional, for multi-instance scaling  
    
**Methods:**
    
    - **Name:** broadcast_to_session  
**Parameters:**
    
    - session_id: str
    - message_schema: BaseMessage
    - exclude_sender_websocket: Optional[WebSocket] = None
    
**Return Type:** None  
**Attributes:** async|public  
    
**Implemented Features:**
    
    - Message Broadcasting to Clients
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Sends messages to all connected clients in a specific collaboration session, optionally excluding the sender.  
**Logic Description:** Uses the `ConnectionManager` to get all active WebSockets for a given `session_id`. Iterates through them and sends the serialized `message_schema`. If `pubsub_manager` is used, this service might publish to a Redis channel, and each instance's ConnectionManager (or a dedicated subscriber) would then send to its local connections. `message_schema` refers to Pydantic models from `application/schemas/message_schemas.py`.  
**Documentation:**
    
    - **Summary:** Responsible for broadcasting messages to clients connected to specific collaboration sessions.
    
**Namespace:** creativeflow.collaboration.infrastructure.websocket  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/external_services/__init__.py  
**Description:** Initializes the 'external_services' sub-package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/external_services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'external_services' directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for clients interacting with external services.
    
**Namespace:** creativeflow.collaboration.infrastructure.external_services  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/infrastructure/external_services/auth_service_client.py  
**Description:** HTTP client for interacting with the Authentication & Authorization Service (REPO-AUTH-SERVICE-001) to validate user tokens.  
**Template:** Python HTTP Client  
**Dependency Level:** 1  
**Name:** auth_service_client  
**Type:** InfrastructureComponent  
**Relative Path:** infrastructure/external_services  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - AntiCorruptionLayer
    - ServiceClient
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** timeout  
**Type:** int  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** validate_token  
**Parameters:**
    
    - token: str
    
**Return Type:** Optional[UserSchema]  
**Attributes:** async|public  
**Notes:** Returns user details if token is valid, else None or raises exception.  
    
**Implemented Features:**
    
    - User Token Validation
    
**Requirement Ids:**
    
    - Section 5.3.2
    
**Purpose:** Provides a client to communicate with the external Authentication Service for token validation.  
**Logic Description:** Uses an HTTP client library like `httpx`. The `validate_token` method sends the token to a specific endpoint on the Auth Service. Handles API responses, including errors (e.g., invalid token, service unavailable). `UserSchema` would be a Pydantic model representing the user data returned by the Auth Service.  
**Documentation:**
    
    - **Summary:** Client for making requests to the Authentication Service, primarily for validating user tokens.
    
**Namespace:** creativeflow.collaboration.infrastructure.external_services  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/collaboration/api/__init__.py  
**Description:** Initializes the 'api' sub-package for WebSocket routers.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'api' (or 'routers') directory as a Python package.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializer for API endpoint definitions, specifically WebSocket routers.
    
**Namespace:** creativeflow.collaboration.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/collaboration/api/websocket_router.py  
**Description:** Defines FastAPI WebSocket endpoints for collaboration sessions. Handles incoming messages, delegates to application services, and manages connection lifecycle.  
**Template:** Python FastAPI WebSocket Router  
**Dependency Level:** 4  
**Name:** websocket_router  
**Type:** Controller  
**Relative Path:** api  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    - Controller
    - APIGatewayPattern (WebSocket specific)
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    - **Name:** connection_manager  
**Type:** ConnectionManager  
**Attributes:** private  
    - **Name:** collaboration_service  
**Type:** CollaborationAppService  
**Attributes:** private  
    - **Name:** auth_client  
**Type:** AuthServiceClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** collaboration_websocket_endpoint  
**Parameters:**
    
    - websocket: WebSocket
    - document_id: str
    - token: Optional[str] = Query(None)
    
**Return Type:** None  
**Attributes:** async|public  
**Decorator:** @router.websocket("/ws/document/{document_id}")  
    
**Implemented Features:**
    
    - Real-time Collaboration Endpoint
    
**Requirement Ids:**
    
    - REQ-013
    - Section 5.3.2
    
**Purpose:** Handles all WebSocket communication for real-time collaboration on documents.  
**Logic Description:** Initializes with `ConnectionManager` and `CollaborationAppService`. The `@router.websocket` endpoint function handles: 1. Accepting connection. 2. Authenticating user via token (using `AuthServiceClient` or a FastAPI dependency). 3. Registering connection with `ConnectionManager`. 4. Handling user joining logic via `CollaborationAppService` (e.g., sending initial document state). 5. Looping to receive messages from client (document updates, presence, etc.). 6. Parsing messages (using `message_schemas`) and dispatching to `CollaborationAppService` commands. 7. Handling client disconnection (unregistering, notifying others).  
**Documentation:**
    
    - **Summary:** Defines the WebSocket endpoint for real-time collaboration, managing client connections and message flow.
    
**Namespace:** creativeflow.collaboration.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** requirements.txt  
**Description:** Lists Python package dependencies for the collaboration service.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    
**Requirement Ids:**
    
    
**Purpose:** Specifies all Python dependencies required to run the service.  
**Logic Description:** List libraries such as fastapi, uvicorn, websockets (FastAPI's built-in), y-py, redis, httpx, pydantic. Versions should be pinned for reproducible builds.  
**Documentation:**
    
    - **Summary:** Contains a list of Python package dependencies for the project.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment variables file. Provides a template for required environment variables.  
**Template:** Environment File  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Template
    
**Requirement Ids:**
    
    
**Purpose:** Serves as a template for developers to create their local .env file for configuration.  
**Logic Description:** Include placeholders for REDIS_URL, AUTH_SERVICE_URL, JWT_SECRET_KEY (if applicable directly, though better from secrets manager in prod), LOG_LEVEL, etc.  
**Documentation:**
    
    - **Summary:** Example file showing necessary environment variables for running the service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** Dockerfile  
**Description:** Dockerfile for building the collaboration service container image.  
**Template:** Docker File  
**Dependency Level:** 1  
**Name:** Dockerfile  
**Type:** BuildScript  
**Relative Path:** ../  
**Repository Id:** REPO-COLLABORATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization
    
**Requirement Ids:**
    
    - PMDT-002 (from general DevOps section, applies here)
    
**Purpose:** Defines instructions to build a Docker image for the collaboration service.  
**Logic Description:** Start from a Python base image (e.g., python:3.11-slim). Set working directory. Copy requirements.txt and install dependencies. Copy application code. Expose the WebSocket port. Define the CMD or ENTRYPOINT to run the Uvicorn server with main:app.  
**Documentation:**
    
    - **Summary:** Instructions for building a Docker container image for the collaboration service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedConflictResolutionUI
  - EnableRedisPubSubScaling
  
- **Database Configs:**
  
  - REDIS_URL
  - REDIS_PASSWORD
  
- **Service Configs:**
  
  - AUTH_SERVICE_URL
  - LOG_LEVEL
  - WEBSOCKET_MAX_MESSAGE_SIZE
  - SESSION_TIMEOUT_SECONDS
  - YJS_GC_INTERVAL_SECONDS
  


---

