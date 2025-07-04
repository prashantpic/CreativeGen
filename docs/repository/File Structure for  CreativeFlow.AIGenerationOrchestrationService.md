# Specification

# 1. Files

- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/main.py  
**Description:** Main application entry point for the FastAPI AI Generation Orchestration Service. Initializes the FastAPI app, includes routers, and sets up middleware and event handlers.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 4  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Microservice
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - FastAPI Application Setup
    
**Requirement Ids:**
    
    - Section 5.3.1
    
**Purpose:** Initializes and runs the FastAPI application.  
**Logic Description:** Creates a FastAPI app instance. Includes API routers from the api.v1.endpoints module. Configures CORS, logging, and exception handling. Sets up startup/shutdown event handlers if needed (e.g., for DB connections, RabbitMQ client).  
**Documentation:**
    
    - **Summary:** Bootstraps the AI Generation Orchestration Service.
    
**Namespace:** creativeflow.services.aigeneration  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/core/config.py  
**Description:** Handles application configuration using Pydantic Settings. Loads settings from environment variables or .env files.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** core/config.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** PROJECT_NAME  
**Type:** str  
**Attributes:**   
    - **Name:** API_V1_STR  
**Type:** str  
**Attributes:**   
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** RABBITMQ_URL  
**Type:** str  
**Attributes:**   
    - **Name:** N8N_CALLBACK_URL  
**Type:** str  
**Attributes:**   
    - **Name:** CREDIT_SERVICE_URL  
**Type:** str  
**Attributes:**   
    - **Name:** NOTIFICATION_SERVICE_URL  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** Provides a centralized way to manage and access application settings.  
**Logic Description:** Defines a Pydantic BaseModel or Settings class to load configuration variables such as database connection strings, RabbitMQ URL, external service URLs, API prefixes, etc., from environment variables or a .env file. Includes validation for essential settings.  
**Documentation:**
    
    - **Summary:** Manages application-wide configuration settings.
    
**Namespace:** creativeflow.services.aigeneration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/core/dependencies.py  
**Description:** Defines FastAPI dependencies for dependency injection, such as database sessions or service clients.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** dependencies  
**Type:** DependencyInjection  
**Relative Path:** core/dependencies.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[Session|AsyncSession, None, None]  
**Attributes:**   
    - **Name:** get_rabbitmq_publisher  
**Parameters:**
    
    
**Return Type:** RabbitMQPublisher  
**Attributes:**   
    - **Name:** get_generation_request_repo  
**Parameters:**
    
    - db_session: Session = Depends(get_db_session)
    
**Return Type:** IGenerationRequestRepository  
**Attributes:**   
    - **Name:** get_orchestration_service  
**Parameters:**
    
    - repo: IGenerationRequestRepository = Depends(get_generation_request_repo)
    - publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher)
    
**Return Type:** OrchestrationService  
**Attributes:**   
    
**Implemented Features:**
    
    - Dependency Injection Setup
    
**Requirement Ids:**
    
    
**Purpose:** Manages and provides dependencies to FastAPI path operations and services.  
**Logic Description:** Contains functions that act as FastAPI dependencies. For example, a function to provide a database session, another for a RabbitMQ publisher instance, or instances of repository/service classes. These are injected into endpoint handlers.  
**Documentation:**
    
    - **Summary:** Sets up dependency injection for the application.
    
**Namespace:** creativeflow.services.aigeneration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/core/error_handlers.py  
**Description:** Custom exception handlers for FastAPI to provide standardized error responses.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** error_handlers  
**Type:** ErrorHandling  
**Relative Path:** core/error_handlers.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validation_exception_handler  
**Parameters:**
    
    - request: Request
    - exc: RequestValidationError
    
**Return Type:** JSONResponse  
**Attributes:**   
    - **Name:** custom_app_exception_handler  
**Parameters:**
    
    - request: Request
    - exc: CustomAppException
    
**Return Type:** JSONResponse  
**Attributes:**   
    
**Implemented Features:**
    
    - Standardized Error Responses
    
**Requirement Ids:**
    
    - REQ-007.1
    
