"""
Domain model for the APIKey aggregate root and related value objects.
It represents the core business entity for an API Key.
"""
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class APIKeyPermissions(BaseModel):
    """
    Value Object representing the permissions/scopes assigned to an API Key.
    """
    can_generate_creative: bool = Field(True, description="Allows initiating creative generation.")
    can_read_assets: bool = Field(True, description="Allows retrieving asset details and lists.")
    can_manage_assets: bool = Field(False, description="Allows uploading or modifying assets.")
    can_read_user_info: bool = Field(False, description="Allows retrieving user/team information.")
    
    class Config:
        frozen = True # Permissions should be treated as an immutable value object


class APIKey(BaseModel):
    """
    Aggregate Root for an API Key. Encapsulates all properties and business
    rules related to an API key's lifecycle.
    """
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    name: str
    key_prefix: str = Field(..., description="The non-secret prefix of the API key, used for lookups.")
    secret_hash: str = Field(..., description="The bcrypt-hashed secret part of the API key.")
    permissions: APIKeyPermissions = Field(default_factory=APIKeyPermissions)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def revoke(self) -> None:
        """
        Marks the API key as inactive and records the revocation time.
        This is an idempotent operation.
        """
        if self.is_active:
            self.is_active = False
            self.revoked_at = datetime.utcnow()

    def update_permissions(self, new_permissions: APIKeyPermissions) -> None:
        """
        Updates the permissions for this API key.
        """
        self.permissions = new_permissions

    def update_name(self, new_name: str) -> None:
        """
        Updates the name for this API key.
        """
        self.name = new_name