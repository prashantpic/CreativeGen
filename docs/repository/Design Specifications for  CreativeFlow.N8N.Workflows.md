# Software Design Specification: CreativeFlow.N8N.Workflows

## 1. Introduction

This document outlines the software design specification for the `CreativeFlow.N8N.Workflows` repository. This repository is responsible for managing and executing all n8n workflow definitions used by the CreativeFlow AI platform. These workflows orchestrate AI creative generation, data processing, error handling, and communication with other microservices and external AI providers. This includes handling asynchronous job processing initiated via RabbitMQ and interacting with Kubernetes for custom AI model inference.

**Repository Purpose:**
To provide a centralized collection of version-controlled n8n workflows and custom nodes that form the core of the AI processing orchestration layer for the CreativeFlow AI platform.

**Scope:**
-   Definition and structure of all n8n workflows (main and sub-workflows).
-   Specification for any custom n8n nodes required for platform-specific integrations or functionalities.
-   Interaction patterns with external services (AI APIs, RabbitMQ, MinIO, Kubernetes, Secrets Management) and internal services (Odoo, Notification Service).

## 2. Overall Workflow Design Philosophy

The n8n workflows within this repository are designed based on the following principles:

*   **Event-Driven Architecture:** Core workflows are triggered by events, primarily messages from RabbitMQ queues, enabling asynchronous processing and decoupling of services.
*   **Orchestration and Sub-Workflows:** A main orchestrator workflow (`CreativeGeneration_Main.workflow.json`) manages the end-to-end creative generation process. It delegates specific tasks to reusable sub-workflows, promoting modularity and maintainability. This aligns with the **Orchestrator Pattern** and **SubWorkflow Pattern**.
*   **Adapter Pattern for External Services:** Sub-workflows dedicated to interacting with specific external AI services (e.g., OpenAI, Stability AI, custom K8s models) act as adapters, encapsulating the specific API details and authentication mechanisms.
*   **Centralized Error Handling:** A global error handling sub-workflow (`Global_AI_Service_FailureHandler.subworkflow.json`) provides common retry logic, fallback strategies, and error reporting for AI service interactions. Individual workflows will also have local error handling for specific steps.
*   **Secure Credential Management:** API keys and other sensitive credentials for external services will be managed securely, either through n8n's built-in credential management system or via a dedicated sub-workflow (`SecureApiKey_Manager.subworkflow.json`) interacting with a secure secrets store like HashiCorp Vault.
*   **Asynchronous Communication:** Interactions with services like Odoo (for status updates, billing) and the Notification Service are primarily asynchronous, using RabbitMQ as the message broker to ensure responsiveness and resilience. This aligns with the **Message Publisher/Consumer Pattern**.
*   **Idempotency:** Workflows handling critical operations should be designed to be idempotent where possible to allow safe retries.
*   **Configuration Driven:** Key parameters, endpoints, and behaviors will be configurable via n8n workflow parameters, environment variables, or global variables to adapt to different environments (dev, staging, prod).

## 3. Workflow Definitions

This section details the design for each n8n workflow. Workflows are defined in JSON format compatible with n8n.

### 3.1 Main Orchestrator Workflows

#### 3.1.1 `CreativeGeneration_Main.workflow.json`
*   **Workflow ID/Name:** `CreativeGeneration_Main`
*   **Purpose:** Orchestrates the entire AI creative generation lifecycle from request intake to final asset delivery and notification. This workflow is central to fulfilling requirements REQ-3-001 to REQ-3-015.
*   **Trigger(s):**
    *   RabbitMQ Trigger Node: Consumes new generation job messages from a dedicated queue (e.g., `creativeflow.generation.jobs`).
*   **Input Parameters/Payload (from RabbitMQ message):**
    json
    {
      "jobId": "uuid", // Unique ID for this generation job
      "userId": "uuid",
      "projectId": "uuid",
      "inputPrompt": "string",
      "styleGuidance": "string", // Optional
      "brandKitId": "uuid", // Optional, to fetch brand elements
      "targetFormats": [ // REQ-3-001, REQ-3-002
        { "platform": "InstagramPost", "dimensions": "1080x1080" },
        { "platform": "InstagramStory", "dimensions": "1080x1920" },
        { "customWidth": 800, "customHeight": 600 }
      ],
      "uploadedImageReferences": ["minio_path_to_image1", "minio_path_to_image2"], // Optional REQ-3-003
      "aiModelPreferences": { // Optional, hints for model selection REQ-3-013, AISIML-002
        "imageGeneration": "OpenAI_Dalle", // or "StabilityAI_SD", "CustomModel_X"
        "textGeneration": "OpenAI_GPT4"
      },
      "outputResolutionPreference": "HD", // e.g., "Standard", "HD", "4K" (REQ-3-009)
      "maxSamples": 4 // REQ-3-008
    }
    
