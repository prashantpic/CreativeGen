```python
import logging
from datetime import date

from fastapi import APIRouter, Depends, Query

from api.dependencies.authentication import get_current_active_api_client
from api.dependencies.common import (
    get_quota_management_service,
    get_usage_tracking_service,
)
from api.schemas.usage_schemas import (
    QuotaStatusResponseSchema,
    UsageSummaryResponseSchema,
)
from application.services.quota_management_service import QuotaManagementService
from application.services.usage_tracking_service import UsageTrackingService
from domain.models.api_key import APIKey as APIKeyDomainModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/usage",
    tags=["API Usage"],
    dependencies=[Depends(get_current_active_api_client)],
)


@router.get(
    "/summary",
    response_model=UsageSummaryResponseSchema,
    summary="Get API Usage Summary",
)
async def get_api_usage_summary(
    start_date: date = Query(..., description="Start date for the usage summary (YYYY-MM-DD)."),
    end_date: date = Query(..., description="End date for the usage summary (YYYY-MM-DD)."),
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
) -> UsageSummaryResponseSchema:
    """
    Retrieves a summary of API usage for the authenticated API key within a specified date range.
    """
    logger.info(
        f"API client {api_client.id} requesting usage summary from {start_date} to {end_date}"
    )
    summary = await usage_service.get_usage_summary(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
        start_date=start_date,
        end_date=end_date,
    )
    return UsageSummaryResponseSchema.model_validate(summary)


@router.get(
    "/quota",
    response_model=QuotaStatusResponseSchema,
    summary="Get Current Quota Status",
)
async def get_current_quota_status(
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    quota_service: QuotaManagementService = Depends(get_quota_management_service),
) -> QuotaStatusResponseSchema:
    """
    Retrieves the current quota status for the authenticated API key,
    including limits, remaining calls, and reset date.
    """
    logger.info(f"API client {api_client.id} requesting quota status.")
    status = await quota_service.get_quota_status(
        api_client_id=api_client.id, user_id=api_client.user_id
    )
    return QuotaStatusResponseSchema.model_validate(status)
```