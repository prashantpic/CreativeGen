# Software Design Specification: CreativeFlow.CreativeManagementService

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.CreativeManagementService`. This microservice is a core backend component of the CreativeFlow AI platform, responsible for managing creative elements such as Brand Kits, Workbenches, Projects, user-uploaded assets, AI-generated asset metadata, version control for creatives, and project templates. It interacts with a PostgreSQL database for metadata storage and MinIO for object storage of asset files.

### 1.2 Scope
This SDS covers the design of the `CreativeManagementService` including:
*   API endpoint definitions and data schemas.
*   Domain models representing creative entities.
*   Application service logic for managing these entities.
*   Data persistence strategies using SQLAlchemy for PostgreSQL.
*   Object storage interactions using the MinIO SDK.
*   Configuration and core dependencies.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **API**: Application Programming Interface
*   **CRUD**: Create, Read, Update, Delete
*   **Pydantic**: Python data validation library
*   **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper (ORM)
*   **MinIO**: High-performance, S3-compatible object storage
*   **JWT**: JSON Web Token
*   **SDS**: Software Design Specification
*   **PWA**: Progressive Web Application
*   **ORM**: Object-Relational Mapper
*   **VO**: Value Object
*   **DTO**: Data Transfer Object
*   **SRS**: Software Requirements Specification
*   **IaC**: Infrastructure as Code

## 2. System Overview
The `CreativeManagementService` acts as the central hub for all metadata and file references related to user's creative endeavors on the platform. It provides internal REST APIs consumed by other backend services or potentially an API Gateway.

Key functionalities include:
*   **Brand Kit Management**: Allowing Pro+ users to define and manage brand colors, fonts, and logos.
*   **Organizational Structure**: Managing Workbenches and Projects to help users organize their work.
*   **Asset Management**: Handling both user-uploaded source assets and metadata for AI-generated creatives. This includes storing files in MinIO and their metadata in PostgreSQL.
*   **Versioning**: Providing version control for creative assets and projects.
*   **Template Management**: Managing a library of system templates and user-saved private templates.

## 3. Design Considerations

### 3.1. Security
*   **Authentication**: Endpoints will require authentication. User context (ID, permissions) will be derived from JWTs provided by an upstream Auth Service or API Gateway, and made available via FastAPI dependencies.
*   **Authorization**: Service logic will enforce ownership and permissions (e.g., a user can only modify their own brand kits or projects, unless team features are involved and RBAC is applied).
*   **Input Validation**: Pydantic schemas will be used for strict input validation at the API layer.
*   **Secrets Management**: MinIO keys and other sensitive configurations will be loaded from environment variables, managed externally (e.g., HashiCorp Vault).
*   **Object Storage Security**: MinIO access will be restricted. Presigned URLs will be used for client-side asset downloads where appropriate to limit direct exposure of bucket structures or credentials.

### 3.2. Data Integrity
*   Database transactions will be used for operations modifying multiple related entities.
*   Foreign key constraints will be enforced at the database level.
*   Validation logic within domain models and application services will ensure data consistency.

### 3.3. Scalability
*   The service is designed to be stateless, allowing for horizontal scaling of FastAPI instances.
*   Database scalability will rely on PostgreSQL's capabilities (read replicas, connection pooling).
*   MinIO is inherently scalable.
*   Efficient querying and indexing strategies will be employed.

### 3.4. Extensibility
*   The use of domain models, repository patterns, and service layers promotes modularity, making it easier to add new features or modify existing ones.
*   API versioning will be used for public-facing aspects if this service directly exposes any, or assumed to be handled by an API Gateway.

## 4. Architectural Design

### 4.1. Service Architecture
The `CreativeManagementService` follows a layered architecture:
1.  **API Layer (Presentation)**: FastAPI routers and Pydantic schemas define RESTful endpoints and handle HTTP request/response processing, validation, and serialization.
2.  **Application Layer**: Application services orchestrate use cases, coordinating domain models and repositories. They contain business logic that is not part of a single domain entity.
3.  **Domain Layer**: Pydantic models represent domain entities (BrandKit, Project, Asset, etc.) and their intrinsic business rules. Abstract repository interfaces define data persistence contracts.
4.  **Infrastructure Layer**: Concrete implementations for data persistence (SQLAlchemy repositories), object storage (MinIO client wrappers), and other external service interactions.

### 4.2. Dependencies
*   **PostgreSQL**: Primary data store for metadata.
*   **MinIO**: Primary object store for asset files.
*   **Authentication Service / API Gateway**: For user authentication and passing user context.
*   **Shared Libraries**: For common utilities, base classes, or configurations.

## 5. Data Design

Data persistence will utilize PostgreSQL with SQLAlchemy ORM for metadata, and MinIO for file storage. Pydantic models will define the structure of domain entities in memory and for API communication.

### 5.1. Domain Models (Pydantic)
These models represent the core entities and value objects within the service's domain. They are used in the application and API layers. They largely reflect the database schema defined in `databaseDesign.json` for the relevant tables.

*   **`domain/models/brand_kit.py`**:
    *   `Color(BaseModel)`: `name: str`, `hex: str`, `variable: Optional[str] = None`
    *   `Font(BaseModel)`: `name: str`, `family: str`, `url: Optional[str] = None` (MinIO path for custom fonts)
    *   `Logo(BaseModel)`: `name: str`, `path: str` (MinIO path), `format: str`
    *   `BrandKit(BaseModel)`: `id: UUID`, `user_id: UUID`, `team_id: Optional[UUID] = None`, `name: str`, `colors: List[Color]`, `fonts: List[Font]`, `logos: Optional[List[Logo]] = None`, `style_preferences: Optional[dict] = None`, `is_default: bool = False`, `created_at: datetime`, `updated_at: datetime`
        *   Methods: `add_color()`, `remove_color()`, `update_font()`, `set_as_default()` (handles logic for ensuring only one default per scope).

*   **`domain/models/workbench.py`**:
    *   `Workbench(BaseModel)`: `id: UUID`, `user_id: UUID`, `name: str`, `default_brand_kit_id: Optional[UUID] = None`, `created_at: datetime`, `updated_at: datetime`

*   **`domain/models/project.py`**:
    *   `Project(BaseModel)`: `id: UUID`, `workbench_id: UUID`, `user_id: UUID`, `template_id: Optional[UUID] = None`, `brand_kit_id: Optional[UUID] = None`, `name: str`, `target_platform: Optional[str] = None`, `collaboration_state: Optional[dict] = None`, `last_collaborated_at: Optional[datetime] = None`, `created_at: datetime`, `updated_at: datetime`
        *   Methods for managing project-specific settings, linking assets.

*   **`domain/models/asset.py`**:
    *   `AssetType(str, Enum)`: `UPLOADED = "Uploaded"`, `AI_GENERATED = "AIGenerated"`, `DERIVED = "Derived"`
    *   `Asset(BaseModel)`: `id: UUID`, `project_id: Optional[UUID] = None`, `user_id: UUID`, `generation_request_id: Optional[UUID] = None`, `name: str`, `type: AssetType`, `file_path: str`, `mime_type: str`, `format: str`, `resolution: Optional[str] = None`, `is_final: bool = False`, `metadata: Optional[dict] = None`, `created_at: datetime`, `updated_at: datetime`, `deleted_at: Optional[datetime] = None`
        *   Methods for updating metadata, marking as final.

*   **`domain/models/asset_version.py`**:
    *   `AssetVersion(BaseModel)`: `id: UUID`, `asset_id: Optional[UUID] = None`, `project_id: Optional[UUID] = None`, `version_number: int`, `file_path: Optional[str] = None`, `state_data: Optional[dict] = None`, `description: Optional[str] = None`, `created_by_user_id: Optional[UUID] = None`, `created_at: datetime`

*   **`domain/models/template.py`**:
    *   `Template(BaseModel)`: `id: UUID`, `user_id: Optional[UUID] = None` (for private templates), `name: str`, `description: Optional[str] = None`, `category: str`, `preview_url: str`, `source_data: dict`, `tags: Optional[List[str]] = None`, `is_public: bool = True`, `created_at: datetime`, `updated_at: datetime`

*   **`domain/models/generation.py`**: (Reflects `GenerationRequest` from `databaseDesign.json`)
    *   `GenerationStatus(str, Enum)`: `PENDING = "Pending"`, `PROCESSING_SAMPLES = "ProcessingSamples"`, ...
    *   `SampleAssetMetadata(BaseModel)`: `asset_id: UUID`, `url: str`, `resolution: str`
    *   `Generation(BaseModel)`: `id: UUID`, `user_id: UUID`, `project_id: UUID`, `input_prompt: str`, `style_guidance: Optional[str] = None`, `input_parameters: Optional[dict] = None`, `status: GenerationStatus = GenerationStatus.PENDING`, `error_message: Optional[str] = None`, `sample_assets: Optional[List[SampleAssetMetadata]] = None`, `selected_sample_id: Optional[UUID] = None`, `final_asset_id: Optional[UUID] = None`, `credits_cost_sample: Optional[Decimal] = None`, `credits_cost_final: Optional[Decimal] = None`, `ai_model_used: Optional[str] = None`, `processing_time_ms: Optional[int] = None`, `created_at: datetime`, `updated_at: datetime`

### 5.2. Database Schema (SQLAlchemy ORM Models)
These models will reside in `infrastructure/persistence/sqlalchemy/models/` and map directly to PostgreSQL tables as defined in `databaseDesign.json`. They will use `SQLAlchemy`'s `Column`, `ForeignKey`, `relationship`, etc.

*   **`brand_kit_orm.py` (BrandKitTable)**: Mirrors `BrandKit` from `databaseDesign.json`.
    *   `id: Column(UUID, primary_key=True, default=uuid.uuid4)`
    *   `user_id: Column(UUID, ForeignKey("users.id"), index=True, nullable=False)` (Assuming a `users` table exists managed by Auth/User service, or a local simplified user reference if this service is highly decoupled)
    *   `team_id: Column(UUID, ForeignKey("teams.id"), index=True, nullable=True)`
    *   `name: Column(String(100), nullable=False)`
    *   `colors: Column(JSONB, nullable=False)`
    *   `fonts: Column(JSONB, nullable=False)`
    *   `logos: Column(JSONB, nullable=True)`
    *   `style_preferences: Column(JSONB, nullable=True)`
    *   `is_default: Column(Boolean, default=False, nullable=False)`
    *   `created_at: Column(DateTime, default=func.now(), nullable=False)`
    *   `updated_at: Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)`

*   **`workbench_orm.py` (WorkbenchTable)**: Mirrors `Workbench` from `databaseDesign.json`.
    *   Relationships to `ProjectTable` (one-to-many), `BrandKitTable` (many-to-one, optional for default).

*   **`project_orm.py` (ProjectTable)**: Mirrors `Project` from `databaseDesign.json`.
    *   Relationships to `WorkbenchTable` (many-to-one), `TemplateTable` (many-to-one, optional), `BrandKitTable` (many-to-one, optional for override), `AssetTable` (one-to-many), `AssetVersionTable` (one-to-many for project states).

*   **`asset_orm.py` (AssetTable)**: Mirrors `Asset` from `databaseDesign.json`.
    *   Relationships to `ProjectTable` (many-to-one, optional), `GenerationRequestTable` (many-to-one, optional), `UserTable` (many-to-one).

*   **`asset_version_orm.py` (AssetVersionTable)**: Mirrors `AssetVersion` from `databaseDesign.json`.
    *   Relationships to `AssetTable` (many-to-one, optional), `ProjectTable` (many-to-one, optional).

*   **`template_orm.py` (TemplateTable)**: Mirrors `Template` from `databaseDesign.json`.
    *   Relationship to `UserTable` (many-to-one, optional for private templates).

*   **`generation_orm.py` (GenerationRequestTable)**: Mirrors `GenerationRequest` from `databaseDesign.json`.
    *   Relationships to `UserTable`, `ProjectTable`, `AssetTable` (for `final_asset_id`).

### 5.3. Object Storage (MinIO)
*   Structure defined in SRS Section 7.4.1 will be strictly followed by `infrastructure/storage/asset_storage.py`.
    *   `users/{user_id}/brand_kits/{brand_kit_id}/logos/{logo_filename}`
    *   `users/{user_id}/brand_kits/{brand_kit_id}/fonts/{font_filename}`
    *   `users/{user_id}/projects/{project_id}/assets/{asset_id_or_type}/{filename_or_version}`
    *   `system/templates/{template_id}/{preview_or_asset_filename}`
    *   `users/{user_id}/private_templates/{template_id}/{preview_or_asset_filename}`
    *   `generations/{generation_request_id}/samples/{sample_asset_id}/{filename}`
    *   `generations/{generation_request_id}/final/{final_asset_id}/{filename}`

## 6. Interface Design

### 6.1. REST API Endpoints (Internal)
Exposed via FastAPI routers. All endpoints are prefixed with `/api/v1`. Authentication (deriving `current_user`) is assumed for all modification endpoints.

#### 6.1.1. Brand Kits (`api/v1/routers/brand_kits.py`)
*   `POST /brand-kits/`: Create a new brand kit.
    *   Request Body: `BrandKitCreateSchema`
    *   Response: `BrandKitResponseSchema` (201 Created)
*   `GET /brand-kits/`: List brand kits for the current user.
    *   Response: `List[BrandKitResponseSchema]`
*   `GET /brand-kits/{brand_kit_id}`: Get a specific brand kit.
    *   Response: `BrandKitResponseSchema`
*   `PUT /brand-kits/{brand_kit_id}`: Update a brand kit.
    *   Request Body: `BrandKitUpdateSchema`
    *   Response: `BrandKitResponseSchema`
*   `DELETE /brand-kits/{brand_kit_id}`: Delete a brand kit.
    *   Response: Status 204 No Content
*   `POST /brand-kits/{brand_kit_id}/set-default`: Set brand kit as default for user.
    *   Response: `BrandKitResponseSchema`

#### 6.1.2. Workbenches (`api/v1/routers/workbenches.py`)
*   `POST /workbenches/`: Create a new workbench.
    *   Request Body: `WorkbenchCreateSchema`
    *   Response: `WorkbenchResponseSchema`
*   `GET /workbenches/`: List workbenches for the current user.
    *   Response: `List[WorkbenchResponseSchema]`
*   `GET /workbenches/{workbench_id}`: Get a specific workbench.
    *   Response: `WorkbenchResponseSchema`
*   `PUT /workbenches/{workbench_id}`: Update a workbench.
    *   Request Body: `WorkbenchUpdateSchema`
    *   Response: `WorkbenchResponseSchema`
*   `DELETE /workbenches/{workbench_id}`: Delete a workbench.
    *   Response: Status 204 No Content

#### 6.1.3. Projects (`api/v1/routers/projects.py`)
*   `POST /projects/`: Create a new project.
    *   Request Body: `ProjectCreateSchema` (includes `workbench_id`)
    *   Response: `ProjectResponseSchema`
*   `GET /workbenches/{workbench_id}/projects/`: List projects within a workbench.
    *   Response: `List[ProjectResponseSchema]`
*   `GET /projects/{project_id}`: Get a specific project.
    *   Response: `ProjectResponseSchema`
*   `PUT /projects/{project_id}`: Update a project.
    *   Request Body: `ProjectUpdateSchema`
    *   Response: `ProjectResponseSchema`
*   `DELETE /projects/{project_id}`: Delete a project.
    *   Response: Status 204 No Content

#### 6.1.4. Assets (`api/v1/routers/assets.py`)
*   `POST /assets/upload`: Upload a new asset.
    *   Request Body: `file: UploadFile`, `project_id: Optional[UUID] = Form(None)`, `name: Optional[str] = Form(None)`
    *   Response: `AssetResponseSchema`
*   `GET /assets/{asset_id}`: Get asset metadata.
    *   Response: `AssetResponseSchema`
*   `GET /assets/{asset_id}/download-url`: Get a presigned URL for asset download.
    *   Response: `PresignedUrlResponseSchema`
*   `GET /projects/{project_id}/assets/`: List assets for a project.
    *   Response: `List[AssetResponseSchema]`
*   `DELETE /assets/{asset_id}`: Delete an asset.
    *   Response: Status 204 No Content
*   `POST /assets/{asset_id}/versions`: Create a new version of an asset.
    *   Request Body: `AssetVersionCreateSchema` (e.g., description, file if new upload)
    *   Response: `AssetVersionResponseSchema`
*   `GET /assets/{asset_id}/versions`: List versions of an asset.
    *   Response: `List[AssetVersionResponseSchema]`

#### 6.1.5. Templates (`api/v1/routers/templates.py`)
*   `GET /templates/public/`: List public templates.
    *   Parameters: `category: Optional[str]`, `keywords: Optional[str]`
    *   Response: `PaginatedResponse[TemplateResponseSchema]`
*   `GET /templates/private/`: List private templates for the current user.
    *   Response: `List[TemplateResponseSchema]`
*   `POST /templates/private/`: Create a new private template from a project/design.
    *   Request Body: `TemplateCreateSchema` (includes `source_project_id` or `source_data`)
    *   Response: `TemplateResponseSchema`
*   `GET /templates/{template_id}`: Get a specific template.
    *   Response: `TemplateResponseSchema`
*   `DELETE /templates/private/{template_id}`: Delete a private template.
    *   Response: Status 204 No Content

#### 6.1.6. Generations (Metadata) (`api/v1/routers/generations.py`)
*   `POST /generations/`: (Internal endpoint, likely called by AI Generation Orchestration Service) Record a new generation request.
    *   Request Body: `GenerationCreateSchema`
    *   Response: `GenerationResponseSchema`
*   `PUT /generations/{generation_id}`: (Internal endpoint) Update generation status/results.
    *   Request Body: `GenerationUpdateSchema`
    *   Response: `GenerationResponseSchema`
*   `GET /projects/{project_id}/generations/`: List generation history for a project.
    *   Response: `List[GenerationResponseSchema]`
*   `GET /generations/{generation_id}`: Get details of a specific generation request.
    *   Response: `GenerationResponseSchema`

### 6.2. API Data Schemas (Pydantic)
Located in `api/v1/schemas/`. Separate schemas for `Create`, `Update`, and `Response` will be defined for each resource, inheriting from a `Base` schema.
*   `brand_kit.py`: `BrandKitBaseSchema`, `BrandKitCreateSchema`, `BrandKitUpdateSchema`, `BrandKitResponseSchema`, `ColorSchema`, `FontSchema`, `LogoSchema`.
*   `workbench.py`: `WorkbenchBaseSchema`, `WorkbenchCreateSchema`, `WorkbenchUpdateSchema`, `WorkbenchResponseSchema`.
*   `project.py`: `ProjectBaseSchema`, `ProjectCreateSchema`, `ProjectUpdateSchema`, `ProjectResponseSchema`.
*   `asset.py`: `AssetBaseSchema`, `AssetResponseSchema`, `AssetUpdateSchema`, `PresignedUrlResponseSchema`.
*   `asset_version.py`: `AssetVersionBaseSchema`, `AssetVersionCreateSchema`, `AssetVersionResponseSchema`.
*   `template.py`: `TemplateBaseSchema`, `TemplateCreateSchema`, `TemplateResponseSchema`.
*   `generation.py`: `GenerationBaseSchema`, `GenerationCreateSchema`, `GenerationUpdateSchema`, `GenerationResponseSchema`, `SampleAssetMetadataSchema`.
*   `common.py`: `UserSchema` (for `current_user`), `MessageResponse`, `PaginatedResponse[T]`.

## 7. Component Design

### 7.1. `main.py`
*   Initializes FastAPI app.
*   Includes routers: `brand_kits_router`, `workbenches_router`, `projects_router`, `assets_router`, `templates_router`, `generations_router`.
*   Sets up CORS middleware, global exception handlers.
*   Potentially includes startup events (e.g., check MinIO bucket existence).

### 7.2. `core/config.py`
*   `Settings(BaseSettings)` class with fields:
    *   `DATABASE_URL: str`
    *   `MINIO_ENDPOINT: str`
    *   `MINIO_ACCESS_KEY: str`
    *   `MINIO_SECRET_KEY: SecretStr`
    *   `MINIO_BUCKET_ASSETS: str = "creativeflow-assets"`
    *   `MINIO_BUCKET_TEMPLATES: str = "creativeflow-templates"`
    *   `MINIO_BUCKET_BRANDKITS_LOGOS: str = "creativeflow-brandkits-logos"`
    *   `MINIO_BUCKET_BRANDKITS_FONTS: str = "creativeflow-brandkits-fonts"`
    *   `API_V1_STR: str = "/api/v1"`
    *   `JWT_SECRET_KEY: str` (if this service decodes tokens)
    *   `JWT_ALGORITHM: str = "HS256"`
*   `@lru_cache def get_settings(): return Settings()`

### 7.3. `core/dependencies.py`
*   `get_db_session()`: Yields a SQLAlchemy `Session` from `SessionLocal`, ensures `db.close()`.
*   `get_minio_client()`: Returns an initialized MinIO client instance.
*   `get_current_user(token: str = Depends(oauth2_scheme))`: Decodes JWT token (using `core.security`) to get `user_id`, `roles`, `subscription_tier`. Returns a simple `UserSchema` Pydantic model. Raises `HTTPException` if invalid.
*   Service getters: `get_brand_kit_service(db: Session = Depends(get_db_session)) -> BrandKitService: return BrandKitService(db=db)` (similar for other services, injecting repositories).
    *   `get_asset_service(db: Session = Depends(get_db_session), minio_client: Minio = Depends(get_minio_client)) -> AssetService: return AssetService(db=db, minio_client=minio_client, asset_storage_service=MinIOAssetStorage(minio_client, get_settings()))`

### 7.4. `core/security.py`
*   `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")` (tokenUrl is placeholder, actual auth is external).
*   `get_user_id_from_token(token: str) -> UUID`: Decodes token, returns user_id. Raises `HTTPException` for invalid tokens. (This logic might be more complex, involving calls to an Auth service for full user details if needed beyond basic ID).
*   Permission checking utilities might reside here or in services, e.g., `has_permission(user: UserSchema, resource: Any, action: str) -> bool`.

