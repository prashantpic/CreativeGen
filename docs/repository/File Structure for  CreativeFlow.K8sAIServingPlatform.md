# Specification

# 1. Files

- **Path:** base/namespaces/ai-serving-namespace.yaml  
**Description:** Kubernetes Namespace definition for all AI model serving platform resources. This ensures logical separation and resource quoting within the Kubernetes cluster.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 0  
**Name:** ai-serving-namespace  
**Type:** KubernetesNamespace  
**Relative Path:** base/namespaces/ai-serving-namespace.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Kubernetes Resource Organization
    
**Requirement Ids:**
    
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Defines the dedicated Kubernetes namespace 'creativeflow-ai-serving' for isolating AI model serving workloads and associated resources.  
**Logic Description:** A standard Kubernetes Namespace manifest (apiVersion: v1, kind: Namespace) specifying metadata.name as 'creativeflow-ai-serving'.  
**Documentation:**
    
    - **Summary:** This YAML file creates a Kubernetes namespace to house all deployments, services, and configurations related to the AI model serving platform.
    
**Namespace:** kubernetes  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** base/rbac/service-account.yaml  
**Description:** Kubernetes ServiceAccount definition for AI model serving pods. Provides an identity for workloads running within the AI serving namespace.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 1  
**Name:** ai-model-server-sa  
**Type:** KubernetesServiceAccount  
**Relative Path:** base/rbac/service-account.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - PrincipleOfLeastPrivilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Workload Identity Management
    
**Requirement Ids:**
    
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Defines a ServiceAccount named 'ai-model-server-sa' within the 'creativeflow-ai-serving' namespace for AI model serving pods.  
**Logic Description:** A Kubernetes ServiceAccount manifest (apiVersion: v1, kind: ServiceAccount) specifying metadata.name and metadata.namespace.  
**Documentation:**
    
    - **Summary:** This YAML file creates a Kubernetes ServiceAccount to provide a distinct identity for AI model serving pods, enabling fine-grained access control via RBAC.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** base/rbac/role.yaml  
**Description:** Kubernetes Role definition for AI model serving pods. Specifies permissions required by the model serving pods within their namespace (e.g., to read ConfigMaps, discover services).  
**Template:** Kubernetes Manifest  
**Dependency Level:** 1  
**Name:** ai-model-server-role  
**Type:** KubernetesRole  
**Relative Path:** base/rbac/role.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - PrincipleOfLeastPrivilege
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Fine-grained Access Control
    
**Requirement Ids:**
    
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Defines a Kubernetes Role with necessary permissions for model serving pods, such as reading ConfigMaps or secrets if needed for model loading, within the 'creativeflow-ai-serving' namespace.  
**Logic Description:** A Kubernetes Role manifest (apiVersion: rbac.authorization.k8s.io/v1, kind: Role) listing rules (apiGroups, resources, verbs) required by model servers. Initially, this might be minimal, e.g., permissions to read ConfigMaps containing model configurations.  
**Documentation:**
    
    - **Summary:** This YAML file defines a Kubernetes Role granting specific, minimal permissions to AI model serving pods within their namespace.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** base/rbac/role-binding.yaml  
**Description:** Kubernetes RoleBinding to associate the 'ai-model-server-role' with the 'ai-model-server-sa' ServiceAccount within the AI serving namespace.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 2  
**Name:** ai-model-server-rb  
**Type:** KubernetesRoleBinding  
**Relative Path:** base/rbac/role-binding.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - RBAC Application
    
**Requirement Ids:**
    
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Binds the defined Role to the ServiceAccount, granting the specified permissions to pods running under that ServiceAccount.  
**Logic Description:** A Kubernetes RoleBinding manifest (apiVersion: rbac.authorization.k8s.io/v1, kind: RoleBinding) linking the 'ai-model-server-role' (RoleRef) to the 'ai-model-server-sa' ServiceAccount (subjects).  
**Documentation:**
    
    - **Summary:** This YAML file creates a Kubernetes RoleBinding that grants the permissions defined in 'ai-model-server-role' to the 'ai-model-server-sa' ServiceAccount.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** base/monitoring/model-server-servicemonitor.yaml  
**Description:** Prometheus ServiceMonitor custom resource to configure scraping of metrics from deployed model serving services. Assumes Prometheus Operator is installed in the cluster.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 1  
**Name:** model-server-servicemonitor  
**Type:** KubernetesCustomResource  
**Relative Path:** base/monitoring/model-server-servicemonitor.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - Observability
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Metrics Collection Configuration
    
