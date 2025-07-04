from uuid import UUID
from pydantic import BaseModel
from typing import Optional

# These are conceptual domain events that could be published to a message bus
# for other services to consume if a more event-driven architecture is desired.
# For the current scope, they are defined but not actively published.

class GenerationRequestInitiatedEvent(BaseModel):
    request_id: UUID
    user_id: str

class SampleGenerationCompletedEvent(BaseModel):
    request_id: UUID
    user_id: str
    sample_count: int

class FinalAssetGeneratedEvent(BaseModel):
    request_id: UUID
    user_id: str
    asset_url: str

class GenerationFailedEvent(BaseModel):
    request_id: UUID
    user_id: str
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]