**Purpose:** Defines custom exception handlers to convert application exceptions into structured JSON error responses.  
**Logic Description:** Implements FastAPI exception handlers for Pydantic's RequestValidationError and any custom application exceptions. Ensures error responses are consistent and informative for API consumers.  
**Documentation:**
    
    - **Summary:** Provides global error handling for the FastAPI application.
    
**Namespace:** creativeflow.services.aigeneration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/core/logging_config.py  
**Description:** Configuration for application-wide logging.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** logging_config  
**Type:** Logging  
**Relative Path:** core/logging_config.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str = 'INFO'
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - Centralized Logging
    
**Requirement Ids:**
    
    - REQ-007.1
    
**Purpose:** Configures the logging format, level, and handlers for the application.  
**Logic Description:** Uses Python's built-in `logging` module to set up structured logging (e.g., JSON format), configure log levels based on environment settings, and define handlers (e.g., console, file).  
**Documentation:**
    
    - **Summary:** Initializes and configures application logging.
    
**Namespace:** creativeflow.services.aigeneration.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/api/v1/endpoints/generation_requests.py  
**Description:** FastAPI router for handling AI creative generation requests.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** generation_requests_router  
**Type:** Controller  
**Relative Path:** api/v1/endpoints/generation_requests.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_generation_request_endpoint  
**Parameters:**
    
    - request_payload: GenerationRequestCreate
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** GenerationRequestRead  
**Attributes:** async def  
    - **Name:** get_generation_request_status_endpoint  
**Parameters:**
    
    - request_id: UUID
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** GenerationRequestRead  
**Attributes:** async def  
    - **Name:** select_sample_for_final_generation_endpoint  
**Parameters:**
    
    - request_id: UUID
    - sample_selection: SampleSelection
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** GenerationRequestRead  
**Attributes:** async def  
    - **Name:** regenerate_samples_endpoint  
**Parameters:**
    
    - request_id: UUID
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** GenerationRequestRead  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Initiate Creative Generation
    - Get Generation Status
    - Select Sample
    - Regenerate Samples
    
**Requirement Ids:**
    
    - REQ-005
    - REQ-008
    - REQ-009
    - Section 5.3.1
    
**Purpose:** Exposes HTTP endpoints for clients to initiate, monitor, and manage AI generation tasks.  
**Logic Description:** Defines FastAPI path operations for creating new generation requests, retrieving status of existing requests, selecting samples for final generation, and triggering sample regeneration. Delegates business logic to the OrchestrationService.  
**Documentation:**
    
    - **Summary:** Handles API requests related to AI creative generation.
    
**Namespace:** creativeflow.services.aigeneration.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/api/v1/endpoints/n8n_callbacks.py  
**Description:** FastAPI router for handling callbacks from the n8n Workflow Engine.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 3  
**Name:** n8n_callbacks_router  
**Type:** Controller  
**Relative Path:** api/v1/endpoints/n8n_callbacks.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** handle_n8n_sample_generation_callback  
**Parameters:**
    
    - callback_payload: N8NSampleResultPayload
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** dict  
**Attributes:** async def  
    - **Name:** handle_n8n_final_generation_callback  
**Parameters:**
    
    - callback_payload: N8NFinalResultPayload
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** dict  
**Attributes:** async def  
    - **Name:** handle_n8n_error_callback  
**Parameters:**
    
    - callback_payload: N8NErrorPayload
    - orchestration_svc: OrchestrationService = Depends(get_orchestration_service)
    
**Return Type:** dict  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Process n8n Sample Results
    - Process n8n Final Asset Results
    - Process n8n Errors
    
**Requirement Ids:**
    
    - REQ-007.1
    - REQ-008
    - REQ-009
    - Section 5.3.1
    
**Purpose:** Provides webhook endpoints for n8n to send updates on generation job status, results, and errors.  
**Logic Description:** Defines FastAPI path operations to receive HTTP POST requests from n8n. Parses callback payloads and delegates processing to the OrchestrationService (e.g., updating request status, storing asset metadata, triggering notifications).  
**Documentation:**
    
    - **Summary:** Handles asynchronous callbacks from the n8n workflow engine.
    
