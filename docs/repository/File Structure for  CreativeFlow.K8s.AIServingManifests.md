# Specification

# 1. Files

- **Path:** base/namespace.yaml  
**Description:** Defines the Kubernetes Namespace for all AI serving workloads, providing a scope for names and a way to divide cluster resources.  
**Template:** Kubernetes YAML  
**Dependency Level:** 0  
**Name:** namespace  
**Type:** KubernetesManifest  
**Relative Path:** base/namespace.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Namespace Definition
    - Resource Isolation
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To create a dedicated Kubernetes namespace 'ai-serving' for isolating AI model deployment resources.  
**Logic Description:** apiVersion: v1
kind: Namespace
metadata:
  name: ai-serving
  labels:
    name: ai-serving  
**Documentation:**
    
    - **Summary:** This manifest defines the 'ai-serving' namespace where all AI models and related Kubernetes resources will be deployed. It helps in organizing resources and applying policies at a namespace level.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** base/rbac/serviceaccount-model-server.yaml  
**Description:** Defines a Kubernetes ServiceAccount for AI model serving pods, enabling fine-grained access control if needed.  
**Template:** Kubernetes YAML  
**Dependency Level:** 1  
**Name:** serviceaccount-model-server  
**Type:** KubernetesManifest  
**Relative Path:** base/rbac/serviceaccount-model-server.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Account Definition
    - Identity for Pods
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To create a ServiceAccount named 'model-server-sa' within the 'ai-serving' namespace for AI model pods.  
**Logic Description:** apiVersion: v1
kind: ServiceAccount
metadata:
  name: model-server-sa
  namespace: ai-serving  
**Documentation:**
    
    - **Summary:** Defines a specific ServiceAccount for AI model serving pods. This allows assigning specific roles and permissions to the pods if they need to interact with the Kubernetes API or other secured resources.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesRBAC
    
- **Path:** base/rbac/role-model-reader.yaml  
**Description:** Defines a Kubernetes Role with permissions typically needed by model servers, e.g., reading ConfigMaps or Secrets if configurations are mounted this way.  
**Template:** Kubernetes YAML  
**Dependency Level:** 1  
**Name:** role-model-reader  
**Type:** KubernetesManifest  
**Relative Path:** base/rbac/role-model-reader.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Role Definition
    - Permission Specification
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To create a Role named 'model-reader-role' in the 'ai-serving' namespace allowing read access to ConfigMaps and Secrets.  
**Logic Description:** apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ai-serving
  name: model-reader-role
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "watch", "list"]  
**Documentation:**
    
    - **Summary:** Defines a Kubernetes Role that grants read-only permissions to ConfigMaps and Secrets within the 'ai-serving' namespace. This can be bound to the 'model-server-sa' ServiceAccount.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesRBAC
    
- **Path:** base/rbac/rolebinding-model-server.yaml  
**Description:** Binds the 'model-reader-role' to the 'model-server-sa' ServiceAccount within the 'ai-serving' namespace.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** rolebinding-model-server  
**Type:** KubernetesManifest  
**Relative Path:** base/rbac/rolebinding-model-server.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Role Binding
    - Permission Assignment
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To bind the 'model-reader-role' to the 'model-server-sa' ServiceAccount, granting its pods the defined permissions.  
**Logic Description:** apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: model-server-rb
  namespace: ai-serving
subjects:
- kind: ServiceAccount
  name: model-server-sa
  namespace: ai-serving
roleRef:
  kind: Role
  name: model-reader-role
  apiGroup: rbac.authorization.k8s.io  
**Documentation:**
    
    - **Summary:** This manifest binds the previously defined 'model-reader-role' to the 'model-server-sa' ServiceAccount. This effectively grants pods running under this service account the permissions specified in the role.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesRBAC
    
- **Path:** base/resource-management/resourcequota.yaml  
**Description:** Defines ResourceQuota for the 'ai-serving' namespace to limit aggregate resource consumption.  
**Template:** Kubernetes YAML  
**Dependency Level:** 1  
**Name:** resourcequota  
**Type:** KubernetesManifest  
**Relative Path:** base/resource-management/resourcequota.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Resource Quota Management
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To set overall resource limits (CPU, memory, GPU) for the 'ai-serving' namespace.  
**Logic Description:** apiVersion: v1
kind: ResourceQuota
metadata:
  name: ai-serving-quota
  namespace: ai-serving
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 100Gi
    limits.cpu: "40"
    limits.memory: 200Gi
    nvidia.com/gpu: "4" # Example GPU limit
    pods: "50"  
**Documentation:**
    
    - **Summary:** Defines a ResourceQuota for the 'ai-serving' namespace. This limits the total amount of CPU, memory, GPU resources, and number of pods that can be consumed by all deployments within this namespace.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** base/resource-management/limitrange.yaml  
**Description:** Defines LimitRange for the 'ai-serving' namespace to set default resource requests and limits for pods.  
**Template:** Kubernetes YAML  
**Dependency Level:** 1  
**Name:** limitrange  
**Type:** KubernetesManifest  
**Relative Path:** base/resource-management/limitrange.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Resource Limits
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To set default CPU and memory requests/limits for containers in the 'ai-serving' namespace if not specified in pod specs.  
**Logic Description:** apiVersion: v1
kind: LimitRange
metadata:
  name: ai-serving-limits
  namespace: ai-serving
