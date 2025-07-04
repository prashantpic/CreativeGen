from __future__ import annotations
import dataclasses
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from uuid import UUID

from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus

@dataclasses.dataclass
class GenerationRequest:
    """
    Domain model representing an AI creative generation request.
    This class encapsulates the data and behavior of a generation request
    throughout its lifecycle. It is persistence-agnostic.
    """
    id: UUID
    user_id: str
    project_id: str
    input_prompt: str
    status: GenerationStatus
    created_at: datetime
    updated_at: datetime
    
    style_guidance: Optional[str] = None
    input_parameters: Dict[str, Any] = dataclasses.field(default_factory=dict)
    error_message: Optional[str] = None
    sample_asset_infos: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    selected_sample_id: Optional[str] = None
    final_asset_info: Optional[Dict[str, Any]] = None
    credits_cost_sample: Optional[float] = None
    credits_cost_final: Optional[float] = None
    ai_model_used: Optional[str] = None

    def update_status(self, new_status: GenerationStatus, error_message: Optional[str] = None) -> None:
        """Changes the request's status and updates the timestamp."""
        self.status = new_status
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)

    def add_sample_result(self, sample_asset_info: Dict[str, Any]) -> None:
        """Appends a new sample asset's information."""
        self.sample_asset_infos.append(sample_asset_info)
        self.updated_at = datetime.now(timezone.utc)

    def set_final_asset(self, final_asset_info: Dict[str, Any]) -> None:
        """Sets the final asset's information."""
        self.final_asset_info = final_asset_info
        self.updated_at = datetime.now(timezone.utc)

    def set_selected_sample(self, sample_id: str) -> None:
        """Records the ID of the selected sample."""
        self.selected_sample_id = sample_id
        self.updated_at = datetime.now(timezone.utc)
        
    def set_credits_cost(self, sample_cost: Optional[float] = None, final_cost: Optional[float] = None) -> None:
        """Sets the credit costs for different stages."""
        if sample_cost is not None:
            self.credits_cost_sample = sample_cost
        if final_cost is not None:
            self.credits_cost_final = final_cost
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the domain model to a dictionary."""
        return dataclasses.asdict(self)
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GenerationRequest:
        """Creates a domain model instance from a dictionary."""
        # Convert status string from DB back to Enum
        status_str = data.get("status")
        if status_str and isinstance(status_str, str):
            data["status"] = GenerationStatus(status_str)
            
        return cls(**data)