**Namespace:** creativeflow.services.aigeneration.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/api/v1/schemas.py  
**Description:** Pydantic models for API request and response data structures (DTOs).  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** api_schemas  
**Type:** DataTransferObject  
**Relative Path:** api/v1/schemas.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Data Contracts
    
**Requirement Ids:**
    
    - REQ-005
    - REQ-006
    - REQ-007
    - REQ-008
    - REQ-009
    
**Purpose:** Defines the data structures for requests and responses handled by the API endpoints.  
**Logic Description:** Contains Pydantic models representing: GenerationRequestCreate (input for new requests, including prompt, format, dimensions, style guidance, brand elements), GenerationRequestRead (output for request status and results), SampleAssetInfo, FinalAssetInfo, ErrorResponse, N8NSampleResultPayload, N8NFinalResultPayload, N8NErrorPayload, SampleSelection.  
**Documentation:**
    
    - **Summary:** Specifies data contracts for the AI Generation Orchestration API.
    
**Namespace:** creativeflow.services.aigeneration.api.v1  
**Metadata:**
    
    - **Category:** API
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/application/services/orchestration_service.py  
**Description:** Core application service for orchestrating the AI creative generation pipeline.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** orchestration_service  
**Type:** ApplicationService  
**Relative Path:** application/services/orchestration_service.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    - **Name:** _repo  
**Type:** IGenerationRequestRepository  
**Attributes:** private  
    - **Name:** _rabbitmq_publisher  
**Type:** RabbitMQPublisher  
**Attributes:** private  
    - **Name:** _credit_service_client  
**Type:** CreditServiceClient  
**Attributes:** private  
    - **Name:** _notification_client  
**Type:** NotificationServiceClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** initiate_generation  
**Parameters:**
    
    - user_id: str
    - project_id: str
    - request_data: GenerationRequestCreateDTO
    
**Return Type:** GenerationRequest  
**Attributes:** async def  
    - **Name:** get_generation_status  
**Parameters:**
    
    - request_id: UUID
    
**Return Type:** GenerationRequest  
**Attributes:** async def  
    - **Name:** process_n8n_sample_callback  
**Parameters:**
    
    - callback_data: N8NSampleResultDTO
    
**Return Type:** None  
**Attributes:** async def  
    - **Name:** process_n8n_final_asset_callback  
**Parameters:**
    
    - callback_data: N8NFinalResultDTO
    
**Return Type:** None  
**Attributes:** async def  
    - **Name:** handle_n8n_error  
**Parameters:**
    
    - error_data: N8NErrorDTO
    
**Return Type:** None  
**Attributes:** async def  
    - **Name:** trigger_sample_regeneration  
**Parameters:**
    
    - request_id: UUID
    - user_id: str
    
**Return Type:** GenerationRequest  
**Attributes:** async def  
    - **Name:** select_sample_and_initiate_final  
**Parameters:**
    
    - request_id: UUID
    - selected_sample_id: str
    - user_id: str
    
**Return Type:** GenerationRequest  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Creative Generation Orchestration
    - Status Tracking
    - Result Handling
    - Error Management
    - Credit Coordination
    - n8n Integration Management
    
**Requirement Ids:**
    
    - REQ-005
    - REQ-006
    - REQ-007
    - REQ-007.1
    - REQ-008
    - REQ-009
    - REQ-016 (Credit deduction coordination)
    - Section 5.3.1
    
**Purpose:** Manages the end-to-end AI creative generation process, from request intake to final asset delivery notification.  
**Logic Description:** Validates incoming generation requests. Interacts with CreditServiceClient for credit checks and deductions. Prepares job parameters (including format, dimensions, prompts, style, brand elements, templates, tone, cultural adaptation hints). Publishes jobs to RabbitMQ for n8n. Updates GenerationRequest status in the database. Processes callbacks from n8n (sample results, final asset results, errors). Triggers notifications via NotificationServiceClient. Implements logic for sample regeneration and final asset generation from a selected sample. Handles error scenarios and determines if credits should be refunded. Coordinates with AIModelSelector if advanced model selection logic is implemented.  
**Documentation:**
    
    - **Summary:** Orchestrates AI creative generation workflows.
    
