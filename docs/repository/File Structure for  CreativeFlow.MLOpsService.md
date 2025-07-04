# Specification

# 1. Files

- **Path:** src/creativeflow/mlops_service/__init__.py  
**Description:** Initializes the mlops_service Python package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** Typically empty or can contain package-level imports.  
**Documentation:**
    
    - **Summary:** Package initializer for the MLOps service.
    
**Namespace:** creativeflow.mlops_service  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/mlops_service/main.py  
**Description:** Main application file for the FastAPI MLOps service. Initializes the FastAPI application, mounts routers, and includes global configurations or middleware.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 5  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main  
**Repository Id:** REPO-MLOPS-SERVICE-001  
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
    - **Name:** on_startup  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    - **Name:** on_shutdown  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** private|async  
    
**Implemented Features:**
    
    - FastAPI App Setup
    - Router Integration
    - Lifecycle Events
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Initializes and configures the FastAPI application for the MLOps service.  
**Logic Description:** Creates a FastAPI instance. Includes API routers from api.v1. Registers startup and shutdown event handlers (e.g. for database connections). Mounts middleware.  
**Documentation:**
    
    - **Summary:** Entry point for the MLOps FastAPI service.
    
**Namespace:** creativeflow.mlops_service  
**Metadata:**
    
    - **Category:** ApplicationCore
    
- **Path:** src/creativeflow/mlops_service/core/config.py  
**Description:** Handles application configuration settings, loading from environment variables or configuration files. Uses Pydantic for typed settings.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** core/config  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** MINIO_ENDPOINT  
**Type:** str  
**Attributes:** public  
    - **Name:** MINIO_ACCESS_KEY  
**Type:** str  
**Attributes:** public  
    - **Name:** MINIO_SECRET_KEY  
**Type:** SecretStr  
**Attributes:** public  
    - **Name:** KUBERNETES_CONFIG_PATH  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** MLFLOW_TRACKING_URI  
**Type:** Optional[str]  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Environment Configuration
    - Typed Settings
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines and loads all necessary configuration settings for the MLOps service.  
**Logic Description:** Defines a Pydantic BaseSettings class to load variables from .env files or environment. Includes settings for database connection, MinIO, Kubernetes, security scanners, and other external services.  
**Documentation:**
    
    - **Summary:** Manages application-wide configuration settings.
    
**Namespace:** creativeflow.mlops_service.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/mlops_service/core/security.py  
**Description:** Contains security-related utility functions, such as authentication middleware integration (if any specific to this service) or API key validation helpers.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** security  
**Type:** Utility  
**Relative Path:** core/security  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_current_active_user  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** User  
**Attributes:** public|async  
    - **Name:** verify_api_key  
**Parameters:**
    
    - api_key: str
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Key Verification Helper
    - User Authentication Helper
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides security utility functions, potentially including API key validation or RBAC checks.  
**Logic Description:** Implements functions for API key validation against stored keys (if applicable for internal service-to-service). Integrates with a shared auth library if user context is needed. Handles basic authorization checks specific to MLOps resources.  
**Documentation:**
    
    - **Summary:** Core security utilities for the MLOps service.
    
**Namespace:** creativeflow.mlops_service.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/mlops_service/database.py  
**Description:** SQLAlchemy database engine and session management setup.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** database  
**Type:** DataAccess  
**Relative Path:** database  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** engine  
**Type:** Engine  
**Attributes:** public  
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Iterator[Session]  
**Attributes:** public  
    
**Implemented Features:**
    
    - Database Connection Setup
    - Session Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Configures SQLAlchemy database engine, session factory, and dependency for FastAPI.  
**Logic Description:** Initializes the SQLAlchemy engine using DATABASE_URL from config. Creates SessionLocal. Defines a get_db dependency injectable for FastAPI routes to get DB sessions.  
**Documentation:**
    
    - **Summary:** Handles database connection and session management for SQLAlchemy.
    
**Namespace:** creativeflow.mlops_service  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/domain/entities/__init__.py  
**Description:** Initializes the domain entities package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** domain/entities/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for domain entities.  
**Logic Description:** Empty or imports key entities for easier access.  
**Documentation:**
    
    - **Summary:** Package initializer for MLOps domain entities.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/entities/ai_model.py  
**Description:** Pydantic model representing an AI Model entity within the MLOps domain.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** ai_model  
**Type:** DomainEntity  
**Relative Path:** domain/entities/ai_model  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** name  
**Type:** str  
**Attributes:** public  
    - **Name:** description  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** task_type  
**Type:** str  
**Attributes:** public  
    - **Name:** owner_id  
**Type:** Optional[UUID]  
**Attributes:** public  
    - **Name:** created_at  
**Type:** datetime  
**Attributes:** public  
    - **Name:** updated_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Data Structure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the data structure and validation for an AI Model entity.  
**Logic Description:** A Pydantic BaseModel defining fields like id, name, description, task_type, owner_id, timestamps. Includes validators for fields.  
**Documentation:**
    
    - **Summary:** Represents an AI Model entity, including its metadata.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/entities/ai_model_version.py  
**Description:** Pydantic model representing a specific version of an AI Model.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** ai_model_version  
**Type:** DomainEntity  
**Relative Path:** domain/entities/ai_model_version  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** model_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** version_string  
**Type:** str  
**Attributes:** public  
    - **Name:** description  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** artifact_path  
**Type:** str  
**Attributes:** public  
    - **Name:** model_format  
**Type:** str  
**Attributes:** public  
    - **Name:** interface_type  
**Type:** str  
**Attributes:** public  
    - **Name:** parameters  
**Type:** Optional[Dict[str, Any]]  
**Attributes:** public  
    - **Name:** metrics  
**Type:** Optional[Dict[str, Any]]  
**Attributes:** public  
    - **Name:** status  
**Type:** ModelVersionStatusEnum  
**Attributes:** public  
    - **Name:** created_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Version Data Structure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the data structure for a version of an AI Model, including its artifact location and metadata.  
**Logic Description:** Pydantic BaseModel with fields for version details, artifact path (MinIO), format, status (staging, production), parameters, metrics, and lineage information.  
**Documentation:**
    
    - **Summary:** Represents a version of an AI Model, linking to its artifacts and metadata.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/entities/deployment.py  
**Description:** Pydantic model representing a deployment instance of an AI Model Version.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** deployment  
**Type:** DomainEntity  
**Relative Path:** domain/entities/deployment  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** model_version_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** environment  
**Type:** str  
**Attributes:** public  
    - **Name:** status  
**Type:** DeploymentStatusEnum  
**Attributes:** public  
    - **Name:** deployment_strategy  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** endpoint_url  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** replicas  
**Type:** Optional[int]  
**Attributes:** public  
    - **Name:** config  
**Type:** Optional[Dict[str, Any]]  
**Attributes:** public  
    - **Name:** deployed_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Deployment Data Structure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the data structure for tracking the deployment of a model version to an environment.  
