from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, Field, validator

from .generation_status import GenerationStatus
from .asset_info import AssetInfo

class GenerationRequest(BaseModel):
    """
    The domain model (Aggregate Root) for an AI generation request.
    This class encapsulates the state and business logic of a generation request.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    project_id: str
    
    # Core input parameters
    input_prompt: str
    style_guidance: Optional[str] = None
    output_format: str
    custom_dimensions: Optional[Dict[str, int]] = None
    brand_kit_id: Optional[str] = None
    uploaded_image_references: Optional[List[str]] = []
    target_platform_hints: Optional[List[str]] = []
    emotional_tone: Optional[str] = None
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = None
    
    # State and results
    status: GenerationStatus = Field(default=GenerationStatus.PENDING)
    error_message: Optional[str] = None
    
    # Asset information
    sample_asset_infos: Optional[List[AssetInfo]] = []
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[AssetInfo] = None
    
    # Financial and metadata
    credits_cost_sample: Optional[Decimal] = None
    credits_cost_final: Optional[Decimal] = None
    ai_model_used: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        orm_mode = True
        validate_assignment = True # Ensures validators run when attributes are changed
        arbitrary_types_allowed = True # For Decimal type

    @validator('updated_at', pre=True, always=True)
    def set_updated_at(cls, v):
        """Ensures updated_at is always current."""
        return datetime.now(timezone.utc)

    def update_status(self, new_status: GenerationStatus, error_msg: Optional[str] = None) -> None:
        """
        Updates the status of the request and handles associated state changes.
        This is the primary method for state transitions.
        """
        if self.status == new_status:
            return # No change
            
        # Add any business rule validation for state transitions here if needed
        # For example: if self.status is COMPLETED, it cannot be changed.
        
        self.status = new_status
        self.error_message = error_msg if new_status in [GenerationStatus.FAILED, GenerationStatus.CONTENT_REJECTED] else None
        self.touch()
        
    def add_sample_results(self, samples: List[AssetInfo]) -> None:
        """Adds a list of generated sample assets to the request."""
        self.sample_asset_infos.extend(samples)
        self.touch()
        
    def set_final_asset(self, final_asset: AssetInfo) -> None:
        """Sets the final generated asset information."""
        self.final_asset_info = final_asset
        self.touch()
        
    def set_selected_sample(self, sample_asset_id: str) -> None:
        """Records the user's selected sample ID."""
        if not any(s.asset_id == sample_asset_id for s in self.sample_asset_infos or []):
            raise ValueError(f"Sample asset ID '{sample_asset_id}' not found in this request.")
        self.selected_sample_id = sample_asset_id
        self.touch()

    def touch(self) -> None:
        """Manually updates the 'updated_at' timestamp."""
        self.updated_at = datetime.now(timezone.utc)