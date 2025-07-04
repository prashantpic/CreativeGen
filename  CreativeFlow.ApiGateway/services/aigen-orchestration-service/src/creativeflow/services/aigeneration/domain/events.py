from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

"""
This file defines conceptual domain events.
These can be used for internal signaling or published to a message broker
for other services to consume if a more event-driven architecture is desired.
"""

class BaseEvent(BaseModel):
    request_id: UUID
    user_id: str

class GenerationRequestInitiatedEvent(BaseEvent):
    project_id: str
    input_prompt: str

class SampleGenerationCompletedEvent(BaseEvent):
    sample_count: int
    sample_urls: List[str]

class FinalAssetGeneratedEvent(BaseEvent):
    asset_url: str
    asset_id: str

class GenerationFailedEvent(BaseEvent):
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]