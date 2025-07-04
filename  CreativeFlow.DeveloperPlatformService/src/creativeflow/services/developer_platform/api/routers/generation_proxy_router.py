from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request

from api.dependencies.authentication import get_current_active_api_client
from api.dependencies.common import (
    get_generation_proxy_service,
    get_usage_tracking_service,
    get_quota_management_service,
    get_rate_limiting_service,
)
from api.schemas.generation_schemas import GenerationCreateRequestSchema, GenerationStatusResponseSchema
from api.schemas.asset_schemas import AssetDetailResponseSchema
from api.schemas.user_team_schemas import UserDetailResponseSchema, TeamDetailResponseSchema
from application.services.generation_proxy_service import GenerationProxyService
from application.services.usage_tracking_service import UsageTrackingService
from application.services.quota_management_service import QuotaManagementService
from application.services.rate_limiting_service import RateLimitingService
from domain.models.api_key import APIKey as APIKeyDomainModel
from core.exceptions import RateLimitExceededError, InsufficientQuotaError, ExternalServiceError, APIKeyPermissionDeniedError

# This router acts as the main gateway for developers using an API key.
router = APIRouter(
    prefix="/proxy/v1",
    tags=["Platform API Proxy"],
    dependencies=[Depends(get_current_active_api_client)],
)


@router.post(
    "/generations",
    response_model=GenerationStatusResponseSchema,
    summary="Initiate Creative Generation",
    description="Proxies a request to the AI Generation service to start a new creative generation task."
)
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
    Handles creative generation requests by:
    1. Checking rate limits and quotas.
    2. Proxying the request to the backend generation service.
    3. Recording the API call for billing and analytics.
    """
    endpoint = f"{request.method} {request.url.path}"

    # 1. Check permissions (future enhancement, placeholder)
    if not api_client.permissions.can_generate_creative:
        raise APIKeyPermissionDeniedError(detail="This API key cannot be used for creative generation.")

    # 2. Check Rate Limiting
    if await rate_limit_service.is_rate_limited(api_client.id, endpoint):
        raise RateLimitExceededError()

    # 3. Check Quotas
    can_proceed = await quota_service.check_quota_available(api_client_id=api_client.id, user_id=api_client.user_id, action_cost=1)
    if not can_proceed:
        raise InsufficientQuotaError()

    is_successful = False
    try:
        # 4. Proxy the request
        response_data = await proxy_service.proxy_initiate_generation(
            api_client=api_client, payload=payload
        )
        is_successful = True
        return GenerationStatusResponseSchema.model_validate(response_data)
    except ExternalServiceError as e:
        # Propagate error from downstream service
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    finally:
        # 5. Record Usage (runs even if proxy call fails, but marks it as unsuccessful)
        await usage_service.record_api_call(
            api_client_id=api_client.id,
            user_id=api_client.user_id,
            endpoint=endpoint,
            is_successful=is_successful,
            cost=1.0 # Example cost, could be dynamic
        )


@router.get(
    "/generations/{generation_id}",
    response_model=GenerationStatusResponseSchema,
    summary="Get Generation Status",
    description="Proxies a request to retrieve the status and results of a specific generation task."
)
async def get_generation_status_proxy(
    request: Request,
    generation_id: UUID,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
    rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service),
) -> GenerationStatusResponseSchema:
    """
    Handles requests for generation status. GET requests are typically cheaper and have higher rate limits.
    """
    endpoint = f"{request.method} {request.url.path}"
    
    if not api_client.permissions.can_read_assets: # Assuming getting status falls under read permissions
        raise APIKeyPermissionDeniedError(detail="This API key cannot be used to query generation status.")

    if await rate_limit_service.is_rate_limited(api_client.id, endpoint):
        raise RateLimitExceededError()

    is_successful = False
    try:
        response_data = await proxy_service.proxy_get_generation_status(
            api_client=api_client, generation_id=generation_id
        )
        is_successful = True
        return GenerationStatusResponseSchema.model_validate(response_data)
    except ExternalServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    finally:
        await usage_service.record_api_call(
            api_client_id=api_client.id,
            user_id=api_client.user_id,
            endpoint=endpoint,
            is_successful=is_successful,
            cost=0.1 # GET requests are cheaper
        )

# --- Asset Proxy Routes (Inferred from SDS) ---

@router.get(
    "/assets/{asset_id}",
    response_model=AssetDetailResponseSchema,
    summary="Retrieve Asset Details",
    description="Proxies a request to the Asset Management service to get details of a specific asset."
)
async def retrieve_asset_details_proxy(
    request: Request,
    asset_id: UUID,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
    rate_limit_service: RateLimitingService = Depends(get_rate_limiting_service),
) -> AssetDetailResponseSchema:
    """
    Handles requests for asset details.
    """
    endpoint = f"{request.method} {request.url.path}"

    if not api_client.permissions.can_read_assets:
        raise APIKeyPermissionDeniedError(detail="This API key cannot be used to retrieve asset details.")

    if await rate_limit_service.is_rate_limited(api_client.id, endpoint):
        raise RateLimitExceededError()

    is_successful = False
    try:
        response_data = await proxy_service.proxy_retrieve_asset_details(
            api_client=api_client, asset_id=asset_id
        )
        is_successful = True
        return AssetDetailResponseSchema.model_validate(response_data)
    except ExternalServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    finally:
        await usage_service.record_api_call(
            api_client_id=api_client.id,
            user_id=api_client.user_id,
            endpoint=endpoint,
            is_successful=is_successful,
            cost=0.1
        )


# --- User/Team Proxy Routes (Inferred Placeholder from SDS) ---

@router.get(
    "/users/{user_id}",
    response_model=UserDetailResponseSchema,
    summary="Retrieve User Details (Scoped)",
    description="Proxies a request to the User/Team service. Access is highly restricted by API key permissions."
)
async def get_user_details_proxy(
    request: Request,
    user_id: UUID,
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    proxy_service: GenerationProxyService = Depends(get_generation_proxy_service),
) -> UserDetailResponseSchema:
    """
    Placeholder for proxying user detail requests.
    This would require extensive permission checks.
    """
    if not api_client.permissions.can_manage_team:
        raise APIKeyPermissionDeniedError(detail="This API key cannot access user information.")
    
    # Rate limiting, usage tracking, etc. would be implemented here as well.
    
    try:
        response_data = await proxy_service.proxy_get_user_details(
            api_client=api_client, user_id=user_id
        )
        return UserDetailResponseSchema.model_validate(response_data)
    except ExternalServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)