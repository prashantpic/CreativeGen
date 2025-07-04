# Use the CreativeFlow AI base image for custom Python FastAPI servers
ARG CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG=latest
FROM creativeflow/custom-python-fastapi-base:${CREATIVEFLOW_CUSTOM_PYTHON_BASE_IMAGE_TAG}

LABEL model.name="yolo-custom"
LABEL model.framework="pytorch" # Assuming YOLOv5/v8 PyTorch based
LABEL model.task="object-detection"

# Copy model-specific source code, which will override or extend the base `src`.
COPY ./models/custom-object-detector-yolo/docker/src /app/src
    
# Copy model weights into the image.
# This assumes the model weights file (e.g., yolov5s.pt) is in this directory.
COPY ./models/custom-object-detector-yolo/model_weights /app/model_weights

# Install model-specific Python requirements. These are installed on top of the base requirements.
COPY ./models/custom-object-detector-yolo/docker/requirements.txt /app/requirements_model.txt
RUN pip install --no-cache-dir -r requirements_model.txt

# Set environment variables for the application. These can be overridden in the K8s Deployment.
ENV MODEL_PATH=/app/model_weights/yolov5s.pt # Default path to the model weights
ENV CONFIDENCE_THRESHOLD=0.25 # Default confidence threshold for detections

# The base image CMD ["uvicorn", "src.main:app", ...] is sufficient if the specialized
# `src/main.py` is structured correctly. No override is needed here.