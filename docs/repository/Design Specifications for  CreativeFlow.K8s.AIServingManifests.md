# Software Design Specification: CreativeFlow.K8s.AIServingManifests

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.K8s.AIServingManifests` repository. This repository is responsible for storing, managing, and versioning all Kubernetes manifests (YAML), Dockerfiles, and related configurations necessary for deploying and managing AI models on the GPU-accelerated AI processing cluster within the CreativeFlow AI platform. These artifacts enable the standardized, repeatable, and scalable deployment of various AI model serving runtimes and custom AI models.

### 1.2 Scope
The scope of this repository includes:
*   Base Kubernetes configurations for the `ai-serving` namespace, including RBAC and resource management.
*   Dockerfile templates for containerizing AI models for different serving runtimes (TensorFlow Serving, TorchServe, NVIDIA Triton Inference Server, custom Python servers).
*   Kubernetes manifest templates (Deployments, Services, ConfigMaps, HPAs) for each supported serving runtime.
*   Concrete examples of model deployments using these templates.
*   Kustomize overlays for managing environment-specific configurations (development, production).
*   Placeholders and guidance for integrating with external secrets management (e.g., HashiCorp Vault).
*   Documentation related to model repository structures and custom server wrappers.

This repository *does not* include:
*   The AI models themselves (these are managed by the MLOps Platform Service and stored elsewhere).
*   The CI/CD pipeline definitions for deploying these manifests (managed in a separate DevOps repository).
*   The actual secret values (managed in HashiCorp Vault).
*   Cluster-level setup scripts for Kubernetes itself or the NVIDIA GPU Operator (though placeholders for configuration awareness are included).

### 1.3 Definitions, Acronyms, and Abbreviations
*   **K8s**: Kubernetes
*   **AI**: Artificial Intelligence
*   **ML**: Machine Learning
*   **GPU**: Graphics Processing Unit
*   **YAML**: YAML Ain't Markup Language
*   **Dockerfile**: A text document that contains all the commands a user could call on the command line to assemble an image.
*   **Deployment**: A Kubernetes object that manages a replicated application.
*   **Service**: A Kubernetes object that defines a logical set of Pods and a policy by which to access them.
*   **ConfigMap**: A Kubernetes object used to store non-confidential data in key-value pairs.
*   **Secret**: A Kubernetes object used to store sensitive data, such as passwords, OAuth tokens, and ssh keys.
*   **RBAC**: Role-Based Access Control
*   **HPA**: Horizontal Pod Autoscaler
*   **PDB**: Pod Disruption Budget
*   **TF Serving**: TensorFlow Serving
*   **TorchServe**: PyTorch Serve
*   **Triton**: NVIDIA Triton Inference Server
*   **IaC**: Infrastructure as Code
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **MVP**: Minimum Viable Product
*   **DR**: Disaster Recovery
*   **SDS**: Software Design Specification

## 2. General Design Principles for Kubernetes Manifests & Dockerfiles

### 2.1 Idempotency and Declarative Configuration
All Kubernetes manifests shall be declarative, describing the desired state of the system. Applying the same manifest multiple times should result in the same state. Dockerfiles should be written to produce consistent images given the same build context.

### 2.2 Parameterization and Templating
*   **Placeholders**: Manifest and Dockerfile templates will use clear placeholders (e.g., `__MODEL_NAME_PLACEHOLDER__`, `__IMAGE_TAG_PLACEHOLDER__`, `__GPU_COUNT_PLACEHOLDER__`) to be replaced by the CI/CD pipeline or MLOps service during deployment.
*   **Kustomize**: Kustomize will be used for managing environment-specific configurations (development, staging, production) by overlaying patches onto base manifests. This promotes DRY (Don't Repeat Yourself) principles.

### 2.3 Security Best Practices
*   **Least Privilege**: ServiceAccounts and Roles will be defined with the minimum necessary permissions.
*   **Secrets Management**: Actual secret values will **never** be hardcoded in manifests. Kubernetes Secrets will either be placeholders populated from HashiCorp Vault via a secrets operator/injector or templated by the CI/CD pipeline with values fetched from Vault.
*   **Container Security**: Dockerfiles will use official and minimal base images where possible. Root privileges will be avoided inside containers unless absolutely necessary. Regular scanning of base images and application dependencies for vulnerabilities is assumed as part of the CI/CD process (handled by other repositories/processes).
*   **Network Policies**: While not explicitly defined in this repository, NetworkPolicies should be considered and implemented at the cluster level or within the `ai-serving` namespace to restrict traffic flow between pods.

### 2.4 Resource Management
*   **Requests and Limits**: All Deployments will specify CPU, memory, and GPU resource requests and limits for containers to ensure predictable performance and resource allocation. These will be parameterized for Kustomize overlays.
*   **ResourceQuotas and LimitRanges**: Namespace-level ResourceQuotas and LimitRanges will be defined to manage aggregate resource consumption and provide default requests/limits.

### 2.5 Versioning
*   **Manifests and Dockerfiles**: All artifacts in this repository will be version-controlled using Git.
*   **Container Images**: Docker images built from these Dockerfiles will be tagged with semantic versioning or commit SHA, managed by the CI/CD pipeline.
*   **Model Versions**: Model serving deployments will support serving specific model versions, typically managed by the model server itself (e.g., TF Serving `models.config`, Triton model repository structure) or by deploying different image tags containing specific model versions.

## 3. Kubernetes Manifest Specifications

All manifests will use `apiVersion` and `kind` appropriate for Kubernetes `v1.29.2` or as specified by the respective Custom Resource Definitions (CRDs) if any are used.

### 3.1 Namespace Configuration (`base/namespace.yaml`)
*   **Purpose**: To create a dedicated Kubernetes namespace `ai-serving` for isolating all AI model deployment resources, enhancing organization and security.
*   **File**: `base/namespace.yaml`
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: ai-serving
      labels:
        name: ai-serving
        project: creativeflow
        tier: ai-processing
    

### 3.2 Role-Based Access Control (RBAC) (`base/rbac/`)
Provides the necessary permissions for AI model serving pods.

#### 3.2.1 ServiceAccount (`base/rbac/serviceaccount-model-server.yaml`)
*   **Purpose**: To define a specific identity (`model-server-sa`) for AI model serving pods within the `ai-serving` namespace.
*   **File**: `base/rbac/serviceaccount-model-server.yaml`
*   **Specification**:
    yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: model-server-sa
      namespace: ai-serving
      labels:
        app.kubernetes.io/name: model-server
        app.kubernetes.io/part-of: ai-serving
    

#### 3.2.2 Role (`base/rbac/role-model-reader.yaml`)
*   **Purpose**: To define a Role (`model-reader-role`) granting read-only access to ConfigMaps and Secrets, which might be needed by model servers for configuration.
*   **File**: `base/rbac/role-model-reader.yaml`
*   **Specification**:
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: ai-serving
      name: model-reader-role
      labels:
        app.kubernetes.io/name: model-reader
        app.kubernetes.io/part-of: ai-serving
    rules:
    - apiGroups: [""] # Core API group
      resources: ["configmaps", "secrets"]
      verbs: ["get", "watch", "list"]
    # Add other permissions if model servers need to interact with K8s API, e.g., leader election or pod discovery
    # - apiGroups: ["coordination.k8s.io"]
    #   resources: ["leases"]
    #   verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
    # - apiGroups: [""]
    #   resources: ["pods"]
    #   verbs: ["get", "list", "watch"]
    

#### 3.2.3 RoleBinding (`base/rbac/rolebinding-model-server.yaml`)
*   **Purpose**: To bind the `model-reader-role` to the `model-server-sa` ServiceAccount, granting its associated pods the defined permissions.
*   **File**: `base/rbac/rolebinding-model-server.yaml`
*   **Specification**:
    yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: model-server-rb
      namespace: ai-serving
      labels:
        app.kubernetes.io/name: model-server-binding
        app.kubernetes.io/part-of: ai-serving
    subjects:
    - kind: ServiceAccount
      name: model-server-sa
      namespace: ai-serving
    roleRef:
      kind: Role
      name: model-reader-role
      apiGroup: rbac.authorization.k8s.io
    

### 3.3 Resource Management (`base/resource-management/`)

#### 3.3.1 ResourceQuota (`base/resource-management/resourcequota.yaml`)
*   **Purpose**: To set overall resource limits (CPU, memory, GPU, pods) for the `ai-serving` namespace to prevent resource starvation and manage costs.
*   **File**: `base/resource-management/resourcequota.yaml`
*   **Specification**:
    yaml
    apiVersion: v1
    kind: ResourceQuota
    metadata:
      name: ai-serving-quota
      namespace: ai-serving
      labels:
        app.kubernetes.io/part-of: ai-serving-platform-governance
    spec:
      hard:
        requests.cpu: "20"           # Total CPU requests allowed in the namespace
        requests.memory: 100Gi       # Total memory requests
        limits.cpu: "40"             # Total CPU limits
        limits.memory: 200Gi          # Total memory limits
        nvidia.com/gpu: "4"          # Total NVIDIA GPUs requestable (matches DEP-001 initial capacity)
        pods: "50"                   # Max number of pods
        count/services: "30"         # Max number of services
        count/configmaps: "100"      # Max number of configmaps
        # Add other resources as needed e.g. persistentvolumeclaims
    
    *Notes*: Values are illustrative and should be adjusted based on cluster capacity and expected workload as per `DEP-001`.

#### 3.3.2 LimitRange (`base/resource-management/limitrange.yaml`)
*   **Purpose**: To set default CPU and memory requests/limits for containers within the `ai-serving` namespace if they are not explicitly defined in pod specifications.
*   **File**: `base/resource-management/limitrange.yaml`
*   **Specification**:
    yaml
    apiVersion: v1
    kind: LimitRange
    metadata:
      name: ai-serving-default-limits
      namespace: ai-serving
      labels:
        app.kubernetes.io/part-of: ai-serving-platform-governance
    spec:
      limits:
      - type: Container
        default: # Default limit if only request is specified
          memory: "1Gi"
          cpu: "500m"
        defaultRequest: # Default request if not specified
          memory: "512Mi"
          cpu: "250m"
        max: # Max limit a container can request
          memory: "64Gi" # Example, adjust based on node capacity
          cpu: "8"       # Example
        min: # Min limit a container can request
          memory: "128Mi"
          cpu: "100m"
        # maxLimitRequestRatio: # Optional: e.g., cpu: 10 means limit can be 10x request
    
    *Notes*: GPU resources are typically explicitly requested and limited per pod due to their nature and cost, so not usually defaulted via LimitRange.

### 3.4 GPU Operator Configuration (`base/cluster-setup/gpu-operator-values.placeholder.yaml`)
*   **Purpose**: To act as a placeholder for NVIDIA GPU Operator configurations. The actual operator installation is a cluster-wide prerequisite. This file acknowledges its importance.
*   **File**: `base/cluster-setup/gpu-operator-values.placeholder.yaml`
*   **Specification**:
    yaml
    # This file is a placeholder and a reminder.
    # NVIDIA GPU Operator is a cluster-level component essential for GPU workloads.
    # Its installation and configuration are managed separately, often via Helm.
    # Ensure the operator is installed and functional, making 'nvidia.com/gpu' resources available.
    #
    # Example Helm values (DO NOT COMMIT ACTUAL VALUES HERE):
    # driver:
    #   enabled: true
    # toolkit:
    #   enabled: true
    # operator:
    #   defaultRuntime: nvidia # Ensure container runtime is configured for NVIDIA GPUs
    # mig: # Optional: Configure MIG strategy if applicable
    #   strategy: "single" # or "mixed"
    

### 3.5 Model Serving Runtime Manifest Templates (`runtimes/`)
These templates will be used as a basis for deploying models. Placeholders will be substituted by the MLOps service or CI/CD pipeline.

Common labels for all model serving deployments:
yaml
labels:
  app.kubernetes.io/name: __APP_NAME_PLACEHOLDER__ # e.g., tf-serving-my-model
  app.kubernetes.io/instance: __INSTANCE_NAME_PLACEHOLDER__ # e.g., my-model-v1
  app.kubernetes.io/version: __MODEL_VERSION_PLACEHOLDER__ # e.g., 1.2.3 or image tag
  app.kubernetes.io/component: model-server
  app.kubernetes.io/part-of: ai-serving-platform
  app.kubernetes.io/managed-by: kustomize # or helm, argo-cd etc.
  creativeflow.ai/model-family: __MODEL_FAMILY_PLACEHOLDER__ # e.g., image-classification
  creativeflow.ai/runtime: __RUNTIME_PLACEHOLDER__ # e.g., tensorflow-serving


#### 3.5.1 TensorFlow Serving (`runtimes/tensorflow-serving/`)

##### 3.5.1.1 Deployment (`deployment.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: tf-serving-__MODEL_NAME_PLACEHOLDER__
      namespace: ai-serving
      labels:
        app: tf-serving-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: tensorflow-serving
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      replicas: __REPLICA_COUNT_PLACEHOLDER__ # e.g., 1 for dev, 3 for prod
      selector:
        matchLabels:
          app: tf-serving-__MODEL_NAME_PLACEHOLDER__
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
      template:
        metadata:
          labels:
            app: tf-serving-__MODEL_NAME_PLACEHOLDER__
            creativeflow.ai/runtime: tensorflow-serving
            creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
        spec:
          serviceAccountName: model-server-sa
          # nodeSelector: # Optional: if you have specific GPU nodes
          #   gpu-type: nvidia-tesla-t4
          # tolerations: # Optional: if GPU nodes have taints
          # - key: "nvidia.com/gpu"
          #   operator: "Exists"
          #   effect: "NoSchedule"
          containers:
          - name: tf-serving-container
            image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__ # e.g., creativeflow/tf-my-model:1.0
            imagePullPolicy: IfNotPresent
            args: # These args depend on how the Docker image is built and models are provided
            - --port=8500
            - --rest_api_port=8501
            - --model_name=__TF_MODEL_SERVING_NAME_PLACEHOLDER__ # Name TF Serving uses internally
            - --model_base_path=/models/__TF_MODEL_SERVING_NAME_PLACEHOLDER__
            # OR using model_config_file:
            # - --model_config_file=/models/models.config 
            # - --model_config_file_poll_wait_seconds=60 # Optional: poll for config changes
            ports:
            - name: grpc
              containerPort: 8500
              protocol: TCP
            - name: rest
              containerPort: 8501
              protocol: TCP
            env:
            - name: MODEL_NAME 
              value: "__TF_MODEL_SERVING_NAME_PLACEHOLDER__"
            # - name: TF_CPP_MIN_LOG_LEVEL
            #   value: "2" # Suppress verbose TensorFlow logs
            resources:
              limits:
                nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__ # e.g., 1
                memory: "__MEMORY_LIMIT_PLACEHOLDER__" # e.g., "4Gi"
                cpu: "__CPU_LIMIT_PLACEHOLDER__"     # e.g., "2"
              requests:
                nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
                memory: "__MEMORY_REQUEST_PLACEHOLDER__" # e.g., "2Gi"
                cpu: "__CPU_REQUEST_PLACEHOLDER__"     # e.g., "1"
            readinessProbe:
              httpGet:
                path: /v1/models/__TF_MODEL_SERVING_NAME_PLACEHOLDER__ # Check if model is loaded
                port: 8501
              initialDelaySeconds: 30 # Give time for model to load
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /v1/models/__TF_MODEL_SERVING_NAME_PLACEHOLDER__
                port: 8501
              initialDelaySeconds: 60
              periodSeconds: 20
              timeoutSeconds: 5
              failureThreshold: 3
            # volumeMounts: # If using ConfigMap for models.config
            # - name: model-config-volume
            #   mountPath: /models/models.config
            #   subPath: models.config
            # - name: model-data-volume # If mounting model data via PV
            #   mountPath: /models/__TF_MODEL_SERVING_NAME_PLACEHOLDER__
          # volumes: # If using ConfigMap for models.config
          # - name: model-config-volume
          #   configMap:
          #     name: tf-serving-__MODEL_NAME_PLACEHOLDER__-models-config
          # - name: model-data-volume # If mounting model data via PV
          #   persistentVolumeClaim:
          #     claimName: __PVC_NAME_PLACEHOLDER__ 
    

