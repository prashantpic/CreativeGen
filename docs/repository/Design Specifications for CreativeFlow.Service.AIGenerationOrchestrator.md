# Software Design Specification (SDS) for CreativeFlow.Service.AIGenerationOrchestrator

## 1. Introduction

### 1.1. Purpose
This document specifies the software design for the **AIGenerationOrchestrator Service**. This service is a core component of the CreativeFlow AI platform, acting as the central coordinator for all AI-driven creative generation workflows. Its primary purpose is to receive generation requests, validate them against business rules (user credits and subscriptions), dispatch them for asynchronous processing, and handle the results. It decouples the user-facing API Gateway from the complexities of the underlying AI workflow engine (n8n), ensuring a responsive user experience and a resilient, scalable backend architecture.

### 1.2. Scope
The scope of this service includes:
- Exposing RESTful API endpoints for initiating AI generation and receiving asynchronous callbacks.
- Orchestrating the `Initiate Generation` and `Process n8n Result` use cases.
- Interfacing with external services for credit validation/deduction (Odoo Service), job queuing (RabbitMQ), and user notifications (Notification Service).
- Managing the state of generation requests in a persistent data store (PostgreSQL).

This document will provide detailed specifications for the application's architecture, components, data models, and interfaces, sufficient for implementation by the development team.

## 2. System Architecture & Design Principles

### 2.1. Architectural Style
The service will be designed as a self-contained microservice, adhering to the principles of a **Layered Architecture** and **Clean Architecture**. This promotes separation of concerns, testability, and maintainability.

- **Domain Layer**: Contains the core business logic and entities (`GenerationRequest` model).
- **Application Layer**: Orchestrates the use cases (`InitiateGenerationUseCase`, `ProcessN8NResultUseCase`) and defines interfaces for external dependencies.
- **Presentation Layer**: Exposes the functionality via RESTful APIs (FastAPI endpoints).
- **Infrastructure Layer**: Provides concrete implementations for external dependencies (database access, message queues, HTTP clients).

### 2.2. Key Design Patterns
- **Event-Driven Architecture (EDA)**: The service initiates long-running AI generation tasks by publishing events (jobs) to a RabbitMQ message queue. This decouples the service from the `n8n` workflow engine, improving scalability and resilience.
- **Repository Pattern**: Data access logic for the `GenerationRequest` entity will be encapsulated within a repository, abstracting the underlying database technology (SQLAlchemy) from the application layer.
- **Dependency Inversion Principle**: The application layer will depend on abstract interfaces (`interfaces.py`) rather than concrete implementations. Concrete infrastructure components will be injected at runtime, facilitating mocking and testing.
- **Data Transfer Objects (DTOs)**: Pydantic models will be used to define and validate the structure of data for API requests, responses, and event payloads, ensuring clear and robust data contracts.

### 2.3. Technology Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Data Access**: SQLAlchemy 2.0 (Core and ORM) with `asyncpg` driver for PostgreSQL.
- **Messaging**: Pika for RabbitMQ integration.
- **HTTP Client**: `httpx` for asynchronous communication with other services.
- **Configuration**: Pydantic for settings management.
- **Containerization**: Docker.

## 3. API Specification

The service will expose a versioned API under the path `/api/v1`.

### 3.1. Endpoint: Initiate Creative Generation
- **Path**: `/api/v1/generations/`
- **Method**: `POST`
- **Description**: Starts a new AI creative generation workflow.
- **Authentication**: Required. Expects a valid JWT from the API Gateway containing `user_id`.
- **Request Body**: `GenerationRequestCreateDTO`
  json
  {
    "projectId": "uuid-of-the-project",
    "inputPrompt": "A futuristic cityscape at sunset, synthwave style.",
    "styleGuidance": "vibrant pinks and blues, retro grid lines",
    "inputParameters": {
      "format": "InstagramStory",
      "resolution": "1080x1920",
      "samples": 4
    }
  }
  
- **Success Response (202 Accepted)**: `GenerationInitiatedResponseDTO`
  json
  {
    "generationId": "uuid-of-the-new-generation-request"
  }
  
- **Error Responses**:
    - `400 Bad Request`: Invalid request body.
    - `401 Unauthorized`: Invalid or missing JWT.
    - `402 Payment Required`: Insufficient credits for the operation.
    - `500 Internal Server Error`: Unexpected service error.

