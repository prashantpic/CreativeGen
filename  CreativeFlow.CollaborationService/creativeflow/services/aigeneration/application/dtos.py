"""
Data Transfer Objects (DTOs) used for internal communication between layers
of the application. This helps decouple the application logic from the
external API schemas.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel

from creativeflow.services.aigeneration.api.v1 import schemas as api_schemas


class GenerationJobParameters(BaseModel):
    """
    Internal DTO representing the payload to be sent to the n8n workflow.
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
    
    # n8n specific parameters
    job_type: str  # "sample_generation", "final_generation", "sample_regeneration"
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str

    # Parameters for final generation or regeneration
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None

class CreditServiceRequest(BaseModel):
    """
    Internal DTO for making requests to the Credit Service Client.
    """
    user_id: str
    request_id: UUID
    amount: float
    action_type: str
    reason: Optional[str] = None

class NotificationRequest(BaseModel):
    """
    Internal DTO for making requests to the Notification Service Client.
    """
    user_id: str
    notification_type: str
    message: str
    payload: Optional[Dict[str, Any]] = None