**Namespace:** creativeflow.services.aigeneration.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/application/services/credit_service_client.py  
**Description:** Client for interacting with the external Credit/Subscription Service (likely an Odoo adapter or dedicated billing service).  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** credit_service_client  
**Type:** ServiceClient  
**Relative Path:** application/services/credit_service_client.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** _base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** _http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** check_credits  
**Parameters:**
    
    - user_id: str
    - required_credits: float
    
**Return Type:** bool  
**Attributes:** async def  
    - **Name:** deduct_credits  
**Parameters:**
    
    - user_id: str
    - request_id: UUID
    - amount: float
    - action_type: str
    
**Return Type:** bool  
**Attributes:** async def  
    - **Name:** refund_credits  
**Parameters:**
    
    - user_id: str
    - request_id: UUID
    - amount: float
    - reason: str
    
**Return Type:** bool  
**Attributes:** async def  
    - **Name:** get_user_subscription_tier  
**Parameters:**
    
    - user_id: str
    
**Return Type:** str  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Credit Check
    - Credit Deduction
    - Credit Refund
    - Subscription Tier Check
    
**Requirement Ids:**
    
    - REQ-016 (Credit deduction coordination)
    - REQ-007.1
    - REQ-009
    
**Purpose:** Provides an interface to manage user credits and check subscription status by calling an external service.  
**Logic Description:** Makes HTTP requests to the Credit/Subscription service API endpoints. Handles API responses and errors. Encapsulates the communication details for credit operations.  
**Documentation:**
    
    - **Summary:** Client for the external user credit and subscription management service.
    
**Namespace:** creativeflow.services.aigeneration.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/application/services/notification_service_client.py  
**Description:** Client for interacting with the Notification Service.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** notification_service_client  
**Type:** ServiceClient  
**Relative Path:** application/services/notification_service_client.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** _base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** _http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send_notification  
**Parameters:**
    
    - user_id: str
    - message: str
    - notification_type: str
    - metadata: dict = None
    
**Return Type:** None  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Send User Notifications
    
**Requirement Ids:**
    
    - Section 5.3.1
    
**Purpose:** Provides an interface to send notifications to users via the dedicated Notification Service.  
**Logic Description:** Makes HTTP requests to the Notification Service API to trigger user notifications (e.g., generation complete, error occurred). Encapsulates the communication details.  
**Documentation:**
    
    - **Summary:** Client for the external Notification Service.
    
**Namespace:** creativeflow.services.aigeneration.application.services  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/application/dtos.py  
**Description:** Internal Data Transfer Objects (DTOs) used within the application layer, potentially differing from API schemas.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** application_dtos  
**Type:** DataTransferObject  
**Relative Path:** application/dtos.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Internal Data Contracts
    
**Requirement Ids:**
    
    
**Purpose:** Defines data structures for internal use between application services and domain layers.  
**Logic Description:** Contains Pydantic models for internal data representation, e.g., `GenerationJobParameters`, `N8NResultInternal`, `CreditServiceRequest`. This helps decouple application logic from specific API schema versions.  
**Documentation:**
    
    - **Summary:** Data Transfer Objects for internal application logic.
    
**Namespace:** creativeflow.services.aigeneration.application  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/domain/models/generation_request.py  
**Description:** Domain model representing an AI creative generation request.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** generation_request_model  
**Type:** DomainModel  
**Relative Path:** domain/models/generation_request.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Entity
    - AggregateRoot
    
**Members:**
    
    - **Name:** id  
**Type:** UUID  
**Attributes:**   
    - **Name:** user_id  
**Type:** str  
**Attributes:**   
    - **Name:** project_id  
**Type:** str  
**Attributes:**   
    - **Name:** input_prompt  
**Type:** str  
**Attributes:**   
    - **Name:** style_guidance  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** input_parameters  
**Type:** dict  
**Attributes:** Contains format, resolution, brand_elements, etc.  
    - **Name:** status  
**Type:** GenerationStatus  
**Attributes:**   
    - **Name:** error_message  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** sample_asset_infos  
**Type:** List[AssetInfo]  
**Attributes:**   
    - **Name:** selected_sample_id  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** final_asset_info  
**Type:** Optional[AssetInfo]  
**Attributes:**   
    - **Name:** credits_cost_sample  