**Logic Description:** Pydantic BaseModel detailing the deployment, including target environment, status, strategy (canary/blue-green), endpoint, and configuration.  
**Documentation:**
    
    - **Summary:** Represents a deployment of a specific AI model version.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/entities/validation_result.py  
**Description:** Pydantic model for storing the results of model validation and security scans.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** validation_result  
**Type:** DomainEntity  
**Relative Path:** domain/entities/validation_result  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** model_version_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** scan_type  
**Type:** str  
**Attributes:** public  
    - **Name:** status  
**Type:** ValidationStatusEnum  
**Attributes:** public  
    - **Name:** summary  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** details_path  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** validated_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Validation Result Data Structure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the structure for storing model validation results, including security and functional checks.  
**Logic Description:** Pydantic BaseModel containing scan type (security, functional, performance), status, summary, and a path to detailed report artifacts (e.g., in MinIO).  
**Documentation:**
    
    - **Summary:** Represents the outcome of a validation process for an AI model version.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/entities/model_feedback.py  
**Description:** Pydantic model for user feedback on AI model performance or output quality.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** model_feedback  
**Type:** DomainEntity  
**Relative Path:** domain/entities/model_feedback  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** model_version_id  
**Type:** UUID  
**Attributes:** public  
    - **Name:** user_id  
**Type:** Optional[UUID]  
**Attributes:** public  
    - **Name:** generation_request_id  
**Type:** Optional[UUID]  
**Attributes:** public  
    - **Name:** rating  
**Type:** Optional[int]  
**Attributes:** public  
    - **Name:** comment  
**Type:** Optional[str]  
**Attributes:** public  
    - **Name:** feedback_data  
**Type:** Optional[Dict[str, Any]]  
**Attributes:** public  
    - **Name:** submitted_at  
**Type:** datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Feedback Data Structure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the structure for capturing user feedback related to AI models.  
**Logic Description:** Pydantic BaseModel to store feedback including rating, comments, and any structured feedback data. Links to model version and optionally user/generation request.  
**Documentation:**
    
    - **Summary:** Represents user-provided feedback on an AI model or its outputs.
    
**Namespace:** creativeflow.mlops_service.domain.entities  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/domain/enums.py  
**Description:** Defines various enumerations used throughout the MLOps domain.  
**Template:** Python Enum  
**Dependency Level:** 0  
**Name:** enums  
**Type:** DomainEnum  
**Relative Path:** domain/enums  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ModelVersionStatusEnum  
**Type:** str, Enum  
**Attributes:** public  
    - **Name:** DeploymentStatusEnum  
**Type:** str, Enum  
**Attributes:** public  
    - **Name:** ValidationStatusEnum  
**Type:** str, Enum  
**Attributes:** public  
    - **Name:** ModelFormatEnum  
**Type:** str, Enum  
**Attributes:** public  
    - **Name:** ServingInterfaceEnum  
**Type:** str, Enum  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Domain Enumerations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides standardized enumerations for model status, deployment status, validation status, etc.  
**Logic Description:** Defines Python Enum classes for ModelVersionStatus (STAGING, PRODUCTION, ARCHIVED), DeploymentStatus (ACTIVE, INACTIVE, FAILED), ValidationStatus (PASSED, FAILED, PENDING), ModelFormat (ONNX, TF_SAVEDMODEL, PYTORCH_TORCHSCRIPT, CUSTOM_PYTHON_CONTAINER), ServingInterface (TF_SERVING, TORCHSERVE, TRITON, CUSTOM_FASTAPI).  
**Documentation:**
    
    - **Summary:** Contains enumerations for consistent state and type management in the MLOps domain.
    
**Namespace:** creativeflow.mlops_service.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creativeflow/mlops_service/api/v1/__init__.py  
**Description:** Initializes the v1 API package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for API v1.  
**Logic Description:** Typically empty or can aggregate routers.  
**Documentation:**
    
    - **Summary:** Package initializer for v1 API routes and schemas.
    
**Namespace:** creativeflow.mlops_service.api.v1  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/endpoints/__init__.py  
**Description:** Initializes the API endpoints package.  
**Template:** Python Package Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/endpoints/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for API endpoints.  
**Logic Description:** Imports and aggregates APIRouter instances from individual endpoint files.  
**Documentation:**
    
    - **Summary:** Package initializer for FastAPI endpoint routers.
    
**Namespace:** creativeflow.mlops_service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/endpoints/models.py  
**Description:** FastAPI router for AI Model and Model Version management endpoints.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 4  
**Name:** models_api  
**Type:** APIController  
**Relative Path:** api/v1/endpoints/models  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** create_model  
**Parameters:**
    
    - model_in: ModelCreateSchema
    - db: Session = Depends(get_db)
    
**Return Type:** ModelResponseSchema  
**Attributes:** public|async  
    - **Name:** get_model  
**Parameters:**
    
    - model_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** ModelResponseSchema  
**Attributes:** public|async  
    - **Name:** list_models  
**Parameters:**
    
    - skip: int = 0
    - limit: int = 100
    - db: Session = Depends(get_db)
    
**Return Type:** List[ModelResponseSchema]  
**Attributes:** public|async  
    - **Name:** create_model_version  
**Parameters:**
    
    - model_id: UUID
    - version_in: ModelVersionCreateSchema
    - file: UploadFile = File(...)
    - db: Session = Depends(get_db)
    
**Return Type:** ModelVersionResponseSchema  
**Attributes:** public|async  
    - **Name:** get_model_version  
**Parameters:**
    
    - version_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** ModelVersionResponseSchema  
**Attributes:** public|async  
    - **Name:** update_model_version_status  
**Parameters:**
    
    - version_id: UUID
    - status_update: ModelVersionStatusUpdateSchema
    - db: Session = Depends(get_db)
    
**Return Type:** ModelVersionResponseSchema  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model CRUD
    - Model Version CRUD
    - Model Upload (artifact)
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides API endpoints for managing AI models and their versions, including uploads.  
**Logic Description:** Defines FastAPI routes for creating, reading, listing models. Routes for creating, reading, updating status of model versions. Handles model artifact file uploads (to be passed to ModelUploadService). Uses ModelRegistryService.  
**Documentation:**
    
    - **Summary:** API endpoints for AI model and version management.
    
**Namespace:** creativeflow.mlops_service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/endpoints/deployments.py  
**Description:** FastAPI router for AI Model Deployment and A/B testing endpoints.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 4  
**Name:** deployments_api  
**Type:** APIController  
**Relative Path:** api/v1/endpoints/deployments  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** create_deployment  
**Parameters:**
    
    - deployment_in: DeploymentCreateSchema
    - db: Session = Depends(get_db)
    
**Return Type:** DeploymentResponseSchema  
**Attributes:** public|async  
    - **Name:** get_deployment_status  
**Parameters:**
    
    - deployment_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** DeploymentResponseSchema  
**Attributes:** public|async  
    - **Name:** list_deployments  