spec:
  limits:
  - default:
      memory: "1Gi"
      cpu: "500m"
    defaultRequest:
      memory: "512Mi"
      cpu: "250m"
    type: Container  
**Documentation:**
    
    - **Summary:** Defines default resource requests and limits for containers within the 'ai-serving' namespace. If a pod does not specify its own resource requirements, these defaults will be applied.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** base/cluster-setup/gpu-operator-values.placeholder.yaml  
**Description:** Placeholder for NVIDIA GPU Operator Helm chart values or configuration. Actual installation is typically cluster-wide and managed separately, but this indicates dependency/awareness.  
**Template:** Kubernetes YAML  
**Dependency Level:** 0  
**Name:** gpu-operator-values.placeholder  
**Type:** KubernetesManifest  
**Relative Path:** base/cluster-setup/gpu-operator-values.placeholder.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - GPU Resource Management Configuration Placeholder
    
**Requirement Ids:**
    
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To act as a placeholder for NVIDIA GPU Operator configurations, reminding that GPU support is critical for this cluster.  
**Logic Description:** # This file is a placeholder.
# NVIDIA GPU Operator is typically installed cluster-wide.
# Refer to official NVIDIA documentation for installation and configuration.
# Example values for a Helm chart might include:
# driver:
#   enabled: true
# toolkit:
#   enabled: true
# operator:
#   defaultRuntime: nvidia  
**Documentation:**
    
    - **Summary:** This file serves as a placeholder and reminder for configuring the NVIDIA GPU Operator, which is essential for enabling GPU resources within the Kubernetes cluster. The actual operator is a cluster-level component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** runtimes/tensorflow-serving/Dockerfile.template  
**Description:** Template Dockerfile for packaging TensorFlow models to be served with TensorFlow Serving.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** Dockerfile.template  
**Type:** Dockerfile  
**Relative Path:** runtimes/tensorflow-serving/Dockerfile.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Container Image Build
    - TensorFlow Model Packaging
    - TensorFlow Serving Integration
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a template for creating Docker images that run TensorFlow Serving with a specific TensorFlow model.  
**Logic Description:** FROM tensorflow/serving:latest # Or a specific version with GPU support e.g., tensorflow/serving:latest-gpu

# Set up Tini, a lightweight init system for containers
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Model name, will be a directory inside /models/
ARG MODEL_NAME=my_model
# Path to the SavedModel directory on the host, to be copied into the image
ARG SAVED_MODEL_PATH=./model_files/

# Copy the SavedModel directory into the image
COPY ${SAVED_MODEL_PATH} /models/${MODEL_NAME}/

# Expose the gRPC and REST API ports
EXPOSE 8500 8501

# Command to run TensorFlow Serving
# The model config file can be used for more complex setups (multiple models, versions)
# CMD ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_name=${MODEL_NAME}", "--model_base_path=/models/${MODEL_NAME}"]
# Alternatively, use a model config file:
COPY models.config /models/models.config
CMD ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_config_file=/models/models.config"]  
**Documentation:**
    
    - **Summary:** This Dockerfile template is used to package a TensorFlow SavedModel for serving with TensorFlow Serving. It copies the model files into the image and configures TensorFlow Serving to load and serve the model via gRPC and REST APIs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtimes/tensorflow-serving/deployment.template.yaml  
**Description:** Kubernetes Deployment manifest template for TensorFlow Serving.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** deployment.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/tensorflow-serving/deployment.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Deployment
    - Pod Configuration
    - GPU Resource Allocation
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To define a Kubernetes Deployment for running TensorFlow Serving instances, configured for a specific model image and GPU resources.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-__MODEL_NAME_PLACEHOLDER__
  namespace: ai-serving
  labels:
    app: tf-serving-__MODEL_NAME_PLACEHOLDER__
spec:
  replicas: __REPLICA_COUNT_PLACEHOLDER__
  selector:
    matchLabels:
      app: tf-serving-__MODEL_NAME_PLACEHOLDER__
  template:
    metadata:
      labels:
        app: tf-serving-__MODEL_NAME_PLACEHOLDER__
    spec:
      serviceAccountName: model-server-sa # Optional, if RBAC is needed
      containers:
      - name: tf-serving-container
        image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__
        ports:
        - containerPort: 8500 # gRPC
        - containerPort: 8501 # REST
        resources:
          limits:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__ # Request 1 GPU
            memory: "__MEMORY_LIMIT_PLACEHOLDER__"
            cpu: "__CPU_LIMIT_PLACEHOLDER__"
          requests:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_REQUEST_PLACEHOLDER__"
            cpu: "__CPU_REQUEST_PLACEHOLDER__"
        readinessProbe:
          tcpSocket:
            port: 8501
          initialDelaySeconds: 15
          periodSeconds: 10
        livenessProbe:
          tcpSocket:
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 20  
**Documentation:**
    
    - **Summary:** This Kubernetes Deployment manifest template describes how to deploy a TensorFlow Serving application. It specifies the Docker image, number of replicas, container ports, resource requests/limits (including GPUs), and health probes. Placeholders should be replaced with specific model details.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesDeployment
    
- **Path:** runtimes/tensorflow-serving/service.template.yaml  
**Description:** Kubernetes Service manifest template for exposing TensorFlow Serving.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** service.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/tensorflow-serving/service.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To expose the TensorFlow Serving Deployment within the Kubernetes cluster via a stable IP address and port.  
**Logic Description:** apiVersion: v1
kind: Service
metadata:
  name: tf-serving-__MODEL_NAME_PLACEHOLDER__-svc
  namespace: ai-serving
  labels:
    app: tf-serving-__MODEL_NAME_PLACEHOLDER__
