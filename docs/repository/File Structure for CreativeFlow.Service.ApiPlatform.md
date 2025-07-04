# Specification

# 1. Files

- **Path:** pyproject.toml  
**Description:** Defines project metadata, dependencies, and build configurations using the TOML format. Manages all required Python packages like FastAPI, SQLAlchemy, Pika, and Uvicorn.  
**Template:** Python Project Template  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    - Project Configuration
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To declare all project dependencies and configuration for the Python build system.  
**Logic Description:** This file will list 'fastapi', 'uvicorn', 'sqlalchemy', 'psycopg2-binary', 'pika', 'python-jose[cryptography]', 'passlib[bcrypt]', 'pydantic-settings', 'alembic', and other necessary libraries under the [tool.poetry.dependencies] section. It will also configure project details like name, version, and author.  
**Documentation:**
    
    - **Summary:** Standard Python project definition file managing all external libraries and project build settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** alembic.ini  
**Description:** Configuration file for Alembic, the database migration tool for SQLAlchemy. It specifies the database connection URL and the location of migration scripts.  
**Template:** Alembic Config Template  
**Dependency Level:** 0  
**Name:** alembic  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Database Migration Configuration
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To configure the Alembic database migration tool, connecting it to the PostgreSQL database and locating migration scripts.  
**Logic Description:** This file contains settings for Alembic. The 'sqlalchemy.url' key will be configured to read the database connection string from environment variables to avoid hardcoding credentials. It will also point to the 'alembic/versions' directory for migration scripts.  
**Documentation:**
    
    - **Summary:** Main configuration file for the Alembic database migration framework.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/creativeflow/service/main.py  
**Description:** The main entry point for the FastAPI application. This file initializes the FastAPI app instance, includes API routers, sets up middleware for CORS, logging, and error handling, and defines startup/shutdown events.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** main  
**Type:** Application  
**Relative Path:** creativeflow/service  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** on_startup  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    - **Name:** on_shutdown  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    
**Implemented Features:**
    
    - Application Initialization
    - Middleware Configuration
    - API Routing
    
**Requirement Ids:**
    
    - REQ-017
    - SEC-005
    
**Purpose:** To bootstrap the FastAPI application, configure global middleware, and include all versioned API routers.  
**Logic Description:** Initializes a FastAPI application. It will add middleware for CORS to enforce the security policy (SEC-005). It includes the main API router from 'api.v1.api_router'. It defines 'on_startup' and 'on_shutdown' events to initialize and close resources like database connections or messaging producers. A global exception handler will be configured to catch and format errors consistently.  
**Documentation:**
    
    - **Summary:** The central file that assembles and launches the API Platform service.
    
**Namespace:** creativeflow.service  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creativeflow/service/core/config.py  
**Description:** Defines application settings and configuration management using Pydantic's BaseSettings. Loads configuration from environment variables for different environments (Dev, Staging, Prod).  
**Template:** Python Service Template  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** creativeflow/service/core  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** RABBITMQ_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** AIGEN_ORCH_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** ODOO_BUSINESS_SERVICE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** SECRET_KEY  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Management
    - Environment Variable Loading
    
**Requirement Ids:**
    
    - DEP-003
    - DEP-004
    
**Purpose:** To provide a centralized and type-safe way to manage all application configurations, loaded from the environment.  
**Logic Description:** This file will contain a Pydantic 'Settings' class that inherits from 'BaseSettings'. It will define fields for all required environment variables, such as database URLs, service endpoints for dependencies, and security keys. This ensures that the application will fail fast if a required configuration is missing and provides type validation.  
**Documentation:**
    
    - **Summary:** Handles all application settings, ensuring a clean separation of configuration from code.
    
**Namespace:** creativeflow.service.core  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/creativeflow/service/core/security.py  
**Description:** Contains security-related functions, including API key hashing and verification, and potentially helpers for scope/permission checking.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** security  
**Type:** Utility  
**Relative Path:** creativeflow/service/core  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** hash_api_secret  
**Parameters:**
    
    - secret: str
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** verify_api_secret  
**Parameters:**
    
    - plain_secret: str
    - hashed_secret: str
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** generate_api_key_and_secret  
**Parameters:**
    
    
**Return Type:** tuple[str, str]  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Key Hashing
    - Secret Verification
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-005
    
