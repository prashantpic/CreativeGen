from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, PrivateAttr

from .generation_status import GenerationStatus


class GenerationRequest:
    """
    Domain model for an AI creative generation request.
    This class encapsulates the state and behavior of a single generation task.
    It is framework-agnostic and represents the core business entity.
    """
    id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str]
    input_parameters: Dict[str, Any]
    status: GenerationStatus
    error_message: Optional[str]
    error_details: Optional[Dict[str, Any]]
    sample_asset_infos: List[Dict[str, Any]]
    selected_sample_id: Optional[str]
    final_asset_info: Optional[Dict[str, Any]]
    credits_cost_sample: Optional[float]
    credits_cost_final: Optional[float]
    ai_model_used: Optional[str]
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: UUID,
        user_id: str,
        project_id: str,
        input_prompt: str,
        input_parameters: Dict[str, Any],
        status: GenerationStatus,
        style_guidance: Optional[str] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
        sample_asset_infos: Optional[List[Dict[str, Any]]] = None,
        selected_sample_id: Optional[str] = None,
        final_asset_info: Optional[Dict[str, Any]] = None,
        credits_cost_sample: Optional[float] = None,
        credits_cost_final: Optional[float] = None,
        ai_model_used: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.project_id = project_id
        self.input_prompt = input_prompt
        self.style_guidance = style_guidance
        self.input_parameters = input_parameters
        self.status = status
        self.error_message = error_message
        self.error_details = error_details
        self.sample_asset_infos = sample_asset_infos or []
        self.selected_sample_id = selected_sample_id
        self.final_asset_info = final_asset_info
        self.credits_cost_sample = credits_cost_sample
        self.credits_cost_final = credits_cost_final
        self.ai_model_used = ai_model_used
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None):
        """
        Updates the status of the request and sets the update timestamp.
        """
        if self.status == new_status:
            return # No change
            
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.utcnow()

    def add_sample_results(self, samples: List[Dict[str, Any]]):
        """
        Adds the results from a sample generation stage.
        """
        self.sample_asset_infos = samples
        self.updated_at = datetime.utcnow()
    
    def set_final_asset(self, final_asset: Dict[str, Any]):
        """
        Sets the final asset information upon completion.
        """
        self.final_asset_info = final_asset
        self.updated_at = datetime.utcnow()

    def set_selected_sample(self, sample_id: str):
        """
        Records the ID of the sample selected by the user for the final stage.
        """
        self.selected_sample_id = sample_id
        self.updated_at = datetime.utcnow()