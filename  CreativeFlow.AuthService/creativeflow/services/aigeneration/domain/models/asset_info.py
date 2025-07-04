from typing import Optional
from pydantic import BaseModel, Field

class AssetInfo(BaseModel):
    """
    A value object representing information about a generated asset.
    This can be used for both sample and final assets.
    """
    asset_id: str = Field(..., description="A unique identifier for the asset, e.g., its path in MinIO.")
    url: str = Field(..., description="A publicly accessible URL to view the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '512x512'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        frozen = True # Value objects should be immutable