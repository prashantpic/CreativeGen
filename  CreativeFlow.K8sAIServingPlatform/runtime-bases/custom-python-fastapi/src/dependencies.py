from typing import Any, Callable
import os
# import joblib # Example for scikit-learn models
# import onnxruntime # Example for ONNX models

# This file is intended to hold common dependency injection logic.
# The following commented-out code provides a pattern for how a model might
# be loaded globally at startup and injected into endpoint functions.
# This avoids reloading a large model on every single API request.

# # This is a placeholder/example. Actual model loading will be specific to the model type.
# # Model-specific Docker images would implement their own loaders.
# _global_model: Any = None

# def load_model_globally(model_path: str) -> Any:
#     """
#     Loads a model from the given path into a global variable.
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

# async def get_model() -> Any:
#     """
#     FastAPI dependency to get the loaded model.
#     This function would be used in endpoint signatures like:
#     `model: Any = Depends(get_model)`
#     """
#     if _global_model is None:
#         # This could be a fallback if startup loading fails, or you could raise an error.
#         # raise HTTPException(status_code=503, detail="Model not loaded")
#         return None
#     return _global_model

def get_example_dependency():
    """
    A simple example of a dependency that can be injected into an endpoint.
    """
    return {"message": "This is an example dependency from base."}