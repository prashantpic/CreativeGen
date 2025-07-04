from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from .generation_status import GenerationStatus
from .asset_info import AssetInfo

class GenerationRequest:
    """
    Domain model representing an AI creative generation request.
    This class encapsulates the state and behavior of a generation request.
    """

    def __init__(
        self,
        id: uuid.UUID,
        user_id: str,
        project_id: str,
        input_prompt: str,
        status: GenerationStatus,
        created_at: datetime,
        updated_at: datetime,
        style_guidance: Optional[str] = None,
        input_parameters: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
        sample_asset_infos: Optional[List[AssetInfo]] = None,
        selected_sample_id: Optional[str] = None,
        final_asset_info: Optional[AssetInfo] = None,
        credits_cost_sample: Optional[float] = None,
        credits_cost_final: Optional[float] = None,
        ai_model_used: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.project_id = project_id
        self.input_prompt = input_prompt
        self.style_guidance = style_guidance
        self.input_parameters = input_parameters or {}
        self.status = status
        self.error_message = error_message
        self.error_details = error_details or {}
        self.sample_asset_infos = sample_asset_infos or []
        self.selected_sample_id = selected_sample_id
        self.final_asset_info = final_asset_info
        self.credits_cost_sample = credits_cost_sample
        self.credits_cost_final = credits_cost_final
        self.ai_model_used = ai_model_used
        self.created_at = created_at
        self.updated_at = updated_at

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None):
        """Changes the status of the request and updates the timestamp."""
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)
        if new_status != GenerationStatus.FAILED and new_status != GenerationStatus.CONTENT_REJECTED:
            self.error_message = None # Clear error on non-failure status updates

    def add_sample_results(self, sample_assets: List[AssetInfo]):
        """Appends a list of sample asset results."""
        self.sample_asset_infos.extend(sample_assets)
        self.updated_at = datetime.now(timezone.utc)

    def set_final_asset(self, final_asset: AssetInfo):
        """Sets the final asset information."""
        self.final_asset_info = final_asset
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str):
        """Records the ID of the selected sample."""
        if not any(s.asset_id == sample_id for s in self.sample_asset_infos):
            raise ValueError(f"Sample with ID {sample_id} not found in this request.")
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<GenerationRequest(id={self.id}, status='{self.status.value}')>"