**Purpose:** To centralize all cryptographic operations related to API key management, ensuring secure practices.  
**Logic Description:** This module will use the 'passlib' library with the bcrypt algorithm to securely hash and verify API secrets. It will also contain a function to generate a cryptographically secure, random string for new API keys and secrets, ensuring they are not guessable. This keeps security logic separate and easily auditable.  
**Documentation:**
    
    - **Summary:** Provides core security functions for hashing, verification, and generation of API credentials.
    
**Namespace:** creativeflow.service.core  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** src/creativeflow/service/db/session.py  
**Description:** Manages SQLAlchemy database sessions. Provides a dependency-injectable function to get a database session for each request, ensuring proper session lifecycle management.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** session  
**Type:** Database  
**Relative Path:** creativeflow/service/db  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - UnitOfWork
    
**Members:**
    
    - **Name:** engine  
**Type:** Engine  
**Attributes:** private  
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:** public  
    
**Implemented Features:**
    
    - Database Session Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a reliable mechanism for obtaining and closing database sessions within the request-response cycle.  
**Logic Description:** This file will create the SQLAlchemy engine instance using the database URL from the core configuration. It defines a 'SessionLocal' session factory. A generator function 'get_db_session' is created to be used with FastAPI's dependency injection system. This function yields a database session and ensures it's closed in a 'finally' block, even if errors occur.  
**Documentation:**
    
    - **Summary:** Handles the creation and lifecycle of SQLAlchemy database sessions for the application.
    
**Namespace:** creativeflow.service.db  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/service/db/models/api_client.py  
**Description:** SQLAlchemy ORM model for the 'APIClient' table. Defines the database schema for storing API keys, hashed secrets, permissions, and associated user information.  
**Template:** Python Service Template  
**Dependency Level:** 2  
**Name:** api_client  
**Type:** Model  
**Relative Path:** creativeflow/service/db/models  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public|primary_key  
    - **Name:** user_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** name  
**Type:** String  
**Attributes:** public  
    - **Name:** api_key  
**Type:** String  
**Attributes:** public|unique  
    - **Name:** secret_hash  
**Type:** String  
**Attributes:** public  
    - **Name:** permissions  
**Type:** JSONB  
**Attributes:** public  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Client Data Model
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** To define the database structure for storing API client credentials and metadata.  
**Logic Description:** This file defines a SQLAlchemy model class 'APIClient' that maps to the corresponding database table. It includes columns for a unique API key, the hashed secret, a user-defined name, status, and a JSONB field for granular permissions. Relationships to other potential models like 'APIUsageLog' could be defined here.  
**Documentation:**
    
    - **Summary:** Represents the 'APIClient' entity in the database, holding all information related to a developer's API key.
    
**Namespace:** creativeflow.service.db.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/service/db/repository/api_client_repository.py  
**Description:** Implements the Repository pattern for the APIClient model. Encapsulates all database query logic for API clients, such as creating, retrieving by key, and updating.  
**Template:** Python Service Template  
**Dependency Level:** 3  
**Name:** api_client_repository  
**Type:** Repository  
**Relative Path:** creativeflow/service/db/repository  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_api_key  
**Parameters:**
    
    - db: Session
    - api_key: str
    
**Return Type:** Optional[APIClient]  
**Attributes:** public  
    - **Name:** create_api_client  
**Parameters:**
    
    - db: Session
    - client_in: APIClientCreateSchema
    
**Return Type:** APIClient  
**Attributes:** public  
    - **Name:** revoke_api_client  
**Parameters:**
    
    - db: Session
    - api_client: APIClient
    
**Return Type:** APIClient  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Client Data Access
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** To abstract the database interactions for the APIClient entity, providing a clean interface for the service layer.  
**Logic Description:** This class will contain methods that perform specific queries on the APIClient table. For instance, 'get_by_api_key' will fetch a client record based on the provided API key. 'create_api_client' will handle the insertion of a new record. This abstracts the raw SQLAlchemy queries from the business logic in the service layer.  
**Documentation:**
    
    - **Summary:** Provides a data access layer for creating, retrieving, updating, and deleting APIClient records from the database.
    
