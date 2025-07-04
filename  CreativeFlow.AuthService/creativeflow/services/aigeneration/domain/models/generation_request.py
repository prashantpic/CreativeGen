import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from .generation_status import GenerationStatus


class GenerationRequest(BaseModel):
    """
    Domain model representing an AI creative generation request.
    This class encapsulates the data and behavior of a request throughout its lifecycle.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    project_id: str
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    status: GenerationStatus = GenerationStatus.PENDING
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    sample_asset_infos: List[Dict[str, Any]] = Field(default_factory=list)
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[Dict[str, Any]] = None
    credits_cost_sample: Optional[Decimal] = None
    credits_cost_final: Optional[Decimal] = None
    ai_model_used: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            uuid.UUID: lambda v: str(v),
        }

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None, error_details: Optional[Dict[str, Any]] = None):
        """Changes status, logs timestamp, and sets error message if any."""
        self.status = new_status
        self.error_message = error_message
        self.error_details = error_details
        self.updated_at = datetime.now(timezone.utc)

    def add_sample_results(self, sample_assets: List[Dict[str, Any]]):
        """Appends a list of sample asset info dicts."""
        self.sample_asset_infos.extend(sample_assets)
        self.updated_at = datetime.now(timezone.utc)

    def set_final_asset(self, final_asset: Dict[str, Any]):
        """Sets the final asset info."""
        self.final_asset_info = final_asset
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str):
        """Sets the selected sample ID."""
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)