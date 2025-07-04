```python
import logging
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from domain.models.usage import APIUsageRecord
from domain.repositories.usage_repository import IUsageRepository
from api.schemas.usage_schemas import UsageSummaryResponseSchema, UsageSummaryDataPoint


logger = logging.getLogger(__name__)


class UsageTrackingService:
    """
    Handles the business logic for recording and reporting API usage.
    """

    def __init__(self, usage_repo: IUsageRepository):
        self.usage_repo = usage_repo

    async def record_api_call(
        self,
        api_client_id: uuid.UUID,
        user_id: uuid.UUID,
        endpoint: str,
        is_successful: bool,
        cost: Optional[Decimal] = None,
    ):
        """
        Creates and stores a record of a single API call.
        """
        usage_record = APIUsageRecord(
            api_client_id=api_client_id,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc),
            endpoint=endpoint,
            is_successful=is_successful,
            cost=cost,
        )
        await self.usage_repo.add_record(usage_record)
        logger.debug(f"Recorded API call for client {api_client_id} to endpoint {endpoint}")

    async def get_usage_summary(
        self, api_client_id: uuid.UUID, start_date: date, end_date: date
    ) -> UsageSummaryResponseSchema:
        """
        Generates a usage summary for a given API client and date range.
        """
        summary_data = await self.usage_repo.get_summary_for_client(
            api_client_id=api_client_id, start_date=start_date, end_date=end_date
        )

        total_calls = 0
        total_cost = Decimal("0.0")
        
        detailed_usage = [
            UsageSummaryDataPoint(
                endpoint=row.endpoint,
                call_count=row.call_count,
                cost=row.total_cost
            )
            for row in summary_data
        ]

        for point in detailed_usage:
            total_calls += point.call_count
            if point.cost is not None:
                total_cost += point.cost

        # We need the user_id for the response, let's assume the first record has it
        # In a real app, we might pass it in or look it up separately.
        user_id = summary_data[0].user_id if summary_data else None

        return UsageSummaryResponseSchema(
            api_client_id=api_client_id,
            user_id=user_id,
            period_start=start_date,
            period_end=end_date,
            total_calls=total_calls,
            total_cost=total_cost,
            detailed_usage=detailed_usage,
        )
```