spec:
  selector:
    app: tf-serving-__MODEL_NAME_PLACEHOLDER__
  ports:
  - name: grpc
    port: 8500
    targetPort: 8500
  - name: rest
    port: 8501
    targetPort: 8501
  type: ClusterIP # Or LoadBalancer/NodePort for external exposure if needed directly  
**Documentation:**
    
    - **Summary:** This Kubernetes Service manifest template creates a stable internal endpoint (ClusterIP) for accessing the TensorFlow Serving pods. It maps service ports to the container ports for gRPC and REST APIs. Placeholders should be replaced with specific model details.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesNetwork
    
- **Path:** runtimes/tensorflow-serving/configmap-models.template.yaml  
**Description:** Kubernetes ConfigMap manifest template for TensorFlow Serving's models.config file.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** configmap-models.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/tensorflow-serving/configmap-models.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Management
    - Model Server Configuration
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a models.config file to TensorFlow Serving, allowing it to serve one or more models with specific version policies.  
**Logic Description:** apiVersion: v1
kind: ConfigMap
metadata:
  name: tf-serving-__MODEL_NAME_PLACEHOLDER__-models-config
  namespace: ai-serving
data:
  models.config: |
    model_config_list: {
      config: {
        name: "__MODEL_NAME_PLACEHOLDER__",
        base_path: "/models/__MODEL_NAME_PLACEHOLDER__/",
        model_platform: "tensorflow",
        model_version_policy: { all: {} } # Serve all versions found in base_path
      }
      # Add more models here if needed
      # config: {
      #   name: "another_model",
      #   base_path: "/models/another_model/",
      #   model_platform: "tensorflow"
      # }
    }  
**Documentation:**
    
    - **Summary:** This ConfigMap template defines a 'models.config' file for TensorFlow Serving. This file tells TF Serving which models to load, where to find them (base_path, typically within the container), and their platform. Placeholders need to be filled.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** runtimes/torchserve/Dockerfile.template  
**Description:** Template Dockerfile for packaging PyTorch models (.mar) to be served with TorchServe.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** Dockerfile.template  
**Type:** Dockerfile  
**Relative Path:** runtimes/torchserve/Dockerfile.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Container Image Build
    - PyTorch Model Packaging
    - TorchServe Integration
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a template for creating Docker images that run TorchServe with specified PyTorch model archive (.mar) files.  
**Logic Description:** FROM pytorch/torchserve:latest # Or a specific version with GPU, e.g., pytorch/torchserve:latest-gpu

# Copy model archive file(s) (.mar) to the model store directory
# ARG MAR_FILES_PATH=./model_store/
# COPY ${MAR_FILES_PATH} /home/model-server/model-store/

# Example: copy a single .mar file provided during build
ARG MODEL_MAR_FILE=my_model.mar
COPY ${MODEL_MAR_FILE} /home/model-server/model-store/

# Copy TorchServe configuration file (optional)
# COPY config.properties /home/model-server/

# Expose TorchServe inference, management, and metrics ports
EXPOSE 8080 8081 8082

# Start TorchServe
# The CMD is usually inherited from the base image, but can be overridden if needed.
# Default CMD often starts torchserve with models in model-store.
# For specific models at startup: torchserve --start --model-store model_store --models model_name1.mar model_name2.mar
# Or use a snapshot: torchserve --start --ts-config /home/model-server/config.properties  
**Documentation:**
    
    - **Summary:** This Dockerfile template packages PyTorch model archive (.mar) files for serving with TorchServe. It copies .mar files into the model store and exposes TorchServe's ports. TorchServe typically auto-loads models from the model store on startup.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtimes/torchserve/deployment.template.yaml  
**Description:** Kubernetes Deployment manifest template for TorchServe.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** deployment.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/torchserve/deployment.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Deployment
    - Pod Configuration
    - GPU Resource Allocation
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To define a Kubernetes Deployment for running TorchServe instances, configured for a specific model image and GPU resources.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: torchserve-__MODEL_NAME_PLACEHOLDER__
  namespace: ai-serving
  labels:
    app: torchserve-__MODEL_NAME_PLACEHOLDER__
spec:
  replicas: __REPLICA_COUNT_PLACEHOLDER__
  selector:
    matchLabels:
      app: torchserve-__MODEL_NAME_PLACEHOLDER__
  template:
    metadata:
      labels:
        app: torchserve-__MODEL_NAME_PLACEHOLDER__
    spec:
      serviceAccountName: model-server-sa # Optional
      containers:
      - name: torchserve-container
        image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__
        ports:
        - name: inference
          containerPort: 8080
        - name: management
          containerPort: 8081
        - name: metrics
          containerPort: 8082
        resources:
          limits:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_LIMIT_PLACEHOLDER__"
            cpu: "__CPU_LIMIT_PLACEHOLDER__"
          requests:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_REQUEST_PLACEHOLDER__"
            cpu: "__CPU_REQUEST_PLACEHOLDER__"
        # TorchServe readiness/liveness can be more complex, often checking specific model health
        # Basic check for inference port:
        readinessProbe:
          tcpSocket:
            port: 8080
          initialDelaySeconds: 30 # TorchServe can take time to load models
          periodSeconds: 15
        livenessProbe:
          tcpSocket:
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30  
**Documentation:**
    
    - **Summary:** This Kubernetes Deployment manifest template is for deploying a TorchServe application. It specifies the Docker image, replicas, ports for inference, management, and metrics, and resource allocation (including GPUs). Placeholders should be filled with model-specific details.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesDeployment
    
