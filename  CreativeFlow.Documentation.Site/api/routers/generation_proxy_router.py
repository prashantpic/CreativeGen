```python
import logging
import uuid

from fastapi import APIRouter, Depends, Request

from api.dependencies.authentication import get_current_active_api_client
from api.dependencies.common import (
    get_generation_proxy_service,
    get_quota_management_service,
    get_rate_limiting_service,
    get_usage_tracking_service,
)
from api.schemas.generation_schemas import (
    GenerationCreateRequestSchema,
    GenerationStatusResponseSchema,
)
from application.services.generation_proxy_service import GenerationProxyService
from application.services.quota_management_service import QuotaManagementService
from application.services.rate_limiting_service import RateLimitingService
from application.services.usage_tracking_service import UsageTrackingService
from core.exceptions import InsufficientQuotaError, RateLimitExceededError
from domain.models.api_key import APIKey as APIKeyDomainModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/proxy/v1/generations",
    tags=["Platform API Proxy"],
    dependencies=[Depends(get_current_active_api_client)],
)


@router.post("/", response_model=GenerationStatusResponseSchema, status_code=202)
async def initiate_creative_generation_proxy(
    request: Request,
    payload: GenerationCreateRequestSchema,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
    quota_service: QuotaManagementService = Depends(get_quota_management_service),
    rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service),
) -> GenerationStatusResponseSchema:
    """
    Proxies a request to initiate a new creative generation task.

    This endpoint first checks for rate limits and quotas before forwarding the
    request to the AI Generation service. Usage is recorded upon a successful proxy.
    """
    endpoint_key = "proxy_initiate_generation"
    logger.info(
        f"Client {api_client.id} attempting to initiate generation with prompt: '{payload.prompt[:30]}...'"
    )

    # 1. Check Rate Limiting
    if await rate_limit_service.is_rate_limited(api_client.id, endpoint_key):
        logger.warning(f"Client {api_client.id} rate limited for endpoint: {endpoint_key}")
        raise RateLimitExceededError()

    # 2. Check Quotas
    can_proceed = await quota_service.check_quota(
        api_client_id=api_client.id, user_id=api_client.user_id, action_cost=1
    )
    if not can_proceed:
        logger.warning(f"Client {api_client.id} has insufficient quota.")
        raise InsufficientQuotaError()

    # 3. Proxy the request
    proxied_response = await proxy_service.proxy_initiate_generation(
        api_client=api_client, payload=payload
    )

    # 4. Record Usage
    await usage_service.record_api_call(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
        endpoint=str(request.url.path),
        is_successful=True,
        cost=proxied_response.get("credits_cost_sample"),
    )
    logger.info(f"Client {api_client.id} successfully initiated generation {proxied_response.get('generation_id')}")

    return GenerationStatusResponseSchema.model_validate(proxied_response)


@router.get("/{generation_id}", response_model=GenerationStatusResponseSchema)
async def get_generation_status_proxy(
    request: Request,
    generation_id: uuid.UUID,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
    rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service),
) -> GenerationStatusResponseSchema:
    """
    Proxies a request to get the status of a specific creative generation task.
    """
    endpoint_key = "proxy_get_generation_status"
    logger.info(f"Client {api_client.id} requesting status for generation {generation_id}")

    # 1. Check Rate Limiting (GET requests might have different limits)
    if await rate_limit_service.is_rate_limited(api_client.id, endpoint_key):
        logger.warning(f"Client {api_client.id} rate limited for endpoint: {endpoint_key}")
        raise RateLimitExceededError()

    # 2. Proxy the request
    proxied_response = await proxy_service.proxy_get_generation_status(
        api_client=api_client, generation_id=generation_id
    )

    # 3. Record Usage (GETs might have zero or low cost)
    await usage_service.record_api_call(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
        endpoint=str(request.url.path),
        is_successful=True,
        cost=0,
    )

    return GenerationStatusResponseSchema.model_validate(proxied_response)
```