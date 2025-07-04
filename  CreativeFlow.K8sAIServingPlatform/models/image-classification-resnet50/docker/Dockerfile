# Use the CreativeFlow AI base image for TensorFlow Serving
ARG CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG=latest 
FROM creativeflow/tensorflow-serving-base:${CREATIVEFLOW_TFSERVING_BASE_IMAGE_TAG}

LABEL model.name="resnet50"
LABEL model.framework="tensorflow"
LABEL model.task="image-classification"

# Path where models will be stored inside the container
ENV MODEL_BASE_PATH=/models
ENV MODEL_NAME=resnet50

# Create the specific model directory inside the base model path
RUN mkdir -p ${MODEL_BASE_PATH}/${MODEL_NAME}

# Copy the ResNet50 SavedModel bundle into the image.
# This command assumes the source directory `../model_artifacts/resnet50` contains
# versioned subdirectories (e.g., `1/`, `2/`) with the `saved_model.pb` file inside.
COPY ../model_artifacts/resnet50 ${MODEL_BASE_PATH}/${MODEL_NAME}

# Expose TensorFlow Serving ports (already exposed in base, but good for clarity)
EXPOSE 8500 # gRPC
EXPOSE 8501 # REST

# The CMD tells TensorFlow Serving to look in MODEL_BASE_PATH for a model named MODEL_NAME.
# Since our COPY command creates the structure `/models/resnet50/[version]`,
# this command is correct. TF Serving will automatically discover the model named `resnet50`
# inside the `/models` directory.
CMD ["tensorflow_model_server", \
    "--port=8500", \
    "--rest_api_port=8501", \
    "--model_name=${MODEL_NAME}", \
    "--model_base_path=${MODEL_BASE_PATH}" \
]