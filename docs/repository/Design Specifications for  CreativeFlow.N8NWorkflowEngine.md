# Software Design Specification: CreativeFlow.N8NWorkflowEngine

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `CreativeFlow.N8NWorkflowEngine` repository. This component is central to the CreativeFlow AI platform, responsible for orchestrating AI creative generation jobs, image processing tasks, and related workflows. It acts as an integration hub, consuming tasks from a message queue, interacting with various AI models (both third-party and custom-hosted), managing content safety checks, storing assets, and notifying other system components of job status.

### 1.2 Scope
The scope of this SDS covers the design and implementation details of:
*   The n8n workflows required for creative generation and utility functions.
*   Custom n8n nodes developed specifically for CreativeFlow AI to handle tasks like secure API key retrieval, AI model selection, and Kubernetes job orchestration.
*   Configuration guidelines for the n8n instance tailored to the CreativeFlow AI environment.
*   Integration points with RabbitMQ, MinIO, AI services (OpenAI, Stability AI, custom K8s models), HashiCorp Vault, and internal notification/logging services.

This document does *not* cover the internal implementation details of the n8n engine itself, nor the design of the external services it integrates with, except as necessary to define interaction patterns.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **n8n**: A free and open fair-code licensed node-based Workflow Automation Tool.
*   **SDS**: Software Design Specification.
*   **AI**: Artificial Intelligence.
*   **API**: Application Programming Interface.
*   **K8s**: Kubernetes.
*   **RabbitMQ**: Message Broker.
*   **MinIO**: S3-Compatible Object Storage.
*   **Vault**: HashiCorp Vault, a secrets management tool.
*   **JSON**: JavaScript Object Notation.
*   **TS**: TypeScript.
*   **Node.js**: JavaScript runtime environment.
*   **CI/CD**: Continuous Integration/Continuous Deployment.
*   **INT-005**: Requirement ID for flexible multi-provider AI model support.
*   **INT-006**: Requirement ID for secure external AI service API key management and usage tracking.

## 2. System Overview
The `CreativeFlow.N8NWorkflowEngine` is a critical backend component within the CreativeFlow AI platform. It operates primarily in an event-driven manner.
1.  **Job Ingestion**: It listens to specific queues on a RabbitMQ message broker for incoming creative generation job requests. These requests are typically published by the `AI Generation Orchestration Service` (after validation and credit checks performed by Odoo).
2.  **Workflow Execution**: Upon receiving a job, n8n executes a predefined workflow. The main workflow (`CreativeGeneration_Main.workflow.json`) orchestrates a series of steps.
3.  **Data Preprocessing & Model Selection**: The workflow preprocesses input data and invokes a custom node (`CreativeFlowModelSelectorNode`) to select the appropriate AI model/provider based on rules defined in INT-005 (e.g., user tier, task type, A/B testing flags).
4.  **AI Interaction**: Based on the selected model, the main workflow calls specialized sub-workflows (`Sub_OpenAI_Image.workflow.json`, `Sub_StabilityAI_Image.workflow.json`, `Sub_CustomK8s_Model.workflow.json`). These sub-workflows, potentially using custom nodes like `SecureVaultApiCallerNode` (for external APIs) or `K8sJobOrchestratorNode` (for custom models), handle the actual interaction with AI services.
5.  **Content Moderation**: Generated content is passed through a content moderation sub-workflow (`Sub_ContentModeration.workflow.json`) to ensure compliance with safety guidelines.
6.  **Result Handling & Storage**: Successful generations are stored in MinIO.
7.  **Usage Tracking & Notifications**: The workflow triggers internal API calls to log AI service usage (INT-006) and publishes status updates (success/failure/moderation status) to RabbitMQ queues for consumption by the Notification Service and Odoo.
8.  **Error Handling**: A utility workflow (`Utility_ErrorHandling.workflow.json`) provides standardized error logging and notification.

This engine relies on secure configuration for API keys (via Vault) and connections to other services. It is designed to be extensible through the addition of new workflows or custom nodes.

## 3. Workflow Design
The n8n instance will host several workflows, each designed as a JSON file.

