from pydantic import BaseModel
from uuid import UUID
from typing import Optional

"""
This file defines conceptual domain events that could be used in a more
advanced event-driven architecture.

These models represent significant state changes in the domain. In a full
implementation, the OrchestrationService might publish these events to a
message bus (like RabbitMQ, but on different topics/exchanges) for other
microservices to consume, further decoupling the system.

For the current scope, they serve as a definition of key business moments.
"""

class BaseEvent(BaseModel):
    request_id: UUID
    user_id: str

class GenerationRequestInitiatedEvent(BaseEvent):
    """Event fired when a new generation request is successfully created and queued."""
    project_id: str
    
class SampleGenerationCompletedEvent(BaseEvent):
    """Event fired when samples are ready for user selection."""
    sample_count: int

class FinalAssetGeneratedEvent(BaseEvent):
    """Event fired when the final asset has been successfully generated."""
    asset_url: str
    final_asset_id: str

class GenerationFailedEvent(BaseEvent):
    """Event fired when a generation process fails for any reason."""
    error_message: str
    is_system_error: bool
    failed_stage: Optional[str]