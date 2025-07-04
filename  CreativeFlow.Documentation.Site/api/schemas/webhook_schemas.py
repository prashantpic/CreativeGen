```python
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class WebhookBase(BaseModel):
    target_url: HttpUrl = Field(..., description="The URL where webhook payloads will be sent.")
    event_types: List[str] = Field(..., min_length=1, description="A list of event types this webhook subscribes to.")


class WebhookCreateSchema(WebhookBase):
    secret: Optional[str] = Field(None, min_length=8, description="An optional secret used to sign webhook payloads for verification.")


class WebhookUpdateSchema(BaseModel):
    target_url: Optional[HttpUrl] = Field(None, description="A new URL for the webhook endpoint.")
    event_types: Optional[List[str]] = Field(None, min_length=1, description="An updated list of subscribed event types.")
    secret: Optional[str] = Field(None, min_length=8, description="A new secret for signing payloads. Providing a new secret will replace the old one.")
    is_active: Optional[bool] = Field(None, description="Set to false to disable this webhook temporarily.")


class WebhookResponseSchema(BaseModel):
    id: uuid.UUID = Field(..., description="The unique identifier for the webhook.")
    user_id: uuid.UUID = Field(..., description="The ID of the user who owns this webhook.")
    target_url: HttpUrl = Field(..., description="The URL where webhook payloads are sent.")
    event_types: List[str] = Field(..., description="The list of event types this webhook is subscribed to.")
    is_active: bool = Field(..., description="Whether the webhook is currently active.")
    created_at: datetime = Field(..., description="The timestamp when the webhook was created.")
    
    class Config:
        from_attributes = True
```