### 3.1 `CreativeGeneration_Main.workflow.json`
*   **Purpose**: Core workflow to manage AI creative requests from start to finish, integrating various services and AI models.
*   **Trigger**: RabbitMQ Trigger node, listening to `creative_generation_queue`. Expects a JSON payload with `jobId`, `userId`, `projectId`, `inputPrompt`, `styleGuidance`, `inputParameters` (format, resolution, input assets), `userContext` (tier, etc.).
*   **Key Steps / Logic**:
    1.  **RabbitMQ Trigger**: Consumes job from `creative_generation_queue`.
    2.  **Set Workflow Context**: Set node to store initial job parameters for later use.
    3.  **Data Validation & Preprocessing**:
        *   Function Node or custom validation node: Validate incoming job data (e.g., required fields, basic format checks). If invalid, route to error handling.
        *   Data transformation (e.g., structuring prompts, preparing image URLs if input images are provided).
    4.  **AI Model Selection**:
        *   Call custom node: `CreativeFlowModelSelectorNode`.
        *   Input: `taskType` (e.g., 'image_generation_from_text'), `userContext` (from job message), `inputParameters`.
        *   Output: `selectedProvider` (e.g., 'OpenAI', 'StabilityAI', 'CustomK8s'), `selectedModelId`, `providerSpecificParams`.
    5.  **AI Generation (Conditional Branching)**:
        *   Switch Node based on `selectedProvider`.
        *   **Case 'OpenAI'**: Execute Workflow node: `Sub_OpenAI_Image.workflow.json`. Pass relevant prompt and parameters.
        *   **Case 'StabilityAI'**: Execute Workflow node: `Sub_StabilityAI_Image.workflow.json`. Pass relevant prompt and parameters.
        *   **Case 'CustomK8s'**: Execute Workflow node: `Sub_CustomK8s_Model.workflow.json`. Pass `selectedModelId` and input data.
        *   **Default/Error Case**: Route to `Utility_ErrorHandling.workflow.json`.
    6.  **Content Moderation**:
        *   Execute Workflow node: `Sub_ContentModeration.workflow.json`.
        *   Input: Reference to the generated content (e.g., image data or URL from AI generation step).
        *   Output: `moderationStatus` ('approved', 'rejected', 'needs_review'), `moderationDetails`.
    7.  **Handle Moderation Result**:
        *   If Node: Check `moderationStatus`.
        *   If 'rejected' or 'needs_review' (and policy is to block):
            *   Set error message.
            *   Update generation status to 'ContentRejected'.
            *   Proceed to Notification & Logging step for failure.
            *   Potentially log to a separate queue for manual review.
    8.  **Store Asset to MinIO**:
        *   MinIO Node (or custom node for more complex logic if needed).
        *   Input: Generated asset data (from AI generation step, if approved by moderation).
        *   Configuration: MinIO endpoint, credentials (from n8n credential store or fetched by a custom node if dynamic), bucket name (e.g., `generated_assets`), path (e.g., `/{projectId}/{generationId}/output.png`).
        *   Output: `minioFilePath`, `assetUrl`.
    9.  **Log AI Service Usage**:
        *   HTTP Request Node.
        *   URL: Internal `UsageLoggingAPIService` endpoint.
        *   Method: POST.
        *   Body: `jobId`, `userId`, `provider`, `modelUsed`, `costData` (if available/calculated by n8n or AI service), `timestamp`.
        *   Authentication: Appropriate mechanism for internal service calls.
    10. **Prepare Notification & Odoo Update Payload**:
        *   Function Node or Set Node: Construct payload for success or failure.
        *   Success: `jobId`, `status: 'Completed'`, `assetUrl`, `minioFilePath`, `creditsUsed`.
        *   Failure: `jobId`, `status: 'Failed'/'ContentRejected'`, `errorMessage`, `creditsUsed` (should be 0 if system error).
    11. **Publish Results (RabbitMQ)**:
        *   RabbitMQ Produce Node (for Notification Service): Publish success/failure payload to `notification_service_queue_creative_updates`.
        *   RabbitMQ Produce Node (for Odoo): Publish success/failure payload to `odoo_updates_queue_creative_status`.
*   **Error Handling**:
    *   Try-Catch nodes around critical sections (AI model calls, MinIO storage).
    *   On error, execute `Utility_ErrorHandling.workflow.json`. The error workflow will log the error and prepare a standardized failure notification.
*   **Inputs**: Job message from RabbitMQ (as described in Trigger).
*   **Outputs**:
    *   Asset stored in MinIO.
    *   Message to `notification_service_queue_creative_updates` (JSON).
    *   Message to `odoo_updates_queue_creative_status` (JSON).
*   **Integration Points**:
    *   RabbitMQ (consume jobs, produce notifications).
    *   `CreativeFlowModelSelectorNode` (custom node).
    *   `Sub_OpenAI_Image.workflow.json`, `Sub_StabilityAI_Image.workflow.json`, `Sub_CustomK8s_Model.workflow.json`.
    *   `Sub_ContentModeration.workflow.json`.
    *   MinIO.
    *   Internal Usage Logging API.
    *   `Utility_ErrorHandling.workflow.json`.

### 3.2 `Sub_OpenAI_Image.workflow.json`
*   **Purpose**: Encapsulates logic for generating images using OpenAI services (e.g., DALL-E).
*   **Trigger**: Called by `Execute Workflow` node from `CreativeGeneration_Main.workflow.json`.
*   **Key Steps / Logic**:
    1.  **Start Node**: Receives parameters (`prompt`, `size`, `quality`, `n_samples`, etc.).
    2.  **Fetch API Key**:
        *   Call custom node: `SecureVaultApiCallerNode`.
        *   Input: `vaultPath` (e.g., `secret/creativeflow/ai_providers/openai/api_key`).
        *   Output: `apiKey`.
    3.  **Prepare API Request**:
        *   Function Node: Format the prompt and parameters according to OpenAI API specifications.
    4.  **Call OpenAI API**:
        *   HTTP Request Node (configured for OpenAI API).
        *   URL: OpenAI DALL-E API endpoint.
        *   Method: POST.
        *   Headers: `Authorization: Bearer {apiKey}`.
        *   Body: Formatted request payload.
    5.  **Parse Response**:
        *   Function Node: Extract image URL(s) or base64 image data from the API response. Handle potential API errors.
    6.  **Error Handling**: If API call fails or returns an error, set an error flag/message.
    7.  **End Node**: Return structured output.
*   **Inputs**: `prompt`, `parameters` (JSON object with OpenAI specific options like `size`, `quality`, `n`, `style`).
*   **Outputs**: JSON object: `{ "status": "success/error", "data": [{ "url": "...", "b64_json": "..." }, ...], "errorMessage": "..." }`.
*   **Error Handling**: Catches API errors from OpenAI, formats them, and passes them to the output. The `SecureVaultApiCallerNode` itself might have retries.
*   **Integration Points**: `SecureVaultApiCallerNode`, OpenAI API.

