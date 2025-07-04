# Software Design Specification: CreativeFlow.K8sAIServingPlatform

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.K8sAIServingPlatform` repository. This platform is responsible for deploying, managing, and scaling AI models on a GPU-accelerated Kubernetes cluster. It serves as the core execution environment for custom and third-party AI models used within the CreativeFlow AI ecosystem. The specifications herein will guide the development of Kubernetes manifests, Docker images, and configurations required for the AI model serving runtimes.

### 1.2 Scope
The scope of this repository includes:
-   Base Kubernetes configurations for the AI serving namespace, Role-Based Access Control (RBAC), and monitoring.
-   Standardized Docker base images for common AI model serving runtimes: TensorFlow Serving, NVIDIA Triton Inference Server, and a custom Python (FastAPI) server.
-   Example Kubernetes deployment patterns for various types of AI models, demonstrating GPU resource allocation, scaling, service exposure, and configuration.
-   Configuration files for model servers (e.g., Triton `config.pbtxt`).
-   Source code for any custom Python model serving wrappers or handlers.

This repository provides the *environment and patterns* for serving AI models. The actual deployment lifecycle (uploading new models, promoting versions) will be managed by the MLOps Platform Service (`AISIML-006` to `AISIML-013`). Inference requests are typically orchestrated by the n8n Workflow Engine.

### 1.3 Definitions, Acronyms, and Abbreviations
-   **AI:** Artificial Intelligence
-   **API:** Application Programming Interface
-   **CI/CD:** Continuous Integration/Continuous Deployment
-   **CPU:** Central Processing Unit
-   **CRD:** Custom Resource Definition (Kubernetes)
-   **GPU:** Graphics Processing Unit
-   **HPA:** Horizontal Pod Autoscaler (Kubernetes)
-   **IaC:** Infrastructure as Code
-   **K8s:** Kubernetes
-   **MIG:** Multi-Instance GPU (NVIDIA)
-   **ML:** Machine Learning
-   **MLOps:** Machine Learning Operations
-   **NFR:** Non-Functional Requirement
-   **ONNX:** Open Neural Network Exchange
-   **PWA:** Progressive Web Application
-   **RBAC:** Role-Based Access Control
-   **SDS:** Software Design Specification
-   **SRS:** Software Requirements Specification
-   **TF Serving:** TensorFlow Serving
-   **YAML:** YAML Ain't Markup Language

## 2. System Overview
The K8s AI Serving Platform is a critical backend component within the CreativeFlow AI architecture. It leverages Kubernetes to orchestrate containerized AI models on GPU-enabled nodes, providing scalable and resilient inference endpoints.
It interacts with:
-   **MLOps Platform Service (`REPO-AISIML-MLOPS-001`):** This service manages the lifecycle of custom AI models, including deploying them to this K8s platform.
-   **n8n Workflow Engine (`REPO-WORKFLOW-N8N-001`):** n8n workflows will invoke the AI models served by this platform to perform creative generation tasks.
-   **Monitoring Stack (Prometheus, Grafana):** Model serving instances will expose metrics for monitoring performance and health.

The platform is designed to support various model types and serving runtimes, ensuring flexibility and extensibility as new AI models and technologies emerge.

## 3. Design Considerations

### 3.1 Technology Stack
-   **Orchestration:** Kubernetes (v1.29.2 or later, e.g., K3s, RKE2, or full K8s)
-   **Containerization:** Docker (Engine v26.0.0 or later)
-   **GPU Management:** NVIDIA GPU Operator (v23.9.2 or later), NVIDIA CUDA Toolkit (v12.3 or later), NVIDIA cuDNN (v8.9.7 or later)
-   **Model Serving Runtimes:**
    -   TensorFlow Serving (v2.15.0 or later)
    -   NVIDIA Triton Inference Server (v24.05.0 or later)
    -   Custom Python Server: Python (v3.12.2 or later), FastAPI, Uvicorn
-   **Configuration:** YAML (for Kubernetes manifests), Dockerfile
-   **Language (for custom servers/wrappers):** Python (v3.12.2 or later)

### 3.2 Modularity
-   **Base Runtime Images:** Common Docker configurations for TensorFlow Serving, Triton, and Custom Python (FastAPI) will be provided as reusable base images.
-   **Model-Specific Deployments:** Each AI model or model type will have its dedicated set of Kubernetes manifests and potentially a specialized Docker image inheriting from a base runtime. This allows for independent configuration and resource allocation.

### 3.3 Scalability
-   **Horizontal Pod Autoscaling (HPA):** Kubernetes HPA will be configured for model deployments to automatically scale the number of serving pods based on CPU utilization, GPU utilization (via custom metrics adapter if needed), or other relevant metrics (NFR-002).
-   **Cluster Autoscaler:** While not configured in this repository, the underlying K8s cluster managed by `REPO-INFRA-CORE-001` is expected to support node scaling (Cluster Autoscaler) to add more GPU nodes if pod scaling demands it.

### 3.4 Configuration Management
-   All Kubernetes resources will be defined declaratively using YAML manifests.
-   Docker images will be built using version-controlled Dockerfiles.
-   Externalized configuration for model servers (e.g., model paths, versions) will be managed via Kubernetes ConfigMaps or environment variables injected into deployments.

### 3.5 Security
-   **RBAC:** Kubernetes RBAC will be used to grant least-privilege permissions to model serving pods via dedicated ServiceAccounts, Roles, and RoleBindings.
-   **GPU Resource Isolation:** The NVIDIA GPU Operator helps manage and isolate GPU resources.
-   **Network Policies:** (Assumed to be configured at the cluster level by `REPO-INFRA-CORE-001`) Network policies should restrict communication to and from model serving pods to only necessary services.
-   **Container Image Security:** Base images will be sourced from official, trusted repositories. Application-specific Dockerfiles will be kept minimal. Vulnerability scanning is expected as part of the MLOps CI/CD pipeline.

### 3.6 Monitoring
-   Model serving runtimes (Triton, TF Serving, custom FastAPI) will be configured or implemented to expose Prometheus-compatible metrics endpoints.
-   Kubernetes `ServiceMonitor` Custom Resources will be defined to enable Prometheus to scrape these metrics.
-   Logs from model serving pods will be streamed to standard output (stdout/stderr) for collection by the centralized logging system (e.g., ELK/Loki, managed by `REPO-MONITORING-001`).

## 4. Kubernetes Platform Base Configuration

### 4.1 Namespace
-   **File:** `base/namespaces/ai-serving-namespace.yaml`
-   **Purpose:** To create a dedicated Kubernetes namespace `creativeflow-ai-serving` for all AI model serving platform resources. This isolates AI workloads from other applications in the cluster.
-   **Specification:**
    yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: creativeflow-ai-serving
        app.kubernetes.io/part-of: creativeflow-platform
    

### 4.2 Role-Based Access Control (RBAC)

#### 4.2.1 ServiceAccount
-   **File:** `base/rbac/service-account.yaml`
-   **Purpose:** To define a ServiceAccount `ai-model-server-sa` for AI model serving pods.
-   **Specification:**
    yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: ai-model-server-sa
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-sa
    

#### 4.2.2 Role
-   **File:** `base/rbac/role.yaml`
-   **Purpose:** To define a Role `ai-model-server-role` granting necessary permissions within the `creativeflow-ai-serving` namespace. Initially, this might be minimal (e.g., reading ConfigMaps for model configurations). Permissions will be expanded based on specific model server needs.
-   **Specification:**
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: ai-model-server-role
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-role
    rules:
    - apiGroups: [""] # core API group
      resources: ["configmaps", "secrets"] # Example: if models load config/secrets
      verbs: ["get", "watch", "list"]
    - apiGroups: [""]
      resources: ["pods", "services"] # If model servers need to discover peers or self-inspect
      verbs: ["get", "list"]
    # Add other permissions as required by specific serving runtimes
    

#### 4.2.3 RoleBinding
-   **File:** `base/rbac/role-binding.yaml`
-   **Purpose:** To bind the `ai-model-server-role` to the `ai-model-server-sa` ServiceAccount.
-   **Specification:**
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: ai-model-server-rb
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-rb
    subjects:
    - kind: ServiceAccount
      name: ai-model-server-sa
      namespace: creativeflow-ai-serving
    roleRef:
      kind: Role
      name: ai-model-server-role
      apiGroup: rbac.authorization.k8s.io
    

### 4.3 Monitoring Configuration

#### 4.3.1 ServiceMonitor
-   **File:** `base/monitoring/model-server-servicemonitor.yaml`
-   **Purpose:** To configure Prometheus (via Prometheus Operator) to scrape metrics from AI model serving Services.
-   **Specification:**
    yaml
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: model-server-servicemonitor
      namespace: creativeflow-ai-serving # Or the namespace where Prometheus Operator looks for ServiceMonitors
      labels:
        app.kubernetes.io/name: model-server-servicemonitor
        # Add labels that Prometheus Operator uses to discover ServiceMonitors, e.g.:
        # release: prometheus 
    spec:
      namespaceSelector:
        matchNames:
        - creativeflow-ai-serving # Scrape services only in this namespace
      selector:
        matchLabels:
          # Services must have this label to be scraped
          creativeflow.ai/scrape-metrics: "true" 
      endpoints:
      - port: metrics # Assumes services expose metrics on a port named 'metrics'
        interval: 30s
        path: /metrics # Default metrics path, can be overridden per service
      # Add more endpoints if services expose metrics on different ports/paths
      # Example for Triton:
      # - port: http-metrics 
      #   interval: 30s
      #   path: /metrics
    
    **Note:** Services for specific model deployments (e.g., `resnet50-tfserving-service`) will need the label `creativeflow.ai/scrape-metrics: "true"` and a port named `metrics` (or other names specified in `endpoints`) for this ServiceMonitor to pick them up.

## 5. Runtime Base Images Design

These Dockerfiles provide common, standardized environments for different model serving runtimes. Specific model images will typically build `FROM` these base images.

### 5.1 TensorFlow Serving Base
-   **File:** `runtime-bases/tensorflow-serving/Dockerfile`
-   **Purpose:** A base image for serving TensorFlow SavedModel bundles.
-   **Specification:**
    dockerfile
    # Use an official TensorFlow Serving image with GPU support
    ARG TENSORFLOW_SERVING_VERSION=latest-gpu
    FROM tensorflow/serving:${TENSORFLOW_SERVING_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for TensorFlow Serving with GPU support on CreativeFlow AI."

    # (Optional) Add common utilities or scripts if needed by all TF Serving deployments
    # e.g., COPY common_utils.sh /usr/local/bin/
    # RUN chmod +x /usr/local/bin/common_utils.sh

    # Expose default TensorFlow Serving ports
    EXPOSE 8500 # gRPC port
    EXPOSE 8501 # REST API port

    # Default command can be overridden by specific model Dockerfiles or K8s deployment
    # This base image does not specify a default model to load.
    # Models will be loaded via configuration passed at runtime (e.g., --model_config_file)
    # or by specific model images baking in the model and CMD.
    CMD ["tensorflow_model_server"]
    

### 5.2 NVIDIA Triton Inference Server Base
-   **File:** `runtime-bases/triton-inference-server/Dockerfile`
-   **Purpose:** A base image for NVIDIA Triton Inference Server, capable of serving models from various frameworks.
-   **Specification:**
    dockerfile
    # Use an official NVIDIA Triton Inference Server image
    ARG TRITON_SERVER_VERSION=24.05-py3 # Specify desired version from nvcr.io
    FROM nvcr.io/nvidia/tritonserver:${TRITON_SERVER_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for NVIDIA Triton Inference Server on CreativeFlow AI."

    # (Optional) Add custom backends, common dependencies, or health check scripts
    # e.g., COPY ./custom_backends /opt/tritonserver/backends/
    # RUN pip install --no-cache-dir <common_python_package_for_backends>

    # Default model repository path within the container
    ENV MODEL_REPOSITORY_PATH=/models

    # Create the model repository directory
    RUN mkdir -p ${MODEL_REPOSITORY_PATH}

    # Expose default Triton ports
    EXPOSE 8000 # HTTP
    EXPOSE 8001 # gRPC
    EXPOSE 8002 # Metrics

    # Default command to start Triton server.
    # The --model-repository can be overridden.
    # Specific model images will COPY their models into ${MODEL_REPOSITORY_PATH}.
    CMD ["tritonserver", "--model-repository=${MODEL_REPOSITORY_PATH}"]
    

### 5.3 Custom Python FastAPI Base
This base provides a common structure for serving custom Python models using FastAPI.

#### 5.3.1 Dockerfile
-   **File:** `runtime-bases/custom-python-fastapi/Dockerfile`
-   **Purpose:** A reusable base for custom Python model servers using FastAPI.
-   **Specification:**
    dockerfile
    ARG PYTHON_VERSION=3.12-slim
    FROM python:${PYTHON_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for custom Python AI models served with FastAPI on CreativeFlow AI."

    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    WORKDIR /app

    # Copy base requirements and install them
    COPY ./runtime-bases/custom-python-fastapi/requirements.txt /app/requirements_base.txt
    RUN pip install --no-cache-dir -r requirements_base.txt

    # Copy the base application structure
    # Specific models can add their own src/ and override/extend this.
    COPY ./runtime-bases/custom-python-fastapi/src /app/src

    # Port for FastAPI application
    EXPOSE 8000

    # Default command to run the FastAPI application using Uvicorn
    # This assumes the entrypoint is src.main:app
    # Specific model images might override this if their entrypoint or app structure differs.
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 
    # Note: Consider adjusting --workers based on application type (CPU/IO bound) and K8s resource requests.
    # For GPU-bound tasks, typically 1 worker per GPU or instance is common.
    

#### 5.3.2 `requirements.txt`
-   **File:** `runtime-bases/custom-python-fastapi/requirements.txt`
-   **Purpose:** Core Python dependencies for the FastAPI base server.
-   **Specification:**
    txt
    fastapi>=0.100.0,<0.112.0
    uvicorn[standard]>=0.23.0,<0.30.0
    pydantic>=2.0.0,<2.8.0
    python-dotenv>=1.0.0,<1.1.0
    # Add other common libraries like prometheus_client for metrics
    prometheus_client>=0.17.0,<0.21.0 
    

#### 5.3.3 `src/main.py`
-   **File:** `runtime-bases/custom-python-fastapi/src/main.py`
-   **Purpose:** Initializes the base FastAPI application.
-   **Specification:**
    python
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import os
    from prometheus_client import Counter, Histogram, make_asgi_app # For metrics
    # from .routers import predict # Example: if base has a generic predict router
    # from .dependencies import load_model_globally # Example

    # Metrics (example)
    REQUEST_COUNT = Counter("custom_server_requests_total", "Total count of requests.", ["method", "endpoint", "http_status"])
    REQUEST_LATENCY = Histogram("custom_server_request_latency_seconds", "Histogram of request latencies.", ["method", "endpoint"])

    app = FastAPI(
        title="CreativeFlow Custom AI Model Server",
        description="Base FastAPI server for custom AI models.",
        version="0.1.0"
    )

    # Add Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # Example: Global model loading at startup (can be specialized by model image)
    # MODEL_PATH = os.getenv("MODEL_PATH", "/app/default_model_path") # Get model path from ENV
    # model = None
    # @app.on_event("startup")
    # async def startup_event():
    #     global model
    #     # model = load_model_globally(MODEL_PATH) # From dependencies.py
    #     # print(f"Model loaded from {MODEL_PATH}")
    #     print("FastAPI application startup complete.")


    @app.get("/health", summary="Health Check", tags=["System"])
    async def health_check():
        """
        Performs a health check of the application.
        Returns HTTP 200 if the application is healthy.
        """
        REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
        return JSONResponse(content={"status": "healthy"})

    # Example: Include routers from other files
    # from .routers import predict_router # Assuming a generic predict router exists
    # app.include_router(predict_router, prefix="/v1", tags=["Predictions"])

    # Models are expected to define their own specific prediction routers
    # and include them in their specialized main.py or use this as a base.
    

#### 5.3.4 `src/dependencies.py`
-   **File:** `runtime-bases/custom-python-fastapi/src/dependencies.py`
-   **Purpose:** Common dependency injection logic, e.g., for model loading.
-   **Specification:**
    python
    # from typing import Any, Callable
    # import os
    # import joblib # Example for scikit-learn models
    # import onnxruntime # Example for ONNX models

    # # This is a placeholder/example. Actual model loading will be specific to the model type.
    # # Model-specific Docker images would implement their own loaders.
    # _global_model: Any = None

    # def load_model_globally(model_path: str) -> Any:
    #     """
    #     Loads a model from the given path.
    #     This is a generic placeholder; actual implementation depends on model type.
    #     """
    #     global _global_model
    #     if _global_model is None:
    #         if not model_path or not os.path.exists(model_path):
    #             raise ValueError(f"Model path '{model_path}' not found or not specified.")
            
    #         print(f"Loading model from: {model_path}")
    #         # Example: Add logic based on file extension or config
    #         # if model_path.endswith(".onnx"):
    #         #     _global_model = onnxruntime.InferenceSession(model_path)
    #         # elif model_path.endswith(".joblib"):
    #         #     _global_model = joblib.load(model_path)
    #         # else:
    #         #     raise ValueError(f"Unsupported model format: {model_path}")
    #         _global_model = "DUMMY_MODEL_LOADED" # Replace with actual loading
    #         print("Model loaded successfully (dummy).")
    #     return _global_model

    # async def get_model_loader() -> Callable:
    #     """
    #     FastAPI dependency to get the loaded model.
    #     """
    #     # This ensures the model is loaded via startup or first request if not already.
    #     # MODEL_PATH = os.getenv("MODEL_PATH")
    #     # if _global_model is None and MODEL_PATH:
    #     #     load_model_globally(MODEL_PATH)
    #     # return _global_model
    #     return lambda: "DUMMY_MODEL_INSTANCE" # Placeholder
    
    **Note:** The actual model loading will be highly specific to each model and its framework. This base `dependencies.py` provides a conceptual placeholder. Model-specific images might override this or provide their own refined model loading mechanism.

#### 5.3.5 `src/routers/predict.py` (Generic Base)
-   **File:** `runtime-bases/custom-python-fastapi/src/routers/predict.py`
-   **Purpose:** A placeholder for a generic prediction router. Specific models will define their own.
-   **Specification:**
    python
    # from fastapi import APIRouter, Depends, HTTPException
    # from typing import Any
    # from ..models.inference import InferenceRequest, InferenceResponse # Example Pydantic models
    # from ..dependencies import get_model_loader # Example dependency

    # router = APIRouter()

    # @router.post("/predict", response_model=InferenceResponse, summary="Generic Prediction Endpoint", tags=["Predictions"])
    # async def predict_custom_model(
    #     request: InferenceRequest,
    #     model: Any = Depends(get_model_loader) # Injects the loaded model
    # ):
    #     """
    #     Placeholder for a generic prediction endpoint.
    #     Specific models should implement their own prediction logic.
    #     """
    #     if model is None:
    #         raise HTTPException(status_code=503, detail="Model not loaded")
        
    #     try:
    #         # Example: (Actual prediction logic will vary greatly)
    #         # input_data = request.features 
    #         # prediction_result = model.predict([input_data]) # Assuming model has a predict method
    #         # return InferenceResponse(predictions=prediction_result.tolist())
    #         return InferenceResponse(predictions=["dummy_prediction_from_base_router"])
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    

#### 5.3.6 `src/models/inference.py` (Generic Base)
-   **File:** `runtime-bases/custom-python-fastapi/src/models/inference.py`
-   **Purpose:** Generic Pydantic models for request/response.
-   **Specification:**
    python
    from pydantic import BaseModel
    from typing import List, Any, Optional

    class BaseInferenceRequest(BaseModel):
        # Define common fields if any, or leave empty for specialization
        pass

    class BaseInferenceResponse(BaseModel):
        predictions: List[Any]
        request_id: Optional[str] = None
        model_name: Optional[str] = None
        model_version: Optional[str] = None
    
    **Note:** Specific models will define their own `InferenceRequest` and `InferenceResponse` inheriting from these or directly, tailored to their I/O schemas.

## 6. Example AI Model Deployment Design

This section outlines the Kubernetes manifests and Docker configurations for serving example AI models. These serve as templates or starting points for deploying actual models managed by the MLOps service.

### 6.1 General Pattern for Model Deployments
Each model deployment will typically consist of:
1.  **Model-Specific Dockerfile:** Builds `FROM` one of the `runtime-bases` or a relevant official image. It copies model artifacts (weights, configuration files) into the image and may set specific `CMD` or `ENTRYPOINT` instructions.
2.  **Kubernetes `Deployment` (`deployment.yaml`):**
    *   Manages replicated pods of the model server.
    *   Specifies the Docker image to use (from the private registry).
    *   Requests GPU resources (e.g., `nvidia.com/gpu: 1`).
    *   Configures readiness and liveness probes.
    *   Mounts ConfigMaps or PersistentVolumes if models/configurations are not baked into the image.
    *   Assigns the `ai-model-server-sa` ServiceAccount.
    *   Sets environment variables (e.g., `MODEL_NAME`, `MODEL_PATH`, logging levels).
    *   Includes labels for service discovery (e.g., `app: <model-name>`, `runtime: <tfserving|triton|custom>`) and metrics scraping (`creativeflow.ai/scrape-metrics: "true"`).
3.  **Kubernetes `Service` (`service.yaml`):**
    *   Provides a stable ClusterIP endpoint for internal access to the model deployment.
    *   Maps service ports to container ports (e.g., gRPC, HTTP, metrics).
    *   Includes the label `creativeflow.ai/scrape-metrics: "true"` if metrics are exposed.
4.  **Kubernetes `HorizontalPodAutoscaler` (`hpa.yaml`):**
    *   Automatically scales the `Deployment` based on metrics like CPU utilization, GPU utilization (e.g., `DCGM_FI_DEV_GPU_UTIL` if using a custom metrics adapter like prometheus-adapter with `nvidia-dcgm-exporter`), or custom metrics like requests per second or queue length (if applicable).
5.  **Kubernetes `ConfigMap` (optional, `configmap-*.yaml`):**
    *   To store model server configuration files (e.g., TensorFlow Serving `models.config`, Triton `config.pbtxt` if not part of the model repository structure baked into the image).

### 6.2 Image Classification: ResNet50 via TensorFlow Serving

#### 6.2.1 `models/image-classification-resnet50/docker/Dockerfile`
-   **Purpose:** Package ResNet50 model with TensorFlow Serving.
-   **Specification:**
    dockerfile
    # Use the CreativeFlow AI base image for TensorFlow Serving
    ARG CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG=latest 
    FROM creativeflow/tensorflow-serving-base:${CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG}
    # Alternatively, use an official TF Serving image directly if the base is not specialized enough:
    # FROM tensorflow/serving:latest-gpu

    LABEL model.name="resnet50"
    LABEL model.framework="tensorflow"
    LABEL model.task="image-classification"

    # Path where models will be stored inside the container
    ENV MODEL_BASE_PATH=/models
    ENV MODEL_NAME=resnet50

    # Create model directory
    RUN mkdir -p ${MODEL_BASE_PATH}/${MODEL_NAME}

    # Copy the ResNet50 SavedModel bundle into the image
    # Assume model artifacts are in ../model_artifacts/resnet50/[version_number]/saved_model.pb and variables/
    COPY ../model_artifacts/resnet50 ${MODEL_BASE_PATH}/${MODEL_NAME}

    # Expose TensorFlow Serving ports (already exposed in base, but good for clarity)
    EXPOSE 8500 # gRPC
    EXPOSE 8501 # REST

    # If not using a model config file, directly specify model name and base path
    # The base image might already have a generic CMD.
    # This CMD assumes the model files are structured correctly for TF Serving auto-discovery,
    # e.g., /models/resnet50/1/saved_model.pb
    CMD ["tensorflow_model_server", \
        "--port=8500", \
        "--rest_api_port=8501", \
        "--model_name=${MODEL_NAME}", \
        "--model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}" \
    ]
    # Alternatively, if using a models.config file:
    # COPY ./models.config /etc/tf_serving/models.config
    # CMD ["tensorflow_model_server", "--model_config_file=/etc/tf_serving/models.config"]
    

#### 6.2.2 `models/image-classification-resnet50/kubernetes/deployment.yaml`
-   **Specification:**
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: resnet50-tfserving
      namespace: creativeflow-ai-serving
      labels:
        app: resnet50-tfserving
        runtime: tensorflow-serving
        model: resnet50
        task: image-classification
    spec:
      replicas: 1 # Start with 1, HPA will manage
      selector:
        matchLabels:
          app: resnet50-tfserving
      template:
        metadata:
          labels:
            app: resnet50-tfserving
            runtime: tensorflow-serving
            model: resnet50
            task: image-classification
            creativeflow.ai/scrape-metrics: "true" # For Prometheus ServiceMonitor
        spec:
          serviceAccountName: ai-model-server-sa
          containers:
          - name: resnet50-tfserving-container
            image: your-private-registry/creativeflow/resnet50-tfserving:latest # Replace with actual registry path
            imagePullPolicy: IfNotPresent
            ports:
            - containerPort: 8500
              name: grpc
            - containerPort: 8501
              name: http
            # TensorFlow Serving itself doesn't expose /metrics by default in older versions.
            # If using a newer version or custom setup that does, add a metrics port:
            # - containerPort: 8502 
            #   name: metrics 
            resources:
              limits:
                nvidia.com/gpu: 1 
              requests:
                nvidia.com/gpu: 1
                # cpu: "1" # Adjust based on pre/post processing needs
                # memory: "2Gi" # Adjust
            readinessProbe:
              httpGet:
                path: "/v1/models/resnet50" # TF Serving readiness endpoint
                port: http 
              initialDelaySeconds: 15
              periodSeconds: 10
            livenessProbe:
              httpGet:
                path: "/v1/models/resnet50"
                port: http
              initialDelaySeconds: 30
            # Volume mounts if models.config is used from ConfigMap
            # volumeMounts:
            # - name: model-config-volume
            #   mountPath: /etc/tf_serving/
            #   readOnly: true
          # volumes:
          # - name: model-config-volume
          #   configMap:
          #     name: resnet50-tfserving-config # Corresponds to configmap-tfserving.yaml
    

#### 6.2.3 `models/image-classification-resnet50/kubernetes/service.yaml`
-   **Specification:**
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: resnet50-tfserving-service
      namespace: creativeflow-ai-serving
      labels:
        app: resnet50-tfserving
        runtime: tensorflow-serving
        creativeflow.ai/scrape-metrics: "true" # If metrics port is exposed by container
    spec:
      selector:
        app: resnet50-tfserving
      ports:
      - name: grpc
        protocol: TCP
        port: 8500
        targetPort: grpc
      - name: http
        protocol: TCP
        port: 8501 # Service port for HTTP
        targetPort: http # Target port name on the pod
      # - name: metrics # If TF Serving is configured to expose Prometheus metrics
      #   protocol: TCP
      #   port: 8502
      #   targetPort: metrics
      type: ClusterIP
    

#### 6.2.4 `models/image-classification-resnet50/kubernetes/hpa.yaml`
-   **Specification:**
    yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: resnet50-tfserving-hpa
      namespace: creativeflow-ai-serving
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: resnet50-tfserving
      minReplicas: 1
      maxReplicas: 5 # Adjust based on capacity and cost
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      # To scale based on GPU, a custom metrics setup is usually needed.
      # Example with custom metric (requires prometheus-adapter & DCGM exporter):
      # - type: Pods # Or External if metric is cluster-wide
      #   pods:
      #     metric:
      #       name: nvidia_gpu_utilization_percentage # Hypothetical custom metric name
      #     target:
      #       type: AverageValue
      #       averageValue: "75" # Target 75% GPU utilization
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
          - type: Percent
            value: 100
            periodSeconds: 60
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
          - type: Percent
            value: 100
            periodSeconds: 15
          - type: Pods
            value: 2 # Add up to 2 pods at a time
            periodSeconds: 15
          selectPolicy: Max
    

#### 6.2.5 `models/image-classification-resnet50/kubernetes/configmap-tfserving.yaml` (Optional)
-   **Purpose:** If models are configured via a `models.config` file passed to TensorFlow Serving.
-   **Specification:**
    yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: resnet50-tfserving-config
      namespace: creativeflow-ai-serving
    data:
      models.config: |
        model_config_list: {
          config: {
            name: "resnet50",
            base_path: "/models/resnet50", # Path inside the container where model files are
            model_platform: "tensorflow"
          }
          # Add other models here if served by the same TF Serving instance
        }
    

### 6.3 Text Generation: GPT-2 via Triton Inference Server

#### 6.3.1 `models/text-generation-gpt2/docker/Dockerfile`
-   **Purpose:** Package GPT-2 model artifacts for Triton Inference Server.
-   **Specification:**
    dockerfile
    # Use the CreativeFlow AI base image for Triton
    ARG CREATIVEFLOW_TRITON_BASE_IMAGE_TAG=latest
    FROM creativeflow/triton-inference-server-base:${CREATIVEFLOW_TRITON_BASE_IMAGE_TAG}
    # Alternatively, use an official Triton image directly:
    # ARG TRITON_SERVER_VERSION=24.05-py3
    # FROM nvcr.io/nvidia/tritonserver:${TRITON_SERVER_VERSION}

    LABEL model.name="gpt2"
    LABEL model.framework="pytorch" # Or onnx, depending on gpt2 artifact
    LABEL model.task="text-generation"

    # Copy the structured model repository for GPT-2
    # Assumes ../model_repository/gpt2/ (containing config.pbtxt and 1/model.pt or model.onnx)
    COPY ../model_repository/gpt2 ${MODEL_REPOSITORY_PATH}/gpt2

    # Base image CMD ["tritonserver", "--model-repository=/models"] should suffice.
    # No specific CMD override needed if models are in /models.
    

#### 6.3.2 `models/text-generation-gpt2/model_repository/gpt2/config.pbtxt`
-   **Purpose:** Triton model configuration for GPT-2.
-   **Specification:** (Example assuming PyTorch backend for a Hugging Face GPT-2 model converted to TorchScript)
    pbtxt
    name: "gpt2"
    platform: "pytorch_libtorch" # Or "onnxruntime_onnx" if ONNX model
    max_batch_size: 8 # Example, tune based on model and GPU memory

    input [
      {
        name: "INPUT__0" # Placeholder, match actual model input tensor name
        data_type: TYPE_INT64
        dims: [ -1, -1 ] # Batch size, sequence length (variable)
      },
      {
        name: "INPUT__1" # Placeholder for attention_mask
        data_type: TYPE_INT64
        dims: [ -1, -1 ]
      }
    ]
    output [
      {
        name: "OUTPUT__0" # Placeholder, match actual model output tensor name
        data_type: TYPE_FP32 # Or appropriate type
        dims: [ -1, -1, -1 ] # Batch size, sequence length, vocab size
      }
    ]

    instance_group [
      {
        kind: KIND_GPU
        count: 1 # Number of model instances per GPU
        gpus: [0] # Assign to specific GPU, or let Triton manage
      }
    ]

    # Optional: Dynamic batching configuration
    # dynamic_batching {
    #   preferred_batch_size: [ 4, 8 ]
    #   max_queue_delay_microseconds: 100
    # }
    
    **Note:** The `INPUT__*` and `OUTPUT__*` names, `data_type`, and `dims` must precisely match the exported model's signature.

#### 6.3.3 `models/text-generation-gpt2/model_repository/gpt2/1/model.py` (if Python backend)
-   **Purpose:** Python backend script for Triton if GPT-2 uses custom logic not directly supported by standard backends.
-   **Specification:** (Conceptual, actual implementation highly dependent on the model export and desired logic)
    python
    import triton_python_backend_utils as pb_utils
    import torch
    # from transformers import GPT2Tokenizer, GPT2LMHeadModel # Example
    import json
    import numpy as np

    class TritonPythonModel:
        def initialize(self, args):
            self.model_config = json.loads(args['model_config'])
            # output0_config = pb_utils.get_output_config_by_name(self.model_config, "OUTPUT__0")
            # self.output_dtype = pb_utils.triton_string_to_numpy(output0_config['data_type'])
            
            # device = "cuda" if args['model_instance_kind'] == 'GPU' else "cpu"
            # model_path = "/models/gpt2/1/pytorch_model.bin" # Path to actual model artifact
            # self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2") # Or path to local tokenizer
            # self.model = GPT2LMHeadModel.from_pretrained("gpt2").to(device) # Or load from model_path
            # self.tokenizer.pad_token = self.tokenizer.eos_token # Example for padding
            print('GPT-2 Python backend initialized...')

        def execute(self, requests):
            responses = []
            # for request in requests:
                # # Get input tensors
                # input_ids_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT__0")
                # attention_mask_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT__1")
                
                # input_ids = input_ids_tensor.as_numpy()
                # attention_mask = attention_mask_tensor.as_numpy()
                
                # # Perform inference
                # with torch.no_grad():
                #     outputs = self.model(input_ids=torch.tensor(input_ids).cuda(), 
                #                          attention_mask=torch.tensor(attention_mask).cuda())
                #     logits = outputs.logits.cpu().numpy()

                # # Create output tensor
                # output_tensor = pb_utils.Tensor("OUTPUT__0", logits.astype(self.output_dtype))
                # inference_response = pb_utils.InferenceResponse(output_tensors=[output_tensor])
                # responses.append(inference_response)
            
            # Placeholder response if not fully implemented
            for request in requests:
                dummy_output = np.array([[[1.0]]], dtype=np.float32) # Match expected output dims/type
                output_tensor = pb_utils.Tensor("OUTPUT__0", dummy_output)
                inference_response = pb_utils.InferenceResponse(output_tensors=[output_tensor])
                responses.append(inference_response)
            return responses

        def finalize(self):
            print('GPT-2 Python backend cleaning up...')
    
    **Note:** This is a simplified placeholder. Actual model files (e.g., `pytorch_model.bin`, `model.onnx`) would reside in the `models/text-generation-gpt2/model_repository/gpt2/1/` directory.

#### 6.3.4 Kubernetes Manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`)
-   These will be similar in structure to the ResNet50 manifests, but with:
    -   `metadata.name` and `app` labels changed to `gpt2-triton`.
    -   `runtime` label set to `triton-inference-server`.
    -   `image` pointing to `your-private-registry/creativeflow/gpt2-triton:latest`.
    -   Container ports for Triton: `8000` (http), `8001` (grpc), `8002` (metrics).
    -   Readiness/Liveness probes targeting Triton's health endpoints (e.g., `/v2/health/ready` on port 8000).
    -   HPA metrics might target CPU, GPU, or Triton-specific metrics if available and configured (e.g., `nv_inference_queue_duration_us`).

