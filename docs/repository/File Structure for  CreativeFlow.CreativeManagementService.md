# Specification

# 1. Files

- **Path:** pyproject.toml  
**Description:** Python project configuration file using PEP 621 or for tools like Poetry. Defines project metadata, dependencies, and build system.  
**Template:** Python Project File  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Dependency Management
    - Build Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Manages project dependencies, build settings, and metadata for the Creative Management Service.  
**Logic Description:** Specifies project name, version, Python compatibility. Lists runtime dependencies like FastAPI, SQLAlchemy, Pydantic, MinIO SDK, and development dependencies like PyTest, linters. Configures build tool if not standard setuptools.  
**Documentation:**
    
    - **Summary:** Core project definition file for Python packaging and dependency management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment variables file. Provides a template for developers to create their local .env files for configuration.  
**Template:** Environment Variables Example  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:** ../  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Templating
    
**Requirement Ids:**
    
    
**Purpose:** Guides developers on required environment variables for running the service.  
**Logic Description:** Lists environment variables such as DATABASE_URL, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, AUTH_SERVICE_URL (if needed), etc., with placeholder or example values.  
**Documentation:**
    
    - **Summary:** Template for local environment configuration, not to be committed with actual secrets.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/creative_management_service/main.py  
**Description:** Main application file for the FastAPI service. Initializes the FastAPI app, includes routers, and sets up middleware.  
**Template:** Python FastAPI Main  
**Dependency Level:** 3  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway (consumed by clients)
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Initialization
    - API Routing Setup
    - Middleware Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Initializes and configures the FastAPI application, serving as the entry point for the microservice.  
**Logic Description:** Creates a FastAPI application instance. Includes API routers from the api.v1.routers package. Sets up CORS middleware, exception handlers, and any other global middleware. May include startup/shutdown event handlers for initializing/closing resources like database connections if not handled per-request.  
**Documentation:**
    
    - **Summary:** Bootstraps the Creative Management FastAPI service.
    
**Namespace:** creative_management_service  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creative_management_service/core/config.py  
**Description:** Handles application configuration loading using Pydantic's BaseSettings for type validation and environment variable parsing.  
**Template:** Python Pydantic Settings  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** core/config.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** MINIO_ENDPOINT  
**Type:** str  
**Attributes:**   
    - **Name:** MINIO_ACCESS_KEY  
**Type:** str  
**Attributes:**   
    - **Name:** MINIO_SECRET_KEY  
**Type:** SecretStr (Pydantic)  
**Attributes:**   
    - **Name:** MINIO_BUCKET_ASSETS  
**Type:** str  
**Attributes:**   
    - **Name:** MINIO_BUCKET_TEMPLATES  
**Type:** str  
**Attributes:**   
    - **Name:** API_V1_STR  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** functools.lru_cache  
    
**Implemented Features:**
    
    - Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** Defines and loads application settings from environment variables or .env files.  
**Logic Description:** Defines a Pydantic BaseSettings class `Settings` with fields for all required configurations (database connection strings, MinIO credentials, API prefixes, etc.). Uses environment variable names or a .env file for sourcing values. Provides a cached function `get_settings()` to access settings globally.  
**Documentation:**
    
    - **Summary:** Manages application configuration.
    
**Namespace:** creative_management_service.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creative_management_service/core/dependencies.py  
**Description:** Defines FastAPI dependencies for use in path operation functions, such as getting database sessions or service instances.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 2  
**Name:** dependencies  
**Type:** DependencyInjection  
**Relative Path:** core/dependencies.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:**   
    - **Name:** get_minio_client  
**Parameters:**
    
    
**Return Type:** Minio  
**Attributes:**   
    - **Name:** get_current_user  
**Parameters:**
    
    - token: str = Depends(oauth2_scheme)
    
**Return Type:** User  
**Attributes:**   
    - **Name:** get_brand_kit_service  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    
**Return Type:** BrandKitService  
**Attributes:**   
    - **Name:** get_asset_service  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    - minio_client: Minio = Depends(get_minio_client)
    
**Return Type:** AssetService  
**Attributes:**   
    
**Implemented Features:**
    
    - Dependency Injection Setup
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable dependencies for FastAPI endpoints, managing resource acquisition and release.  
**Logic Description:** Implements dependency provider functions for database sessions (using a context manager to ensure sessions are closed), MinIO client instances, and instances of application services. Handles authentication token validation to provide current user context if required by this service.  
**Documentation:**
    
    - **Summary:** Manages FastAPI dependency injection.
    
