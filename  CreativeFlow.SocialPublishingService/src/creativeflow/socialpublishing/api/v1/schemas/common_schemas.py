"""
Pydantic schemas for common API responses like status or error messages.
"""
from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Schema for a generic status response."""
    status: str
    message: Optional[str] = None


class ErrorDetail(BaseModel):
    """Schema for a detailed error response."""
    code: str
    detail: str