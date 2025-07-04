from typing import Optional
from pydantic import BaseModel, HttpUrl

class AssetInfo(BaseModel):
    """
    A Value Object representing information about a generated asset.
    It's treated as immutable.
    """
    asset_id: str  # Could be a MinIO path or an internal ID from an asset service
    url: HttpUrl
    resolution: Optional[str]  # e.g., '1024x1024'
    format: str  # e.g., 'png', 'jpg'

    class Config:
        frozen = True # Makes the model immutable