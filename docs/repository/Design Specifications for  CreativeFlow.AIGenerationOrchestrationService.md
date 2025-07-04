# Software Design Specification (SDS) for CreativeFlow.AIGenerationOrchestrationService

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the **CreativeFlow.AIGenerationOrchestrationService**. This microservice is a central component of the CreativeFlow AI platform, responsible for managing and orchestrating the entire lifecycle of AI-driven creative content generation. It acts as the intermediary between user-facing requests (often originating from or routed through the Odoo backend) and the n8n workflow engine that executes the actual AI generation tasks.

### 1.2 Scope
The scope of this service includes:
*   Receiving and validating creative generation requests.
*   Coordinating with the Credit/Subscription Service (Odoo Adapter) for credit checks and deductions.
*   Preparing job parameters and publishing generation tasks to a RabbitMQ message queue for consumption by the n8n Workflow Engine.
*   Tracking the status of ongoing generation requests.
*   Receiving and processing callbacks (results, errors) from the n8n Workflow Engine.
*   Storing metadata related to generation requests and their outcomes (e.g., links to generated assets).
*   Triggering user notifications via the Notification Service.
*   Handling error scenarios, including potential credit refunds for system-side failures.
*   Exposing internal APIs for initiating generation requests and querying their status.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **AI:** Artificial Intelligence
*   **API:** Application Programming Interface
*   **CI/CD:** Continuous Integration / Continuous Deployment
*   **CRUD:** Create, Read, Update, Delete
*   **DTO:** Data Transfer Object
*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **JSON:** JavaScript Object Notation
*   **JWT:** JSON Web Token
*   **MinIO:** High-performance, S3-compatible object storage.
*   **n8n:** A free and open fair-code licensed node-based Workflow Automation Tool.
*   **Odoo:** A suite of open-source business apps.
*   **Pika:** Python RabbitMQ client library.
*   **PostgreSQL:** Powerful, open-source object-relational database system.
*   **Pydantic:** Data validation and settings management using Python type annotations.
*   **PWA:** Progressive Web Application
*   **RabbitMQ:** Open-source message broker.
*   **REST:** Representational State Transfer
*   **RTL:** React Testing Library
*   **SDS:** Software Design Specification
*   **SQLAlchemy:** SQL toolkit and Object-Relational Mapper for Python.
*   **TS:** TypeScript
*   **UUID:** Universally Unique Identifier

## 2. System Overview

The AI Generation Orchestration Service is a Python-based microservice built using the FastAPI framework. It plays a crucial role in the AI creative generation pipeline by:

1.  **Request Intake & Validation:** Accepting generation requests, validating input parameters using Pydantic models.
2.  **Pre-processing & Job Preparation:** Interacting with the Credit/Subscription Service (Odoo Adapter or dedicated client) to verify user entitlements and deduct credits. It prepares detailed job parameters for the n8n workflow engine, including user inputs (prompts, images, brand elements), desired formats, styles, and other generation-specific configurations.
3.  **Job Dispatching:** Publishing the prepared generation jobs to a RabbitMQ exchange, ensuring tasks are reliably queued for processing by n8n worker instances.
4.  **Status Tracking & Persistence:** Maintaining the state of each generation request in a PostgreSQL database, from initiation through various processing stages to completion or failure.
5.  **Result Handling:** Receiving asynchronous callbacks from n8n upon completion of sample generation, final asset generation, or encountering errors. It processes these results, updates the database, and potentially stores asset metadata.
6.  **Notification:** Triggering user notifications (e.g., "samples ready", "final asset generated", "generation failed") via the dedicated Notification Service.
7.  **Error Management:** Implementing logic to handle errors reported by n8n or internal processing, including coordinating potential credit refunds for system-attributable failures.

The service exposes internal RESTful APIs for other platform components to initiate generation tasks and query their status. It relies heavily on asynchronous communication patterns (RabbitMQ) to decouple itself from the potentially long-running AI generation processes handled by n8n.

## 3. Configuration (`creativeflow.services.aigeneration.core.config`)

The service's configuration will be managed by `core/config.py` using Pydantic's `BaseSettings`. Settings will be loaded from environment variables or a `.env` file. An example `.env.example` file will be provided.

**Key Configuration Variables:**

