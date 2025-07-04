from pydantic import BaseModel, Field
from typing import Optional

class AssetInfo(BaseModel):
    """
    A value object representing information about a generated asset.
    It is immutable.
    """
    asset_id: str = Field(..., description="A unique identifier for the asset, e.g., a MinIO path.")
    url: str = Field(..., description="A publicly accessible URL to view the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png'.")

    class Config:
        frozen = True # Makes the model immutable