**Requirement Ids:**
    
    - DEP-001 (AI Processing Cluster infrastructure reqs implies monitoring)
    
**Purpose:** Defines how Prometheus should discover and scrape metrics endpoints exposed by AI model serving services.  
**Logic Description:** A ServiceMonitor CRD manifest (apiVersion: monitoring.coreos.com/v1, kind: ServiceMonitor) specifying a selector for services labeled for AI model serving, the metrics endpoint path (e.g., /metrics), and scrape interval.  
**Documentation:**
    
    - **Summary:** This YAML file configures Prometheus to automatically discover and scrape metrics from AI model servers that expose a metrics endpoint and match the specified labels.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** runtime-bases/tensorflow-serving/Dockerfile  
**Description:** Base Dockerfile for TensorFlow Serving. Uses an official TensorFlow Serving image as a base and can be extended with common dependencies or configurations.  
**Template:** Dockerfile  
**Dependency Level:** 0  
**Name:** tensorflow-serving-base  
**Type:** DockerConfiguration  
**Relative Path:** runtime-bases/tensorflow-serving/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - TensorFlow Model Serving Environment
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Provides a standardized base image for deploying TensorFlow models, ensuring consistent runtime environments.  
**Logic Description:** FROM tensorflow/serving:<latest-gpu-version>. Optionally, ADD common utilities or scripts. Exposes port 8500 (gRPC) and 8501 (HTTP). Defines a default CMD or ENTRYPOINT if needed.  
**Documentation:**
    
    - **Summary:** This Dockerfile defines a base image for TensorFlow Serving, suitable for serving TensorFlow SavedModel bundles. It can be used as a parent image for specific model deployments.
    
**Namespace:** creativeflow.infrastructure.aiserving.runtimes.tensorflow_serving  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtime-bases/triton-inference-server/Dockerfile  
**Description:** Base Dockerfile for NVIDIA Triton Inference Server. Uses an official Triton image as a base. Ensures GPU support and common configurations.  
**Template:** Dockerfile  
**Dependency Level:** 0  
**Name:** triton-inference-server-base  
**Type:** DockerConfiguration  
**Relative Path:** runtime-bases/triton-inference-server/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Multi-Framework Model Serving Environment
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Provides a standardized base image for Triton Inference Server, enabling deployment of models from various frameworks (TensorFlow, PyTorch, ONNX).  
**Logic Description:** FROM nvcr.io/nvidia/tritonserver:<latest-version>-py3. Optionally, ADD custom backends or common dependencies. Exposes HTTP (8000), gRPC (8001), and metrics (8002) ports. Defines CMD to start `tritonserver` with a base model repository path.  
**Documentation:**
    
    - **Summary:** This Dockerfile defines a base image for NVIDIA Triton Inference Server. It is designed to serve models in various formats from a model repository.
    
**Namespace:** creativeflow.infrastructure.aiserving.runtimes.triton_inference_server  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtime-bases/custom-python-fastapi/Dockerfile  
**Description:** Base Dockerfile for custom Python model servers using FastAPI. Includes common Python dependencies and a basic application structure.  
**Template:** Dockerfile  
**Dependency Level:** 0  
**Name:** custom-python-fastapi-base  
**Type:** DockerConfiguration  
**Relative Path:** runtime-bases/custom-python-fastapi/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Python Model Serving Environment
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Provides a reusable base for custom Python model servers, pre-configured with FastAPI, Uvicorn, and essential libraries for ML inference.  
**Logic Description:** FROM python:3.10-slim. WORKDIR /app. COPY ./src /app/src. COPY requirements.txt .. RUN pip install --no-cache-dir -r requirements.txt. EXPOSE 8000. CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"].  
**Documentation:**
    
    - **Summary:** This Dockerfile sets up a Python environment with FastAPI for serving custom machine learning models. It copies a common server structure and installs dependencies.
    
