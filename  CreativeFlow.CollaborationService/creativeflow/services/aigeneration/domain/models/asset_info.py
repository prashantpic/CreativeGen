from typing import Optional
from pydantic import BaseModel, Field

class AssetInfo(BaseModel):
    """
    Value Object representing information about a generated asset.
    It's a Pydantic model for data validation and structure, used within the domain.
    """
    asset_id: str = Field(..., description="A unique identifier for the asset, e.g., a MinIO path or internal ID.")
    url: str = Field(..., description="A publicly accessible URL to view the asset.")
    resolution: Optional[str] = Field(None, description="The resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="The file format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        frozen = True  # Makes the model immutable, suitable for a Value Object