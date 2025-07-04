from pydantic import BaseModel, Field
from typing import Optional

class AssetInfo(BaseModel):
    """
    Value Object representing information about a single generated asset.
    This can be a sample or a final asset.
    """
    asset_id: str = Field(..., description="A unique reference to the asset, e.g., a MinIO path or an internal ID.")
    url: str = Field(..., description="A publicly accessible URL to view the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '512x512'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        frozen = True # Value objects should be immutable