*   `PROJECT_NAME`: (str) Name of the project (e.g., "CreativeFlow AI Generation Orchestration Service").
*   `API_V1_STR`: (str) API prefix for version 1 (e.g., "/api/v1").
*   `DATABASE_URL`: (str) Connection string for the PostgreSQL database (e.g., `postgresql+asyncpg://user:pass@host:port/dbname`).
*   `RABBITMQ_URL`: (str) Connection string for RabbitMQ (e.g., `amqp://user:pass@host:port/vhost`).
*   `RABBITMQ_GENERATION_EXCHANGE`: (str) Name of the RabbitMQ exchange for generation jobs (e.g., `generation_jobs_exchange`).
*   `RABBITMQ_N8N_JOB_QUEUE`: (str) Name of the RabbitMQ queue n8n consumes from.
*   `RABBITMQ_N8N_JOB_ROUTING_KEY`: (str) Routing key for n8n generation jobs.
*   `N8N_CALLBACK_BASE_URL`: (str) Base URL for this service that n8n will use for callbacks.
*   `CREDIT_SERVICE_API_URL`: (str) Base URL for the Credit/Subscription Service API.
*   `NOTIFICATION_SERVICE_API_URL`: (str) Base URL for the Notification Service API.
*   `ODOO_URL`: (str) URL for the Odoo XML-RPC/JSON-RPC endpoint.
*   `ODOO_DB`: (str) Odoo database name.
*   `ODOO_UID`: (int) Odoo user ID for API access (technical user).
*   `ODOO_PASSWORD`: (str) Odoo password for API access.
*   `LOG_LEVEL`: (str) Logging level (e.g., "INFO", "DEBUG"). Default: "INFO".
*   `LOG_FORMAT`: (str) Log format (e.g., "json", "text"). Default: "json".

**Feature Toggles:**

*   `ENABLE_ADVANCED_MODEL_SELECTOR`: (bool) If true, enables logic for more complex AI model selection.
*   `ENABLE_DETAILED_N8N_ERROR_LOGGING`: (bool) If true, logs more verbose error details from n8n callbacks.
*   `ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE`: (bool) If true, automatically triggers credit refund attempts for system-caused generation failures.

## 4. API Design

The service will expose internal RESTful APIs. All API request/response bodies will be defined using Pydantic models in `api/v1/schemas.py`.

### 4.1 Generation Request API (`api/v1/endpoints/generation_requests.py`)

Base path: `{API_V1_STR}/generation-requests`

#### 4.1.1 Create Generation Request
*   **Endpoint:** `POST /`
*   **Request Body:** `GenerationRequestCreate` (from `schemas.py`)
    *   `user_id: str`
    *   `project_id: str`
    *   `input_prompt: str`
    *   `style_guidance: Optional[str]`
    *   `output_format: str` (e.g., "InstagramPost_1x1", "Custom")
    *   `custom_dimensions: Optional[CustomDimensions]` (if `output_format` is "Custom")
        *   `width: int`
        *   `height: int`
    *   `brand_kit_id: Optional[str]`
    *   `uploaded_image_references: Optional[List[str]]` (MinIO paths or asset IDs)
    *   `target_platform_hints: Optional[List[str]]`
    *   `emotional_tone: Optional[str]`
    *   `cultural_adaptation_parameters: Optional[dict]`
*   **Response Body:** `GenerationRequestRead` (from `schemas.py`)
    *   Includes request ID, status, and other relevant details.
*   **Logic:**
    1.  Validates the request payload.
    2.  Delegates to `OrchestrationService.initiate_generation`.
    3.  Returns the created/updated generation request details.
*   **Requirements:** REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, Section 5.3.1

#### 4.1.2 Get Generation Request Status
*   **Endpoint:** `GET /{request_id}`
*   **Path Parameter:** `request_id: UUID`
*   **Response Body:** `GenerationRequestRead` (from `schemas.py`)
*   **Logic:**
    1.  Delegates to `OrchestrationService.get_generation_status`.
    2.  Returns the current status and details of the specified generation request.
*   **Requirements:** Section 5.3.1

#### 4.1.3 Select Sample for Final Generation
*   **Endpoint:** `POST /{request_id}/select-sample`
*   **Path Parameter:** `request_id: UUID`
*   **Request Body:** `SampleSelection` (from `schemas.py`)
    *   `selected_sample_id: str` (Asset ID of the chosen sample)
    *   `user_id: str` (For authorization/credit check context)
    *   `desired_resolution: Optional[str]` (e.g., "1024x1024", "4K", defaults to a standard HD if not provided)
*   **Response Body:** `GenerationRequestRead` (from `schemas.py`)
*   **Logic:**
    1.  Validates the request.
    2.  Delegates to `OrchestrationService.select_sample_and_initiate_final`.
    3.  Returns the updated generation request details.
*   **Requirements:** REQ-008, REQ-009, Section 5.3.1

#### 4.1.4 Regenerate Samples
*   **Endpoint:** `POST /{request_id}/regenerate-samples`
*   **Path Parameter:** `request_id: UUID`
*   **Request Body:** `RegenerateSamplesRequest` (from `schemas.py`)
    *   `user_id: str` (For authorization/credit check context)
    *   `updated_prompt: Optional[str]` (Optional new prompt for regeneration)
    *   `updated_style_guidance: Optional[str]`
*   **Response Body:** `GenerationRequestRead` (from `schemas.py`)
*   **Logic:**
    1.  Validates the request.
    2.  Delegates to `OrchestrationService.trigger_sample_regeneration`.
    3.  Returns the updated generation request details.
*   **Requirements:** REQ-008

### 4.2 n8n Callback API (`api/v1/endpoints/n8n_callbacks.py`)

Base path: `{API_V1_STR}/n8n-callbacks` (or derived from `N8N_CALLBACK_BASE_URL` config)
These endpoints will be secured, e.g., using a shared secret in headers or by IP whitelisting n8n worker IPs.

