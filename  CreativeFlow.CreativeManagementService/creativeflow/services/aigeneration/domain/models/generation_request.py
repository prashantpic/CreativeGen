from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .generation_status import GenerationStatus
from .asset_info import AssetInfo

class GenerationRequest(BaseModel):
    """
    Domain model representing an AI creative generation request.
    This class encapsulates the data and state of a single request.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    project_id: str
    
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Dict[str, Any] # Stores a copy of all original request params
    
    status: GenerationStatus = GenerationStatus.PENDING
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None

    sample_asset_infos: Optional[List[Dict[str, Any]]] = None
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[Dict[str, Any]] = None
    
    credits_cost_sample: Optional[float] = None
    credits_cost_final: Optional[float] = None
    
    ai_model_used: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None):
        """Changes the status of the request and updates the timestamp."""
        self.status = new_status
        if error_message:
            self.error_message = error_message
        self.touch()

    def add_sample_results(self, samples: List[AssetInfo]):
        """Adds sample asset information to the request."""
        self.sample_asset_infos = [sample.dict() for sample in samples]
        self.touch()
    
    def set_final_asset(self, final_asset: AssetInfo):
        """Sets the final asset information."""
        self.final_asset_info = final_asset.dict()
        self.touch()

    def set_selected_sample(self, sample_id: str):
        """Records the ID of the selected sample."""
        self.selected_sample_id = sample_id
        self.touch()

    def touch(self):
        """Updates the updated_at timestamp to the current time."""
        self.updated_at = datetime.now(timezone.utc)

    class Config:
        # Pydantic will validate that status is an instance of GenerationStatus
        use_enum_values = False
        validate_assignment = True