### 7.5. Application Services (`application/services/`)

#### 7.5.1. `BrandKitService`
*   Constructor: `__init__(self, brand_kit_repo: IBrandKitRepository, asset_storage_service: IAssetStorage)`
*   Methods:
    *   `create_brand_kit(user_id: UUID, data: BrandKitCreateSchema) -> BrandKit`: Validates data. Handles logo/font uploads by calling `asset_storage_service.upload_file` for each logo/font, storing resulting paths. Saves `BrandKit` via repository.
    *   `get_brand_kit_by_id(brand_kit_id: UUID, user_id: UUID) -> Optional[BrandKit]`: Retrieves, checks ownership.
    *   `list_brand_kits_by_user(user_id: UUID) -> List[BrandKit]`: Retrieves all brand kits for a user.
    *   `update_brand_kit(brand_kit_id: UUID, user_id: UUID, data: BrandKitUpdateSchema) -> BrandKit`: Retrieves, checks ownership, updates fields. Handles updates to logos/fonts (delete old, upload new if changed).
    *   `delete_brand_kit(brand_kit_id: UUID, user_id: UUID) -> None`: Retrieves, checks ownership. Deletes from DB. Deletes associated logo/font files from MinIO.
    *   `set_default_brand_kit(brand_kit_id: UUID, user_id: UUID) -> BrandKit`: Ensures only one default per user. Updates `is_default` flags.