*   **Core Logic/Steps:**
    1.  **Receive Job:** RabbitMQ Trigger node receives the job.
    2.  **Initial Validation & Logging:**
        *   Validate incoming payload structure.
        *   Log job reception.
    3.  **Secure API Key Fetching (for external AI services):**
        *   Call `SecureApiKey_Manager.subworkflow.json` if needed for selected AI models.
    4.  **Input Data Preprocessing:**
        *   Call `InputData_Preprocessor.subworkflow.json` (REQ-3-003).
            *   Fetch brand elements (colors, fonts, logos) if `brandKitId` is provided.
            *   Process text prompts, uploaded images.
    5.  **AI Model Selection Logic (REQ-3-013, AISIML-002):**
        *   Function Node or Switch Node: Based on `aiModelPreferences`, task type, user tier (fetched via Odoo interaction if necessary), or A/B testing configuration, select the appropriate AI model/sub-workflow.
    6.  **Sample Generation Loop (REQ-3-008):**
        *   Loop `maxSamples` times (typically 4).
        *   Within the loop, for each `targetFormat`:
            *   Call the selected AI generation sub-workflow (e.g., `ImageGeneration_OpenAI_Dalle.subworkflow.json`, `ImageGeneration_StabilityAI_SD.subworkflow.json`, or `CustomModel_K8s_Inference.subworkflow.json`) with preprocessed inputs and format-specific parameters (dimensions, style adaptations REQ-3-005).
            *   Handle errors from AI sub-workflow using `Global_AI_Service_FailureHandler.subworkflow.json` (REQ-3-006).
            *   **Content Safety Check (REQ-3-015):** Call `ContentSafety_Moderator.subworkflow.json` for each generated sample. If unsafe, mark and potentially skip or provide a placeholder.
            *   **Store Sample Asset:** HTTP Request Node (or custom node) to upload the low-resolution sample (e.g., 512x512 as per REQ-3-009) to MinIO. Receive MinIO path.
            *   Collect sample metadata (MinIO path, resolution, AI model used).
    7.  **Notify Odoo & User about Samples (REQ-3-011):**
        *   Call `RabbitMQ_Publisher_Odoo.subworkflow.json` to update Odoo with job status (`AwaitingSelection`), sample asset metadata, and `creditsCostSample`.
        *   Call `NotificationService_Trigger.subworkflow.json` to notify the user (via WebSocket/Push) that samples are ready.
    8.  **Wait for Sample Selection (Simulated or via external trigger):**
        *   This step might involve a Wait node, or the workflow could terminate here and a new workflow instance be triggered by Odoo/user action when a sample is selected. *For this design, assume the main workflow handles this or a subsequent part of the flow is triggered with the selected sample ID.*
        *   *Alternative:* If the flow splits, a separate "HighResGeneration.workflow.json" could be triggered by Odoo with the `selectedSampleId`. *For simplicity here, we'll keep it in the main flow assuming it can resume or is triggered with selection info.*
    9.  **Receive Selected Sample ID (if workflow resumes/is re-triggered):**
        *   Input will include `jobId` and `selectedSampleId`.
    10. **High-Resolution Generation (REQ-3-009, REQ-3-012):**
        *   Fetch metadata of the selected sample (MinIO path, original prompt, parameters).
        *   Call the appropriate AI generation sub-workflow again, but this time requesting high resolution (up to 4K) and potentially more refinement steps.
        *   Handle errors using `Global_AI_Service_FailureHandler.subworkflow.json`.
        *   **Content Safety Check:** Call `ContentSafety_Moderator.subworkflow.json` for the final high-resolution asset.
        *   **Store Final Asset:** HTTP Request Node (or custom node) to upload the high-resolution asset to MinIO.
    11. **Notify Odoo & User about Final Asset (REQ-3-012):**
        *   Call `RabbitMQ_Publisher_Odoo.subworkflow.json` to update Odoo with job status (`Completed` or `Failed`), final asset metadata (MinIO path), and `creditsCostFinal`.
        *   Call `NotificationService_Trigger.subworkflow.json` to notify the user that the final asset is ready.
    12. **Final Logging:** Log job completion.
*   **Output(s):**
    *   Messages to RabbitMQ for Odoo updates (status, asset details, credit costs).
    *   Messages to RabbitMQ (or direct API calls) for user notifications via Notification Service.
    *   Assets stored in MinIO.
*   **Key Nodes Used:** RabbitMQ Trigger, HTTP Request (MinIO, AI APIs if not in sub-workflows), Set, IF, Switch, Merge, Function, Execute Workflow (for sub-workflows), Wait (optional), Error Trigger.
*   **Credentials/Connections:** RabbitMQ, MinIO (S3 compatible), AI Service API Keys (managed via `SecureApiKey_Manager` or n8n credentials), Odoo (indirectly via RabbitMQ), Notification Service (indirectly via RabbitMQ/API).
*   **Relevant Requirements Met:** REQ-3-001 to REQ-3-015, INT-005, INT-006, AISIML-005, Section 5.3.1.
*   **Error Handling:**
    *   Each call to a sub-workflow or external service will have an error path.
    *   `Global_AI_Service_FailureHandler.subworkflow.json` will be used for AI service call failures.
    *   Failures in storing assets or notifying services will be logged, and an error status will be sent to Odoo.
    *   Credit deduction logic (REQ-3-007, REQ-6-012): Ensure credits are not deducted for system-side errors or transient AI model issues. This logic would be part of error handling paths or signaled to Odoo for correct billing.

