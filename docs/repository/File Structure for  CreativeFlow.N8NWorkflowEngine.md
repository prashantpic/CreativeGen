# Specification

# 1. Files

- **Path:** workflows/CreativeGeneration_Main.workflow.json  
**Description:** Main n8n workflow orchestrating the entire AI creative generation process. Consumes jobs from RabbitMQ, performs data preprocessing, selects AI models, interacts with AI services (via sub-workflows or custom nodes), handles results, stores assets to MinIO, and triggers notifications.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 3  
**Name:** CreativeGeneration_Main.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/CreativeGeneration_Main.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - EventDrivenArchitecture
    - WorkflowPattern
    - Saga (conceptual for steps)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Creative Generation Orchestration
    - RabbitMQ Job Consumption
    - Data Preprocessing
    - AI Model/Provider Selection Trigger
    - Interaction with OpenAI/StabilityAI/Custom K8s Models (via sub-workflows/nodes)
    - Error Handling & Fallback Invocation
    - Content Moderation Invocation
    - Asset Storage to MinIO
    - Notification Service Integration
    - AI Service Usage Tracking/Costing Invocation
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n role in Creative Generation Pipeline)
    - Section 3.2 (Creative Generation Engine based on n8n workflow)
    - INT-005
    - INT-006
    
**Purpose:** Core workflow to manage AI creative requests from start to finish, integrating various services and AI models.  
**Logic Description:** 1. RabbitMQ Trigger: Consume job from 'creative_generation_queue'. 2. Data Validation & Preprocessing node. 3. Call 'AIModelSelectorNode' (custom node) to determine model/provider based on INT-005 rules. 4. Conditional branching (Switch node) based on selected provider: Call 'Sub_OpenAI_Image.workflow', 'Sub_StabilityAI_Image.workflow', or 'Sub_CustomK8s_Model.workflow'. 5. Call 'Sub_ContentModeration.workflow'. 6. If content rejected, handle error and notify. 7. MinIO Node: Store generated asset. 8. HTTP Request Node: Call internal service to log usage (INT-006). 9. RabbitMQ Produce Node: Send 'generation_complete' or 'generation_failed' event to Notification Service and Odoo queues. 10. Implement try-catch blocks around critical steps, calling 'Utility_ErrorHandling.workflow' on failure.  
**Documentation:**
    
    - **Summary:** Orchestrates AI creative generation. Input: Job message from RabbitMQ. Output: Generated asset stored in MinIO, status notifications.
    
**Namespace:** CreativeFlow.N8N.Workflows  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** workflows/Sub_OpenAI_Image.workflow.json  
**Description:** Sub-workflow for interacting with OpenAI's DALL-E (or similar) for image generation. Handles API key retrieval (via SecureVaultApiCallerNode), prompt formatting, API call, and result parsing.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** Sub_OpenAI_Image.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/Sub_OpenAI_Image.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - WorkflowPattern
    - ServiceAdapter
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - OpenAI DALL-E Image Generation
    - Secure API Key Handling for OpenAI
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Encapsulates logic for generating images using OpenAI services.  
**Logic Description:** 1. Input: Prompt, parameters. 2. Call 'SecureVaultApiCallerNode' to get OpenAI API key. 3. OpenAI Node (or HTTP Request Node): Make API call to DALL-E. 4. Parse response, extract image URL/data. 5. Output: Image data/reference, status.  
**Documentation:**
    
    - **Summary:** Sub-workflow for OpenAI image generation. Input: Prompt. Output: Image data.
    
