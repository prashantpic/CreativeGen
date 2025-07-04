from pydantic import BaseModel
from typing import List, Any, Optional

class BaseInferenceRequest(BaseModel):
    """
    A generic base for inference request bodies.
    Specific models should inherit from this and add their own input fields.
    For example:
    class MyModelRequest(BaseInferenceRequest):
        text_prompt: str
        num_samples: int = 1
    """
    # Define common fields if any, or leave empty for specialization.
    # A request_id can be useful for tracing.
    request_id: Optional[str] = None


class BaseInferenceResponse(BaseModel):
    """
    A generic base for inference response bodies.
    Specific models should inherit from this or use it directly.
    """
    predictions: List[Any]
    request_id: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None