#### 4.2.1 Handle n8n Sample Generation Callback
*   **Endpoint:** `POST /sample-result`
*   **Request Body:** `N8NSampleResultPayload` (from `schemas.py`)
    *   `generation_request_id: UUID`
    *   `status: str` (e.g., "AWAITING_SELECTION")
    *   `samples: List[SampleAssetInfo]`
        *   `asset_id: str` (MinIO path or internal asset ID)
        *   `url: str` (Publicly accessible URL or presigned URL for the sample)
        *   `resolution: str`
        *   `format: str`
*   **Response Body:** `{"status": "received"}` (dict)
*   **Logic:**
    1.  Validates payload.
    2.  Delegates to `OrchestrationService.process_n8n_sample_callback`.
*   **Requirements:** REQ-008, Section 5.3.1

#### 4.2.2 Handle n8n Final Generation Callback
*   **Endpoint:** `POST /final-result`
*   **Request Body:** `N8NFinalResultPayload` (from `schemas.py`)
    *   `generation_request_id: UUID`
    *   `status: str` (e.g., "COMPLETED")
    *   `final_asset: FinalAssetInfo`
        *   `asset_id: str`
        *   `url: str`
        *   `resolution: str`
        *   `format: str`
        *   `metadata: Optional[dict]`
*   **Response Body:** `{"status": "received"}` (dict)
*   **Logic:**
    1.  Validates payload.
    2.  Delegates to `OrchestrationService.process_n8n_final_asset_callback`.
*   **Requirements:** REQ-009, Section 5.3.1

#### 4.2.3 Handle n8n Error Callback
*   **Endpoint:** `POST /error`
*   **Request Body:** `N8NErrorPayload` (from `schemas.py`)
    *   `generation_request_id: UUID`
    *   `error_code: Optional[str]`
    *   `error_message: str`
    *   `error_details: Optional[dict]`
    *   `failed_stage: Optional[str]` (e.g., "sample_processing", "final_processing")
*   **Response Body:** `{"status": "received"}` (dict)
*   **Logic:**
    1.  Validates payload.
    2.  Delegates to `OrchestrationService.handle_n8n_error`.
*   **Requirements:** REQ-007.1, Section 5.3.1

### 4.3 API Schemas (`api/v1/schemas.py`)
Key Pydantic models will include:
*   `GenerationRequestBase`: Common fields for generation requests.
*   `CustomDimensions`: `width: int`, `height: int`.
*   `GenerationRequestCreate(GenerationRequestBase)`: For creating new requests. Includes fields like `user_id`, `project_id`, `input_prompt`, `style_guidance`, `output_format`, `custom_dimensions`, `brand_kit_id`, `uploaded_image_references`, `target_platform_hints`, `emotional_tone`, `cultural_adaptation_parameters`.
*   `AssetInfoBase`: Common fields for asset information.
    *   `asset_id: str`
    *   `url: str`
    *   `resolution: str`
    *   `format: str`
*   `SampleAssetInfo(AssetInfoBase)`: Specific for sample assets.
*   `FinalAssetInfo(AssetInfoBase)`: Specific for final assets, may include additional `metadata: Optional[dict]`.
*   `GenerationRequestRead(GenerationRequestBase)`: For API responses. Includes `id: UUID`, `status: str`, `created_at: datetime`, `updated_at: datetime`, `sample_asset_infos: Optional[List[SampleAssetInfo]]`, `final_asset_info: Optional[FinalAssetInfo]]`, `error_message: Optional[str]`.
*   `N8NSampleResultPayload`: `generation_request_id: UUID`, `status: str`, `samples: List[SampleAssetInfo]`.
*   `N8NFinalResultPayload`: `generation_request_id: UUID`, `status: str`, `final_asset: FinalAssetInfo`.
*   `N8NErrorPayload`: `generation_request_id: UUID`, `error_code: Optional[str]`, `error_message: str`, `error_details: Optional[dict]`, `failed_stage: Optional[str]`.
*   `SampleSelection`: `selected_sample_id: str`, `user_id: str`, `desired_resolution: Optional[str]`.
*   `RegenerateSamplesRequest`: `user_id: str`, `updated_prompt: Optional[str]`, `updated_style_guidance: Optional[str]`.
*   `ErrorDetail`: `loc: List[str]`, `msg: str`, `type: str`.
*   `ErrorResponse`: `detail: Union[str, List[ErrorDetail]]`.

## 5. Core Logic & Services

### 5.1 Orchestration Service (`application/services/orchestration_service.py`)
This service contains the core business logic for managing the AI generation pipeline.

**Constructor:**
`__init__(self, repo: IGenerationRequestRepository, rabbitmq_publisher: RabbitMQPublisher, credit_service_client: CreditServiceClient | OdooAdapterClient, notification_client: NotificationServiceClient)`

**Methods:**