**Namespace:** creativeflow.service.db.repository  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/service/service/api_key_service.py  
**Description:** Contains the business logic for managing the API key lifecycle. It coordinates the generation of new keys, secure storage, and revocation, using the security module and repository.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** api_key_service  
**Type:** Service  
**Relative Path:** creativeflow/service/service  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_new_api_key  
**Parameters:**
    
    - db: Session
    - user_id: UUID
    - key_name: str
    
**Return Type:** tuple[APIClient, str]  
**Attributes:** public  
    - **Name:** revoke_api_key  
**Parameters:**
    
    - db: Session
    - user_id: UUID
    - api_key_id: UUID
    
**Return Type:** APIClient  
**Attributes:** public  
    - **Name:** authenticate_api_key  
**Parameters:**
    
    - db: Session
    - api_key: str
    
**Return Type:** Optional[APIClient]  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Key Lifecycle Management
    - API Key Authentication Logic
    
**Requirement Ids:**
    
    - SEC-001
    - REQ-7-002
    
**Purpose:** To orchestrate the creation, validation, and revocation of API keys for developers.  
**Logic Description:** This service contains the core business logic. The 'create_new_api_key' method will call the security module to generate a key/secret pair, hash the secret, and then use the repository to save the new client record to the database. It returns the full secret only once. The 'revoke_api_key' method will find the key and set its 'is_active' flag to false. 'authenticate_api_key' will be used by API dependencies to validate incoming keys.  
**Documentation:**
    
    - **Summary:** Implements the use cases for API key management, acting as a transactional boundary for these operations.
    
**Namespace:** creativeflow.service.service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/service/api/v1/endpoints/api_keys.py  
**Description:** FastAPI router that exposes HTTP endpoints for API key management (/keys). It handles incoming requests, validates them using Pydantic schemas, and calls the appropriate service layer functions.  
**Template:** Python Service Template  
**Dependency Level:** 5  
**Name:** api_keys  
**Type:** Controller  
**Relative Path:** creativeflow/service/api/v1/endpoints  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Controller
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** create_api_key  
**Parameters:**
    
    - key_in: APIKeyCreateSchema
    - db: Session
    - current_user: User
    
**Return Type:** APIKeyCreateResponseSchema  
**Attributes:** public|post  
    - **Name:** list_api_keys  
**Parameters:**
    
    - db: Session
    - current_user: User
    
**Return Type:** list[APIKeySchema]  
**Attributes:** public|get  
    - **Name:** revoke_api_key_endpoint  
**Parameters:**
    
    - key_id: UUID
    - db: Session
    - current_user: User
    
**Return Type:** APIKeySchema  
**Attributes:** public|delete  
    
**Implemented Features:**
    
    - API Key Management Endpoints
    
**Requirement Ids:**
    
    - SEC-001
    - REQ-7-002
    
**Purpose:** To provide RESTful endpoints for developers to manage their API keys.  
**Logic Description:** This file will define a FastAPI APIRouter. It will have endpoints for POST /keys, GET /keys, and DELETE /keys/{key_id}. Each endpoint will depend on getting the current authenticated user (this service authenticates with its own user JWTs for the developer portal) and a database session. It will use the 'api_key_service' to perform the business logic and return data formatted according to the defined Pydantic response schemas.  
**Documentation:**
    
    - **Summary:** Exposes the API for creating, listing, and revoking developer API keys.
    
**Namespace:** creativeflow.service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creativeflow/service/messaging/producer.py  
**Description:** Handles publishing messages to RabbitMQ. Contains a class or functions to connect to RabbitMQ and send messages to specific exchanges, such as for dispatching webhook events.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** producer  
**Type:** Messaging  
**Relative Path:** creativeflow/service/messaging  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Producer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** publish_webhook_event  
**Parameters:**
    
    - event_payload: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Webhook Event Publishing
    
**Requirement Ids:**
    
    - REQ-017
    - REQ-7-004
    