**Namespace:** CreativeFlow.N8N.Workflows.Sub  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** workflows/Sub_StabilityAI_Image.workflow.json  
**Description:** Sub-workflow for interacting with Stability AI's Stable Diffusion models for image generation or style transfer. Handles API key retrieval, API call, and result parsing.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** Sub_StabilityAI_Image.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/Sub_StabilityAI_Image.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - WorkflowPattern
    - ServiceAdapter
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Stability AI Image Generation
    - Secure API Key Handling for Stability AI
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Encapsulates logic for generating images using Stability AI services.  
**Logic Description:** 1. Input: Prompt, parameters. 2. Call 'SecureVaultApiCallerNode' to get Stability AI API key. 3. Stability AI Node (or HTTP Request Node): Make API call to Stable Diffusion. 4. Parse response. 5. Output: Image data/reference, status.  
**Documentation:**
    
    - **Summary:** Sub-workflow for Stability AI image generation. Input: Prompt. Output: Image data.
    
**Namespace:** CreativeFlow.N8N.Workflows.Sub  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** workflows/Sub_CustomK8s_Model.workflow.json  
**Description:** Sub-workflow for interacting with custom AI models hosted on the Kubernetes cluster. Uses the 'K8sJobOrchestratorNode' to submit jobs and retrieve results.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** Sub_CustomK8s_Model.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/Sub_CustomK8s_Model.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - WorkflowPattern
    - ServiceAdapter
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom AI Model Invocation on Kubernetes
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Encapsulates logic for invoking custom AI models deployed on Kubernetes.  
**Logic Description:** 1. Input: Model ID, input data/prompt. 2. Call 'K8sJobOrchestratorNode' to submit inference job. 3. Poll for job completion or use webhook callback. 4. Retrieve results. 5. Output: Generation result, status.  
**Documentation:**
    
    - **Summary:** Sub-workflow for custom K8s model inference. Input: Model ID, data. Output: Inference result.
    
**Namespace:** CreativeFlow.N8N.Workflows.Sub  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** workflows/Sub_ContentModeration.workflow.json  
**Description:** Sub-workflow responsible for content moderation checks. Takes generated content as input and interacts with a content moderation service (internal or third-party).  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** Sub_ContentModeration.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/Sub_ContentModeration.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - WorkflowPattern
    - ServiceAdapter
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Safety Check Integration
    
**Requirement Ids:**
    
    - INT-006 (unsafe content handling)
    
**Purpose:** Performs content safety analysis on generated creatives.  
**Logic Description:** 1. Input: Asset reference or content data. 2. HTTP Request Node (or custom node): Call content moderation service API. 3. Parse moderation result (safe, unsafe, needs review). 4. Output: Moderation status, details.  
**Documentation:**
    
    - **Summary:** Sub-workflow for content moderation. Input: Content. Output: Moderation status.
    
**Namespace:** CreativeFlow.N8N.Workflows.Sub  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** workflows/Utility_ErrorHandling.workflow.json  
**Description:** Reusable sub-workflow for standardized error handling, logging, and potentially triggering notifications for workflow failures.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 1  
**Name:** Utility_ErrorHandling.workflow  
**Type:** WorkflowDefinition  
**Relative Path:** workflows/Utility_ErrorHandling.workflow.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - WorkflowPattern
    - ErrorHandlingPattern
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Standardized Workflow Error Logging
    - Failure Notification Trigger
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Provides common error handling logic for other workflows.  
**Logic Description:** 1. Input: Error object, workflow context. 2. Log Error Node: Log detailed error information. 3. RabbitMQ Produce Node: Send 'workflow_error' event for monitoring/alerting. 4. Output: Standardized error response.  
**Documentation:**
    
    - **Summary:** Utility workflow for error handling. Input: Error details. Output: Error response.
    
**Namespace:** CreativeFlow.N8N.Workflows.Utility  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** nodes/package.json  
**Description:** NPM package file for managing dependencies and defining custom n8n nodes developed within this repository. This allows n8n to discover and load these custom nodes.  
**Template:** Node.js package.json  
**Dependency Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** nodes/package.json  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Node Package Definition
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Defines the collection of custom n8n nodes and their dependencies for CreativeFlow AI.  
**Logic Description:** Specifies 'name', 'version', 'description', 'license', 'author', 'main' (entry point, typically not needed for n8n nodes structured this way), and 'n8n.nodes' array listing paths to node definition files (e.g., 'dist/nodes/CreativeFlowModelSelector/CreativeFlowModelSelector.node.js'). Lists dependencies like '@n8n_io/nodes-core', 'axios', 'kubernetes-client', 'hashicorp-vault-client'. Includes 'scripts' for building TypeScript nodes to JavaScript.  
**Documentation:**
    
    - **Summary:** Package definition for custom CreativeFlow AI n8n nodes.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** nodes/CreativeFlowModelSelector/CreativeFlowModelSelector.node.ts  