##### 3.5.1.2 Service (`service.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: tf-serving-__MODEL_NAME_PLACEHOLDER__-svc
      namespace: ai-serving
      labels:
        app: tf-serving-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: tensorflow-serving
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      selector:
        app: tf-serving-__MODEL_NAME_PLACEHOLDER__
      ports:
      - name: grpc
        port: 8500
        targetPort: grpc
        protocol: TCP
      - name: rest
        port: 8501
        targetPort: rest
        protocol: TCP
      type: ClusterIP # Default, suitable for internal access
    

##### 3.5.1.3 ConfigMap for `models.config` (`configmap-models.template.yaml`)
*   **Purpose**: To provide `models.config` to TF Serving, allowing flexible model loading.
*   **Specification**:
    yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: tf-serving-__MODEL_NAME_PLACEHOLDER__-models-config
      namespace: ai-serving
      labels:
        app: tf-serving-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: tensorflow-serving
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    data:
      models.config: |
        model_config_list: {
          config: {
            name: "__TF_MODEL_SERVING_NAME_PLACEHOLDER__",
            base_path: "/models/__TF_MODEL_SERVING_NAME_PLACEHOLDER__/",
            model_platform: "tensorflow",
            model_version_policy: { __VERSION_POLICY_PLACEHOLDER__: {} } // e.g., latest: { num_versions: 1 } or all: {}
            // version_labels: { "stable": 1, "canary": 2} // Optional
          }
          // Add more model configs here if this TF Serving instance serves multiple models
        }
    