- **Path:** runtimes/torchserve/service.template.yaml  
**Description:** Kubernetes Service manifest template for exposing TorchServe.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** service.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/torchserve/service.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To expose the TorchServe Deployment within the Kubernetes cluster for inference, management, and metrics access.  
**Logic Description:** apiVersion: v1
kind: Service
metadata:
  name: torchserve-__MODEL_NAME_PLACEHOLDER__-svc
  namespace: ai-serving
  labels:
    app: torchserve-__MODEL_NAME_PLACEHOLDER__
spec:
  selector:
    app: torchserve-__MODEL_NAME_PLACEHOLDER__
  ports:
  - name: inference
    port: 8080
    targetPort: 8080
  - name: management
    port: 8081
    targetPort: 8081
  - name: metrics
    port: 8082
    targetPort: 8082
  type: ClusterIP  
**Documentation:**
    
    - **Summary:** This Service manifest template creates internal ClusterIP services for accessing TorchServe's inference, management, and metrics endpoints. It routes traffic to the appropriate pods selected by the label selector. Placeholders are for model-specific naming.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesNetwork
    
- **Path:** runtimes/triton-inference-server/Dockerfile.template  
**Description:** Template Dockerfile for NVIDIA Triton Inference Server, typically focusing on organizing the model repository structure.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** Dockerfile.template  
**Type:** Dockerfile  
**Relative Path:** runtimes/triton-inference-server/Dockerfile.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Container Image Build
    - Multi-Framework Model Serving
    - Triton Integration
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a template for creating Docker images that run Triton Inference Server, primarily by copying a structured model repository.  
**Logic Description:** FROM nvcr.io/nvidia/tritonserver:latest-py3 # Or specific version with appropriate backend support e.g., :23.10-py3

# Triton expects a model repository. This Dockerfile would copy it.
# The structure of the model repository is crucial.
# See runtimes/triton-inference-server/model-repository-structure.md
ARG MODEL_REPO_PATH=./model_repository/
COPY ${MODEL_REPO_PATH} /models/

# Expose Triton's HTTP, gRPC, and metrics ports
EXPOSE 8000 8001 8002

# The base image's CMD usually starts tritonserver pointing to /models
# CMD ["tritonserver", "--model-repository=/models"]  
**Documentation:**
    
    - **Summary:** This Dockerfile template is for NVIDIA Triton Inference Server. Its main role is to copy a pre-structured model repository (containing models in various supported formats like ONNX, TensorRT, TensorFlow, PyTorch) into the '/models' directory, which Triton automatically scans. 
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtimes/triton-inference-server/deployment.template.yaml  
**Description:** Kubernetes Deployment manifest template for Triton Inference Server.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** deployment.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/triton-inference-server/deployment.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Deployment
    - Pod Configuration
    - GPU Resource Allocation
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To define a Kubernetes Deployment for running Triton Inference Server instances, configured for a specific model image and GPU resources.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
  namespace: ai-serving
  labels:
    app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
spec:
  replicas: __REPLICA_COUNT_PLACEHOLDER__
  selector:
    matchLabels:
      app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
  template:
    metadata:
      labels:
        app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
    spec:
      serviceAccountName: model-server-sa # Optional
      containers:
      - name: triton-server-container
        image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__
        ports:
        - name: http
          containerPort: 8000
        - name: grpc
          containerPort: 8001
        - name: metrics
          containerPort: 8002
        resources:
          limits:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_LIMIT_PLACEHOLDER__"
            cpu: "__CPU_LIMIT_PLACEHOLDER__"
          requests:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_REQUEST_PLACEHOLDER__"
            cpu: "__CPU_REQUEST_PLACEHOLDER__"
        readinessProbe:
          httpGet:
            path: /v2/health/ready
            port: 8000
          initialDelaySeconds: 20
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /v2/health/live
            port: 8000
          initialDelaySeconds: 45
          periodSeconds: 15  
**Documentation:**
    
    - **Summary:** This Kubernetes Deployment manifest template is for deploying NVIDIA Triton Inference Server. It specifies the Docker image (which includes the model repository), replicas, standard Triton ports, and resource allocation (including GPUs). Placeholders are for collection-specific naming.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesDeployment
    
- **Path:** runtimes/triton-inference-server/service.template.yaml  
**Description:** Kubernetes Service manifest template for exposing Triton Inference Server.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** service.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/triton-inference-server/service.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To expose the Triton Inference Server Deployment within the Kubernetes cluster for HTTP, gRPC, and metrics access.  
**Logic Description:** apiVersion: v1
kind: Service
metadata:
  name: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__-svc
  namespace: ai-serving
  labels:
    app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
spec:
  selector:
    app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
  ports:
  - name: http
    port: 8000
    targetPort: 8000
  - name: grpc
    port: 8001
    targetPort: 8001
  - name: metrics
    port: 8002
    targetPort: 8002
  type: ClusterIP  