**Description:** Custom n8n node for implementing complex AI model/provider selection logic based on business rules (cost, performance, user tier, A/B testing) as per INT-005.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** CreativeFlowModelSelector.node  
**Type:** CustomNodeDefinition  
**Relative Path:** nodes/CreativeFlowModelSelector/CreativeFlowModelSelector.node.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - StrategyPattern (for selection logic)
    
**Members:**
    
    - **Name:** description  
**Type:** INodeTypeDescription  
**Attributes:** public|static|readonly  
    - **Name:** nodeProperties  
**Type:** INodeProperties[]  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - this: IExecuteFunctions
    
**Return Type:** Promise<INodeExecutionData[][]>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Rule-based AI Model Selection
    - User Tier Based Model Routing
    - A/B Testing Model Routing
    
**Requirement Ids:**
    
    - INT-005
    
**Purpose:** Selects an appropriate AI model and provider based on input parameters and configured business rules.  
**Logic Description:** 1. Define node properties: input data (prompt, task type), user context (tier, ID), A/B test configuration path/ID. 2. `execute` method: Fetch user tier, A/B test config if applicable. 3. Evaluate business rules (e.g., from a JSON configuration or internal logic) considering cost, performance, task type, user tier. 4. If A/B test active, route user to appropriate model variant. 5. Output selected model ID, provider name, and any specific parameters for that model.  
**Documentation:**
    
    - **Summary:** Custom n8n node for AI model selection logic.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeLogic
    
- **Path:** nodes/CreativeFlowModelSelector/description.ts  
**Description:** Defines the properties, inputs, outputs, and display details for the CreativeFlowModelSelector custom n8n node.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** description  
**Type:** CustomNodeConfiguration  
**Relative Path:** nodes/CreativeFlowModelSelector/description.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Node UI Definition for AI Model Selector
    
**Requirement Ids:**
    
    - INT-005
    
**Purpose:** Configures the user interface and behavior of the CreativeFlowModelSelector node within the n8n editor.  
**Logic Description:** Exports an `INodeTypeDescription` object. Defines `displayName`, `name` (internal), `group` (e.g., ['CreativeFlow AI']), `version`, `description`, `defaults`, `inputs`, `outputs`, and `properties` for the node editor UI (e.g., fields for user tier input, task type, rule configuration source).  
**Documentation:**
    
    - **Summary:** UI and property definitions for the CreativeFlowModelSelector n8n node.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeConfiguration
    
- **Path:** nodes/SecureVaultApiCaller/SecureVaultApiCaller.node.ts  
**Description:** Custom n8n node for securely fetching API keys/secrets from HashiCorp Vault and making HTTP requests to external AI services. Implements retry/fallback logic as per INT-006.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** SecureVaultApiCaller.node  
**Type:** CustomNodeDefinition  
**Relative Path:** nodes/SecureVaultApiCaller/SecureVaultApiCaller.node.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - CircuitBreaker (conceptual for retries/fallbacks)
    - SecureFacade
    
**Members:**
    
    - **Name:** description  
**Type:** INodeTypeDescription  
**Attributes:** public|static|readonly  
    - **Name:** nodeProperties  
**Type:** INodeProperties[]  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - this: IExecuteFunctions
    
