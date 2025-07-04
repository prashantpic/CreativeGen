# Specification

# 1. Files

- **Path:** package.json  
**Description:** Defines project metadata, dependencies for custom n8n nodes, and scripts for building, linting, and managing the n8n development environment. This file is central to managing the TypeScript/JavaScript aspects of the repository.  
**Template:** Node.js Package  
**Dependency Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** package.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Node Dependency Management
    - Build Automation Scripts
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To manage Node.js dependencies for custom n8n nodes and define development scripts.  
**Logic Description:** Contains dependencies like '@n8n/core', '@n8n/workflow', 'typescript', 'eslint'. Scripts section includes 'build' to compile TypeScript nodes, 'dev' to run n8n locally with custom nodes, and 'lint' for code quality checks.  
**Documentation:**
    
    - **Summary:** Standard npm package.json file for the n8n custom nodes and workflow development environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** tsconfig.json  
**Description:** TypeScript compiler configuration for building custom n8n nodes from TypeScript source files into JavaScript files that n8n can execute. Specifies compiler options like target version, module system, and output directory.  
**Template:** TypeScript Configuration  
**Dependency Level:** 0  
**Name:** tsconfig  
**Type:** Configuration  
**Relative Path:** tsconfig.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - TypeScript Compilation
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To configure the TypeScript compiler for custom n8n nodes.  
**Logic Description:** Sets compiler options such as 'target': 'es2020', 'module': 'commonjs', 'outDir': './dist', 'rootDir': './nodes', and 'strict': true to ensure type safety and modern JavaScript output.  
**Documentation:**
    
    - **Summary:** Defines how TypeScript files, primarily for custom nodes, are transpiled into JavaScript.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** .env.example  
**Description:** An example file defining all necessary environment variables for running the n8n workflows. This serves as a template for developers to create their local .env file. It includes placeholders for database credentials, RabbitMQ connection strings, MinIO access keys, external AI service API keys, and internal service URLs. It should not contain any real secrets.  
**Template:** Environment Variables  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:** .env.example  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Environment Configuration
    
**Requirement Ids:**
    
    - Section 5.3.1
    - INT-005
    - INT-007
    
**Purpose:** To provide a template for environment-specific configuration and secrets.  
**Logic Description:** Lists key-value pairs for all external dependencies. Example keys: N8N_DATABASE_URL, RABBITMQ_URI, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, OPENAI_API_KEY, STABILITYAI_API_KEY, KUBERNETES_API_URL, NOTIFICATION_SERVICE_URL.  
**Documentation:**
    
    - **Summary:** A template file specifying all environment variables required by the n8n instance and its workflows. Developers must copy this to a .env file and populate it with actual values for their local environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/workflows/creative-generation/01-process-sample-generation-request.workflow.json  
**Description:** The main n8n workflow that orchestrates the generation of four low-resolution creative samples. It is triggered by a message from a RabbitMQ queue, preprocesses the input data, selects the appropriate AI model, invokes the generation process, stores the results in MinIO, and publishes a completion event.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** 01-process-sample-generation-request.workflow  
**Type:** Workflow  
**Relative Path:** workflows/creative-generation/01-process-sample-generation-request.workflow.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    - Event-Driven Architecture (EDA)
    - Saga
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Sample Generation Orchestration
    - Asynchronous Task Processing
    - AI Model Selection
    - Error Handling
    
**Requirement Ids:**
    
    - REQ-005
    - REQ-006
    - REQ-007
    - REQ-008
    - REQ-009
    - INT-005
    - Section 5.3.1
    
**Purpose:** To manage the end-to-end process of generating initial creative samples from a user request.  
**Logic Description:** Workflow steps: 1. RabbitMQ Trigger node consumes a job. 2. Data Transformation node prepares prompt and parameters. 3. 'select-ai-model.subworkflow' is executed. 4. Switch node routes to the correct AI invocation sub-workflow (OpenAI, Stability, Internal K8s) based on selection. This is repeated four times for four samples. 5. 'store-asset-in-minio.subworkflow' saves each sample. 6. Data Aggregation node collects all sample URLs. 7. 'publish-completion-event.subworkflow' sends results back via RabbitMQ. 8. An error route triggers 'handle-generation-failure.workflow'.  
**Documentation:**
    
    - **Summary:** This workflow is the entry point for generating creative samples. It receives a job from the backend, orchestrates calls to various AI models to produce four distinct variations, saves them to object storage, and notifies the backend of the results.
    