#### 7.5.2. `AssetService`
*   Constructor: `__init__(self, asset_repo: IAssetRepository, asset_version_repo: IAssetVersionRepository, asset_storage_service: IAssetStorage)`
*   Methods:
    *   `upload_asset(user_id: UUID, file_content: bytes, filename: str, mime_type: str, project_id: Optional[UUID] = None, asset_type: AssetType = AssetType.UPLOADED) -> Asset`:
        *   Generates unique `asset_id`.
        *   Constructs MinIO path using `user_id`, `project_id` (if provided), `asset_id`, `filename` following SRS 7.4.1.
        *   Calls `asset_storage_service.upload_file()`.
        *   Creates and saves `Asset` metadata via `asset_repo`.
    *   `get_asset_by_id(asset_id: UUID, user_id: UUID) -> Optional[Asset]`: Retrieves metadata, checks ownership.
    *   `get_asset_download_url(asset_id: UUID, user_id: UUID) -> str`: Retrieves asset, checks ownership, generates presigned URL via `asset_storage_service`.
    *   `list_assets(user_id: UUID, project_id: Optional[UUID] = None) -> List[Asset]`: Lists assets, optionally filtered by project.
    *   `delete_asset(asset_id: UUID, user_id: UUID) -> None`: Checks ownership. Deletes metadata and file from MinIO via `asset_storage_service`. Handles deletion of associated versions.
    *   `create_asset_version(asset_id: UUID, user_id: UUID, description: Optional[str] = None, file_content: Optional[bytes] = None, filename: Optional[str] = None, mime_type: Optional[str] = None, state_data: Optional[dict] = None) -> AssetVersion`:
        *   Creates a new version record. If `file_content` is provided, uploads it to a versioned path in MinIO.
        *   Saves `AssetVersion` metadata.
    *   `list_asset_versions(asset_id: UUID, user_id: UUID) -> List[AssetVersion]`.
    *   `record_ai_generated_asset_metadata(...) -> Asset`: Called (e.g., by GenerationService or AI Orchestration via an event/callback) to create an Asset record for an AI-generated file already in MinIO.