**Namespace:** creativeflow.infrastructure.aiserving.runtimes.custom_python_fastapi  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtime-bases/custom-python-fastapi/src/main.py  
**Description:** Main application file for the custom Python FastAPI base server. Initializes the FastAPI app and includes routers.  
**Template:** Python Application  
**Dependency Level:** 1  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** runtime-bases/custom-python-fastapi/src/main.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - APIServer
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - FastAPI Application Setup
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Entry point for the FastAPI-based custom model server. Sets up the application instance and basic routes like health checks.  
**Logic Description:** Import FastAPI. Create an `app = FastAPI()` instance. Include routers (e.g., for prediction endpoints, health checks). Define a root path or health check endpoint (e.g., @app.get("/health")).  
**Documentation:**
    
    - **Summary:** This Python script initializes the FastAPI application, configures global settings, and includes API routers for various functionalities like health checks and model predictions.
    
**Namespace:** creativeflow.infrastructure.aiserving.ruting_bases.custom_python_fastapi.src.main  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** runtime-bases/custom-python-fastapi/src/dependencies.py  
**Description:** Defines common dependencies for the FastAPI application, such as model loading logic or shared utilities.  
**Template:** Python Application  
**Dependency Level:** 1  
**Name:** dependencies  
**Type:** UtilityModule  
**Relative Path:** runtime-bases/custom-python-fastapi/src/dependencies.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_model_loader  
**Parameters:**
    
    
**Return Type:** Callable  
**Attributes:** public  
    - **Name:** load_model_globally  
**Parameters:**
    
    - model_path: str
    
**Return Type:** Any  
**Attributes:** public  
    
**Implemented Features:**
    
    - Dependency Management
    - Model Loading
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Provides reusable dependency injection functions, primarily for loading ML models once and making them available to request handlers.  
**Logic Description:** May contain functions to load ML models from a specified path during application startup (e.g., using a global variable or a singleton pattern accessible via FastAPI's dependency injection system). This helps in avoiding reloading models on every request.  
**Documentation:**
    
    - **Summary:** This module centralizes dependency management for the FastAPI application, focusing on efficient model loading and providing shared utility functions.
    
**Namespace:** creativeflow.infrastructure.aiserving.ruting_bases.custom_python_fastapi.src.dependencies  
**Metadata:**
    
    - **Category:** ApplicationLogic
    
- **Path:** runtime-bases/custom-python-fastapi/src/routers/predict.py  
**Description:** FastAPI router defining prediction endpoints for custom Python model servers.  
**Template:** Python Application  
**Dependency Level:** 2  
**Name:** predict_router  
**Type:** APIController  
**Relative Path:** runtime-bases/custom-python-fastapi/src/routers/predict.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - APIRouter
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** predict_custom_model  
**Parameters:**
    
    - request: InferenceRequest
    - model: Any = Depends(get_model_loader)
    
**Return Type:** InferenceResponse  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Inference API Endpoint
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Handles incoming prediction requests, performs pre-processing, invokes the loaded model, performs post-processing, and returns the prediction.  
**Logic Description:** Import APIRouter from FastAPI, Depends. Import request/response Pydantic models. Import model loading dependency. Define an APIRouter instance. Create POST endpoint(s) (e.g., @router.post("/predict")) that take Pydantic models as request body, use the loaded model to make predictions, and return Pydantic response models.  
**Documentation:**
    
    - **Summary:** This module defines the `/predict` API endpoint(s) for the custom model server. It uses FastAPI's APIRouter for modularity and handles request validation, model inference, and response formatting.
    
**Namespace:** creativeflow.infrastructure.aiserving.ruting_bases.custom_python_fastapi.src.routers.predict  
**Metadata:**
    
    - **Category:** API
    
- **Path:** runtime-bases/custom-python-fastapi/src/models/inference.py  
**Description:** Pydantic models defining the structure for inference request and response data for custom Python model servers.  
**Template:** Python Application  
**Dependency Level:** 1  
**Name:** inference_models  
**Type:** DataModel  
**Relative Path:** runtime-bases/custom-python-fastapi/src/models/inference.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DTO
    
**Members:**
    
    - **Name:** features  
**Type:** List[float]  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Data Contracts
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Defines the expected JSON structure for API requests and responses, enabling data validation and serialization/deserialization.  
**Logic Description:** Import BaseModel from Pydantic. Define classes like `InferenceRequest(BaseModel)` with fields for input features (e.g., image_url: str, text_prompt: str, numerical_features: List[float]). Define classes like `InferenceResponse(BaseModel)` with fields for predictions (e.g., predictions: List[Any], probabilities: Optional[List[float]] = None).  
**Documentation:**
    
    - **Summary:** This Python script uses Pydantic to define data models for API request and response bodies, ensuring data validation and clear API contracts.
    
**Namespace:** creativeflow.infrastructure.aiserving.ruting_bases.custom_python_fastapi.src.models.inference  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** runtime-bases/custom-python-fastapi/requirements.txt  
**Description:** Python dependencies for the custom Python FastAPI base server (e.g., fastapi, uvicorn, pydantic, joblib/onnxruntime if common).  
**Template:** Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyConfiguration  
**Relative Path:** runtime-bases/custom-python-fastapi/requirements.txt  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting capabilities)
    