**Namespace:** CreativeFlow.Workflows.CreativeGeneration  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/workflows/creative-generation/02-process-highres-generation-request.workflow.json  
**Description:** An n8n workflow for generating the final, high-resolution creative asset after a user has selected one of the low-resolution samples. This workflow is triggered by a specific RabbitMQ message containing the selected sample's details.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 2  
**Name:** 02-process-highres-generation-request.workflow  
**Type:** Workflow  
**Relative Path:** workflows/creative-generation/02-process-highres-generation-request.workflow.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    - Event-Driven Architecture (EDA)
    - Saga
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - High-Resolution Generation Orchestration
    - Progressive Enhancement
    
**Requirement Ids:**
    
    - REQ-009
    - Section 5.3.1
    
**Purpose:** To manage the workflow for upscaling a selected creative sample to a final high-resolution asset.  
**Logic Description:** Workflow steps: 1. RabbitMQ Trigger node consumes a 'high-res generation' job. 2. Data Transformation node retrieves original prompt and parameters, adding high-resolution flags. 3. Invokes the appropriate AI model sub-workflow for upscaling or regeneration at high-res. 4. 'store-asset-in-minio.subworkflow' saves the final asset. 5. 'publish-completion-event.subworkflow' sends the final asset URL and metadata back via RabbitMQ. 6. An error route triggers 'handle-generation-failure.workflow'.  
**Documentation:**
    
    - **Summary:** This workflow handles the second stage of the creative process: taking a user-selected sample and generating the final, high-quality output. It manages the call to the upscaling/high-res generation model and notifies the backend upon completion.
    
**Namespace:** CreativeFlow.Workflows.CreativeGeneration  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/workflows/sub-workflows/invoke-internal-k8s-model.subworkflow.json  
**Description:** A reusable sub-workflow that encapsulates the logic for submitting a job to the internal Kubernetes cluster to run a custom AI model. It uses the custom 'KubernetesJobSubmitter' node.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 1  
**Name:** invoke-internal-k8s-model.subworkflow  
**Type:** SubWorkflow  
**Relative Path:** workflows/sub-workflows/invoke-internal-k8s-model.subworkflow.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Model Invocation
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.3.1
    
**Purpose:** To abstract the process of running a custom, self-hosted AI model on the Kubernetes GPU cluster.  
**Logic Description:** This workflow receives parameters like the model name, version, and input data. It uses the custom KubernetesJobSubmitter node to create a new job in the K8s cluster. It then enters a loop with a wait period to poll the job's status. Once the job completes, it retrieves the output (e.g., a path to an asset in a shared volume) and returns it to the parent workflow.  
**Documentation:**
    
    - **Summary:** Provides a standardized way for other workflows to execute custom AI models hosted on the internal Kubernetes cluster. It handles job submission and status monitoring.
    
**Namespace:** CreativeFlow.SubWorkflows.AI  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/workflows/error-handling/handle-generation-failure.workflow.json  
**Description:** A centralized error handling workflow. It is called by other workflows when a failure occurs. It logs detailed error information and publishes an event to RabbitMQ to notify the backend about the failure, potentially triggering a credit refund.  
**Template:** n8n Workflow JSON  
**Dependency Level:** 1  
**Name:** handle-generation-failure.workflow  
**Type:** Workflow  
**Relative Path:** workflows/error-handling/handle-generation-failure.workflow.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    - Saga (Compensation)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Error Handling
    - Credit Refund Trigger
    
**Requirement Ids:**
    
    - REQ-007.1
    
**Purpose:** To provide a consistent and reusable process for handling failures within AI generation workflows.  
**Logic Description:** This workflow is triggered with error details as input. It uses a Function node to format a detailed error log. It then uses a RabbitMQ Send node to publish a message to a dedicated 'generation.failed' exchange, including the original generation request ID, user ID, and a flag indicating if it was a system-side error eligible for a credit refund.  
**Documentation:**
    
    - **Summary:** This workflow standardizes error handling. When invoked, it logs the error and sends a message to the backend to process the failure, ensuring users are not charged for system-side issues.
    