**Namespace:** creative_management_service.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creative_management_service/core/security.py  
**Description:** Contains security-related utility functions, such as JWT decoding or permission checks if not handled by a dedicated auth service or API gateway.  
**Template:** Python Security Utilities  
**Dependency Level:** 1  
**Name:** security  
**Type:** Utility  
**Relative Path:** core/security.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** oauth2_scheme  
**Type:** OAuth2PasswordBearer  
**Attributes:** static  
    
**Methods:**
    
    - **Name:** get_user_id_from_token  
**Parameters:**
    
    - token: str
    
**Return Type:** UUID  
**Attributes:**   
    - **Name:** verify_user_permission  
**Parameters:**
    
    - user_id: UUID
    - resource_id: UUID
    - permission_type: str
    
**Return Type:** bool  
**Attributes:**   
    
**Implemented Features:**
    
    - Token Introspection (if needed)
    - Basic Permission Utilities
    
**Requirement Ids:**
    
    - REQ-004
    - REQ-010
    - REQ-011
    
**Purpose:** Provides security helper functions for token processing and permission checks if handled within this service.  
**Logic Description:** Includes functions to decode JWTs (if this service validates them directly, otherwise interacts with an Auth service client), extract user information from tokens, and potentially helper functions for basic permission checks on resources managed by this service. This might be minimal if an API Gateway or Auth Service handles most security.  
**Documentation:**
    
    - **Summary:** Security utilities, primarily for user context from tokens.
    
**Namespace:** creative_management_service.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creative_management_service/domain/models/brand_kit.py  
**Description:** Domain model for BrandKit aggregate root, including value objects like Color, Font, Logo.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** brand_kit  
**Type:** DomainModel  
**Relative Path:** domain/models/brand_kit.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    - ValueObject
    
**Members:**
    
    - **Name:** Color  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    - **Name:** Font  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    - **Name:** Logo  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    - **Name:** BrandKit  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    - **Name:** BrandKit.add_color  
**Parameters:**
    
    - color: Color
    
**Return Type:** None  
**Attributes:** method  
    - **Name:** BrandKit.set_as_default  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** method  
    
**Implemented Features:**
    
    - Brand Kit Entity
    - Brand Color VO
    - Brand Font VO
    - Brand Logo VO
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Defines the structure and behavior of a brand kit and its components.  
**Logic Description:** BrandKit class (Pydantic model) with fields: id, user_id, team_id, name, colors (List[Color]), fonts (List[Font]), logos (List[Logo]), style_preferences, is_default. Color, Font, Logo as nested Pydantic models (Value Objects). Methods for business logic like adding elements, validation.  
**Documentation:**
    
    - **Summary:** Represents the BrandKit aggregate and its constituent elements.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/workbench.py  
**Description:** Domain model for Workbench aggregate root.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** workbench  
**Type:** DomainModel  
**Relative Path:** domain/models/workbench.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    
**Members:**
    
    - **Name:** Workbench  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    - **Name:** Workbench.update_name  
**Parameters:**
    
    - name: str
    
**Return Type:** None  
**Attributes:** method  
    - **Name:** Workbench.set_default_brand_kit  
**Parameters:**
    
    - brand_kit_id: UUID
    
**Return Type:** None  
**Attributes:** method  
    
**Implemented Features:**
    
    - Workbench Entity
    
**Requirement Ids:**
    
    - REQ-010
    - Section 3.3
    
**Purpose:** Defines the structure and behavior of a workbench.  
**Logic Description:** Workbench class (Pydantic model) with fields: id, user_id, name, default_brand_kit_id. Business logic methods.  
**Documentation:**
    
    - **Summary:** Represents the Workbench aggregate for organizing projects.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/project.py  
**Description:** Domain model for Project aggregate root.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** project  
**Type:** DomainModel  
**Relative Path:** domain/models/project.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    
**Members:**
    
    - **Name:** Project  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    - **Name:** Project.update_settings  
**Parameters:**
    
    - name: str
    - brand_kit_id: Optional[UUID]
    
**Return Type:** None  
**Attributes:** method  
    - **Name:** Project.add_asset  
**Parameters:**
    
    - asset_id: UUID
    
**Return Type:** None  
**Attributes:** method  
    
**Implemented Features:**
    
    - Project Entity
    