#### 3.5.2 TorchServe (`runtimes/torchserve/`)

##### 3.5.2.1 Deployment (`deployment.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: torchserve-__MODEL_NAME_PLACEHOLDER__
      namespace: ai-serving
      labels:
        app: torchserve-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: torchserve
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      replicas: __REPLICA_COUNT_PLACEHOLDER__
      selector:
        matchLabels:
          app: torchserve-__MODEL_NAME_PLACEHOLDER__
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
      template:
        metadata:
          labels:
            app: torchserve-__MODEL_NAME_PLACEHOLDER__
            creativeflow.ai/runtime: torchserve
            creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
        spec:
          serviceAccountName: model-server-sa
          containers:
          - name: torchserve-container
            image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__ # e.g., creativeflow/torchserve-my-model:1.0
            imagePullPolicy: IfNotPresent
            args: # Assumes Docker image copies .mar file and config.properties if needed
            - torchserve
            - --start
            - --ts-config=/home/model-server/config.properties # If using custom config
            - --model-store=/home/model-server/model-store
            - --models # Specify models to load at startup
            - __TORCHSERVE_MODEL_NAME_PLACEHOLDER__=__MAR_FILE_NAME_PLACEHOLDER__ # e.g., my_classifier=my_classifier.mar
            # - all # Or load all models in model_store
            ports:
            - name: inference
              containerPort: 8080
              protocol: TCP
            - name: management
              containerPort: 8081
              protocol: TCP
            - name: metrics
              containerPort: 8082
              protocol: TCP
            env:
            - name: JAVA_TOOL_OPTIONS # Optional: For JVM tuning
              value: "-Xmx__JVM_MAX_HEAP_PLACEHOLDER__ -Xms__JVM_MIN_HEAP_PLACEHOLDER__"
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
                path: /ping # TorchServe management API
                port: management # Port 8081
              initialDelaySeconds: 45 # TorchServe and model loading can take time
              periodSeconds: 15
              timeoutSeconds: 5
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /ping
                port: management
              initialDelaySeconds: 90
              periodSeconds: 30
              timeoutSeconds: 5
              failureThreshold: 3
            # volumeMounts: # If config.properties is from a ConfigMap
            # - name: torchserve-config-volume
            #   mountPath: /home/model-server/config.properties
            #   subPath: config.properties
            # - name: model-store-volume # If mounting model store via PV
            #   mountPath: /home/model-server/model-store
          # volumes:
          # - name: torchserve-config-volume
          #   configMap:
          #     name: torchserve-__MODEL_NAME_PLACEHOLDER__-config
          # - name: model-store-volume
          #   persistentVolumeClaim:
          #     claimName: __PVC_MODEL_STORE_PLACEHOLDER__
    

##### 3.5.2.2 Service (`service.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: torchserve-__MODEL_NAME_PLACEHOLDER__-svc
      namespace: ai-serving
      labels:
        app: torchserve-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: torchserve
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      selector:
        app: torchserve-__MODEL_NAME_PLACEHOLDER__
      ports:
      - name: inference
        port: 8080
        targetPort: inference
        protocol: TCP
      - name: management
        port: 8081
        targetPort: management
        protocol: TCP
      - name: metrics
        port: 8082
        targetPort: metrics
        protocol: TCP
      type: ClusterIP
    
*   *(ConfigMap for `config.properties` can be added if complex configurations are needed)*

#### 3.5.3 NVIDIA Triton Inference Server (`runtimes/triton-inference-server/`)

