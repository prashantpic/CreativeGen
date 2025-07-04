from uuid import UUID
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base class for all domain events."""
    request_id: UUID = Field(..., description="The unique ID of the generation request associated with the event.")
    user_id: str = Field(..., description="The ID of the user associated with the event.")


class GenerationRequestInitiatedEvent(BaseEvent):
    """
    Event published when a new generation request is successfully initiated and validated.
    """
    pass


class SampleGenerationCompletedEvent(BaseEvent):
    """
    Event published when the sample generation stage is successfully completed.
    """
    sample_count: int = Field(..., description="The number of samples generated.")


class FinalAssetGeneratedEvent(BaseEvent):
    """
    Event published when the final asset is successfully generated.
    """
    asset_url: str = Field(..., description="The URL of the final generated asset.")


class GenerationFailedEvent(BaseEvent):
    """
    Event published when the generation process fails at any stage.
    """
    error_message: str = Field(..., description="A summary of the error that occurred.")
    is_system_error: bool = Field(..., description="Flag indicating if the failure was due to a system error (eligible for refund).")
    failed_stage: str = Field(..., description="The stage at which the process failed (e.g., 'sample_processing', 'final_processing').")

# Note: These events are conceptual for now. Actual implementation might involve
# publishing these to a dedicated event bus (e.g., a different RabbitMQ topic)
# if a more event-driven internal architecture is adopted. For the current scope,
# the OrchestrationService may handle these logical flows by directly calling
# other services like the NotificationServiceClient.