### 3.2. Endpoint: n8n Workflow Callback
- **Path**: `/api/v1/callbacks/n8n`
- **Method**: `POST`
- **Description**: A webhook endpoint for the n8n workflow engine to post back the results of a generation job.
- **Authentication**: Optional, can be secured via a static API key in the header if needed (`X-N8N-Webhook-Secret`).
- **Request Body**: `N8NCallbackDTO`
  json
  {
    "generationId": "uuid-of-the-generation-request",
    "status": "success", // or "failure"
    "stage": "samples_generated", // or "final_asset_generated"
    "results": {
      "sampleAssets": [
        {"assetId": "uuid1", "url": "/path/to/sample1.jpg"},
        {"assetId": "uuid2", "url": "/path/to/sample2.jpg"}
      ]
    },
    "error": null // or { "code": "AI_MODEL_UNAVAILABLE", "message": "..." }
  }
  
- **Success Response (200 OK)**: Empty body.
- **Error Responses**:
    - `400 Bad Request`: Invalid payload.
    - `404 Not Found`: `generationId` does not exist.
    - `500 Internal Server Error`: Error while processing the callback.

## 4. Core Domain Model

### 4.1. `GenerationRequest` Entity
This is the central domain model, representing a single AI generation job.

- **File**: `src/creativeflow/service/aigeneration_orchestrator/domain/models/generation_request.py`
- **Attributes**:
    - `id: UUID` (Primary Key)
    - `userId: UUID`
    - `projectId: UUID`
    - `inputPrompt: str`
    - `styleGuidance: Optional[str]`
    - `inputParameters: dict`
    - `status: str` (Enum: 'Pending', 'ProcessingSamples', 'AwaitingSelection', 'ProcessingFinal', 'Completed', 'Failed', 'Cancelled', 'ContentRejected')
    - `errorMessage: Optional[str]`
    - `sampleAssets: Optional[dict]`
    - `selectedSampleId: Optional[UUID]`
    - `finalAssetId: Optional[UUID]`
    - `creditsCostSample: Optional[Decimal]`
    - `creditsCostFinal: Optional[Decimal]`
    - `aiModelUsed: Optional[str]`
    - `createdAt: datetime`
    - `updatedAt: datetime`
- **State Transition Methods**:
    - `def mark_as_processing_samples(self) -> None`: Sets status to `ProcessingSamples`.
    - `def mark_as_awaiting_selection(self, sample_assets: dict) -> None`: Sets status and stores sample asset data.
    - `def select_sample(self, sample_id: UUID) -> None`: Sets status to `ProcessingFinal` and records `selectedSampleId`.
    - `def mark_as_completed(self, final_asset_id: UUID) -> None`: Sets status to `Completed` and records `finalAssetId`.
    - `def mark_as_failed(self, error_message: str) -> None`: Sets status to `Failed` and records the error message.

## 5. Application & Business Logic (Use Cases)

### 5.1. `InitiateGenerationUseCase`
- **File**: `src/creativeflow/service/aigeneration_orchestrator/app/use_cases/initiate_generation.py`
- **Logic**:
  1. **Constructor (`__init__`)**: Injects dependencies: `ICreditService`, `IJobPublisher`, `IGenerationRepository`.
  2. **`execute(user_id, request_data)` method**:
     a. Determine the initial credit cost (e.g., for sample generation) based on `request_data.inputParameters`.
     b. Call `credit_service.check_and_reserve_credits(user_id, cost)`.
        - If `False`, raise an `HTTPException(status_code=402, detail="Insufficient credits")`.
     c. Create a `GenerationRequest` domain entity instance with the input data and an initial `Pending` status.
     d. Persist the new entity using `generation_repo.add(generation_request)`.
     e. Construct the job payload for RabbitMQ. This dictionary must include `generationId`, `userId`, `inputPrompt`, and all other parameters needed by the n8n workflow.
     f. Publish the job using `job_publisher.publish_generation_job(job_payload)`.
     g. Return the created `GenerationRequest` entity, which will be mapped to a response DTO by the API layer.

### 5.2. `ProcessN8NResultUseCase`
- **File**: `src/creativeflow/service/aigeneration_orchestrator/app/use_cases/process_n8n_result.py`
- **Logic**:
  1. **Constructor (`__init__`)**: Injects dependencies: `IGenerationRepository`, `INotificationService`, `ICreditService`.
  2. **`execute(payload: N8NCallbackDTO)` method**:
     a. Retrieve the `GenerationRequest` using `generation_repo.get_by_id(payload.generationId)`.
        - If not found, log a critical error and return.
     b. **If `payload.status == 'failure'`**:
        - Call `generation_request.mark_as_failed(payload.error.message)`.
        - Persist the change using `generation_repo.update()`.
        - Call `credit_service.refund_credits()` for any reserved credits.
        - Call `notification_service.notify_user()` with a failure message.
        - Exit.
     c. **If `payload.status == 'success'`**:
        - **If `payload.stage == 'samples_generated'`**:
            - Call `generation_request.mark_as_awaiting_selection(payload.results.sampleAssets)`.
            - Persist the change using `generation_repo.update()`.
            - Call `credit_service.deduct_credits()` for the sample generation cost.
            - Call `notification_service.notify_user()` with a success message and sample data.
        - **If `payload.stage == 'final_asset_generated'`**:
            - Call `generation_request.mark_as_completed(payload.results.finalAssetId)`.
            - Persist the change using `generation_repo.update()`.
            - Call `credit_service.deduct_credits()` for the final generation cost.
            - Call `notification_service.notify_user()` with a completion message and final asset link.