### 3.3 `Sub_StabilityAI_Image.workflow.json`
*   **Purpose**: Encapsulates logic for generating images using Stability AI services (e.g., Stable Diffusion).
*   **Trigger**: Called by `Execute Workflow` node from `CreativeGeneration_Main.workflow.json`.
*   **Key Steps / Logic**:
    1.  **Start Node**: Receives parameters (`prompt`, `negative_prompt`, `steps`, `cfg_scale`, `width`, `height`, `seed`, `engine_id` etc.).
    2.  **Fetch API Key**:
        *   Call custom node: `SecureVaultApiCallerNode`.
        *   Input: `vaultPath` (e.g., `secret/creativeflow/ai_providers/stabilityai/api_key`).
        *   Output: `apiKey`.
    3.  **Prepare API Request**:
        *   Function Node: Format prompt and parameters for Stability AI API.
    4.  **Call Stability AI API**:
        *   HTTP Request Node (configured for Stability AI API).
        *   URL: Stability AI API endpoint.
        *   Method: POST.
        *   Headers: `Authorization: Bearer {apiKey}`.
        *   Body: Formatted request payload.
    5.  **Parse Response**:
        *   Function Node: Extract image URL(s) or base64 image data. Handle potential API errors.
    6.  **Error Handling**: Catches API errors.
    7.  **End Node**: Return structured output.
*   **Inputs**: `prompt`, `parameters` (JSON object with Stability AI specific options).
*   **Outputs**: JSON object: `{ "status": "success/error", "data": [{ "base64": "...", "seed": "..." }, ...], "errorMessage": "..." }`.
*   **Error Handling**: Catches API errors from Stability AI.
*   **Integration Points**: `SecureVaultApiCallerNode`, Stability AI API.

### 3.4 `Sub_CustomK8s_Model.workflow.json`
*   **Purpose**: Encapsulates logic for invoking custom AI models deployed on the internal Kubernetes cluster.
*   **Trigger**: Called by `Execute Workflow` node from `CreativeGeneration_Main.workflow.json`.
*   **Key Steps / Logic**:
    1.  **Start Node**: Receives parameters (`modelId`, `version`, `inputData` (e.g., prompt, image reference)).
    2.  **Prepare Job Request**:
        *   Function Node: Construct the job payload for the `K8sJobOrchestratorNode`, including model details and input data. This might involve fetching model-specific endpoint/manifest details from a configuration or another service if not passed directly.
    3.  **Submit K8s Job**:
        *   Call custom node: `K8sJobOrchestratorNode`.
        *   Input: Kubernetes API details (if not globally configured in node), job manifest details, input data.
        *   Output: `jobStatus`, `jobId_k8s`, `resultData` (e.g., path to output in MinIO if model writes directly, or base64 data), `errorMessage`.
    4.  **Error Handling**: Catches errors from K8s job submission or execution.
    5.  **End Node**: Return structured output.
*   **Inputs**: `modelId` (or name/version to look up), `inputData`.
*   **Outputs**: JSON object: `{ "status": "success/error", "data": { ...inference_result... }, "errorMessage": "..." }`.
*   **Error Handling**: Catches K8s job failures or timeouts.
*   **Integration Points**: `K8sJobOrchestratorNode`.

### 3.5 `Sub_ContentModeration.workflow.json`
*   **Purpose**: Performs content safety analysis on generated creatives.
*   **Trigger**: Called by `Execute Workflow` node.
*   **Key Steps / Logic**:
    1.  **Start Node**: Receives `assetReference` (e.g., image URL from MinIO, or base64 data) or `textContent`.
    2.  **Fetch Moderation API Key (if needed)**:
        *   If using a third-party moderation service requiring a key, call `SecureVaultApiCallerNode`.
        *   Input: `vaultPath` for moderation API key.
        *   Output: `moderationApiKey`.
    3.  **Call Content Moderation Service**:
        *   HTTP Request Node.
        *   URL: `CONTENT_MODERATION_API_ENDPOINT` (environment variable).
        *   Method: POST.
        *   Headers: Authentication headers (e.g., `Authorization: Bearer {moderationApiKey}`).
        *   Body: Payload containing asset reference or content.
    4.  **Parse Moderation Result**:
        *   Function Node: Interpret the response from the moderation service. This might involve parsing scores for different categories (hate, self-harm, sexual, violence) and applying thresholds to determine `moderationStatus`.
        *   `moderationStatus` can be 'approved', 'rejected', 'needs_review'.
    5.  **Error Handling**: Handle API errors from the moderation service.
    6.  **End Node**: Return structured moderation result.
*   **Inputs**: `assetReference` (URL or base64 data), `contentType` ('image', 'text').
*   **Outputs**: JSON object: `{ "status": "success/error", "moderationStatus": "approved/rejected/needs_review", "details": { ...scores_or_reasons... }, "errorMessage": "..." }`.
*   **Error Handling**: Catches errors from the content moderation API.
*   **Integration Points**: Content Moderation Service API (internal or third-party), `SecureVaultApiCallerNode` (optional).

### 3.6 `Utility_ErrorHandling.workflow.json`
*   **Purpose**: Provides common error handling logic for other workflows.
*   **Trigger**: Called by `Execute Workflow` node when an error is caught in a parent workflow.
*   **Key Steps / Logic**:
    1.  **Start Node**: Receives `errorObject` (n8n error structure), `workflowContext` (e.g., original `jobId`, `userId`, workflow name where error occurred).
    2.  **Format Error Log**:
        *   Function Node: Extract relevant information from `errorObject` (message, stack, node name) and `workflowContext`. Format into a structured log message (JSON).
    3.  **Log Error (Centrally)**:
        *   HTTP Request Node (or dedicated logging node if available for ELK/Loki): Send the formatted error log to a centralized logging system's API endpoint.
    4.  **Prepare Error Notification (Optional)**:
        *   If Node: Check if the error warrants immediate admin notification (e.g., based on error type or severity if passed in context).
        *   Function Node: Construct a payload for an admin alert.
        *   RabbitMQ Produce Node: Send admin alert to a specific `admin_alerts_queue`.
    5.  **End Node**: Return a standardized error object that parent workflows can use.