##### 3.5.3.1 Deployment (`deployment.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
      namespace: ai-serving
      labels:
        app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: triton-inference-server
        creativeflow.ai/model-collection: __MODEL_COLLECTION_NAME_PLACEHOLDER__
    spec:
      replicas: __REPLICA_COUNT_PLACEHOLDER__
      selector:
        matchLabels:
          app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
      template:
        metadata:
          labels:
            app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
            creativeflow.ai/runtime: triton-inference-server
            creativeflow.ai/model-collection: __MODEL_COLLECTION_NAME_PLACEHOLDER__
        spec:
          serviceAccountName: model-server-sa
          containers:
          - name: triton-server-container
            image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__ # e.g., creativeflow/triton-my-collection:1.0
            imagePullPolicy: IfNotPresent
            args:
            - tritonserver
            - --model-repository=/models # Assumes Docker image has models at /models
            - --strict-model-config=false # Or true based on needs
            # - --log-verbose=1 # For more logs
            ports:
            - name: http
              containerPort: 8000
              protocol: TCP
            - name: grpc
              containerPort: 8001
              protocol: TCP
            - name: metrics
              containerPort: 8002
              protocol: TCP
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
                port: http # Port 8000
              initialDelaySeconds: 30 # Triton can take time to load models
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /v2/health/live
                port: http
              initialDelaySeconds: 60
              periodSeconds: 20
              timeoutSeconds: 5
              failureThreshold: 3
            # volumeMounts: # If model repository is mounted from PV
            # - name: model-repository-volume
            #   mountPath: /models
          # volumes:
          # - name: model-repository-volume
          #   persistentVolumeClaim:
          #     claimName: __PVC_MODEL_REPO_PLACEHOLDER__
    

##### 3.5.3.2 Service (`service.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__-svc
      namespace: ai-serving
      labels:
        app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: triton-inference-server
        creativeflow.ai/model-collection: __MODEL_COLLECTION_NAME_PLACEHOLDER__
    spec:
      selector:
        app: triton-server-__MODEL_COLLECTION_NAME_PLACEHOLDER__
      ports:
      - name: http
        port: 8000
        targetPort: http
        protocol: TCP
      - name: grpc
        port: 8001
        targetPort: grpc
        protocol: TCP
      - name: metrics
        port: 8002
        targetPort: metrics
        protocol: TCP
      type: ClusterIP
    

#### 3.5.4 Custom Python Server (`runtimes/custom-python/`)

##### 3.5.4.1 Deployment (`deployment.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: custom-py-server-__MODEL_NAME_PLACEHOLDER__
      namespace: ai-serving
      labels:
        app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: custom-python
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      replicas: __REPLICA_COUNT_PLACEHOLDER__
      selector:
        matchLabels:
          app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
      template:
        metadata:
          labels:
            app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
            creativeflow.ai/runtime: custom-python
            creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
        spec:
          serviceAccountName: model-server-sa
          containers:
          - name: custom-py-server-container
            image: __IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__ # e.g., creativeflow/custom-my-model:1.0
            imagePullPolicy: IfNotPresent
            ports:
            - name: http # Or whatever name is appropriate
              containerPort: __CONTAINER_PORT_PLACEHOLDER__ # e.g., 8000
              protocol: TCP
            envFrom: # Example for loading secrets or configmaps as env vars
            - secretRef:
                name: __SECRET_NAME_PLACEHOLDER__ # Optional
            # - configMapRef:
            #     name: __CONFIGMAP_NAME_PLACEHOLDER__ # Optional
            resources:
              limits:
                nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__ # 0 if no GPU needed
                memory: "__MEMORY_LIMIT_PLACEHOLDER__"
                cpu: "__CPU_LIMIT_PLACEHOLDER__"
              requests:
                nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
                memory: "__MEMORY_REQUEST_PLACEHOLDER__"
                cpu: "__CPU_REQUEST_PLACEHOLDER__"
            readinessProbe:
              httpGet:
                path: __READINESS_PROBE_PATH_PLACEHOLDER__ # e.g., /health/ready
                port: __CONTAINER_PORT_PLACEHOLDER__
              initialDelaySeconds: 15
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: __LIVENESS_PROBE_PATH_PLACEHOLDER__ # e.g., /health/live
                port: __CONTAINER_PORT_PLACEHOLDER__
              initialDelaySeconds: 30
              periodSeconds: 20
              timeoutSeconds: 5
              failureThreshold: 3
            # volumeMounts: # Example for mounting model artifacts or config
            # - name: model-artifact-volume
            #   mountPath: /app/model_artifacts
            # - name: app-config-volume
            #   mountPath: /app/config
          # volumes:
          # - name: model-artifact-volume
          #   persistentVolumeClaim:
          #     claimName: __PVC_MODEL_ARTIFACT_PLACEHOLDER__
          # - name: app-config-volume
          #   configMap:
          #     name: __APP_CONFIGMAP_NAME_PLACEHOLDER__
    

##### 3.5.4.2 Service (`service.template.yaml`)
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: custom-py-server-__MODEL_NAME_PLACEHOLDER__-svc
      namespace: ai-serving
      labels:
        app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
        creativeflow.ai/runtime: custom-python
        creativeflow.ai/model-name: __MODEL_NAME_PLACEHOLDER__
    spec:
      selector:
        app: custom-py-server-__MODEL_NAME_PLACEHOLDER__
      ports:
      - name: http # Or whatever name is appropriate
        port: 80 # External port for the service
        targetPort: __CONTAINER_PORT_PLACEHOLDER__ # Matches containerPort in Deployment
        protocol: TCP
      type: ClusterIP
    

### 3.6 Model-Specific Deployment Examples (`models/`)
These will be concrete instantiations of the templates above, demonstrating how to deploy specific types of models.

#### 3.6.1 Example: TensorFlow Image Classification
*   **`models/example-image-classification-tf/deployment.yaml`**:
    *   This will be an instantiation of `runtimes/tensorflow-serving/deployment.template.yaml`.
    *   Placeholders like `__MODEL_NAME_PLACEHOLDER__` will be `image-classifier`, `__TF_MODEL_SERVING_NAME_PLACEHOLDER__` will be `image_classifier_model`.
    *   Image will point to a pre-built TF Serving image or a custom one built using the TF Serving Dockerfile template that includes the model.
    *   Appropriate GPU count (e.g., 1), memory, and CPU resources will be set.
    *   It will reference `tf-serving-image-classifier-models-config` ConfigMap.
*   **`models/example-image-classification-tf/service.yaml`**:
    *   Instantiation of `runtimes/tensorflow-serving/service.template.yaml` with `image-classifier` specific names.
*   **`models/example-image-classification-tf/configmap-models-config.yaml`**:
    *   Instantiation of `runtimes/tensorflow-serving/configmap-models.template.yaml`.
    *   `__TF_MODEL_SERVING_NAME_PLACEHOLDER__` replaced with `image_classifier_model`.
    *   `base_path` will be `/models/image_classifier_model/`.
    *   `model_version_policy` set to serve latest version: `{ latest: { num_versions: 1 } }`.

#### 3.6.2 Example: Custom Python Text Generation

##### `models/example-text-generation-gpt/deployment.yaml` (Illustrative)
*   This would be an instantiation of `runtimes/custom-python/deployment.template.yaml`.
*   Placeholders:
    *   `__MODEL_NAME_PLACEHOLDER__`: `text-generation-gpt`
    *   `__IMAGE_NAME_PLACEHOLDER__:__IMAGE_TAG_PLACEHOLDER__`: `creativeflow/custom-text-gen-gpt:0.1.0` (example)
    *   `__CONTAINER_PORT_PLACEHOLDER__`: `8000`
    *   `__GPU_COUNT_PLACEHOLDER__`: `1` (if model is GPU accelerated) or `0`
    *   Memory/CPU limits and requests set appropriately.
    *   `__READINESS_PROBE_PATH_PLACEHOLDER__`: `/health/ready`
    *   `__LIVENESS_PROBE_PATH_PLACEHOLDER__`: `/health/live`
    *   `__SECRET_NAME_PLACEHOLDER__`: `text-generation-model-secrets` (if it needs API keys etc.)

