# Software Design Specification: CreativeFlow.MLOpsService

## 1. Introduction

### 1.1 Purpose
This document outlines the software design for the `CreativeFlow.MLOpsService`. This service is a core component of the CreativeFlow AI platform, responsible for managing the complete lifecycle of custom AI models. Its primary functions include facilitating the upload, validation, versioning, deployment, monitoring, and feedback collection for AI models utilized within the platform. This service aims to provide a robust and automated MLOps pipeline, enabling administrators and designated enterprise users to integrate and manage their specialized AI models efficiently and securely.

### 1.2 Scope
The scope of this document is limited to the design of the `CreativeFlow.MLOpsService`. This includes its internal architecture, API interfaces, domain model, service logic, interactions with other platform components (PostgreSQL, MinIO, Kubernetes), and underlying infrastructure adapters. It covers functionalities related to:
*   AI Model and Model Version registration and management.
*   Model artifact storage and retrieval.
*   Model validation (security, functional, performance).
*   Model deployment to a Kubernetes-based GPU cluster, including strategies like canary and blue-green.
*   A/B testing configuration for deployed models.
*   Monitoring of deployed model performance and health.
*   Collection of user feedback on model outputs.

This document does not cover the design of the AI models themselves, the AI Generation Orchestration Service (which consumes models deployed by this MLOps service), or the detailed design of the Kubernetes cluster beyond the interaction points.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **MLOps**: Machine Learning Operations - A set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently.
*   **AI**: Artificial Intelligence
*   **API**: Application Programming Interface
*   **CRUD**: Create, Read, Update, Delete
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **DB**: Database
*   **DTO**: Data Transfer Object (often represented by Pydantic schemas in FastAPI)
*   **ERD**: Entity-Relationship Diagram
*   **GPU**: Graphics Processing Unit
*   **HTTP**: Hypertext Transfer Protocol
*   **JSON**: JavaScript Object Notation
*   **JWT**: JSON Web Token
*   **K8s**: Kubernetes
*   **MinIO**: S3-compatible object storage
*   **ORM**: Object-Relational Mapper (e.g., SQLAlchemy)
*   **PWA**: Progressive Web Application
*   **Pydantic**: Python data validation library
*   **REST**: Representational State Transfer
*   **SDS**: Software Design Specification
*   **SDK**: Software Development Kit
*   **SQL**: Structured Query Language
*   **SQLAlchemy**: SQL toolkit and ORM for Python
*   **SRS**: Software Requirements Specification
*   **TS**: TypeScript
*   **UUID**: Universally Unique Identifier
*   **UML**: Unified Modeling Language
*   **YAML**: YAML Ain't Markup Language
*   **MLflow**: Open-source platform for the machine learning lifecycle (optional for registry)
*   **ONNX**: Open Neural Network Exchange
*   **TensorFlow SavedModel**: A format for saving TensorFlow models.
*   **PyTorch TorchScript**: A way to create serializable and optimizable models from PyTorch code.
*   **Snyk/Clair**: Container security scanning tools.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.

### 1.4 References
*   CreativeFlow AI Software Requirements Specification (SRS)
    *   Section 9.3.1: Custom AI Model Hosting and MLOps Pipeline (INT-007)
    *   Section 11.1.1: Hosting Environment (DEP-001)
    *   Section 2.5: Legal & Business Constraints (Content Policies)
    *   Section 7.4.1: Object Storage Organization (MinIO)
    *   Section 8: Security Requirements
    *   NFRs related to performance, scalability, and reliability of AI model serving.
*   API Design Guidelines (Internal Document)
*   Database Schema Document (especially tables: `AIModel`, `AIModelVersion`, `AIModelDeployment`, `AIModelValidationResult`, `AIModelFeedback`)

## 2. System Overview

The `CreativeFlow.MLOpsService` is a Python-based microservice built using the FastAPI framework. It serves as the central platform for managing the lifecycle of custom AI models within the CreativeFlow ecosystem. Its key responsibilities include:

1.  **Model Registration & Versioning**: Allowing authorized users to register new AI models and manage multiple versions of each model, including metadata like parameters, metrics, and lineage.
2.  **Artifact Management**: Storing and retrieving model artifacts (e.g., serialized model files, configuration files) in a secure MinIO object storage.
3.  **Model Validation**: Orchestrating automated validation processes, including security scans (e.g., for embedded malicious code in container images or model files using tools like Snyk/Clair), functional validation (format checks, I/O compatibility), performance benchmarking, and adherence to content safety guidelines.
4.  **Model Deployment**: Managing the deployment of validated model versions as containerized services to the GPU-accelerated Kubernetes cluster. This includes supporting advanced deployment strategies like canary releases and blue-green deployments to minimize risk and enable A/B testing.
5.  **A/B Testing & Experimentation**: Providing capabilities for A/B testing different model versions or entirely new custom models, collecting performance metrics and user feedback to inform promotion decisions.
6.  **Monitoring & Observability**: Continuously monitoring deployed custom models for operational performance (latency, throughput, error rates), resource consumption, and potential model drift or degradation in output quality.
7.  **Feedback Loop**: Collecting user feedback on content generated by custom models to inform retraining or fine-tuning efforts.

