```python
import logging
import uuid

from fastapi import APIRouter, Depends, Request

from api.dependencies.authentication import get_current_active_api_client
from api.dependencies.common import (
    get_asset_proxy_service,
    get_rate_limiting_service,
    get_usage_tracking_service,
)
from api.schemas.asset_schemas import AssetDetailResponseSchema
from application.services.asset_proxy_service import AssetProxyService
from application.services.rate_limiting_service import RateLimitingService
from application.services.usage_tracking_service import UsageTrackingService
from core.exceptions import RateLimitExceededError
from domain.models.api_key import APIKey as APIKeyDomainModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/proxy/v1/assets",
    tags=["Platform API Proxy"],
    dependencies=[Depends(get_current_active_api_client)],
)


@router.get("/{asset_id}", response_model=AssetDetailResponseSchema)
async def retrieve_asset_details_proxy(
    request: Request,
    asset_id: uuid.UUID,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: AssetProxyService = Depends(get_asset_proxy_service),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
    rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service),
) -> AssetDetailResponseSchema:
    """
    Proxies a request to retrieve details for a specific asset.
    """
    endpoint_key = "proxy_retrieve_asset_details"
    logger.info(f"Client {api_client.id} requesting details for asset {asset_id}")

    # 1. Check Rate Limiting
    if await rate_limit_service.is_rate_limited(api_client.id, endpoint_key):
        logger.warning(f"Client {api_client.id} rate limited for endpoint: {endpoint_key}")
        raise RateLimitExceededError()

    # 2. Proxy the request
    proxied_response = await proxy_service.proxy_retrieve_asset_details(
        api_client=api_client, asset_id=asset_id
    )

    # 3. Record Usage
    await usage_service.record_api_call(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
        endpoint=str(request.url.path),
        is_successful=True,
        cost=0,  # Assuming GET requests are free
    )

    return AssetDetailResponseSchema.model_validate(proxied_response)

# Add other asset management proxy endpoints here (e.g., list, upload, delete)
# following the same pattern of rate limiting, proxying, and usage tracking.
```