**Requirement Ids:**
    
    - REQ-010
    - REQ-012
    - Section 3.3
    
**Purpose:** Defines the structure and behavior of a creative project.  
**Logic Description:** Project class (Pydantic model) with fields: id, workbench_id, user_id, template_id, brand_kit_id, name, target_platform_format, collaboration_state. Methods for managing project settings and associated assets.  
**Documentation:**
    
    - **Summary:** Represents the Project aggregate, a container for creative assets and their generation context.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/asset.py  
**Description:** Domain model for Asset aggregate root (uploaded or AI-generated).  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** asset  
**Type:** DomainModel  
**Relative Path:** domain/models/asset.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    
**Members:**
    
    - **Name:** Asset  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    - **Name:** Asset.update_metadata  
**Parameters:**
    
    - name: str
    - metadata: dict
    
**Return Type:** None  
**Attributes:** method  
    - **Name:** Asset.mark_as_final  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** method  
    
**Implemented Features:**
    
    - Asset Entity
    
**Requirement Ids:**
    
    - REQ-011
    - Section 7.2
    
**Purpose:** Defines the structure and behavior of a creative asset.  
**Logic Description:** Asset class (Pydantic model) with fields: id, project_id, user_id, generation_request_id, name, type, file_path (MinIO), mime_type, format, resolution, is_final, metadata. Business logic for asset management.  
**Documentation:**
    
    - **Summary:** Represents a creative asset, either uploaded by a user or generated by AI.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/asset_version.py  
**Description:** Domain model for AssetVersion entity.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** asset_version  
**Type:** DomainModel  
**Relative Path:** domain/models/asset_version.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** AssetVersion  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Version Entity
    
**Requirement Ids:**
    
    - REQ-011
    - Section 7.2
    
**Purpose:** Defines the structure of an asset version.  
**Logic Description:** AssetVersion class (Pydantic model) with fields: id, asset_id, project_id, version_number, file_path (MinIO), state_data (JSONB for project state), description, created_by_user_id.  
**Documentation:**
    
    - **Summary:** Represents a specific version of a creative asset or project state.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/template.py  
**Description:** Domain model for Template aggregate root.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** template  
**Type:** DomainModel  
**Relative Path:** domain/models/template.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - AggregateRoot
    - Entity
    
**Members:**
    
    - **Name:** Template  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Template Entity
    
**Requirement Ids:**
    
    - REQ-010
    
**Purpose:** Defines the structure of a project template.  
**Logic Description:** Template class (Pydantic model) with fields: id, user_id (for private templates), name, description, category, preview_url, source_data (JSONB), tags, is_public.  
**Documentation:**
    
    - **Summary:** Represents a predefined or user-saved creative template.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/models/generation.py  
**Description:** Domain model for Generation entity, storing metadata about AI generation requests and their outcomes.  
**Template:** Python Pydantic Model  
**Dependency Level:** 0  
**Name:** generation  
**Type:** DomainModel  
**Relative Path:** domain/models/generation.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    
**Members:**
    
    - **Name:** Generation  
**Type:** BaseModel (Pydantic)  
**Attributes:** class  
    
**Methods:**
    
    - **Name:** Generation.update_status  
**Parameters:**
    
    - status: str
    - error_message: Optional[str]
    
**Return Type:** None  
**Attributes:** method  
    
**Implemented Features:**
    
    - AI Generation Metadata Entity
    
**Requirement Ids:**
    
    - Section 7.2
    
**Purpose:** Defines the structure and state of an AI creative generation process and its metadata.  
**Logic Description:** Generation class (Pydantic model) reflecting SRS 7.2.1 `generations` table: id, user_id, project_id, input_prompt, style_guidance, input_parameters, status, error_message, sample_assets (JSONB list of Asset references/metadata), selected_sample_id, final_asset_id, credits_cost_sample, credits_cost_final, ai_model_used, processing_time_ms.  
**Documentation:**
    
    - **Summary:** Represents metadata associated with an AI creative generation request.
    
**Namespace:** creative_management_service.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/domain/repositories.py  
**Description:** Defines abstract repository interfaces for domain aggregates.  
**Template:** Python ABC Interfaces  
**Dependency Level:** 0  
**Name:** repositories  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    - DependencyInversionPrinciple
    
**Members:**
    
    
**Methods:**
    
    - **Name:** IBrandKitRepository.get_by_id  