**Documentation:**
    
    - **Summary:** This Service manifest template creates internal ClusterIP services for accessing Triton Inference Server's HTTP, gRPC, and metrics endpoints. It routes traffic to the Triton pods. Placeholders are for collection-specific naming.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesNetwork
    
- **Path:** runtimes/triton-inference-server/model-repository-structure.md  
**Description:** Markdown document explaining the expected directory structure for Triton's model repository.  
**Template:** Markdown  
**Dependency Level:** 1  
**Name:** model-repository-structure  
**Type:** Documentation  
**Relative Path:** runtimes/triton-inference-server/model-repository-structure.md  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Documentation
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To document the required layout for models to be served by Triton Inference Server.  
**Logic Description:** # Triton Model Repository Structure

This document outlines the directory structure Triton Inference Server expects for its model repository.

/models  (root model directory)
  └── <model_name_1>/
      ├── config.pbtxt  (model configuration file)
      └── <version_number_1>/
          └── <model_artifact_file_1> (e.g., model.onnx, model.plan, model.savedmodel/variables)
      └── <version_number_2>/
          └── <model_artifact_file_2>
  └── <model_name_2>/
      ├── config.pbtxt
      └── <version_number_1>/
          └── <model_artifact_file_3>

Refer to NVIDIA Triton documentation for details on `config.pbtxt` and specific model backends.  
**Documentation:**
    
    - **Summary:** Provides guidance on how to structure the model repository when using NVIDIA Triton Inference Server. This structure allows Triton to discover and load models automatically.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** runtimes/custom-python/Dockerfile.template  
**Description:** Template Dockerfile for packaging custom Python (e.g., FastAPI, Flask) AI model servers.  
**Template:** Dockerfile  
**Dependency Level:** 1  
**Name:** Dockerfile.template  
**Type:** Dockerfile  
**Relative Path:** runtimes/custom-python/Dockerfile.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Container Image Build
    - Custom Python Server Packaging
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a template for building Docker images for custom Python-based AI model serving applications.  
**Logic Description:** FROM python:3.9-slim # Or desired Python version

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./model_artifacts /app/model_artifacts # Example: if model files are co-packaged

EXPOSE 8000 # Assuming the custom server runs on port 8000

# Command to run the custom Python server (e.g., using uvicorn for FastAPI)
# CMD ["python", "./src/main.py"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]  
**Documentation:**
    
    - **Summary:** This Dockerfile template is for custom Python AI model servers (e.g., built with FastAPI or Flask). It installs dependencies from 'requirements.txt', copies application code and model artifacts, exposes the server port, and defines the command to run the server.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Containerization
    
- **Path:** runtimes/custom-python/deployment.template.yaml  
**Description:** Kubernetes Deployment manifest template for custom Python model servers.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** deployment.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/custom-python/deployment.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Deployment
    - Pod Configuration
    - GPU Resource Allocation
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To define a Kubernetes Deployment for running custom Python AI server instances, configured for a specific image and resources.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-py-server-__MODEL_NAME_PLACEHOLDER__
  namespace: ai-serving
  labels:
    app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
spec:
  replicas: __REPLICA_COUNT_PLACEHOLDER__
  selector:
    matchLabels:
      app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
  template:
    metadata:
      labels:
        app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
    spec:
      serviceAccountName: model-server-sa # Optional
      containers:
      - name: custom-py-server-container
        image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__
        ports:
        - containerPort: 8000 # Match EXPOSE in Dockerfile
        resources:
          limits:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__ # If model needs GPU
            memory: "__MEMORY_LIMIT_PLACEHOLDER__"
            cpu: "__CPU_LIMIT_PLACEHOLDER__"
          requests:
            nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
            memory: "__MEMORY_REQUEST_PLACEHOLDER__"
            cpu: "__CPU_REQUEST_PLACEHOLDER__"
        readinessProbe:
          httpGet:
            path: /health/ready # Assuming a /health/ready endpoint
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health/live # Assuming a /health/live endpoint
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 20  
**Documentation:**
    
    - **Summary:** This Kubernetes Deployment template is for custom Python AI model servers. It specifies the image, replicas, port, resource allocation (including optional GPU), and health probes. Health probe paths (/health/ready, /health/live) are common conventions. Placeholders need updating.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesDeployment
    
- **Path:** runtimes/custom-python/service.template.yaml  
**Description:** Kubernetes Service manifest template for exposing custom Python model servers.  
**Template:** Kubernetes YAML  
**Dependency Level:** 2  
**Name:** service.template  
**Type:** KubernetesManifest  
**Relative Path:** runtimes/custom-python/service.template.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To expose the custom Python AI server Deployment within the Kubernetes cluster.  
**Logic Description:** apiVersion: v1
kind: Service
metadata:
  name: custom-py-server-__MODEL_NAME_PLACEHOLDER__-svc
  namespace: ai-serving
  labels:
    app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
spec:
  selector:
    app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
  ports:
  - name: http
    port: 80 # Service port
    targetPort: 8000 # Container port
  type: ClusterIP  
**Documentation:**
    
    - **Summary:** This Service manifest template creates an internal ClusterIP service for custom Python AI servers. It maps a service port (e.g., 80) to the container's application port (e.g., 8000). Placeholders are for model-specific naming.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesNetwork
    
