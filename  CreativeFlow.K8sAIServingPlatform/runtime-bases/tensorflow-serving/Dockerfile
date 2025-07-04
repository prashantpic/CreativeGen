# Use an official TensorFlow Serving image with GPU support
# The specific version is chosen to align with the platform's technology stack.
ARG TENSORFLOW_SERVING_VERSION=2.15.0-gpu
FROM tensorflow/serving:${TENSORFLOW_SERVING_VERSION}

LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
LABEL description="Base image for TensorFlow Serving with GPU support on CreativeFlow AI."

# (Optional) Add common utilities or scripts if needed by all TF Serving deployments
# e.g., COPY common_utils.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/common_utils.sh

# Expose default TensorFlow Serving ports
EXPOSE 8500 # gRPC port
EXPOSE 8501 # REST API port

# Default command can be overridden by specific model Dockerfiles or K8s deployment.
# This base image does not specify a default model to load.
# Models will be loaded via configuration passed at runtime (e.g., --model_config_file)
# or by specific model images that bake in the model and override this CMD.
CMD ["tensorflow_model_server"]