*   **`async def initiate_generation(self, user_id: str, project_id: str, request_data: GenerationRequestCreateDTO) -> GenerationRequest:`**
    1.  **Input Validation:** `request_data` is already validated by FastAPI using Pydantic models.
    2.  **Credit/Subscription Check:**
        *   Determine required credits for sample generation (e.g., 0.25 credits as per REQ-016, or 0 if on a plan with unlimited standard generations).
        *   Call `self._credit_service_client.get_user_subscription_tier(user_id)`.
        *   If tier allows unlimited standard generations, skip credit check for samples.
        *   Else, call `self._credit_service_client.check_credits(user_id, required_credits_for_sample)`.
        *   If insufficient credits or invalid subscription, raise an appropriate HTTP exception (e.g., `HTTPException(status_code=402, detail="Insufficient credits or invalid subscription")`).
    3.  **Create GenerationRequest Record:**
        *   Create a new `GenerationRequest` domain object with initial status (e.g., `GenerationStatus.VALIDATING_CREDITS` or `GenerationStatus.PENDING`).
        *   Store `user_id`, `project_id`, and all input parameters from `request_data`.
        *   Call `self._repo.add(new_generation_request)`.
    4.  **Deduct Credits (for samples, if applicable):**
        *   If credits are required and checked, call `self._credit_service_client.deduct_credits(user_id, new_generation_request.id, required_credits_for_sample, "sample_generation_fee")`.
        *   If deduction fails, update `GenerationRequest` status to `FAILED`, log error, and potentially trigger refund if a pre-authorization model was used. Raise exception.
    5.  **Prepare n8n Job Payload:**
        *   Construct a JSON payload for n8n. This payload must include:
            *   `generation_request_id`: `new_generation_request.id`
            *   `user_id`
            *   `project_id`
            *   `input_prompt`
            *   `style_guidance`
            *   `output_format`
            *   `custom_dimensions` (if applicable)
            *   `brand_kit_id` (if provided)
            *   `uploaded_image_references`
            *   `target_platform_hints`
            *   `emotional_tone`
            *   `cultural_adaptation_parameters`
            *   `callback_url_sample_result`: URL to `/api/v1/n8n-callbacks/sample-result`
            *   `callback_url_error`: URL to `/api/v1/n8n-callbacks/error`
            *   `job_type`: "sample_generation"
    6.  **Publish Job to RabbitMQ:**
        *   Call `self._rabbitmq_publisher.publish_generation_job(job_payload, routing_key=settings.RABBITMQ_N8N_JOB_ROUTING_KEY, exchange_name=settings.RABBITMQ_GENERATION_EXCHANGE)`.
    7.  **Update GenerationRequest Status:**
        *   Set status to `GenerationStatus.PROCESSING_SAMPLES`.
        *   Call `self._repo.update(new_generation_request)`.
    8.  Return the `new_generation_request` domain object (or a DTO representation).

*   **`async def get_generation_status(self, request_id: UUID) -> GenerationRequest:`**
    1.  Fetch `GenerationRequest` from `self._repo.get_by_id(request_id)`.
    2.  If not found, raise `HTTPException(status_code=404, detail="Generation request not found")`.
    3.  Return the `GenerationRequest` object.

*   **`async def process_n8n_sample_callback(self, callback_data: N8NSampleResultDTO) -> None:`**
    1.  Fetch `GenerationRequest` using `callback_data.generation_request_id` from `self._repo`.
    2.  If not found, log error and return (or handle appropriately).
    3.  Update `GenerationRequest` object:
        *   Set status to `GenerationStatus.AWAITING_SELECTION`.
        *   Populate `sample_asset_infos` with data from `callback_data.samples`. Each sample should include an `asset_id` (MinIO path or internal ID), `url`, `resolution`, `format`.
        *   Record `credits_cost_sample` if not already set or if it varies dynamically.
    4.  Call `self._repo.update(generation_request)`.
    5.  Call `self._notification_client.send_notification(user_id=generation_request.user_id, notification_type="samples_ready", message="Your AI creative samples are ready!", payload={"request_id": str(generation_request.id)})`.

*   **`async def process_n8n_final_asset_callback(self, callback_data: N8NFinalResultDTO) -> None:`**
    1.  Fetch `GenerationRequest` using `callback_data.generation_request_id` from `self._repo`.
    2.  If not found, log error and return.
    3.  Update `GenerationRequest` object:
        *   Set status to `GenerationStatus.COMPLETED`.
        *   Populate `final_asset_info` with data from `callback_data.final_asset`.
        *   Record `credits_cost_final` if not already set.
    4.  Call `self._repo.update(generation_request)`.
    5.  Call `self._notification_client.send_notification(user_id=generation_request.user_id, notification_type="final_asset_ready", message="Your final AI creative is ready!", payload={"request_id": str(generation_request.id), "asset_url": callback_data.final_asset.url})`.