### 6.4 Custom Object Detection: YOLO via Custom Python FastAPI

#### 6.4.1 `models/custom-object-detector-yolo/docker/Dockerfile`
-   **Purpose:** Package YOLO model and its specific serving logic.
-   **Specification:**
    dockerfile
    # Use the CreativeFlow AI base image for custom Python FastAPI servers
    ARG CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG=latest
    FROM creativeflow/custom-python-fastapi-base:${CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG}

    LABEL model.name="yolo-custom"
    LABEL model.framework="pytorch" # Assuming YOLOv5/v8 PyTorch based
    LABEL model.task="object-detection"

    # Copy model-specific source code (overriding/extending base src)
    COPY ./models/custom-object-detector-yolo/docker/src /app/src
    
    # Copy model weights
    # Assume weights are in ../model_weights/yolovX.pt
    COPY ./models/custom-object-detector-yolo/model_weights /app/model_weights

    # Install model-specific requirements
    COPY ./models/custom-object-detector-yolo/docker/requirements.txt /app/requirements_model.txt
    RUN pip install --no-cache-dir -r requirements_model.txt

    # Set environment variable for model path, can be overridden in K8s Deployment
    ENV MODEL_PATH=/app/model_weights/yolov5s.pt # Example path

    # The base image CMD might be sufficient if src/main.py is structured correctly.
    # If specific startup logic is needed for YOLO:
    # CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
    