**Return Type:** Promise<INodeExecutionData[][]>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Secure API Key Retrieval from Vault
    - External AI Service Invocation
    - Retry and Fallback Logic for API Calls
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Provides a secure and resilient way to call external AI APIs using secrets from Vault.  
**Logic Description:** 1. Define node properties: Vault path for secret, target API URL, HTTP method, payload, retry configuration, fallback provider/endpoint. 2. `execute` method: Authenticate with Vault using configured method (e.g., AppRole, K8s auth). 3. Fetch API key from Vault. 4. Make HTTP request to target API. 5. Implement retry logic (exponential backoff) for transient errors. 6. If retries fail, attempt fallback if configured. 7. Handle API errors gracefully. 8. Output API response or error.  
**Documentation:**
    
    - **Summary:** Custom n8n node for secure API calls with Vault integration.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeLogic
    
- **Path:** nodes/SecureVaultApiCaller/description.ts  
**Description:** Defines the properties, inputs, outputs, and display details for the SecureVaultApiCaller custom n8n node.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** description  
**Type:** CustomNodeConfiguration  
**Relative Path:** nodes/SecureVaultApiCaller/description.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Node UI Definition for Secure API Caller
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Configures the user interface and behavior of the SecureVaultApiCaller node within the n8n editor.  
**Logic Description:** Exports an `INodeTypeDescription` object. Defines `displayName`, `name`, `group`, `version`, `description`, `defaults`, `inputs`, `outputs`, and `properties` (e.g., fields for Vault path, API URL, method, headers, body, retry attempts, fallback options).  
**Documentation:**
    
    - **Summary:** UI and property definitions for the SecureVaultApiCaller n8n node.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeConfiguration
    
- **Path:** nodes/K8sJobOrchestrator/K8sJobOrchestrator.node.ts  
**Description:** Custom n8n node to interact with the Kubernetes API for managing AI model inference jobs on the custom GPU cluster. Supports job submission, status polling, and result retrieval.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** K8sJobOrchestrator.node  
**Type:** CustomNodeDefinition  
**Relative Path:** nodes/K8sJobOrchestrator/K8sJobOrchestrator.node.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    - OrchestratorPattern
    
**Members:**
    
    - **Name:** description  
**Type:** INodeTypeDescription  
**Attributes:** public|static|readonly  
    - **Name:** nodeProperties  
**Type:** INodeProperties[]  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - this: IExecuteFunctions
    
**Return Type:** Promise<INodeExecutionData[][]>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Kubernetes AI Job Submission
    - K8s Job Status Monitoring
    - K8s Job Result Retrieval
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Manages the lifecycle of AI inference jobs on the Kubernetes cluster.  
**Logic Description:** 1. Define node properties: K8s cluster API endpoint, namespace, job manifest template, input data parameters. 2. `execute` method: Use Kubernetes client library. 3. Authenticate with K8s API. 4. Create and submit Job resource based on template and inputs. 5. Poll Job status or set up watch. 6. Once Job completes, retrieve logs or output artifacts from associated Pods/PVCs. 7. Handle job failures and timeouts. 8. Output job result or error.  
**Documentation:**
    
    - **Summary:** Custom n8n node for orchestrating AI jobs on Kubernetes.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeLogic
    
- **Path:** nodes/K8sJobOrchestrator/description.ts  
**Description:** Defines the properties, inputs, outputs, and display details for the K8sJobOrchestrator custom n8n node.  
**Template:** n8n Custom Node TypeScript  
**Dependency Level:** 1  
**Name:** description  
**Type:** CustomNodeConfiguration  
**Relative Path:** nodes/K8sJobOrchestrator/description.ts  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Node UI Definition for K8s Job Orchestrator
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Configures the user interface and behavior of the K8sJobOrchestrator node within the n8n editor.  
**Logic Description:** Exports an `INodeTypeDescription` object. Defines `displayName`, `name`, `group`, `version`, `description`, `defaults`, `inputs`, `outputs`, and `properties` (e.g., fields for K8s API config, job manifest details, polling interval, timeout).  
**Documentation:**
    
    - **Summary:** UI and property definitions for the K8sJobOrchestrator n8n node.
    