**Parameters:**
    
    - id: UUID
    
**Return Type:** Optional[BrandKit]  
**Attributes:** abstractmethod  
    - **Name:** IBrandKitRepository.save  
**Parameters:**
    
    - brand_kit: BrandKit
    
**Return Type:** BrandKit  
**Attributes:** abstractmethod  
    - **Name:** IWorkbenchRepository.get_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[Workbench]  
**Attributes:** abstractmethod  
    - **Name:** IProjectRepository.add  
**Parameters:**
    
    - project: Project
    
**Return Type:** Project  
**Attributes:** abstractmethod  
    - **Name:** IAssetRepository.find_by_project_id  
**Parameters:**
    
    - project_id: UUID
    
**Return Type:** List[Asset]  
**Attributes:** abstractmethod  
    - **Name:** IAssetVersionRepository.get_versions_for_asset  
**Parameters:**
    
    - asset_id: UUID
    
**Return Type:** List[AssetVersion]  
**Attributes:** abstractmethod  
    - **Name:** ITemplateRepository.list_public  
**Parameters:**
    
    
**Return Type:** List[Template]  
**Attributes:** abstractmethod  
    - **Name:** IGenerationRepository.get_by_project_id  
**Parameters:**
    
    - project_id: UUID
    
**Return Type:** List[Generation]  
**Attributes:** abstractmethod  
    
**Implemented Features:**
    
    - Repository Interfaces
    
**Requirement Ids:**
    
    - REQ-004
    - REQ-010
    - REQ-011
    - Section 7.2
    
**Purpose:** Specifies contracts for data persistence operations related to domain entities.  
**Logic Description:** Contains abstract base classes (ABCs) for repository interfaces: IBrandKitRepository, IWorkbenchRepository, IProjectRepository, IAssetRepository, IAssetVersionRepository, ITemplateRepository, IGenerationRepository. Each interface defines methods for CRUD operations and specific queries relevant to its aggregate.  
**Documentation:**
    
    - **Summary:** Abstract interfaces for data access layers.
    
**Namespace:** creative_management_service.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** src/creative_management_service/application/services/brand_kit_service.py  
**Description:** Application service for managing brand kits.  
**Template:** Python Application Service  
**Dependency Level:** 1  
**Name:** brand_kit_service  
**Type:** Service  
**Relative Path:** application/services/brand_kit_service.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** _brand_kit_repo  
**Type:** IBrandKitRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_brand_kit  
**Parameters:**
    
    - user_id: UUID
    - name: str
    - colors: List[dict]
    - ...
    
**Return Type:** BrandKit  
**Attributes:**   
    - **Name:** get_brand_kit  
**Parameters:**
    
    - brand_kit_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[BrandKit]  
**Attributes:**   
    - **Name:** update_brand_kit  
**Parameters:**
    
    - brand_kit_id: UUID
    - user_id: UUID
    - update_data: BrandKitUpdateSchema
    
**Return Type:** BrandKit  
**Attributes:**   
    - **Name:** delete_brand_kit  
**Parameters:**
    
    - brand_kit_id: UUID
    - user_id: UUID
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - Brand Kit CRUD Operations
    - Setting Default Brand Kit
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Orchestrates operations related to brand kits, interacting with domain models and repositories.  
**Logic Description:** Contains business logic for creating, retrieving, updating, and deleting brand kits. Validates user permissions (e.g., ownership). Interacts with IBrandKitRepository for persistence and potentially MinIO client for logo/font file handling if not just storing paths.  
**Documentation:**
    
    - **Summary:** Manages all use cases related to brand kits.
    
**Namespace:** creative_management_service.application.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creative_management_service/application/services/asset_service.py  
**Description:** Application service for managing assets, including uploads and AI-generated asset metadata.  
**Template:** Python Application Service  
**Dependency Level:** 1  
**Name:** asset_service  
**Type:** Service  
**Relative Path:** application/services/asset_service.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** _asset_repo  
**Type:** IAssetRepository  
**Attributes:** private  
    - **Name:** _minio_storage  
**Type:** MinIOAssetStorage  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** upload_asset  
**Parameters:**
    
    - user_id: UUID
    - project_id: Optional[UUID]
    - file_content: bytes
    - filename: str
    - mime_type: str
    
**Return Type:** Asset  
**Attributes:**   
    - **Name:** get_asset_details  
**Parameters:**
    
    - asset_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[Asset]  