#### 6.4.2 `models/custom-object-detector-yolo/docker/requirements.txt`
-   **Purpose:** Python dependencies specific to the YOLO model.
-   **Specification:**
    txt
    # Example for YOLOv5, adjust for actual YOLO version/flavor
    torch>=1.10.0,<2.3.0
    torchvision>=0.11.0,<0.18.0
    ultralytics>=8.0.0,<8.2.0 # If using YOLOv8/Ultralytics framework
    # Or specific YOLOv5 requirements:
    # yolov5>=7.0.0 
    opencv-python-headless>=4.5.0,<4.10.0
    Pillow>=9.0.0,<10.4.0
    numpy>=1.20.0,<1.27.0
    # Add any other specific dependencies for this model
    

#### 6.4.3 `models/custom-object-detector-yolo/docker/src/model_handler.py`
-   **Purpose:** Contains YOLO-specific model loading, pre/post-processing logic.
-   **Specification:**
    python
    import torch
    import os
    from PIL import Image
    import io
    import numpy as np
    # from ultralytics import YOLO # For YOLOv8
    # For YOLOv5, typically torch.hub.load is used

    class YOLOModelHandler:
        def __init__(self, model_path: str, confidence_threshold: float = 0.25):
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"YOLO Handler: Using device: {self.device}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model weights not found at {model_path}")
            
            # Example for YOLOv5 (adjust if using Ultralytics YOLO class or other versions)
            try:
                self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False) 
                # Or if it's a local .pt file directly:
                # self.model = torch.hub.load('.', 'custom', path=model_path, source='local')
                self.model.to(self.device)
                self.model.eval()
                self.confidence_threshold = confidence_threshold
                print(f"YOLO model loaded successfully from {model_path}")
            except Exception as e:
                print(f"Error loading YOLO model: {e}")
                raise

        def _preprocess_image(self, image_bytes: bytes) -> Image.Image:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            return image

        def _postprocess_detections(self, results) -> list:
            # Process results from model.xyxy[0] or results.pandas().xyxy[0] for YOLOv5
            # For Ultralytics YOLO: results is a list of Results objects
            detections = []
            # Example for YOLOv5 results (results.xyxy[0] is a tensor)
            if hasattr(results, 'xyxy') and len(results.xyxy) > 0:
                for det in results.xyxy[0].cpu().numpy(): # x1, y1, x2, y2, conf, class_idx
                    if det[4] >= self.confidence_threshold:
                        detections.append({
                            "xmin": float(det[0]),
                            "ymin": float(det[1]),
                            "xmax": float(det[2]),
                            "ymax": float(det[3]),
                            "confidence": float(det[4]),
                            "class_id": int(det[5]),
                            "class_name": self.model.names[int(det[5])]
                        })
            # Adapt for Ultralytics YOLO results if using that directly
            # elif isinstance(results, list) and len(results) > 0 and hasattr(results[0], 'boxes'): # Ultralytics YOLO
            #     for res in results:
            #         for box in res.boxes:
            #             if box.conf.item() >= self.confidence_threshold:
            #                 coords = box.xyxy[0].tolist()
            #                 detections.append({
            #                     "xmin": coords[0],
            #                     "ymin": coords[1],
            #                     "xmax": coords[2],
            #                     "ymax": coords[3],
            #                     "confidence": box.conf.item(),
            #                     "class_id": int(box.cls.item()),
            #                     "class_name": self.model.names[int(box.cls.item())]
            #                 })
            return detections

        def predict(self, image_bytes: bytes) -> list:
            pil_image = self._preprocess_image(image_bytes)
            with torch.no_grad():
                results = self.model(pil_image, size=640) # Example size, can be configurable
            
            processed_results = self._postprocess_detections(results)
            return processed_results
    