*   **Inputs**: `errorObject` (JSON), `workflowContext` (JSON).
*   **Outputs**: Standardized JSON error response: `{ "status": "error", "message": "Processed error: [original_error_message]", "details": { ...formatted_error_log... } }`.
*   **Error Handling**: This is the error handler; further errors here should be minimal and logged by n8n itself.
*   **Integration Points**: Centralized Logging System API, RabbitMQ (for admin alerts).

## 4. Custom Node Design
Custom nodes extend n8n's capabilities. They are written in TypeScript and compiled to JavaScript.

### 4.1 `CreativeFlowModelSelectorNode`
*   **Location**: `nodes/CreativeFlowModelSelector/`
*   **Files**:
    *   `CreativeFlowModelSelector.node.ts`: Core logic.
    *   `description.ts`: UI definition for n8n editor.
*   **Purpose**: Selects an appropriate AI model and provider based on input parameters and configured business rules (INT-005). This node centralizes model selection logic, allowing for A/B testing and dynamic routing.
*   **UI Properties (`description.ts`)**:
    *   `displayName`: "CreativeFlow AI Model Selector"
    *   `name`: `creativeFlowModelSelector`
    *   `group`: `['CreativeFlow AI']`
    *   `version`: 1
    *   `description`: "Selects an AI model and provider based on task type, user context, and business rules."
    *   `defaults`: {}
    *   `inputs`: `['main']`
    *   `outputs`: `['main']` (one success output, one error output if complex)
    *   `properties`:
        *   `taskType`: String (e.g., 'image_generation_from_text', 'text_summarization') - Required.
        *   `userTier`: String (e.g., 'Free', 'Pro', 'Enterprise') - Required.
        *   `userId`: String (for A/B testing user-stickiness) - Optional.
        *   `additionalParameters`: JSON Object (any other parameters that might influence model selection, e.g., `desired_quality`, `cost_sensitivity`) - Optional.
        *   `rulesConfigSource`: String (Path to JSON/YAML rules file, or an API endpoint. Default to internal logic if empty) - Optional.
        *   `abTestConfigId`: String (Identifier for an A/B test configuration) - Optional.
*   **Core Logic (`CreativeFlowModelSelector.node.ts` - `execute` method)**:
    1.  Retrieve input parameters: `taskType`, `userTier`, `userId`, `additionalParameters`, `rulesConfigSource`, `abTestConfigId`.
    2.  **Load Business Rules**:
        *   If `rulesConfigSource` is provided and valid, fetch rules from the specified file or API endpoint.
        *   Otherwise, use a default set of hardcoded or internally configurable rules.
        *   Rules could define:
            *   Provider/model preference per `taskType` and `userTier`.
            *   Cost thresholds.
            *   Performance (latency/quality) considerations.
    3.  **A/B Testing Logic**:
        *   If `abTestConfigId` is provided:
            *   Fetch A/B test configuration (e.g., from a config file or a service). This config would specify models/providers in the test, traffic split percentages.
            *   Use `userId` (or a hash) to deterministically assign the user to a test group (A or B).
            *   Set `selectedProvider` and `selectedModelId` based on the assigned group.
            *   Log A/B test assignment.
    4.  **Rule-Based Selection (if not A/B testing or A/B test falls through)**:
        *   Iterate through rules, matching against `taskType`, `userTier`, and `additionalParameters`.
        *   Consider a priority system for rules.
        *   Select the first matching rule that satisfies constraints (e.g., cost, availability).
    5.  **Default Fallback**: If no rules match or A/B test config is invalid, select a default provider/model for the given `taskType`.
    6.  **Output**: Return an item with `selectedProvider`, `selectedModelId`, and `providerSpecificParams` (any params that need to be passed to the downstream AI interaction sub-workflow).
*   **Error Handling**:
    *   Throw exceptions for invalid input or missing critical parameters.
    *   Handle errors in fetching rules or A/B test configurations gracefully, potentially falling back to defaults.
*   **Dependencies**: None (internal logic, or HTTP client if fetching rules/configs from API).
*   **Feature Toggles**: `ENABLE_AB_TESTING_MODEL_SELECTOR` (can influence if A/B logic is active).

### 4.2 `SecureVaultApiCallerNode`
*   **Location**: `nodes/SecureVaultApiCaller/`
*   **Files**:
    *   `SecureVaultApiCaller.node.ts`: Core logic.
    *   `description.ts`: UI definition.
*   **Purpose**: Securely fetches API keys/secrets from HashiCorp Vault and makes HTTP requests to external AI services. Implements retry/fallback logic as per INT-006.
*   **UI Properties (`description.ts`)**:
    *   `displayName`: "Secure Vault API Caller"
    *   `name`: `secureVaultApiCaller`
    *   `group`: `['CreativeFlow AI']`
    *   `version`: 1
    *   `description`: "Securely calls an external API using credentials from HashiCorp Vault. Supports retries and fallbacks."
    *   `defaults`: `{ "retries": 3, "retryDelayMs": 1000 }`
    *   `inputs`: `['main']`
    *   `outputs`: `['main', 'fallback']` (main for success/final error, fallback for when fallback path is taken)
    *   `properties`:
        *   `vaultSecretPath`: String (Path in Vault to the secret, e.g., `kv/creativeflow/openai`) - Required.
        *   `vaultSecretKey`: String (Key within the Vault secret containing the API token, e.g., `api_key`) - Required.
        *   `apiUrl`: String (URL of the external API) - Required, supports expressions.
        *   `httpMethod`: Select (GET, POST, PUT, DELETE) - Required.
        *   `headers`: JSON Object (Custom headers, API key header will be added automatically) - Optional.
        *   `body`: JSON Object or String (Request body for POST/PUT) - Optional.
        *   `apiKeyHeaderName`: String (e.g., `Authorization`) - Required.
        *   `apiKeyPrefix`: String (e.g., `Bearer `) - Optional.
        *   `retries`: Number (Max number of retries on transient errors) - Default 3.
        *   `retryDelayMs`: Number (Initial delay in ms for retries, uses exponential backoff) - Default 1000.
        *   `enableFallback`: Boolean (Enable fallback mechanism) - Default false.
        *   `fallbackApiUrl`: String (URL for fallback API) - Optional, required if `enableFallback` is true.
        *   `fallbackVaultSecretPath`: String (Vault path for fallback API secret) - Optional.
        *   `fallbackVaultSecretKey`: String (Key for fallback API secret) - Optional.
