# Specification

# 1. Files

- **Path:** workflows/main_orchestrators/CreativeGeneration_Main.workflow.json  
**Description:** Main n8n workflow orchestrating the end-to-end AI creative generation process. This includes receiving generation requests, calling sub-workflows for data preprocessing, AI model interaction, sample generation, high-resolution output, error handling, and communication with other services (Odoo, Notification Service, MinIO).  
**Template:** n8n Workflow JSON  
**Dependency Level:** 1  
**Name:** CreativeGeneration_Main.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** main_orchestrators/CreativeGeneration_Main.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - OrchestratorPattern
    - SubWorkflowPattern
    - EventDrivenArchitecture
    
**Members:**
    
    - **Name:** triggerNodeConfig  
**Type:** Object  
**Attributes:** config  
    - **Name:** aiModelSelectionLogic  
**Type:** Object  
**Attributes:** config  
    - **Name:** sampleGenerationLoopConfig  
**Type:** Object  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** HandleGenerationRequest  
**Parameters:**
    
    - jobData
    
**Return Type:** void  
**Attributes:** workflow_stage  
    - **Name:** OrchestrateSampleGeneration  
**Parameters:**
    
    - processedInput
    
**Return Type:** Array<SampleAsset>  
**Attributes:** workflow_stage  
    - **Name:** OrchestrateHighResGeneration  
**Parameters:**
    
    - selectedSample
    - originalRequest
    
**Return Type:** FinalAsset  
**Attributes:** workflow_stage  
    - **Name:** NotifyCompletion  
**Parameters:**
    
    - generationResult
    
**Return Type:** void  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - End-to-end AI creative generation orchestration
    - Multi-format creative generation
    - Four-sample preview system
    - Progressive enhancement workflow (low-res to high-res)
    - Integration with various AI models and internal services
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n role in pipeline)
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    - REQ-3-005
    - REQ-3-006
    - REQ-3-007
    - REQ-3-008
    - REQ-3-009
    - REQ-3-010
    - REQ-3-011
    - REQ-3-012
    - REQ-3-013
    - REQ-3-015
    - INT-005
    - INT-006
    - AISIML-005
    
**Purpose:** Orchestrates the entire AI creative generation lifecycle from request intake to final asset delivery and notification.  
**Logic Description:** Triggered by RabbitMQ message. Fetches secure API keys. Preprocesses input. Applies brand/style. Selects AI model. Generates samples using AI sub-workflows. Handles errors. Stores samples in MinIO. Notifies Odoo/User. Waits for sample selection. Generates high-res output. Stores final asset. Notifies Odoo/User. Includes error handling for each major step and content safety checks.  
**Documentation:**
    
    - **Summary:** The central workflow coordinating all steps for AI creative generation. Inputs: generation job data from RabbitMQ. Outputs: final asset details, status updates to Odoo and Notification Service.
    
**Namespace:** CreativeFlow.N8N.Workflows.MainOrchestrators  
**Metadata:**
    
    - **Category:** WorkflowOrchestration
    
- **Path:** workflows/sub_workflows/ai_services/ImageGeneration_OpenAI_Dalle.subworkflow.json  
**Description:** Sub-workflow dedicated to generating images using OpenAI DALL-E API. Handles API authentication, request formatting, and response parsing.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** ImageGeneration_OpenAI_Dalle.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/ai_services/ImageGeneration_OpenAI_Dalle.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** openAICredentials  
**Type:** Object  
**Attributes:** config  
    - **Name:** dalleApiEndpoint  
**Type:** String  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** GenerateImage  
**Parameters:**
    
    - prompt
    - size
    - quality
    - apiKey
    
**Return Type:** ImageObject  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - OpenAI DALL-E image generation
    
**Requirement Ids:**
    
    - INT-005
    
