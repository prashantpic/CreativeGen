from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field

from .generation_status import GenerationStatus
from .asset_info import AssetInfo

class GenerationRequest(BaseModel):
    """
    Domain model representing an AI creative generation request.
    This class encapsulates the data and state transitions of a request.
    """
    id: UUID
    user_id: str
    project_id: str
    
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    status: GenerationStatus = Field(default=GenerationStatus.PENDING)
    error_message: Optional[str] = None
    
    sample_asset_infos: Optional[List[AssetInfo]] = Field(default_factory=list)
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[AssetInfo] = None
    
    credits_cost_sample: Optional[Decimal] = None
    credits_cost_final: Optional[Decimal] = None
    
    ai_model_used: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        validate_assignment = True # Ensures type validation on attribute assignment

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None) -> None:
        """
        Changes the status of the request and updates the timestamp.
        """
        self.status = new_status
        if error_message:
            self.error_message = error_message
        self.touch()

    def add_sample_result(self, sample_asset: AssetInfo) -> None:
        """Appends a new sample asset to the list."""
        if self.sample_asset_infos is None:
            self.sample_asset_infos = []
        self.sample_asset_infos.append(sample_asset)
        self.touch()

    def set_final_asset(self, final_asset: AssetInfo) -> None:
        """Sets the final asset information."""
        self.final_asset_info = final_asset
        self.touch()

    def set_selected_sample(self, sample_id: str) -> None:
        """Sets the ID of the selected sample."""
        self.selected_sample_id = sample_id
        self.touch()

    def touch(self) -> None:
        """Updates the updated_at timestamp to the current time."""
        self.updated_at = datetime.utcnow()