**Purpose:** Lists Python packages required for the base custom server to function.  
**Logic Description:** A plain text file listing Python packages and their versions, one per line (e.g., fastapi==0.100.0, uvicorn[standard]==0.23.2, pydantic==2.0.0).  
**Documentation:**
    
    - **Summary:** This file specifies the Python dependencies required for the custom FastAPI model serving runtime. These packages will be installed during the Docker image build.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** models/image-classification-resnet50/kubernetes/deployment.yaml  
**Description:** Kubernetes Deployment for a ResNet50 image classification model served via TensorFlow Serving. Requests GPU resources.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 2  
**Name:** resnet50-tfserving-deployment  
**Type:** KubernetesDeployment  
**Relative Path:** models/image-classification-resnet50/kubernetes/deployment.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - MicroserviceDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Image Classification Model Serving
    - GPU Utilization
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    - Section 2.4 (AI Processing operating environment)
    - DEP-001
    
**Purpose:** Deploys the ResNet50 TensorFlow Serving container to Kubernetes, ensuring it runs with GPU access and can be scaled.  
**Logic Description:** apiVersion: apps/v1, kind: Deployment. metadata: name: resnet50-tfserving, namespace: creativeflow-ai-serving. spec: replicas, selector, template: metadata: labels, spec: serviceAccountName: ai-model-server-sa, containers: name, image: <registry>/resnet50-tfserving:latest, ports (8500, 8501), resources: limits: nvidia.com/gpu: 1, requests: nvidia.com/gpu: 1, livenessProbe, readinessProbe, volumeMounts (for model from ConfigMap/PersistentVolume or baked into image).  
**Documentation:**
    
    - **Summary:** This YAML defines the Kubernetes Deployment for serving a ResNet50 image classification model using TensorFlow Serving. It specifies GPU requirements, probes, and scaling parameters.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/image-classification-resnet50/kubernetes/service.yaml  
**Description:** Kubernetes Service to expose the ResNet50 TensorFlow Serving deployment internally within the cluster.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** resnet50-tfserving-service  
**Type:** KubernetesService  
**Relative Path:** models/image-classification-resnet50/kubernetes/service.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Internal Service Exposure
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Provides a stable internal endpoint for other services (e.g., n8n via API Gateway) to send inference requests to the ResNet50 model.  
**Logic Description:** apiVersion: v1, kind: Service. metadata: name: resnet50-tfserving, namespace: creativeflow-ai-serving, labels for ServiceMonitor. spec: selector (matching deployment labels), ports: name: grpc, port: 8500, targetPort: 8500; name: http, port: 8501, targetPort: 8501. type: ClusterIP.  
**Documentation:**
    
    - **Summary:** This YAML defines a Kubernetes ClusterIP Service to provide a stable internal network endpoint for the ResNet50 TensorFlow Serving deployment.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/image-classification-resnet50/kubernetes/hpa.yaml  
**Description:** Kubernetes HorizontalPodAutoscaler for the ResNet50 TensorFlow Serving deployment. Scales based on CPU/GPU utilization or custom metrics.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** resnet50-tfserving-hpa  
**Type:** KubernetesHorizontalPodAutoscaler  
**Relative Path:** models/image-classification-resnet50/kubernetes/hpa.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - Autoscaling
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Scaling
    
**Requirement Ids:**
    
    - NFR-002 (Scalable GPU orchestration for throughput)
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Automatically adjusts the number of ResNet50 serving pods based on observed load, optimizing resource usage and maintaining performance.  
**Logic Description:** apiVersion: autoscaling/v2, kind: HorizontalPodAutoscaler. metadata: name: resnet50-tfserving-hpa, namespace: creativeflow-ai-serving. spec: scaleTargetRef: apiVersion: apps/v1, kind: Deployment, name: resnet50-tfserving. minReplicas, maxReplicas, metrics: type: Resource, resource: name: cpu (or nvidia.com/gpu), target: type: Utilization, averageUtilization: (e.g., 70 for CPU, or custom metrics adapter for GPU).  
**Documentation:**
    
    - **Summary:** This YAML configures a HorizontalPodAutoscaler for the ResNet50 deployment, enabling it to automatically scale the number of pods based on CPU or GPU utilization metrics.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/image-classification-resnet50/kubernetes/configmap-tfserving.yaml  
