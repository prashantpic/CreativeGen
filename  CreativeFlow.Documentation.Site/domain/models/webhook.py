```python
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class WebhookEvent(str, Enum):
    """
    Value Object representing the types of events a webhook can subscribe to.
    """
    GENERATION_COMPLETED = "generation.completed"
    GENERATION_FAILED = "generation.failed"
    ASSET_CREATED = "asset.created"
    # Add more event types as the system grows
    # e.g., BILLING_INVOICE_CREATED = "billing.invoice.created"


class Webhook(BaseModel):
    """
    Domain Model representing a Webhook subscription.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    target_url: HttpUrl
    event_types: List[WebhookEvent]
    hashed_secret: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
        use_enum_values = True # Important for serialization of Enum
```