##### `models/example-text-generation-gpt/service.yaml` (Illustrative)
*   Instantiation of `runtimes/custom-python/service.template.yaml` with `text-generation-gpt` specific names.

##### `models/example-text-generation-gpt/hpa.yaml`
*   **Purpose**: To automatically scale the `custom-py-server-text-generation` Deployment.
*   **Specification**:
    yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: text-generation-gpt-hpa
      namespace: ai-serving
      labels:
        app: custom-py-server-text-generation
        creativeflow.ai/autoscaling-for: text-generation-gpt
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: custom-py-server-text-generation # Must match the Deployment name
      minReplicas: 1
      maxReplicas: 5 # Example max
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70 # Target 70% CPU utilization
      # Example for GPU based scaling (requires metrics-server supporting nvidia.com/gpu metrics)
      # - type: Resource
      #   resource:
      #     name: nvidia.com/gpu
      #     target:
      #       type: Utilization # Percentage of GPU utilization
      #       averageUtilization: 75
      behavior: # Optional: fine-tune scaling behavior
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
            value: 2 # Add max 2 pods at a time
            periodSeconds: 15
          selectPolicy: Max
    

##### `models/example-text-generation-gpt/secret.placeholder.yaml`
*   **Purpose**: Placeholder for secrets needed by the text generation model (e.g., API key for an external LLM if this is a wrapper). Actual values are sourced from HashiCorp Vault.
*   **Specification**:
    yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: text-generation-model-secrets # Referenced in Deployment envFrom
      namespace: ai-serving
      labels:
        app.kubernetes.io/part-of: text-generation-gpt
    type: Opaque
    # Data keys should align with what the application expects as environment variables.
    # Values are placeholders (base64 encoded "placeholder").
    # Actual values injected by CI/CD from HashiCorp Vault.
    # Example:
    # data:
    #   EXTERNAL_LLM_API_KEY: cGxhY2Vob2xkZXI=
    #   MODEL_CONFIG_PARAM: cGxhY2Vob2xkZXI=
    stringData: # Easier to read placeholders, will be base64 encoded by Kubernetes
      EXAMPLE_API_KEY_FOR_LLM: "placeholder-llm-api-key"
      # Add other secret keys as needed
    

### 3.7 Kustomize Overlays for Environment Configuration (`config/overlays/`)
Kustomize allows managing environment-specific configurations by applying patches to base manifests.

#### 3.7.1 Development Overlay (`config/overlays/development/`)
*   **`kustomization.yaml`**:
    yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    namespace: ai-serving # Ensures all resources are in this namespace

    # Bases can be specific models or common runtime templates
    # This example assumes you deploy specific model examples from the /models directory
    resources:
      - ../../../base # Common namespace, RBAC, resource quotas
      - ../../../models/example-image-classification-tf # The full definition for this model
      - ../../../models/example-text-generation-gpt/deployment.yaml # Assuming text-gen has its own deployment definition
      - ../../../models/example-text-generation-gpt/service.yaml
      # - ../../../models/example-text-generation-gpt/hpa.yaml # HPA might be disabled or have lower targets in dev

    patchesStrategicMerge:
      # Patches for TensorFlow model
      - |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: tf-serving-image-classifier
          namespace: ai-serving
        spec:
          replicas: 1
          template:
            spec:
              containers:
              - name: tf-serving-container
                resources:
                  limits:
                    nvidia.com/gpu: 1 # Or 0 if GPUs are scarce in dev
                    memory: "2Gi"
                    cpu: "1"
                  requests:
                    nvidia.com/gpu: 1 # Or 0
                    memory: "1Gi"
                    cpu: "500m"
      # Patches for Custom Python model
      - |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: custom-py-server-text-generation
          namespace: ai-serving
        spec:
          replicas: 1
          template:
            spec:
              containers:
              - name: custom-py-server-container
                resources:
                  limits:
                    memory: "1Gi"
                    cpu: "500m"
                  requests:
                    memory: "512Mi"
                    cpu: "250m"
    
    # Optional: if HPA for text-generation needs different values in dev
    # patchesJson6902:
    # - target:
    #     group: autoscaling
    #     version: v2
    #     kind: HorizontalPodAutoscaler
    #     name: text-generation-gpt-hpa
    #   patch: |-
    #     - op: replace
    #       path: /spec/minReplicas
    #       value: 1
    #     - op: replace
    #       path: /spec/maxReplicas
    #       value: 2

    commonLabels:
      environment: development
      deployed-by: kustomize-dev
    
*   **Patch files (e.g., `patch-replicas-dev.yaml`, `patch-resources-dev.yaml`)**: These would be referenced in `kustomization.yaml` if not using inline patches as shown above. The inline approach is often simpler for a few changes.

#### 3.7.2 Production Overlay (`config/overlays/production/`)
*   **`kustomization.yaml`**:
    yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    namespace: ai-serving

    resources:
      - ../../../base
      - ../../../models/example-image-classification-tf
      - ../../../models/example-text-generation-gpt/deployment.yaml
      - ../../../models/example-text-generation-gpt/service.yaml
      - ../../../models/example-text-generation-gpt/hpa.yaml # Enable HPA for production

    patchesStrategicMerge:
      # Patches for TensorFlow model
      - |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: tf-serving-image-classifier
          namespace: ai-serving
        spec:
          replicas: 3 # Higher replicas for prod
          template:
            spec:
              containers:
              - name: tf-serving-container
                resources:
                  limits:
                    nvidia.com/gpu: 1
                    memory: "8Gi" # Higher resources for prod
                    cpu: "4"
                  requests:
                    nvidia.com/gpu: 1
                    memory: "4Gi"
                    cpu: "2"
      # Patches for Custom Python model
      - |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: custom-py-server-text-generation
          namespace: ai-serving
        spec:
          replicas: 2 # Example: HPA will manage this up to maxReplicas
          template:
            spec:
              containers:
              - name: custom-py-server-container
                resources: # Ensure these align with HPA targets or are appropriate base values
                  limits:
                    nvidia.com/gpu: 1 # If text-gen model uses GPU
                    memory: "4Gi"
                    cpu: "2"
                  requests:
                    nvidia.com/gpu: 1
                    memory: "2Gi"
                    cpu: "1"
    
    # HPA for text-generation-gpt is already included in resources, ensure its values are production-ready.
    # If HPA itself needs patching for production (e.g. different maxReplicas):
    # patchesJson6902:
    # - target:
    #     group: autoscaling
    #     version: v2
    #     kind: HorizontalPodAutoscaler
    #     name: text-generation-gpt-hpa
    #   patch: |-
    #     - op: replace
    #       path: /spec/maxReplicas
    #       value: 10 # Higher max replicas for production

    commonLabels:
      environment: production
      deployed-by: kustomize-prod
    

## 4. Dockerfile Specifications
General Dockerfile best practices include:
*   Use official, versioned base images.
*   Minimize layers.
*   Use multi-stage builds where appropriate to reduce final image size.
*   Run containers as non-root users.
*   Clean up temporary files and build caches.
*   Clearly document `ARG`s and `ENV`s.