### 3.2 AI Service Sub-Workflows

These sub-workflows act as adapters to specific AI model providers.

#### 3.2.1 `ImageGeneration_OpenAI_Dalle.subworkflow.json`
*   **Workflow ID/Name:** `ImageGeneration_OpenAI_Dalle`
*   **Purpose:** Generates images using OpenAI DALL-E API.
*   **Trigger(s):** Execute Workflow node from a parent workflow (e.g., `CreativeGeneration_Main`).
*   **Input Parameters/Payload:**
    json
    {
      "prompt": "string",
      "size": "string", // e.g., "1024x1024"
      "quality": "string", // e.g., "standard", "hd"
      "n": 1, // Number of images to generate
      "apiKey": "string" // Passed from SecureApiKey_Manager or n8n credentials
    }
    
*   **Core Logic/Steps:**
    1.  **Receive Parameters:** Input from calling workflow.
    2.  **Format API Request:** Function Node to structure the request body for the DALL-E API based on input parameters.
    3.  **HTTP Request Node:**
        *   Method: `POST`
        *   URL: OpenAI DALL-E API endpoint (configurable, e.g., `https://api.openai.com/v1/images/generations`)
        *   Authentication: Bearer Token using `apiKey`.
        *   Body: JSON request payload.
    4.  **Parse Response:** Function Node to extract image URL(s) or Base64 data from the API response.
    5.  **Error Handling:**
        *   Catch HTTP errors (4xx, 5xx).
        *   Parse error messages from OpenAI.
        *   Output a structured error object if failed.
*   **Output(s):**
    *   **Success:**
        json
        {
          "success": true,
          "imageData": [ // Array of generated image details
            { "url": "image_url_from_openai", "b64_json": "optional_base64_data" }
          ]
        }
        
    *   **Failure:**
        json
        {
          "success": false,
          "error": { "code": "openai_error_code", "message": "error_message" }
        }
        
*   **Key Nodes Used:** HTTP Request, Function, Set, IF, Error Trigger.
*   **Credentials/Connections:** OpenAI API (key provided as input or via n8n credential).
*   **Relevant Requirements Met:** INT-005 (OpenAI integration).

#### 3.2.2 `ImageGeneration_StabilityAI_SD.subworkflow.json`
*   **Workflow ID/Name:** `ImageGeneration_StabilityAI_SD`
*   **Purpose:** Generates images using Stability AI (Stable Diffusion) API.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "prompt": "string",
      "negative_prompt": "string", // Optional
      "width": 512,
      "height": 512,
      "cfg_scale": 7,
      "steps": 50,
      // ... other Stability AI parameters
      "apiKey": "string"
    }
    
*   **Core Logic/Steps:** Similar to OpenAI DALL-E sub-workflow:
    1.  Receive parameters.
    2.  Format API Request for Stability AI.
    3.  HTTP Request Node to Stability AI API endpoint.
    4.  Parse Response (image data/URLs).
    5.  Error Handling specific to Stability AI.
*   **Output(s):** Similar structure to OpenAI sub-workflow output (success/failure, imageData).
*   **Key Nodes Used:** HTTP Request, Function, Set, IF, Error Trigger.
*   **Credentials/Connections:** Stability AI API.
*   **Relevant Requirements Met:** INT-005 (Stability AI integration).

#### 3.2.3 `CustomModel_K8s_Inference.subworkflow.json`
*   **Workflow ID/Name:** `CustomModel_K8s_Inference`
*   **Purpose:** Submits inference jobs to custom AI models hosted on the Kubernetes GPU cluster.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "modelName": "string", // Name of the deployed model service in K8s
      "modelVersion": "string", // Version tag
      "inputData": { // Model-specific input structure
        "prompt": "string", // Example
        "image_url": "minio_path_to_input_image" // Example
      },
      "kubernetesJobTemplateName": "string" // Optional: name of a pre-defined K8s job template
    }
    