**Namespace:** CreativeFlow.Workflows.ErrorHandling  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/nodes/KubernetesJobSubmitter/KubernetesJobSubmitter.node.ts  
**Description:** A custom n8n node, written in TypeScript, that interacts with the Kubernetes API to create, monitor, and manage batch jobs, specifically for running custom AI models. This node abstracts the complexity of Kubernetes API calls.  
**Template:** n8n Custom Node  
**Dependency Level:** 1  
**Name:** KubernetesJobSubmitter.node  
**Type:** CustomNode  
**Relative Path:** nodes/KubernetesJobSubmitter/KubernetesJobSubmitter.node.ts  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    - Adapter
    
**Members:**
    
    - **Name:** description  
**Type:** INodeTypeDescription  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** execute  
**Parameters:**
    
    - this: IExecuteFunctions
    
**Return Type:** Promise<INodeExecutionData[][]>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Kubernetes Job Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To provide a simple, configurable n8n node for running containerized jobs on the Kubernetes cluster.  
**Logic Description:** The node's properties define inputs for the Kubernetes Job YAML (image, command, args, volume mounts, resource requests). The execute method constructs the Job manifest, uses the configured Kubernetes credentials to make an API call to create the Job. It can then optionally poll the job's status endpoint until it's completed or has failed, returning the final status and any relevant logs or output file paths.  
**Documentation:**
    
    - **Summary:** This custom node allows n8n workflows to run containerized AI models on the internal Kubernetes GPU cluster by creating and managing Kubernetes Jobs.
    
**Namespace:** CreativeFlow.Nodes.Kubernetes  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/nodes/KubernetesJobSubmitter/package.json  
**Description:** Defines the n8n metadata for the KubernetesJobSubmitter custom node, including the entry point to the compiled JavaScript file. This file is essential for n8n to discover and load the custom node.  
**Template:** Node.js Package  
**Dependency Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** nodes/KubernetesJobSubmitter/package.json  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Node Registration
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To register the custom node with the n8n instance.  
**Logic Description:** Contains a special 'n8n' key which points to the locations of node definition files. For example, 'n8n': { 'nodes': ['dist/KubernetesJobSubmitter.node.js'] }. This ensures n8n loads the compiled node logic.  
**Documentation:**
    
    - **Summary:** Metadata file for the KubernetesJobSubmitter custom node, making it discoverable by n8n.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** .docker/docker-compose.yml  
**Description:** Docker Compose file to set up a local development environment. It defines services for n8n, PostgreSQL (for n8n's own database), RabbitMQ, and MinIO. This allows developers to run and test workflows locally in an environment that mimics production services.  
**Template:** Docker Compose  
**Dependency Level:** 1  
**Name:** docker-compose  
**Type:** Configuration  
**Relative Path:** .docker/docker-compose.yml  
**Repository Id:** REPO-SERVICE-AIORCH-N8N-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Local Development Environment
    
**Requirement Ids:**
    
    - Section 5.2.2
    - DEP-004
    
**Purpose:** To enable a consistent and easy-to-start local development and testing environment.  
**Logic Description:** Defines services: 'n8n' (using the official n8n image, mounting local workflows and custom nodes, and passing environment variables from a .env file), 'postgres' (for n8n backend), 'rabbitmq' (for message queuing), and 'minio' (for object storage). It sets up persistent volumes for data and establishes a common network for inter-service communication.  
**Documentation:**
    
    - **Summary:** This file orchestrates the setup of all necessary services for local n8n workflow development and testing, ensuring developers have a production-like environment on their machines.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DevOps
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableCustomModelA/BTesting
  - useStabilityAIAsDefault
  - enableAdvancedColorSchemeSuggestion
  
- **Database Configs:**
  
  - N8N_DB_TYPE
  - N8N_DB_POSTGRESDB_HOST
  - N8N_DB_POSTGRESDB_PORT
  - N8N_DB_POSTGRESDB_DATABASE
  - N8N_DB_POSTGRESDB_USER
  - N8N_DB_POSTGRESDB_PASSWORD
  


---