**Attributes:**   
    - **Name:** list_assets_for_project  
**Parameters:**
    
    - project_id: UUID
    - user_id: UUID
    
**Return Type:** List[Asset]  
**Attributes:**   
    - **Name:** delete_asset  
**Parameters:**
    
    - asset_id: UUID
    - user_id: UUID
    
**Return Type:** None  
**Attributes:**   
    - **Name:** record_ai_generated_asset  
**Parameters:**
    
    - user_id: UUID
    - project_id: UUID
    - generation_request_id: UUID
    - file_path: str
    - name: str
    - ...
    
**Return Type:** Asset  
**Attributes:**   
    
**Implemented Features:**
    
    - Asset Upload
    - Asset Metadata Management
    - Asset History Tracking
    
**Requirement Ids:**
    
    - REQ-011
    - Section 7.2
    - Section 7.4.1
    
**Purpose:** Handles asset lifecycle, including uploads to MinIO and metadata persistence in PostgreSQL.  
**Logic Description:** Manages uploading assets to MinIO (using MinIOAssetStorage), creating/updating asset metadata in the database via IAssetRepository. Implements logic for recording AI-generated assets and linking them to generation requests. Enforces storage organization strategy.  
**Documentation:**
    
    - **Summary:** Orchestrates asset creation, retrieval, and deletion.
    
**Namespace:** creative_management_service.application.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creative_management_service/application/services/project_service.py  
**Description:** Application service for managing creative projects.  
**Template:** Python Application Service  
**Dependency Level:** 1  
**Name:** project_service  
**Type:** Service  
**Relative Path:** application/services/project_service.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - ApplicationService
    
**Members:**
    
    - **Name:** _project_repo  
**Type:** IProjectRepository  
**Attributes:** private  
    - **Name:** _workbench_repo  
**Type:** IWorkbenchRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** create_project  
**Parameters:**
    
    - user_id: UUID
    - workbench_id: UUID
    - name: str
    - template_id: Optional[UUID]
    - brand_kit_id: Optional[UUID]
    
**Return Type:** Project  
**Attributes:**   
    - **Name:** get_project  
**Parameters:**
    
    - project_id: UUID
    - user_id: UUID
    
**Return Type:** Optional[Project]  
**Attributes:**   
    - **Name:** list_projects_in_workbench  
**Parameters:**
    
    - workbench_id: UUID
    - user_id: UUID
    
**Return Type:** List[Project]  
**Attributes:**   
    - **Name:** update_project  
**Parameters:**
    
    - project_id: UUID
    - user_id: UUID
    - update_data: ProjectUpdateSchema
    
**Return Type:** Project  
**Attributes:**   
    
**Implemented Features:**
    
    - Project CRUD Operations
    - Linking Projects to Workbenches, Templates, BrandKits
    
**Requirement Ids:**
    
    - REQ-010
    - Section 3.3
    
**Purpose:** Manages the lifecycle of creative projects.  
**Logic Description:** Handles creation, retrieval, update, and deletion of projects. Validates associations with workbenches, brand kits, and templates. Interacts with IProjectRepository and potentially other repositories for validation.  
**Documentation:**
    
    - **Summary:** Orchestrates all use cases related to projects.
    
**Namespace:** creative_management_service.application.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creative_management_service/infrastructure/persistence/sqlalchemy/database.py  
**Description:** SQLAlchemy database engine, session management, and declarative base.  
**Template:** Python SQLAlchemy Setup  
**Dependency Level:** 1  
**Name:** database  
**Type:** DatabaseSetup  
**Relative Path:** infrastructure/persistence/sqlalchemy/database.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SQLALCHEMY_DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** engine  
**Type:** Engine  
**Attributes:**   
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:**   
    - **Name:** Base  
**Type:** DeclarativeMeta  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:**   
    
**Implemented Features:**
    
    - Database Connection Management
    - ORM Base Definition
    
**Requirement Ids:**
    
    
**Purpose:** Configures SQLAlchemy for database interaction.  
**Logic Description:** Initializes the SQLAlchemy engine using DATABASE_URL from config. Creates SessionLocal for generating database sessions. Defines Base for declarative ORM models. Provides `get_db` dependency for FastAPI.  
**Documentation:**
    
    - **Summary:** SQLAlchemy core setup for database access.
    