*   **`async def handle_n8n_error(self, error_data: N8NErrorDTO) -> None:`** (REQ-007.1)
    1.  Fetch `GenerationRequest` using `error_data.generation_request_id` from `self._repo`.
    2.  If not found, log error and return.
    3.  Update `GenerationRequest` object:
        *   Set status to `GenerationStatus.FAILED` or `GenerationStatus.CONTENT_REJECTED` based on error type.
        *   Store `error_data.error_message` and `error_data.error_details`.
    4.  **Credit Refund Logic (REQ-007.1, REQ-016):**
        *   Determine if the error is a system-side error (e.g., AI model unavailable, n8n workflow crash not due to bad input) or a user input error (e.g., invalid prompt parameters *after* warnings, content policy violation).
        *   This might involve inspecting `error_data.error_code` or `error_data.failed_stage`.
        *   If it's a system-side error and credits were deducted for the failed stage (sample or final), and `settings.ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE` is true:
            *   Identify amount to refund (e.g., `generation_request.credits_cost_sample` or `generation_request.credits_cost_final`).
            *   Call `self._credit_service_client.refund_credits(user_id=generation_request.user_id, request_id=generation_request.id, amount_to_refund, reason="System error during AI generation")`.
            *   Log refund attempt status.
    5.  Call `self._repo.update(generation_request)`.
    6.  Call `self._notification_client.send_notification(user_id=generation_request.user_id, notification_type="generation_failed", message=f"AI generation failed: {error_data.error_message}", payload={"request_id": str(generation_request.id)})`.
    7.  If `settings.ENABLE_DETAILED_N8N_ERROR_LOGGING` is true, log `error_data.error_details`.

*   **`async def trigger_sample_regeneration(self, request_id: UUID, user_id: str, updated_prompt: Optional[str] = None, updated_style_guidance: Optional[str] = None) -> GenerationRequest:`** (REQ-008)
    1.  Fetch `GenerationRequest` using `request_id` from `self._repo`.
    2.  If not found or `generation_request.user_id != user_id`, raise `HTTPException(status_code=404/403)`.
    3.  Check if regeneration is allowed (e.g., based on subscription tier, previous attempts).
    4.  **Credit Check & Deduction for Regeneration:**
        *   Determine regeneration cost (e.g., same as initial sample cost, REQ-016).
        *   Call `self._credit_service_client.check_credits/deduct_credits`. If fails, raise exception.
    5.  **Prepare n8n Job Payload (similar to `initiate_generation` but for regeneration):**
        *   Use `updated_prompt` or `updated_style_guidance` if provided, otherwise reuse original or modified parameters.
        *   `job_type`: "sample_regeneration"
        *   Ensure new callbacks are set.
    6.  Publish job to RabbitMQ.
    7.  Update `GenerationRequest` status to `GenerationStatus.PROCESSING_SAMPLES`.
    8.  Update `credits_cost_sample` (could be cumulative or per attempt, to be defined).
    9.  Call `self._repo.update(generation_request)`.
    10. Return the updated `generation_request`.

*   **`async def select_sample_and_initiate_final(self, request_id: UUID, selected_sample_id: str, user_id: str, desired_resolution: Optional[str] = None) -> GenerationRequest:`** (REQ-009)
    1.  Fetch `GenerationRequest` using `request_id` from `self._repo`.
    2.  If not found or `generation_request.user_id != user_id`, raise `HTTPException(status_code=404/403)`.
    3.  Verify `generation_request.status` is `GenerationStatus.AWAITING_SELECTION`.
    4.  Validate `selected_sample_id` exists within `generation_request.sample_asset_infos`.
    5.  **Credit Check & Deduction for Final Generation:**
        *   Determine final generation cost (e.g., 1 or 2 credits based on resolution, REQ-016).
        *   Call `self._credit_service_client.check_credits/deduct_credits`. If fails, raise exception.
    6.  **Prepare n8n Job Payload for Final Generation:**
        *   Include `generation_request_id`, `user_id`, `project_id`.
        *   Reference the `selected_sample_id` (or its MinIO path/asset ID).
        *   Specify `desired_resolution` (e.g., "1024x1024", "4K", or use a default if not provided by user).
        *   `callback_url_final_result`: URL to `/api/v1/n8n-callbacks/final-result`
        *   `callback_url_error`: URL to `/api/v1/n8n-callbacks/error`
        *   `job_type`: "final_generation"
    7.  Publish job to RabbitMQ.
    8.  Update `GenerationRequest`:
        *   Set `selected_sample_id`.
        *   Set status to `GenerationStatus.PROCESSING_FINAL`.
        *   Store `credits_cost_final`.
    9.  Call `self._repo.update(generation_request)`.
    10. Return the updated `generation_request`.

### 5.2 External Service Clients

#### 5.2.1 Credit Service Client (`application/services/credit_service_client.py`)
*   **Purpose:** Interacts with the external Credit/Subscription Service API (which might be an adapter to Odoo or a standalone billing service).
*   Uses `httpx.AsyncClient` for asynchronous HTTP requests.
*   **Methods:**
    *   `async def check_credits(self, user_id: str, required_credits: float) -> bool:`
    *   `async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:`
    *   `async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:`
    *   `async def get_user_subscription_tier(self, user_id: str) -> str:`
*   **Error Handling:** Should handle HTTP errors from the credit service and raise appropriate application exceptions.

