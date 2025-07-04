```python
import uuid
from typing import Any, Dict

from .base_client import BaseExternalClient


class AssetManagementClient(BaseExternalClient):
    """
    HTTP client for interacting with the Asset Management Service.
    """
    _service_name = "AssetManagementService"

    async def get_asset_details(self, asset_id: uuid.UUID) -> Dict[str, Any]:
        """
        Calls the downstream service to retrieve details of a specific asset.
        """
        return await self._request("GET", f"/assets/{asset_id}")

    # Add other methods like list_assets, upload_asset, etc. as needed.


# Singleton instance
asset_management_client = AssetManagementClient()
```