The service exposes internal REST APIs for these MLOps tasks, which will be consumed by other platform services (e.g., AI Generation Orchestration Service for model discovery, administrative UIs). It relies on PostgreSQL for storing metadata (model registry, deployment status, validation results, feedback) and MinIO for storing model artifacts. Interaction with the Kubernetes cluster for model deployment and management is handled via the Kubernetes Python client.

## 3. Detailed Design

### 3.1 API Design (Internal REST API - v1)
The MLOps service will expose a versioned RESTful API (`/api/v1/mlops/`). Authentication for this internal API will be handled via service-to-service authentication mechanisms (e.g., API keys, mutual TLS, or JWTs issued by a central auth service, to be determined based on overall platform security architecture - placeholder: `core.security.verify_api_key`).

All API responses will be in JSON format. Standard HTTP status codes will be used.

#### 3.1.1 Models API (`/models`)
Manages AI Model definitions and their versions.

*   **Endpoint:** `POST /models`
    *   **Description:** Create a new AI Model entry.
    *   **Request Body:** `ModelCreateSchema` (name, description, task_type, owner_id)
    *   **Response Body:** `ModelResponseSchema`
    *   **Logic:** Creates a new model record in the database.
*   **Endpoint:** `GET /models/{model_id}`
    *   **Description:** Retrieve an AI Model by its ID.
    *   **Path Parameter:** `model_id: UUID`
    *   **Response Body:** `ModelResponseSchema`
    *   **Logic:** Fetches model details from the database.
*   **Endpoint:** `GET /models`
    *   **Description:** List all AI Models with pagination.
    *   **Query Parameters:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[ModelResponseSchema]`
    *   **Logic:** Retrieves a paginated list of models.
*   **Endpoint:** `POST /models/{model_id}/versions`
    *   **Description:** Create a new version for an existing AI Model and upload its artifact.
    *   **Path Parameter:** `model_id: UUID`
    *   **Form Data:**
        *   `version_details: ModelVersionCreateSchema` (version_string, description, model_format, interface_type, parameters)
        *   `file: UploadFile` (the model artifact)
    *   **Response Body:** `ModelVersionResponseSchema`
    *   **Logic:**
        1.  Calls `ModelUploadService` to store the artifact in MinIO.
        2.  Calls `ModelRegistryService` to create the model version record with the artifact path and other details.
        3.  Initial status typically 'STAGING' or 'PENDING_VALIDATION'.
*   **Endpoint:** `GET /models/versions/{version_id}`
    *   **Description:** Retrieve a specific AI Model Version by its ID.
    *   **Path Parameter:** `version_id: UUID`
    *   **Response Body:** `ModelVersionResponseSchema`
    *   **Logic:** Fetches model version details.
*   **Endpoint:** `GET /models/{model_id}/versions`
    *   **Description:** List all versions for a specific AI Model.
    *   **Path Parameter:** `model_id: UUID`
    *   **Query Parameters:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[ModelVersionResponseSchema]`
    *   **Logic:** Fetches all versions for the given model.
*   **Endpoint:** `PATCH /models/versions/{version_id}/status`
    *   **Description:** Update the status of an AI Model Version (e.g., promote to production, archive).
    *   **Path Parameter:** `version_id: UUID`
    *   **Request Body:** `ModelVersionStatusUpdateSchema` (new_status: `ModelVersionStatusEnum`)
    *   **Response Body:** `ModelVersionResponseSchema`
    *   **Logic:** Updates the status of the model version in the registry. May trigger further actions (e.g., undeploying archived models).

#### 3.1.2 Deployments API (`/deployments`)
Manages deployments of AI Model Versions to different environments.

*   **Endpoint:** `POST /deployments`
    *   **Description:** Create a new deployment for an AI Model Version.
    *   **Request Body:** `DeploymentCreateSchema` (model_version_id, environment, deployment_strategy, replicas, config for A/B testing)
    *   **Response Body:** `DeploymentResponseSchema`
    *   **Logic:**
        1.  Validates model version status (must be validated and suitable for deployment).
        2.  Calls `ModelDeploymentService` to orchestrate deployment to Kubernetes.
        3.  Creates a deployment record in the database.
*   **Endpoint:** `GET /deployments/{deployment_id}`
    *   **Description:** Get the status and details of a specific deployment.
    *   **Path Parameter:** `deployment_id: UUID`
    *   **Response Body:** `DeploymentResponseSchema`
    *   **Logic:** Fetches deployment record and potentially queries K8s for live status.
*   **Endpoint:** `GET /deployments`
    *   **Description:** List all deployments, filterable by model version or environment.
    *   **Query Parameters:** `model_version_id: Optional[UUID] = None`, `environment: Optional[str] = None`, `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[DeploymentResponseSchema]`
    *   **Logic:** Retrieves a list of deployments based on filters.