#### 4.1 TensorFlow Serving (`runtimes/tensorflow-serving/Dockerfile.template`)
*   **Purpose**: To package TensorFlow SavedModels for serving with TensorFlow Serving.
*   **Specification**:
    dockerfile
    # Use an official TensorFlow Serving image, preferably with GPU support for AI cluster
    # Example: tensorflow/serving:2.15.0-gpu or latest-gpu
    ARG TF_SERVING_VERSION=latest-gpu 
    FROM tensorflow/serving:${TF_SERVING_VERSION}

    # Environment variable for the model name (optional, can be passed at runtime or in models.config)
    ARG MODEL_NAME=generic_model
    ENV MODEL_NAME=${MODEL_NAME}

    # Path to the model directory containing version subdirectories (e.g., ./my_model_files/1)
    # This path is relative to the build context.
    ARG MODEL_FILES_PATH=./model_files 

    # Copy model files into the image at the location TF Serving expects
    # The directory structure inside /models/ should be /models/<MODEL_NAME>/<VERSION>/saved_model.pb and variables/
    COPY ${MODEL_FILES_PATH}/ /models/${MODEL_NAME}/

    # Optional: Copy a models.config file if serving multiple models or complex versioning
    # ARG MODELS_CONFIG_FILE=./models.config.template
    # COPY ${MODELS_CONFIG_FILE} /models/models.config
    # If using models.config, the CMD below might change to only use --model_config_file

    # Expose gRPC (8500) and REST (8501) ports
    EXPOSE 8500 8501

    # Default command to start TensorFlow Serving for a single model
    # If using models.config, the command would be:
    # CMD ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_config_file=/models/models.config", "--enable_batching"]
    # For single model without models.config:
    CMD ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_name=${MODEL_NAME}", "--model_base_path=/models/${MODEL_NAME}"]
    

#### 4.2 TorchServe (`runtimes/torchserve/Dockerfile.template`)
*   **Purpose**: To package PyTorch models (.mar files) for serving with TorchServe.
*   **Specification**:
    dockerfile
    # Use an official PyTorch TorchServe image, preferably with GPU support
    # Example: pytorch/torchserve:0.9.0-gpu or latest-gpu
    ARG TORCHSERVE_VERSION=latest-gpu
    FROM pytorch/torchserve:${TORCHSERVE_VERSION}

    # Working directory for model server files
    USER root # TorchServe base image might need root to copy to /home/model-server
    WORKDIR /home/model-server

    # Path to the model archive (.mar) file or a directory containing .mar files
    # This path is relative to the build context.
    ARG MAR_FILES_PATH=./model_store_content/

    # Copy model archive(s) into the model store directory TorchServe uses
    COPY ${MAR_FILES_PATH} ./model-store/

    # Optional: Copy a custom TorchServe config.properties file
    # ARG CONFIG_PROPERTIES_FILE=./config.properties.template
    # COPY ${CONFIG_PROPERTIES_FILE} ./config.properties

    # Optional: Install additional dependencies if your model handlers need them
    # COPY requirements_handler.txt .
    # RUN pip install --no-cache-dir -r requirements_handler.txt

    USER model-server # Switch back to non-root user if possible (base image dependent)

    # Expose inference (8080), management (8081), and metrics (8082) ports
    EXPOSE 8080 8081 8082

    # The base image's CMD usually starts TorchServe.
    # If specific models need to be loaded at startup or a config file used:
    # CMD ["torchserve", "--start", "--ts-config=/home/model-server/config.properties", "--model-store", "model-store", "--models", "all"]
    # Or specific model: "--models", "my_model_name=my_model.mar"
    # Default CMD from base image is often sufficient if MARs are in model-store.
    
    *Notes*: `config.properties` can define initial models to load, inference address, number of workers, etc.

#### 4.3 NVIDIA Triton Inference Server (`runtimes/triton-inference-server/Dockerfile.template`)
*   **Purpose**: To package a model repository for serving with Triton Inference Server.
*   **Specification**:
    dockerfile
    # Use an official NVIDIA Triton Inference Server image
    # Example: nvcr.io/nvidia/tritonserver:24.05-py3 (check latest recommended version)
    ARG TRITON_VERSION=24.05-py3
    FROM nvcr.io/nvidia/tritonserver:${TRITON_VERSION}

    # Path to the model repository directory on the host.
    # This directory should be structured according to Triton's requirements.
    # See runtimes/triton-inference-server/model-repository-structure.md
    ARG MODEL_REPOSITORY_PATH=./triton_model_repo/

    # Copy the entire model repository into the image
    COPY ${MODEL_REPOSITORY_PATH} /models/

    # Optional: Install custom backend or Python backend dependencies if needed
    # USER root
    # COPY custom_requirements.txt /tmp/custom_requirements.txt
    # RUN /opt/tritonserver/bin/pip install --no-cache-dir -r /tmp/custom_requirements.txt && rm /tmp/custom_requirements.txt
    # USER triton-server

    # Expose HTTP (8000), gRPC (8001), and metrics (8002) ports
    EXPOSE 8000 8001 8002

    # Default command from base image is usually:
    # CMD ["tritonserver", "--model-repository=/models"]
    # Add other flags as needed, e.g., --strict-model-config=true, --log-verbose=1
    

#### 4.4 Custom Python Server (`runtimes/custom-python/Dockerfile.template`)
*   **Purpose**: To package custom Python AI model servers (e.g., using FastAPI, Flask).
*   **Specification**:
    dockerfile
    # Use a slim Python base image
    ARG PYTHON_VERSION=3.12-slim
    FROM python:${PYTHON_VERSION}

    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    ENV APP_HOME /app

    WORKDIR ${APP_HOME}

    # Install system dependencies if any (e.g., for OpenCV or other libraries)
    # RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

    # Copy application source code and model artifacts
    # Structure assumes:
    # ./src/ (Python code)
    # ./model_artifacts/ (model files)
    # ./requirements.txt
    COPY ./requirements.txt .
    COPY ./src ./src
    COPY ./model_artifacts ./model_artifacts # Only if model artifacts are co-packaged

    # Install Python dependencies
    # Using --no-cache-dir to reduce image size
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose the port the application runs on
    ARG APP_PORT=8000
    EXPOSE ${APP_PORT}

    # User to run the application (security best practice)
    # RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser
    # USER appuser

    # Command to run the application (e.g., using Uvicorn for FastAPI)
    # Assumes main.py with an 'app' instance is in src/
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "${APP_PORT}"]
    # For Flask with Gunicorn:
    # CMD ["gunicorn", "--bind", "0.0.0.0:${APP_PORT}", "src.main:app"]
    

## 5. Python Wrapper for Custom Models (Illustrative)
Located in `runtimes/custom-python/src/`.

#### 5.1 FastAPI Application Structure (`runtimes/custom-python/src/main.py.template`)
*   **Purpose**: Provides a basic FastAPI application for serving a custom model.
*   **Key Components**:
    *   `app = FastAPI()`: Initializes FastAPI app.
    *   `startup_event()`: Function to load the model when the application starts. The model should be loaded once and stored globally or in app state.
    *   `/predict` (POST): Endpoint to receive input data, preprocess, run inference, postprocess, and return predictions. Input/output schemas should be defined using Pydantic models for validation and documentation.
    *   `/health/live` (GET): Liveness probe endpoint, returns 200 OK if the server is running.
    *   `/health/ready` (GET): Readiness probe endpoint, returns 200 OK if the server is running AND the model is loaded and ready to serve requests.
