"""
Internal Data Transfer Objects (DTOs) used within the application layer,
potentially differing from API schemas to decouple application logic from the
public-facing API contract.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from creativeflow.services.aigeneration.api.v1 import schemas


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
    custom_dimensions: Optional[schemas.CustomDimensions]
    brand_kit_id: Optional[str]
    uploaded_image_references: Optional[List[str]]
    target_platform_hints: Optional[List[str]]
    emotional_tone: Optional[str]
    cultural_adaptation_parameters: Optional[Dict[str, Any]]
    
    # Callback URLs for n8n
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str
    
    # Job Type Identifier
    job_type: str # e.g., "sample_generation", "final_generation", "sample_regeneration"

    # Specific parameters for final/regeneration jobs
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None


class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    """
    user_id: str
    request_id: UUID
    amount: float
    action_type: Optional[str] = None
    reason: Optional[str] = None

# For internal processing, the API schemas for n8n callbacks can be used directly
# as DTOs, but aliasing them here makes the intent clearer in the service layer.
# This provides a layer of abstraction if they ever need to diverge.

N8NSampleResultDTO = schemas.N8NSampleResultPayload
N8NFinalResultDTO = schemas.N8NFinalResultPayload
N8NErrorDTO = schemas.N8NErrorPayload