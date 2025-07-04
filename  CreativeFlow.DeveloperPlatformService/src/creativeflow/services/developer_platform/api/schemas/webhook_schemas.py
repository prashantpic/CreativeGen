"""
Pydantic schemas for webhook related requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class WebhookBase(BaseModel):
    """Base schema for a webhook, containing common fields."""
    target_url: HttpUrl = Field(..., description="The URL where webhook payloads will be sent.")
    event_types: List[str] = Field(..., min_length=1, description="A list of event types to subscribe to, e.g., ['generation.completed'].")


class WebhookCreateSchema(WebhookBase):
    """Schema for registering a new webhook."""
    secret: Optional[str] = Field(None, min_length=16, max_length=256, description="An optional secret used to sign webhook payloads with HMAC-SHA256 for verification.")


class WebhookUpdateSchema(BaseModel):
    """Schema for updating an existing webhook."""
    target_url: Optional[HttpUrl] = Field(None, description="A new target URL for the webhook.")
    event_types: Optional[List[str]] = Field(None, min_length=1, description="An updated list of event types to subscribe to.")
    secret: Optional[str] = Field(None, min_length=16, max_length=256, description="A new secret for signing payloads. Providing a new secret will replace the old one.")
    is_active: Optional[bool] = Field(None, description="Set to false to deactivate the webhook without deleting it.")


class WebhookResponseSchema(WebhookBase):
    """Schema for representing a webhook in API responses."""
    id: UUID = Field(..., description="The unique identifier for the webhook.")
    user_id: UUID = Field(..., description="The ID of the user who owns this webhook.")
    is_active: bool = Field(..., description="Indicates if the webhook is currently active.")
    created_at: datetime = Field(..., description="The timestamp when the webhook was created.")
    
    class Config:
        from_attributes = True