*   **Logic Example**:
    python
    # In src/main.py.template
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    # from . import model_loader # Assuming model_loader.py is in the same directory (src)
    
    # Define request/response Pydantic models for type checking and API docs
    class PredictionRequest(BaseModel):
        # Define expected input fields, e.g.
        # feature1: float
        # text_input: str
        raw_data: dict # Generic example

    class PredictionResponse(BaseModel):
        # Define expected output fields, e.g.
        # prediction_label: str
        # confidence: float
        result: dict # Generic example

    app = FastAPI(
        title="Custom AI Model Server",
        description="Serves predictions for a custom AI model.",
        version="0.1.0"
    )
    
    # Placeholder for the loaded model
    # This should be typed correctly based on your model library
    loaded_model: object = None 

    @app.on_event("startup")
    async def load_model_on_startup():
        global loaded_model
        try:
            # Assuming model_loader.py has a function `get_model_instance`
            # loaded_model = model_loader.get_model_instance(model_path="/app/model_artifacts/your_model_file.ext")
            # For template, we'll just simulate
            loaded_model = object() # Replace with actual model loading
            if loaded_model:
                 print("INFO: Model loaded successfully during startup.")
            else:
                 print("ERROR: Model loading failed during startup.")
        except Exception as e:
            print(f"ERROR: Exception during model loading: {e}")
            # Optionally, prevent app from starting or set a not-ready state

    @app.post("/predict", response_model=PredictionResponse)
    async def predict(request: PredictionRequest):
        if not loaded_model:
            raise HTTPException(status_code=503, detail="Model not ready or loading failed.")
        try:
            # 1. Preprocess request.raw_data (or specific fields from PredictionRequest)
            #    This depends heavily on your model's expected input format.
            #    Example: processed_input = preprocess_input(request.raw_data)
            
            # 2. Perform inference
            #    Example: model_output = loaded_model.predict(processed_input)
            
            # 3. Postprocess model_output to match PredictionResponse schema
            #    Example: response_data = postprocess_output(model_output)

            # Placeholder logic:
            print(f"Received prediction request: {request.dict()}")
            response_data = {"message": "Prediction processed (placeholder)", "input_received": request.raw_data}
            
            return PredictionResponse(result=response_data)
        except Exception as e:
            print(f"ERROR: Exception during prediction: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing prediction: {str(e)}")

    @app.get("/health/live", status_code=200)
    async def health_live():
        return {"status": "live"}

    @app.get("/health/ready", status_code=200)
    async def health_ready():
        if not loaded_model:
             # If model loading is critical for readiness
            raise HTTPException(status_code=503, detail="Model not ready")
        return {"status": "ready"}

    # If running directly with uvicorn from command line:
    # import uvicorn
    # if __name__ == "__main__":
    #     uvicorn.run(app, host="0.0.0.0", port=8000)
    