#### 7.5.3. `ProjectService`
*   Constructor: `__init__(self, project_repo: IProjectRepository, workbench_repo: IWorkbenchRepository, template_repo: ITemplateRepository, brand_kit_repo: IBrandKitRepository)`
*   Methods:
    *   `create_project(user_id: UUID, data: ProjectCreateSchema) -> Project`: Validates `workbench_id` ownership. If `template_id` provided, loads template data. If `brand_kit_id` not provided, inherits from workbench default. Saves `Project`.
    *   `get_project_by_id(project_id: UUID, user_id: UUID) -> Optional[Project]`: Retrieves, checks ownership.
    *   `list_projects_by_workbench(workbench_id: UUID, user_id: UUID) -> List[Project]`: Retrieves, checks workbench ownership.
    *   `update_project(project_id: UUID, user_id: UUID, data: ProjectUpdateSchema) -> Project`: Retrieves, checks ownership, updates.
    *   `delete_project(project_id: UUID, user_id: UUID) -> None`: Retrieves, checks ownership. Deletes project and potentially associated assets (or marks them as unlinked, based on policy).

#### 7.5.4. `WorkbenchService`
*   Constructor: `__init__(self, workbench_repo: IWorkbenchRepository, brand_kit_repo: IBrandKitRepository)`
*   Methods: `create_workbench`, `get_workbench_by_id`, `list_workbenches_by_user`, `update_workbench`, `delete_workbench`. Logic similar to `ProjectService` for CRUD and ownership.

