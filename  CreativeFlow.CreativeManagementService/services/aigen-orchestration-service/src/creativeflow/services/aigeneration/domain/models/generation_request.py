"""
Domain model representing an AI creative generation request.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field

from .generation_status import GenerationStatus


class GenerationRequest(BaseModel):
    """
    Represents the GenerationRequest domain entity.
    This class encapsulates the data and behavior of a generation request.
    """
    id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    status: GenerationStatus
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    
    # Using Dict for JSONB compatibility in repo layer, validated by AssetInfo schema elsewhere
    sample_asset_infos: Optional[List[Dict[str, Any]]] = None 
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[Dict[str, Any]] = None

    credits_cost_sample: Optional[float] = None
    credits_cost_final: Optional[float] = None
    ai_model_used: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime

    class Config:
        validate_assignment = True # Allow fields to be updated

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None) -> None:
        """
        Changes the status of the request and updates the timestamp.
        """
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)

    def add_sample_results(self, sample_assets: List[Dict[str, Any]]) -> None:
        """
        Adds sample asset information to the request.
        """
        self.sample_asset_infos = sample_assets
        self.updated_at = datetime.now(timezone.utc)
    
    def set_final_asset(self, final_asset: Dict[str, Any]) -> None:
        """
        Sets the final asset information for the request.
        """
        self.final_asset_info = final_asset
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str) -> None:
        """
        Records the ID of the selected sample.
        """
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)