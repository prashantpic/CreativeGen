from pydantic import BaseModel, Field
from typing import Optional

class AssetInfo(BaseModel):
    """
    Value Object representing information about a generated asset.
    It is immutable by convention.
    """
    asset_id: str = Field(..., description="A unique identifier for the asset, e.g., a MinIO path or internal ID.")
    url: str = Field(..., description="A publicly accessible URL to view or download the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '512x512'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        frozen = True # Makes the model immutable