- **Path:** runtimes/custom-python/src/main.py.template  
**Description:** Python template for a simple FastAPI/Flask model serving application.  
**Template:** Python FastAPI/Flask Template  
**Dependency Level:** 0  
**Name:** main.py.template  
**Type:** PythonServerCode  
**Relative Path:** runtimes/custom-python/src/main.py.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** model  
**Type:** object  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** load_model  
**Parameters:**
    
    - model_path: str
    
**Return Type:** object  
**Attributes:** private  
    - **Name:** predict  
**Parameters:**
    
    - data: dict
    
**Return Type:** dict  
**Attributes:** public|async (FastAPI)  
    - **Name:** health_live  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public|async (FastAPI)  
    - **Name:** health_ready  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public|async (FastAPI)  
    
**Implemented Features:**
    
    - Model Loading
    - Inference Endpoint
    - Health Checks
    - Request Handling
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To provide a basic structure for a custom Python AI model server using FastAPI, including model loading, prediction endpoint, and health checks.  
**Logic Description:** # Example using FastAPI
from fastapi import FastAPI
# import model_loader # Assume a model_loader.py exists

app = FastAPI()
model = None

@app.on_event("startup")
async def startup_event():
    global model
    # model = model_loader.load_model("/app/model_artifacts/my_model.pkl") # Example
    print("Model loaded (placeholder)")

@app.post("/predict")
async def predict(request_data: dict):
    # Preprocess request_data
    # predictions = model.predict(processed_data) # Example
    # Postprocess predictions
    return {"predictions": "placeholder_result"}

@app.get("/health/live")
async def health_live():
    return {"status": "live"}

@app.get("/health/ready")
async def health_ready():
    # Add checks if model is loaded, etc.
    global model
    # if model is None: raise HTTPException(status_code=503, detail="Model not ready")
    return {"status": "ready"}

# To run: uvicorn main:app --host 0.0.0.0 --port 8000  
**Documentation:**
    
    - **Summary:** A template for a Python-based AI model serving application using FastAPI. It includes placeholders for model loading logic (e.g., from './model_artifacts/'), a '/predict' endpoint for inference, and '/health/live' & '/health/ready' endpoints for Kubernetes probes.
    
**Namespace:** src  
**Metadata:**
    
    - **Category:** ApplicationCode
    
- **Path:** runtimes/custom-python/src/model_loader.py.template  
**Description:** Python template for model loading logic, to be used by main.py.  
**Template:** Python Utility  
**Dependency Level:** 0  
**Name:** model_loader.py.template  
**Type:** PythonServerCode  
**Relative Path:** runtimes/custom-python/src/model_loader.py.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** load_custom_model  
**Parameters:**
    
    - model_path: str
    
**Return Type:** object  
**Attributes:** public  
    
**Implemented Features:**
    
    - Custom Model Loading Logic
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To encapsulate the logic for loading a custom AI model from a specified path.  
**Logic Description:** import pickle # Example for scikit-learn models
# Or import tensorflow, torch, etc. depending on the model type

def load_custom_model(model_path: str):
    """Loads a custom model from the given path."""
    # Example for a scikit-learn model saved with pickle
    # with open(model_path, 'rb') as f:
    #     model = pickle.load(f)
    # return model
    print(f"Model loading from {model_path} (placeholder)")
    return object() # Placeholder for actual model object  
**Documentation:**
    
    - **Summary:** This template provides a placeholder for Python code responsible for loading a custom machine learning model. The actual implementation will depend on the model's framework and serialization format (e.g., pickle, joblib, TensorFlow SavedModel, PyTorch state_dict).
    
**Namespace:** src  
**Metadata:**
    
    - **Category:** ApplicationCode
    
- **Path:** runtimes/custom-python/src/requirements.txt.template  
**Description:** Template requirements.txt file for custom Python model servers.  
**Template:** Python Requirements  
**Dependency Level:** 0  
**Name:** requirements.txt.template  
**Type:** ConfigurationFile  
**Relative Path:** runtimes/custom-python/src/requirements.txt.template  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    
**Requirement Ids:**
    
    - INT-007 (Custom AI model hosting - K8s deployment)
    
**Purpose:** To list Python dependencies required by the custom AI model serving application.  
**Logic Description:** fastapi
uvicorn[standard]
# scikit-learn
# pandas
# numpy
# tensorflow or torch (if used directly)
# other_dependencies  
**Documentation:**
    
    - **Summary:** A template 'requirements.txt' file for specifying Python package dependencies for a custom model server. Common libraries like FastAPI, Uvicorn, and machine learning framework libraries would be listed here.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** models/example-image-classification-tf/deployment.yaml  
**Description:** Specific Kubernetes Deployment for an example TensorFlow image classification model served with TensorFlow Serving.  
**Template:** Kubernetes YAML  
**Dependency Level:** 3  
**Name:** deployment  
**Type:** KubernetesManifest  
**Relative Path:** models/example-image-classification-tf/deployment.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Deployment
    - GPU Resource Allocation
    - Volume Mounting for Models
    
**Requirement Ids:**
    
    - INT-007
    - DEP-001
    
