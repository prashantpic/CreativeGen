from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DomainEvent(BaseModel):
    """Base class for domain events."""
    event_id: UUID
    request_id: UUID
    user_id: str


class GenerationRequestInitiatedEvent(DomainEvent):
    """
    Event published when a new generation request is successfully initiated.
    """
    project_id: str


class SampleGenerationCompletedEvent(DomainEvent):
    """

    Event published when the sample generation stage is complete and samples are ready for review.
    """
    sample_count: int


class FinalAssetGeneratedEvent(DomainEvent):
    """
    Event published when the final asset has been successfully generated.
    """
    asset_url: str


class GenerationFailedEvent(DomainEvent):
    """
    Event published when a generation request fails at any stage.
    """
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]