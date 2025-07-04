"""
Pydantic schemas for social media connection API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SocialConnectionResponse(BaseModel):
    """Response schema for a social media connection."""
    id: UUID
    user_id: str
    platform: str
    external_user_id: str
    external_display_name: Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    scopes: Optional[List[str]] = None

    class Config:
        from_attributes = True


class OAuthCallbackQuery(BaseModel):
    """Schema for query parameters in the OAuth callback."""
    code: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None


class InitiateOAuthResponse(BaseModel):
    """Response schema for initiating an OAuth flow."""
    authorization_url: str