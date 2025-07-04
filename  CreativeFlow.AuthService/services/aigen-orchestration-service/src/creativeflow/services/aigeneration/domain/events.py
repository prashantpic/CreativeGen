from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class DomainEvent(BaseModel):
    """Base class for all domain events."""
    event_id: UUID = Field(default_factory=UUID)
    occurred_on: datetime = Field(default_factory=datetime.utcnow)

class GenerationRequestInitiatedEvent(DomainEvent):
    """Event raised when a new generation request is successfully initiated."""
    request_id: UUID
    user_id: str
    project_id: str

class SampleGenerationCompletedEvent(DomainEvent):
    """Event raised when n8n returns a successful sample generation result."""
    request_id: UUID
    user_id: str
    sample_count: int

class FinalAssetGeneratedEvent(DomainEvent):
    """Event raised when n8n returns a final generated asset."""
    request_id: UUID
    user_id: str
    asset_url: str

class GenerationFailedEvent(DomainEvent):
    """Event raised when a generation process fails for any reason."""
    request_id: UUID
    user_id: str
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]

# Note: These events are defined conceptually. Their actual implementation (e.g., publishing
# to a message queue) would be handled by the OrchestrationService or a dedicated
# event publisher service if a more event-driven architecture is desired.