**Parameters:**
    
    - model_version_id: Optional[UUID] = None
    - environment: Optional[str] = None
    - db: Session = Depends(get_db)
    
**Return Type:** List[DeploymentResponseSchema]  
**Attributes:** public|async  
    - **Name:** update_deployment  
**Parameters:**
    
    - deployment_id: UUID
    - deployment_update: DeploymentUpdateSchema
    - db: Session = Depends(get_db)
    
**Return Type:** DeploymentResponseSchema  
**Attributes:** public|async  
    - **Name:** delete_deployment  
**Parameters:**
    
    - deployment_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model Deployment CRUD
    - A/B Test Configuration (via deployment config)
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides API endpoints for deploying models, managing deployment strategies (canary/blue-green), and A/B testing.  
**Logic Description:** Defines FastAPI routes for creating, reading, listing, updating, and deleting model deployments. Leverages ModelDeploymentService to interact with Kubernetes and update registry.  
**Documentation:**
    
    - **Summary:** API endpoints for managing AI model deployments and A/B tests.
    
**Namespace:** creativeflow.mlops_service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/endpoints/validation.py  
**Description:** FastAPI router for AI Model Validation and Security Scanning endpoints.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 4  
**Name:** validation_api  
**Type:** APIController  
**Relative Path:** api/v1/endpoints/validation  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** trigger_model_validation  
**Parameters:**
    
    - version_id: UUID
    - validation_config: ValidationRequestSchema
    - db: Session = Depends(get_db)
    
**Return Type:** ValidationResultResponseSchema  
**Attributes:** public|async  
    - **Name:** get_validation_result  
**Parameters:**
    
    - result_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** ValidationResultResponseSchema  
**Attributes:** public|async  
    - **Name:** list_validation_results_for_version  
**Parameters:**
    
    - version_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** List[ValidationResultResponseSchema]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Trigger Model Validation
    - Get Validation Results
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides API endpoints for initiating model validation (security, functional) and retrieving results.  
**Logic Description:** Defines FastAPI routes to trigger validation processes for a model version and fetch validation outcomes. Interacts with ModelValidationService.  
**Documentation:**
    
    - **Summary:** API endpoints for AI model validation processes.
    
**Namespace:** creativeflow.mlops_service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/endpoints/feedback.py  
**Description:** FastAPI router for collecting user feedback on AI models.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 4  
**Name:** feedback_api  
**Type:** APIController  
**Relative Path:** api/v1/endpoints/feedback  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** submit_model_feedback  
**Parameters:**
    
    - feedback_in: ModelFeedbackCreateSchema
    - db: Session = Depends(get_db)
    
**Return Type:** ModelFeedbackResponseSchema  
**Attributes:** public|async  
    - **Name:** get_feedback_for_model_version  
**Parameters:**
    
    - version_id: UUID
    - db: Session = Depends(get_db)
    
**Return Type:** List[ModelFeedbackResponseSchema]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Submit Model Feedback
    - Retrieve Model Feedback
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides API endpoints for users to submit feedback on model outputs and for admins to retrieve it.  
**Logic Description:** Defines FastAPI routes for submitting feedback (rating, comments) and retrieving aggregated feedback for model versions. Uses ModelFeedbackService.  
**Documentation:**
    
    - **Summary:** API endpoints for managing AI model feedback.
    
**Namespace:** creativeflow.mlops_service.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/schemas/__init__.py  
**Description:** Initializes the API schemas package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/v1/schemas/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for API schemas.  
**Logic Description:** Imports Pydantic schemas for easier access.  
**Documentation:**
    
    - **Summary:** Package initializer for Pydantic API request/response schemas.
    
**Namespace:** creativeflow.mlops_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/schemas/model_schemas.py  
**Description:** Pydantic schemas for AI Model and Model Version API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** model_schemas  
**Type:** APISchema  
**Relative Path:** api/v1/schemas/model_schemas  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ModelBaseSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** ModelCreateSchema  
**Type:** ModelBaseSchema  
**Attributes:** public  
    - **Name:** ModelUpdateSchema  
**Type:** ModelBaseSchema  
**Attributes:** public  
    - **Name:** ModelResponseSchema  
**Type:** ModelBaseSchema  
**Attributes:** public  
    - **Name:** ModelVersionBaseSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** ModelVersionCreateSchema  
**Type:** ModelVersionBaseSchema  
**Attributes:** public  
    - **Name:** ModelVersionUpdateSchema  
**Type:** ModelVersionBaseSchema  
**Attributes:** public  
    - **Name:** ModelVersionResponseSchema  
**Type:** ModelVersionBaseSchema  
**Attributes:** public  
    - **Name:** ModelVersionStatusUpdateSchema  
**Type:** BaseModel  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model API Schemas
    - Model Version API Schemas
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines Pydantic models for validating API requests and formatting responses related to models and versions.  
**Logic Description:** Includes schemas for creating, updating, and reading AI models and their versions. Fields align with domain entities but adapted for API interaction (e.g., file upload fields in create schemas).  
**Documentation:**
    
    - **Summary:** Pydantic schemas for AI model and version API data structures.
    
**Namespace:** creativeflow.mlops_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/schemas/deployment_schemas.py  
**Description:** Pydantic schemas for Model Deployment API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** deployment_schemas  
**Type:** APISchema  
**Relative Path:** api/v1/schemas/deployment_schemas  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DeploymentBaseSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** DeploymentCreateSchema  
**Type:** DeploymentBaseSchema  
**Attributes:** public  
    - **Name:** DeploymentUpdateSchema  
**Type:** DeploymentBaseSchema  
**Attributes:** public  
    - **Name:** DeploymentResponseSchema  
**Type:** DeploymentBaseSchema  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Deployment API Schemas
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines Pydantic models for deployment-related API interactions.  
**Logic Description:** Schemas for creating, updating, and reading deployment configurations, including environment, strategy, replica counts, and A/B testing parameters.  
**Documentation:**
    
    - **Summary:** Pydantic schemas for AI model deployment API data structures.
    
**Namespace:** creativeflow.mlops_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/schemas/validation_schemas.py  
**Description:** Pydantic schemas for Model Validation API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** validation_schemas  
**Type:** APISchema  
**Relative Path:** api/v1/schemas/validation_schemas  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ValidationRequestSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** ValidationResultBaseSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** ValidationResultResponseSchema  
**Type:** ValidationResultBaseSchema  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Validation API Schemas
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines Pydantic models for triggering model validation and retrieving validation results.  
**Logic Description:** Schemas for requesting a validation run (specifying scan types) and for representing the outcome of validation processes.  
**Documentation:**
    
    - **Summary:** Pydantic schemas for AI model validation API data structures.
    
