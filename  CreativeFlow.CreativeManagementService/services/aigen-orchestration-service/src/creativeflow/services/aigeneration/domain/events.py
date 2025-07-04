"""
Domain Events for the AI Generation Lifecycle.

This module defines Pydantic models for significant events that occur within
the AI generation domain. These events can be used for various purposes,
such as decoupling services, triggering side effects (like analytics), or
implementing a more event-driven architecture internally.

Note: As per the SDS, these are conceptual for now. Actual publishing of these
events would require further implementation in the OrchestrationService.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class DomainEvent(BaseModel):
    """Base class for all domain events."""
    event_id: UUID = Field(default_factory=UUID)
    occurred_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GenerationRequestInitiatedEvent(DomainEvent):
    """Event published when a new generation request is successfully initiated."""
    request_id: UUID
    user_id: str
    project_id: str

class SampleGenerationCompletedEvent(DomainEvent):
    """Event published when sample generation is successfully completed."""
    request_id: UUID
    user_id: str
    sample_count: int

class FinalAssetGeneratedEvent(DomainEvent):
    """Event published when the final asset is successfully generated."""
    request_id: UUID
    user_id: str
    asset_url: str

class GenerationFailedEvent(DomainEvent):
    """Event published when a generation process fails for any reason."""
    request_id: UUID
    user_id: str
    error_message: str
    failed_stage: Optional[str]
    is_system_error: bool