from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, timezone

class BaseEvent(BaseModel):
    """Base model for all domain events."""
    event_id: UUID = Field(default_factory=UUID)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GenerationRequestInitiatedEvent(BaseEvent):
    """Event raised when a new generation request is successfully initiated."""
    request_id: UUID
    user_id: str

class SampleGenerationCompletedEvent(BaseEvent):
    """Event raised when sample generation is complete and ready for selection."""
    request_id: UUID
    user_id: str
    sample_count: int

class FinalAssetGeneratedEvent(BaseEvent):
    """Event raised when the final asset has been generated and is ready."""
    request_id: UUID
    user_id: str
    asset_url: str

class GenerationFailedEvent(BaseEvent):
    """Event raised when a generation process fails for any reason."""
    request_id: UUID
    user_id: str
    error_message: str
    is_system_error: bool