**Purpose:** Encapsulates the logic for interacting with the OpenAI DALL-E API for image generation.  
**Logic Description:** Receives prompt and generation parameters. Retrieves OpenAI API key securely (potentially via credential node or dedicated API key fetcher sub-workflow). Formats request for DALL-E API. Makes HTTP request. Parses response. Handles API-specific errors. Returns generated image data or reference.  
**Documentation:**
    
    - **Summary:** Sub-workflow for OpenAI DALL-E image generation. Inputs: prompt, parameters. Outputs: generated image data/URL.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.AIServices  
**Metadata:**
    
    - **Category:** AIIntegration
    
- **Path:** workflows/sub_workflows/ai_services/ImageGeneration_StabilityAI_SD.subworkflow.json  
**Description:** Sub-workflow dedicated to generating images using Stability AI (Stable Diffusion) API. Handles API authentication, request formatting, and response parsing.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** ImageGeneration_StabilityAI_SD.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/ai_services/ImageGeneration_StabilityAI_SD.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** stabilityAICredentials  
**Type:** Object  
**Attributes:** config  
    - **Name:** stableDiffusionApiEndpoint  
**Type:** String  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** GenerateImage  
**Parameters:**
    
    - prompt
    - parameters
    - apiKey
    
**Return Type:** ImageObject  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - Stability AI Stable Diffusion image generation
    
**Requirement Ids:**
    
    - INT-005
    
**Purpose:** Encapsulates the logic for interacting with the Stability AI API for image generation.  
**Logic Description:** Receives prompt and generation parameters. Retrieves Stability AI API key. Formats request for Stability AI API. Makes HTTP request. Parses response. Handles API-specific errors. Returns generated image data or reference.  
**Documentation:**
    
    - **Summary:** Sub-workflow for Stability AI image generation. Inputs: prompt, parameters. Outputs: generated image data/URL.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.AIServices  
**Metadata:**
    
    - **Category:** AIIntegration
    
- **Path:** workflows/sub_workflows/ai_services/CustomModel_K8s_Inference.subworkflow.json  
**Description:** Sub-workflow for submitting inference jobs to custom AI models hosted on the Kubernetes GPU cluster. Handles K8s job specification, submission, and monitoring.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** CustomModel_K8s_Inference.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/ai_services/CustomModel_K8s_Inference.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - AdapterPattern
    - AsynchronousProcessing
    
**Members:**
    
    - **Name:** kubernetesClusterConfig  
**Type:** Object  
**Attributes:** config  
    - **Name:** modelSpecificJobTemplate  
**Type:** Object  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** SubmitInferenceJob  
**Parameters:**
    
    - modelName
    - modelVersion
    - inputDataPath
    
**Return Type:** JobId  
**Attributes:** workflow_stage  
    - **Name:** PollJobStatus  
**Parameters:**
    
    - jobId
    
**Return Type:** JobStatus  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - Custom AI model inference via Kubernetes
    
**Requirement Ids:**
    
    - INT-005
    - Section 5.3.1 (n8n submits job to K8s)
    
**Purpose:** Orchestrates inference requests to custom AI models deployed on Kubernetes.  
**Logic Description:** Receives model identifier and input data reference. Constructs Kubernetes job manifest using a template. Submits job to K8s API (possibly using n8n Kubernetes node or a custom node). Polls for job completion status. Retrieves output data path upon success. Handles K8s job errors.  
**Documentation:**
    
    - **Summary:** Sub-workflow for running custom AI models on Kubernetes. Inputs: model details, input data. Outputs: inference result data/URL.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.AIServices  
**Metadata:**
    
    - **Category:** AIIntegration
    
- **Path:** workflows/sub_workflows/data_processing/InputData_Preprocessor.subworkflow.json  
**Description:** Sub-workflow for preprocessing various input data types (text prompts, uploaded images, brand elements) before feeding them to AI models.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** InputData_Preprocessor.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/data_processing/InputData_Preprocessor.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** PreprocessTextPrompt  
**Parameters:**
    
    - rawText
    
**Return Type:** ProcessedText  
**Attributes:** workflow_stage  
    - **Name:** PreprocessUploadedImage  
