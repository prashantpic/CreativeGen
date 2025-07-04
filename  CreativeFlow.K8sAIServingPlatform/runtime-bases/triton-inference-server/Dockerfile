# Use an official NVIDIA Triton Inference Server image
# The specific version is chosen to align with the platform's technology stack.
ARG TRITON_SERVER_VERSION=24.05-py3
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
EXPOSE 8002 # Metrics (HTTP)

# Default command to start Triton server.
# The --model-repository can be overridden by K8s deployment arguments.
# Specific model images will COPY their models into ${MODEL_REPOSITORY_PATH}.
CMD ["tritonserver", "--model-repository=${MODEL_REPOSITORY_PATH}"]