**Namespace:** creativeflow.mlops_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/api/v1/schemas/feedback_schemas.py  
**Description:** Pydantic schemas for Model Feedback API requests and responses.  
**Template:** Python Pydantic Model  
**Dependency Level:** 1  
**Name:** feedback_schemas  
**Type:** APISchema  
**Relative Path:** api/v1/schemas/feedback_schemas  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ModelFeedbackBaseSchema  
**Type:** BaseModel  
**Attributes:** public  
    - **Name:** ModelFeedbackCreateSchema  
**Type:** ModelFeedbackBaseSchema  
**Attributes:** public  
    - **Name:** ModelFeedbackResponseSchema  
**Type:** ModelFeedbackBaseSchema  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Feedback API Schemas
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines Pydantic models for submitting and retrieving user feedback on AI models.  
**Logic Description:** Schemas for creating feedback entries (rating, comment) and for representing feedback data in API responses.  
**Documentation:**
    
    - **Summary:** Pydantic schemas for AI model feedback API data structures.
    
**Namespace:** creativeflow.mlops_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/mlops_service/services/__init__.py  
**Description:** Initializes the services package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** services/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for application services.  
**Logic Description:** Empty or imports key service classes.  
**Documentation:**
    
    - **Summary:** Package initializer for MLOps application services.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_registry_service.py  
**Description:** Service layer for managing AI Models and Model Versions in the registry.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_registry_service  
**Type:** Service  
**Relative Path:** services/model_registry_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** model_repo  
**Type:** ModelRepository  
**Attributes:** private  
    - **Name:** version_repo  
**Type:** ModelVersionRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_model  
**Parameters:**
    
    - model_data: AIModelCreate
    
**Return Type:** AIModel  
**Attributes:** public|async  
    - **Name:** get_model_by_id  
**Parameters:**
    
    - model_id: UUID
    
**Return Type:** Optional[AIModel]  
**Attributes:** public|async  
    - **Name:** get_models  
**Parameters:**
    
    - skip: int
    - limit: int
    
**Return Type:** List[AIModel]  
**Attributes:** public|async  
    - **Name:** create_model_version  
**Parameters:**
    
    - model_id: UUID
    - version_data: AIModelVersionCreate
    - artifact_path: str
    
**Return Type:** AIModelVersion  
**Attributes:** public|async  
    - **Name:** get_model_version_by_id  
**Parameters:**
    
    - version_id: UUID
    
**Return Type:** Optional[AIModelVersion]  
**Attributes:** public|async  
    - **Name:** update_version_status  
**Parameters:**
    
    - version_id: UUID
    - new_status: ModelVersionStatusEnum
    
**Return Type:** AIModelVersion  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model Registry Logic
    - Version Lifecycle Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Handles business logic for model registration, versioning, metadata storage, and lifecycle management.  
**Logic Description:** Contains methods for creating, retrieving, updating models and versions. Interacts with ModelRepository and ModelVersionRepository for data persistence. Manages model status transitions (e.g., staging to production).  
**Documentation:**
    
    - **Summary:** Service responsible for AI Model Registry operations.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_upload_service.py  
**Description:** Service for handling the upload of AI model artifacts.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_upload_service  
**Type:** Service  
**Relative Path:** services/model_upload_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** storage_adapter  
**Type:** MinioAdapter  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** upload_model_artifact  
**Parameters:**
    
    - file_stream: BinaryIO
    - file_name: str
    - model_id: UUID
    - version_string: str
    
**Return Type:** str  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model Artifact Upload
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Manages the process of uploading model files to object storage (MinIO).  
**Logic Description:** Receives model file stream, generates a unique path based on model ID and version, and uploads it to MinIO using the MinioAdapter. Returns the storage path.  
**Documentation:**
    
    - **Summary:** Service responsible for uploading AI model artifacts to storage.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_validation_service.py  
**Description:** Service for orchestrating AI model validation and security scanning.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_validation_service  
**Type:** Service  
**Relative Path:** services/model_validation_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** validation_repo  
**Type:** ValidationResultRepository  
**Attributes:** private  
    - **Name:** scanner_adapter  
**Type:** ScannerAdapter  
**Attributes:** private  
    - **Name:** version_repo  
**Type:** ModelVersionRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** initiate_validation  
**Parameters:**
    
    - model_version_id: UUID
    - config: ValidationRequestSchema
    
**Return Type:** ValidationResult  
**Attributes:** public|async  
    - **Name:** get_validation_result  
**Parameters:**
    
    - result_id: UUID
    
**Return Type:** Optional[ValidationResult]  
**Attributes:** public|async  
    - **Name:** perform_security_scan  
**Parameters:**
    
    - model_version: AIModelVersion
    
**Return Type:** ScanOutcome  
**Attributes:** private|async  
    - **Name:** perform_functional_validation  
**Parameters:**
    
    - model_version: AIModelVersion
    
**Return Type:** ValidationOutcome  
**Attributes:** private|async  
    
**Implemented Features:**
    
    - Model Validation Orchestration
    - Security Scanning Trigger
    - Functional Validation Trigger
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Orchestrates the validation pipeline for models including security scans, format checks, I/O tests, and content safety.  
**Logic Description:** Triggers security scans (e.g., Snyk/Clair via adapter). Performs functional tests (format compatibility, basic inference test). Stores validation results. Updates model version status based on validation outcome.  
**Documentation:**
    
    - **Summary:** Service responsible for managing and executing AI model validation processes.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_deployment_service.py  
**Description:** Service for managing AI model deployments to Kubernetes, including A/B testing.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_deployment_service  
**Type:** Service  
**Relative Path:** services/model_deployment_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** k8s_adapter  
**Type:** KubernetesAdapter  
**Attributes:** private  
    - **Name:** deployment_repo  
**Type:** DeploymentRepository  
**Attributes:** private  
    - **Name:** version_repo  
**Type:** ModelVersionRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** deploy_model_version  
**Parameters:**
    
    - version_id: UUID
    - deployment_config: DeploymentCreateSchema
    
**Return Type:** Deployment  
**Attributes:** public|async  
    - **Name:** get_deployment_details  
**Parameters:**
    
    - deployment_id: UUID
    
**Return Type:** Optional[Deployment]  
**Attributes:** public|async  
    - **Name:** update_deployment_strategy  
**Parameters:**
    
    - deployment_id: UUID
    - strategy_config: DeploymentUpdateSchema
    
**Return Type:** Deployment  
**Attributes:** public|async  
    - **Name:** rollback_deployment  
**Parameters:**
    
    - deployment_id: UUID
    
**Return Type:** Deployment  
**Attributes:** public|async  
    - **Name:** delete_deployment  
**Parameters:**
    
    - deployment_id: UUID
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model Deployment to K8s
    - Canary/Blue-Green Strategy Management
    - A/B Test Setup
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Handles logic for deploying models to Kubernetes, managing deployment strategies (canary, blue-green), configuring A/B tests.  
**Logic Description:** Interacts with KubernetesAdapter to deploy containerized models. Manages K8s manifests/configurations. Implements logic for traffic splitting for canary/A-B. Updates deployment status in the registry.  
**Documentation:**
    
    - **Summary:** Service responsible for AI model deployment and A/B test management.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_monitoring_service.py  
