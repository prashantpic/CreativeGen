from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, validator

from .generation_status import GenerationStatus

class GenerationRequest(BaseModel):
    """
    Domain model representing an AI creative generation request.
    This is the aggregate root for the generation context.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    status: GenerationStatus = GenerationStatus.PENDING
    error_message: Optional[str] = None
    sample_asset_infos: List[Dict[str, Any]] = Field(default_factory=list)
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[Dict[str, Any]] = None
    credits_cost_sample: Optional[float] = None
    credits_cost_final: Optional[float] = None
    ai_model_used: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        validate_assignment = True # Allows fields to be updated and re-validated

    @validator('updated_at', pre=True, always=True)
    def set_updated_at(cls, v):
        return datetime.now(timezone.utc)
        
    @classmethod
    def create_new(
        cls,
        user_id: str,
        project_id: str,
        input_prompt: str,
        status: GenerationStatus,
        style_guidance: Optional[str] = None,
        input_parameters: Optional[Dict[str, Any]] = None,
    ) -> GenerationRequest:
        """Factory method to create a new GenerationRequest instance."""
        return cls(
            user_id=user_id,
            project_id=project_id,
            input_prompt=input_prompt,
            status=status,
            style_guidance=style_guidance,
            input_parameters=input_parameters or {},
        )

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None):
        """Updates the status of the request and the updated_at timestamp."""
        if self.status == new_status:
            return # No change
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)

    def add_sample_results(self, sample_assets: List[Dict[str, Any]]):
        """Appends a list of sample asset information."""
        self.sample_asset_infos.extend(sample_assets)
        self.updated_at = datetime.now(timezone.utc)

    def set_final_asset(self, final_asset: Dict[str, Any]):
        """Sets the final asset information."""
        self.final_asset_info = final_asset
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str):
        """Records the ID of the selected sample."""
        if not any(sample['asset_id'] == sample_id for sample in self.sample_asset_infos):
            raise ValueError(f"Sample with ID {sample_id} not found in this request.")
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)

    def set_credit_cost(self, sample_cost: float = 0.0, final_cost: float = 0.0, append: bool = False):
        """Sets or appends the credit cost for generation stages."""
        if sample_cost:
            if append and self.credits_cost_sample:
                self.credits_cost_sample += sample_cost
            else:
                self.credits_cost_sample = sample_cost
        
        if final_cost:
            self.credits_cost_final = final_cost
        
        self.updated_at = datetime.now(timezone.utc)