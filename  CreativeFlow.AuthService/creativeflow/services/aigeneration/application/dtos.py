from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

"""
This file contains Data Transfer Objects (DTOs) used for internal communication
between different layers of the application (e.g., API layer to Application Service layer).
They can be similar to API schemas but provide a layer of separation, allowing
internal data structures to evolve independently of the public API contract.
"""

class GenerationJobParameters(BaseModel):
    """
    DTO for constructing the payload sent to the n8n RabbitMQ queue.
    """
    generation_request_id: str
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
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str
    job_type: str  # e.g., "sample_generation", "final_generation", "sample_regeneration"
    # Fields specific to final generation or regeneration
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None


class N8NResultInternal(BaseModel):
    """
    A generic internal representation of a result from an n8n callback.
    """
    generation_request_id: UUID
    status: str
    data: Dict[str, Any]


class CreditServiceRequest(BaseModel):
    """
    DTO for making requests to the Credit Service Client.
    """
    user_id: str
    request_id: UUID
    amount: float
    action_type: str
    reason: Optional[str] = None