**Parameters:**
    
    - imagePath
    - targetFormat
    
**Return Type:** ProcessedImagePath  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - Text prompt cleaning
    - Image format validation/conversion
    - Brand element data extraction
    
**Requirement Ids:**
    
    - REQ-3-003
    
**Purpose:** Standardizes and prepares input data for AI generation tasks.  
**Logic Description:** Receives raw input data (text, image references, brand kit data). For text, performs cleaning, tokenization (if needed locally). For images, validates format, resizes if necessary for model input. Extracts relevant brand colors, fonts, logos. Outputs processed data structured for AI model consumption.  
**Documentation:**
    
    - **Summary:** Sub-workflow for input data preprocessing. Inputs: raw user inputs. Outputs: AI model-ready inputs.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.DataProcessing  
**Metadata:**
    
    - **Category:** DataProcessing
    
- **Path:** workflows/sub_workflows/security/SecureApiKey_Manager.subworkflow.json  
**Description:** Sub-workflow responsible for securely fetching API keys for external AI services (e.g., OpenAI, Stability AI) from a secrets management system (e.g., HashiCorp Vault).  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** SecureApiKey_Manager.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/security/SecureApiKey_Manager.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - SecretsManagement
    
**Members:**
    
    - **Name:** secretsManagerEndpoint  
**Type:** String  
**Attributes:** config  
    - **Name:** serviceAuthCredentials  
**Type:** Object  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** FetchApiKey  
**Parameters:**
    
    - serviceName
    
**Return Type:** ApiKeyString  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - Secure retrieval of third-party AI service API keys
    
**Requirement Ids:**
    
    - INT-006
    - AISIML-003 (indirectly, as n8n needs keys)
    
**Purpose:** Provides a secure and centralized way for other n8n workflows to obtain API keys.  
**Logic Description:** Receives the name of the external AI service. Authenticates to the secrets management system (e.g., Vault using AppRole or token). Retrieves the specified API key. Returns the API key. Implements error handling for failed retrieval or authentication.  
**Documentation:**
    
    - **Summary:** Sub-workflow for fetching API keys from a secure store. Input: service identifier. Output: API key.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** workflows/sub_workflows/security/ContentSafety_Moderator.subworkflow.json  
**Description:** Sub-workflow for integrating content safety checks on AI-generated content. May call external moderation APIs or internal models.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** ContentSafety_Moderator.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/security/ContentSafety_Moderator.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** moderationServiceEndpoint  
**Type:** String  
**Attributes:** config  
    - **Name:** moderationApiKey  
**Type:** String  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** CheckContentSafety  
**Parameters:**
    
    - contentData
    - contentType
    
**Return Type:** ModerationResult  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - AI-generated content moderation
    - Harmful content filtering
    
**Requirement Ids:**
    
    - REQ-3-015
    - AISIML-005
    - Section 2.5 Legal Constraints
    
**Purpose:** Ensures AI-generated content adheres to platform safety guidelines before being presented to users.  
**Logic Description:** Receives content (image URL, text). Calls a content moderation service (e.g., OpenAI Moderation API, or a custom internal model). Parses the moderation result (e.g., flags for violence, hate speech). If content is unsafe, triggers an error or a specific handling path (e.g., flag for manual review, prevent display).  
**Documentation:**
    
    - **Summary:** Sub-workflow for content safety checks. Inputs: content. Outputs: safety assessment, flags.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.Security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** workflows/sub_workflows/communication/RabbitMQ_Publisher_Odoo.subworkflow.json  
**Description:** Sub-workflow to publish messages to RabbitMQ, specifically for updating Odoo with generation status or other relevant events.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** RabbitMQ_Publisher_Odoo.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/communication/RabbitMQ_Publisher_Odoo.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - MessagePublisher
    
**Members:**
    
    - **Name:** rabbitMQConnectionDetails  
**Type:** Object  
**Attributes:** config  
    - **Name:** odooExchangeName  
