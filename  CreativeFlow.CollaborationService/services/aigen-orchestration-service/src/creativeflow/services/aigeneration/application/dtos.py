from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel

from creativeflow.services.aigeneration.api.v1.schemas import CustomDimensions

class GenerationJobParameters(BaseModel):
    """
    Internal DTO for constructing the payload sent to n8n via RabbitMQ.
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
    
    # Parameters for final generation / regeneration
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None


class N8NResultInternal(BaseModel):
    """
    Internal DTO to represent data from n8n callbacks within the application layer.
    This can be a union of different callback types in a more complex scenario.
    """
    generation_request_id: UUID
    # This DTO is conceptual; in practice, the application service directly
    # uses the Pydantic schemas from the API layer for n8n callbacks
    # to avoid redundant mapping. If the internal logic diverges significantly
    # from the callback structure, this DTO becomes more useful.

class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    """
    user_id: str
    request_id: Optional[UUID] = None # For linking transactions
    amount: float
    action_type: Optional[str] = None
    reason: Optional[str] = None