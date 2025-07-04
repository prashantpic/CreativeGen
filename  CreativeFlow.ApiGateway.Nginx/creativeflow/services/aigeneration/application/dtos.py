from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID

from ..api.v1.schemas import SampleAssetInfo, FinalAssetInfo, CustomDimensions

# DTOs are used for clearer data contracts between application layers,
# decoupling them from the direct API schemas or domain models.

class GenerationRequestCreateDTO(BaseModel):
    """
    Data Transfer Object for creating a new generation request.
    Passed from the API layer to the OrchestrationService.
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

class N8NJobPayloadDTO(BaseModel):
    """
    Data Transfer Object for the payload sent to n8n via RabbitMQ.
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
    
    # Parameters for final/regeneration jobs
    selected_sample_id: Optional[str]
    desired_resolution: Optional[str]

    # Control flow and callbacks
    job_type: str  # e.g., "sample_generation", "final_generation", "sample_regeneration"
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str


class CreditServiceRequest(BaseModel):
    """
    DTO for requests to the Credit Service Client.
    """
    user_id: str
    request_id: UUID
    amount: float
    action_type: str
    reason: Optional[str]


class NotificationRequestDTO(BaseModel):
    """
    DTO for requests to the Notification Service Client.
    """
    user_id: str
    notification_type: str
    message: str
    payload: Optional[Dict[str, Any]]