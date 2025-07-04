"""
Pydantic schemas for proxying creative generation requests and responses,
mirroring the structure expected by the downstream AI Generation Orchestration service.
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class GenerationCreateRequestSchema(BaseModel):
    """Schema for initiating a new creative generation task via the proxy."""
    prompt: str = Field(..., description="The main text prompt for the generation.")
    output_format: str = Field("png", description="The desired output format, e.g., 'png', 'jpeg', 'mp4'.")
    num_samples: int = Field(4, ge=1, le=8, description="The number of initial samples to generate.")
    project_id: Optional[UUID] = Field(None, description="The ID of the project to associate this generation with.")
    style_preferences: Optional[Dict[str, Any]] = Field(None, description="A dictionary of style preferences or a brand kit reference.")
    custom_dimensions: Optional[Tuple[int, int]] = Field(None, description="Custom output dimensions as a (width, height) tuple.")


class GenerationStatusResponseSchema(BaseModel):
    """Schema for the status of a creative generation task."""
    generation_id: UUID = Field(..., description="The unique identifier for the generation task.")
    status: str = Field(..., description="The current status of the task (e.g., 'ProcessingSamples', 'Completed', 'Failed').")
    progress: Optional[int] = Field(None, ge=0, le=100, description="The progress of the task, from 0 to 100.")
    sample_urls: Optional[List[HttpUrl]] = Field(None, description="URLs to the generated sample assets, available when status is 'AwaitingSelection'.")
    result_url: Optional[HttpUrl] = Field(None, description="URL to the final generated asset, available when status is 'Completed'.")
    error_message: Optional[str] = Field(None, description="A description of the error if the task failed.")
    credits_cost_sample: Optional[Decimal] = Field(None, description="The number of credits consumed for the sample generation phase.")
    credits_cost_final: Optional[Decimal] = Field(None, description="The number of credits consumed for the final generation phase.")
    created_at: datetime = Field(..., description="The timestamp when the generation task was created.")
    updated_at: datetime = Field(..., description="The timestamp when the task status was last updated.")

    class Config:
        from_attributes = True