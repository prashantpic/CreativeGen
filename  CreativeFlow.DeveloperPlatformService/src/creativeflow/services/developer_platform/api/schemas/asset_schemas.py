"""
Pydantic schemas for proxying asset management requests and responses,
mirroring the structure of the downstream Asset Management service.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class AssetDetailResponseSchema(BaseModel):
    """Schema for responding with details of a specific asset."""
    asset_id: UUID = Field(..., description="The unique identifier for the asset.")
    name: str = Field(..., description="The name of the asset file.")
    type: str = Field(..., description="The type of asset (e.g., 'AIGenerated', 'Uploaded').")
    mime_type: str = Field(..., description="The MIME type of the asset (e.g., 'image/png').")
    download_url: HttpUrl = Field(..., description="A temporary, secure URL to download the asset.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata associated with the asset.")
    created_at: datetime = Field(..., description="The timestamp when the asset was created.")

    class Config:
        from_attributes = True

# Placeholder for future Asset Upload Schema
# class AssetUploadSchema(BaseModel):
#     ...

# Placeholder for future Asset Update Schema
# class AssetUpdateSchema(BaseModel):
#     name: Optional[str] = None
#     metadata: Optional[Dict[str, Any]] = None