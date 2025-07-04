"""
Defines the GenerationRequest domain entity. This class encapsulates the state
and behavior of a single AI generation job, from initiation to completion or failure.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class GenerationStatus(str, Enum):
    """
    Represents the possible statuses of a GenerationRequest.
    """
    PENDING = 'Pending'
    PROCESSING_SAMPLES = 'ProcessingSamples'
    AWAITING_SELECTION = 'AwaitingSelection'
    PROCESSING_FINAL = 'ProcessingFinal'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    CANCELLED = 'Cancelled'
    CONTENT_REJECTED = 'ContentRejected'


@dataclass
class GenerationRequest:
    """
    The central domain model, representing a single AI generation job.
    It holds all relevant data for a single request and contains methods
    that enforce valid state transitions, ensuring the entity is always
    in a consistent state.
    """
    id: UUID = field(default_factory=uuid4)
    userId: UUID
    projectId: UUID
    inputPrompt: str
    styleGuidance: Optional[str]
    inputParameters: dict
    status: GenerationStatus = GenerationStatus.PENDING
    errorMessage: Optional[str] = None
    sampleAssets: Optional[dict] = None
    selectedSampleId: Optional[UUID] = None
    finalAssetId: Optional[UUID] = None
    creditsCostSample: Optional[Decimal] = None
    creditsCostFinal: Optional[Decimal] = None
    aiModelUsed: Optional[str] = None
    createdAt: datetime = field(default_factory=datetime.utcnow)
    updatedAt: datetime = field(default_factory=datetime.utcnow)

    def mark_as_processing_samples(self) -> None:
        """Sets status to ProcessingSamples."""
        if self.status == GenerationStatus.PENDING:
            self.status = GenerationStatus.PROCESSING_SAMPLES
            self.updatedAt = datetime.utcnow()
        else:
            raise ValueError(f"Cannot transition from {self.status} to ProcessingSamples")

    def mark_as_awaiting_selection(self, sample_assets: dict) -> None:
        """Sets status and stores sample asset data."""
        if self.status == GenerationStatus.PROCESSING_SAMPLES:
            self.status = GenerationStatus.AWAITING_SELECTION
            self.sampleAssets = sample_assets
            self.updatedAt = datetime.utcnow()
        else:
            raise ValueError(f"Cannot transition from {self.status} to AwaitingSelection")

    def mark_as_processing_final(self, selected_sample_id: UUID) -> None:
        """Sets status to ProcessingFinal and records selectedSampleId."""
        if self.status == GenerationStatus.AWAITING_SELECTION:
            self.status = GenerationStatus.PROCESSING_FINAL
            self.selectedSampleId = selected_sample_id
            self.updatedAt = datetime.utcnow()
        else:
            raise ValueError(f"Cannot transition from {self.status} to ProcessingFinal")

    def mark_as_completed(self, final_asset_id: UUID) -> None:
        """Sets status to Completed and records finalAssetId."""
        if self.status in [GenerationStatus.PROCESSING_FINAL, GenerationStatus.PROCESSING_SAMPLES]:
            self.status = GenerationStatus.COMPLETED
            self.finalAssetId = final_asset_id
            self.updatedAt = datetime.utcnow()
        else:
            raise ValueError(f"Cannot transition from {self.status} to Completed")

    def mark_as_failed(self, error_message: str) -> None:
        """Sets status to Failed and records the error message."""
        self.status = GenerationStatus.FAILED
        self.errorMessage = error_message
        self.updatedAt = datetime.utcnow()