**Description:** Kubernetes ConfigMap for TensorFlow Serving model configuration for ResNet50, if models are loaded from a shared volume/path rather than baked into the image.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 1  
**Name:** resnet50-tfserving-config  
**Type:** KubernetesConfigMap  
**Relative Path:** models/image-classification-resnet50/kubernetes/configmap-tfserving.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - ExternalizedConfiguration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Configuration Management
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Provides the `models.config` file content to TensorFlow Serving, specifying which models to load and from where.  
**Logic Description:** apiVersion: v1, kind: ConfigMap. metadata: name: resnet50-tfserving-config, namespace: creativeflow-ai-serving. data: models.config: | model_config_list: { config: { name: 'resnet50', base_path: '/models/resnet50', model_platform: 'tensorflow' } }  
**Documentation:**
    
    - **Summary:** This ConfigMap stores the TensorFlow Serving model configuration file, which tells the server what models to load. This file would be mounted into the TFServing pods.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/image-classification-resnet50/docker/Dockerfile  
**Description:** Dockerfile for the ResNet50 image classification model, using TensorFlow Serving. This might simply use the base TF Serving image and add model files, or be more custom.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** resnet50-tfserving  
**Type:** DockerConfiguration  
**Relative Path:** models/image-classification-resnet50/docker/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Image Classification Model Packaging
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Packages the ResNet50 model and TensorFlow Serving runtime into a deployable Docker image.  
**Logic Description:** FROM creativeflow/tensorflow-serving-base:latest (or direct official image). COPY ../model_artifacts/resnet50 /models/resnet50. (If model is baked in). EXPOSE 8500 8501. CMD ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_name=resnet50", "--model_base_path=/models/resnet50"]. (If not using ConfigMap for model config).  
**Documentation:**
    
    - **Summary:** This Dockerfile builds an image containing the ResNet50 model artifacts and configures TensorFlow Serving to serve it. It may build upon a base TF Serving image.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.image_classification_resnet50  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** models/text-generation-gpt2/kubernetes/deployment.yaml  
**Description:** Kubernetes Deployment for a GPT-2 text generation model served via Triton Inference Server. Requests GPU resources.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 2  
**Name:** gpt2-triton-deployment  
**Type:** KubernetesDeployment  
**Relative Path:** models/text-generation-gpt2/kubernetes/deployment.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - MicroserviceDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Text Generation Model Serving
    - GPU Utilization
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    - Section 2.4 (AI Processing operating environment)
    - DEP-001
    
**Purpose:** Deploys the GPT-2 Triton Inference Server container to Kubernetes, ensuring GPU access and scalability.  
**Logic Description:** Similar to ResNet50 deployment.yaml but with image: <registry>/gpt2-triton:latest, and Triton specific ports (8000, 8001, 8002). Command might involve `tritonserver --model-repository=/models`. Volume mounts for the model repository.  
**Documentation:**
    
    - **Summary:** This YAML defines the Kubernetes Deployment for serving a GPT-2 model using Triton Inference Server, specifying GPU requirements and other deployment parameters.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/text-generation-gpt2/kubernetes/service.yaml  
**Description:** Kubernetes Service to expose the GPT-2 Triton Inference Server deployment.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** gpt2-triton-service  
**Type:** KubernetesService  
**Relative Path:** models/text-generation-gpt2/kubernetes/service.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Internal Service Exposure
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Provides a stable internal endpoint for inference requests to the GPT-2 model.  
**Logic Description:** Similar to ResNet50 service.yaml but targeting Triton ports (e.g., HTTP on 8000, gRPC on 8001). selector matches gpt2-triton deployment labels.  
**Documentation:**
    
    - **Summary:** This YAML defines a Kubernetes ClusterIP Service for the GPT-2 Triton Inference Server deployment, enabling internal cluster communication.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/text-generation-gpt2/kubernetes/hpa.yaml  