**Namespace:** creative_management_service.infrastructure.persistence.sqlalchemy  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creative_management_service/infrastructure/persistence/sqlalchemy/models/brand_kit.py  
**Description:** SQLAlchemy ORM model for BrandKit.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** brand_kit_orm  
**Type:** ORMModel  
**Relative Path:** infrastructure/persistence/sqlalchemy/models/brand_kit.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** static  
    - **Name:** id  
**Type:** Column(UUID)  
**Attributes:** primary_key=True  
    - **Name:** user_id  
**Type:** Column(UUID)  
**Attributes:** index=True  
    - **Name:** name  
**Type:** Column(String)  
**Attributes:**   
    - **Name:** colors  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** fonts  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** logos  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** style_preferences  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** is_default  
**Type:** Column(Boolean)  
**Attributes:** default=False  
    
**Methods:**
    
    
**Implemented Features:**
    
    - BrandKit Database Mapping
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Maps the BrandKit domain model to a PostgreSQL table.  
**Logic Description:** Defines the `brand_kits` table schema using SQLAlchemy declarative mapping. Includes columns for ID, user ID, name, colors, fonts, logos (as JSONB), style preferences, and default status. Reflects the `BrandKit` entity from databaseDesign.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM representation for BrandKits.
    
**Namespace:** creative_management_service.infrastructure.persistence.sqlalchemy.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creative_management_service/infrastructure/persistence/sqlalchemy/repositories/brand_kit_repository.py  
**Description:** SQLAlchemy implementation of IBrandKitRepository.  
**Template:** Python SQLAlchemy Repository  
**Dependency Level:** 2  
**Name:** brand_kit_repository_impl  
**Type:** RepositoryImplementation  
**Relative Path:** infrastructure/persistence/sqlalchemy/repositories/brand_kit_repository.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _db  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - id: UUID
    
**Return Type:** Optional[BrandKitDomainModel]  
**Attributes:**   
    - **Name:** save  
**Parameters:**
    
    - brand_kit: BrandKitDomainModel
    
**Return Type:** BrandKitDomainModel  
**Attributes:**   
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** List[BrandKitDomainModel]  
**Attributes:**   
    
**Implemented Features:**
    
    - BrandKit Data Access Logic
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Provides concrete data access operations for BrandKits using SQLAlchemy.  
**Logic Description:** Implements methods defined in `IBrandKitRepository`. Uses SQLAlchemy Session to interact with the `brand_kits` table. Handles mapping between ORM models and domain models if they differ significantly (otherwise can return ORM models to be mapped by service).  
**Documentation:**
    
    - **Summary:** SQLAlchemy-based repository for BrandKit persistence.
    
**Namespace:** creative_management_service.infrastructure.persistence.sqlalchemy.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creative_management_service/infrastructure/storage/minio_client.py  
**Description:** MinIO client initialization and configuration.  
**Template:** Python MinIO Client Setup  
**Dependency Level:** 1  
**Name:** minio_client_setup  
**Type:** StorageClientSetup  
**Relative Path:** infrastructure/storage/minio_client.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** minio_client  
**Type:** Minio  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_minio_client_instance  
**Parameters:**
    
    
**Return Type:** Minio  
**Attributes:**   
    
**Implemented Features:**
    
    - MinIO Client Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Configures and provides access to the MinIO client.  
**Logic Description:** Initializes the MinIO client using endpoint, access key, and secret key from application configuration (core.config). Ensures bucket existence if necessary (e.g., on startup). Provides a function to get the client instance for dependency injection.  
**Documentation:**
    
    - **Summary:** Handles MinIO client setup and configuration.
    
**Namespace:** creative_management_service.infrastructure.storage  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creative_management_service/infrastructure/storage/asset_storage.py  
**Description:** Implements asset storage operations using MinIO, adhering to defined bucket structures.  
**Template:** Python MinIO Storage Service  
**Dependency Level:** 2  
**Name:** asset_storage_minio  
**Type:** StorageService  
**Relative Path:** infrastructure/storage/asset_storage.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _client  
**Type:** Minio  
**Attributes:** private  
    - **Name:** _bucket_name_assets  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** upload_file  
**Parameters:**
    
    - user_id: UUID
    - project_id: UUID
    - asset_id: UUID
    - file_data: bytes
    - file_name: str
    - content_type: str
    
**Return Type:** str (object_path)  
**Attributes:**   
    - **Name:** get_file_url  
**Parameters:**
    
    - object_path: str
    