**Type:** Optional[float]  
**Attributes:**   
    - **Name:** credits_cost_final  
**Type:** Optional[float]  
**Attributes:**   
    - **Name:** ai_model_used  
**Type:** Optional[str]  
**Attributes:**   
    - **Name:** created_at  
**Type:** datetime  
**Attributes:**   
    - **Name:** updated_at  
**Type:** datetime  
**Attributes:**   
    
**Methods:**
    
    - **Name:** update_status  
**Parameters:**
    
    - new_status: GenerationStatus
    - error_message: Optional[str] = None
    
**Return Type:** None  
**Attributes:**   
    - **Name:** add_sample_result  
**Parameters:**
    
    - sample_asset: AssetInfo
    
**Return Type:** None  
**Attributes:**   
    - **Name:** set_final_asset  
**Parameters:**
    
    - final_asset: AssetInfo
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - Generation Request State Management
    
**Requirement Ids:**
    
    - REQ-005
    - REQ-006
    - REQ-007
    - REQ-008
    - REQ-009
    
**Purpose:** Encapsulates the data and behavior of an AI generation request throughout its lifecycle.  
**Logic Description:** Represents a single AI generation task. Holds all input parameters, tracks its current status (e.g., Pending, ProcessingSamples, AwaitingSelection, Completed, Failed), stores references to generated sample and final assets, and associated costs. Methods manage state transitions.  
**Documentation:**
    
    - **Summary:** Core domain entity for AI generation requests.
    
**Namespace:** creativeflow.services.aigeneration.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/domain/models/generation_status.py  
**Description:** Enum defining possible statuses for a generation request.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** generation_status_enum  
**Type:** Enum  
**Relative Path:** domain/models/generation_status.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** PENDING  
**Type:** str  
**Attributes:**   
    - **Name:** VALIDATING_CREDITS  
**Type:** str  
**Attributes:**   
    - **Name:** PUBLISHING_TO_QUEUE  
**Type:** str  
**Attributes:**   
    - **Name:** PROCESSING_SAMPLES  
**Type:** str  
**Attributes:**   
    - **Name:** AWAITING_SELECTION  
**Type:** str  
**Attributes:**   
    - **Name:** PROCESSING_FINAL  
**Type:** str  
**Attributes:**   
    - **Name:** COMPLETED  
**Type:** str  
**Attributes:**   
    - **Name:** FAILED  
**Type:** str  
**Attributes:**   
    - **Name:** CONTENT_REJECTED  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - Generation Status Definition
    
**Requirement Ids:**
    
    - REQ-008
    - REQ-009
    - Section 5.3.1
    