**Description:** Kubernetes HorizontalPodAutoscaler for the GPT-2 Triton deployment.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** gpt2-triton-hpa  
**Type:** KubernetesHorizontalPodAutoscaler  
**Relative Path:** models/text-generation-gpt2/kubernetes/hpa.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - Autoscaling
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Scaling
    
**Requirement Ids:**
    
    - NFR-002 (Scalable GPU orchestration for throughput)
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Automatically scales the GPT-2 Triton serving pods based on load.  
**Logic Description:** Similar to ResNet50 hpa.yaml, targeting the gpt2-triton Deployment and appropriate metrics (CPU, GPU, or custom Triton metrics if available).  
**Documentation:**
    
    - **Summary:** This YAML configures a HorizontalPodAutoscaler for the GPT-2 Triton deployment, enabling dynamic scaling based on utilization metrics.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/text-generation-gpt2/docker/Dockerfile  
**Description:** Dockerfile for the GPT-2 text generation model, using Triton Inference Server. Copies model artifacts into the expected model repository structure.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** gpt2-triton  
**Type:** DockerConfiguration  
**Relative Path:** models/text-generation-gpt2/docker/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Text Generation Model Packaging
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Packages the GPT-2 model and Triton Inference Server runtime into a deployable Docker image.  
**Logic Description:** FROM creativeflow/triton-inference-server-base:latest (or official Triton image). COPY ../model_repository /models. (The model_repository dir contains gpt2/config.pbtxt and gpt2/1/model.pt or similar). EXPOSE 8000 8001 8002. CMD ["tritonserver", "--model-repository=/models"].  
**Documentation:**
    
    - **Summary:** This Dockerfile builds an image for serving a GPT-2 model with Triton. It copies the model files structured for Triton's model repository.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.text_generation_gpt2  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** models/text-generation-gpt2/model_repository/gpt2/config.pbtxt  
**Description:** Triton Inference Server model configuration file for the GPT-2 model. Defines backend (e.g., PyTorch, ONNX), input/output tensors, and instance grouping.  
**Template:** Text Configuration  
**Dependency Level:** 0  
**Name:** gpt2-triton-model-config  
**Type:** ModelConfiguration  
**Relative Path:** models/text-generation-gpt2/model_repository/gpt2/config.pbtxt  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Triton Model Configuration
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Specifies how Triton should load and serve the GPT-2 model, including its input and output tensor definitions.  
**Logic Description:** A .pbtxt file with fields like name: "gpt2", platform: "pytorch_libtorch" or "onnxruntime_onnx", input [{name, data_type, dims}], output [{name, data_type, dims}]. instance_group [{kind: KIND_GPU, count:1}].  
**Documentation:**
    
    - **Summary:** This Triton `config.pbtxt` file provides metadata for the GPT-2 model, such as its platform, input/output tensor specifications, and instance group configuration for GPU execution.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** models/text-generation-gpt2/model_repository/gpt2/1/model.py  
**Description:** Placeholder for a Python backend script if Triton's Python backend is used for GPT-2. (Actual model weights/files e.g. model.pt would also be here).  
**Template:** Python Application  
**Dependency Level:** 0  
**Name:** gpt2_python_backend_model  
**Type:** ModelImplementation  
**Relative Path:** models/text-generation-gpt2/model_repository/gpt2/1/model.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initialize  
**Parameters:**
    
    - args
    
**Return Type:** TritonPythonModel  
**Attributes:** public  
    - **Name:** execute  
**Parameters:**
    
    - requests
    
**Return Type:** List[InferenceResponse]  
**Attributes:** public  
    - **Name:** finalize  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Triton Python Backend Logic
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** If using Triton Python backend, this script contains the logic to load the GPT-2 model and perform inference.  
**Logic Description:** Implements the TritonPythonModel class with initialize, execute, and finalize methods. `initialize` loads the model. `execute` handles inference requests.  
**Documentation:**
    
    - **Summary:** This file is a placeholder for a Triton Python backend script. It would contain the core logic for loading the GPT-2 model and handling inference requests if Triton's Python backend is chosen.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.text_generation_gpt2.model_repository.gpt2.1  
**Metadata:**
    
    - **Category:** AILogic
    
- **Path:** models/custom-object-detector-yolo/kubernetes/deployment.yaml  
**Description:** Kubernetes Deployment for a custom YOLO object detection model served via a custom Python FastAPI server. Requests GPU resources.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 2  
**Name:** yolo-custom-fastapi-deployment  
**Type:** KubernetesDeployment  
**Relative Path:** models/custom-object-detector-yolo/kubernetes/deployment.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - MicroserviceDeployment
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Object Detection Model Serving
    - GPU Utilization
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    - Section 2.4 (AI Processing operating environment)
    - DEP-001
    
