# Software Design Specification (SDS) for CreativeFlow.Service.AIOrchestration.N8n

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.Service.AIOrchestration.N8n` repository. This repository is responsible for orchestrating the AI-driven creative generation pipelines. It defines the n8n workflows, custom nodes, and configurations necessary to receive generation requests, interact with various AI models (both internal and external), and manage the flow of data throughout the generation process.

### 1.2. Scope
The scope of this document is limited to the components within this repository. This includes:
- The structure and logic of all n8n workflows and sub-workflows.
- The design and implementation of custom n8n nodes required for specific integrations (e.g., Kubernetes).
- Configuration files for the development environment and custom node definitions.
- The definition of data contracts for inputs received from and outputs sent to the message queue (RabbitMQ).

This system acts as a central orchestration engine, triggered by events and interacting with other services as defined in the system architecture.

## 2. System Overview & Design

The `AIOrchestration.N8n` service is a core component of the event-driven architecture. It operates as a consumer of jobs from a RabbitMQ message queue and orchestrates complex, potentially long-running processes without blocking the user-facing backend services.

**Key Design Principles:**
- **Asynchronous & Event-Driven:** All workflows are initiated by asynchronous messages, ensuring the platform remains responsive. (REQ-SSPE-009)
- **Modularity & Reusability:** Logic is broken down into main workflows and reusable sub-workflows (e.g., for storage, notifications, model invocation). This improves maintainability and testability.
- **Extensibility:** The design supports adding new AI models and providers with minimal changes by using a standardized sub-workflow and adapter pattern approach. (INT-005)
- **Error Handling:** A centralized error handling workflow ensures consistent failure management and communication back to the core system. (REQ-007.1)
- **Configuration-Driven:** AI model selection and other parameters are driven by the data passed in the trigger message, allowing for dynamic behavior based on user tier, A/B testing flags, etc.

## 3. Configuration Files Specification

### 3.1. `package.json`
This file manages the Node.js project for custom node development.
- **`name`**: `creativeflow-n8n-nodes`
- **`version`**: `1.0.0`
- **`description`**: "Custom nodes and workflow definitions for CreativeFlow AI's n8n orchestration engine."
- **`license`**: "UNLICENSED" (or appropriate license)
- **`main`**: "dist/nodes/index.js"
- **`n8n`**:
  json
  "n8n": {
    "nodes": [
      "dist/nodes/KubernetesJobSubmitter/KubernetesJobSubmitter.node.js"
    ]
  }
  
- **`dependencies`**:
  - `@kubernetes/client-node`: "^0.20.0" (or latest stable) - For Kubernetes API interaction.
- **`devDependencies`**:
  - `@n8n/core`: "^1.0.0"
  - `@n8n/workflow`: "^1.0.0"
  - `@types/node`: "^20.0.0"
  - `typescript`: "^5.0.0"
  - `eslint`: "^8.0.0"
  - `prettier`: "^3.0.0"
  - `@typescript-eslint/parser`: "^7.0.0"
  - `ts-node`: "^10.9.2"
- **`scripts`**:
  - `build`: "tsc" - Compiles TypeScript custom nodes to JavaScript.
  - `dev`: "n8n start --tunnel" - Starts n8n locally, loading custom nodes for development.
  - `lint`: "eslint nodes/**/*.ts" - Runs linter on custom node source code.
  - `format`: "prettier --write nodes/**/*.ts" - Formats code.

### 3.2. `tsconfig.json`
Configures the TypeScript compiler for custom nodes.
json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node"
  },
  "include": ["src/nodes/**/*.ts"],
  "exclude": ["node_modules"]
}


### 3.3. `.env.example`
Provides a template for all required environment variables.
env
# n8n Core Settings
N8N_HOST="localhost"
N8N_PORT=5678
NODE_ENV="development"

# Credentials for n8n to connect to its own database
N8N_DB_TYPE=postgresdb
N8N_DB_POSTGRESDB_HOST=localhost
N8N_DB_POSTGRESDB_PORT=5432
N8N_DB_POSTGRESDB_DATABASE=n8n
N8N_DB_POSTGRESDB_USER=n8n_user
N8N_DB_POSTGRESDB_PASSWORD=supersecretpassword

# RabbitMQ Connection
RABBITMQ_URI="amqp://guest:guest@localhost:5672/"

# MinIO Connection
MINIO_ENDPOINT="localhost"
MINIO_PORT=9000
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
MINIO_USE_SSL=false
MINIO_BUCKET_GENERATED_ASSETS="generated-assets"

# External AI Service APIs
OPENAI_API_KEY=""
STABILITYAI_API_KEY=""

# Internal Kubernetes Cluster API
# These will be configured via K8s service account for in-cluster access
# For local dev, they might point to a kubeconfig file or proxy
KUBERNETES_API_URL="https://kubernetes.default.svc"
KUBERNETES_NAMESPACE="ai-jobs"

# Internal Service URLs
NOTIFICATION_SERVICE_URL="http://notification-service:8080/notify"
ODOO_ADAPTER_URL="http://odoo-adapter:8080/api/v1"


### 3.4. `.docker/docker-compose.yml`
Defines the local development stack.
yaml
version: '3.8'
services:
  n8n:
    image: n8n-custom:latest
    build:
      context: ..
      dockerfile: .docker/Dockerfile
    ports:
      - "5678:5678"
    environment:
      - NODE_ENV=development
    env_file:
      - ../.env
    volumes:
      - ../src/workflows:/home/node/.n8n/workflows
      - ../dist:/home/node/packages/nodes/dist # Mount compiled custom nodes
    depends_on:
      - postgres
      - rabbitmq
      - minio

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=n8n_user
      - POSTGRES_PASSWORD=supersecretpassword
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672" # AMQP
      - "15672:15672" # Management UI

  minio:
    image: minio/minio
    ports:
      - "9000:9000" # S3 API
      - "9001:9001" # Console
    volumes:
      - minio_data:/data
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"

volumes:
  postgres_data:
  minio_data:


## 4. Custom Node Specification

### 4.1. `src/nodes/KubernetesJobSubmitter/KubernetesJobSubmitter.node.ts`
This node is the bridge between n8n and the internal GPU cluster.
- **Purpose**: To create a Kubernetes `Job` from workflow parameters, monitor its execution, and return the result. (INT-007)
- **Node Properties (UI Fields)**:
  - **`Job Name Prefix`**: (String, Required) A prefix for the job name (e.g., `creative-gen-`). n8n will append a unique ID.
  - **`Namespace`**: (String, Default: `ai-jobs`) The K8s namespace to create the job in.
  - **`Container Image`**: (String, Required) The Docker image URL for the AI model container.
  - **`Command`**: (String Array, Optional) The command to run in the container.
  - **`Arguments`**: (String Array, Optional) Arguments for the command.
  - **`Input Data`**: (JSON, Required) JSON data to be passed to the job, likely as an environment variable or a mounted ConfigMap.
  - **`GPU Request`**: (Number, Default: 1) Number of GPUs to request (e.g., `nvidia.com/gpu: 1`).
  - **`CPU Request`**: (String, Default: '1') CPU resource request (e.g., '500m', '1').
  - **`Memory Request`**: (String, Default: '2Gi') Memory resource request (e.g., '1Gi', '4Gi').
  - **`Wait for Completion`**: (Boolean, Default: true) If true, the node waits for the job to succeed or fail. If false, it returns immediately after submission.
  - **`Polling Interval (s)`**: (Number, Default: 10) How often to check job status if waiting.
  - **`Timeout (s)`**: (Number, Default: 600) Maximum time to wait for job completion.
- **`execute` Method Logic**:
  1. **Initialization**: Load K8s client configuration (in-cluster service account or from credentials).
  2. **Parameter Retrieval**: Get all node properties using `this.getNodeParameter()`.
  3. **Job Manifest Construction**:
     - Create a unique job name: `jobNamePrefix` + `this.getExecutionId()`.
     - Construct a valid K8s `V1Job` manifest object.
     - The container spec will include the `image`, `command`, `args`, and `resources.requests/limits` (CPU, memory, GPU).
     - Input data will be serialized to a string and passed as an environment variable (e.g., `INPUT_JSON`).
  4. **Job Creation**: Use the K8s `BatchV1Api` client to `createNamespacedJob`.
  5. **Status Monitoring (if `Wait for Completion` is true)**:
     - Implement a polling loop (`setInterval`).
     - In each interval, call `readNamespacedJobStatus` to check `job.status.succeeded` or `job.status.failed`.
     - If succeeded, retrieve logs from the associated pod using the `CoreV1Api`. Parse the logs for the output (e.g., a MinIO path). Resolve the promise with the output data.
     - If failed, retrieve logs, construct a meaningful error message, and reject the promise.
     - If timeout is reached, reject the promise with a timeout error.
  6. **Return Data**: Return the execution data containing the job output or status.

## 5. Workflow Specifications

### 5.1. `01-process-sample-generation-request.workflow.json`
Orchestrates the initial low-resolution sample generation. (REQ-008)
- **Trigger**: `RabbitMQ Trigger` node listening to the `generation.sample.request` queue.
- **Input Data Contract (from RabbitMQ message)**:
  json
  {
    "generationRequestId": "uuid",
    "userId": "uuid",
    "projectId": "uuid",
    "inputPrompt": "A futuristic cityscape...",
    "styleGuidance": "cyberpunk, neon lights",
    "inputParameters": {
      "format": "InstagramPost",
      "dimensions": "1080x1080",
      "brandKitId": "uuid_or_null",
      "modelSelectionStrategy": "quality" // or 'cost', 'fastest', or a specific model ID
    }
  }
  
- **Workflow Logic**:
  1. **`Set Initial Data`**: A `Set` node to store the initial trigger data for later reference.
  2. **`Prepare Generation Loop`**: A `Split in Batches` node configured to loop 4 times (for 4 samples).
  3. **`Select AI Model (Sub-workflow)`**: `Execute Workflow` node calls a sub-workflow (`select-ai-model`) which takes `modelSelectionStrategy` as input and returns the chosen `modelId` and `provider` (e.g., OpenAI, StabilityAI, Internal).
  4. **`Route to Provider`**: A `Switch` node routes execution based on the `provider` returned from the previous step.
     - Case 'OpenAI': Execute an OpenAI-specific sub-workflow.
     - Case 'StabilityAI': Execute a StabilityAI-specific sub-workflow.
     - Case 'Internal': Execute `invoke-internal-k8s-model.subworkflow.json`.
  5. **`Store Asset in MinIO (Sub-workflow)`**: The output from the AI model (an image file/buffer) is passed to a `store-asset-in-minio` sub-workflow. This sub-workflow uploads the file to MinIO under the correct path (`userId/projectId/generationRequestId/sample_{{loop_index}}.png`) and returns the public URL and asset metadata. (REQ-4-004)
  6. **`Aggregate Results`**: A `Merge` node collects the results from all 4 loops.
  7. **`Publish Completion Event (Sub-workflow)`**: An `Execute Workflow` node calls a sub-workflow that formats the completion message (with all sample asset URLs) and publishes it to the `generation.sample.complete` RabbitMQ exchange. (REQ-3-011)
- **Error Handling**: The error output of the AI invocation nodes and the MinIO storage node are connected to the `handle-generation-failure.workflow.json` workflow.

### 5.2. `02-process-highres-generation-request.workflow.json`
Orchestrates the final high-resolution generation. (REQ-009)
- **Trigger**: `RabbitMQ Trigger` node listening to `generation.highres.request` queue.
- **Input Data Contract**:
  json
  {
    "generationRequestId": "uuid",
    "userId": "uuid",
    "projectId": "uuid",
    "selectedSampleId": "uuid_of_the_asset",
    "originalInputPrompt": "A futuristic cityscape...", // from the original request
    "originalInputParameters": { ... }, // from the original request
    "outputResolution": "4096x4096"
  }
  
- **Workflow Logic**:
  1. **`Set Initial Data`**: Store trigger data.
  2. **`Select AI Model`**: Similar to the sample workflow, select the appropriate upscaling or high-resolution generation model. This might be a different model than the one used for samples.
  3. **`Invoke High-Res Model`**: Route to the correct AI provider sub-workflow, passing the original prompt/parameters and the new high-resolution target.
  4. **`Store Final Asset in MinIO`**: Use the `store-asset-in-minio` sub-workflow to save the final asset to a path like `userId/projectId/generationRequestId/final.png`.
  5. **`Publish Final Completion`**: Publish a message to the `generation.final.complete` RabbitMQ exchange with the final asset URL and metadata. (REQ-3-012)
- **Error Handling**: Connect critical node failure outputs to `handle-generation-failure.workflow.json`.

### 5.3. `handle-generation-failure.workflow.json`
Centralized error management. (REQ-007.1)
- **Trigger**: `Workflow Trigger` node (called by other workflows).
- **Input Data Contract**:
  json
  {
    "generationRequestId": "uuid",
    "userId": "uuid",
    "errorDetails": {
      "workflowName": "...",
      "nodeName": "...",
      "errorMessage": "...",
      "errorData": { ... } // full error object
    },
    "isSystemError": true // boolean to determine if credit refund is applicable
  }
  
- **Workflow Logic**:
  1. **`Format Log Message`**: A `Function` node creates a structured JSON log message from the input error data.
  2. **`Log Error`**: (Optional) An `HTTP Request` node could post this log to a dedicated logging service/endpoint.
  3. **`Publish Failure Event`**: A `RabbitMQ Send` node publishes a message to the `generation.failed` exchange. The message body contains the `generationRequestId`, `userId`, `errorMessage`, and `isSystemError` flag. This allows the backend to update the request status and trigger a credit refund if necessary.

## 6. Sub-Workflow Specifications

Common logic will be encapsulated in sub-workflows for reusability.

### 6.1. `select-ai-model.subworkflow.json`
- **Inputs**: `strategy` (string: "quality", "cost", "fastest"), `taskType` (string: "image_generation", "upscaling").
- **Logic**: A series of `Switch` and `Set` nodes that implement the business rules for model selection. For example, if `strategy` is "quality" and `taskType` is "image_generation", set `modelId` to `dall-e-3` and `provider` to `OpenAI`.
- **Outputs**: `{ "modelId": "...", "provider": "..." }`.

### 6.2. `store-asset-in-minio.subworkflow.json`
- **Inputs**: `fileData` (binary), `filePath` (string), `contentType` (string).
- **Logic**: Uses the `MinIO` node to upload the binary data to the specified path in the configured bucket.
- **Outputs**: `{ "url": "...", "path": "...", "size": ... }`.

### 6.3. `publish-completion-event.subworkflow.json`
- **Inputs**: `exchangeName` (string), `routingKey` (string), `payload` (JSON).
- **Logic**: A `RabbitMQ Send` node configured to publish the `payload` to the specified `exchangeName` with the `routingKey`.
- **Outputs**: `{ "status": "published" }`.