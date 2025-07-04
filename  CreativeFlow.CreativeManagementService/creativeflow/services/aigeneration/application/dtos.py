from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, HttpUrl

from ..api.v1.schemas import CustomDimensions, SampleAssetInfo, FinalAssetInfo

# DTOs can be used to decouple the application layer from the API layer.
# For this service, the API schemas are often suitable for direct use in the
# service layer, but defining separate DTOs provides a layer of insulation.

class GenerationRequestCreateDTO(BaseModel):
    """
    Data Transfer Object for creating a generation request.
    Mirrors the API schema but is an internal contract.
    """
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

class N8NSampleResultDTO(BaseModel):
    """
    DTO for n8n sample result callbacks.
    """
    generation_request_id: UUID
    status: str
    samples: List[SampleAssetInfo]

class N8NFinalResultDTO(BaseModel):
    """
    DTO for n8n final result callbacks.
    """
    generation_request_id: UUID
    status: str
    final_asset: FinalAssetInfo

class N8NErrorDTO(BaseModel):
    """
    DTO for n8n error callbacks.
    """
    generation_request_id: UUID
    error_code: Optional[str]
    error_message: str
    error_details: Optional[Dict[str, Any]]
    failed_stage: Optional[str]

class GenerationJobParameters(BaseModel):
    """
    Defines the structure of the job payload sent to RabbitMQ for n8n.
    """
    generation_request_id: str
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
    callback_url_sample_result: HttpUrl
    callback_url_final_result: HttpUrl
    callback_url_error: HttpUrl
    job_type: str # e.g., "sample_generation", "final_generation", "sample_regeneration"
    # Fields for final generation / regeneration
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None

class CreditServiceRequest(BaseModel):
    """
    DTO for requests to the Credit Service Client.
    """
    user_id: str
    amount: float
    request_id: Optional[UUID] = None
    action_type: Optional[str] = None
    reason: Optional[str] = None