*   **Core Logic (`SecureVaultApiCaller.node.ts` - `execute` method)**:
    1.  Retrieve input parameters.
    2.  **Initialize Vault Client**: Use environment variables `VAULT_ADDR`, `VAULT_TOKEN_OR_APPROLE_ID`, `VAULT_APPROLE_SECRET_ID` (or other configured auth methods for Vault) to initialize a Vault client (e.g., using `node-vault` library).
    3.  **Primary API Call Attempt**:
        *   `try...catch` block for the entire primary attempt + retries.
        *   Fetch API key from Vault using `vaultSecretPath` and `vaultSecretKey`.
        *   Construct HTTP request (URL, method, headers with API key, body) using `axios` or similar.
        *   Execute request. Implement retry logic for transient HTTP errors (e.g., 5xx, network errors) up to `retries` times with exponential backoff starting at `retryDelayMs`.
        *   If successful, return response data on the main output.
    4.  **Fallback API Call Attempt (if primary fails and `enableFallback` is true)**:
        *   `try...catch` block for fallback.
        *   Fetch fallback API key from Vault (if `fallbackVaultSecretPath` provided).
        *   Construct and execute HTTP request to `fallbackApiUrl`.
        *   If successful, return response data on the 'fallback' output.
    5.  **Error Handling**: If all attempts (primary + retries, and fallback if enabled) fail, throw a comprehensive error detailing the failures.
*   **Error Handling**:
    *   Handles Vault connection/authentication errors.
    *   Handles Vault secret retrieval errors.
    *   Handles HTTP request errors (network, status codes).
    *   Distinguishes between transient errors (for retries) and permanent errors.
*   **Dependencies**: `node-vault` (or equivalent HashiCorp Vault client), `axios`.
*   **Feature Toggles**: `USE_VAULT_FOR_ALL_AI_KEYS` (implies this node is the standard).

### 4.3 `K8sJobOrchestratorNode`
*   **Location**: `nodes/K8sJobOrchestrator/`
*   **Files**:
    *   `K8sJobOrchestrator.node.ts`: Core logic.
    *   `description.ts`: UI definition.
*   **Purpose**: Interacts with the Kubernetes API to submit, monitor, and retrieve results from AI model inference jobs running on the custom GPU cluster.
*   **UI Properties (`description.ts`)**:
    *   `displayName`: "Kubernetes AI Job Orchestrator"
    *   `name`: `k8sJobOrchestrator`
    *   `group`: `['CreativeFlow AI']`
    *   `version`: 1
    *   `description`: "Submits and monitors AI inference jobs on a Kubernetes cluster."
    *   `defaults`: `{ "pollingIntervalSeconds": 10, "timeoutSeconds": 300 }`
    *   `inputs`: `['main']`
    *   `outputs`: `['main']` (success output), `['error']` (error output)
    *   `properties`:
        *   `kubeConfig`: String (Path to kubeconfig file or inline config. Alternatively, use in-cluster config if n8n runs in K8s) - Optional (can default to in-cluster).
        *   `namespace`: String (K8s namespace for the job) - Default 'default'.
        *   `jobManifest`: JSON Object or String (YAML/JSON K8s Job manifest template. Can use n8n expressions for dynamic values) - Required.
        *   `inputData`: JSON Object (Data to be passed to the job, e.g., as env vars or mounted configmap/secret) - Optional.
        *   `waitForCompletion`: Boolean (Wait for job to complete before node finishes) - Default true.
        *   `pollingIntervalSeconds`: Number (If `waitForCompletion`, how often to poll status) - Default 10.
        *   `timeoutSeconds`: Number (Max time to wait for job completion) - Default 300.
        *   `retrieveLogs`: Boolean (Attempt to retrieve logs from the completed/failed pod) - Default true.
*   **Core Logic (`K8sJobOrchestrator.node.ts` - `execute` method)**:
    1.  Retrieve input parameters.
    2.  **Initialize Kubernetes Client**: Use `@kubernetes/client-node` library. Load config from `kubeConfig` or use in-cluster service account.
    3.  **Prepare Job Manifest**:
        *   Parse `jobManifest` (if string, parse YAML/JSON).
        *   Use n8n expressions/templating to inject `inputData` or dynamic values into the manifest (e.g., job name, image tag, environment variables, volume mounts for data).
        *   Ensure unique job name generation.
    4.  **Submit Job**: Call K8s Batch API to create the Job.
    5.  **Monitor Job (if `waitForCompletion` is true)**:
        *   Periodically poll the Job status using K8s API (every `pollingIntervalSeconds`).
        *   Check for `succeeded` or `failed` conditions.
        *   Implement timeout based on `timeoutSeconds`.
    6.  **Retrieve Results/Logs (if job completed and `retrieveLogs` is true)**:
        *   If job `succeeded`, identify the completed Pod(s).
        *   Fetch logs from the Pod(s). This might involve parsing logs for a specific output format or retrieving files from a shared PVC if the model writes output to disk.
        *   If job `failed`, fetch logs to aid debugging.
    7.  **Output**: Return job status, results (logs or structured output), and any error messages.