#### 6.4.4 `models/custom-object-detector-yolo/docker/src/main.py`
-   **Purpose:** FastAPI application specialized for the YOLO model.
-   **Specification:**
    python
    from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
    from fastapi.responses import JSONResponse
    import os
    from typing import List, Dict
    from .model_handler import YOLOModelHandler # Import the YOLO specific handler
    from pydantic import BaseModel
    from prometheus_client import Counter, Histogram, make_asgi_app

    # Metrics
    REQUEST_COUNT = Counter("yolo_server_requests_total", "Total count of YOLO requests.", ["method", "endpoint", "http_status"])
    REQUEST_LATENCY = Histogram("yolo_server_request_latency_seconds", "Histogram of YOLO request latencies.", ["method", "endpoint"])
    DETECTION_COUNT = Counter("yolo_detections_total", "Total number of objects detected.", ["class_name"])

    app = FastAPI(
        title="CreativeFlow YOLO Object Detector",
        description="Serves a custom YOLO model for object detection.",
        version="1.0.0"
    )

    # Add Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    yolo_handler_instance: YOLOModelHandler = None

    @app.on_event("startup")
    async def startup_event():
        global yolo_handler_instance
        model_path = os.getenv("MODEL_PATH", "/app/model_weights/yolov5s.pt") # Default path
        confidence_str = os.getenv("CONFIDENCE_THRESHOLD", "0.25")
        try:
            confidence_threshold = float(confidence_str)
        except ValueError:
            print(f"Warning: Invalid CONFIDENCE_THRESHOLD '{confidence_str}', using default 0.25.")
            confidence_threshold = 0.25
            
        try:
            yolo_handler_instance = YOLOModelHandler(model_path=model_path, confidence_threshold=confidence_threshold)
            print("YOLO Model Handler initialized successfully.")
        except Exception as e:
            print(f"Error initializing YOLO Model Handler: {e}")
            # Allow app to start but /predict will fail until resolved.
            # Or, raise to prevent startup: raise RuntimeError(f"Failed to initialize YOLOModelHandler: {e}")
            yolo_handler_instance = None


    class Detection(BaseModel):
        xmin: float
        ymin: float
        xmax: float
        ymax: float
        confidence: float
        class_id: int
        class_name: str

    class PredictionResponse(BaseModel):
        detections: List[Detection]
        image_filename: Optional[str] = None

    @app.post("/v1/predict", response_model=PredictionResponse, summary="Detect Objects in Image", tags=["Object Detection"])
    async def predict_yolo_objects(file: UploadFile = File(...)):
        """
        Accepts an image file, performs object detection using YOLO,
        and returns a list of detected objects with their bounding boxes,
        confidence scores, and class names.
        """
        if yolo_handler_instance is None:
            REQUEST_COUNT.labels(method="POST", endpoint="/v1/predict", http_status=503).inc()
            raise HTTPException(status_code=503, detail="Model not available or failed to load.")

        image_bytes = await file.read()
        if not image_bytes:
            REQUEST_COUNT.labels(method="POST", endpoint="/v1/predict", http_status=400).inc()
            raise HTTPException(status_code=400, detail="No image file provided.")

        with REQUEST_LATENCY.labels(method="POST", endpoint="/v1/predict").time():
            try:
                detections_data = yolo_handler_instance.predict(image_bytes)
                for det in detections_data:
                    DETECTION_COUNT.labels(class_name=det.get("class_name", "unknown")).inc()
                REQUEST_COUNT.labels(method="POST", endpoint="/v1/predict", http_status=200).inc()
                return PredictionResponse(detections=detections_data, image_filename=file.filename)
            except Exception as e:
                print(f"Error during YOLO prediction: {e}")
                REQUEST_COUNT.labels(method="POST", endpoint="/v1/predict", http_status=500).inc()
                raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    @app.get("/health", summary="Health Check", tags=["System"])
    async def health_check():
        """
        Performs a health check of the application.
        Returns HTTP 200 if the application is healthy.
        """
        if yolo_handler_instance is None:
            return JSONResponse(content={"status": "unhealthy", "detail": "Model handler not initialized"}, status_code=503)
        REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
        return JSONResponse(content={"status": "healthy"})

    

#### 6.4.5 Kubernetes Manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`)
-   These will be similar in structure to the ResNet50/GPT-2 manifests, but with:
    -   `metadata.name` and `app` labels changed to `yolo-custom-fastapi`.
    -   `runtime` label set to `custom-fastapi`.
    -   `image` pointing to `your-private-registry/creativeflow/yolo-custom-fastapi:latest`.
    -   Container port `8000` (http) and optionally a separate metrics port if FastAPI default /metrics is not used or is on a different port.
    -   Environment variable `MODEL_PATH` (e.g., `/app/model_weights/yolovX.pt`) and `CONFIDENCE_THRESHOLD` can be set in the Deployment spec.
    -   Readiness/Liveness probes targeting the `/health` endpoint on port 8000.
    -   HPA metrics might target CPU, GPU utilization, or custom FastAPI metrics (e.g., requests per second via `prometheus_client`).

## 7. GPU Resource Management
-   The NVIDIA GPU Operator must be installed and configured on the Kubernetes cluster (responsibility of `REPO-INFRA-CORE-001`). This allows Kubernetes to schedule pods on GPU nodes and expose GPU resources to containers.
-   All model serving `Deployment` manifests must explicitly request GPU resources:
    yaml
    resources:
      limits:
        nvidia.com/gpu: 1 # Number of GPUs per pod
      requests:
        nvidia.com/gpu: 1
    
-   The number of GPUs requested (`1` in the example) should match the model's requirements and instance group configurations (e.g., in Triton's `config.pbtxt`).
-   Multi-Instance GPU (MIG) can be leveraged if the underlying NVIDIA GPUs (e.g., A100, H100 series) and the GPU Operator version support it. This allows a single physical GPU to be partitioned into multiple smaller, isolated GPU instances, which can be assigned to different pods. This decision and configuration would be part of the MLOps deployment strategy based on model size and concurrency needs (INT-007). Configuration would involve creating MIG profiles on nodes and requesting specific MIG device types in pod specs.
-   GPU time-slicing (older mechanism, less isolation than MIG) might be considered for certain workloads if MIG is not available/suitable, but generally MIG is preferred for newer hardware.

## 8. Configuration and Environment Variables
-   **Model Paths & Names:** For models baked into Docker images, paths are typically fixed. For models loaded from shared volumes or ConfigMaps, paths are specified in the server's configuration (e.g., TF Serving `models.config`, Triton's `--model-repository` flag) or via environment variables.
    -   Example for custom FastAPI: `ENV MODEL_PATH=/app/model_weights/yolov5s.pt` in Dockerfile, overridable in K8s Deployment.
-   **Serving Runtime Flags:** Passed as arguments in the `CMD` or `args` section of the container spec in Kubernetes `Deployment`s.
    -   e.g., `"--model_name=${MODEL_NAME}"`, `"--model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}"` for TF Serving.
    -   e.g., `"--model-repository=/models"`, `"--strict-model-config=false"` for Triton.