#### 7.5.5. `TemplateService`
*   Constructor: `__init__(self, template_repo: ITemplateRepository, asset_storage_service: IAssetStorage)`
*   Methods:
    *   `list_public_templates(category: Optional[str], keywords: Optional[str]) -> List[Template]`.
    *   `list_private_templates(user_id: UUID) -> List[Template]`.
    *   `create_private_template(user_id: UUID, data: TemplateCreateSchema) -> Template`: If `source_project_id` is given, fetch project state to populate `source_data`. If `preview_file` provided, upload to MinIO.
    *   `get_template_by_id(template_id: UUID, user_id: Optional[UUID] = None) -> Optional[Template]`: Checks if public or if user owns private.
    *   `delete_private_template(template_id: UUID, user_id: UUID) -> None`.

#### 7.5.6. `GenerationMetadataService`
*   Constructor: `__init__(self, generation_repo: IGenerationRepository, asset_repo: IAssetRepository)`
*   Methods:
    *   `create_generation_record(user_id: UUID, data: GenerationCreateSchema) -> Generation`.
    *   `update_generation_status(generation_id: UUID, status: GenerationStatus, sample_assets_metadata: Optional[List[SampleAssetMetadataSchema]] = None, final_asset_id: Optional[UUID] = None, error_message: Optional[str] = None, ...) -> Generation`. This method will also create `Asset` records for samples and final assets via `AssetService` if their metadata is passed in.
    *   `get_generation_by_id(generation_id: UUID, user_id: UUID) -> Optional[Generation]`.
    *   `list_generations_by_project(project_id: UUID, user_id: UUID) -> List[Generation]`.