**Purpose:** Deploys the custom YOLO FastAPI server container to Kubernetes for object detection inference.  
**Logic Description:** apiVersion: apps/v1, kind: Deployment. metadata: name: yolo-custom-fastapi. spec: replicas, selector, template: metadata: labels, spec: containers: name, image: <registry>/yolo-custom-fastapi:latest, ports (e.g., 8000), resources: limits: nvidia.com/gpu: 1, requests: nvidia.com/gpu: 1, livenessProbe, readinessProbe, env (e.g., MODEL_PATH).  
**Documentation:**
    
    - **Summary:** This YAML defines the Kubernetes Deployment for a custom YOLO object detection model served via a FastAPI application. It specifies GPU requirements and deployment settings.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/custom-object-detector-yolo/kubernetes/service.yaml  
**Description:** Kubernetes Service to expose the custom YOLO FastAPI server deployment.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** yolo-custom-fastapi-service  
**Type:** KubernetesService  
**Relative Path:** models/custom-object-detector-yolo/kubernetes/service.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Internal Service Exposure
    
**Requirement Ids:**
    
    - INT-007
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Provides a stable internal endpoint for inference requests to the custom YOLO model server.  
**Logic Description:** apiVersion: v1, kind: Service. metadata: name: yolo-custom-fastapi. spec: selector (matching deployment labels), ports: name: http, port: 80, targetPort: 8000. type: ClusterIP.  
**Documentation:**
    
    - **Summary:** This YAML defines a Kubernetes ClusterIP Service for the custom YOLO FastAPI server, enabling internal cluster communication to its inference endpoint.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/custom-object-detector-yolo/kubernetes/hpa.yaml  
**Description:** Kubernetes HorizontalPodAutoscaler for the custom YOLO FastAPI server deployment.  
**Template:** Kubernetes Manifest  
**Dependency Level:** 3  
**Name:** yolo-custom-fastapi-hpa  
**Type:** KubernetesHorizontalPodAutoscaler  
**Relative Path:** models/custom-object-detector-yolo/kubernetes/hpa.yaml  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - Autoscaling
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Scaling
    
**Requirement Ids:**
    
    - NFR-002 (Scalable GPU orchestration for throughput)
    - Section 5.2.2 (AI Processing Orchestration on Kubernetes)
    
**Purpose:** Automatically scales the custom YOLO serving pods based on load.  
**Logic Description:** apiVersion: autoscaling/v2, kind: HorizontalPodAutoscaler. metadata: name: yolo-custom-fastapi-hpa. spec: scaleTargetRef: apiVersion: apps/v1, kind: Deployment, name: yolo-custom-fastapi. minReplicas, maxReplicas, metrics (CPU, GPU, or custom metrics).  
**Documentation:**
    
    - **Summary:** This YAML configures a HorizontalPodAutoscaler for the custom YOLO FastAPI server, enabling dynamic scaling based on utilization or custom metrics.
    
**Namespace:** creativeflow-ai-serving  
**Metadata:**
    
    - **Category:** InfrastructureAsCode
    
- **Path:** models/custom-object-detector-yolo/docker/Dockerfile  
**Description:** Dockerfile for the custom YOLO object detector model, using the custom Python FastAPI base. Copies specific model weights and potentially a custom handler.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** yolo-custom-fastapi  
**Type:** DockerConfiguration  
**Relative Path:** models/custom-object-detector-yolo/docker/Dockerfile  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - Containerization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Object Detection Model Packaging
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Packages the YOLO model, its specific dependencies, and serving logic into a deployable Docker image.  
**Logic Description:** FROM creativeflow/custom-python-fastapi-base:latest. COPY ./src /app/src. COPY ./model_weights /app/model_weights. COPY requirements.txt .. RUN pip install --no-cache-dir -r requirements.txt. ENV MODEL_PATH=/app/model_weights/yolov5s.pt. (Or set via K8s env var).  
**Documentation:**
    
    - **Summary:** This Dockerfile builds an image for a custom YOLO object detector. It builds upon the custom FastAPI base, adds model weights, and any model-specific Python code and dependencies.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.custom_object_detector_yolo  
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** models/custom-object-detector-yolo/docker/src/model_handler.py  
**Description:** Python script containing the specific logic for loading the YOLO model, pre-processing input images, running inference, and post-processing detections for the custom FastAPI server.  
**Template:** Python Application  
**Dependency Level:** 2  
**Name:** yolo_model_handler  
**Type:** ModelImplementation  
**Relative Path:** models/custom-object-detector-yolo/docker/src/model_handler.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - StrategyPattern
    