#### 5.2.2 Notification Service Client (`application/services/notification_service_client.py` or `infrastructure/clients/notification_client.py`)
*   **Purpose:** Sends notification requests to the dedicated Notification Service.
*   Uses `httpx.AsyncClient`.
*   **Methods:**
    *   `async def send_notification(self, user_id: str, message: str, notification_type: str, metadata: dict = None) -> None:`
        *   Constructs payload and POSTs to `settings.NOTIFICATION_SERVICE_API_URL`.
*   **Error Handling:** Log errors if notification sending fails but generally should not block core generation flow.

#### 5.2.3 Odoo Adapter Client (`infrastructure/clients/odoo_adapter_client.py`)
*   **Purpose:** If direct Odoo interaction is needed beyond what the Credit Service Client provides (e.g., for more complex subscription validation or direct Odoo record updates not exposed via the Credit Service Client).
*   Uses a library like `odoorpc` or Python's `xmlrpc.client` / `jsonrpc` for RPC calls.
*   **Methods (Example):**
    *   `async def call_odoo_rpc(self, model: str, method: str, args: list, kwargs: dict = None) -> Any:` Generic method to call Odoo.
    *   Specific methods for validating subscriptions or other Odoo-specific tasks if the `CreditServiceClient` is too abstract.
        *   `async def validate_user_subscription_and_credits(...)`
        *   `async def deduct_user_credits(...)`
        *   `async def refund_user_credits(...)`
        *(Note: These methods overlap with CreditServiceClient; the design decision is whether CreditServiceClient calls this OdooAdapterClient, or if OrchestrationService directly uses one or the other depending on the abstraction level of CreditServiceClient.)*

### 5.3 Internal DTOs (`application/dtos.py`)
*   `GenerationJobParameters`: Internal representation of data sent to n8n.
*   `N8NResultInternal`: Internal representation of data received from n8n callbacks.
*   `CreditServiceRequest`: Internal DTO for requests to the Credit Service Client.

## 6. Domain Model (`domain/models/`)

#### 6.1 GenerationRequest (`generation_request.py`)
*   **Attributes:** As defined in the file structure. Includes `id`, `user_id`, `project_id`, `input_prompt`, `style_guidance`, `input_parameters` (dict for format, resolution, brand_elements, etc.), `status` (enum `GenerationStatus`), `error_message`, `sample_asset_infos` (List of `AssetInfo`), `selected_sample_id`, `final_asset_info` (`AssetInfo`), `credits_cost_sample`, `credits_cost_final`, `ai_model_used`, `created_at`, `updated_at`.
*   **Methods:**
    *   `update_status(new_status: GenerationStatus, error_message: Optional[str] = None)`: Changes status and logs timestamp.
    *   `add_sample_result(sample_asset: AssetInfo)`: Appends to `sample_asset_infos`.
    *   `set_final_asset(final_asset: AssetInfo)`: Sets `final_asset_info`.
    *   `set_selected_sample(sample_id: str)`

#### 6.2 GenerationStatus (`generation_status.py`)
*   Python `Enum` with values: `PENDING`, `VALIDATING_CREDITS`, `PUBLISHING_TO_QUEUE`, `PROCESSING_SAMPLES`, `AWAITING_SELECTION`, `PROCESSING_FINAL`, `COMPLETED`, `FAILED`, `CONTENT_REJECTED`.

#### 6.3 AssetInfo (`asset_info.py`)
*   Pydantic BaseModel or dataclass (Value Object).
*   **Attributes:** `asset_id: str` (reference/path), `url: str`, `resolution: Optional[str]`, `format: str`.

### 6.4 Domain Events (`domain/events.py`)
Pydantic models for events like:
*   `GenerationRequestInitiatedEvent(request_id: UUID, user_id: str)`
*   `SampleGenerationCompletedEvent(request_id: UUID, user_id: str, sample_count: int)`
*   `FinalAssetGeneratedEvent(request_id: UUID, user_id: str, asset_url: str)`
*   `GenerationFailedEvent(request_id: UUID, user_id: str, error_message: str, is_system_error: bool)`
*(These events are conceptual for now; actual publishing might be handled by the OrchestrationService directly calling other services or publishing to different MQ topics if a more event-driven internal architecture is desired beyond the n8n job queue.)*

## 7. Data Persistence

### 7.1 Repository Interface (`domain/repositories/generation_request_repository.py`)
*   `IGenerationRequestRepository(ABC)`
*   **Methods:**
    *   `async def get_by_id(self, request_id: UUID) -> Optional[GenerationRequest]: abstractmethod`
    *   `async def add(self, generation_request: GenerationRequest) -> None: abstractmethod`
    *   `async def update(self, generation_request: GenerationRequest) -> None: abstractmethod`
    *   `async def list_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GenerationRequest]: abstractmethod`