**Return Type:** str (presigned_url)  
**Attributes:**   
    - **Name:** delete_file  
**Parameters:**
    
    - object_path: str
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - MinIO File Operations
    
**Requirement Ids:**
    
    - REQ-011
    - Section 7.4.1
    
**Purpose:** Provides an abstraction for storing and retrieving asset files in MinIO.  
**Logic Description:** Implements an interface (e.g., IAssetStorage) for file operations. Constructs object paths based on SRS Section 7.4.1 (e.g., /users/{user_id}/projects/{project_id}/assets/{asset_id}/{filename}). Uses the MinIO client to perform put, get, delete operations. Handles presigned URL generation for downloads.  
**Documentation:**
    
    - **Summary:** Manages asset file persistence in MinIO object storage.
    
**Namespace:** creative_management_service.infrastructure.storage  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creative_management_service/api/v1/routers/brand_kits.py  
**Description:** FastAPI router for BrandKit related API endpoints.  
**Template:** Python FastAPI Router  
**Dependency Level:** 2  
**Name:** brand_kits_router  
**Type:** Controller  
**Relative Path:** api/v1/routers/brand_kits.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway (exposed through)
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** create_brand_kit_endpoint  
**Parameters:**
    
    - brand_kit_in: BrandKitCreateSchema
    - current_user: User = Depends(get_current_user)
    - service: BrandKitService = Depends(get_brand_kit_service)
    
**Return Type:** BrandKitResponseSchema  
**Attributes:** router.post  
    - **Name:** get_brand_kit_endpoint  
**Parameters:**
    
    - brand_kit_id: UUID
    - current_user: User = Depends(get_current_user)
    - service: BrandKitService = Depends(get_brand_kit_service)
    
**Return Type:** BrandKitResponseSchema  
**Attributes:** router.get  
    - **Name:** list_user_brand_kits_endpoint  
**Parameters:**
    
    - current_user: User = Depends(get_current_user)
    - service: BrandKitService = Depends(get_brand_kit_service)
    
**Return Type:** List[BrandKitResponseSchema]  
**Attributes:** router.get  
    
**Implemented Features:**
    
    - Brand Kit API Endpoints
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Exposes BrandKit management functionalities via a REST API.  
**Logic Description:** Defines FastAPI path operations for creating, retrieving, updating, listing, and deleting brand kits. Uses Pydantic schemas for request validation and response formatting. Depends on BrandKitService for business logic and get_current_user for authentication/authorization context.  
**Documentation:**
    
    - **Summary:** API endpoints for managing brand kits.
    
**Namespace:** creative_management_service.api.v1.routers  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creative_management_service/api/v1/schemas/brand_kit.py  
**Description:** Pydantic schemas for BrandKit API requests and responses.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 0  
**Name:** brand_kit_schemas  
**Type:** DTO  
**Relative Path:** api/v1/schemas/brand_kit.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ColorSchema  
**Type:** BaseModel  
**Attributes:** class  
    - **Name:** FontSchema  
**Type:** BaseModel  
**Attributes:** class  
    - **Name:** LogoSchema  
**Type:** BaseModel  
**Attributes:** class  
    - **Name:** BrandKitBaseSchema  
**Type:** BaseModel  
**Attributes:** class  
    - **Name:** BrandKitCreateSchema  
**Type:** BrandKitBaseSchema  
**Attributes:** class  
    - **Name:** BrandKitUpdateSchema  
**Type:** BrandKitBaseSchema  
**Attributes:** class  
    - **Name:** BrandKitResponseSchema  
**Type:** BrandKitBaseSchema  
**Attributes:** class (includes id, created_at, etc.)  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Brand Kit API Data Structures
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** Defines data structures for BrandKit API interactions.  
**Logic Description:** Pydantic models for BrandKit creation, update, and response. Includes nested schemas for Colors, Fonts, and Logos. Ensures data validation and serialization for API layer.  
**Documentation:**
    
    - **Summary:** Pydantic models for BrandKit data transfer objects.
    
**Namespace:** creative_management_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creative_management_service/api/v1/routers/assets.py  
**Description:** FastAPI router for Asset related API endpoints, including uploads.  
**Template:** Python FastAPI Router  
**Dependency Level:** 2  
**Name:** assets_router  
**Type:** Controller  
**Relative Path:** api/v1/routers/assets.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway (exposed through)
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    
**Methods:**
    
    - **Name:** upload_asset_endpoint  