*   **Endpoint:** `PUT /deployments/{deployment_id}`
    *   **Description:** Update an existing deployment (e.g., change replica count, update A/B test traffic split).
    *   **Path Parameter:** `deployment_id: UUID`
    *   **Request Body:** `DeploymentUpdateSchema`
    *   **Response Body:** `DeploymentResponseSchema`
    *   **Logic:** Calls `ModelDeploymentService` to apply updates to the Kubernetes deployment and updates the database record.
*   **Endpoint:** `DELETE /deployments/{deployment_id}`
    *   **Description:** Delete/undeploy a model.
    *   **Path Parameter:** `deployment_id: UUID`
    *   **Response Body:** `204 No Content`
    *   **Logic:** Calls `ModelDeploymentService` to remove the deployment from Kubernetes and updates/archives the database record.

#### 3.1.3 Validation API (`/validation`)
Manages the validation process for AI Model Versions.

*   **Endpoint:** `POST /validation/versions/{version_id}/trigger`
    *   **Description:** Trigger a validation process for a specific model version.
    *   **Path Parameter:** `version_id: UUID`
    *   **Request Body:** `ValidationRequestSchema` (scan_types: List[str] e.g., "security", "functional", "performance")
    *   **Response Body:** `ValidationResultResponseSchema` (initial pending status)
    *   **Logic:** Calls `ModelValidationService` to initiate asynchronous validation tasks. Creates a validation result record.
*   **Endpoint:** `GET /validation/results/{result_id}`
    *   **Description:** Get the result of a specific validation run.
    *   **Path Parameter:** `result_id: UUID`
    *   **Response Body:** `ValidationResultResponseSchema`
    *   **Logic:** Fetches the validation result record.
*   **Endpoint:** `GET /validation/versions/{version_id}/results`
    *   **Description:** List all validation results for a specific model version.
    *   **Path Parameter:** `version_id: UUID`
    *   **Response Body:** `List[ValidationResultResponseSchema]`
    *   **Logic:** Fetches all validation results associated with the model version.

#### 3.1.4 Feedback API (`/feedback`)
Manages user feedback related to AI Models.

*   **Endpoint:** `POST /feedback`
    *   **Description:** Submit feedback for an AI Model Version or a specific generation.
    *   **Request Body:** `ModelFeedbackCreateSchema` (model_version_id, user_id (optional), generation_request_id (optional), rating, comment, feedback_data)
    *   **Response Body:** `ModelFeedbackResponseSchema`
    *   **Logic:** Calls `ModelFeedbackService` to store the feedback.