### 7.2 PostgreSQL Implementation (`infrastructure/repositories/postgres_generation_request_repository.py`)
*   `PostgresGenerationRequestRepository(IGenerationRequestRepository)`
*   Uses SQLAlchemy Core or ORM with `asyncpg` driver for asynchronous database operations.
*   The `GenerationRequest` domain model will be mapped to a PostgreSQL table (e.g., `generation_requests`).
    *   `id (UUID, PK)`
    *   `user_id (VARCHAR)`
    *   `project_id (VARCHAR)`
    *   `input_prompt (TEXT)`
    *   `style_guidance (TEXT, nullable)`
    *   `input_parameters (JSONB, nullable)`
    *   `status (VARCHAR)`
    *   `error_message (TEXT, nullable)`
    *   `sample_asset_infos (JSONB, nullable)` (stores list of `AssetInfo` as JSON)
    *   `selected_sample_id (VARCHAR, nullable)`
    *   `final_asset_info (JSONB, nullable)` (stores `AssetInfo` as JSON)
    *   `credits_cost_sample (DECIMAL, nullable)`
    *   `credits_cost_final (DECIMAL, nullable)`
    *   `ai_model_used (VARCHAR, nullable)`
    *   `created_at (TIMESTAMP WITH TIME ZONE)`
    *   `updated_at (TIMESTAMP WITH TIME ZONE)`
*   Implements all interface methods using database sessions provided via dependency injection.

### 7.3 Database Configuration (`infrastructure/database/db_config.py`)
*   `init_db(database_url: str)`: Initializes SQLAlchemy engine.
*   `get_db()`: FastAPI dependency to provide DB sessions.
*   Will use `create_async_engine` and `AsyncSession` from SQLAlchemy for async operations.

## 8. Messaging (`infrastructure/messaging/rabbitmq_publisher.py`)

*   **RabbitMQ Integration:**
    *   Uses `pika` library for interacting with RabbitMQ.
    *   Connects using `RABBITMQ_URL` from settings.
*   **Message Publishing:**
    *   `publish_generation_job(job_payload: dict, routing_key: str, exchange_name: str)`:
        1.  Ensures connection and channel are active.
        2.  Declares the exchange (e.g., `settings.RABBITMQ_GENERATION_EXCHANGE`, type: direct or topic).
        3.  Serializes `job_payload` to JSON string.
        4.  Publishes the message with `delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE` for durability.
*   **Message Format for n8n Jobs:**
    *   JSON object containing all necessary parameters for n8n to execute the generation workflow, as detailed in `OrchestrationService.initiate_generation`. Example:
        json
        {
          "generation_request_id": "uuid-of-request",
          "user_id": "user-id-string",
          "project_id": "project-id-string",
          "input_prompt": "A futuristic cityscape",
          "style_guidance": "cyberpunk, neon lights",
          "output_format": "InstagramPost_1x1",
          "brand_elements": { "logo_url": "...", "colors": ["#FF0000"] },
          // ... other parameters ...
          "callback_url_sample_result": "http://orchestrator/api/v1/n8n-callbacks/sample-result",
          "callback_url_final_result": "http://orchestrator/api/v1/n8n-callbacks/final-result",
          "callback_url_error": "http://orchestrator/api/v1/n8n-callbacks/error",
          "job_type": "sample_generation" // or "final_generation", "sample_regeneration"
        }
        
*   Connection management (`connect`, `close`) and error handling (e.g., connection loss, retry logic) within the publisher.

## 9. Error Handling (`creativeflow.services.aigeneration.core.error_handlers.py`)

*   FastAPI custom exception handlers will be defined to catch specific application exceptions and Pydantic's `RequestValidationError`.
*   `validation_exception_handler`: Catches `RequestValidationError` and returns a `422 Unprocessable Entity` JSONResponse with detailed error messages.
*   `custom_app_exception_handler`: Catches custom exceptions (e.g., `InsufficientCreditsError`, `GenerationJobPublishError`) and returns appropriate HTTP status codes (e.g., 402, 500) with a structured JSON error message: `{"detail": "Error message"}`.
*   This ensures consistent error responses across the API.
*   REQ-007.1 is primarily handled within the `OrchestrationService` when processing n8n error callbacks, but API-level errors (e.g., bad request to initiate generation) are handled here.

## 10. Logging (`creativeflow.services.aigeneration.core.logging_config.py`)

*   `setup_logging(log_level: str)`: Configures Python's `logging` module.
*   **Structured Logging:** Logs will be formatted as JSON (if `LOG_FORMAT` is "json") for easier parsing by log aggregation systems (e.g., ELK/Loki).
*   **Log Level:** Configurable via `LOG_LEVEL` environment variable.
*   **Correlation IDs:** If a correlation ID (trace ID) is passed in request headers, it should be included in log messages for distributed tracing.
*   Key events to log:
    *   Incoming API requests (method, path, parameters - PII scrubbed).
    *   Generation job publishing events (request ID, job payload summary).
    *   n8n callback events (request ID, status, summary of results/errors).
    *   Credit service interactions (request ID, action, outcome).
    *   Notification service interactions (request ID, notification type).
    *   Errors and exceptions with stack traces.
    *   REQ-007.1: Detailed logging for AI generation errors, especially if `ENABLE_DETAILED_N8N_ERROR_LOGGING` is true.

