from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel

from creativeflow.services.aigeneration.api.v1.schemas import CustomDimensions, SampleAssetInfo, FinalAssetInfo


class GenerationJobParameters(BaseModel):
    """
    Internal DTO representing the payload sent to the n8n workflow engine.
    """
    generation_request_id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str]
    output_format: str
    custom_dimensions: Optional[CustomDimensions]
    brand_kit_id: Optional[str]
    uploaded_image_references: Optional[List[str]]
    target_platform_hints: Optional[List[str]]
    emotional_tone: Optional[str]
    cultural_adaptation_parameters: Optional[Dict[str, Any]]
    
    # n8n specific parameters
    job_type: str  # e.g., "sample_generation", "final_generation", "sample_regeneration"
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str
    
    # Parameters for final/regeneration jobs
    selected_sample_id: Optional[str]
    desired_resolution: Optional[str]


class N8NResultInternal(BaseModel):
    """
    Internal DTO for processing n8n callback data.
    This can be a union of the different callback types if needed,
    but for now, the API schemas are used directly in the orchestration service.
    """
    generation_request_id: UUID
    status: str
    samples: Optional[List[SampleAssetInfo]]
    final_asset: Optional[FinalAssetInfo]
    error_message: Optional[str]
    error_details: Optional[Dict[str, Any]]


class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    """
    user_id: str
    request_id: UUID
    amount: float
    action_type: str # e.g., "deduct", "refund"
    reason: Optional[str]