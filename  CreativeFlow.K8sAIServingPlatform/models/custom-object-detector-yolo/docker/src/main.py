from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
from typing import List, Optional
from pydantic import BaseModel
from .model_handler import YOLOModelHandler, get_yolo_handler
from prometheus_client import Counter, Histogram, make_asgi_app

# --- Prometheus Metrics Definition ---
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

# --- FastAPI App Initialization ---
app = FastAPI(
    title="CreativeFlow Custom YOLO Object Detector",
    description="Serves a custom YOLO model for object detection via FastAPI.",
    version="1.0.0"
)

# Mount Prometheus ASGI app on /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --- Application Events ---
@app.on_event("startup")
async def startup_event():
    """Initializes the YOLOModelHandler singleton instance on application startup."""
    model_path = os.getenv("MODEL_PATH", "/app/model_weights/yolov5s.pt")
    confidence_str = os.getenv("CONFIDENCE_THRESHOLD", "0.25")
    
    try:
        confidence_threshold = float(confidence_str)
    except (ValueError, TypeError):
        print(f"Warning: Invalid CONFIDENCE_THRESHOLD '{confidence_str}', using default 0.25.")
        confidence_threshold = 0.25
    
    try:
        # This call creates and initializes the singleton instance
        YOLOModelHandler(model_path=model_path, confidence_threshold=confidence_threshold)
        print(f"YOLO Model Handler initialized successfully with model: {model_path}")
    except Exception as e:
        # Log the critical error. The /health endpoint will report unhealthy.
        print(f"CRITICAL: Error initializing YOLO Model Handler during startup: {e}")

# --- Pydantic Models for API Contract ---
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
    model_name: str = "yolo-custom"
    model_version: Optional[str] = os.getenv("MODEL_VERSION_TAG", "dev")

# --- API Endpoints ---
@app.post("/v1/predict", 
          response_model=PredictionResponse, 
          summary="Detect Objects in Image using YOLO", 
          tags=["Object Detection"])
async def predict_yolo_objects(
    file: UploadFile = File(..., description="Image file to perform object detection on."),
    yolo_handler: YOLOModelHandler = Depends(get_yolo_handler) # Dependency injection
):
    """
    Accepts an image file, performs object detection using the loaded YOLO model,
    and returns a list of detected objects with their bounding boxes and class names.
    """
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
                detections=detections_data, 
                image_filename=file.filename
            )
        except ValueError as ve: # Specific error for bad image data from handler
            YOLO_REQUEST_COUNT.labels(http_status=400).inc()
            raise HTTPException(status_code=400, detail=str(ve))
        except RuntimeError as re: # E.g., model not loaded
             YOLO_REQUEST_COUNT.labels(http_status=503).inc()
             raise HTTPException(status_code=503, detail=str(re))
        except Exception as e:
            print(f"Error during YOLO prediction: {type(e).__name__} - {e}")
            YOLO_REQUEST_COUNT.labels(http_status=500).inc()
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred during prediction.")

@app.get("/health", summary="Health Check", tags=["System"])
async def health_check():
    """
    Performs a health check. Returns healthy only if the model handler was initialized.
    """
    try:
        # get_yolo_handler will raise RuntimeError if the instance is not initialized
        get_yolo_handler()
        return JSONResponse(content={"status": "healthy"})
    except RuntimeError as e:
        return JSONResponse(content={"status": "unhealthy", "detail": str(e)}, status_code=503)