*   **Endpoint:** `GET /feedback/versions/{version_id}`
    *   **Description:** Retrieve all feedback for a specific AI Model Version.
    *   **Path Parameter:** `version_id: UUID`
    *   **Query Parameters:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[ModelFeedbackResponseSchema]`
    *   **Logic:** Fetches feedback records.

### 3.2 Domain Model / Entities (`domain/entities/`)
Pydantic models define the core data structures. These are used for internal data representation and can be distinct from API schemas or ORM models, though often they share many similarities.

*   **`AIModel`**:
    *   Attributes: `id: UUID`, `name: str`, `description: Optional[str]`, `task_type: str` (e.g., from `ModelTaskTypeEnum`), `owner_id: Optional[UUID]` (user or team ID), `created_at: datetime`, `updated_at: datetime`.
*   **`AIModelVersion`**:
    *   Attributes: `id: UUID`, `model_id: UUID` (FK to AIModel), `version_string: str`, `description: Optional[str]`, `artifact_path: str` (MinIO path), `model_format: ModelFormatEnum`, `interface_type: ServingInterfaceEnum` (e.g., TF_SERVING, CUSTOM_FASTAPI), `parameters: Optional[Dict[str, Any]]` (training/inference params), `metrics: Optional[Dict[str, Any]]` (e.g., accuracy, F1 from training), `status: ModelVersionStatusEnum`, `created_at: datetime`, `created_by_user_id: Optional[UUID]`.
*   **`Deployment`**:
    *   Attributes: `id: UUID`, `model_version_id: UUID` (FK to AIModelVersion), `environment: str` (e.g., "staging", "production"), `status: DeploymentStatusEnum`, `deployment_strategy: Optional[str]` (e.g., "blue_green", "canary"), `endpoint_url: Optional[str]`, `replicas: Optional[int]`, `config: Optional[Dict[str, Any]]` (e.g., K8s manifest snippets, A/B test config like traffic split), `deployed_at: datetime`, `deployed_by_user_id: Optional[UUID]`.
*   **`ValidationResult`**:
    *   Attributes: `id: UUID`, `model_version_id: UUID` (FK to AIModelVersion), `scan_type: str` (e.g., "security_container", "functional_io", "performance_benchmark", "content_safety"), `status: ValidationStatusEnum`, `summary: Optional[str]`, `details_path: Optional[str]` (MinIO path to full report), `validated_at: datetime`, `validated_by_user_id: Optional[UUID]`.
*   **`ModelFeedback`**:
    *   Attributes: `id: UUID`, `model_version_id: UUID` (FK to AIModelVersion), `user_id: Optional[UUID]`, `generation_request_id: Optional[UUID]`, `rating: Optional[int]` (1-5), `comment: Optional[str]`, `feedback_data: Optional[Dict[str, Any]]` (structured feedback), `submitted_at: datetime`.

#### Enums (`domain/enums.py`)
*   `ModelVersionStatusEnum(str, Enum)`: `STAGING`, `PENDING_VALIDATION`, `VALIDATION_FAILED`, `VALIDATED`, `PRODUCTION`, `DEPRECATED`, `ARCHIVED`.
*   `DeploymentStatusEnum(str, Enum)`: `REQUESTED`, `DEPLOYING`, `ACTIVE`, `INACTIVE_BLUEGREEN`, `ROLLING_OUT_CANARY`, `FAILED`, `ROLLED_BACK`, `DELETED`.
*   `ValidationStatusEnum(str, Enum)`: `PENDING`, `RUNNING`, `PASSED`, `FAILED`, `WARNING`, `SKIPPED`.
*   `ModelFormatEnum(str, Enum)`: `ONNX`, `TENSORFLOW_SAVEDMODEL`, `PYTORCH_TORCHSCRIPT`, `CUSTOM_PYTHON_CONTAINER`, `OTHER`.
*   `ServingInterfaceEnum(str, Enum)`: `TENSORFLOW_SERVING`, `TORCHSERVE`, `TRITON_INFERENCE_SERVER`, `CUSTOM_FASTAPI`, `CUSTOM_FLASK`.

### 3.3 Service Layer (`services/`)

#### 3.3.1 `ModelRegistryService`
*   **Responsibilities:** Business logic for model and version registration, metadata management, lifecycle state transitions.
*   **Methods:**
    *   `async def create_model(db: Session, model_in: ModelCreateSchema) -> AIModelORM`: Creates an `AIModel` record.
    *   `async def get_model_by_id(db: Session, model_id: UUID) -> Optional[AIModelORM]`: Retrieves an `AIModel`.
    *   `async def get_models(db: Session, skip: int, limit: int) -> List[AIModelORM]`: Lists `AIModel`s.
    *   `async def create_model_version(db: Session, model_id: UUID, version_in: ModelVersionCreateSchema, artifact_path: str, user_id: Optional[UUID]) -> AIModelVersionORM`: Creates an `AIModelVersion` record, linking it to the artifact and model. Sets initial status.
    *   `async def get_model_version_by_id(db: Session, version_id: UUID) -> Optional[AIModelVersionORM]`: Retrieves an `AIModelVersion`.
    *   `async def get_versions_for_model(db: Session, model_id: UUID, skip: int, limit: int) -> List[AIModelVersionORM]`: Lists versions for a model.
    *   `async def update_version_status(db: Session, version_id: UUID, new_status: ModelVersionStatusEnum, user_id: Optional[UUID]) -> AIModelVersionORM`: Updates the status of a model version. Implements logic for valid transitions.
*   **Dependencies:** `ModelRepository`, `ModelVersionRepository`.

#### 3.3.2 `ModelUploadService`
*   **Responsibilities:** Handles the secure upload of model artifacts to MinIO.
*   **Methods:**
    *   `async def upload_model_artifact(file_stream: BinaryIO, file_name: str, model_id: UUID, version_string: str, content_type: str) -> str`:
        *   Generates a unique object name/path in MinIO (e.g., `models/{model_id}/{version_string}/{file_name}`).
        *   Uses `MinioAdapter` to upload the file.
        *   Returns the full MinIO object path.
*   **Dependencies:** `MinioAdapter`, `core.config.Settings`.

#### 3.3.3 `ModelValidationService`
*   **Responsibilities:** Orchestrates model validation processes (security, functional, performance, content safety).
*   **Methods:**
    *   `async def initiate_validation(db: Session, version_id: UUID, validation_config: ValidationRequestSchema, user_id: Optional[UUID]) -> AIModelValidationResultORM`:
        *   Retrieves `AIModelVersionORM`.
        *   Creates a `AIModelValidationResultORM` record with `PENDING` status.
        *   Asynchronously triggers validation tasks based on `validation_config.scan_types`:
            *   If "security_container" or "security_artifact": call `ScannerAdapter.scan_container_image()` or `scan_model_artifact()`.
            *   If "functional_io": Perform basic format checks and I/O compatibility tests (logic to be defined, potentially involving dummy inference).
            *   If "performance_benchmark": Trigger performance tests (details TBD, might involve temporary deployment).
            *   If "content_safety": Run checks against platform content policies (details TBD).
        *   Updates `AIModelValidationResultORM` and `AIModelVersionORM.status` based on outcomes.
    *   `async def get_validation_result_by_id(db: Session, result_id: UUID) -> Optional[AIModelValidationResultORM]`: Retrieves a specific validation result.
    *   `async def get_results_for_version(db: Session, version_id: UUID) -> List[AIModelValidationResultORM]`: Retrieves all validation results for a version.
*   **Dependencies:** `ValidationResultRepository`, `ModelVersionRepository`, `ScannerAdapter`, `MinioAdapter` (to fetch artifact for scanning/validation), potentially `KubernetesAdapter` (for performance test deployments).

#### 3.3.4 `ModelDeploymentService`
*   **Responsibilities:** Manages model deployment to Kubernetes, including strategies like canary/blue-green and A/B testing.
*   **Methods:**
    *   `async def deploy_model_version(db: Session, version_id: UUID, deployment_config: DeploymentCreateSchema, user_id: Optional[UUID]) -> AIModelDeploymentORM`:
        *   Retrieves `AIModelVersionORM`. Checks if `status` is `VALIDATED` or `PRODUCTION`.
        *   Constructs Kubernetes deployment manifest (Deployment, Service, potentially Ingress/Istio rules for canary/blue-green/A-B) based on `deployment_config` and `AIModelVersion.interface_type` (e.g., TF Serving, TorchServe, custom FastAPI container).
        *   Uses `KubernetesAdapter` to apply manifests.
        *   Creates and returns `AIModelDeploymentORM` record with status `DEPLOYING` or `ACTIVE`.
    *   `async def get_deployment_by_id(db: Session, deployment_id: UUID) -> Optional[AIModelDeploymentORM]`: Retrieves deployment details.
    *   `async def list_deployments_for_version(db: Session, version_id: UUID, environment: Optional[str]) -> List[AIModelDeploymentORM]`: Lists deployments.
    *   `async def update_deployment(db: Session, deployment_id: UUID, deployment_update: DeploymentUpdateSchema, user_id: Optional[UUID]) -> AIModelDeploymentORM`:
        *   Updates K8s deployment (e.g., replica count, image for new version in blue-green, traffic split for canary).
        *   Updates `AIModelDeploymentORM` record.
    *   `async def delete_deployment(db: Session, deployment_id: UUID, user_id: Optional[UUID]) -> None`:
        *   Uses `KubernetesAdapter` to delete K8s resources.
        *   Updates `AIModelDeploymentORM` status to `DELETED` or archives it.
*   **Dependencies:** `DeploymentRepository`, `ModelVersionRepository`, `KubernetesAdapter`.

#### 3.3.5 `ModelMonitoringService`
*   **Responsibilities:** Interface for model performance/drift monitoring, input/output logging.
*   **Methods (primarily interfaces to external monitoring systems or logging pipelines):**
    *   `async def get_model_performance_metrics(deployment_id: UUID, time_window: str) -> Dict[str, Any]`: Retrieves metrics (latency, throughput, error_rate) from Prometheus/monitoring system for a given deployment.
    *   `async def check_for_model_drift(deployment_id: UUID) -> Dict[str, Any]`: Placeholder for drift detection logic. Could involve analyzing logged inputs/outputs or specialized drift detection tools.
    *   `async def log_inference_request_response(deployment_id: UUID, request_data: Any, response_data: Any, user_id: Optional[UUID]) -> None`: Logs inputs and outputs (ensuring PII scrubbing according to `NFR-006`) to a dedicated logging stream or database for auditing and retraining.
*   **Dependencies:** `KubernetesAdapter` (to identify model pods/services), Prometheus client library, centralized logging system.

#### 3.3.6 `ModelFeedbackService`
*   **Responsibilities:** Manages user-provided feedback on models.
*   **Methods:**
    *   `async def submit_feedback(db: Session, feedback_in: ModelFeedbackCreateSchema) -> AIModelFeedbackORM`: Stores feedback in the database.
    *   `async def get_feedback_for_model_version(db: Session, version_id: UUID, skip: int, limit: int) -> List[AIModelFeedbackORM]`: Retrieves feedback.
*   **Dependencies:** `ModelFeedbackRepository`.

### 3.4 Infrastructure Adapters (`infrastructure/`)

#### 3.4.1 Database (`infrastructure/database/`)
*   **ORM Models (`orm_models/`)**:
    *   `AIModelORM(Base)`: Maps to `aimodels` table. Fields: `id (UUID, PK)`, `name (String, unique)`, `description (Text, nullable)`, `task_type (String, index)`, `owner_id (UUID, nullable)`, `created_at (DateTime)`, `updated_at (DateTime)`. Relationship: `versions = relationship("AIModelVersionORM", back_populates="model")`.
    *   `AIModelVersionORM(Base)`: Maps to `aimodelversions` table. Fields: `id (UUID, PK)`, `model_id (UUID, FK(aimodels.id), index)`, `version_string (String)`, `description (Text, nullable)`, `artifact_path (String)` (MinIO path), `model_format (String)`, `interface_type (String)`, `parameters (JSONB, nullable)`, `metrics (JSONB, nullable)`, `status (String, index)`, `created_at (DateTime)`, `created_by_user_id (UUID, nullable)`. Relationships: `model = relationship("AIModelORM", back_populates="versions")`, `deployments = relationship("AIModelDeploymentORM", back_populates="model_version")`, `validation_results = relationship("AIModelValidationResultORM", back_populates="model_version")`, `feedbacks = relationship("AIModelFeedbackORM", back_populates="model_version")`.
    *   `AIModelDeploymentORM(Base)`: Maps to `aimodeldeployments` table. Fields: `id (UUID, PK)`, `model_version_id (UUID, FK(aimodelversions.id), index)`, `environment (String, index)`, `status (String, index)`, `deployment_strategy (String, nullable)`, `endpoint_url (String, nullable)`, `replicas (Integer, nullable)`, `config (JSONB, nullable)`, `deployed_at (DateTime)`, `deployed_by_user_id (UUID, nullable)`. Relationship: `model_version = relationship("AIModelVersionORM", back_populates="deployments")`.
    *   `AIModelValidationResultORM(Base)`: Maps to `aimodelvalidationresults` table. Fields: `id (UUID, PK)`, `model_version_id (UUID, FK(aimodelversions.id), index)`, `scan_type (String)`, `status (String, index)`, `summary (Text, nullable)`, `details_path (String, nullable)` (MinIO path to report), `validated_at (DateTime)`, `validated_by_user_id (UUID, nullable)`. Relationship: `model_version = relationship("AIModelVersionORM", back_populates="validation_results")`.
    *   `AIModelFeedbackORM(Base)`: Maps to `aimodelfeedback` table. Fields: `id (UUID, PK)`, `model_version_id (UUID, FK(aimodelversions.id), index)`, `user_id (UUID, nullable, index)`, `generation_request_id (UUID, nullable, index)`, `rating (Integer, nullable)`, `comment (Text, nullable)`, `feedback_data (JSONB, nullable)`, `submitted_at (DateTime)`. Relationship: `model_version = relationship("AIModelVersionORM", back_populates="feedbacks")`.
*   **Repositories (`repositories/`)**:
    *   `BaseRepository`: Generic CRUD operations (as defined in file structure).
    *   `ModelRepository(BaseRepository[AIModelORM])`: Specific methods like `async def get_by_name(db: Session, name: str) -> Optional[AIModelORM]`.
    *   `ModelVersionRepository(BaseRepository[AIModelVersionORM])`: Specific methods like `async def get_by_model_id_and_version_string(db: Session, model_id: UUID, version_string: str) -> Optional[AIModelVersionORM]`, `async def list_by_model_id(db: Session, model_id: UUID) -> List[AIModelVersionORM]`.
    *   `DeploymentRepository(BaseRepository[AIModelDeploymentORM])`: `async def list_by_model_version_id_and_env(db: Session, model_version_id: UUID, environment: str) -> List[AIModelDeploymentORM]`.
    *   `ValidationResultRepository(BaseRepository[AIModelValidationResultORM])`: `async def list_by_model_version_id(db: Session, model_version_id: UUID) -> List[AIModelValidationResultORM]`.
    *   `ModelFeedbackRepository(BaseRepository[AIModelFeedbackORM])`: `async def list_by_model_version_id(db: Session, model_version_id: UUID) -> List[AIModelFeedbackORM]`.

#### 3.4.2 Storage (`infrastructure/storage/minio_adapter.py`)
*   **Responsibilities:** Interface with MinIO for storing/retrieving model artifacts, validation reports.
*   **Key Methods:**
    *   `async def upload_file(self, bucket_name: str, object_name: str, file_stream: BinaryIO, length: int, content_type: str) -> str`: Uploads a file.
    *   `async def download_file_stream(self, bucket_name: str, object_name: str) -> StreamingResponse`: Downloads a file as a stream.
    *   `async def delete_file(self, bucket_name: str, object_name: str) -> None`: Deletes a file.
    *   `async def get_presigned_url(self, bucket_name: str, object_name: str, expires: timedelta = timedelta(hours=1)) -> str`: Generates a presigned URL for temporary access.
*   **Configuration:** `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, specific bucket names (e.g., `MINIO_MODEL_BUCKET_NAME`, `MINIO_VALIDATION_REPORTS_BUCKET_NAME`) from `core.config`.