*   **Core Logic/Steps:**
    1.  **Receive Parameters.**
    2.  **Construct K8s Job Manifest:**
        *   Function Node to dynamically create a Kubernetes Job manifest (YAML/JSON).
        *   This manifest will specify the container image for the model, input data (e.g., mounted as volume or passed as environment variables), resource requests (GPU), and output paths.
        *   Use `kubernetesJobTemplateName` if provided to fetch a base template.
    3.  **Kubernetes Node (or HTTP Request to K8s API):**
        *   Action: `Create Job`.
        *   Provide the generated Job manifest.
        *   Namespace: (configurable).
    4.  **Get Job ID:** Extract Job ID/Name from K8s API response.
    5.  **Poll Job Status (Loop with Wait node):**
        *   Kubernetes Node (Action: `Get Job Status`) or HTTP Request.
        *   Check job status (`Succeeded`, `Failed`, `Running`).
        *   Implement a timeout for polling.
    6.  **Retrieve Output:**
        *   If `Succeeded`, fetch logs or output file paths from the completed K8s job/pod. This might involve getting pod logs or interacting with a predefined output mechanism (e.g., model writes to a shared MinIO path).
    7.  **Error Handling:** Handle K8s job submission errors, job failures, timeouts.
*   **Output(s):**
    *   **Success:**
        json
        {
          "success": true,
          "outputData": { /* model-specific output */ },
          "outputDataPath": "minio_path_to_output_if_applicable"
        }
        
    *   **Failure:**
        json
        {
          "success": false,
          "error": { "code": "k8s_error_code", "message": "error_message", "jobId": "k8s_job_id" }
        }
        
*   **Key Nodes Used:** Function, Kubernetes Node (or HTTP Request), Loop, Wait, IF, Set, Error Trigger.
*   **Credentials/Connections:** Kubernetes API (service account token, kubeconfig).
*   **Relevant Requirements Met:** INT-005 (Custom model hosting), Section 5.3.1 (n8n submits job to K8s).

### 3.3 Data Processing Sub-Workflows

#### 3.3.1 `InputData_Preprocessor.subworkflow.json`
*   **Workflow ID/Name:** `InputData_Preprocessor`
*   **Purpose:** Preprocesses various input data types for AI models.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "rawTextPrompt": "string", // Optional
      "uploadedImageReferences": ["minio_path1", "minio_path2"], // Optional
      "brandKitData": { // Optional, fetched from DB by calling workflow or passed in
        "colors": [{ "name": "Primary", "hex": "#FF0000" }],
        "fonts": [{ "name": "Heading", "family": "Arial" }],
        "logos": [{ "name": "Main Logo", "path": "minio_path_logo" }]
      }
      // ... other potential inputs like target style from REQ-3-003
    }
    
*   **Core Logic/Steps:**
    1.  **Text Preprocessing:**
        *   IF node: Check if `rawTextPrompt` exists.
        *   Function Node: Clean text (remove extra spaces, special characters if needed), potentially integrate brand names/keywords.
    2.  **Image Preprocessing:**
        *   IF node: Check if `uploadedImageReferences` exist.
        *   Loop through image references.
        *   HTTP Request Node (or custom MinIO node): Download image from MinIO temporarily (if needed for local processing by n8n or a specialized microservice not directly accessible by AI model).
        *   Function Node (or call external image processing service/node): Validate format, resize (if a standard input size is needed before passing to AI model selector), potentially extract features.
        *   *Note: Actual image manipulation might be better handled by a dedicated microservice called by n8n if complex.*
    3.  **Brand Element Extraction:**
        *   IF node: Check if `brandKitData` exists.
        *   Function Node: Extract primary colors, font families, logo paths to be used as style hints for AI models.
    4.  **Assemble Processed Data:** Function Node to combine all processed inputs into a structured object.
*   **Output(s):**
    json
    {
      "processedTextPrompt": "string", // Optional
      "processedImagePaths": ["temp_path_or_minio_path_processed1"], // Optional
      "brandStyleHints": { // Optional
        "primaryColor": "#FF0000",
        "headingFont": "Arial",
        "logoPath": "minio_path_logo"
      }
    }
    
*   **Key Nodes Used:** Function, IF, Loop, HTTP Request, Set.
*   **Credentials/Connections:** MinIO (if downloading/uploading processed images within this sub-workflow).
*   **Relevant Requirements Met:** REQ-3-003 (Advanced input processing).

### 3.4 Security Sub-Workflows

#### 3.4.1 `SecureApiKey_Manager.subworkflow.json`
*   **Workflow ID/Name:** `SecureApiKey_Manager`
*   **Purpose:** Securely fetches API keys for external AI services from a secrets management system (e.g., HashiCorp Vault).
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "serviceName": "string" // e.g., "OpenAI", "StabilityAI"
    }
    
*   **Core Logic/Steps:**
    1.  **Receive `serviceName`.**
    2.  **Determine Secret Path:** Function Node or Switch Node to map `serviceName` to the corresponding secret path in Vault (e.g., `kv/creativeflow/ai_services/openai_api_key`).
    3.  **Vault Node (Custom or HTTP Request to Vault API):**
        *   Authenticate to Vault (e.g., using AppRole, Token passed via n8n credentials).
        *   Read secret from the determined path.
    4.  **Extract API Key:** Function Node to parse the Vault response and extract the API key value.
    5.  **Error Handling:** Handle Vault connection errors, authentication failures, secret not found.
