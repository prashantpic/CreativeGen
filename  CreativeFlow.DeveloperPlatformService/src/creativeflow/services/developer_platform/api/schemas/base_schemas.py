"""
Common base Pydantic schemas, e.g., for generic status responses.
"""

from typing import Optional

from pydantic import BaseModel, Field


class StatusResponseSchema(BaseModel):
    """A generic response schema for endpoints that return a status message."""
    status: str = Field("success", description="The status of the operation.")
    message: Optional[str] = Field(None, description="An optional descriptive message.")