-   **Log Levels:** Configured via environment variables for custom Python servers (e.g., `LOG_LEVEL=INFO`). Serving runtimes like Triton and TF Serving also have their own logging verbosity flags.
-   **GPU Allocation:** Managed via `resources.limits` and `resources.requests` for `nvidia.com/gpu`.
-   **Kubernetes ConfigMaps:** Used for non-sensitive configuration files like TensorFlow Serving's `models.config` or custom application settings. These are mounted as volumes into pods.
-   **Kubernetes Secrets:** While not directly configured in this repository's *example* model files, if model servers needed to access secure resources (e.g., a private model registry, authenticated data sources), Kubernetes Secrets would be used and mounted as volumes or environment variables. Secrets management is a broader platform concern (HashiCorp Vault, etc.).

## 9. Logging and Monitoring
-   **Logging:**
    -   All model serving containers (TF Serving, Triton, Custom Python) should log to `stdout` and `stderr`.
    -   The cluster's log aggregation solution (e.g., ELK/Loki via Filebeat/Fluentd, managed by `REPO-MONITORING-001`) will collect these logs.
    -   Custom Python (FastAPI) servers will use standard Python logging, configured to output structured JSON logs if possible, including correlation IDs.
-   **Monitoring:**
    -   **NVIDIA DCGM Exporter:** Assumed to be deployed on GPU nodes (by `REPO-INFRA-CORE-001` or `REPO-MONITORING-001`) to expose detailed GPU metrics (utilization, memory, temperature) to Prometheus.
    -   **Triton Inference Server:** Exposes Prometheus metrics on port `8002` by default (e.g., `nv_inference_request_success`, `nv_inference_queue_duration_us`, `nv_gpu_utilization`).
    -   **TensorFlow Serving:** Metrics exposure depends on version and configuration. Newer versions might expose Prometheus metrics or require a sidecar exporter.
    -   **Custom Python FastAPI Servers:** Will use `prometheus_client` library to define and expose custom metrics (request counts, latencies, prediction counts, model-specific metrics) on a `/metrics` endpoint (e.g., port 8000 or a separate metrics port).
    -   The `base/monitoring/model-server-servicemonitor.yaml` provides the template for Prometheus to scrape these metrics endpoints based on service labels.

## 10. Security Considerations
-   **RBAC:** Implemented as per section 4.2 to ensure model serving pods run with least privilege.
-   **Network Policies:** (Cluster-level responsibility) Ingress and egress network policies should be defined for the `creativeflow-ai-serving` namespace to restrict traffic flow to only authorized sources and destinations. Model inference endpoints should generally only be accessible from within the cluster (e.g., by API Gateway, n8n).
-   **Container Image Security:**
    -   Base images are from trusted, official sources (TensorFlow, NVIDIA, Python).
    -   Specific model Dockerfiles should minimize added layers and RUN commands.
    -   Vulnerability scanning of images is expected as part of the MLOps CI/CD pipeline before deployment.
-   **GPU Security:** NVIDIA GPU Operator helps manage secure access to GPU devices.
-   **Input/Output Sanitization:** For custom model servers, any input directly from users (though typically proxied by n8n/API Gateway) should be validated. Outputs should be checked if they could contain sensitive information or executable content (though model outputs are usually structured data/predictions). Content safety checks (REQ-3-015) are primarily handled by n8n or a dedicated service before user exposure.
-   **Resource Quotas and LimitRanges:** Can be defined at the namespace level in Kubernetes to prevent AI workloads from consuming excessive cluster resources, though HPA helps manage scaling.

## 11. Deployment Strategy for this Repository's Artifacts
The artifacts in this repository (Kubernetes YAML, Dockerfiles) define the *platform capabilities and patterns* for serving AI models.
-   **Base Configurations (`base/`):** Applied once to the Kubernetes cluster to set up the namespace, RBAC, and base monitoring. This can be done using `kubectl apply -f base/namespaces/ai-serving-namespace.yaml`, etc., or via Kustomize/Helm by `REPO-INFRA-CORE-001`.
-   **Runtime Base Images (`runtime-bases/`):**
    -   Dockerfiles are built and pushed to the private container registry by a CI/CD pipeline (managed by `REPO-DEVOPS-CICD-001`).
    -   These images are tagged (e.g., `creativeflow/tensorflow-serving-base:latest`, `creativeflow/triton-inference-server-base:v24.05`).
-   **Example Model Deployments (`models/`):**
    -   These serve as templates or starting points.
    -   **For actual model deployments:** The MLOps Platform Service (`REPO-AISIML-MLOPS-001`) will be responsible for:
        1.  Taking a validated model artifact (from Model Registry).
        2.  Packaging it into a Docker image, likely using a Dockerfile derived from the `runtime-bases` or these examples.
        3.  Generating or customizing Kubernetes manifests (Deployment, Service, HPA, ConfigMaps) based on these examples and the specific model's requirements (e.g., model name, resource needs, configuration).
        4.  Deploying these manifests to the `creativeflow-ai-serving` namespace in the Kubernetes cluster.
    -   This repository's example model Dockerfiles can be built and pushed to the registry as part of CI for validation of the base runtimes.
    -   The Kubernetes manifests for example models can be applied to a development/staging cluster for testing the patterns, e.g., using `kubectl apply -k models/image-classification-resnet50/kubernetes/`.

Deployment tools like Kustomize or Helm are recommended for managing the application of Kubernetes manifests, allowing for environment-specific overlays and parameterization. This repository could provide Kustomization files for its base components and example models.

# Example Kustomization structure (conceptual for applying base)
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: creativeflow-ai-serving # Default namespace for resources in this kustomization
resources:
  - namespaces/ai-serving-namespace.yaml # Note: Namespace itself isn't namespaced
  - rbac/service-account.yaml
  - rbac/role.yaml
  - rbac/role-binding.yaml
  - monitoring/model-server-servicemonitor.yaml

# Then apply with: kubectl apply -k base/


This approach ensures that the `CreativeFlow.K8sAIServingPlatform` repository provides the foundational elements and standardized patterns, while the MLOps service handles the dynamic deployment and management of specific AI models based on these foundations.

