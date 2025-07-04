from uuid import UUID
from pydantic import BaseModel

"""
This file defines conceptual domain events.
In a more advanced event-driven architecture, these might be published to a message
broker (like RabbitMQ, but on a different exchange/topic) for other services
to consume, promoting further decoupling.

For the current scope, these serve as a conceptual model of key business moments.
The OrchestrationService handles the side effects of these events directly
(e.g., calling the NotificationServiceClient).
"""

class BaseEvent(BaseModel):
    request_id: UUID
    user_id: str

class GenerationRequestInitiatedEvent(BaseEvent):
    """Event fired when a new generation request is successfully created and queued."""
    pass

class SampleGenerationCompletedEvent(BaseEvent):
    """Event fired when samples are ready for a generation request."""
    sample_count: int

class FinalAssetGeneratedEvent(BaseEvent):
    """Event fired when the final asset is successfully generated."""
    asset_url: str

class GenerationFailedEvent(BaseEvent):
    """Event fired when a generation request fails."""
    error_message: str
    is_system_error: bool
    failed_stage: str