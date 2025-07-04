from pydantic import BaseModel, AnyHttpUrl
from typing import Optional, List, Dict, Any
from uuid import UUID

from creativeflow.services.aigeneration.api.v1 import schemas as api_schemas

# DTOs can be aliases if no transformation is needed, or separate classes for decoupling.
# Using separate classes for clarity and future-proofing.

class GenerationRequestCreateDTO(api_schemas.GenerationRequestCreate):
    """
    Data Transfer Object for creating a generation request.
    Mirrors the API schema for now.
    """
    pass

class N8NSampleResultDTO(api_schemas.N8NSampleResultPayload):
    """
    Data Transfer Object for n8n sample results.
    """
    pass

class N8NFinalResultDTO(api_schemas.N8NFinalResultPayload):
    """
    Data Transfer Object for n8n final asset results.
    """
    pass

class N8NErrorDTO(api_schemas.N8NErrorPayload):
    """
    Data Transfer Object for n8n error callbacks.
    """
    pass

class GenerationJobParameters(BaseModel):
    """
    Internal representation of the data payload sent to n8n via RabbitMQ.
    """
    generation_request_id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str]
    output_format: str
    custom_dimensions: Optional[api_schemas.CustomDimensions]
    brand_kit_id: Optional[str]
    uploaded_image_references: Optional[List[str]]
    target_platform_hints: Optional[List[str]]
    emotional_tone: Optional[str]
    cultural_adaptation_parameters: Optional[Dict[str, Any]]
    
    # Callbacks
    callback_url_sample_result: AnyHttpUrl
    callback_url_final_result: AnyHttpUrl
    callback_url_error: AnyHttpUrl
    
    # Job type
    job_type: str # e.g., "sample_generation", "final_generation", "sample_regeneration"

    # Additional parameters for specific job types
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None

class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    Example DTO, might not be needed if parameters are simple.
    """
    user_id: str
    amount: float
    request_id: UUID
    action_type: str
    reason: Optional[str] = None