*   **Error Handling**:
    *   Handles K8s API connection errors.
    *   Handles errors in job submission.
    *   Handles job failures (e.g., pod errors, image pull errors).
    *   Handles timeouts.
*   **Dependencies**: `@kubernetes/client-node`.
*   **Environment Variables**: `KUBERNETES_API_SERVER` (optional, if not using kubeconfig/in-cluster), `KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH` (for in-cluster).

## 5. Configuration

### 5.1 Environment Variables
The n8n instance will rely on the following environment variables for its operation:
*   **`N8N_ENCRYPTION_KEY`**: Secret key used by n8n to encrypt sensitive data in its database. (Critical for security)
*   **`DB_TYPE`**: Set to `postgres`.
*   **`DB_POSTGRESDB_HOST`**: Hostname/IP of the PostgreSQL database server.
*   **`DB_POSTGRESDB_PORT`**: Port for PostgreSQL (default 5432).
*   **`DB_POSTGRESDB_USER`**: Username for PostgreSQL connection.
*   **`DB_POSTGRESDB_PASSWORD`**: Password for PostgreSQL connection.
*   **`DB_POSTGRESDB_DATABASE`**: Database name for n8n.
*   **`N8N_CUSTOM_EXTENSIONS_PATH`**: Filesystem path where custom nodes (like those in `/nodes`) are located, allowing n8n to load them. Example: `/home/node/.n8n/custom`.
*   **`RABBITMQ_URI`**: Connection string for RabbitMQ. E.g., `amqp://user:pass@host:port/vhost`. (Alternatively, set individual `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST` if n8n RabbitMQ node supports it directly or custom nodes handle it).
*   **`MINIO_ENDPOINT`**: Endpoint URL for MinIO.
*   **`MINIO_ACCESS_KEY`**: MinIO access key.
*   **`MINIO_SECRET_KEY`**: MinIO secret key.
*   **`VAULT_ADDR`**: URL of the HashiCorp Vault server.
*   **`VAULT_TOKEN_OR_APPROLE_ID`**: Vault token or AppRole RoleID for n8n nodes to authenticate with Vault.
*   **`VAULT_APPROLE_SECRET_ID`**: Vault AppRole SecretID (if using AppRole auth).
*   **`KUBERNETES_API_SERVER`**: API server endpoint for the Kubernetes cluster (if not using in-cluster config for `K8sJobOrchestratorNode`).
*   **`KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH`**: Path to the service account token if n8n is running within Kubernetes and using in-cluster auth for `K8sJobOrchestratorNode`.
*   **`CONTENT_MODERATION_API_ENDPOINT`**: URL for the content moderation service API.
*   **`CONTENT_MODERATION_API_KEY_VAULT_PATH`**: Vault path to fetch the API key for the content moderation service.
*   **`USAGE_LOGGING_API_ENDPOINT`**: URL for the internal service that logs AI usage and costs.
*   **`NOTIFICATION_SERVICE_RABBITMQ_EXCHANGE`**: Name of the RabbitMQ exchange for publishing notifications to the Notification Service.
*   **`ODOO_UPDATES_RABBITMQ_EXCHANGE`**: Name of the RabbitMQ exchange for publishing updates to Odoo.
*   **`N8N_LOG_LEVEL`**: e.g., `info`, `debug`, `warn`, `error`.
*   **`N8N_LOG_OUTPUT`**: e.g., `console`, `file`.
*   **`EXECUTIONS_DATA_PRUNE`**: `true`
*   **`EXECUTIONS_DATA_MAX_AGE_HOURS`**: e.g., `720` (30 days) - for pruning old execution data from n8n DB.

### 5.2 n8n Instance Settings (`config/n8n_instance_settings.md`)
This document will detail:
*   Recommended n8n execution modes (e.g., `main`, `queue` if using n8n scaling).
*   Guidance on configuring `N8N_ENCRYPTION_KEY` securely.
*   Database connection parameters (already covered by ENV vars).
*   Custom node path configuration (`N8N_CUSTOM_EXTENSIONS_PATH`).
*   Execution data pruning (`EXECUTIONS_DATA_PRUNE`, `EXECUTIONS_DATA_MAX_AGE_HOURS`).
*   Logging (`N8N_LOG_LEVEL`, `N8N_LOG_OUTPUT`).
*   Webhook configuration if n8n needs to expose webhook endpoints for external triggers (though primary trigger is RabbitMQ).
*   Resource allocation recommendations for the n8n instance (CPU, Memory).

### 5.3 External Service Connection Details
*   **RabbitMQ (`config/rabbitmq_connection.md`)**:
    *   Connection URI or individual parameters (host, port, user, pass, vhost).
    *   Queue names for job consumption: `creative_generation_queue`.
    *   Exchange/Queue names for publishing results/notifications:
        *   `notification_service_exchange` (type: `direct` or `topic`) with routing keys like `notifications.creative.completed`, `notifications.creative.failed`.
        *   `odoo_updates_exchange` (type: `direct` or `topic`) with routing keys like `odoo.creative.status.completed`, `odoo.creative.status.failed`.
    *   Connection options (e.g., SSL/TLS, heartbeat).