**Description:** Service stubs for defining how custom model monitoring metrics are configured or collected.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_monitoring_service  
**Type:** Service  
**Relative Path:** services/model_monitoring_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** k8s_adapter  
**Type:** KubernetesAdapter  
**Attributes:** private  
    - **Name:** prometheus_client  
**Type:** PrometheusClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_model_performance_metrics  
**Parameters:**
    
    - deployment_id: UUID
    - time_window: str
    
**Return Type:** Dict[str, Any]  
**Attributes:** public|async  
    - **Name:** check_for_model_drift  
**Parameters:**
    
    - deployment_id: UUID
    
**Return Type:** DriftReport  
**Attributes:** public|async  
    - **Name:** log_inference_request_response  
**Parameters:**
    
    - deployment_id: UUID
    - request_data: Any
    - response_data: Any
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Model Performance Data Retrieval
    - Model Drift Detection (Interface)
    - Input/Output Logging for Models
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Manages monitoring of deployed custom models for performance, drift, and resource usage. Logs inputs/outputs.  
**Logic Description:** Interfaces with monitoring systems (e.g., Prometheus via client, K8s metrics API) to fetch performance data. Implements logic for drift detection (could be complex or rely on external tools). Handles logging of model inputs/outputs ensuring PII scrubbing.  
**Documentation:**
    
    - **Summary:** Service for monitoring custom AI model performance and health.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/services/model_feedback_service.py  
**Description:** Service for managing user feedback related to AI models.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** model_feedback_service  
**Type:** Service  
**Relative Path:** services/model_feedback_service  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** feedback_repo  
**Type:** ModelFeedbackRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** submit_feedback  
**Parameters:**
    
    - feedback_data: ModelFeedbackCreate
    
**Return Type:** ModelFeedback  
**Attributes:** public|async  
    - **Name:** get_feedback_for_version  
**Parameters:**
    
    - model_version_id: UUID
    
**Return Type:** List[ModelFeedback]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Store Model Feedback
    - Retrieve Model Feedback
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Handles the collection, storage, and retrieval of user feedback on AI model outputs.  
**Logic Description:** Stores feedback submissions associated with specific model versions and generation requests. Provides methods to retrieve feedback for analysis and model retraining.  
**Documentation:**
    
    - **Summary:** Service responsible for managing user feedback on AI models.
    
**Namespace:** creativeflow.mlops_service.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/__init__.py  
**Description:** Initializes the database infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for database interaction components.  
**Logic Description:** Empty or imports base repository/ORM model classes.  
**Documentation:**
    
    - **Summary:** Package initializer for database infrastructure components.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/base_repository.py  
**Description:** Base repository class with common SQLAlchemy CRUD operations.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** base_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/base_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - GenericRepository
    
**Members:**
    
    - **Name:** db  
**Type:** Session  
**Attributes:** protected  
    - **Name:** model  
**Type:** Type[ModelType]  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** get  
**Parameters:**
    
    - id: Any
    
**Return Type:** Optional[ModelType]  
**Attributes:** public  
    - **Name:** get_multi  
**Parameters:**
    
    - skip: int = 0
    - limit: int = 100
    
**Return Type:** List[ModelType]  
**Attributes:** public  
    - **Name:** create  
**Parameters:**
    
    - obj_in: CreateSchemaType
    
**Return Type:** ModelType  
**Attributes:** public  
    - **Name:** update  
**Parameters:**
    
    - db_obj: ModelType
    - obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    
**Return Type:** ModelType  
**Attributes:** public  
    - **Name:** remove  
**Parameters:**
    
    - id: Any
    
**Return Type:** ModelType  
**Attributes:** public  
    
**Implemented Features:**
    
    - Generic CRUD Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides a generic base class for SQLAlchemy repositories with common CRUD methods.  
**Logic Description:** Implements common database operations (get by ID, get multiple, create, update, delete) using SQLAlchemy session and a generic model type.  
**Documentation:**
    
    - **Summary:** Base repository providing common data access patterns.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/__init__.py  
**Description:** Initializes the ORM models package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/orm_models/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for SQLAlchemy ORM models.  
**Logic Description:** Imports all SQLAlchemy ORM model classes.  
**Documentation:**
    
    - **Summary:** Package initializer for SQLAlchemy ORM models.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/ai_model_orm.py  
**Description:** SQLAlchemy ORM model for AI Models.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/orm_models/ai_model_orm  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** Column(UUIDType)  
**Attributes:** public|primary_key  
    - **Name:** name  
**Type:** Column(String)  
**Attributes:** public|unique|index  
    - **Name:** description  
**Type:** Column(Text)  
**Attributes:** public|nullable  
    - **Name:** task_type  
**Type:** Column(String)  
**Attributes:** public|index  
    - **Name:** owner_id  
**Type:** Column(UUIDType)  
**Attributes:** public|nullable  
    - **Name:** created_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** updated_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** versions  
**Type:** relationship  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model DB Schema
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the database table structure for AI Models using SQLAlchemy.  
**Logic Description:** SQLAlchemy model mapping to the `aimodels` table. Includes columns for ID, name, description, task type, owner, and timestamps. Defines relationship to AIModelVersionORM.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for storing AI Model metadata.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/ai_model_version_orm.py  
**Description:** SQLAlchemy ORM model for AI Model Versions.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_version_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/orm_models/ai_model_version_orm  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** Column(UUIDType)  
**Attributes:** public|primary_key  
    - **Name:** model_id  
**Type:** Column(UUIDType, ForeignKey('aimodels.id'))  
**Attributes:** public|index  
    - **Name:** version_string  
**Type:** Column(String)  
**Attributes:** public  
    - **Name:** description  
**Type:** Column(Text)  
**Attributes:** public|nullable  
    - **Name:** artifact_path  
**Type:** Column(String)  
**Attributes:** public  
    - **Name:** model_format  
**Type:** Column(String)  
**Attributes:** public  
    - **Name:** interface_type  
**Type:** Column(String)  
**Attributes:** public  
    - **Name:** parameters  
**Type:** Column(JSONB)  
**Attributes:** public|nullable  
    - **Name:** metrics  
**Type:** Column(JSONB)  
**Attributes:** public|nullable  
    - **Name:** status  
**Type:** Column(String)  
**Attributes:** public|index  
    - **Name:** created_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** model  
**Type:** relationship  
**Attributes:** public  
    - **Name:** deployments  
**Type:** relationship  
**Attributes:** public  
    - **Name:** validation_results  
**Type:** relationship  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Version DB Schema
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the database table structure for AI Model Versions using SQLAlchemy.  
**Logic Description:** SQLAlchemy model for `aimodelversions` table. Includes version string, artifact path, format, status, parameters, metrics, and foreign key to AIModelORM.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for storing AI Model Version metadata.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/deployment_orm.py  
**Description:** SQLAlchemy ORM model for Model Deployments.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** deployment_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/orm_models/deployment_orm  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** Column(UUIDType)  
**Attributes:** public|primary_key  
    - **Name:** model_version_id  