#### 3.4.3 Kubernetes (`infrastructure/kubernetes/k8s_adapter.py`)
*   **Responsibilities:** Interact with the Kubernetes API to deploy, manage, and monitor model serving containers.
*   **Key Methods:**
    *   `async def apply_deployment(self, namespace: str, manifest: Dict[str, Any]) -> V1Deployment`: Creates or updates a K8s Deployment.
    *   `async def delete_deployment(self, namespace: str, name: str) -> V1Status`: Deletes a K8s Deployment.
    *   `async def get_deployment_status(self, namespace: str, name: str) -> Optional[V1DeploymentStatus]`: Gets deployment status.
    *   `async def apply_service(self, namespace: str, manifest: Dict[str, Any]) -> V1Service`: Creates or updates a K8s Service.
    *   `async def delete_service(self, namespace: str, name: str) -> V1Status`: Deletes a K8s Service.
    *   `async def get_pod_logs(self, namespace: str, pod_name: str, container_name: Optional[str] = None) -> str`: Retrieves logs from a pod.
    *   Methods for managing Ingress, Istio VirtualService/DestinationRule for advanced deployment strategies if applicable.
*   **Configuration:** Loads K8s config (in-cluster or from path specified in `core.config.KUBERNETES_CONFIG_PATH`). Uses `KUBERNETES_NAMESPACE_MODELS`.