### 7.6. Repository Interfaces (`domain/repositories.py`)
Define abstract methods for each repository interface as listed in the file structure. E.g., for `IBrandKitRepository`: `get_by_id`, `get_by_user_id`, `save`, `delete`, `find_default_by_user_id`.

### 7.7. SQLAlchemy Repositories (`infrastructure/persistence/sqlalchemy/repositories/`)
Implementations of the repository interfaces using SQLAlchemy.
*   Example for `BrandKitRepositoryImpl(IBrandKitRepository)`:
    *   `get_by_id(id: UUID) -> Optional[BrandKitDomainModel]`: `self._db.query(BrandKitTable).filter(BrandKitTable.id == id).first()` (map to domain model).
    *   `save(brand_kit_domain: BrandKitDomainModel) -> BrandKitDomainModel`: Convert domain model to ORM model, `self._db.add(orm_brand_kit)`, `self._db.commit()`, `self._db.refresh(orm_brand_kit)` (map back to domain model).

### 7.8. MinIO Storage (`infrastructure/storage/`)
#### 7.8.1. `minio_client.py`
*   Initialize MinIO client with settings from `core.config`.
*   Function `get_minio_client_instance()` for dependency injection.

#### 7.8.2. `asset_storage.py` (implements `IAssetStorage` interface)
*   `class MinIOAssetStorage(IAssetStorage):`
    *   Constructor: `__init__(self, client: Minio, settings: Settings)`
    *   `upload_file(...) -> str (object_path)`: Constructs path based on SRS 7.4.1. Uses `client.put_object()`.
    *   `get_presigned_url(object_path: str, expires_in_seconds: int = 3600) -> str`: Uses `client.presigned_get_object()`.
    *   `delete_file(object_path: str) -> None`: Uses `client.remove_object()`.
    *   `check_object_exists(object_path: str) -> bool`: Uses `client.stat_object()`.

