from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID

from creativeflow.services.aigeneration.api.v1.schemas import GenerationRequestCreate, N8NSampleResultPayload, N8NFinalResultPayload, N8NErrorPayload

"""
This file defines Data Transfer Objects (DTOs) used for internal communication
between different layers of the application (e.g., API layer to Application Service layer).

In this specific design, the API schemas defined in `api.v1.schemas` are directly
reused as DTOs for simplicity, as their structure aligns well with the needs of the
application service layer. This avoids redundant model definitions.

If the internal representation needed to diverge significantly from the API contract,
this file would contain distinct Pydantic models for that purpose.
"""

# Re-exporting API schemas to be used as DTOs
GenerationRequestCreateDTO = GenerationRequestCreate
N8NSampleResultDTO = N8NSampleResultPayload
N8NFinalResultDTO = N8NFinalResultPayload
N8NErrorDTO = N8NErrorPayload


# Example of a DTO that could be different from an API schema
class GenerationJobParameters(BaseModel):
    """
    A distinct DTO representing the exact structure of a job payload
    sent to RabbitMQ. This can help decouple the orchestration logic
    from the specific API request format.
    """
    generation_request_id: UUID
    user_id: str
    project_id: str
    job_type: str = Field(..., description="e.g., 'sample_generation', 'final_generation', 'sample_regeneration'")
    
    # AI Generation Parameters
    input_prompt: str
    style_guidance: Optional[str]
    output_format: str
    custom_dimensions: Optional[Dict[str, int]]
    brand_kit_id: Optional[str]
    uploaded_image_references: Optional[List[str]]
    target_platform_hints: Optional[List[str]]
    emotional_tone: Optional[str]
    cultural_adaptation_parameters: Optional[Dict[str, Any]]
    
    # Parameters for final generation / regeneration
    selected_sample_id: Optional[str] = None
    desired_resolution: Optional[str] = None

    # Callback URLs for n8n
    callback_url_sample_result: str
    callback_url_final_result: str
    callback_url_error: str
    
# DTO for interacting with the credit service
class CreditServiceRequest(BaseModel):
    user_id: str
    request_id: UUID
    amount: float
    action_type: Optional[str]
    reason: Optional[str]