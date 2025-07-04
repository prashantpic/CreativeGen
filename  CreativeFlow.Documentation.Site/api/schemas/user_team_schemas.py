```python
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserDetailResponseSchema(BaseModel):
    """
    Schema for the response when retrieving user details.
    This is a simplified view from the User/Team Management service.
    """
    id: uuid.UUID
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    subscription_tier: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TeamMemberSchema(BaseModel):
    """Represents a member within a team."""
    user_id: uuid.UUID
    email: EmailStr
    role: str # e.g., 'Owner', 'Admin', 'Editor'


class TeamDetailResponseSchema(BaseModel):
    """
    Schema for the response when retrieving team details.
    This mirrors the output of the User/Team Management service.
    """
    id: uuid.UUID
    name: str
    owner_id: uuid.UUID
    members: List[TeamMemberSchema]
    created_at: datetime
```