**Type:** String  
**Attributes:** config  
    - **Name:** odooRoutingKey  
**Type:** String  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** PublishOdooUpdate  
**Parameters:**
    
    - messagePayload
    
**Return Type:** void  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - Asynchronous status updates to Odoo
    
**Requirement Ids:**
    
    - REQ-3-011
    - REQ-3-012
    - Section 5.3.1
    
**Purpose:** Provides a standardized way for n8n workflows to send updates to the Odoo backend via RabbitMQ.  
**Logic Description:** Receives a message payload. Connects to RabbitMQ using configured credentials. Publishes the message to the specified Odoo exchange with the appropriate routing key. Handles connection or publishing errors.  
**Documentation:**
    
    - **Summary:** Sub-workflow for publishing messages to RabbitMQ for Odoo. Input: message payload. Output: none.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.Communication  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** workflows/sub_workflows/communication/NotificationService_Trigger.subworkflow.json  
**Description:** Sub-workflow to trigger user notifications via the Notification Service, typically by publishing an event to RabbitMQ or calling a Notification Service API.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** NotificationService_Trigger.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/communication/NotificationService_Trigger.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - MessagePublisher
    
**Members:**
    
    - **Name:** notificationServiceQueueConfig  
**Type:** Object  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** SendNotification  
**Parameters:**
    
    - userId
    - notificationType
    - message
    - metadata
    
**Return Type:** void  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - User notification triggering
    
**Requirement Ids:**
    
    - REQ-3-011
    - REQ-3-012
    - Section 5.2.2 Notification Service
    
**Purpose:** Centralizes logic for sending user notifications from n8n workflows.  
**Logic Description:** Receives notification details (user, type, message, metadata). Formats the notification payload. Publishes the payload to a designated RabbitMQ queue consumed by the Notification Service or makes an HTTP request to the Notification Service API. Handles errors in sending the notification trigger.  
**Documentation:**
    
    - **Summary:** Sub-workflow for triggering user notifications. Inputs: notification details. Output: none.
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.Communication  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** workflows/sub_workflows/error_handling/Global_AI_Service_FailureHandler.subworkflow.json  
**Description:** A generic sub-workflow to handle failures from external AI services. Implements retry logic, fallback strategies, and user notification for failures.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 0  
**Name:** Global_AI_Service_FailureHandler.subworkflow  
**Type:** WorkflowDefinition  
**Relative Path:** sub_workflows/error_handling/Global_AI_Service_FailureHandler.subworkflow.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - ErrorHandlingPattern
    - RetryPattern
    - FallbackPattern
    
**Members:**
    
    - **Name:** maxRetries  
**Type:** Integer  
**Attributes:** config  
    - **Name:** fallbackModelProvider  
**Type:** String  
**Attributes:** config  
    
**Methods:**
    
    - **Name:** HandleFailure  
**Parameters:**
    
    - failedService
    - originalRequest
    - errorDetails
    
**Return Type:** RecoveryOutcome  
**Attributes:** workflow_stage  
    
**Implemented Features:**
    
    - AI service error handling
    - Retry mechanisms
    - Fallback to alternative AI providers
    - User-friendly error messaging
    
**Requirement Ids:**
    
    - REQ-3-006
    - REQ-3-007
    - AISIML-005
    - INT-006 (error handling part)
    
**Purpose:** Provides a consistent approach to managing failures when interacting with AI services.  
**Logic Description:** Receives error details from a failed AI service call. Implements retry logic with exponential backoff. If retries fail, attempts to use a configured fallback AI provider/model (if available and applicable for the task). If fallback also fails or is not available, logs the error comprehensively, ensures user credits are not unduly deducted (REQ-3-007), and prepares a user-friendly error message. Triggers appropriate notifications.  
**Documentation:**
    
    - **Summary:** Sub-workflow for handling AI service failures. Inputs: error context. Outputs: outcome (success after retry/fallback, or final failure status).
    