**Type:** Column(UUIDType, ForeignKey('aimodelversions.id'))  
**Attributes:** public|index  
    - **Name:** environment  
**Type:** Column(String)  
**Attributes:** public|index  
    - **Name:** status  
**Type:** Column(String)  
**Attributes:** public|index  
    - **Name:** deployment_strategy  
**Type:** Column(String)  
**Attributes:** public|nullable  
    - **Name:** endpoint_url  
**Type:** Column(String)  
**Attributes:** public|nullable  
    - **Name:** replicas  
**Type:** Column(Integer)  
**Attributes:** public|nullable  
    - **Name:** config  
**Type:** Column(JSONB)  
**Attributes:** public|nullable  
    - **Name:** deployed_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** model_version  
**Type:** relationship  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Deployment DB Schema
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the database table structure for Model Deployments using SQLAlchemy.  
**Logic Description:** SQLAlchemy model for `deployments` table. Tracks deployed model versions, environment, status, strategy, endpoint, and configuration.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for storing AI model deployment records.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/validation_result_orm.py  
**Description:** SQLAlchemy ORM model for Model Validation Results.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** validation_result_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/orm_models/validation_result_orm  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** Column(UUIDType)  
**Attributes:** public|primary_key  
    - **Name:** model_version_id  
**Type:** Column(UUIDType, ForeignKey('aimodelversions.id'))  
**Attributes:** public|index  
    - **Name:** scan_type  
**Type:** Column(String)  
**Attributes:** public  
    - **Name:** status  
**Type:** Column(String)  
**Attributes:** public|index  
    - **Name:** summary  
**Type:** Column(Text)  
**Attributes:** public|nullable  
    - **Name:** details_path  
**Type:** Column(String)  
**Attributes:** public|nullable  
    - **Name:** validated_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** model_version  
**Type:** relationship  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Validation Result DB Schema
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the database table structure for storing results of model validation.  
**Logic Description:** SQLAlchemy model for `validationresults` table. Stores validation type, status, summary, and link to detailed reports.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for storing AI model validation results.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/orm_models/model_feedback_orm.py  
**Description:** SQLAlchemy ORM model for Model Feedback.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** model_feedback_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/database/orm_models/model_feedback_orm  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** id  
**Type:** Column(UUIDType)  
**Attributes:** public|primary_key  
    - **Name:** model_version_id  
**Type:** Column(UUIDType, ForeignKey('aimodelversions.id'))  
**Attributes:** public|index  
    - **Name:** user_id  
**Type:** Column(UUIDType)  
**Attributes:** public|nullable|index  
    - **Name:** generation_request_id  
**Type:** Column(UUIDType)  
**Attributes:** public|nullable|index  
    - **Name:** rating  
**Type:** Column(Integer)  
**Attributes:** public|nullable  
    - **Name:** comment  
**Type:** Column(Text)  
**Attributes:** public|nullable  
    - **Name:** feedback_data  
**Type:** Column(JSONB)  
**Attributes:** public|nullable  
    - **Name:** submitted_at  
**Type:** Column(DateTime)  
**Attributes:** public  
    - **Name:** model_version  
**Type:** relationship  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Feedback DB Schema
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines the database table structure for storing user feedback on models.  
**Logic Description:** SQLAlchemy model for `modelfeedback` table. Stores feedback, rating, comments, associated model version, user, and generation request.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for storing user feedback on AI models.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.orm_models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/__init__.py  
**Description:** Initializes the database repositories package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/database/repositories/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for database repositories.  
**Logic Description:** Imports repository classes.  
**Documentation:**
    
    - **Summary:** Package initializer for SQLAlchemy repositories.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/model_repository.py  
**Description:** SQLAlchemy repository for AIModel entities.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** model_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/model_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_name  
**Parameters:**
    
    - name: str
    
**Return Type:** Optional[AIModelORM]  
**Attributes:** public  
    
**Implemented Features:**
    
    - AIModel DB Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides data access methods for AIModel entities using SQLAlchemy.  
**Logic Description:** Inherits from BaseRepository. Implements specific query methods for AIModelORM, such as find_by_name. Handles mapping between domain entity and ORM model if applicable.  
**Documentation:**
    
    - **Summary:** Repository for managing AIModel data in PostgreSQL.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/version_repository.py  
**Description:** SQLAlchemy repository for AIModelVersion entities.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** version_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/version_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_model_id_and_version_string  
**Parameters:**
    
    - model_id: UUID
    - version_string: str
    
**Return Type:** Optional[AIModelVersionORM]  
**Attributes:** public  
    - **Name:** list_by_model_id  
**Parameters:**
    
    - model_id: UUID
    
**Return Type:** List[AIModelVersionORM]  
**Attributes:** public  
    
**Implemented Features:**
    
    - AIModelVersion DB Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides data access methods for AIModelVersion entities.  
**Logic Description:** Inherits from BaseRepository. Implements specific queries for AIModelVersionORM, like finding by model ID and version string. Handles mapping if domain entities are separate.  
**Documentation:**
    
    - **Summary:** Repository for managing AIModelVersion data.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/deployment_repository.py  
**Description:** SQLAlchemy repository for Deployment entities.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** deployment_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/deployment_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** list_by_model_version_id  
**Parameters:**
    
    - model_version_id: UUID
    
**Return Type:** List[DeploymentORM]  
**Attributes:** public  
    - **Name:** list_by_environment  
**Parameters:**
    
    - environment: str
    
**Return Type:** List[DeploymentORM]  
**Attributes:** public  
    
**Implemented Features:**
    
    - Deployment DB Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides data access methods for Deployment entities.  
**Logic Description:** Inherits from BaseRepository. Implements specific queries for DeploymentORM. Handles mapping if domain entities are separate.  
**Documentation:**
    
    - **Summary:** Repository for managing Deployment data.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/validation_repository.py  
**Description:** SQLAlchemy repository for ValidationResult entities.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** validation_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/validation_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** list_by_model_version_id  
**Parameters:**
    
    - model_version_id: UUID
    
**Return Type:** List[ValidationResultORM]  
**Attributes:** public  
    
**Implemented Features:**
    
    - ValidationResult DB Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides data access methods for ValidationResult entities.  
**Logic Description:** Inherits from BaseRepository. Implements specific queries for ValidationResultORM. Handles mapping if domain entities are separate.  
**Documentation:**
    
    - **Summary:** Repository for managing ValidationResult data.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/database/repositories/feedback_repository.py  
**Description:** SQLAlchemy repository for ModelFeedback entities.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** feedback_repository  
**Type:** Repository  
**Relative Path:** infrastructure/database/repositories/feedback_repository  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** list_by_model_version_id  
**Parameters:**
    
    - model_version_id: UUID
    
