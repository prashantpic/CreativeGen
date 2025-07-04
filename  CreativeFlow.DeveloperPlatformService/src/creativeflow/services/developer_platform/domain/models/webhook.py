"""
Domain model for the Webhook entity and related value objects.
"""
import enum
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class WebhookEvent(str, enum.Enum):
    """
    Value Object representing the types of events a webhook can subscribe to.
    """
    GENERATION_COMPLETED = "generation.completed"
    GENERATION_FAILED = "generation.failed"
    ASSET_CREATED = "asset.created"
    # Add other event types as needed
    # e.g., BILLING_ALERT = "billing.alert"


class Webhook(BaseModel):
    """
    Entity representing a webhook subscription. Encapsulates the configuration
    for sending event-driven notifications to an external URL.
    """
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    target_url: HttpUrl
    event_types: List[WebhookEvent]
    hashed_secret: Optional[str] = Field(None, description="A bcrypt-hashed secret used for generating HMAC signatures.")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

    def deactivate(self) -> None:
        """Marks the webhook as inactive."""
        self.is_active = False

    def activate(self) -> None:
        """Marks the webhook as active."""
        self.is_active = True

    # Note on HMAC signature generation:
    # The actual generation of the HMAC signature is a responsibility of the
    # application/infrastructure layer (e.g., a WebhookPublisher or a dedicated
    # worker). The service layer will retrieve the plain secret (if stored
    # securely, e.g., in a vault) or the hashed secret (if the plain secret is
    # not stored) to perform the signing. This domain model only holds the
    # hashed secret for persistence.