**Purpose:** To deploy a specific TensorFlow image classification model using a pre-built TensorFlow Serving image, mounting model files from a ConfigMap or PersistentVolume.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-image-classifier
  namespace: ai-serving
  labels:
    app: tf-serving-image-classifier
    model: image-classification
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tf-serving-image-classifier
  template:
    metadata:
      labels:
        app: tf-serving-image-classifier
    spec:
      serviceAccountName: model-server-sa
      containers:
      - name: tf-serving-container
        image: tensorflow/serving:latest-gpu # Use GPU enabled image
        args:
        - --port=8500
        - --rest_api_port=8501
        - --model_config_file=/models/models.config
        ports:
        - containerPort: 8500
        - containerPort: 8501
        volumeMounts:
        - name: model-config-volume
          mountPath: /models/models.config
          subPath: models.config
        # Example of mounting model files from a PV if not baked into image
        # - name: model-files-pv
        #   mountPath: /models/image_classifier_model # Corresponds to base_path in models.config
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "4Gi"
            cpu: "2"
          requests:
            nvidia.com/gpu: 1
            memory: "2Gi"
            cpu: "1"
      volumes:
      - name: model-config-volume
        configMap:
          name: tf-serving-image-classifier-models-config
      # - name: model-files-pv
      #   persistentVolumeClaim:
      #     claimName: image-classifier-model-pvc  
**Documentation:**
    
    - **Summary:** Deploys an example image classification TensorFlow model using TensorFlow Serving. It uses a ConfigMap for the models.config file and assumes the actual model files are either baked into a custom image or mounted via a PersistentVolumeClaim (commented out example).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesDeployment
    
- **Path:** models/example-image-classification-tf/service.yaml  
**Description:** Kubernetes Service for the example TensorFlow image classification model.  
**Template:** Kubernetes YAML  
**Dependency Level:** 3  
**Name:** service  
**Type:** KubernetesManifest  
**Relative Path:** models/example-image-classification-tf/service.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Exposure
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To expose the TensorFlow image classification model serving deployment.  
**Logic Description:** apiVersion: v1
kind: Service
metadata:
  name: tf-serving-image-classifier-svc
  namespace: ai-serving
  labels:
    app: tf-serving-image-classifier
spec:
  selector:
    app: tf-serving-image-classifier
  ports:
  - name: grpc
    port: 8500
    targetPort: 8500
  - name: rest
    port: 8501
    targetPort: 8501
  type: ClusterIP  
**Documentation:**
    
    - **Summary:** Exposes the 'tf-serving-image-classifier' Deployment internally within the cluster using a ClusterIP Service for gRPC and REST traffic.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesNetwork
    
- **Path:** models/example-image-classification-tf/configmap-models-config.yaml  
**Description:** ConfigMap containing the models.config for the example TensorFlow image classification model.  
**Template:** Kubernetes YAML  
**Dependency Level:** 3  
**Name:** configmap-models-config  
**Type:** KubernetesManifest  
**Relative Path:** models/example-image-classification-tf/configmap-models-config.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Server Configuration
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To provide the specific models.config file for the image classification model.  
**Logic Description:** apiVersion: v1
kind: ConfigMap
metadata:
  name: tf-serving-image-classifier-models-config
  namespace: ai-serving
data:
  models.config: |
    model_config_list: {
      config: {
        name: "image_classifier_model",
        base_path: "/models/image_classifier_model/", # This path must exist in the container, typically mounted or part of image
        model_platform: "tensorflow",
        model_version_policy: { latest: { num_versions: 1 } }
      }
    }  
**Documentation:**
    
    - **Summary:** This ConfigMap provides the 'models.config' specifically for the 'image_classifier_model'. It tells TensorFlow Serving to load the latest version of this model from the specified 'base_path' within the container.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** models/example-text-generation-gpt/hpa.yaml  
**Description:** HorizontalPodAutoscaler for an example text generation model.  
**Template:** Kubernetes YAML  
**Dependency Level:** 4  
**Name:** hpa  
**Type:** KubernetesManifest  
**Relative Path:** models/example-text-generation-gpt/hpa.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Horizontal Pod Autoscaling
    
**Requirement Ids:**
    
    - NFR-002 (Scalable GPU orchestration)
    - DEP-001 (AI Processing Cluster hardware and K8s orchestration)
    
**Purpose:** To automatically scale the number of pods for the 'custom-py-server-text-generation' Deployment based on CPU utilization.  
**Logic Description:** apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: text-generation-hpa
  namespace: ai-serving
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: custom-py-server-text-generation # Assumes a Deployment with this name exists
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # - type: Resource  # Example for GPU based scaling if metrics server supports nvidia.com/gpu
  #   resource:
  #     name: nvidia.com/gpu
  #     target:
  #       type: Utilization # Or AverageValue
  #       averageUtilization: 75  
**Documentation:**
    
    - **Summary:** Defines a HorizontalPodAutoscaler (HPA) for the 'custom-py-server-text-generation' model deployment. It will scale the number of pods between 1 and 5 based on average CPU utilization, targeting 70%. GPU-based scaling example is commented out as it requires specific metrics server setup.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesAutoscaling
    
- **Path:** models/example-text-generation-gpt/secret.placeholder.yaml  
**Description:** Placeholder for Kubernetes Secret for the example text generation model, e.g., for API keys if it calls external services. Actual values sourced from HashiCorp Vault.  
**Template:** Kubernetes YAML  
**Dependency Level:** 3  
**Name:** secret.placeholder  
**Type:** KubernetesManifest  
**Relative Path:** models/example-text-generation-gpt/secret.placeholder.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Secure Secret Injection Placeholder
    
**Requirement Ids:**
    
    - INT-007
    