**Return Type:** List[ModelFeedbackORM]  
**Attributes:** public  
    
**Implemented Features:**
    
    - ModelFeedback DB Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides data access methods for ModelFeedback entities.  
**Logic Description:** Inherits from BaseRepository. Implements specific queries for ModelFeedbackORM. Handles mapping if domain entities are separate.  
**Documentation:**
    
    - **Summary:** Repository for managing ModelFeedback data.
    
**Namespace:** creativeflow.mlops_service.infrastructure.database.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/infrastructure/storage/__init__.py  
**Description:** Initializes the storage infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/storage/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for object storage interaction.  
**Logic Description:** Empty.  
**Documentation:**
    
    - **Summary:** Package initializer for storage adapter components.
    
**Namespace:** creativeflow.mlops_service.infrastructure.storage  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/infrastructure/storage/minio_adapter.py  
**Description:** Adapter for interacting with MinIO object storage.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** minio_adapter  
**Type:** InfrastructureAdapter  
**Relative Path:** infrastructure/storage/minio_adapter  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** client  
**Type:** Minio  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** upload_file  
**Parameters:**
    
    - bucket_name: str
    - object_name: str
    - file_stream: BinaryIO
    - length: int
    - content_type: str
    
**Return Type:** str  
**Attributes:** public|async  
    - **Name:** download_file  
**Parameters:**
    
    - bucket_name: str
    - object_name: str
    
**Return Type:** Response  
**Attributes:** public|async  
    - **Name:** delete_file  
**Parameters:**
    
    - bucket_name: str
    - object_name: str
    
**Return Type:** None  
**Attributes:** public|async  
    - **Name:** generate_presigned_url  
**Parameters:**
    
    - bucket_name: str
    - object_name: str
    - expires: int
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - MinIO File Operations
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides an interface to MinIO for storing and retrieving model artifacts and other large files.  
**Logic Description:** Uses the MinIO Python SDK to perform operations like put_object, get_object, remove_object. Handles connection setup from config.  
**Documentation:**
    
    - **Summary:** Adapter for MinIO object storage interactions.
    
**Namespace:** creativeflow.mlops_service.infrastructure.storage  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/infrastructure/kubernetes/__init__.py  
**Description:** Initializes the Kubernetes infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/kubernetes/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for Kubernetes interaction.  
**Logic Description:** Empty.  
**Documentation:**
    
    - **Summary:** Package initializer for Kubernetes adapter components.
    
**Namespace:** creativeflow.mlops_service.infrastructure.kubernetes  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/infrastructure/kubernetes/k8s_adapter.py  
**Description:** Adapter for interacting with the Kubernetes API.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** k8s_adapter  
**Type:** InfrastructureAdapter  
**Relative Path:** infrastructure/kubernetes/k8s_adapter  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** core_v1_api  
**Type:** CoreV1Api  
**Attributes:** private  
    - **Name:** apps_v1_api  
**Type:** AppsV1Api  
**Attributes:** private  
    - **Name:** custom_objects_api  
**Type:** CustomObjectsApi  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** deploy_model_service  
**Parameters:**
    
    - deployment_manifest: Dict[str, Any]
    - namespace: str
    
**Return Type:** V1Deployment  
**Attributes:** public|async  
    - **Name:** delete_model_service  
**Parameters:**
    
    - deployment_name: str
    - namespace: str
    
**Return Type:** V1Status  
**Attributes:** public|async  
    - **Name:** get_deployment_status  
**Parameters:**
    
    - deployment_name: str
    - namespace: str
    
**Return Type:** Optional[V1DeploymentStatus]  
**Attributes:** public|async  
    - **Name:** create_service  
**Parameters:**
    
    - service_manifest: Dict[str, Any]
    - namespace: str
    
**Return Type:** V1Service  
**Attributes:** public|async  
    - **Name:** apply_custom_resource  
**Parameters:**
    
    - group: str
    - version: str
    - namespace: str
    - plural: str
    - body: Dict[str, Any]
    
**Return Type:** object  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Kubernetes Deployment Management
    - Service Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides an interface to Kubernetes for deploying and managing model serving containers.  
**Logic Description:** Uses the Kubernetes Python client library to interact with the K8s API. Methods for creating/updating/deleting Deployments, Services, Ingresses (if needed for A/B), and potentially CRDs for advanced serving platforms like Seldon/KServe.  
**Documentation:**
    
    - **Summary:** Adapter for Kubernetes API interactions.
    
**Namespace:** creativeflow.mlops_service.infrastructure.kubernetes  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/infrastructure/security_scanners/__init__.py  
**Description:** Initializes the security scanners infrastructure package.  
**Template:** Python Package Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** infrastructure/security_scanners/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for security scanner interaction.  
**Logic Description:** Empty.  
**Documentation:**
    
    - **Summary:** Package initializer for security scanner adapter components.
    
**Namespace:** creativeflow.mlops_service.infrastructure.security_scanners  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/infrastructure/security_scanners/scanner_adapter.py  
**Description:** Adapter for interacting with security scanning tools like Snyk or Clair.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** scanner_adapter  
**Type:** InfrastructureAdapter  
**Relative Path:** infrastructure/security_scanners/scanner_adapter  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    
**Methods:**
    
    - **Name:** scan_container_image  
**Parameters:**
    
    - image_name: str
    - tag: str
    
**Return Type:** ScanResult  
**Attributes:** public|async  
    - **Name:** scan_model_artifact  
**Parameters:**
    
    - artifact_path: str
    
**Return Type:** ScanResult  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Container Image Scanning
    - Model Artifact Scanning (if applicable)
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides an interface to trigger security scans for container images or model artifacts.  
**Logic Description:** Abstracts interaction with chosen security scanning tools (e.g., Snyk API, Clair CLI/API). This might involve triggering scans and parsing results. This could also be a client to a separate scanning service/pipeline.  
**Documentation:**
    
    - **Summary:** Adapter for security scanning tools.
    
**Namespace:** creativeflow.mlops_service.infrastructure.security_scanners  
**Metadata:**
    
    - **Category:** InfrastructureAdapter
    
- **Path:** src/creativeflow/mlops_service/utils/__init__.py  
**Description:** Initializes the utilities package.  
**Template:** Python Package Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils/__init__  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package for utility functions.  
**Logic Description:** Empty.  
**Documentation:**
    
    - **Summary:** Package initializer for common utilities.
    
**Namespace:** creativeflow.mlops_service.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/creativeflow/mlops_service/utils/logging_config.py  
**Description:** Configuration for application logging.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** logging_config  
**Type:** Utility  
**Relative Path:** utils/logging_config  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str = 'INFO'
    
**Return Type:** None  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Structured Logging Setup
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Configures structured logging for the MLOps service.  
**Logic Description:** Sets up Python's logging module for structured JSON logging. Configures log levels based on environment settings. May include correlation ID handling setup.  
**Documentation:**
    
    - **Summary:** Handles standardized logging configuration for the application.
    