#### 5.2 Model Loading Logic (`runtimes/custom-python/src/model_loader.py.template`)
*   **Purpose**: To encapsulate the logic for loading the specific AI model from disk or a remote location.
*   **Key Function**: `get_model_instance(model_path: str) -> object`
*   **Logic Example**:
    python
    # In src/model_loader.py.template
    import os
    # Import necessary libraries for your model type, e.g.:
    # import joblib
    # import tensorflow as tf
    # import torch

    # Placeholder for the actual model loading logic
    def get_model_instance(model_path: str) -> object:
        """
        Loads and returns the AI model instance.
        The actual implementation depends on the model framework and format.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

        # Example for a scikit-learn model saved with joblib:
        # try:
        #     model = joblib.load(model_path)
        #     print(f"INFO: Scikit-learn model loaded from {model_path}")
        #     return model
        # except Exception as e:
        #     print(f"ERROR: Failed to load scikit-learn model from {model_path}: {e}")
        #     raise

        # Example for a TensorFlow SavedModel:
        # try:
        #     model = tf.saved_model.load(model_path)
        #     print(f"INFO: TensorFlow SavedModel loaded from {model_path}")
        #     return model.signatures["serving_default"] # Or specific signature
        # except Exception as e:
        #     print(f"ERROR: Failed to load TensorFlow SavedModel from {model_path}: {e}")
        #     raise

        # Example for a PyTorch model (state_dict):
        # try:
        #     # Assuming YourModelClass is defined and imported
        #     # model = YourModelClass(*args, **kwargs) 
        #     # model.load_state_dict(torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
        #     # model.eval() # Set to evaluation mode
        #     # print(f"INFO: PyTorch model loaded from {model_path}")
        #     # return model
        #     pass # Placeholder
        # except Exception as e:
        #     print(f"ERROR: Failed to load PyTorch model from {model_path}: {e}")
        #     raise
        
        # Placeholder:
        print(f"INFO: Attempting to load model from {model_path} (actual loading logic needed).")
        # Simulate a loaded model object
        class PlaceholderModel:
            def predict(self, data):
                return {"prediction_placeholder": "This is a simulated prediction"}
        return PlaceholderModel()
    

#### 5.3 Dependencies (`runtimes/custom-python/src/requirements.txt.template`)
*   **Purpose**: To list all Python dependencies required by the custom model server.
*   **Specification**:
    txt
    # FastAPI and Uvicorn for the web server
    fastapi>=0.100.0,<0.110.0
    uvicorn[standard]>=0.23.0,<0.24.0
    pydantic>=2.0.0,<3.0.0

    # Add ML framework libraries, e.g.:
    # tensorflow>=2.10.0,<2.16.0
    # torch>=2.0.0,<2.2.0
    # scikit-learn>=1.2.0,<1.4.0
    # joblib>=1.2.0,<1.4.0

    # Add other necessary libraries:
    # pandas
    # numpy
    # pillow # For image processing
    

## 6. Configuration File Specifications

#### 6.1 Triton Model Repository Structure (`runtimes/triton-inference-server/model-repository-structure.md`)
*   **Purpose**: To document the directory structure Triton Inference Server expects for its model repository.
*   **Specification**:
    markdown
    # Triton Model Repository Structure

    This document outlines the required directory structure for models to be served by the NVIDIA Triton Inference Server. The server will automatically discover and load models that adhere to this structure.

    ## Root Directory
    The model repository is a top-level directory (e.g., `/models` inside the Docker container, or a path specified by `--model-repository` flag).

    ## Model Directory
    Each model must reside in its own subdirectory within the root model repository. The name of this subdirectory is used as the `<model-name>` by Triton.

    
    /models
    └── <model_name_1>/
    └── <model_name_2>/
        ...
    

    ## Version Directory
    Within each `<model_name>` directory, there must be one or more numerically named subdirectories representing different versions of the model. Triton will serve one or more of these versions based on the model's `config.pbtxt` version policy.

    
    /models
    └── <model_name_1>/
        ├── config.pbtxt
        ├── 1/ 
        │   └── <model_artifact_file(s)>
        └── 2/
            └── <model_artifact_file(s)>
    
    *   `<version_number>` must be an integer (e.g., 1, 2, 10).

    ## Model Artifacts
    The `<model_artifact_file(s)>` are the actual model files specific to the model's framework/backend.
    *   **TensorFlow SavedModel**: `model.savedmodel/` directory containing `saved_model.pb` and `variables/`.
    *   **TensorFlow GraphDef**: `model.graphdef`
    *   **ONNX**: `model.onnx`
    *   **PyTorch TorchScript**: `model.pt`
    *   **TensorRT PLAN**: `model.plan`
    *   **Python Backend**: `model.py` (and any other required Python files)
    *   ... and other supported backends.

    ## Model Configuration File (`config.pbtxt`)
    Each `<model_name>` directory **must** contain a `config.pbtxt` file. This file describes the model's metadata, including:
    *   `name`: The name of the model (must match the directory name).
    *   `platform` or `backend`: The framework/backend for the model (e.g., "tensorflow_savedmodel", "onnxruntime_onnx", "pytorch_libtorch", "python").
    *   `max_batch_size`: Maximum batch size supported by the model.
    *   `input` tensor definitions (name, data_type, dims).
    *   `output` tensor definitions (name, data_type, dims).
    *   `instance_group`: Configuration for how many instances of the model to load on each GPU or CPU.
    *   `version_policy`: Specifies which versions to serve (e.g., `latest { num_versions: 1 }`, `all: {}`, `specific: { versions: [1,3] }`).
    *   Other backend-specific or optimization settings.

    **Example `config.pbtxt` (simplified):**
    protobuf
    name: "my_onnx_model"
    platform: "onnxruntime_onnx"
    max_batch_size: 8
    input [
      {
        name: "input_tensor"
        data_type: TYPE_FP32
        dims: [ -1, 3, 224, 224 ] # Dynamic batch size, C, H, W
      }
    ]
    output [
      {
        name: "output_tensor"
        data_type: TYPE_FP32
        dims: [ -1, 1000 ] # Dynamic batch size, num_classes
      }
    ]
    instance_group [
      {
        count: 1
        kind: KIND_GPU
      }
    ]
    

    For detailed information, refer to the [official NVIDIA Triton Inference Server documentation](https://developer.nvidia.com/triton-inference-server).
    

## 7. Integration and Operational Aspects

### 7.1 Integration with Secrets Management (HashiCorp Vault)
*   Kubernetes Secrets defined in this repository (e.g., `secret.placeholder.yaml`) will be placeholders.
*   The CI/CD pipeline (from `REPO-CICD-PIPELINE-001`) or a Kubernetes secrets operator (e.g., HashiCorp Vault Agent Injector, External Secrets Operator) will be responsible for fetching actual secret values from HashiCorp Vault (`REPO-SECRETS-MANAGEMENT-001`) and injecting them into the cluster as Kubernetes Secrets or directly into pod environments.
*   This ensures sensitive data is not stored in Git.
*   RBAC for model serving pods (`model-reader-role`) grants permissions to read these injected Secrets if they are mounted as volumes or environment variables.

### 7.2 Integration with MLOps Service (AISIML-Service)
*   The MLOps Service (`REPO-AISIML-SERVICE-001`) will utilize the Kustomize overlays and manifest templates from this repository to deploy custom AI models.
*   The MLOps Service will:
    1.  Identify the correct runtime template (TensorFlow Serving, TorchServe, Triton, Custom Python).
    2.  Build a Docker image using the appropriate Dockerfile template and the user-uploaded/validated model artifacts. The image will be tagged and pushed to the private container registry (`REPO-CONTAINER-REGISTRY-001`).
    3.  Populate placeholders in the Kubernetes manifest templates (Deployment, Service, etc.) with model-specific details (image name:tag, model name, resource requests, GPU count, replica count, etc.).
    4.  Apply the Kustomize overlay for the target environment (dev, staging, prod).
    5.  Use `kubectl apply -k` or an equivalent GitOps mechanism to deploy the model to the `ai-serving` namespace in the Kubernetes cluster.
    6.  Manage the lifecycle (deployment, update, rollback, scaling via HPA changes) of these model deployments.

### 7.3 CI/CD Pipeline Integration
*   Changes to this repository (manifests, Dockerfiles, Kustomize overlays) will trigger CI pipeline jobs in `REPO-CICD-PIPELINE-001`.
*   CI jobs will include:
    *   Linting YAML files (e.g., using `kubeval`, `yamllint`).
    *   Linting Dockerfiles (e.g., using `hadolint`).
    *   Validating Kustomize configurations (`kustomize build` for each overlay).
    *   Optionally, dry-run deployments to a test Kubernetes cluster.
*   The CD part of the pipeline, managed by the MLOps service or a GitOps controller, will use these version-controlled artifacts for actual deployments.

### 7.4 GPU Resource Specification
*   All Deployment manifests for GPU-accelerated models **must** include resource requests and limits for `nvidia.com/gpu`.
    yaml
    resources:
      limits:
        nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__ 
      requests:
        nvidia.com/gpu: __GPU_COUNT_PLACEHOLDER__
    
*   The `__GPU_COUNT_PLACEHOLDER__` will be determined by the model's requirements and available cluster capacity.
*   The NVIDIA GPU Operator must be installed and functioning on the Kubernetes cluster for these resource requests to be satisfied.
*   Consideration for MIG (Multi-Instance GPU) can be configured at the GPU Operator level and reflected in model scheduling if specific model instances require only fractions of a GPU. This would involve more complex `instance_group` configurations in Triton or similar mechanisms for other servers.

### 7.5 Health Probes (Liveness & Readiness)
*   All Deployment manifests **must** define appropriate liveness and readiness probes for the model serving containers.
*   **Readiness Probes**: Indicate when a pod is ready to start accepting traffic. For model servers, this usually means the model(s) are loaded and the inference endpoint is responsive.
*   **Liveness Probes**: Indicate whether a pod is still running correctly. If a liveness probe fails, Kubernetes will restart the container.
*   Probe types (HTTP, TCP, gRPC, Exec) and paths/ports will vary based on the serving runtime:
    *   **TensorFlow Serving**: HTTP GET to `/v1/models/<model_name>` (REST API port, e.g., 8501).
    *   **TorchServe**: HTTP GET to `/ping` (management port, e.g., 8081).
    *   **Triton Inference Server**: HTTP GET to `/v2/health/ready` and `/v2/health/live` (HTTP port, e.g., 8000).
    *   **Custom Python Servers**: Should implement dedicated `/health/ready` and `/health/live` endpoints.
*   `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, and `failureThreshold` for probes must be tuned based on model loading times and server responsiveness.

## 8. Documentation Generation
This repository, by its nature (containing declarative manifests and Dockerfiles), serves as a form of "infrastructure and deployment as documentation." However, to enhance usability:
*   **README.md (Root)**: A top-level README will explain the repository structure, purpose, and how to use Kustomize overlays for environment-specific deployments. It will link to runtime-specific READMEs.
*   **README.md (Runtime-specific)**: Each `runtimes/<runtime_name>/` directory will contain a README explaining:
    *   How to use the Dockerfile template.
    *   How to use the Kubernetes manifest templates.
    *   Required placeholders and their significance.
    *   Example configurations or commands for building and deploying.
*   **`model-repository-structure.md` (for Triton)**: Already defined in the file structure, provides specific guidance for Triton.
*   **Comments in Manifests/Dockerfiles**: All YAML and Dockerfile artifacts will be well-commented to explain non-obvious configurations and choices.
*   **Automatic Documentation**: If feasible, tools like `helm-docs` (if Helm charts were used, not the case here but similar concept for Kustomize) or custom scripts could be used to generate summaries or tables of configurable parameters from Kustomize bases/patches, although this is less common for pure Kustomize. Primary documentation will be through well-structured READMEs and inline comments.
*   The `generateDocumentation: true` flag for this repository implies that these structured YAML files, Dockerfiles, and markdown files are the primary documentation artifacts for AI model deployment configurations. The CI/CD pipeline could potentially run linters or validators that also check for basic documentation presence (e.g., required comments or README sections).