**Purpose:** To define the structure of a Kubernetes Secret that the text generation model might need. Actual secret values are managed externally in HashiCorp Vault and injected during deployment.  
**Logic Description:** apiVersion: v1
kind: Secret
metadata:
  name: text-generation-model-secrets
  namespace: ai-serving
type: Opaque
# Data should be base64 encoded. Values below are placeholders.
# Actual values will be injected from HashiCorp Vault by the CI/CD pipeline or a secrets operator.
data:
  # EXAMPLE_API_KEY: "cGxhY2Vob2xkZXJfYXBpX2tleV92YWx1ZQ==" # placeholder_api_key_value
  # ANOTHER_SECRET: "cGxhY2Vob2xkZXJfc2VjcmV0X3ZhbHVl"
  # For Vault integration, this manifest might be managed by a Vault agent/injector or templated by CI/CD.
  # Ensure this file is NOT committed with actual secret values.  
**Documentation:**
    
    - **Summary:** This is a placeholder for a Kubernetes Secret. It defines the expected keys that a model might need (e.g., API keys for external services). The actual base64 encoded secret values are NOT stored here; they are injected from a secure secrets management system like HashiCorp Vault during the deployment process (dependency REPO-SECRETS-MANAGEMENT-001).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** config/overlays/development/kustomization.yaml  
**Description:** Kustomize configuration for the development environment overlay.  
**Template:** Kubernetes Kustomization  
**Dependency Level:** 4  
**Name:** kustomization  
**Type:** KubernetesManifest  
**Relative Path:** config/overlays/development/kustomization.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Environment Configuration
    - Kustomize Overlay
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To define Kustomize overlays for tailoring AI serving deployments to the development environment.  
**Logic Description:** apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: ai-serving

# Specify base resources common to all environments
# This might point to ../../base or specific models under ../../models/
resources:
  - ../../../base # Includes namespace, common rbac, etc.
  - ../../../models/example-image-classification-tf
  - ../../../models/example-text-generation-gpt # Assuming it has its own base deployment.yaml

# Patches specific to development environment
patchesStrategicMerge:
  - patch-replicas-dev.yaml
  - patch-resources-dev.yaml

# Example: Add a common label to all resources for this overlay
commonLabels:
  environment: development  
**Documentation:**
    
    - **Summary:** This Kustomization file defines the development environment specific configurations. It references base Kubernetes manifests and applies development-specific patches (e.g., for replica counts, resource requests/limits) using Kustomize.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** config/overlays/development/patch-replicas-dev.yaml  
**Description:** Kustomize patch to set replica counts for development.  
**Template:** Kubernetes YAML  
**Dependency Level:** 4  
**Name:** patch-replicas-dev  
**Type:** KubernetesManifest  
**Relative Path:** config/overlays/development/patch-replicas-dev.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Patching
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To reduce replica counts for deployments in the development environment.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-image-classifier # Target specific deployment
  namespace: ai-serving
spec:
  replicas: 1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-py-server-text-generation # Target another deployment
  namespace: ai-serving
spec:
  replicas: 1  
**Documentation:**
    
    - **Summary:** A Kustomize patch file that modifies the 'replicas' field for specified Deployments, typically setting them to a lower value (e.g., 1) for development environments to conserve resources.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** config/overlays/production/kustomization.yaml  
**Description:** Kustomize configuration for the production environment overlay.  
**Template:** Kubernetes Kustomization  
**Dependency Level:** 4  
**Name:** kustomization  
**Type:** KubernetesManifest  
**Relative Path:** config/overlays/production/kustomization.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Environment Configuration
    - Kustomize Overlay
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    
**Purpose:** To define Kustomize overlays for tailoring AI serving deployments to the production environment.  
**Logic Description:** apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: ai-serving

resources:
  - ../../../base
  - ../../../models/example-image-classification-tf
  - ../../../models/example-text-generation-gpt

patchesStrategicMerge:
  - patch-replicas-prod.yaml
  - patch-resources-prod.yaml
  # Potentially HPA configurations specific to prod or more aggressive settings
  # - ../../../models/example-text-generation-gpt/hpa.yaml # If HPA is only for prod

commonLabels:
  environment: production  
**Documentation:**
    
    - **Summary:** This Kustomization file defines production-specific configurations. It references base manifests and applies production-level patches (e.g., higher replica counts, robust resource limits, enabling HPA).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    
- **Path:** config/overlays/production/patch-replicas-prod.yaml  
**Description:** Kustomize patch to set replica counts for production.  
**Template:** Kubernetes YAML  
**Dependency Level:** 4  
**Name:** patch-replicas-prod  
**Type:** KubernetesManifest  
**Relative Path:** config/overlays/production/patch-replicas-prod.yaml  
**Repository Id:** REPO-K8S-AISERVINGMANIFESTS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Patching
    
**Requirement Ids:**
    
    - Section 2.4 (AI Processing environment on K8s)
    - NFR-002
    
**Purpose:** To set appropriate replica counts for deployments in the production environment for scalability and availability.  
**Logic Description:** apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-image-classifier
  namespace: ai-serving
spec:
  replicas: 3 # Example for production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-py-server-text-generation
  namespace: ai-serving
spec:
  replicas: 2 # Example for production  
**Documentation:**
    
    - **Summary:** A Kustomize patch file that modifies the 'replicas' field for specified Deployments, setting them to higher values suitable for production load and high availability.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** KubernetesConfiguration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