## 8. Configuration Management
*   Environment variables are the primary source of configuration, parsed by Pydantic in `core/config.py`.
*   `.env.example` provides a template for local development.
*   Secrets (database passwords, MinIO keys, JWT secret) must be handled securely (e.g., injected via environment variables from a secret management system in production).

## 9. Error Handling
*   FastAPI's default exception handling will be used for standard HTTP errors.
*   Custom exception handlers can be added in `main.py` for specific domain or application errors to return appropriate HTTP status codes and error messages (e.g., `ResourceNotFound`, `PermissionDenied`).
*   Pydantic `ValidationError` will be automatically handled by FastAPI, returning 422 responses.
*   Service methods should raise specific exceptions (e.g., `BrandKitNotFoundException`, `AssetUploadFailedException`) which are then caught by API layer or global handlers.

## 10. Logging
*   Standard Python `logging` module configured in `main.py` or via FastAPI settings.
*   Log format should be structured (e.g., JSON) for easier parsing by log aggregation systems.
*   Include correlation IDs in logs for distributed tracing.
*   Log key events: API requests/responses, errors, significant business logic steps, interactions with MinIO/DB.
*   Configurable log levels (DEBUG, INFO, WARNING, ERROR) per environment.

## 11. Data Retention (REQ-4-011)
*   `AssetService` and `ProjectService` deletion methods must consider retention policies based on user subscription tier and asset type/age as per SRS 7.5.
*   For example, listing assets for deletion by a background job might be an internal method. Actual deletion upon request will check these rules.
    *   `AssetService.delete_asset()`: Before deleting, check if asset retention policy allows deletion (e.g., free user assets older than 12 months might be deletable, Pro user assets only if explicitly deleted and subscription inactive).
    *   `AssetVersionService`: Apply limits on version history for Free users (e.g., only keep last N versions or versions within X days).
    *   Generated samples (if stored as `Asset` entities of type `SAMPLE`) should have a shorter retention (e.g., 30 days if not promoted to final).
*   This service will *not* implement the automated purging cron jobs; it will provide the data and enforce rules on direct deletion calls. The actual scheduled cleanup is likely an Odoo or separate batch job responsibility.

## 12. Platform Specific Optimization (REQ-012)
*   `ProjectService` and `Project` domain model will store `target_platform_format` (e.g., "Instagram_Story_9x16").
*   The actual rendering/cropping/safe-zone display is primarily a frontend (UI-002) or AI generation engine concern. This service stores the user's intent and the selected format metadata.
*   API endpoints for projects will allow setting/getting this target format.

## 13. AI-Generated Asset Metadata
*   The `Generation` domain model (and corresponding ORM/table `GenerationRequestTable`) is key here.
*   When the AI Generation Orchestration Service completes a generation (samples or final), it (or a callback handler in this service) will call `GenerationMetadataService.update_generation_status()` with details, including paths to assets in MinIO and IDs of created `Asset` records.
*   `AssetService.record_ai_generated_asset_metadata()` will be used to create `Asset` entries for AI outputs.

This SDS provides a detailed blueprint for the `CreativeFlow.CreativeManagementService`. Implementation should follow these specifications closely, ensuring all requirements mapped to this service are fulfilled.