*   **Output(s):**
    *   **Success:** `{"apiKey": "actual_api_key_value"}`
    *   **Failure:** `{"success": false, "error": "error_message"}`
*   **Key Nodes Used:** Function, Switch, HTTP Request (if direct Vault API) or Custom Vault Node, Set, IF, Error Trigger.
*   **Credentials/Connections:** HashiCorp Vault (or other secrets manager).
*   **Relevant Requirements Met:** INT-006, AISIML-003 (n8n part).

#### 3.4.2 `ContentSafety_Moderator.subworkflow.json`
*   **Workflow ID/Name:** `ContentSafety_Moderator`
*   **Purpose:** Integrates content safety checks for AI-generated content.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "contentData": "string", // URL to image/video, or text content
      "contentType": "string" // e.g., "image_url", "text"
    }
    
*   **Core Logic/Steps:**
    1.  **Receive `contentData` and `contentType`.**
    2.  **Select Moderation Service:** Switch Node (if multiple moderation services are used).
    3.  **HTTP Request Node (to moderation API, e.g., OpenAI Moderation API):**
        *   Format request with content.
        *   Authenticate (using API key from `SecureApiKey_Manager` or n8n credentials).
    4.  **Parse Moderation Response:** Function Node to interpret flags (e.g., violence, hate, self-harm).
    5.  **Determine Safety Status:** Function Node or IF Node to decide if content is safe, unsafe, or needs review based on flags and thresholds.
*   **Output(s):**
    json
    {
      "isSafe": true/false,
      "flags": ["violence", "hate"], // If unsafe
      "moderationDetails": { /* raw response from moderation service */ }
    }
    
*   **Key Nodes Used:** HTTP Request, Function, IF, Switch, Set.
*   **Credentials/Connections:** Moderation Service API (e.g., OpenAI).
*   **Relevant Requirements Met:** REQ-3-015, AISIML-005, Section 2.5.

### 3.5 Communication Sub-Workflows

#### 3.5.1 `RabbitMQ_Publisher_Odoo.subworkflow.json`
*   **Workflow ID/Name:** `RabbitMQ_Publisher_Odoo`
*   **Purpose:** Publishes messages to RabbitMQ for Odoo backend updates.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "messagePayload": { /* JSON object to send to Odoo */ },
      "routingKey": "string" // e.g., "odoo.generation.status_update"
    }
    
*   **Core Logic/Steps:**
    1.  **Receive `messagePayload` and `routingKey`.**
    2.  **RabbitMQ Producer Node:**
        *   Configure connection details (host, port, user, password from n8n credentials).
        *   Exchange Name: (configurable, e.g., `creativeflow_odoo_exchange`).
        *   Routing Key: Use input `routingKey`.
        *   Message: `messagePayload`.
        *   Ensure message persistence if required.
    3.  **Error Handling:** Handle RabbitMQ connection or publishing errors.
*   **Output(s):** None directly, or a status `{"published": true/false}`.
*   **Key Nodes Used:** RabbitMQ Producer Node, Function (for formatting if needed), Error Trigger.
*   **Credentials/Connections:** RabbitMQ.
*   **Relevant Requirements Met:** REQ-3-011, REQ-3-012, Section 5.3.1.

#### 3.5.2 `NotificationService_Trigger.subworkflow.json`
*   **Workflow ID/Name:** `NotificationService_Trigger`
*   **Purpose:** Triggers user notifications via the Notification Service.
*   **Trigger(s):** Execute Workflow node.
*   **Input Parameters/Payload:**
    json
    {
      "userId": "uuid",
      "notificationType": "string", // e.g., "samples_ready", "final_asset_ready", "generation_failed"
      "message": "string", // User-facing message content
      "metadata": { /* Optional: link to project, asset, etc. */ }
    }
    
*   **Core Logic/Steps:**
    1.  **Receive notification details.**
    2.  **Format Notification Payload:** Function Node to structure the payload for the Notification Service.
    3.  **RabbitMQ Producer Node (or HTTP Request Node to Notification Service API):**
        *   If RabbitMQ: Publish to a specific queue consumed by Notification Service.
        *   If HTTP: Call the Notification Service's API endpoint.
    4.  **Error Handling:** Handle errors in sending the trigger.
*   **Output(s):** None directly, or a status `{"triggered": true/false}`.
*   **Key Nodes Used:** Function, RabbitMQ Producer Node (or HTTP Request Node), Error Trigger.
*   **Credentials/Connections:** RabbitMQ or Notification Service API.
*   **Relevant Requirements Met:** REQ-3-011, REQ-3-012, Section 5.2.2 (Notification Service).

### 3.6 Error Handling Sub-Workflows

