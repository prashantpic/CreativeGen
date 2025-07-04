```python
import uuid
from typing import Any, Dict

from core.exceptions import ExternalServiceError
from domain.models.api_key import APIKey
from infrastructure.external_clients.asset_management_client import AssetManagementClient


class AssetProxyService:
    """
    Service to proxy requests to the internal Asset Management Service.
    """

    def __init__(self, asset_mgmt_client: AssetManagementClient):
        self.asset_mgmt_client = asset_mgmt_client

    async def proxy_retrieve_asset_details(
        self, api_client: APIKey, asset_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Forwards the request to get asset details to the Asset Management service.
        """
        try:
            # Downstream service is responsible for checking if the user
            # associated with the API key can access this asset.
            response_data = await self.asset_mgmt_client.get_asset_details(
                asset_id=asset_id
            )
            return response_data
        except ExternalServiceError as e:
            raise e
```