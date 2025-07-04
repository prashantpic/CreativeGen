import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field

from .asset_info import AssetInfo
from .generation_status import GenerationStatus


class GenerationRequest(BaseModel):
    """
    Represents the state and properties of a single AI creative generation task.
    This is the core aggregate root for the generation domain.
    """
    id: UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the generation request.")
    user_id: str = Field(..., description="The ID of the user who initiated the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")

    # Input Parameters
    input_prompt: str = Field(..., description="The primary text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Additional guidance on the desired style.")
    input_parameters: Dict[str, Any] = Field(default_factory=dict, description="A flexible dictionary for all other input parameters, e.g., format, resolution, brand elements.")
    
    # State and Outcome
    status: GenerationStatus = Field(GenerationStatus.PENDING, description="The current status of the generation request.")
    error_message: Optional[str] = Field(None, description="Stores any error message if the request fails.")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Stores structured error details from n8n or internal processes.")

    # Asset Information
    sample_asset_infos: List[AssetInfo] = Field(default_factory=list, description="A list of generated sample assets.")
    selected_sample_id: Optional[str] = Field(None, description="The asset_id of the sample selected by the user for final generation.")
    final_asset_info: Optional[AssetInfo] = Field(None, description="Information about the final generated asset.")
    
    # Cost and Metadata
    credits_cost_sample: Optional[float] = Field(None, description="The number of credits deducted for the sample generation stage.")
    credits_cost_final: Optional[float] = Field(None, description="The number of credits deducted for the final generation stage.")
    ai_model_used: Optional[str] = Field(None, description="The identifier of the specific AI model or workflow used for the generation.")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the request was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the request was last updated.")

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None, error_details: Optional[Dict[str, Any]] = None) -> None:
        """
        Updates the status of the request and sets the update timestamp.
        Optionally records an error message and details.
        """
        self.status = new_status
        self.error_message = error_message
        self.error_details = error_details
        self.updated_at = datetime.utcnow()

    def add_sample_results(self, sample_assets: List[AssetInfo]) -> None:
        """
        Adds a list of generated sample asset information to the request.
        """
        self.sample_asset_infos.extend(sample_assets)
        self.updated_at = datetime.utcnow()
    
    def set_selected_sample(self, sample_id: str) -> None:
        """
        Records the ID of the sample selected by the user for final processing.
        """
        if any(sample.asset_id == sample_id for sample in self.sample_asset_infos):
            self.selected_sample_id = sample_id
            self.updated_at = datetime.utcnow()
        else:
            raise ValueError(f"Sample with ID '{sample_id}' not found in this generation request.")

    def set_final_asset(self, final_asset: AssetInfo) -> None:
        """
        Sets the final generated asset information.
        """
        self.final_asset_info = final_asset
        self.updated_at = datetime.utcnow()

    class Config:
        orm_mode = True
        validate_assignment = True