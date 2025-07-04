```python
import uuid
from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class APIKeyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="A user-defined name for the API key.")
    permissions: Optional[Dict[str, bool]] = Field(None, description="Granular permissions for the key.")


class APIKeyCreateSchema(APIKeyBase):
    pass


class APIKeyUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="A new user-defined name for the API key.")
    permissions: Optional[Dict[str, bool]] = Field(None, description="Updated granular permissions for the key.")
    is_active: Optional[bool] = Field(None, description="Set to false to deactivate the key.")


class APIKeyResponseSchema(APIKeyBase):
    id: uuid.UUID = Field(..., description="The unique identifier for the API key.")
    key_prefix: str = Field(..., description="The non-secret prefix of the API key, used for identification.")
    is_active: bool = Field(..., description="Whether the API key is currently active.")
    created_at: datetime = Field(..., description="The timestamp when the API key was created.")
    revoked_at: Optional[datetime] = Field(None, description="The timestamp when the API key was revoked, if applicable.")
    
    class Config:
        from_attributes = True


class APIKeyCreateResponseSchema(APIKeyResponseSchema):
    api_key: str = Field(..., description="The full API key, including the secret. This is only shown once upon creation.")
```