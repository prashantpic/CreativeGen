"""
Pydantic schemas for API key related requests and responses.
"""
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class APIKeyBase(BaseModel):
    """Base schema for an API Key, containing common fields."""
    name: str = Field(..., min_length=3, max_length=100, description="A user-defined name for the API key.")
    permissions: Optional[Dict[str, bool]] = Field(None, description="Granular permissions for the key, e.g., {'can_generate': true}.")


class APIKeyCreateSchema(APIKeyBase):
    """Schema for creating a new API Key."""
    pass


class APIKeyUpdateSchema(BaseModel):
    """Schema for updating an existing API Key."""
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="A new user-defined name for the API key.")
    permissions: Optional[Dict[str, bool]] = Field(None, description="Updated granular permissions for the key.")
    is_active: Optional[bool] = Field(None, description="Set to false to deactivate the key.")


class APIKeyResponseSchema(APIKeyBase):
    """Schema for representing an API Key in API responses (secret excluded)."""
    id: UUID = Field(..., description="The unique identifier for the API key.")
    key_prefix: str = Field(..., description="The non-secret prefix of the API key, used for identification.")
    is_active: bool = Field(..., description="Indicates if the API key is currently active.")
    created_at: datetime = Field(..., description="The timestamp when the API key was created.")
    revoked_at: Optional[datetime] = Field(None, description="The timestamp when the API key was revoked, if applicable.")
    
    class Config:
        from_attributes = True


class APIKeyCreateResponseSchema(APIKeyResponseSchema):
    """
    Schema for the response after creating an API Key.
    Includes the full plaintext API key, which should only be shown once.
    """
    api_key: str = Field(..., description="The full, un-hashed API key. This is the only time the secret part is revealed.")