**Purpose:** To decouple webhook sending from the main application flow by publishing events to a message queue.  
**Logic Description:** This module will contain a 'WebhookProducer' class that establishes a connection to RabbitMQ using the Pika library. It will have a method 'publish_webhook_event' that takes a payload, serializes it to JSON, and publishes it to a predefined 'webhooks' exchange. This ensures that even if the webhook-sending consumer is down, the event is not lost.  
**Documentation:**
    
    - **Summary:** A client for publishing messages to the RabbitMQ message broker, specifically for webhook events.
    
**Namespace:** creativeflow.service.messaging  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/service/quota_service.py  
**Description:** Manages rate limiting and usage quotas for API clients. It checks usage against limits before allowing an operation to proceed.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** quota_service  
**Type:** Service  
**Relative Path:** creativeflow/service/service  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** check_and_log_usage  
**Parameters:**
    
    - db: Session
    - api_client: APIClient
    - action_cost: int
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Rate Limiting Logic
    - Quota Enforcement
    
**Requirement Ids:**
    
    - REQ-018
    - REQ-7-003
    - SEC-005
    
**Purpose:** To enforce usage limits and track consumption for billing and fair use.  
**Logic Description:** This service will have a core method like 'check_and_log_usage'. This method will first check the rate limit (potentially using a Redis-based token bucket algorithm, though Redis is not a direct dependency of this repo, it might be a dependency of the Odoo service it calls). It will then call the Odoo Business Service client to verify the user's quota/billing status. If checks pass, it will use the 'usage_log_repository' to record the API call and its cost. If checks fail, it will raise a specific HTTP exception (e.g., 429 Too Many Requests).  
**Documentation:**
    
    - **Summary:** Provides business logic for API usage tracking, rate limiting, and quota enforcement.
    
**Namespace:** creativeflow.service.service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/service/integrations/aigen_orchestration_client.py  
**Description:** An HTTP client for communicating with the AI Generation Orchestration Service. It encapsulates the API calls for initiating and checking the status of generation jobs.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** aigen_orchestration_client  
**Type:** Client  
**Relative Path:** creativeflow/service/integrations  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Circuit Breaker
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiate_generation  
**Parameters:**
    
    - generation_data: dict
    - user_context: dict
    
**Return Type:** dict  
**Attributes:** public|async  
    - **Name:** get_generation_status  
**Parameters:**
    
    - job_id: UUID
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - AI Generation Service Integration
    
**Requirement Ids:**
    
    - REQ-017
    
**Purpose:** To provide a clean, typed interface for interacting with the downstream AI Generation Orchestration Service.  
**Logic Description:** This class will use an HTTP client library like 'httpx' to make requests to the AI Generation service's internal API. It will handle adding appropriate authentication headers (e.g., an internal service-to-service token). Methods will be typed using Pydantic models for request and response data. It should also implement a basic retry mechanism or a circuit breaker pattern for resilience.  
**Documentation:**
    
    - **Summary:** A client that abstracts communication with the AI Generation Orchestration microservice.
    
**Namespace:** creativeflow.service.integrations  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/api/v1/dependencies.py  
**Description:** Defines common FastAPI dependencies used across endpoints, such as authenticating an API client from a request header and providing a database session.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** dependencies  
**Type:** Utility  
**Relative Path:** creativeflow/service/api/v1  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Dependency Injection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_api_client  
**Parameters:**
    
    - api_key: str = Security(api_key_scheme)
    - db: Session = Depends(get_db_session)
    
**Return Type:** APIClient  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Authentication Dependency
    - Database Session Dependency
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-005
    
**Purpose:** To create reusable components for dependency injection in API endpoints, primarily for authentication and database access.  
**Logic Description:** This file defines a 'get_current_api_client' dependency. It will extract the API key from the 'Authorization' header, query the database via the repository to find the matching active API client, and return it. If the key is invalid or inactive, it will raise an 'HTTPException' with a 401 or 403 status code. This allows endpoints to be protected by simply adding this as a dependency.  
**Documentation:**
    
    - **Summary:** Provides injectable dependencies for FastAPI endpoints, handling concerns like API key authentication.
    
