```python
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class APIKeyPermissions(BaseModel):
    """Value object for granular API key permissions."""
    can_generate_creative: bool = Field(True)
    can_read_assets: bool = Field(True)
    can_manage_assets: bool = Field(False)
    can_read_user_info: bool = Field(True)
    can_manage_teams: bool = Field(False)


class APIKey(BaseModel):
    """Domain model for an API Key aggregate root."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    name: str
    key_prefix: str
    secret_hash: str
    permissions: APIKeyPermissions = Field(default_factory=APIKeyPermissions)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked_at: Optional[datetime] = None

    def revoke(self):
        """Revokes the API key."""
        if self.is_active:
            self.is_active = False
            self.revoked_at = datetime.utcnow()
    
    class Config:
        from_attributes = True

```