#### 3.4.4 Security Scanners (`infrastructure/security_scanners/scanner_adapter.py`)
*   **Responsibilities:** Abstract interactions with security scanning tools (e.g., Snyk, Clair).
*   **Key Methods:**
    *   `async def scan_container_image(self, image_name_with_tag: str) -> Dict[str, Any]`: Triggers a scan on a container image and returns a summary of results (e.g., vulnerability counts by severity).
    *   `async def scan_model_artifact(self, artifact_minio_path: str, model_format: str) -> Dict[str, Any]`: If direct artifact scanning is supported/required, triggers it. This might be more complex and depend on the tool.
*   **Configuration:** `SECURITY_SCANNER_API_ENDPOINT`, `SECURITY_SCANNER_API_KEY` from `core.config`. The implementation will depend heavily on the chosen scanner's API/CLI.

### 3.5 Core Components (`core/`)
*   **`config.py`**:
    *   `Settings(BaseSettings)` class using Pydantic.
    *   Loads from `.env` file and environment variables.
    *   Variables: `DATABASE_URL`, `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_MODEL_BUCKET_NAME`, `MINIO_VALIDATION_REPORTS_BUCKET_NAME`, `KUBERNETES_CONFIG_PATH` (optional), `KUBERNETES_NAMESPACE_MODELS`, `SECURITY_SCANNER_API_ENDPOINT` (optional), `SECURITY_SCANNER_API_KEY` (optional, Pydantic `SecretStr`), `MLFLOW_TRACKING_URI` (optional, if MLflow is used for registry/tracking), `LOG_LEVEL`.