## 11. Dependencies (`creativeflow.services.aigeneration.core.dependencies.py`)

This module will provide FastAPI `Depends` utilities for injecting shared resources or service instances.

*   `async def get_db_session() -> AsyncGenerator[AsyncSession, None]:`
    *   Yields an SQLAlchemy `AsyncSession` from `SessionLocal` (defined in `db_config.py`).
    *   Ensures the session is closed after the request.
*   `async def get_rabbitmq_publisher() -> RabbitMQPublisher:`
    *   Provides an instance of `RabbitMQPublisher`. May involve connection pooling or singleton management if appropriate for `pika`.
    *   Handles startup connection and graceful shutdown.
*   `def get_generation_request_repo(db_session: AsyncSession = Depends(get_db_session)) -> IGenerationRequestRepository:`
    *   Returns an instance of `PostgresGenerationRequestRepository` initialized with a DB session.
*   `def get_odoo_adapter_client() -> OdooAdapterClient:`
    *   Returns an instance of `OdooAdapterClient`.
*   `def get_credit_service_client(odoo_client: OdooAdapterClient = Depends(get_odoo_adapter_client)) -> CreditServiceClient:`
    *   Returns an instance of `CreditServiceClient`. *This implies that CreditServiceClient might use OdooAdapterClient, or OrchestrationService might decide which one to use based on abstraction needs. For simplicity here, let's assume CreditServiceClient is the primary interface and it might internally use OdooAdapterClient if the "Credit Service" is indeed Odoo.*
    *   Alternatively, if `CREDIT_SERVICE_API_URL` points to a non-Odoo dedicated service, this client would use `httpx`. The file structure implies a separate `credit_service_client.py` and `odoo_adapter_client.py`. The `OrchestrationService` would likely inject the one primarily responsible for credit operations. If Odoo *is* the credit service, then `OdooAdapterClient` is used for that purpose.
*   `def get_notification_client() -> NotificationServiceClient:`
    *   Returns an instance of `NotificationServiceClient`.
*   `def get_orchestration_service(...) -> OrchestrationService:`
    *   Injects all necessary dependencies (`IGenerationRequestRepository`, `RabbitMQPublisher`, `CreditServiceClient`/`OdooAdapterClient`, `NotificationServiceClient`) into the `OrchestrationService`.

## 12. Scalability and Performance Considerations

*   **Asynchronous Operations:** FastAPI's async nature and the use of `httpx` for external calls, along with asynchronous database access (`asyncpg`), are crucial for I/O-bound performance.
*   **Message Queuing:** RabbitMQ decouples job submission from processing, allowing the API to remain responsive and enabling n8n workers to scale independently.
*   **Database:** Connection pooling (managed by SQLAlchemy or a separate pooler like PgBouncer) will be used. Read replicas for PostgreSQL can be added if read load becomes a bottleneck on the `generation_requests` table (though this service is more write/update heavy for request status).
*   **Stateless Service:** The service itself should be designed to be stateless to allow for easy horizontal scaling of FastAPI instances behind a load balancer. Session/state related to long-running generations is stored in PostgreSQL and RabbitMQ.

## 13. Security Considerations

*   **API Security:**
    *   Internal APIs should be protected (e.g., network policies, mutual TLS, or API keys if accessed by other internal services not in the same trusted zone).
    *   n8n callbacks must be secured (e.g., shared secret validation, IP whitelisting).
*   **Input Validation:** Pydantic models provide robust input validation for all API endpoints.
*   **Secrets Management:** Database credentials, RabbitMQ credentials, Odoo credentials, and any other secrets will be loaded from environment variables (managed by `core.config`) and should not be hardcoded. These would typically be injected into the environment by a secrets management system in production (e.g., HashiCorp Vault).
*   **Dependency Vulnerabilities:** Regularly scan Python dependencies for known vulnerabilities.
*   **PII Handling:** Ensure any PII in prompts or parameters is handled according to data privacy policies (e.g., if logging payloads, scrub PII).
*   **Error Handling:** Avoid leaking sensitive information in error messages.

## 14. Main Application Entrypoint (`main.py`)

*   Creates the FastAPI application instance: `app = FastAPI(title=settings.PROJECT_NAME)`.
*   **CORS:** Configures `CORSMiddleware` if cross-origin requests are expected (likely from a frontend).
*   **Logging:** Calls `setup_logging()` from `core.logging_config`.
*   **Error Handlers:** Registers custom exception handlers from `core.error_handlers`.
*   **Routers:** Includes API routers from `api.v1.endpoints.generation_requests` and `api.v1.endpoints.n8n_callbacks`.
*   **Startup/Shutdown Events:**
    *   `@app.on_event("startup")`: Initialize RabbitMQ publisher connection, database engine (if not handled per-request).
    *   `@app.on_event("shutdown")`: Gracefully close RabbitMQ connection, database engine connections.
*   Runs the application using Uvicorn: `uvicorn.run(app, host="0.0.0.0", port=8000)`.