## 6. Infrastructure & External Interfaces

### 6.1. Database (SQLAlchemy)
- **File**: `src/creativeflow/service/aigeneration_orchestrator/infrastructure/db/repositories/sqlalchemy_generation_repository.py`
- **Implementation**: The `SqlAlchemyGenerationRepository` will implement the `IGenerationRepository` interface.
- **ORM Model**: A SQLAlchemy ORM class will be defined to map the `GenerationRequest` domain entity to a `generation_requests` table in PostgreSQL.
- **Session Management**: A database session will be created per request using FastAPI's dependency injection system to ensure transactional integrity.

### 6.2. Messaging (RabbitMQ/Pika)
- **File**: `src/creativeflow/service/aigeneration_orchestrator/infrastructure/messaging/pika_publisher.py`
- **Implementation**: The `PikaJobPublisher` will implement the `IJobPublisher` interface.
- **Connection**: It will establish and manage a connection to RabbitMQ on application startup.
- **Queue/Exchange**: It will publish messages to a pre-defined, durable queue (e.g., `creativeflow.jobs.generation`) via a direct exchange.
- **Message Format**: Messages will be JSON strings. They will be published with the `delivery_mode=2` property to ensure they are persistent.

### 6.3. HTTP Clients (httpx)
- **File(s)**: `src/creativeflow/service/aigeneration_orchestrator/infrastructure/http_clients/*.py`
- **Implementation**:
    - **`OdooCreditService`**: Implements `ICreditService`. It will use an `httpx.AsyncClient` to make `POST` requests to the Odoo Service endpoints (e.g., `/credits/check_and_reserve`, `/credits/deduct`). It must handle connection errors, timeouts, and non-2xx responses gracefully.
    - **`HttpNotificationService`**: Implements `INotificationService`. It will use an `httpx.AsyncClient` to make a `POST` request to the Notification Service's `/notify` endpoint. It will operate in a "fire-and-forget" manner but log any failures.

## 7. Configuration
- **File**: `src/creativeflow/service/aigeneration_orchestrator/config/settings.py`
- The `Settings` class will load the following environment variables:
  - `DATABASE_URL`: SQLAlchemy connection string for PostgreSQL.
  - `DATABASE_POOL_SIZE`: Integer for DB connection pool size.
  - `RABBITMQ_URL`: AMQP connection string for RabbitMQ.
  - `GENERATION_JOB_QUEUE`: Name of the queue to publish jobs to.
  - `N8N_CALLBACK_SECRET`: Optional secret for securing the n8n webhook.
  - `ODOO_SERVICE_URL`: Base URL for the Odoo/CoreBusiness Service.
  - `NOTIFICATION_SERVICE_URL`: Base URL for the Notification Service.

## 8. Error Handling & Logging
- **Centralized Exception Handling**: A FastAPI middleware will be used to catch unhandled exceptions, log them, and return a standardized JSON error response (e.g., `{"error": "Internal Server Error", "request_id": "..."}`).
- **Logging**: The application will use Python's standard `logging` module, configured to output structured JSON logs. A middleware will generate and inject a unique correlation/request ID into every log message for a given request, enabling distributed tracing.
- **Business Exceptions**: Use cases will raise specific, custom exceptions (e.g., `InsufficientCreditsError`, `GenerationNotFoundError`) which the API layer will map to appropriate HTTP status codes (e.g., 402, 404).

## 9. Testing Strategy
- **Unit Tests**:
    - Use `pytest`.
    - All use cases will be tested by mocking the injected repository and service interfaces (`IGenerationRepository`, `IJobPublisher`, etc.).
    - Domain model state transitions will be thoroughly tested.
- **Integration Tests**:
    - Use `pytest` with `httpx.ASGITransport` to test the FastAPI application in-memory.
    - Test interactions with a real (test-containerized) PostgreSQL database and RabbitMQ instance to verify the infrastructure layer implementations.
    - Focus on the flow from API endpoint -> use case -> repository/publisher.