*   **MinIO (`config/minio_integration.md`)**:
    *   Endpoint URL.
    *   Access Key & Secret Key.
    *   Default Bucket: `creativeflow-assets`.
    *   Path conventions (as per SRS 7.4.1):
        *   User Uploads: `/user_uploads/{userId}/{timestamp}_{filename}`
        *   Generated Assets (Samples): `/generated_assets/{projectId}/{generationId}/samples/{sampleIndex}_{filename}`
        *   Generated Assets (Final): `/generated_assets/{projectId}/{generationId}/final/{filename}`
        *   Brand Kit Assets: `/brand_kits/{brandKitId}/{assetType}/{filename}`
*   **HashiCorp Vault (`config/secrets_management_integration.md`)**:
    *   `VAULT_ADDR`.
    *   Authentication method for n8n nodes (e.g., AppRole with `VAULT_APPROLE_ID`, `VAULT_APPROLE_SECRET_ID`; or Kubernetes Auth if n8n runs in K8s).
    *   Example secret paths:
        *   OpenAI: `secret/data/creativeflow/ai_providers/openai` (key: `api_key`)
        *   StabilityAI: `secret/data/creativeflow/ai_providers/stabilityai` (key: `api_key`)
        *   Content Moderation Service: `secret/data/creativeflow/services/content_moderation` (key: `api_key`)
        *   Other internal service API keys if needed by n8n.
*   **Kubernetes (`nodes/K8sJobOrchestrator/description.ts` and ENV vars)**:
    *   Cluster API endpoint (if not in-cluster).
    *   Authentication (kubeconfig path or service account token path).
    *   Default namespace for jobs.

### 5.4 Feature Toggles
*   **`USE_VAULT_FOR_ALL_AI_KEYS`** (Boolean, Default: `true`): If true, `SecureVaultApiCallerNode` is used for all external AI calls. If false, allows direct use of API keys from n8n credentials for specific nodes (less secure, for dev/testing only).
*   **`ENABLE_AB_TESTING_MODEL_SELECTOR`** (Boolean, Default: `false`): Enables A/B testing logic within `CreativeFlowModelSelectorNode`.
*   **`ENABLE_CONTENT_MODERATION_WORKFLOW`** (Boolean, Default: `true`): Determines if the `Sub_ContentModeration.workflow.json` is called.
*   **`ENABLE_DETAILED_USAGE_LOGGING_VIA_API`** (Boolean, Default: `true`): Controls if the step to log AI service usage via internal API is executed in `CreativeGeneration_Main.workflow.json`.

### 5.5 n8n Credentials (`.n8n/credentials.json.example`)
This file will provide example structures for:
*   `RabbitMqCredentialsApi`: For connecting to RabbitMQ (if not fully configured by ENV vars).
*   `HttpHeaderAuth`: Example if an API key needs to be stored directly in n8n credentials (discouraged if Vault node is used).
*   `VaultAuth`: If n8n has a core Vault credential type, otherwise custom nodes handle Vault auth via ENV vars.
*   `MinioCredentialsApi`: For MinIO connection.
*   `KubernetesCredentialsApi`: For K8s connection (if `K8sJobOrchestratorNode` uses n8n credentials).
Emphasis: **Actual secrets must NEVER be committed.** This file is for structure and type guidance only.

## 6. Dependencies
*   **REPO-RABBITMQ-BROKER-001**: For message queuing (job consumption and result/notification publishing).
*   **REPO-K8S-AI-SERVING-001**: For orchestrating custom AI models. n8n interacts via Kubernetes API.
*   **REPO-MINIO-STORAGE-001**: For storing generated assets and potentially temporary files during workflows.
*   **REPO-NOTIFICATION-SERVICE-001**: n8n publishes events (via RabbitMQ) that this service consumes to notify users.
*   **HashiCorp Vault (External System)**: For secure storage and retrieval of API keys and other secrets.
*   **OpenAI API (External System)**: For DALL-E image generation.
*   **Stability AI API (External System)**: For Stable Diffusion image generation.
*   **Content Moderation Service (Internal or External System)**: For safety checks.
*   **Internal Usage Logging API Service**: For tracking AI service usage and costs.
*   **Odoo Backend (REPO-ODOO-BACKEND-001)**: n8n publishes status updates for Odoo to consume (via RabbitMQ).
*   **PostgreSQL (REPO-DB-POSTGRESQL-001)**: n8n stores its own operational data (workflow definitions, execution logs, credentials) here.

## 7. Security Considerations
*   **Secrets Management**: All external API keys (OpenAI, StabilityAI, Content Moderation) MUST be stored in HashiCorp Vault and retrieved at runtime by custom nodes (e.g., `SecureVaultApiCallerNode`). n8n's own `N8N_ENCRYPTION_KEY` must be strong and managed securely. Credentials for internal services (RabbitMQ, MinIO, K8s if applicable) should also be managed securely, preferably via Vault if custom nodes are making these connections or via n8n's encrypted credential store if using built-in nodes.
*   **Custom Node Security**: Custom nodes accessing sensitive resources (like Vault or K8s) must be carefully reviewed for security vulnerabilities. Input sanitization should be performed if they accept arbitrary user input that forms part of API calls or K8s manifests.
*   **Least Privilege**: n8n's access to Vault, Kubernetes, and other services should follow the principle of least privilege. Vault policies, K8s RBAC, and service-specific permissions must be configured accordingly.
*   **Input Validation**: Workflows, especially the main `CreativeGeneration_Main.workflow.json`, should validate incoming job parameters from RabbitMQ to prevent malformed data from causing issues downstream.
*   **Content Moderation**: The `Sub_ContentModeration.workflow.json` is critical for ensuring generated content adheres to safety policies.
*   **n8n Instance Security**: The n8n instance itself (admin UI, API) must be secured (e.g., strong admin credentials, network access controls, HTTPS).

