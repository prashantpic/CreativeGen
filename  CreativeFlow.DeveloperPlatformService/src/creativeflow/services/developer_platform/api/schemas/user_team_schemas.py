"""
Pydantic schemas for proxying user and team management requests and responses.
These are placeholders and should be defined based on the actual capabilities
exposed by the downstream User/Team Management service.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class UserDetailResponseSchema(BaseModel):
    """
    Placeholder schema for proxied user detail responses.
    Exposes a limited, safe subset of user information.
    """
    id: UUID = Field(..., description="The user's unique identifier.")
    username: Optional[str] = Field(None, description="The user's public username.")
    full_name: Optional[str] = Field(None, description="The user's full name.")
    profile_picture_url: Optional[str] = Field(None, description="URL for the user's profile picture.")

    class Config:
        from_attributes = True


class TeamMemberSchema(BaseModel):
    """Placeholder schema for a member within a team."""
    user: UserDetailResponseSchema
    role: str = Field(..., description="The user's role in the team (e.g., 'Owner', 'Admin', 'Member').")
    joined_at: datetime


class TeamListResponseSchema(BaseModel):
    """Placeholder schema for a list of teams a user belongs to."""
    id: UUID = Field(..., description="The team's unique identifier.")
    name: str = Field(..., description="The name of the team.")
    member_count: int = Field(..., description="The number of members in the team.")
    created_at: datetime = Field(..., description="The timestamp when the team was created.")

    class Config:
        from_attributes = True