**Namespace:** CreativeFlow.N8N.Workflows.SubWorkflows.ErrorHandling  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** custom_nodes/README.md  
**Description:** Placeholder for documentation regarding any custom n8n nodes developed for CreativeFlow AI. This would include setup, configuration, and usage instructions for these nodes. (Note: Actual file generation is out of scope based on user request, this is a structural placeholder if custom nodes were developed).  
**Template:** Markdown Document  
**Dependency Level:** 0  
**Name:** README  
**Type:** Documentation  
**Relative Path:** custom_nodes/README.md  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Node Documentation
    
**Requirement Ids:**
    
    
**Purpose:** Provides guidance for developers working with or extending custom n8n nodes.  
**Logic Description:** This file would contain: Overview of custom nodes. Installation instructions for custom nodes in an n8n environment. Configuration details for each custom node. Examples of how to use custom nodes within workflows. Development guidelines if others are to contribute to custom nodes.  
**Documentation:**
    
    - **Summary:** Guide for custom n8n nodes specific to the CreativeFlow AI platform.
    
**Namespace:** CreativeFlow.N8N.CustomNodes  
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** custom_nodes/secrets_manager_node/SecretsManager.node.ts  
**Description:** TypeScript source code for a custom n8n node that securely fetches secrets from HashiCorp Vault or a similar secrets management service. (Illustrative example, if built-in HTTP node + credentials are not sufficient or secure enough).  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 0  
**Name:** SecretsManager.node  
**Type:** CustomNodeLogic  
**Relative Path:** custom_nodes/secrets_manager_node/SecretsManager.node.ts  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** description  
**Type:** INodeTypeDescription  
**Attributes:** public|static|readonly  
    - **Name:** nodeProperties  
**Type:** INodeProperties[]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - this: IExecuteFunctions
    
**Return Type:** Promise<INodeExecutionData[][]>  
**Attributes:** public  
    - **Name:** loadOptions  
**Parameters:**
    
    - this: ILoadOptionsFunctions
    - propertyName: string
    
**Return Type:** Promise<INodePropertyOptions[]>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Secure secret retrieval for n8n workflows
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Provides a dedicated n8n node to securely access secrets from a configured secrets manager.  
**Logic Description:** Implements the n8n node interface. Defines node properties for specifying secret path and secrets manager credentials (using n8n's credential system). The execute method connects to the secrets manager, authenticates, fetches the requested secret, and returns it as output. Includes error handling for connection, authentication, and secret retrieval failures.  
**Documentation:**
    
    - **Summary:** Custom n8n node for interacting with a secrets management service. Inputs: secret path, credential name. Outputs: secret value.
    
**Namespace:** CreativeFlow.N8N.CustomNodes.SecretsManager  
**Metadata:**
    
    - **Category:** CustomNode
    
- **Path:** custom_nodes/secrets_manager_node/package.json  
**Description:** package.json file for the SecretsManager custom n8n node, defining its dependencies (e.g., Vault client library) and n8n node metadata.  
**Template:** Node.js package.json  
**Dependency Level:** 0  
**Name:** package  
**Type:** NodePackageConfig  
**Relative Path:** custom_nodes/secrets_manager_node/package.json  
**Repository Id:** REPO-N8N-WORKFLOWS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** metadata  
    - **Name:** version  
**Type:** String  
**Attributes:** metadata  
    - **Name:** description  
**Type:** String  
**Attributes:** metadata  
    - **Name:** n8n  
**Type:** Object  
**Attributes:** metadata  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom node packaging
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Defines metadata and dependencies for the custom SecretsManager n8n node.  
**Logic Description:** Standard package.json structure. Specifies node name, version, description, main entry point (SecretsManager.node.js after compilation), dependencies (e.g., 'node-vault'), and the n8n specific section declaring the node type and its credential types.  
**Documentation:**
    
    - **Summary:** NPM package definition for the SecretsManager custom n8n node.
    
**Namespace:** CreativeFlow.N8N.CustomNodes.SecretsManager  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