## 8. Error Handling and Fallback Strategy (INT-006)
*   **Workflow Level**:
    *   The `CreativeGeneration_Main.workflow.json` will use n8n's built-in error handling capabilities (e.g., "Error Trigger" node settings, "Continue on Fail" options, or explicit error branches using "IF" nodes).
    *   Critical steps like AI model calls and MinIO operations will be wrapped in try-catch like structures within the workflow.
    *   On catching an error, the `Utility_ErrorHandling.workflow.json` will be invoked.
*   **`Utility_ErrorHandling.workflow.json`**:
    *   Logs detailed error information (including workflow ID, execution ID, node that failed, error message, stack trace if available) to the centralized logging system.
    *   Publishes a structured error event to a dedicated RabbitMQ queue for system monitoring and alerting (e.g., `system_alerts_queue_n8n_errors`).
    *   Prepares a user-friendly error message and status to be sent back to the originating system (via Odoo/Notification service queues).
*   **Custom Node Level (`SecureVaultApiCallerNode`, `K8sJobOrchestratorNode`)**:
    *   Implement retry mechanisms with exponential backoff for transient errors (e.g., network issues, temporary service unavailability) when calling external APIs or K8s.
    *   The `SecureVaultApiCallerNode` will support a configurable fallback API endpoint. If the primary API call fails after retries, and fallback is enabled, it will attempt the call to the fallback provider/endpoint.
    *   Nodes will throw specific, catchable errors if all attempts fail, allowing parent workflows to handle them.
*   **Fallback for AI Providers (INT-005)**:
    *   The `CreativeFlowModelSelectorNode` can be configured with primary and secondary model/provider preferences.
    *   If the `CreativeGeneration_Main.workflow.json` detects a failure from the primary selected AI provider (after retries in the sub-workflow), it can potentially re-invoke the `CreativeFlowModelSelectorNode` with a flag to exclude the failed provider, or directly attempt a pre-configured secondary provider if the selection logic is simpler. This fallback path needs to be carefully designed to avoid infinite loops and manage costs.
*   **User Notification**: Failed generations due to system errors or AI provider issues (after retries/fallbacks) should not deduct user credits. The error message propagated back should clearly indicate the nature of the failure.

## 9. Data Management (MinIO Interaction)
*   **Storage**: Generated assets (samples and final outputs) are stored in MinIO.
*   **Paths**: Workflows will use dynamic paths based on `projectId`, `generationId`, `userId`, etc., as specified in `config/minio_integration.md` and SRS 7.4.1.
*   **Metadata**: While assets are in MinIO, metadata (including the MinIO path) is stored in PostgreSQL by the `AI Generation Orchestration Service` or Odoo after n8n signals completion.
*   **Access**: n8n uses configured MinIO credentials (from n8n credential store or environment variables) to write assets.

## 10. Deployment (Conceptual)
*   The n8n application (engine, UI, database) will be deployed as per `DEP-001` (Core Platform Infrastructure & Operations), likely using Docker containers orchestrated by Kubernetes or managed via Ansible for a self-hosted setup.
*   This repository (`CreativeFlow.N8NWorkflowEngine`) primarily contributes:
    *   Workflow JSON files (`*.workflow.json`) to be imported into the running n8n instance.
    *   Custom node source code (`nodes/**/*.ts`) which needs to be compiled to JavaScript and made available to the n8n instance via the `N8N_CUSTOM_EXTENSIONS_PATH`. The `nodes/package.json` facilitates this.
*   **CI/CD for Workflows & Nodes**:
    1.  **Lint & Test Custom Nodes**: TypeScript compilation, linting, and unit tests for custom nodes.
    2.  **Package Custom Nodes**: Create a distributable package or Docker layer for custom nodes.
    3.  **Validate Workflows**: JSON schema validation for workflow files. Potentially, use n8n CLI tools for more advanced validation if available.
    4.  **Deploy**:
        *   Custom Nodes: Update the n8n deployment to include the new/updated custom node package/files and restart n8n.
        *   Workflows: Use n8n API or CLI to import/update workflows in the target n8n instance (dev, staging, prod). Workflow definitions should be version-controlled.
*   Configuration (environment variables, connection details) will be managed per environment via Ansible or Kubernetes ConfigMaps/Secrets.

## 11. Scalability and Performance
*   n8n can be scaled by running multiple instances in `queue` mode, consuming jobs from RabbitMQ. This distributes workflow execution load. (Refer to n8n documentation for scaling strategies).
*   Custom nodes should be designed to be performant and non-blocking where possible. Long-running operations within custom nodes (like K8s job polling) should be handled efficiently (e.g., with appropriate timeouts and asynchronous patterns if n8n supports them well within a single node execution).
*   Sub-workflows allow breaking down complex logic, which can improve maintainability but adds some overhead per execution.
*   Database load from n8n (for its own data) should be monitored. Pruning old execution data (`EXECUTIONS_DATA_MAX_AGE_HOURS`) is important.

## 12. Future Considerations
*   **Advanced A/B Testing**: More sophisticated A/B testing logic in `CreativeFlowModelSelectorNode` or a dedicated A/B testing service that n8n calls.
*   **Dynamic Workflow Composition**: Building workflows dynamically based on job parameters, though n8n's primary model is static workflow definitions.
*   **Enhanced n8n Monitoring**: Deeper integration with Prometheus/Grafana for n8n-specific metrics (execution times per node, queue wait times if n8n internal queues are used heavily).
*   **Visual Workflow Versioning and Rollback**: Leveraging n8n's native versioning or external Git-based versioning for workflows with clear rollback procedures.
*   **Serverless Execution for Custom Nodes**: If parts of custom node logic are very resource-intensive or need isolated scaling, consider offloading them to serverless functions called by the n8n node.