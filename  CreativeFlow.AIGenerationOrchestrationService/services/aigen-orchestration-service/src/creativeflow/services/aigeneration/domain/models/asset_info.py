from typing import Optional
from pydantic import BaseModel, Field, AnyHttpUrl


class AssetInfo(BaseModel):
    """
    A value object representing information about a generated digital asset.
    It is immutable by nature.
    """
    asset_id: str = Field(
        ...,
        description="Unique identifier for the asset in the asset management system (e.g., MinIO path or internal DB ID)."
    )
    url: AnyHttpUrl = Field(
        ...,
        description="A publicly accessible URL (or a presigned URL) to view or download the asset."
    )
    resolution: Optional[str] = Field(
        None,
        description="The resolution of the asset, e.g., '1024x1024'."
    )
    format: str = Field(
        ...,
        description="The file format of the asset, e.g., 'png', 'jpg'."
    )

    class Config:
        frozen = True  # Makes the model immutable