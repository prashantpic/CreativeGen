"""
This module contains Pydantic Data Transfer Objects (DTOs) for AI creative
generation requests and responses. They define the data structures for initiating
and tracking AI generation tasks.
"""
from typing import Any, Dict, List, Optional
from uuid import UUID

from .base import BaseDTO, BaseResponseDTO


# =============================================================================
# Request DTOs
# =============================================================================

class GenerationCreateRequestDTO(BaseDTO):
    """DTO for initiating a new AI generation job."""
    project_id: UUID
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Optional[Dict[str, Any]] = None # e.g., resolution, aspect_ratio


class GenerationUpscaleRequestDTO(BaseDTO):
    """DTO for requesting an upscale of a selected sample asset."""
    generation_request_id: UUID
    selected_sample_asset_id: UUID


# =============================================================================
# Response DTOs
# =============================================================================

class GenerationStatusResponseDTO(BaseResponseDTO):
    """DTO for returning the status and details of a generation request."""
    user_id: UUID
    project_id: UUID
    status: str  # e.g., 'Pending', 'ProcessingSamples', 'Completed', 'Failed'
    error_message: Optional[str] = None
    sample_assets: Optional[List[Dict[str, Any]]] = None  # List of asset references
    final_asset_id: Optional[UUID] = None
    credits_cost_sample: Optional[float] = None
    credits_cost_final: Optional[float] = None
    ai_model_used: Optional[str] = None


class GenerationFinalResponseDTO(GenerationStatusResponseDTO):
    """A more specific DTO confirming the final asset is ready."""
    final_asset_id: UUID
    status: str = "Completed"