*   **`security.py`**:
    *   Primarily focused on internal service-to-service authentication/authorization if this service is called by others. If this service calls other internal services that require auth, it would also handle client-side auth.
    *   `async def get_current_service_principal(...)`: Placeholder for authenticating incoming requests from other services.
    *   RBAC checks for MLOps operations if roles like "MLOpsAdmin", "EnterpriseModelManager" are defined.

### 3.6 Database (`database.py`, Alembic)
*   `database.py`:
    *   `engine = create_engine(settings.DATABASE_URL)`
    *   `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`
    *   `def get_db(): ...` FastAPI dependency.
*   Alembic (`alembic/`, `alembic.ini`):
    *   Standard Alembic setup for managing schema migrations based on changes in `infrastructure/database/orm_models/`.
    *   `env.py` configured to use `Base.metadata` from ORM models and `settings.DATABASE_URL`.

### 3.7 Utilities (`utils/`)
*   **`logging_config.py`**:
    *   `setup_logging(log_level: str)`: Configures Python's `logging` module.
    *   Uses `python-json-logger` or similar for structured JSON logs.
    *   Includes timestamp, level, message, service name (`mlops-service`), and potentially correlation IDs if passed via request headers.
*   **`exceptions.py`**:
    *   `MLOpsServiceException(HTTPException)`: Base for service-specific errors.
    *   `ModelNotFoundException(MLOpsServiceException)`: Status 404.
    *   `ModelVersionNotFoundException(MLOpsServiceException)`: Status 404.
    *   `DeploymentFailedException(MLOpsServiceException)`: Status 500 or specific (e.g., 400 if bad config).
    *   `ValidationFailedException(MLOpsServiceException)`: Status 400 (if user input caused) or 500.
    *   `ArtifactUploadFailedException(MLOpsServiceException)`: Status 500.
    *   FastAPI exception handlers in `main.py` to convert these into appropriate HTTP responses.

### 3.8 Main Application (`main.py`)
*   `app = FastAPI(...)`
*   Routers from `api.v1.endpoints` are included: `models_api.router`, `deployments_api.router`, etc.
*   `on_startup` events:
    *   Initialize database connection pool (implicitly handled by SQLAlchemy engine setup).
    *   Initialize MinIO client.
    *   Initialize Kubernetes client.
    *   Initialize Security Scanner client (if applicable).
*   `on_shutdown` events:
    *   Graceful shutdown of connections.
*   Middleware for request logging, correlation ID handling, error handling.

## 4. Data Management
*   **Model Artifacts**: Stored in MinIO. Paths are referenced in `AIModelVersionORM.artifact_path`. Bucket: `settings.MINIO_MODEL_BUCKET_NAME`.
*   **Validation Reports**: Detailed reports from security/functional scans stored in MinIO. Paths referenced in `AIModelValidationResultORM.details_path`. Bucket: `settings.MINIO_VALIDATION_REPORTS_BUCKET_NAME`.
*   **Metadata**: All other MLOps entities (models, versions, deployments, validation summaries, feedback) stored in PostgreSQL, managed by SQLAlchemy ORM.
*   **Data Validation**: Pydantic used for API request/response validation and for domain entity integrity.
*   **Data Retention**: Not explicitly managed by this service; relies on platform-wide data retention policies (SRS 7.5) which might involve external cron jobs or Odoo processes for cleanup. This service should allow "soft delete" or "archival" statuses.

