from uuid import UUID
from pydantic import BaseModel

"""
This file defines domain events. In a more advanced event-driven architecture,
these might be published to a message broker (like RabbitMQ, on a different
exchange/topic) for other services to consume.

For now, they serve as a conceptual model. The OrchestrationService currently
calls other services directly (like the NotificationServiceClient) instead of
publishing these events.
"""

class BaseEvent(BaseModel):
    request_id: UUID
    user_id: str

class GenerationRequestInitiatedEvent(BaseEvent):
    pass

class SampleGenerationCompletedEvent(BaseEvent):
    sample_count: int

class FinalAssetGeneratedEvent(BaseEvent):
    asset_url: str

class GenerationFailedEvent(BaseEvent):
    error_message: str
    is_system_error: bool