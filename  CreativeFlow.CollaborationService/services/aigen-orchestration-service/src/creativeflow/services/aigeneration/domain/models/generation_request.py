from __future__ import annotations
import logging
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from decimal import Decimal

from pydantic import BaseModel, Field

from .generation_status import GenerationStatus
from .asset_info import AssetInfo

logger = logging.getLogger(__name__)

class GenerationRequest(BaseModel):
    """
    Domain model representing an AI creative generation request.
    This is the aggregate root for the generation process.
    """
    id: UUID = Field(default_factory=uuid4)
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
    credits_cost_sample: Optional[Decimal] = None
    credits_cost_final: Optional[Decimal] = None
    ai_model_used: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        validate_assignment = True # Allows field updates to be validated

    @classmethod
    def create(
        cls,
        user_id: str,
        project_id: str,
        input_prompt: str,
        style_guidance: Optional[str] = None,
        input_parameters: Optional[Dict[str, Any]] = None,
    ) -> GenerationRequest:
        """Factory method to create a new GenerationRequest."""
        logger.info(f"Creating new GenerationRequest for user {user_id}")
        return cls(
            user_id=user_id,
            project_id=project_id,
            input_prompt=input_prompt,
            style_guidance=style_guidance,
            input_parameters=input_parameters or {},
        )

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None):
        """Changes the status of the request and updates the timestamp."""
        logger.info(f"Updating status for request {self.id} from {self.status.value} to {new_status.value}")
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)

    def add_sample_results(self, sample_assets: List[Dict[str, Any]]):
        """Appends a list of sample asset info dictionaries."""
        logger.info(f"Adding {len(sample_assets)} samples to request {self.id}")
        self.sample_asset_infos.extend(sample_assets)
        self.updated_at = datetime.now(timezone.utc)

    def set_final_asset(self, final_asset: Dict[str, Any]):
        """Sets the final asset info dictionary."""
        logger.info(f"Setting final asset for request {self.id}")
        self.final_asset_info = final_asset
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str):
        """Records the ID of the selected sample."""
        logger.info(f"Setting selected sample for request {self.id} to {sample_id}")
        if not any(s.get('asset_id') == sample_id for s in self.sample_asset_infos):
            logger.error(f"Attempted to select invalid sample_id {sample_id} for request {self.id}")
            raise ValueError(f"Sample with asset_id '{sample_id}' not found in this request.")
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)