**Purpose:** Provides a standardized set of statuses for AI generation requests.  
**Logic Description:** Defines an enumeration (e.g., using Python's `Enum` class) for all possible states of a generation request.  
**Documentation:**
    
    - **Summary:** Enumeration of AI generation request statuses.
    
**Namespace:** creativeflow.services.aigeneration.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/domain/models/asset_info.py  
**Description:** Value object representing information about a generated asset.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** asset_info_vo  
**Type:** ValueObject  
**Relative Path:** domain/models/asset_info.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - ValueObject
    
**Members:**
    
    - **Name:** asset_id  
**Type:** str  
**Attributes:** Identifier for the asset in the asset management system/MinIO  
    - **Name:** url  
**Type:** str  
**Attributes:** URL to access the asset  
    - **Name:** resolution  
**Type:** Optional[str]  
**Attributes:** e.g., '512x512'  
    - **Name:** format  
**Type:** str  
**Attributes:** e.g., 'png', 'jpg'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Information Representation
    
**Requirement Ids:**
    
    - REQ-008
    - REQ-009
    
**Purpose:** A_ACTION_INPUT_CONTEXT_ASSIST_TEXT_START_A_ACTION_INPUT_CONTEXT_ASSIST_TEXT_STARTProvides a structured way to represent details of a generated creative asset.A_ACTION_INPUT_CONTEXT_ASSIST_TEXT_END  
**Logic Description:** A Pydantic BaseModel or dataclass representing immutable asset information such as its ID (reference to an asset management system or MinIO path), access URL, resolution, and format.  
**Documentation:**
    
    - **Summary:** Value object for generated asset details.
    
**Namespace:** creativeflow.services.aigeneration.domain.models  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/domain/repositories/generation_request_repository.py  
**Description:** Interface (abstract base class) for the GenerationRequest repository.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** generation_request_repository_interface  
**Type:** RepositoryInterface  
**Relative Path:** domain/repositories/generation_request_repository.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Repository
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - request_id: UUID
    
**Return Type:** Optional[GenerationRequest]  
**Attributes:** abstractmethod async def  
    - **Name:** add  
**Parameters:**
    
    - generation_request: GenerationRequest
    
**Return Type:** None  
**Attributes:** abstractmethod async def  
    - **Name:** update  
**Parameters:**
    
    - generation_request: GenerationRequest
    
**Return Type:** None  
**Attributes:** abstractmethod async def  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    - skip: int = 0
    - limit: int = 100
    
**Return Type:** List[GenerationRequest]  
**Attributes:** abstractmethod async def  
    
**Implemented Features:**
    
    - Generation Request Persistence Contract
    
**Requirement Ids:**
    
    
**Purpose:** Defines the contract for data access operations related to GenerationRequest entities.  
**Logic Description:** An abstract base class (ABC) defining methods for CRUD operations on GenerationRequest entities (e.g., save, find by ID, find by user, update status).  
**Documentation:**
    
    - **Summary:** Repository interface for AI generation requests.
    
**Namespace:** creativeflow.services.aigeneration.domain.repositories  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/domain/events.py  
**Description:** Defines domain events related to the AI generation lifecycle.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 0  
**Name:** domain_events  
**Type:** DomainEvent  
**Relative Path:** domain/events.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - DomainEvents
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Domain Event Definitions
    
**Requirement Ids:**
    
    
**Purpose:** Defines events that occur within the AI generation domain, used for decoupling and reacting to state changes.  
**Logic Description:** Pydantic models or dataclasses representing domain events like `GenerationRequestInitiatedEvent`, `SampleGenerationCompletedEvent`, `FinalAssetGeneratedEvent`, `GenerationFailedEvent`. These events carry relevant data about the occurrence.  
**Documentation:**
    
    - **Summary:** Domain events for the AI generation process.
    
**Namespace:** creativeflow.services.aigeneration.domain  
**Metadata:**
    
    - **Category:** DomainLogic
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/infrastructure/repositories/postgres_generation_request_repository.py  
**Description:** PostgreSQL implementation of the IGenerationRequestRepository interface.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** postgres_generation_request_repository  
**Type:** RepositoryImplementation  
**Relative Path:** infrastructure/repositories/postgres_generation_request_repository.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Repository
    
**Members:**
    
    - **Name:** _db_session  
**Type:** Session | AsyncSession  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** get_by_id  
**Parameters:**
    
    - request_id: UUID
    
**Return Type:** Optional[GenerationRequest]  
**Attributes:** async def  
    - **Name:** add  
**Parameters:**
    
    - generation_request: GenerationRequest
    
**Return Type:** None  
**Attributes:** async def  
    - **Name:** update  
**Parameters:**
    
    - generation_request: GenerationRequest
    
**Return Type:** None  
**Attributes:** async def  
    - **Name:** list_by_user_id  
**Parameters:**
    
    - user_id: str
    - skip: int = 0
    - limit: int = 100
    
**Return Type:** List[GenerationRequest]  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Generation Request Persistence to PostgreSQL
    
**Requirement Ids:**
    
    - Section 5.3.1
    
**Purpose:** Handles data access operations for GenerationRequest entities using PostgreSQL.  
**Logic Description:** Implements the methods defined in `IGenerationRequestRepository` using SQLAlchemy (or another ORM/query builder) to interact with the PostgreSQL database. Handles mapping between domain models and database schema.  
**Documentation:**
    
    - **Summary:** PostgreSQL repository for AI generation requests.
    
**Namespace:** creativeflow.services.aigeneration.infrastructure.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/infrastructure/messaging/rabbitmq_publisher.py  
**Description:** Client for publishing messages (generation jobs) to RabbitMQ.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** rabbitmq_publisher  
**Type:** MessageProducer  
**Relative Path:** infrastructure/messaging/rabbitmq_publisher.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _connection_url  
**Type:** str  
**Attributes:** private  
    - **Name:** _connection  
**Type:** pika.BlockingConnection  
**Attributes:** private  
    - **Name:** _channel  
**Type:** pika.channel.Channel  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:**   
    - **Name:** publish_generation_job  
**Parameters:**
    
    - job_payload: dict
    - routing_key: str
    - exchange_name: str = 'generation_jobs'
    
**Return Type:** None  
**Attributes:**   
    - **Name:** close  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - Publish Generation Jobs to RabbitMQ
    
**Requirement Ids:**
    
    - Section 5.3.1
    
**Purpose:** Encapsulates the logic for connecting to RabbitMQ and publishing messages.  
**Logic Description:** Uses the Pika library to establish a connection to RabbitMQ. Provides methods to publish messages (e.g., serialized generation job parameters) to specific exchanges and routing keys. Handles connection management and error scenarios.  
**Documentation:**
    
    - **Summary:** RabbitMQ client for publishing messages.
    
**Namespace:** creativeflow.services.aigeneration.infrastructure.messaging  
**Metadata:**
    
    - **Category:** Messaging
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/infrastructure/database/db_config.py  
**Description:** Database connection and session management setup (SQLAlchemy).  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 1  
**Name:** db_config  
**Type:** DatabaseConfiguration  
**Relative Path:** infrastructure/database/db_config.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** engine  
**Type:** Engine | AsyncEngine  
**Attributes:** global  
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:** global  
    
**Methods:**
    
    - **Name:** init_db  
**Parameters:**
    
    - database_url: str
    
**Return Type:** None  
**Attributes:**   
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Generator[Session|AsyncSession, None, None]  
**Attributes:**   
    
**Implemented Features:**
    
    - Database Connection Management
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the database engine and session factory for SQLAlchemy.  
**Logic Description:** Sets up the SQLAlchemy engine using the database URL from configuration. Creates a `sessionmaker` for creating database sessions. Provides a dependency function (`get_db`) for FastAPI to inject sessions into repository instances.  
**Documentation:**
    
    - **Summary:** Configuration and session management for the PostgreSQL database.
    
**Namespace:** creativeflow.services.aigeneration.infrastructure.database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/infrastructure/clients/odoo_adapter_client.py  
**Description:** Client for interacting with Odoo backend (specifically for credit checks, deductions, and subscription validation if not handled by a separate billing service).  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** odoo_adapter_client  
**Type:** ServiceClient  
**Relative Path:** infrastructure/clients/odoo_adapter_client.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** _odoo_url  
**Type:** str  
**Attributes:** private  
    - **Name:** _odoo_db  
**Type:** str  
**Attributes:** private  
    - **Name:** _odoo_uid  
**Type:** int  
**Attributes:** private  
    - **Name:** _odoo_password  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** call_odoo_rpc  
**Parameters:**
    
    - model: str
    - method: str
    - args: list
    - kwargs: dict = None
    
**Return Type:** Any  
**Attributes:** async def  
    - **Name:** validate_user_subscription_and_credits  
**Parameters:**
    
    - user_id: str
    - required_credits: float
    
**Return Type:** Tuple[bool, str]  
**Attributes:** async def 'Returns (isValid, reason_if_not_valid)'  
    - **Name:** deduct_user_credits  
**Parameters:**
    
    - user_id: str
    - generation_request_id: UUID
    - credits_to_deduct: float
    - action_description: str
    
**Return Type:** bool  
**Attributes:** async def  
    - **Name:** refund_user_credits  
**Parameters:**
    
    - user_id: str
    - generation_request_id: UUID
    - credits_to_refund: float
    - reason: str
    
**Return Type:** bool  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Odoo Credit Check
    - Odoo Credit Deduction
    - Odoo Credit Refund
    
**Requirement Ids:**
    
    - REQ-016 (Credit deduction coordination)
    - REQ-007.1
    - Section 5.3.1
    
**Purpose:** Acts as an adapter to the Odoo system for functionalities related to user credits, subscriptions, and potentially triggering Odoo-side updates post-generation.  
**Logic Description:** Uses Odoo's XML-RPC or JSON-RPC API to communicate with the Odoo instance. Implements methods to check a user's credit balance against a required amount, instruct Odoo to deduct credits for a generation, and request credit refunds in case of system errors. May also fetch subscription status if needed by model selection logic.  
**Documentation:**
    
    - **Summary:** Client adapter for interacting with the Odoo backend for billing/credit operations.
    
**Namespace:** creativeflow.services.aigeneration.infrastructure.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** services/aigen-orchestration-service/src/creativeflow/services/aigeneration/infrastructure/clients/notification_client.py  
**Description:** Client to send notification requests to the dedicated Notification Service.  
**Template:** Python FastAPI Service Template  
**Dependency Level:** 2  
**Name:** notification_client  
**Type:** ServiceClient  
**Relative Path:** infrastructure/clients/notification_client.py  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** _notification_service_url  
**Type:** str  
**Attributes:** private  
    - **Name:** _http_client  
**Type:** httpx.AsyncClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send_user_notification  
**Parameters:**
    
    - user_id: str
    - notification_type: str
    - message: str
    - payload: dict = None
    
**Return Type:** None  
**Attributes:** async def  
    
**Implemented Features:**
    
    - Trigger User Notifications
    
**Requirement Ids:**
    
    - Section 5.3.1
    
**Purpose:** Facilitates sending notifications (e.g., generation status updates) to users by calling the central Notification Service.  
**Logic Description:** Makes HTTP requests to the Notification Service's API endpoints, passing user ID, notification type, message content, and any relevant payload (e.g., link to the generated asset).  
**Documentation:**
    
    - **Summary:** Client for the CreativeFlow Notification Service.
    
**Namespace:** creativeflow.services.aigeneration.infrastructure.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** services/aigen-orchestration-service/pyproject.toml  
**Description:** Python project configuration file using Poetry or similar. Defines dependencies, project metadata, and build settings.  
**Template:** Python Project File  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** BuildConfiguration  
**Relative Path:** ../../pyproject.toml  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    - Project Build Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Manages project dependencies and build configurations for the AI Generation Orchestration Service.  
**Logic Description:** Specifies dependencies like FastAPI, Uvicorn, Pydantic, Pika, SQLAlchemy, Alembic (if used), httpx. Also includes project metadata such as name, version, authors, and scripts for running/testing.  
**Documentation:**
    
    - **Summary:** Project configuration and dependency management file.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** services/aigen-orchestration-service/.env.example  
**Description:** Example environment file showing required configuration variables.  
**Template:** Environment File  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** ConfigurationTemplate  
**Relative Path:** ../../.env.example  
**Repository Id:** REPO-AIGEN-ORCH-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Example
    
**Requirement Ids:**
    
    
**Purpose:** Provides a template for developers to set up their local environment variables.  
**Logic Description:** Lists all environment variables used by `core/config.py` with placeholder or example values, e.g., DATABASE_URL, RABBITMQ_URL, CREDIT_SERVICE_URL, etc.  
**Documentation:**
    
    - **Summary:** Example environment configuration file.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_advanced_model_selector
  - enable_detailed_n8n_error_logging
  - enable_credit_refund_on_system_failure
  
- **Database Configs:**
  
  - AIGEN_DB_HOST
  - AIGEN_DB_PORT
  - AIGEN_DB_USER
  - AIGEN_DB_PASSWORD
  - AIGEN_DB_NAME
  
- **Message Queue Configs:**
  
  - RABBITMQ_HOST
  - RABBITMQ_PORT
  - RABBITMQ_USER
  - RABBITMQ_PASSWORD
  - RABBITMQ_VHOST
  - RABBITMQ_GENERATION_EXCHANGE
  - RABBITMQ_N8N_JOB_QUEUE
  - RABBITMQ_N8N_JOB_ROUTING_KEY
  
- **Service Endpoints:**
  
  - CREDIT_SERVICE_API_URL
  - NOTIFICATION_SERVICE_API_URL
  - N8N_CALLBACK_BASE_URL
  
- **Logging Configs:**
  
  - LOG_LEVEL
  - LOG_FORMAT
  


---

