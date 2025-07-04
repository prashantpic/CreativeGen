"""
dtos.py

Internal Data Transfer Objects (DTOs) used within the application layer.

These models facilitate data transfer between different parts of the application,
such as from the API layer to the service layer, or from the service layer to
infrastructure components like messaging. They help decouple the core application
logic from the specific contracts of the external-facing API.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

# --- DTOs for n8n Job Publishing ---

class GenerationJobParameters(BaseModel):
    """
    Internal DTO representing the payload for a generation job sent to n8n.
    This structure is serialized to JSON and published to RabbitMQ.
    """
    generation_request_id: UUID
    user_id: str
    project_id: str
    job_type: str = Field(..., description="Type of job, e.g., 'sample_generation', 'final_generation', 'sample_regeneration'")

    # Core generation parameters
    input_prompt: str
    style_guidance: Optional[str] = None
    output_format: str
    custom_dimensions: Optional[Dict[str, int]] = None
    brand_kit_id: Optional[str] = None
    uploaded_image_references: Optional[List[str]] = None
    target_platform_hints: Optional[List[str]] = None
    emotional_tone: Optional[str] = None
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = None

    # Parameters for final/regeneration jobs
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None
    
    # Callback URLs for n8n
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str


# --- DTOs for processing n8n Callbacks ---

class N8NSampleResultDTO(BaseModel):
    """Internal DTO for processing sample results from n8n."""
    generation_request_id: UUID
    samples: List[Dict[str, Any]]

class N8NFinalResultDTO(BaseModel):
    """Internal DTO for processing the final result from n8n."""
    generation_request_id: UUID
    final_asset: Dict[str, Any]

class N8NErrorDTO(BaseModel):
    """Internal DTO for processing an error from n8n."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = None


# --- DTOs for Credit Service Interactions ---

class DeductCreditsDTO(BaseModel):
    """DTO for a request to the Credit Service to deduct credits."""
    user_id: str
    request_id: UUID
    amount: float
    action_type: str

class RefundCreditsDTO(BaseModel):
    """DTO for a request to the Credit Service to refund credits."""
    user_id: str
    request_id: UUID
    amount: float
    reason: str

class CreditServiceRequest(BaseModel):
    """A generic container for credit service requests, if needed."""
    action: str
    payload: Dict[str, Any]