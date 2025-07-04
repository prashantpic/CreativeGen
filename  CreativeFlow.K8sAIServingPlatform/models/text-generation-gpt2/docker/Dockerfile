# Use the CreativeFlow AI base image for Triton
ARG CREATIVEFLOW_TRITON_BASE_IMAGE_TAG=latest
FROM creativeflow/triton-inference-server-base:${CREATIVEFLOW_TRITON_BASE_IMAGE_TAG}

LABEL model.name="gpt2"
LABEL model.framework="pytorch_libtorch" # Or onnxruntime_onnx, depending on the artifact
LABEL model.task="text-generation"

# Copy the structured model repository for GPT-2 into the default
# model repository path defined in the base image (`/models`).
# This assumes the source `../model_repository/gpt2` directory contains:
# - config.pbtxt
# - 1/model.pt (or model.onnx, or model.py for python backend)
COPY ../model_repository/gpt2 ${MODEL_REPOSITORY_PATH}/gpt2

# The CMD is inherited from the base image: `tritonserver --model-repository=/models`.
# No specific CMD override is needed as long as the model is copied into the
# expected repository structure.