markdown
# Software Design Specification: CreativeFlow.K8sAIServingPlatform

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.K8sAIServingPlatform` repository. This platform is responsible for deploying, managing, and scaling AI models on a GPU-accelerated Kubernetes cluster. It serves as the core execution environment for custom and third-party AI models used within the CreativeFlow AI ecosystem. The specifications herein will guide the development of Kubernetes manifests, Docker images, and configurations required for the AI model serving runtimes.

### 1.2 Scope
The scope of this repository includes:
-   Base Kubernetes configurations for the AI serving namespace, Role-Based Access Control (RBAC), and monitoring.
-   Standardized Docker base images for common AI model serving runtimes: TensorFlow Serving, NVIDIA Triton Inference Server, and a custom Python (FastAPI) server.
-   Example Kubernetes deployment patterns for various types of AI models, demonstrating GPU resource allocation, scaling, service exposure, and configuration.
-   Configuration files for model servers (e.g., Triton `config.pbtxt`).
-   Source code for any custom Python model serving wrappers or handlers.

This repository provides the *environment and patterns* for serving AI models. The actual deployment lifecycle (uploading new models, promoting versions) will be managed by the MLOps Platform Service (`REPO-AISIML-MLOPS-001`, see requirements AISIML-006 to AISIML-013). Inference requests are typically orchestrated by the n8n Workflow Engine (`REPO-WORKFLOW-N8N-001`).

### 1.3 Definitions, Acronyms, and Abbreviations
-   **AI:** Artificial Intelligence
-   **API:** Application Programming Interface
-   **CI/CD:** Continuous Integration/Continuous Deployment
-   **CPU:** Central Processing Unit
-   **CRD:** Custom Resource Definition (Kubernetes)
-   **GPU:** Graphics Processing Unit
-   **HPA:** Horizontal Pod Autoscaler (Kubernetes)
-   **IaC:** Infrastructure as Code
-   **K8s:** Kubernetes
-   **MIG:** Multi-Instance GPU (NVIDIA)
-   **ML:** Machine Learning
-   **MLOps:** Machine Learning Operations
-   **NFR:** Non-Functional Requirement
-   **ONNX:** Open Neural Network Exchange
-   **PWA:** Progressive Web Application
-   **RBAC:** Role-Based Access Control
-   **SDS:** Software Design Specification
-   **SRS:** Software Requirements Specification
-   **TF Serving:** TensorFlow Serving
-   **YAML:** YAML Ain't Markup Language

## 2. System Overview
The K8s AI Serving Platform is a critical backend component within the CreativeFlow AI architecture. It leverages Kubernetes to orchestrate containerized AI models on GPU-enabled nodes, providing scalable and resilient inference endpoints. This platform adheres to requirements specified in SRS Sections 2.4 (AI Processing operating environment), 5.1 (GPU Cluster), and 5.2.2 (AI Processing Orchestration on Kubernetes).

It interacts with:
-   **MLOps Platform Service (`REPO-AISIML-MLOPS-001`):** This service manages the lifecycle of custom AI models, including deploying them to this K8s platform (INT-007).
-   **n8n Workflow Engine (`REPO-WORKFLOW-N8N-001`):** n8n workflows will invoke the AI models served by this platform to perform creative generation tasks.
-   **Monitoring Stack (Prometheus, Grafana):** Model serving instances will expose metrics for monitoring performance and health (DEP-001 implies monitoring).

The platform is designed to support various model types and serving runtimes (INT-007), ensuring flexibility and extensibility. It will be built to handle scalable GPU orchestration for high throughput (NFR-002) on the infrastructure specified in DEP-001.

## 3. Design Considerations

### 3.1 Technology Stack
-   **Orchestration:** Kubernetes (v1.29.2 or later, e.g., K3s, RKE2, or full K8s)
-   **Containerization:** Docker (Engine v26.0.0 or later)
-   **GPU Management:** NVIDIA GPU Operator (v23.9.2 or later), NVIDIA CUDA Toolkit (v12.3 or later), NVIDIA cuDNN (v8.9.7 or later)
-   **Model Serving Runtimes:**
    -   TensorFlow Serving (v2.15.0 or later)
    -   NVIDIA Triton Inference Server (v24.05.0 or later)
    -   Custom Python Server: Python (v3.12.2 or later), FastAPI, Uvicorn
-   **Configuration:** YAML (for Kubernetes manifests), Dockerfile
-   **Language (for custom servers/wrappers):** Python (v3.12.2 or later)

### 3.2 Modularity
-   **Base Runtime Images:** Common Docker configurations for TensorFlow Serving, Triton, and Custom Python (FastAPI) will be provided as reusable base images.
-   **Model-Specific Deployments:** Each AI model or model type will have its dedicated set of Kubernetes manifests and potentially a specialized Docker image inheriting from a base runtime. This allows for independent configuration and resource allocation.

### 3.3 Scalability (NFR-002)
-   **Horizontal Pod Autoscaling (HPA):** Kubernetes HPA will be configured for model deployments to automatically scale the number of serving pods based on CPU utilization, GPU utilization (via custom metrics adapter if needed), or other relevant metrics.
-   **Cluster Autoscaler:** The underlying K8s cluster is expected to support node scaling to add more GPU nodes if pod scaling demands it.

### 3.4 Configuration Management
-   All Kubernetes resources will be defined declaratively using YAML manifests.
-   Docker images will be built using version-controlled Dockerfiles.
-   Externalized configuration for model servers will be managed via Kubernetes ConfigMaps or environment variables.

### 3.5 Security
-   **RBAC:** Kubernetes RBAC will be used to grant least-privilege permissions to model serving pods.
-   **GPU Resource Isolation:** The NVIDIA GPU Operator helps manage and isolate GPU resources.
-   **Network Policies:** Network policies should restrict communication to and from model serving pods.
-   **Container Image Security:** Base images from trusted sources; vulnerability scanning is external.

### 3.6 Monitoring (DEP-001 implies monitoring)
-   Model serving runtimes will expose Prometheus-compatible metrics.
-   Kubernetes `ServiceMonitor` Custom Resources will enable Prometheus scraping.
-   Logs from pods will be streamed to `stdout`/`stderr` for centralized collection.

## 4. Kubernetes Platform Base Configuration

### 4.1 Namespace
-   **File:** `base/namespaces/ai-serving-namespace.yaml`
-   **Purpose:** Create `creativeflow-ai-serving` namespace for resource isolation (Section 5.2.2).
-   **Specification:**
    yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: creativeflow-ai-serving
        app.kubernetes.io/part-of: creativeflow-platform
    

### 4.2 Role-Based Access Control (RBAC)

#### 4.2.1 ServiceAccount
-   **File:** `base/rbac/service-account.yaml`
-   **Purpose:** Define `ai-model-server-sa` for model serving pods (Section 5.2.2).
-   **Specification:**
    yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: ai-model-server-sa
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-sa
    

#### 4.2.2 Role
-   **File:** `base/rbac/role.yaml`
-   **Purpose:** Define `ai-model-server-role` with minimal necessary permissions (Section 5.2.2).
-   **Specification:**
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: ai-model-server-role
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-role
    rules:
    - apiGroups: [""] 
      resources: ["configmaps", "secrets"] 
      verbs: ["get", "watch", "list"]
    - apiGroups: [""]
      resources: ["pods", "services"] 
      verbs: ["get", "list"]
    

#### 4.2.3 RoleBinding
-   **File:** `base/rbac/role-binding.yaml`
-   **Purpose:** Bind `ai-model-server-role` to `ai-model-server-sa` (Section 5.2.2).
-   **Specification:**
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: ai-model-server-rb
      namespace: creativeflow-ai-serving
      labels:
        app.kubernetes.io/name: ai-model-server-rb
    subjects:
    - kind: ServiceAccount
      name: ai-model-server-sa
      namespace: creativeflow-ai-serving
    roleRef:
      kind: Role
      name: ai-model-server-role
      apiGroup: rbac.authorization.k8s.io
    

### 4.3 Monitoring Configuration

#### 4.3.1 ServiceMonitor
-   **File:** `base/monitoring/model-server-servicemonitor.yaml`
-   **Purpose:** Configure Prometheus to scrape metrics from AI model serving Services (DEP-001).
-   **Specification:**
    yaml
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: model-server-servicemonitor
      namespace: creativeflow-ai-serving # Or Prometheus Operator's namespace
      labels:
        app.kubernetes.io/name: model-server-servicemonitor
        # release: prometheus # Example label for discovery
    spec:
      namespaceSelector:
        matchNames:
        - creativeflow-ai-serving
      selector:
        matchLabels:
          creativeflow.ai/scrape-metrics: "true"
      endpoints:
      - port: metrics 
        interval: 30s
        path: /metrics
      - port: http-metrics # For Triton default metrics port
        interval: 30s
        path: /metrics
        honorLabels: true # If Triton uses different job labels
    

## 5. Runtime Base Images Design (INT-007)

### 5.1 TensorFlow Serving Base
-   **File:** `runtime-bases/tensorflow-serving/Dockerfile`
-   **Purpose:** Base image for serving TensorFlow SavedModel bundles.
-   **Specification:**
    dockerfile
    ARG TENSORFLOW_SERVING_VERSION=2.15.0-gpu # Matches specified tech
    FROM tensorflow/serving:${TENSORFLOW_SERVING_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for TensorFlow Serving with GPU support on CreativeFlow AI."

    EXPOSE 8500 # gRPC
    EXPOSE 8501 # REST

    CMD ["tensorflow_model_server"]
    

### 5.2 NVIDIA Triton Inference Server Base
-   **File:** `runtime-bases/triton-inference-server/Dockerfile`
-   **Purpose:** Base image for NVIDIA Triton Inference Server.
-   **Specification:**
    dockerfile
    ARG TRITON_SERVER_VERSION=24.05-py3 # Matches specified tech
    FROM nvcr.io/nvidia/tritonserver:${TRITON_SERVER_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for NVIDIA Triton Inference Server on CreativeFlow AI."

    ENV MODEL_REPOSITORY_PATH=/models
    RUN mkdir -p ${MODEL_REPOSITORY_PATH}

    EXPOSE 8000 # HTTP
    EXPOSE 8001 # gRPC
    EXPOSE 8002 # Metrics (HTTP)

    CMD ["tritonserver", "--model-repository=${MODEL_REPOSITORY_PATH}"]
    

### 5.3 Custom Python FastAPI Base (INT-007)
Provides a common structure for serving custom Python models.

#### 5.3.1 `runtime-bases/custom-python-fastapi/Dockerfile`
-   **Specification:**
    dockerfile
    ARG PYTHON_VERSION=3.12.2-slim 
    FROM python:${PYTHON_VERSION}

    LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
    LABEL description="Base image for custom Python AI models served with FastAPI on CreativeFlow AI."

    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    ENV APP_MODULE="src.main:app" # Default app module

    WORKDIR /app

    COPY ./runtime-bases/custom-python-fastapi/requirements.txt /app/requirements_base.txt
    RUN pip install --no-cache-dir -r requirements_base.txt

    COPY ./runtime-bases/custom-python-fastapi/src /app/src

    EXPOSE 8000

    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
    

#### 5.3.2 `runtime-bases/custom-python-fastapi/requirements.txt`
-   **Specification:**
    txt
    fastapi>=0.110.0,<0.112.0 # Updated for Python 3.12
    uvicorn[standard]>=0.27.0,<0.30.0
    pydantic>=2.5.0,<2.8.0
    python-dotenv>=1.0.0,<1.1.0
    prometheus_client>=0.17.0,<0.21.0
    

#### 5.3.3 `runtime-bases/custom-python-fastapi/src/main.py`
-   **Purpose:** Initializes FastAPI app, includes health check and Prometheus metrics endpoint.
-   **Specification:**
    python
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from prometheus_client import Counter, Histogram, make_asgi_app, REGISTRY
    # Unregister default collectors to avoid duplicate metrics if running multiple workers in future
    # or if platform-level node_exporter provides them. For simplicity, keep for now.
    # from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
    # REGISTRY.unregister(PROCESS_COLLECTOR)
    # REGISTRY.unregister(PLATFORM_COLLECTOR)
    # REGISTRY.unregister(REGISTRY._default_collector)


    REQUEST_COUNT = Counter(
        "custom_server_requests_total",
        "Total count of requests.",
        ["method", "endpoint", "http_status"]
    )
    REQUEST_LATENCY = Histogram(
        "custom_server_request_latency_seconds",
        "Histogram of request latencies.",
        ["method", "endpoint"]
    )

    app = FastAPI(
        title="CreativeFlow Custom AI Model Server - Base",
        description="Base FastAPI application for serving custom AI models.",
        version="0.1.0"
    )

    # Mount Prometheus ASGI app on /metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    @app.on_event("startup")
    async def startup_event():
        print("Base FastAPI application startup complete.")
        # Placeholder for global model loading if needed by base,
        # but typically model-specific handlers do this.

    @app.get("/health", summary="Health Check", tags=["System"])
    async def health_check():
        REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
        return JSONResponse(content={"status": "healthy"})

    # Specific model routers will be included by specialized main.py files
    # For example:
    # from .routers import specific_model_router
    # app.include_router(specific_model_router, prefix="/v1/models/specific_model")
    

#### 5.3.4 `runtime-bases/custom-python-fastapi/src/dependencies.py`
-   **Purpose:** Generic dependency utilities. Model loading should be handled by specific model handlers.
-   **Specification:**
    python
    # This file can contain shared utility functions or dependency injectors
    # if needed across multiple custom model server types.
    # For now, it can be minimal or empty as model loading is model-specific.

    def get_example_dependency():
        return {"message": "This is an example dependency from base."}
    

#### 5.3.5 `runtime-bases/custom-python-fastapi/src/routers/predict.py`
-   **Note:** This is a placeholder. Actual prediction routers will be highly model-specific and defined within each model's `src` directory.

#### 5.3.6 `runtime-bases/custom-python-fastapi/src/models/inference.py`
-   **Purpose:** Base Pydantic models for generic request/response structures.
-   **Specification:**
    python
    from pydantic import BaseModel
    from typing import List, Any, Optional, Dict

    class BaseInferenceRequest(BaseModel):
        request_id: Optional[str] = None
        # Common input fields can be added here if applicable across many custom models
        # e.g. metadata: Optional[Dict[str, Any]] = None
        pass

    class BaseInferenceResponse(BaseModel):
        request_id: Optional[str] = None
        model_name: Optional[str] = None
        model_version: Optional[str] = None
        # Common output fields
        # e.g. processing_time_ms: Optional[float] = None
        pass
    

## 6. Example AI Model Deployment Design (INT-007)

### 6.1 Image Classification: ResNet50 (TensorFlow Serving)
Illustrates deploying a TensorFlow SavedModel.

#### 6.1.1 `models/image-classification-resnet50/docker/Dockerfile`
-   **Specification:**
    dockerfile
    ARG CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG=latest
    FROM creativeflow/tensorflow-serving-base:${CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG}

    LABEL model.name="resnet50"
    LABEL model.framework="tensorflow"
    LABEL model.task="image-classification"

    ENV MODEL_NAME=resnet50
    ENV MODEL_BASE_PATH=/models 

    RUN mkdir -p ${MODEL_BASE_PATH}/${MODEL_NAME}
    COPY ../model_artifacts/resnet50 ${MODEL_BASE_PATH}/${MODEL_NAME}

    EXPOSE 8500 
    EXPOSE 8501

    # This command assumes model versioning structure like /models/resnet50/1/...
    CMD ["tensorflow_model_server", \
        "--port=8500", \
        "--rest_api_port=8501", \
        "--model_name=${MODEL_NAME}", \
        "--model_base_path=${MODEL_BASE_PATH}" \ 
    ]
    # If specific versions are not in subdirs, use --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}
    # If using models.config:
    # COPY ./models.config /etc/tf_serving/models.config
    # CMD ["tensorflow_model_server", "--model_config_file=/etc/tf_serving/models.config", "--port=8500", "--rest_api_port=8501"]
    
    *Assume `../model_artifacts/resnet50` contains the versioned SavedModel, e.g., `../model_artifacts/resnet50/1/saved_model.pb` and `../model_artifacts/resnet50/1/variables/`.*

#### 6.1.2 `models/image-classification-resnet50/kubernetes/deployment.yaml`
-   **Specification:**
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: resnet50-tfserving
      namespace: creativeflow-ai-serving
      labels:
        app: resnet50-tfserving
        runtime: tensorflow-serving
    spec:
      replicas: 1 
      selector:
        matchLabels:
          app: resnet50-tfserving
      template:
        metadata:
          labels:
            app: resnet50-tfserving
            runtime: tensorflow-serving
            creativeflow.ai/scrape-metrics: "true" # Enable if TF Serving exposes metrics
        spec:
          serviceAccountName: ai-model-server-sa
          containers:
          - name: resnet50-tfserving-container
            image: your-private-registry/creativeflow/resnet50-tfserving:latest # Replace
            imagePullPolicy: IfNotPresent
            ports:
            - containerPort: 8500
              name: grpc
            - containerPort: 8501
              name: http
            # - containerPort: 8502 # If exposing metrics
            #   name: metrics
            resources:
              limits:
                nvidia.com/gpu: 1
              requests:
                nvidia.com/gpu: 1
                cpu: "500m"
                memory: "1Gi"
            readinessProbe:
              httpGet:
                path: "/v1/models/resnet50" 
                port: http
              initialDelaySeconds: 20
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: "/v1/models/resnet50"
                port: http
              initialDelaySeconds: 45
              periodSeconds: 20
              timeoutSeconds: 5
              failureThreshold: 3
            # Example using models.config from a ConfigMap
            # env:
            # - name: MODEL_CONFIG_FILE
            #   value: "/config/models.config"
            # volumeMounts:
            # - name: model-config-volume
            #   mountPath: /config
            #   readOnly: true
          # volumes:
          # - name: model-config-volume
          #   configMap:
          #     name: resnet50-tfserving-config
    

#### 6.1.3 `models/image-classification-resnet50/kubernetes/service.yaml`
-   **Specification:**
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: resnet50-tfserving-service
      namespace: creativeflow-ai-serving
      labels:
        app: resnet50-tfserving
        runtime: tensorflow-serving
        creativeflow.ai/scrape-metrics: "true" # If metrics port exposed
    spec:
      selector:
        app: resnet50-tfserving
      ports:
      - name: grpc
        protocol: TCP
        port: 8500
        targetPort: grpc
      - name: http
        protocol: TCP
        port: 8501 
        targetPort: http
      # - name: metrics
      #   protocol: TCP
      #   port: 8502 # Service port
      #   targetPort: metrics # Pod port name
      type: ClusterIP
    

#### 6.1.4 `models/image-classification-resnet50/kubernetes/hpa.yaml`
-   **Specification:**
    yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: resnet50-tfserving-hpa
      namespace: creativeflow-ai-serving
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: resnet50-tfserving
      minReplicas: 1
      maxReplicas: 3 # Adjust based on expected load and GPU capacity
      metrics:
      - type: Resource
        resource:
          name: cpu 
          target:
            type: Utilization
            averageUtilization: 75 # Target 75% CPU utilization
      # - type: Resource # If GPU metrics are directly available and reliable for scaling TF Serving
      #   resource:
      #     name: nvidia.com/gpu
      #     target:
      #       type: Utilization # This usually refers to GPU *allocation*, not actual utilization
      #       averageUtilization: 80 # This might not be the best metric for scaling TF Serving directly
      # For GPU utilization-based scaling, custom metrics via Prometheus Adapter are usually preferred.
      # Example (assuming custom metric 'gpu_load_average' is exposed and collected):
      # - type: Pods
      #   pods:
      #     metric:
      #       name: tfserving_gpu_utilization_percent # Hypothetical metric
      #     target:
      #       type: AverageValue
      #       averageValue: "70" # Target 70% average GPU utilization per pod
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
          - type: Percent
            value: 100
            periodSeconds: 180
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
          - type: Percent
            value: 100
            periodSeconds: 60
          - type: Pods
            value: 1
            periodSeconds: 60
          selectPolicy: Max
    

#### 6.1.5 `models/image-classification-resnet50/kubernetes/configmap-tfserving.yaml` (If used)
-   **Specification:**
    yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: resnet50-tfserving-config
      namespace: creativeflow-ai-serving
    data:
      models.config: |
        model_config_list: {
          config: {
            name: "resnet50",
            base_path: "/models/resnet50", 
            model_platform: "tensorflow"
            # version_policy: { latest: { num_versions: 1 } } # Optional: serve only latest
          }
        }
    

### 6.2 Text Generation: GPT-2 (Triton Inference Server)

#### 6.2.1 `models/text-generation-gpt2/docker/Dockerfile`
-   **Specification:**
    dockerfile
    ARG CREATIVEFLOW_TRITON_BASE_IMAGE_TAG=latest
    FROM creativeflow/triton-inference-server-base:${CREATIVEFLOW_TRITON_BASE_IMAGE_TAG}

    LABEL model.name="gpt2"
    LABEL model.framework="pytorch_libtorch" # Or onnxruntime_onnx
    LABEL model.task="text-generation"

    # MODEL_REPOSITORY_PATH is /models from base image
    COPY ../model_repository/gpt2 ${MODEL_REPOSITORY_PATH}/gpt2

    # CMD is inherited from base: tritonserver --model-repository=/models
    
    *Assume `../model_repository/gpt2/` contains `config.pbtxt` and `1/model.pt` (or `model.onnx`).*

#### 6.2.2 `models/text-generation-gpt2/model_repository/gpt2/config.pbtxt`
-   **Specification:**
    pbtxt
    name: "gpt2"
    platform: "pytorch_libtorch" 
    max_batch_size: 4 # Example
    input [
      {
        name: "INPUT_IDS" 
        data_type: TYPE_INT64
        dims: [ -1 ] # Variable sequence length
      },
      {
        name: "ATTENTION_MASK"
        data_type: TYPE_INT64
        dims: [ -1 ] # Matches INPUT_IDS dims
      }
    ]
    output [
      {
        name: "OUTPUT_LOGITS" 
        data_type: TYPE_FP32 
        dims: [ -1, -1 ] # Sequence length, Vocab size
      }
    ]
    instance_group [ { kind: KIND_GPU, count: 1 } ]
    # Ensure these names (INPUT_IDS, etc.) match what your Triton Python backend (if used) or the model expects.
    # Or, if using a standard backend for a framework like ONNX, these are derived from the model file.
    
    *Model specific details for input/output tensors are critical here.*

#### 6.2.3 `models/text-generation-gpt2/model_repository/gpt2/1/model.py` (If Python backend)
-   As specified in Section 5.2.3 of the SRS or a similar structure adapted for GPT-2. This file will implement the `TritonPythonModel` class with `initialize`, `execute`, and `finalize` methods. `initialize` would load the GPT-2 model (e.g., from Hugging Face Transformers, converted to TorchScript or ONNX if not using Python backend directly) and tokenizer. `execute` would take input IDs and attention masks, generate text, and return output logits or generated token IDs.

#### 6.2.4 Kubernetes Manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`)
-   **`deployment.yaml`:** Similar to ResNet50, but image `your-private-registry/creativeflow/gpt2-triton:latest`, name `gpt2-triton`, labels updated. Ports: 8000 (http), 8001 (grpc), 8002 (http-metrics). Readiness/Liveness probes: `httpGet` path `/v2/health/ready` and `/v2/health/live` on port 8000. GPU resources requested.
    yaml
    # models/text-generation-gpt2/kubernetes/deployment.yaml (Excerpt)
    # ...
    spec:
      # ...
      template:
        # ...
        spec:
          serviceAccountName: ai-model-server-sa
          containers:
          - name: gpt2-triton-container
            image: your-private-registry/creativeflow/gpt2-triton:latest # Replace
            # ...
            ports:
            - containerPort: 8000
              name: http
            - containerPort: 8001
              name: grpc
            - containerPort: 8002
              name: http-metrics # Triton's metrics port
            # ...
            readinessProbe:
              httpGet:
                path: "/v2/health/ready"
                port: http 
              initialDelaySeconds: 30 # Triton can take time to load models
              # ...
            livenessProbe:
              httpGet:
                path: "/v2/health/live"
                port: http
              initialDelaySeconds: 60
              # ...
    