**Namespace:** creativeflow.service.api.v1  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** alembic/env.py  
**Description:** Alembic environment script. Configures the migration context, sets the target metadata for autogeneration, and handles database connection setup for running migrations.  
**Template:** Alembic Env Template  
**Dependency Level:** 3  
**Name:** env  
**Type:** Configuration  
**Relative Path:** alembic  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** run_migrations_offline  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** run_migrations_online  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Database Migration Execution Context
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To provide the runtime configuration for Alembic migrations, linking the ORM models to the migration engine.  
**Logic Description:** This script will be configured to import the 'Base' declarative base from 'db.base' and set it as the 'target_metadata'. This allows Alembic's 'autogenerate' command to compare the current state of the database with the state defined by the SQLAlchemy models and create new migration scripts. It also handles the logic for running migrations online (against a live DB) or offline (generating SQL scripts).  
**Documentation:**
    
    - **Summary:** Runtime environment configuration script for Alembic database migrations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/service/db/models/webhook.py  
**Description:** SQLAlchemy ORM model for the 'Webhook' table, defining the schema for storing developer-registered webhook endpoints, their associated events, and secrets.  
**Template:** Python Service Template  
**Dependency Level:** 2  
**Name:** webhook  
**Type:** Model  
**Relative Path:** creativeflow/service/db/models  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public|primary_key  
    - **Name:** api_client_id  
**Type:** UUID  
**Attributes:** public|foreign_key  
    - **Name:** target_url  
**Type:** String  
**Attributes:** public  
    - **Name:** event_type  
**Type:** String  
**Attributes:** public  
    - **Name:** secret_hash  
**Type:** String  
**Attributes:** public  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Webhook Data Model
    
**Requirement Ids:**
    
    - REQ-017
    - REQ-7-004
    
**Purpose:** To define the database structure for storing webhook configurations.  
**Logic Description:** This file defines the 'Webhook' SQLAlchemy model. It includes the target URL, the specific event type it subscribes to (e.g., 'generation.completed'), a reference to the owning API client, and a hashed secret for signing webhook payloads, allowing the developer to verify the authenticity of the webhook.  
**Documentation:**
    
    - **Summary:** Represents a webhook registration entity in the database.
    
**Namespace:** creativeflow.service.db.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/service/api/v1/schemas/generation_schemas.py  
**Description:** Pydantic schemas for API requests and responses related to creative generation. Defines the data contracts for initiating a generation and retrieving its status.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** generation_schemas  
**Type:** Schema  
**Relative Path:** creativeflow/service/api/v1/schemas  
**Repository Id:** REPO-SERVICE-APIPLATFORM-001  
**Pattern Ids:**
    
    - Data Transfer Object
    
**Members:**
    
    - **Name:** GenerationRequestSchema  
**Type:** Pydantic.BaseModel  
**Attributes:** public  
    - **Name:** GenerationResponseSchema  
**Type:** Pydantic.BaseModel  
**Attributes:** public  
    - **Name:** GenerationStatusSchema  
**Type:** Pydantic.BaseModel  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Data Contracts for Generation
    
**Requirement Ids:**
    
    - REQ-017
    - REQ-7-001
    
**Purpose:** To define and validate the data structures for creative generation API endpoints.  
**Logic Description:** This module will contain Pydantic models for the API layer. 'GenerationRequestSchema' will define the expected input from the developer, including fields like 'prompt', 'format', 'style_hints', etc., with appropriate validation. 'GenerationResponseSchema' will define the structure of the successful initiation response (e.g., returning a 'job_id'). 'GenerationStatusSchema' will define the structure for the status check response.  
**Documentation:**
    
    - **Summary:** Defines the request and response models for the creative generation API endpoints.
    
**Namespace:** creativeflow.service.api.v1.schemas  
**Metadata:**
    
    - **Category:** Presentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableCanaryDeploymentsForWebhooks
  - enableVolumeDiscounts
  - enableVerboseApiLogging
  
- **Database Configs:**
  
  - DATABASE_URL
  - DB_POOL_SIZE
  - DB_POOL_TIMEOUT
  


---