## 5. Deployment and Operations (`Dockerfile`, `entrypoint.sh`, `requirements.txt`)
*   **`Dockerfile`**:
    *   Multi-stage build.
    *   Stage 1: Python base image, install `poetry` (if `pyproject.toml` used) or `pip`, install dependencies from `requirements.txt` / `pyproject.toml`.
    *   Stage 2: Slim Python image, copy installed dependencies and application code from Stage 1.
    *   Expose port (e.g., 8000).
    *   Set `entrypoint.sh` as entrypoint.
*   **`entrypoint.sh`**:
    *   `#!/bin/sh`
    *   `echo "Running Alembic migrations..."`
    *   `alembic upgrade head`
    *   `echo "Starting MLOps Service..."`
    *   `uvicorn creativeflow.mlops_service.main:app --host ${SERVICE_HOST:-0.0.0.0} --port ${SERVICE_PORT:-8000} --workers ${UVICORN_WORKERS:-1}` (workers count can be configured)
*   **`requirements.txt` / `dev-requirements.txt` / `pyproject.toml`**:
    *   `requirements.txt`: `fastapi`, `uvicorn[standard]`, `pydantic`, `SQLAlchemy`, `psycopg2-binary`, `minio`, `kubernetes`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `alembic`, `python-json-logger`. Optional: `mlflow-skinny` (if MLflow registry is used).
    *   `dev-requirements.txt`: `pytest`, `pytest-asyncio`, `httpx`, `flake8`, `black`, `mypy`, `isort`.
    *   `pyproject.toml`: If Poetry or modern PEP 621 build system is used, dependencies will be here.

## 6. Integration Points
*   **PostgreSQL Database (`REPO-POSTGRES-DB-001`)**: For all metadata storage.
    *   Interface: SQLAlchemy ORM, direct SQL.
*   **MinIO Object Storage (`REPO-MINIO-STORAGE-001`)**: For model artifacts and validation reports.
    *   Interface: MinIO Python SDK.
*   **Kubernetes AI Serving Cluster (`REPO-K8S-AI-SERVING-001`)**: For deploying and managing model serving instances.
    *   Interface: Kubernetes Python Client API.
*   **Shared Libraries (`REPO-SHARED-LIBS-001`)**: For common utilities, potentially custom auth client, Pydantic base models, etc.
    *   Interface: Python package imports.
*   **Security Scanning Tools (External/Internal Service)**: Snyk, Clair, or similar.
    *   Interface: `ScannerAdapter` (API or CLI calls).
*   **MLflow Registry (Optional, External/Internal Service)**: If MLflow is chosen for the model registry.
    *   Interface: MLflow Python Client API.
*   **Consumers**: Other backend services (e.g., AI Generation Orchestration Service) will call this service's API to list/get model versions and deployment endpoints. Administrative UIs will use its API for management.

## 7. Security Considerations
*   **Artifact Security**: Model artifacts in MinIO should have restricted access. Presigned URLs for temporary download if needed.
*   **Model Validation**: Mandatory security scanning for uploaded models/containers (AISIML-009).
*   **API Security**: Internal API should be protected (e.g., network policies, service mesh authentication, API keys).
*   **Kubernetes Security**: Secure communication with K8s API server. RBAC for service account used by MLOps service to interact with K8s. Pod Security Policies / Admission Controllers for deployed models.
*   **Database Security**: Credentials managed via secrets management. Limited privileges for the service account.
*   **Secrets Management**: All credentials (DB, MinIO, K8s, Scanner API keys) loaded from `core.config` which should integrate with HashiCorp Vault or similar, not hardcoded.
*   **Input Validation**: Pydantic models provide input validation for API requests.
*   **Content Policies**: Adherence to platform content policies for custom models (SRS Sec 2.5).

## 8. Non-Functional Requirements specific to MLOps Service
*   **Scalability**: The service itself should be stateless and horizontally scalable. The underlying K8s cluster for model serving must be scalable.
*   **Reliability**: Model registry data (PostgreSQL) and artifacts (MinIO) must be highly available and durable (achieved via underlying DB/Storage HA strategies). Deployment processes must be robust.
*   **Performance**:
    *   API response times for CRUD operations should be fast (<200ms P95).
    *   Model upload time depends on artifact size and network, but API should respond quickly acknowledging upload start.
    *   Model deployment time to K8s depends on image size, cluster state, and K8s scheduler, but the API should initiate quickly and provide status polling.
    *   Validation process time is asynchronous and depends on scan complexity.
*   **Maintainability**: Modular code, clear separation of concerns, comprehensive tests, and documentation.
*   **Extensibility**: Adapter patterns for K8s, storage, scanners should allow for future changes or additions of providers/tools.

This SDS provides a blueprint for the development of the `CreativeFlow.MLOpsService`. Implementation details will further refine these specifications.