#### 3.6.1 `Global_AI_Service_FailureHandler.subworkflow.json`
*   **Workflow ID/Name:** `Global_AI_Service_FailureHandler`
*   **Purpose:** Generic handler for failures from external AI services.
*   **Trigger(s):** Execute Workflow node (typically from an error path of an AI service call).
*   **Input Parameters/Payload:**
    json
    {
      "failedServiceName": "string", // e.g., "OpenAI_Dalle", "StabilityAI_SD"
      "originalRequest": { /* The initial request data sent to the AI service */ },
      "errorDetails": { /* Error object from the failed service or HTTP call */ },
      "jobId": "uuid", // Original job ID for context
      "userId": "uuid",
      "currentRetryCount": 0 // Passed in by calling workflow
    }
    
*   **Core Logic/Steps:**
    1.  **Log Failure:** Log `errorDetails` and context.
    2.  **Retry Logic (IF node & Loop):**
        *   Check `currentRetryCount` against `maxRetries` (configurable, e.g., 3).
        *   If retries remaining:
            *   Wait Node (implement exponential backoff, e.g., `Math.pow(2, currentRetryCount) * 1000` ms).
            *   Increment `currentRetryCount`.
            *   Execute Workflow Node: Re-call the original AI service sub-workflow that failed, passing `originalRequest` and updated `currentRetryCount`.
            *   If retry succeeds, output success.
            *   If retry fails, continue to fallback or final failure.
    3.  **Fallback Logic (IF node, optional):**
        *   If retries exhausted and `fallbackModelProvider` is configured for `failedServiceName`:
            *   Attempt to call the fallback AI service sub-workflow.
            *   If fallback succeeds, output success with fallback indication.
    4.  **Prepare Final Failure Outcome:**
        *   Set output status to `failure`.
        *   Construct user-friendly error message based on `errorDetails`.
        *   **Ensure No Credit Deduction (REQ-3-007):** Prepare a flag or specific error code that indicates to the main orchestrator (and subsequently Odoo) that this failure should not deduct credits.
    5.  **Trigger User Notification (Optional):** Call `NotificationService_Trigger.subworkflow.json` with the user-friendly error.
*   **Output(s):**
    *   **Success (after retry/fallback):** `{"success": true, "result": { /* AI service result */ }, "recoveredVia": "retry/fallback"}`
    *   **Final Failure:** `{"success": false, "error": "user_friendly_error_message", "details": { /* technical error details */ }, "noCreditDeduction": true }`
*   **Key Nodes Used:** Function, IF, Loop, Wait, Execute Workflow, Set, Error Trigger.
*   **Credentials/Connections:** None directly, relies on calling workflows for AI service credentials.
*   **Relevant Requirements Met:** REQ-3-006, REQ-3-007, AISIML-005, INT-006.

## 4. Custom Node Specifications

This section details any custom n8n nodes developed specifically for CreativeFlow AI if built-in nodes are insufficient.

### 4.1 `custom_nodes/README.md`
*   This document will provide an overview of all custom nodes, their purpose, installation procedures within an n8n instance, detailed configuration options for each node, usage examples within workflows, and guidelines for contributing to custom node development.

### 4.2 Secrets Manager Custom Node (`custom_nodes/secrets_manager_node/`)

#### 4.2.1 `SecretsManager.node.ts`
*   **Node Name (Display):** `CreativeFlow: Secrets Manager`
*   **Node Type Name (Internal):** `CreativeFlowSecretsManager`
*   **Purpose:** To provide a dedicated and secure n8n node for fetching secrets (e.g., API keys, database credentials) from HashiCorp Vault or a similar configured secrets management service, abstracting the direct API interaction. This enhances security by centralizing secret access logic and leveraging n8n's credential system for the Vault connection itself.
*   **Input Properties (Node UI):**
    *   `credentialVault`: Credential Type. Selects n8n credentials configured for HashiCorp Vault (e.g., containing AppRole ID, Secret ID, or Vault token and Vault address).
    *   `secretPath`: String. The full path to the secret in Vault (e.g., `kv/data/creativeflow/ai_services/openai`).
    *   `secretKey`: String. (Optional) The specific key within the secret data to retrieve. If empty, returns the entire secret data object.
*   **Output Properties (Node Output):**
    *   `secretValue`: String or Object. The retrieved secret value or the entire secret data object.
    *   `error`: String. (Optional) Error message if retrieval fails.
*   **Core Logic (TypeScript):**
    1.  Retrieve Vault connection details and authentication method from selected `credentialVault`.
    2.  Instantiate Vault client library (e.g., `node-vault`).
    3.  Authenticate to Vault using the provided credentials.
    4.  Read the secret from the specified `secretPath`.
    5.  If `secretKey` is provided, extract that specific key from the secret data. Otherwise, return the entire data object.
    6.  Output the `secretValue`.
*   **Error Handling:**
    *   Catch and output errors related to Vault connection, authentication, invalid path, secret not found, or permission issues.
    *   Provide clear error messages in the `error` output property.
*   **Dependencies (in `package.json`):** `n8n-workflow`, `n8n-core`, `node-vault` (or equivalent Vault client).
*   **Relevant Requirements Met:** INT-006 (Secure API Key Management, alternative to sub-workflow).

