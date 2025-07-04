```python
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, HttpUrl


class AssetDetailResponseSchema(BaseModel):
    """
    Schema for the response when retrieving details about an asset.
    This mirrors the output of the Asset Management service.
    """
    asset_id: uuid.UUID
    name: str
    type: str = Field(..., description="Type of asset, e.g., 'AIGenerated', 'Uploaded'.")
    mime_type: str
    download_url: HttpUrl = Field(..., description="A temporary, secure URL to download the asset file.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata associated with the asset.")
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "asset_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                    "name": "Astronaut_on_Mars.jpeg",
                    "type": "AIGenerated",
                    "mime_type": "image/jpeg",
                    "download_url": "https://storage.creativeflow.ai/assets/a1b2c3d4-e5f6-7890-1234-567890abcdef?token=...",
                    "metadata": {
                        "source_prompt": "An astronaut on Mars",
                        "resolution": "1024x1024"
                    },
                    "created_at": "2023-10-27T10:00:00Z"
                }
            ]
        }
    }
```