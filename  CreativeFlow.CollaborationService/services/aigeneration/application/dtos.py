from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID

# DTOs are used for internal data transfer between layers,
# decoupling the application logic from the API schemas or database models.

class GenerationJobParameters(BaseModel):
    """
    Internal representation of data sent to n8n for a generation job.
    """
    generation_request_id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str]
    output_format: str
    custom_dimensions: Optional[Dict[str, int]]
    brand_kit_id: Optional[str]
    uploaded_image_references: Optional[List[str]]
    target_platform_hints: Optional[List[str]]
    emotional_tone: Optional[str]
    cultural_adaptation_parameters: Optional[Dict[str, Any]]
    job_type: str  # e.g., "sample_generation", "final_generation", "sample_regeneration"
    
    # Callback URLs for n8n
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str
    
    # Parameters for specific job types
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None


class AssetInfoInternal(BaseModel):
    """Internal DTO for asset information."""
    asset_id: str
    url: str
    resolution: str
    format: str
    metadata: Optional[Dict[str, Any]] = None

class N8NSampleResultInternal(BaseModel):
    """
    Internal representation of data received from n8n sample result callback.
    """
    generation_request_id: UUID
    samples: List[AssetInfoInternal]

class N8NFinalResultInternal(BaseModel):
    """
    Internal representation of data received from n8n final result callback.
    """
    generation_request_id: UUID
    final_asset: AssetInfoInternal

class N8NErrorInternal(BaseModel):
    """
    Internal representation of data received from n8n error callback.
    """
    generation_request_id: UUID
    error_code: Optional[str]
    error_message: str
    error_details: Optional[Dict[str, Any]]
    failed_stage: Optional[str]


class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    """
    user_id: str
    amount: float
    request_id: Optional[UUID] = None
    action_type: Optional[str] = None
    reason: Optional[str] = None