#### 4.2.2 `package.json` (for `SecretsManager.node.ts`)
*   **Contents:**
    json
    {
      "name": "@creativeflow/n8n-nodes-secrets-manager",
      "version": "0.1.0",
      "description": "Custom n8n node to fetch secrets from HashiCorp Vault for CreativeFlow AI.",
      "main": "dist/SecretsManager.node.js", // Compiled JS output
      "n8n": {
        "nodes": [
          {
            "file": "dist/SecretsManager.node.js",
            "type": "CreativeFlowSecretsManager" // Matches internal node type name
          }
        ],
        "credentials": [
          // Define a credential type for Vault if not using generic HTTP Auth
          // Example: { "name": "vaultApi", "url": "/credentials/vault" }
        ]
      },
      "scripts": {
        "build": "tsc",
        "dev": "tsc --watch"
      },
      "dependencies": {
        "n8n-workflow": "*", // Use version from n8n instance
        "n8n-core": "*",
        "node-vault": "^0.10.0" // Example
      },
      "devDependencies": {
        "typescript": "~5.4.0", // Or match n8n's recommended version
        "@types/node": "^20.0.0"
      }
    }
    

## 5. Configuration Management

*   **Workflow Parameters:** Sensitive data like API endpoints, specific queue names, exchange names, and behavior flags (e.g., `maxRetries`) should be exposed as workflow parameters or utilize n8n expressions to fetch from environment variables or global n8n variables.
*   **Credentials:**
    *   **n8n Credential Manager:** Standard n8n credential management should be used for RabbitMQ connections, HTTP Basic/OAuth2/API Key authentications where built-in nodes support them.
    *   **Secrets Manager Integration:** For API keys to external AI services or sensitive configurations, the `SecureApiKey_Manager.subworkflow.json` or the custom `SecretsManager.node.ts` will be used. This node/workflow itself will use n8n credentials to connect to the central secrets management system (e.g., HashiCorp Vault).
*   **Environment Variables:** n8n instance configuration (e.g., `N8N_ENCRYPTION_KEY`, database connections for n8n itself) will be managed via environment variables as per standard n8n deployment practices. Workflow-specific environment variables can be accessed using `{{ $env.VARIABLE_NAME }}`.

## 6. Error Handling Strategy (Overall Platform Level within n8n)

*   **Local Error Handling:** Each significant step in a workflow (e.g., HTTP request, database operation, RabbitMQ publish) will have an error output connected to an error handling path.
*   **Sub-Workflow Error Propagation:** Sub-workflows will catch their internal errors and output a standardized error object (e.g., `{"success": false, "error": "message"}`). Parent workflows will check this output.
*   **Global AI Service Failure Handler:** As described in section 3.6.1, this sub-workflow centralizes retry and fallback logic for AI service calls.
*   **Dead Letter Queues (DLQ) for RabbitMQ:** For critical RabbitMQ consumers (like the main job trigger), configure DLQs to capture messages that cannot be processed after several retries by n8n, allowing for manual inspection and reprocessing.
*   **Logging:** n8n execution logs provide detailed step-by-step logging. Critical errors should be explicitly logged with more context using Function nodes if necessary. Errors will also be propagated to Odoo for visibility and potential customer support actions.
*   **User Notifications:** For user-initiated tasks that fail terminally, the user must be notified (via `NotificationService_Trigger.subworkflow.json`) with a clear, user-friendly message, and potentially options to retry or contact support, as per REQ-3-006.
*   **Credit Non-Deduction:** Workflows must implement logic or signal (e.g., via specific error codes/flags in messages to Odoo) to ensure user credits are not deducted for failures attributable to system errors or AI provider issues (REQ-3-007).

## 7. Deployment

*   **Workflow Deployment:** n8n workflows are JSON files. Deployment to an n8n instance involves importing these JSON definitions. This process will be automated as part of the CI/CD pipeline.
    *   Workflows will be stored in the Git repository.
    *   The CI/CD pipeline will use n8n's API (if available and suitable) or `n8n-cli` tool to import/update workflows in the target n8n instances (dev, staging, prod).
*   **Custom Node Deployment:**
    *   Custom nodes (TypeScript/Python) will be packaged according to n8n documentation.
    *   For TypeScript nodes, the build process (e.g., `npm run build`) will compile TS to JS.
    *   The compiled nodes and their `package.json` will be deployed to the n8n instance's custom nodes directory. This can be part of the n8n Docker image build process or mounted into the n8n container.
    *   The n8n instance will need to be restarted or reloaded to recognize new/updated custom nodes.
*   **Versioning:**
    *   Workflow JSON files will be version-controlled in Git.
    *   Custom node source code will be version-controlled in Git.
    *   Consider using tags or release branches for managing different versions of workflows and nodes deployed to production.

## 8. Data Flow & Interfaces

