from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException

from api.dependencies.authentication import get_current_active_api_client
from api.dependencies.common import get_usage_tracking_service, get_quota_management_service
from api.schemas.usage_schemas import UsageSummaryResponseSchema, QuotaStatusResponseSchema
from application.services.usage_tracking_service import UsageTrackingService
from application.services.quota_management_service import QuotaManagementService
from domain.models.api_key import APIKey as APIKeyDomainModel

# API usage queries are authenticated via the API Key itself.
router = APIRouter(
    prefix="/usage",
    tags=["API Usage"],
    dependencies=[Depends(get_current_active_api_client)],
)


@router.get(
    "/summary",
    response_model=UsageSummaryResponseSchema,
    summary="Get API Usage Summary",
    description="Retrieves a summary of API calls made with the provided API key within a specified date range."
)
async def get_api_usage_summary(
    start_date: date = Query(..., description="The start date for the usage summary (YYYY-MM-DD)."),
    end_date: date = Query(..., description="The end date for the usage summary (YYYY-MM-DD)."),
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    usage_service: UsageTrackingService = Depends(get_usage_tracking_service),
) -> UsageSummaryResponseSchema:
    """
    Provides a summary of API usage for the authenticated API client.
    """
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")

    summary_dto = await usage_service.get_usage_summary(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
        start_date=start_date,
        end_date=end_date,
    )
    return UsageSummaryResponseSchema.model_validate(summary_dto)


@router.get(
    "/quota",
    response_model=QuotaStatusResponseSchema,
    summary="Get Current Quota Status",
    description="Retrieves the current quota status (e.g., monthly generation limits) for the account associated with the API key."
)
async def get_current_quota_status(
    api_client: APIKeyDomainModel = Depends(get_current_active_api_client),
    quota_service: QuotaManagementService = Depends(get_quota_management_service),
) -> QuotaStatusResponseSchema:
    """
    Provides the current quota status for the authenticated API client.
    """
    quota_status_dto = await quota_service.get_quota_status(
        api_client_id=api_client.id,
        user_id=api_client.user_id,
    )
    if not quota_status_dto:
         raise HTTPException(status_code=404, detail="No active quota found for this client.")
         
    return QuotaStatusResponseSchema.model_validate(quota_status_dto)