**Namespace:** CreativeFlow.N8N.Nodes  
**Metadata:**
    
    - **Category:** NodeConfiguration
    
- **Path:** config/n8n_instance_settings.md  
**Description:** Conceptual markdown file describing key environment variables or `config.json` settings required for the CreativeFlow AI n8n instance. This is for documentation and setup guidance, not a direct config file deployed by this repo.  
**Template:** Markdown Documentation  
**Dependency Level:** 0  
**Name:** n8n_instance_settings  
**Type:** ConfigurationDocumentation  
**Relative Path:** config/n8n_instance_settings.md  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - n8n Instance Configuration Guidance
    
**Requirement Ids:**
    
    - Section 5.2.2 (AI Processing Orchestration component as n8n)
    
**Purpose:** Documents essential configuration parameters for running the n8n instance tailored for CreativeFlow AI.  
**Logic Description:** Lists and describes environment variables like: `N8N_ENCRYPTION_KEY`, `DB_TYPE` (postgres), `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD`, `DB_POSTGRESDB_DATABASE`, `N8N_CUSTOM_EXTENSIONS` (path to custom nodes), `EXECUTIONS_DATA_PRUNE` (true/max_age), `WEBHOOK_TUNNEL_URL` (if needed for local dev), `N8N_LOG_LEVEL`, `N8N_LOG_OUTPUT`. Also discusses conceptual `config.json` settings for execution modes or resource limits if applicable.  
**Documentation:**
    
    - **Summary:** Guide to configuring the n8n instance for CreativeFlow AI.
    
**Namespace:** CreativeFlow.N8N.Config  
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** config/rabbitmq_connection.md  
**Description:** Conceptual markdown file describing RabbitMQ connection parameters required by n8n workflows for consuming jobs and publishing notifications. For documentation purposes.  
**Template:** Markdown Documentation  
**Dependency Level:** 0  
**Name:** rabbitmq_connection  
**Type:** ConfigurationDocumentation  
**Relative Path:** config/rabbitmq_connection.md  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - RabbitMQ Connection Configuration Guidance
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n role in Creative Generation Pipeline)
    
**Purpose:** Documents how n8n should be configured to connect to RabbitMQ.  
**Logic Description:** Details environment variables or n8n credential setup for RabbitMQ: `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST`. Specifies queue names like `creative_generation_queue` (consumer) and `notification_service_queue`, `odoo_updates_queue` (producer).  
**Documentation:**
    
    - **Summary:** Guide for RabbitMQ connection parameters needed by n8n.
    
**Namespace:** CreativeFlow.N8N.Config  
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** config/minio_integration.md  
**Description:** Conceptual markdown file describing MinIO connection parameters and bucket/path conventions used by n8n workflows for storing and retrieving assets. For documentation purposes.  
**Template:** Markdown Documentation  
**Dependency Level:** 0  
**Name:** minio_integration  
**Type:** ConfigurationDocumentation  
**Relative Path:** config/minio_integration.md  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Integration Configuration Guidance
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n role in Creative Generation Pipeline)
    
**Purpose:** Documents how n8n should be configured to interact with MinIO for asset storage.  
**Logic Description:** Details environment variables or n8n credential setup for MinIO: `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET_ASSETS`. Describes path conventions like `/user_uploads/{userId}/`, `/generated_assets/{generationId}/`. Explains usage of MinIO nodes in n8n.  
**Documentation:**
    
    - **Summary:** Guide for MinIO integration parameters needed by n8n.
    
**Namespace:** CreativeFlow.N8N.Config  
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** config/secrets_management_integration.md  
**Description:** Conceptual markdown file describing the strategy for integrating n8n (especially custom nodes) with HashiCorp Vault for secure API key management as per INT-006. For documentation purposes.  
**Template:** Markdown Documentation  
**Dependency Level:** 0  
**Name:** secrets_management_integration  
**Type:** ConfigurationDocumentation  
**Relative Path:** config/secrets_management_integration.md  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Secrets Management (Vault) Integration Guidance
    