*   **Incoming Data (from RabbitMQ - `CreativeGeneration_Main`):**
    *   **Queue:** e.g., `creativeflow.generation.jobs`
    *   **Message Format:** JSON (as defined in section 3.1.1 Input)
    *   **Source:** Odoo Backend (via AI Generation Orchestration Service adapter if one exists, or directly from Odoo custom module)
*   **Outgoing Data (to RabbitMQ):**
    *   **To Odoo (`RabbitMQ_Publisher_Odoo.subworkflow.json`):**
        *   **Exchange:** e.g., `creativeflow_odoo_exchange`
        *   **Routing Keys:** e.g., `odoo.generation.status_update`, `odoo.billing.credit_deduction_request`
        *   **Message Format:** JSON, containing job ID, user ID, status, asset metadata, credit costs, error details.
    *   **To Notification Service (`NotificationService_Trigger.subworkflow.json`):**
        *   **Queue/Exchange:** e.g., `creativeflow.notifications.user`
        *   **Message Format:** JSON, containing user ID, notification type, message, metadata.
*   **External HTTP API Calls (from AI Service Sub-Workflows & Content Safety):**
    *   **OpenAI API:** `POST https://api.openai.com/v1/images/generations`, `POST https://api.openai.com/v1/moderations`
    *   **Stability AI API:** (Specific endpoint as per their documentation)
    *   **Custom Model K8s API:** (Internal Kubernetes service endpoint for deployed models)
    *   **Secrets Manager API (Vault):** (Vault HTTP API endpoint)
    *   Authentication: Bearer Tokens (API Keys)
    *   Payloads: JSON
*   **MinIO Interaction (S3 API):**
    *   Operations: `PUT Object` (for storing samples and final assets), `GET Object` (if preprocessing needs to download).
    *   Authentication: S3 Access Key/Secret Key (managed via n8n credentials).

## 9. Security Considerations

*   **API Key Management (INT-006, AISIML-003):**
    *   Keys for external AI services (OpenAI, StabilityAI, moderation services) must NOT be hardcoded in workflows.
    *   They will be fetched at runtime using the `SecureApiKey_Manager.subworkflow.json` (which interacts with HashiCorp Vault) or via n8n's encrypted credential store.
    *   The custom `SecretsManager.node.ts` provides an alternative dedicated node for this.
*   **Content Safety (REQ-3-015, Section 2.5):**
    *   The `ContentSafety_Moderator.subworkflow.json` will be invoked for AI-generated content.
    *   Workflows must handle outputs from the moderation sub-workflow, preventing unsafe content from being stored as final assets or shown to users without appropriate measures (e.g., flagging, admin review path).
*   **Access Control to n8n:**
    *   The n8n instance itself must be secured (authentication, network access).
    *   Access to edit workflows should be restricted to authorized DevOps/engineering personnel.
*   **RabbitMQ Security:**
    *   Connections to RabbitMQ from n8n will use authenticated credentials.
    *   TLS should be enabled for RabbitMQ communication.
*   **Kubernetes API Security:**
    *   n8n interactions with the Kubernetes API (for custom model jobs) must use a service account with least-privilege RBAC permissions, scoped only to what's necessary for job submission and status checking.
*   **MinIO Security:**
    *   Connections to MinIO will use S3 credentials managed securely by n8n.
    *   Bucket policies on MinIO should restrict access.
*   **Error Handling and Information Disclosure:**
    *   Error messages propagated to users or external systems (like Odoo) should not reveal sensitive internal details or stack traces. User-friendly, generic messages should be provided by the main orchestrator, while detailed technical errors are logged internally.

## 10. Design Patterns Used

*   **Orchestrator Pattern:** `CreativeGeneration_Main.workflow.json` acts as the central orchestrator.
*   **SubWorkflow Pattern (Execute Workflow Node):** Used extensively for modularity and reusability (e.g., AI service calls, data processing, communication).
*   **Adapter Pattern:** AI service sub-workflows (`ImageGeneration_OpenAI_Dalle`, `ImageGeneration_StabilityAI_SD`, `CustomModel_K8s_Inference`) adapt the specific APIs of different AI providers to a common internal expectation (e.g., receive prompt, return image data).
*   **Secrets Management:** `SecureApiKey_Manager.subworkflow.json` or the custom `SecretsManager.node.ts` centralizes secure credential retrieval.
*   **Message Publisher/Consumer:** Workflows publish messages to RabbitMQ (for Odoo, Notification Service) and the main workflow consumes job messages from RabbitMQ.
*   **Error Handling Pattern:** `Global_AI_Service_FailureHandler.subworkflow.json` implements common error handling strategies like retries and fallbacks.
*   **Retry Pattern:** Implemented within the `Global_AI_Service_FailureHandler.subworkflow.json`.
*   **Fallback Pattern:** Implemented within the `Global_AI_Service_FailureHandler.subworkflow.json` to switch to alternative AI providers if configured.
*   **Asynchronous Processing:** The entire creative generation process is fundamentally asynchronous, initiated by a message and processed in the background by n8n.