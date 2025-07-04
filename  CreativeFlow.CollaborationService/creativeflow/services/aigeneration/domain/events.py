"""
This module defines conceptual domain events.
In a fully event-driven architecture, these might be published to a message bus
for other services to consume. For now, they serve as structured representations
of significant occurrences within the domain.
"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class DomainEvent(BaseModel):
    """Base class for all domain events."""
    event_id: UUID = Field(default_factory=UUID)
    occurred_on: str = Field(..., description="ISO 8601 timestamp of when the event occurred.")

class GenerationRequestInitiatedEvent(DomainEvent):
    request_id: UUID
    user_id: str

class SampleGenerationCompletedEvent(DomainEvent):
    request_id: UUID
    user_id: str
    sample_count: int

class FinalAssetGeneratedEvent(DomainEvent):
    request_id: UUID
    user_id: str
    asset_url: str

class GenerationFailedEvent(DomainEvent):
    request_id: UUID
    user_id: str
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]