**Parameters:**
    
    - project_id: Optional[UUID]
    - file: UploadFile
    - current_user: User = Depends(get_current_user)
    - service: AssetService = Depends(get_asset_service)
    
**Return Type:** AssetResponseSchema  
**Attributes:** router.post  
    - **Name:** get_asset_endpoint  
**Parameters:**
    
    - asset_id: UUID
    - current_user: User = Depends(get_current_user)
    - service: AssetService = Depends(get_asset_service)
    
**Return Type:** AssetResponseSchema  
**Attributes:** router.get  
    - **Name:** get_asset_download_url_endpoint  
**Parameters:**
    
    - asset_id: UUID
    - current_user: User = Depends(get_current_user)
    - service: AssetService = Depends(get_asset_service)
    
**Return Type:** PresignedUrlResponseSchema  
**Attributes:** router.get  
    
**Implemented Features:**
    
    - Asset API Endpoints
    - Asset Upload
    
**Requirement Ids:**
    
    - REQ-011
    
**Purpose:** Exposes Asset management functionalities via a REST API.  
**Logic Description:** Defines FastAPI path operations for uploading, retrieving metadata, and getting download URLs for assets. Uses AssetService for business logic.  
**Documentation:**
    
    - **Summary:** API endpoints for managing creative assets.
    
**Namespace:** creative_management_service.api.v1.routers  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creative_management_service/api/v1/schemas/asset.py  
**Description:** Pydantic schemas for Asset API requests and responses.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 0  
**Name:** asset_schemas  
**Type:** DTO  
**Relative Path:** api/v1/schemas/asset.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** AssetBaseSchema  
**Type:** BaseModel  
**Attributes:** class  
    - **Name:** AssetCreateSchema  
**Type:** AssetBaseSchema  
**Attributes:** class (internal use by service)  
    - **Name:** AssetUpdateSchema  
**Type:** AssetBaseSchema  
**Attributes:** class  
    - **Name:** AssetResponseSchema  
**Type:** AssetBaseSchema  
**Attributes:** class (includes id, created_at, file_path, etc.)  
    - **Name:** PresignedUrlResponseSchema  
**Type:** BaseModel  
**Attributes:** class (field: url)  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset API Data Structures
    
**Requirement Ids:**
    
    - REQ-011
    
**Purpose:** Defines data structures for Asset API interactions.  
**Logic Description:** Pydantic models for Asset creation, update, and response. Includes fields from the Asset domain model suitable for API exposure.  
**Documentation:**
    
    - **Summary:** Pydantic models for Asset data transfer objects.
    
**Namespace:** creative_management_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creative_management_service/api/v1/schemas/common.py  
**Description:** Pydantic schemas for common API responses or shared structures.  
**Template:** Python Pydantic Schema  
**Dependency Level:** 0  
**Name:** common_schemas  
**Type:** DTO  
**Relative Path:** api/v1/schemas/common.py  
**Repository Id:** REPO-CREATIVEMGMT-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** UserSchema  
**Type:** BaseModel  
**Attributes:** class (Represents user context, e.g., user_id)  
    - **Name:** MessageResponse  
**Type:** BaseModel  
**Attributes:** class (field: message: str)  
    - **Name:** PaginatedResponse  
**Type:** Generic[T], BaseModel  
**Attributes:** class (fields: items: List[T], total: int, page: int, size: int)  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Common API Data Structures
    
**Requirement Ids:**
    
    
**Purpose:** Defines shared Pydantic models used across multiple API endpoints.  
**Logic Description:** Includes schemas like UserSchema for representing authenticated user context derived from a token, MessageResponse for simple status messages, and PaginatedResponse for list endpoints.  
**Documentation:**
    
    - **Summary:** Shared Pydantic models for API consistency.
    
**Namespace:** creative_management_service.api.v1.schemas  
**Metadata:**
    
    - **Category:** Presentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_asset_versioning_deep_history
  - enable_advanced_template_recommendations
  
- **Database Configs:**
  
  - DATABASE_URL
  - MINIO_ENDPOINT
  - MINIO_ACCESS_KEY
  - MINIO_SECRET_KEY
  - MINIO_BUCKET_ASSETS
  - MINIO_BUCKET_TEMPLATES
  - MINIO_BUCKET_BRANDKITS_LOGOS
  - MINIO_BUCKET_BRANDKITS_FONTS
  


---