**Members:**
    
    - **Name:** model  
**Type:** torch.hub.load or similar  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - model_path: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** preprocess_image  
**Parameters:**
    
    - image_bytes: bytes
    
**Return Type:** Tensor  
**Attributes:** private  
    - **Name:** postprocess_detections  
**Parameters:**
    
    - results: Any
    
**Return Type:** List[Dict]  
**Attributes:** private  
    - **Name:** predict  
**Parameters:**
    
    - image_bytes: bytes
    
**Return Type:** List[Dict]  
**Attributes:** public  
    
**Implemented Features:**
    
    - YOLO Model Inference Logic
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Encapsulates all logic related to handling a YOLO object detection model, from loading weights to returning structured detection results.  
**Logic Description:** Class `YOLOModelHandler`: constructor loads model from `MODEL_PATH` (e.g., `torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)`). `predict` method takes image bytes, pre-processes (resize, normalize), runs inference, post-processes (NMS, format bounding boxes), returns JSON. Relies on libraries like OpenCV, PyTorch, ultralytics/yolov5.  
**Documentation:**
    
    - **Summary:** This Python module provides a handler class for the YOLO object detection model. It includes methods for model loading, image pre-processing, inference, and post-processing of detection results.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.custom_object_detector_yolo.docker.src.model_handler  
**Metadata:**
    
    - **Category:** AILogic
    
- **Path:** models/custom-object-detector-yolo/docker/src/main.py  
**Description:** FastAPI main application file, specialized for the YOLO model if needed, or re-uses the base runtime. This might override/extend the base FastAPI app from `runtime-bases`.  
**Template:** Python Application  
**Dependency Level:** 3  
**Name:** yolo_fastapi_main  
**Type:** ApplicationEntrypoint  
**Relative Path:** models/custom-object-detector-yolo/docker/src/main.py  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    - APIServer
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    - **Name:** yolo_handler  
**Type:** YOLOModelHandler  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** predict_yolo  
**Parameters:**
    
    - file: UploadFile = File(...)
    
**Return Type:** List[Dict]  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - YOLO Inference API
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Sets up and runs the FastAPI server specifically for the YOLO model, defining its API endpoints.  
**Logic Description:** Imports FastAPI, UploadFile, File. Imports `YOLOModelHandler`. Creates FastAPI app. Initializes `yolo_handler = YOLOModelHandler(os.getenv('MODEL_PATH'))`. Defines a POST endpoint `/predict` that accepts an image file, calls `yolo_handler.predict(await file.read())`, returns results. Adds health check endpoint.  
**Documentation:**
    
    - **Summary:** This script is the entry point for the YOLO model's FastAPI server. It initializes the model handler and defines the `/predict` endpoint to process uploaded images for object detection.
    
**Namespace:** creativeflow.infrastructure.aiserving.models.custom_object_detector_yolo.docker.src.main  
**Metadata:**
    
    - **Category:** API
    
- **Path:** models/custom-object-detector-yolo/docker/requirements.txt  
**Description:** Python dependencies specific to the YOLO model server, e.g., torch, torchvision, ultralytics, opencv-python.  
**Template:** Requirements File  
**Dependency Level:** 1  
**Name:** yolo_requirements  
**Type:** DependencyConfiguration  
**Relative Path:** models/custom-object-detector-yolo/docker/requirements.txt  
**Repository Id:** REPO-K8S-AI-SERVING-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management for YOLO
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** Lists Python packages required for the custom YOLO model server to function. These are in addition to or may override those in the base FastAPI runtime.  
**Logic Description:** A plain text file listing Python packages like torch, torchvision, pyyaml, opencv-python-headless, ultralytics.  
**Documentation:**
    
    - **Summary:** This file specifies the Python dependencies unique to the YOLO object detection model server, such as specific versions of PyTorch and the ultralytics library.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableModelSpecificMetrics
  - enableAdvancedGPUFeaturesMIG
  
- **Database Configs:**
  
  


---

