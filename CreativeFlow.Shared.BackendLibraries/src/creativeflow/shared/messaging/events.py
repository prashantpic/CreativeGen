"""
Contains Pydantic models that define the schemas for events published to and
consumed from RabbitMQ. This establishes a strict, versioned contract for all
asynchronous communication between microservices.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, UUID4


class BaseEvent(BaseModel):
    """Base model for all domain events."""
    event_id: UUID4 = Field(default_factory=uuid.uuid4)
    event_type: str
    correlation_id: UUID4 = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: BaseModel  # Enforce typed payloads


# =============================================================================
# User Domain Events
# =============================================================================

class UserRegisteredPayload(BaseModel):
    """Payload for the UserRegisteredEvent."""
    user_id: UUID4
    email: EmailStr
    verification_token: str


class UserRegisteredEvent(BaseEvent):
    """Event published when a new user completes the registration form."""
    event_type: Literal["user.registered"] = "user.registered"
    payload: UserRegisteredPayload


# =============================================================================
# AI Generation Domain Events
# =============================================================================

class AIGenerationJobRequestedPayload(BaseModel):
    """Payload for the event when an AI generation job is requested."""
    generation_id: UUID4
    user_id: UUID4
    project_id: UUID4
    input_prompt: str
    style_guidance: Optional[str] = None
    input_parameters: Optional[Dict[str, Any]] = None


class AIGenerationJobRequestedEvent(BaseEvent):
    """Event published to trigger an AI generation workflow."""
    event_type: Literal["ai.generation.requested"] = "ai.generation.requested"
    payload: AIGenerationJobRequestedPayload


class GenerationCompletedPayload(BaseModel):
    """Payload for the GenerationCompletedEvent."""
    generation_id: UUID4
    user_id: UUID4
    status: Literal["Completed", "Failed", "ContentRejected"]
    final_asset_id: Optional[UUID4] = None
    error_message: Optional[str] = None


class GenerationCompletedEvent(BaseEvent):
    """Event published when a generation job finishes (successfully or not)."""
    event_type: Literal["generation.completed"] = "generation.completed"
    payload: GenerationCompletedPayload

# =============================================================================
# Billing Domain Events
# =============================================================================

class SubscriptionTierChangedPayload(BaseModel):
    """Payload for the event when a user's subscription changes."""
    user_id: UUID4
    old_tier: str
    new_tier: str
    change_date: datetime

class SubscriptionTierChangedEvent(BaseEvent):
    """Event published when a user's subscription tier is upgraded or downgraded."""
    event_type: Literal["subscription.tier.changed"] = "subscription.tier.changed"
    payload: SubscriptionTierChangedPayload