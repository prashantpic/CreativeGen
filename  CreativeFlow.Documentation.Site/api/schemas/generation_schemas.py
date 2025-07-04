```python
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, HttpUrl


class GenerationCreateRequestSchema(BaseModel):
    """
    Schema for initiating a creative generation, mirroring the expected payload
    of the downstream AI Generation Orchestration service.
    """
    prompt: str = Field(..., description="The main text prompt for the generation.")
    output_format: str = Field("png", description="The desired output format (e.g., 'png', 'jpeg').")
    num_samples: int = Field(4, gt=0, le=8, description="The number of initial samples to generate.")
    project_id: Optional[uuid.UUID] = Field(None, description="Optional ID of the project to associate this generation with.")
    style_preferences: Optional[Dict[str, Any]] = Field(None, description="A dictionary of style preferences.")
    custom_dimensions: Optional[Tuple[int, int]] = Field(None, description="Custom width and height for the output.")


class GenerationStatusResponseSchema(BaseModel):
    """
    Schema representing the status and results of a generation task.
    """
    generation_id: uuid.UUID = Field(..., description="The unique ID for the generation task.")
    status: str = Field(..., description="The current status of the task (e.g., 'ProcessingSamples', 'Completed', 'Failed').")
    progress: Optional[int] = Field(None, ge=0, le=100, description="The generation progress percentage.")
    sample_urls: Optional[List[HttpUrl]] = Field(None, description="URLs to the generated sample assets.")
    result_url: Optional[HttpUrl] = Field(None, description="URL to the final, high-resolution asset.")
    error_message: Optional[str] = Field(None, description="An error message if the task failed.")
    credits_cost_sample: Optional[Decimal] = Field(None, description="The credit cost for the sample generation phase.")
    credits_cost_final: Optional[Decimal] = Field(None, description="The credit cost for the final generation phase.")
    created_at: datetime = Field(..., description="Timestamp when the generation task was created.")
    updated_at: datetime = Field(..., description="Timestamp when the generation task was last updated.")

    class Config:
        from_attributes = True
```