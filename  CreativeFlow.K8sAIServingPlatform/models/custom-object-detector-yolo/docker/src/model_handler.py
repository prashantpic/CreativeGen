import torch
import os
from PIL import Image
import io
import numpy as np
# from ultralytics import YOLO # Uncomment if using the Ultralytics YOLO class directly

class YOLOModelHandler:
    """
    A singleton class to handle YOLO model loading and inference.
    This ensures the model is loaded into memory only once.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(YOLOModelHandler, cls).__new__(cls)
            # Initialize the instance only once
            model_path = kwargs.get("model_path")
            confidence_threshold = kwargs.get("confidence_threshold", 0.25)
            
            cls._instance.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"YOLO Handler: Initializing model on device: {cls._instance.device}")

            if not model_path or not os.path.exists(model_path):
                raise FileNotFoundError(f"Model weights not found at {model_path}")
            
            try:
                # Load YOLOv5 model from torch.hub. This can also work for other YOLO versions.
                # `force_reload=False` will use cached models if available.
                # `_verbose=False` reduces console output from torch.hub.
                cls._instance.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False, _verbose=False)
                cls._instance.model.to(cls._instance.device)
                cls._instance.model.eval() # Set model to evaluation mode
                cls._instance.confidence_threshold = float(confidence_threshold)
                cls._instance.model_names = cls._instance.model.names # Class names
                print(f"YOLO model loaded successfully from {model_path} with confidence {cls._instance.confidence_threshold}")
            except Exception as e:
                print(f"CRITICAL: Error loading YOLO model: {e}")
                raise RuntimeError(f"Failed to load YOLO model: {e}") from e
        return cls._instance

    def _preprocess_image(self, image_bytes: bytes) -> Image.Image:
        """Converts image bytes to a PIL Image."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            return image
        except Exception as e:
            raise ValueError(f"Invalid image data: {e}") from e

    def _postprocess_detections(self, results) -> list:
        """Formats YOLOv5 detection results into a list of dictionaries."""
        detections = []
        # `results.xyxy[0]` contains detections for the first image in the batch
        # Format: [xmin, ymin, xmax, ymax, confidence, class_id]
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
        """Performs a full prediction cycle: preprocess, infer, postprocess."""
        if not hasattr(self, 'model') or self.model is None:
             raise RuntimeError("YOLO model is not loaded.")
             
        pil_image = self._preprocess_image(image_bytes)
        
        with torch.no_grad():
            # Perform inference
            results = self.model(pil_image, size=image_size) 
        
        processed_results = self._postprocess_detections(results)
        return processed_results

def get_yolo_handler() -> YOLOModelHandler:
    """FastAPI dependency to get the initialized YOLO handler instance."""
    if YOLOModelHandler._instance is None:
        # This case should ideally not be hit if the startup event initializes it correctly.
        # It's a safeguard.
        raise RuntimeError("YOLOModelHandler not initialized. Check FastAPI startup events.")
    return YOLOModelHandler._instance