**Namespace:** creativeflow.mlops_service.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/creativeflow/mlops_service/utils/exceptions.py  
**Description:** Custom exception classes for the MLOps service.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** Utility  
**Relative Path:** utils/exceptions  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** MLOpsServiceException  
**Type:** class (Exception)  
**Attributes:** public  
    - **Name:** ModelNotFoundException  
**Type:** class (MLOpsServiceException)  
**Attributes:** public  
    - **Name:** DeploymentFailedException  
**Type:** class (MLOpsServiceException)  
**Attributes:** public  
    - **Name:** ValidationFailedException  
**Type:** class (MLOpsServiceException)  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Exceptions
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines custom exceptions for specific error conditions within the MLOps service.  
**Logic Description:** Includes base MLOpsServiceException and specific exceptions like ModelNotFound, DeploymentFailed, ValidationFailed, etc., for better error handling and API responses.  
**Documentation:**
    
    - **Summary:** Custom exception classes for granular error handling.
    
**Namespace:** creativeflow.mlops_service.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/creativeflow/mlops_service/alembic/env.py  
**Description:** Alembic environment configuration script for database migrations.  
**Template:** Alembic Migration Script  
**Dependency Level:** 2  
**Name:** env  
**Type:** MigrationScript  
**Relative Path:** alembic/env  
**Repository Id:** REPO-MLOPS-SERVICE-001  
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
**Attributes:** public  
    
**Implemented Features:**
    
    - Alembic Configuration
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Configures the Alembic migration environment, sets up database connection, and defines how migrations are run.  
**Logic Description:** Standard Alembic env.py. Imports SQLAlchemy base metadata and configures the target database URL from application settings for online migrations.  
**Documentation:**
    
    - **Summary:** Alembic environment script for managing database schema migrations.
    
**Namespace:** creativeflow.mlops_service.alembic  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/mlops_service/alembic.ini  
**Description:** Configuration file for Alembic database migration tool.  
**Template:** Alembic Migration Script  
**Dependency Level:** 1  
**Name:** alembic  
**Type:** ConfigurationFile  
**Relative Path:** alembic.ini  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alembic Settings
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Contains settings for Alembic, such as the database URL and script location.  
**Logic Description:** Standard alembic.ini file. sqlalchemy.url will point to the database connection string, typically sourced from an environment variable. script_location points to the alembic directory.  
**Documentation:**
    
    - **Summary:** Configuration file for Alembic database migrations.
    
**Namespace:** creativeflow.mlops_service  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** requirements.txt  
**Description:** Lists Python package dependencies for the MLOps service.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyFile  
**Relative Path:** ../requirements.txt  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Specifies all Python dependencies required to run the application.  
**Logic Description:** A plain text file listing packages like fastapi, uvicorn, pydantic, sqlalchemy, psycopg2-binary, minio, kubernetes, python-jose[cryptography], passlib[bcrypt], python-multipart. Versions should be pinned.  
**Documentation:**
    
    - **Summary:** Python package dependencies.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** dev-requirements.txt  
**Description:** Lists Python package dependencies for development and testing.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** dev-requirements  
**Type:** DependencyFile  
**Relative Path:** ../dev-requirements.txt  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development Dependency Management
    
**Requirement Ids:**
    
    
**Purpose:** Specifies Python dependencies for development, like linters and test runners.  
**Logic Description:** A plain text file listing packages like pytest, pytest-asyncio, httpx, flake8, black, mypy, alembic. Often includes everything from requirements.txt.  
**Documentation:**
    
    - **Summary:** Python package dependencies for development.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** Dockerfile  
**Description:** Dockerfile for building a container image for the MLOps service.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** Dockerfile  
**Type:** BuildScript  
**Relative Path:** ../Dockerfile  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Defines instructions to build a Docker image for the FastAPI MLOps service.  
**Logic Description:** Multi-stage Dockerfile. First stage installs dependencies. Second stage copies application code and sets up the entrypoint to run Uvicorn with the FastAPI app.  
**Documentation:**
    
    - **Summary:** Instructions for building the MLOps service Docker image.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** entrypoint.sh  
**Description:** Entrypoint script for the Docker container.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** entrypoint  
**Type:** BuildScript  
**Relative Path:** ../entrypoint.sh  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Container Initialization
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Script executed when the Docker container starts. Handles pre-start tasks like running database migrations.  
**Logic Description:** Shell script that can run Alembic migrations (`alembic upgrade head`) before starting the Uvicorn server for the FastAPI application.  
**Documentation:**
    
    - **Summary:** Container entrypoint script, handling migrations and app startup.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment variables file.  
**Template:** Env File  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** ConfigurationFile  
**Relative Path:** ../.env.example  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Example Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Provides a template for required environment variables.  
**Logic Description:** Contains placeholder values for all environment variables defined in core/config.py, e.g., DATABASE_URL, MINIO_ENDPOINT, etc.  
**Documentation:**
    
    - **Summary:** Example environment variable definitions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** pyproject.toml  
**Description:** Python project configuration file (e.g., for Poetry or PEP 621).  
**Template:** TOML  
**Dependency Level:** 0  
**Name:** pyproject.toml  
**Type:** ConfigurationFile  
**Relative Path:** ../pyproject.toml  
**Repository Id:** REPO-MLOPS-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Metadata
    - Build System Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Defines project metadata, dependencies, and build system configuration (e.g. for Poetry, Flit, or Hatch).  
**Logic Description:** Specifies project name, version, description, authors. Lists dependencies and dev-dependencies. Configures tools like black, mypy, pytest if managed through pyproject.toml.  
**Documentation:**
    
    - **Summary:** Python project configuration adhering to PEP 517/518/621.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableMLflowRegistryIntegration
  - EnableAdvancedABTestingUI
  - EnableAutomatedSecurityScanningTrigger
  - EnableAutomatedPerformanceBenchmarking
  
- **Database Configs:**
  
  - MLOPS_DATABASE_URL
  - ALEMBIC_DATABASE_URL
  
- **External Service Configs:**
  
  - MINIO_ENDPOINT
  - MINIO_ACCESS_KEY
  - MINIO_SECRET_KEY
  - MINIO_MODEL_BUCKET_NAME
  - MINIO_VALIDATION_REPORTS_BUCKET_NAME
  - KUBERNETES_API_SERVER_URL
  - KUBERNETES_NAMESPACE_MODELS
  - KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH
  - SECURITY_SCANNER_API_ENDPOINT
  - SECURITY_SCANNER_API_KEY
  - MLFLOW_TRACKING_URI
  - MLFLOW_REGISTRY_URI
  
- **Application Settings:**
  
  - SERVICE_HOST
  - SERVICE_PORT
  - LOG_LEVEL
  - DEFAULT_MODEL_STATUS_ON_UPLOAD
  - DEFAULT_VALIDATION_PIPELINE_CONFIG
  


---