-   **`service.yaml`:** Targets `app: gpt2-triton`. Exposes ports 8000, 8001, and 8002 (named `http-metrics`). Label `creativeflow.ai/scrape-metrics: "true"`.
    yaml
    # models/text-generation-gpt2/kubernetes/service.yaml (Excerpt)
    # ...
    metadata:
      name: gpt2-triton-service
      namespace: creativeflow-ai-serving
      labels:
        app: gpt2-triton
        runtime: triton
        creativeflow.ai/scrape-metrics: "true"
    spec:
      selector:
        app: gpt2-triton
      ports:
      - name: http
        port: 8000
        targetPort: http
      - name: grpc
        port: 8001
        targetPort: grpc
      - name: http-metrics
        port: 8002
        targetPort: http-metrics
    # ...
    
-   **`hpa.yaml`:** Targets `gpt2-triton` deployment. Metrics can be CPU, or custom metrics from Triton like `nv_inference_request_success_total` rate, or `nv_inference_queue_duration_us`.

### 6.3 Custom Object Detection: YOLO (Custom Python FastAPI)

#### 6.3.1 `models/custom-object-detector-yolo/docker/Dockerfile`
-   **Specification:**
    dockerfile
    ARG CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG=latest
    FROM creativeflow/custom-python-fastapi-base:${CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG}

    LABEL model.name="yolo-custom"
    LABEL model.framework="pytorch" 
    LABEL model.task="object-detection"

    COPY ./models/custom-object-detector-yolo/docker/src /app/src
    COPY ./models/custom-object-detector-yolo/model_weights /app/model_weights
    COPY ./models/custom-object-detector-yolo/docker/requirements.txt /app/requirements_model.txt
    RUN pip install --no-cache-dir -r requirements_model.txt

    ENV MODEL_PATH=/app/model_weights/yolov5s.pt # Example, ensure this exists
    ENV CONFIDENCE_THRESHOLD=0.25
    
    # CMD from base image is likely sufficient:
    # CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
    
    *Assume `../model_weights/yolov5s.pt` exists.*

#### 6.3.2 `models/custom-object-detector-yolo/docker/requirements.txt`
-   **Specification:**
    txt
    # From base:
    # fastapi>=0.110.0,<0.112.0
    # uvicorn[standard]>=0.27.0,<0.30.0
    # pydantic>=2.5.0,<2.8.0
    # prometheus_client>=0.17.0,<0.21.0

    # YOLO specific:
    torch>=2.0.0,<2.3.0 # Ensure compatibility with CUDA version on host/base image
    torchvision>=0.15.0,<0.18.0
    # For YOLOv5 from ultralytics/yolov5 repo
    # pyyaml>=5.3.1
    # requests>=2.23.0
    # Pillow>=7.1.2
    # opencv-python-headless>=4.5.0 
    # matplotlib>=3.2.2 # Often a transitive dependency
    # pandas>=1.1.4 # For results.pandas()
    # seaborn>=0.11.0 # For plotting, might not be needed for server
    # tqdm>=4.64.0
    
    # If using Ultralytics YOLO package directly:
    ultralytics>=8.0.0,<8.2.0
    # Ensure ultralytics includes opencv, Pillow etc. or list them explicitly.
    
    *Note: Review dependencies based on the exact YOLO version and how it's loaded (`torch.hub.load` vs `ultralytics` package).*

#### 6.3.3 `models/custom-object-detector-yolo/docker/src/model_handler.py`
-   **Specification (Refined from file structure):**
    python
    import torch
    import os
    from PIL import Image
    import io
    import numpy as np
    # from ultralytics import YOLO # Uncomment if using YOLO from ultralytics package

    class YOLOModelHandler:
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super(YOLOModelHandler, cls).__new__(cls)
                # Initialize only once
                model_path = kwargs.get("model_path")
                confidence_threshold = kwargs.get("confidence_threshold", 0.25)
                
                cls._instance.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                print(f"YOLO Handler: Initializing model on device: {cls._instance.device}")

                if not model_path or not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model weights not found at {model_path}")
                
                try:
                    # Example for YOLOv5 via torch.hub. Needs internet on first run if not cached.
                    # For air-gapped, ensure 'ultralytics/yolov5' is locally available or use 'local' source.
                    cls._instance.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False, _verbose=False)
                    cls._instance.model.to(cls._instance.device)
                    cls._instance.model.eval()
                    cls._instance.confidence_threshold = float(confidence_threshold)
                    cls._instance.model_names = cls._instance.model.names # class names
                    print(f"YOLO model loaded successfully from {model_path} with confidence {cls._instance.confidence_threshold}")
                except Exception as e:
                    print(f"Error loading YOLO model: {e}")
                    raise RuntimeError(f"Failed to load YOLO model: {e}") from e
            return cls._instance

        def _preprocess_image(self, image_bytes: bytes) -> Image.Image:
            try:
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                return image
            except Exception as e:
                raise ValueError(f"Invalid image data: {e}") from e

        def _postprocess_detections(self, results) -> list:
            detections = []
            # For YOLOv5 from torch.hub.load, results.xyxy[0] is a tensor
            # [xmin, ymin, xmax, ymax, confidence, class_idx]
            if hasattr(results, 'xyxy') and results.xyxy and len(results.xyxy[0]) > 0:
                for det in results.xyxy[0].cpu().numpy():
                    if det[4] >= self.confidence_threshold:
                        class_id = int(det[5])
                        detections.append({
                            "xmin": float(det[0]),
                            "ymin": float(det[1]),
                            "xmax": float(det[2]),
                            "ymax": float(det[3]),
                            "confidence": float(det[4]),
                            "class_id": class_id,
                            "class_name": self.model_names[class_id] if class_id < len(self.model_names) else "unknown"
                        })
            return detections

        def predict(self, image_bytes: bytes, image_size: int = 640) -> list:
            if self.model is None:
                 raise RuntimeError("YOLO model is not loaded.")
            pil_image = self._preprocess_image(image_bytes)
            
            with torch.no_grad():
                # Inference
                results = self.model(pil_image, size=image_size) 
            
            processed_results = self._postprocess_detections(results)
            return processed_results

    # Global instance for FastAPI dependency injection
    # Initialized in main.py's startup event
    def get_yolo_handler() -> YOLOModelHandler:
        if YOLOModelHandler._instance is None:
             # This case should ideally not be hit if startup event initializes it.
             # Fallback or raise error.
            raise RuntimeError("YOLOModelHandler not initialized. Check FastAPI startup events.")
        return YOLOModelHandler._instance
    

