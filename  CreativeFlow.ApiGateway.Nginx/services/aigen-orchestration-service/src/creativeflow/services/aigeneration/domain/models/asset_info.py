from pydantic import BaseModel, Field
from typing import Optional

class AssetInfo(BaseModel):
    """
    A Value Object representing information about a generated asset.
    It is used within the GenerationRequest domain model.
    """
    asset_id: str = Field(..., description="A unique reference to the asset, e.g., a MinIO path or an internal ID.")
    url: str = Field(..., description="A publicly accessible URL to view the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png'.")

    class Config:
        frozen = True # Value objects should be immutable