**Requirement Ids:**
    
    - INT-006
    
**Purpose:** Documents the approach for n8n custom nodes to securely access secrets from HashiCorp Vault.  
**Logic Description:** Describes required Vault configuration: `VAULT_ADDR`, authentication method for n8n nodes (e.g., AppRole, K8s Service Account Auth). Specifies example Vault paths for storing API keys (e.g., `secret/creativeflow/ai_providers/openai_api_key`). Outlines how the `SecureVaultApiCallerNode` would use this configuration.  
**Documentation:**
    
    - **Summary:** Guide for HashiCorp Vault integration strategy with n8n.
    
**Namespace:** CreativeFlow.N8N.Config  
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** .n8n/credentials.json.example  
**Description:** An example structure for the n8n `credentials.json` file. This file itself is managed by the n8n runtime and contains encrypted credentials. This example is for developer guidance on what types of credentials might be configured through the n8n UI if not using Vault for everything directly in nodes.  
**Template:** JSON Example  
**Dependency Level:** 0  
**Name:** credentials.json.example  
**Type:** ConfigurationExample  
**Relative Path:** .n8n/credentials.json.example  
**Repository Id:** REPO-N8N-WORKFLOW-ENGINE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Example Credential Structure Documentation
    
**Requirement Ids:**
    
    - INT-005
    - INT-006
    
**Purpose:** Provides a template showing the structure of n8n credentials, aiding developers in understanding how various services (RabbitMQ, HTTP APIs if not using Vault node) are connected.  
**Logic Description:** Contains placeholder JSON structures for different credential types that n8n might manage, such as: `RabbitMqCredentialsApi` (for RabbitMQ connection), `HttpHeaderAuth` or `GenericOAuth2Api` (for generic API calls if keys are manually entered into n8n and not fetched from Vault by a custom node). It should clearly state that actual secrets should not be committed.  
**Documentation:**
    
    - **Summary:** Example of n8n credentials file structure. DO NOT COMMIT ACTUAL SECRETS.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - USE_VAULT_FOR_ALL_AI_KEYS
  - ENABLE_AB_TESTING_MODEL_SELECTOR
  - ENABLE_CONTENT_MODERATION_WORKFLOW
  - ENABLE_DETAILED_USAGE_LOGGING_VIA_API
  
- **Database Configs:**
  
  
- **Environment Variables:**
  
  - N8N_ENCRYPTION_KEY
  - DB_TYPE=postgres
  - DB_POSTGRESDB_HOST
  - DB_POSTGRESDB_PORT
  - DB_POSTGRESDB_USER
  - DB_POSTGRESDB_PASSWORD
  - DB_POSTGRESDB_DATABASE
  - N8N_CUSTOM_EXTENSIONS_PATH
  - RABBITMQ_URI
  - MINIO_ENDPOINT
  - MINIO_ACCESS_KEY
  - MINIO_SECRET_KEY
  - VAULT_ADDR
  - VAULT_TOKEN_OR_APPROLE_ID
  - VAULT_APPROLE_SECRET_ID
  - KUBERNETES_API_SERVER
  - KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH
  - CONTENT_MODERATION_API_ENDPOINT
  - CONTENT_MODERATION_API_KEY_VAULT_PATH
  - USAGE_LOGGING_API_ENDPOINT
  - NOTIFICATION_SERVICE_RABBITMQ_EXCHANGE
  - ODOO_UPDATES_RABBITMQ_EXCHANGE
  
- **Other Settings:**
  
  - **Model_Selection_Rules_Config_Path:** Path to a JSON/YAML file defining business rules for AI model selection, or indicates rules are hardcoded/fetched from a service.
  - **Ab_Testing_Config_Source:** Path to config or service endpoint for A/B testing parameters for AI models.
  - **Default_Openai_Model:** e.g., gpt-4-turbo, dall-e-3
  - **Default_Stabilityai_Model:** e.g., stable-diffusion-xl-1024-v1-0
  


---