#### 6.3.4 `models/custom-object-detector-yolo/docker/src/main.py`
-   **Specification (Refined from file structure):**
    python
    from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
    from fastapi.responses import JSONResponse
    import os
    from typing import List, Dict, Optional
    from pydantic import BaseModel
    from .model_handler import YOLOModelHandler, get_yolo_handler # Import the YOLO specific handler and getter
    from prometheus_client import Counter, Histogram, make_asgi_app

    # Metrics - Ensure these are distinct from base server metrics if both are active
    YOLO_REQUEST_COUNT = Counter(
        "yolo_detector_requests_total",
        "Total count of YOLO detection requests.",
        ["http_status"]
    )
    YOLO_REQUEST_LATENCY = Histogram(
        "yolo_detector_request_latency_seconds",
        "Histogram of YOLO detection request latencies."
    )
    YOLO_DETECTION_COUNT = Counter(
        "yolo_detector_detections_total",
        "Total number of objects detected by YOLO.",
        ["class_name"]
    )

    app = FastAPI(
        title="CreativeFlow Custom YOLO Object Detector",
        description="Serves a custom YOLO model for object detection via FastAPI.",
        version="1.0.0" # Model/Service Version
    )

    # Mount Prometheus ASGI app on /metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    @app.on_event("startup")
    async def startup_event():
        model_path = os.getenv("MODEL_PATH", "/app/model_weights/yolov5s.pt") # Default path
        confidence_str = os.getenv("CONFIDENCE_THRESHOLD", "0.25")
        try:
            confidence_threshold = float(confidence_str)
        except ValueError:
            print(f"Warning: Invalid CONFIDENCE_THRESHOLD '{confidence_str}', using default 0.25.")
            confidence_threshold = 0.25
        
        # Initialize the singleton YOLOModelHandler instance
        try:
            YOLOModelHandler(model_path=model_path, confidence_threshold=confidence_threshold)
            print(f"YOLO Model Handler initialized successfully with model: {model_path}")
        except Exception as e:
            print(f"CRITICAL: Error initializing YOLO Model Handler during startup: {e}")
            # Depending on desired behavior, could re-raise to fail startup or allow starting in a degraded state.
            # For now, allow startup, /health will report unhealthy.

    class Detection(BaseModel):
        xmin: float
        ymin: float
        xmax: float
        ymax: float
        confidence: float
        class_id: int
        class_name: str

    class PredictionResponse(BaseModel):
        request_id: Optional[str] = None
        detections: List[Detection]
        image_filename: Optional[str] = None
        model_name: str = "yolo-custom" # Example model name
        model_version: Optional[str] = os.getenv("MODEL_VERSION_TAG", "dev") # Example version

    @app.post("/v1/predict", 
              response_model=PredictionResponse, 
              summary="Detect Objects in Image using YOLO", 
              tags=["Object Detection"])
    async def predict_yolo_objects(
        file: UploadFile = File(..., description="Image file to perform object detection on."),
        request_id: Optional[str] = None, # Example of an optional request parameter
        yolo_handler: YOLOModelHandler = Depends(get_yolo_handler) # Dependency injection
    ):
        image_bytes = await file.read()
        if not image_bytes:
            YOLO_REQUEST_COUNT.labels(http_status=400).inc()
            raise HTTPException(status_code=400, detail="No image file provided or image is empty.")

        with YOLO_REQUEST_LATENCY.time():
            try:
                detections_data = yolo_handler.predict(image_bytes)
                for det in detections_data:
                    YOLO_DETECTION_COUNT.labels(class_name=det.get("class_name", "unknown")).inc()
                
                YOLO_REQUEST_COUNT.labels(http_status=200).inc()
                return PredictionResponse(
                    request_id=request_id,
                    detections=detections_data, 
                    image_filename=file.filename,
                    model_version=os.getenv("MODEL_VERSION_TAG", "yolo-custom-v1") # Example
                )
            except ValueError as ve: # Specific error for bad image data from handler
                YOLO_REQUEST_COUNT.labels(http_status=400).inc()
                raise HTTPException(status_code=400, detail=str(ve))
            except RuntimeError as re: # E.g. model not loaded
                 YOLO_REQUEST_COUNT.labels(http_status=503).inc()
                 raise HTTPException(status_code=503, detail=str(re))
            except Exception as e:
                print(f"Error during YOLO prediction: {type(e).__name__} - {e}")
                YOLO_REQUEST_COUNT.labels(http_status=500).inc()
                raise HTTPException(status_code=500, detail=f"Error processing image: {type(e).__name__}.")

    @app.get("/health", summary="Health Check", tags=["System"])
    async def health_check():
        if YOLOModelHandler._instance is None or YOLOModelHandler._instance.model is None:
            return JSONResponse(content={"status": "unhealthy", "detail": "YOLOModelHandler or model not initialized"}, status_code=503)
        # Add more sophisticated checks if needed (e.g., try a dummy inference)
        return JSONResponse(content={"status": "healthy"})

    # Include other routers if needed, e.g., for different model versions or tasks served by this pod
    

#### 6.3.5 Kubernetes Manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`)
-   **`deployment.yaml`:** Name `yolo-custom-fastapi`, labels updated. Image `your-private-registry/creativeflow/yolo-custom-fastapi:latest`. Port 8000 (http) and a metrics port (e.g. 8000 if FastAPI serves /metrics on same port, or separate). Env vars `MODEL_PATH`, `CONFIDENCE_THRESHOLD`, `MODEL_VERSION_TAG`. Readiness/Liveness probes target `/health` on port 8000. GPU resources.
    yaml
    # models/custom-object-detector-yolo/kubernetes/deployment.yaml (Excerpt)
    # ...
    spec:
      template:
        metadata:
          labels:
            app: yolo-custom-fastapi
            runtime: custom-fastapi
            creativeflow.ai/scrape-metrics: "true" # Assuming FastAPI exposes /metrics
        spec:
          serviceAccountName: ai-model-server-sa
          containers:
          - name: yolo-custom-fastapi-container
            image: your-private-registry/creativeflow/yolo-custom-fastapi:latest # Replace
            ports:
            - containerPort: 8000
              name: http # Also serves /metrics by default with prometheus_client.make_asgi_app
            env:
            - name: MODEL_PATH
              value: "/app/model_weights/yolov5s.pt" # Default, can be overridden
            - name: CONFIDENCE_THRESHOLD
              value: "0.25" 
            - name: MODEL_VERSION_TAG 
              value: "yolo-prod-v1.2" # Example version
            # ... resources, probes as before ...
            readinessProbe:
              httpGet:
                path: "/health"
                port: http 
              initialDelaySeconds: 30 # Allow time for model loading
            livenessProbe:
              httpGet:
                path: "/health"
                port: http
              initialDelaySeconds: 60
    
-   **`service.yaml`:** Targets `app: yolo-custom-fastapi`. Exposes port 8000 (http), maps to targetPort `http`. Label `creativeflow.ai/scrape-metrics: "true"`.
-   **`hpa.yaml`:** Targets `yolo-custom-fastapi` deployment. Metrics could be CPU, GPU, or custom Prometheus metrics from the FastAPI app (e.g., `yolo_detector_requests_total` rate, `yolo_detector_request_latency_seconds`).

## 7. GPU Resource Management (INT-007, NFR-002, DEP-001)
-   The NVIDIA GPU Operator (installed on K8s cluster) is essential for exposing GPU resources to pods.
-   Kubernetes `Deployment`s for GPU-accelerated models *must* include:
    yaml
    spec:
      containers:
      - name: ...
        resources:
          limits:
            nvidia.com/gpu: 1 # Or more, if model can utilize multiple GPUs per instance
          requests:
            nvidia.com/gpu: 1 
    
-   **Multi-Instance GPU (MIG):** If supported by the NVIDIA hardware (e.g., A100, H100) and enabled on the nodes, MIG can partition a physical GPU into multiple, fully isolated GPU instances. Pods can then request these specific MIG profiles. This allows finer-grained GPU allocation for models that don't need a full GPU.
    -   Configuration of MIG profiles is done at the node level (outside this repo's direct scope but important context).
    -   Pods would request a specific MIG device, e.g., `nvidia.com/mig-1g.5gb: 1`.
-   **GPU Time-Slicing:** For GPUs that don't support MIG, Kubernetes with the NVIDIA device plugin might offer time-slicing by oversubscribing GPU requests. This provides shared access but less isolation and potentially more performance contention than MIG. Use with caution and extensive testing.
-   The choice between full GPU, MIG instance, or time-slicing depends on model requirements, hardware capabilities, and cost/utilization optimization goals, to be determined by the MLOps team during model deployment.

## 8. Deployment of Repository Artifacts
-   **Base Configurations (`base/` directory):**
    -   These YAML files (namespace, RBAC, base ServiceMonitor) should be applied once to the Kubernetes cluster during initial platform setup.
    -   Method: `kubectl apply -k base/` (if a `kustomization.yaml` is provided in `base/`) or `kubectl apply -f <file>` for each.
-   **Runtime Base Images (`runtime-bases/` directory):**
    -   The Dockerfiles in this directory are built by the CI/CD pipeline (`REPO-DEVOPS-CICD-001`).
    -   Built images are tagged (e.g., `creativeflow/tensorflow-serving-base:0.1.0`, `creativeflow/triton-inference-server-base:0.1.0-24.05`) and pushed to the project's private container registry.
-   **Example Model Deployments (`models/` directory):**
    -   These serve as templates and examples for the MLOps Platform Service (`REPO-AISIML-MLOPS-001`).
    -   **Model-Specific Dockerfiles:** When a new custom model is onboarded by the MLOps service, its Dockerfile (likely based on one of the `runtime-bases`) will be built and pushed to the private registry by the MLOps CI/CD pipeline.
    -   **Model-Specific Kubernetes Manifests:** The MLOps service will use these example manifests as templates. It will parameterize them (e.g., image tag, model name, resource requests, specific configurations via ConfigMaps) and then deploy them to the `creativeflow-ai-serving` namespace in the Kubernetes cluster using `kubectl apply` or a GitOps approach.
-   **Kustomize:** It is highly recommended to use Kustomize for managing Kubernetes configurations. Each model deployment (`models/<model_name>/kubernetes/`) should have its own `kustomization.yaml`. A top-level `kustomization.yaml` could also be used to manage deployment of multiple models or base components.
    yaml
    # Example: models/image-classification-resnet50/kubernetes/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    namespace: creativeflow-ai-serving # Ensure resources are created in the correct namespace
    resources:
      - deployment.yaml
      - service.yaml
      - hpa.yaml
      # - configmap-tfserving.yaml # If used
    # Patches or common labels can be added here
    
This layered approach ensures that the K8s AI Serving Platform provides robust, standardized foundations, while the MLOps service handles the dynamic and specific aspects of individual AI model deployments.
