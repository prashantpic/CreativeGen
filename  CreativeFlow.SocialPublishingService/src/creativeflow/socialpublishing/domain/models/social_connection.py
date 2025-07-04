"""
Domain entity representing a user's connection to a social media platform.
"""
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SocialConnection(BaseModel):
    """
    Represents a user's authenticated connection to a social media platform,
    holding encrypted tokens and metadata.
    """
    id: UUID
    user_id: str
    platform: str
    external_user_id: str
    external_display_name: Optional[str] = None
    access_token_encrypted: bytes
    refresh_token_encrypted: Optional[bytes] = None
    expires_at: Optional[datetime] = None
    scopes: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    def is_token_expired(self) -> bool:
        """
        Checks if the access token has expired.

        Returns:
            True if the token has an expiration date and it's in the past,
            False otherwise.
        """
        if self.expires_at:
            return datetime.now(timezone.utc) >= self.expires_at
        return False

    def update_tokens(
        self,
        new_access_token_encrypted: bytes,
        new_expires_at: datetime,
        new_refresh_token_encrypted: Optional[bytes] = None,
    ) -> None:
        """
        Updates the connection with new tokens and expiry information.

        Args:
            new_access_token_encrypted: The new encrypted access token.
            new_expires_at: The new expiration datetime for the access token.
            new_refresh_token_encrypted: The new encrypted refresh token, if any.
        """
        self.access_token_encrypted = new_access_token_encrypted
        self.expires_at = new_expires_at
        if new_refresh_token_encrypted:
            self.refresh_token_encrypted = new_refresh_token_encrypted
        self.updated_at = datetime.now(timezone.utc)

    class Config:
        from_attributes = True