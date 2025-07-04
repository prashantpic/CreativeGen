import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from ....developer_platform.api.schemas import usage_schemas
from ....developer_platform.domain.models.usage import APIUsageRecord
from ....developer_platform.domain.repositories.usage_repository import IUsageRepository


class UsageTrackingService:
    """
    Handles business logic for recording API calls and generating usage summaries.
    """

    def __init__(self, usage_repo: IUsageRepository):
        """
        Initializes the UsageTrackingService.

        Args:
            usage_repo: The repository for persisting and querying usage data.
        """
        self.usage_repo = usage_repo

    async def record_api_call(
        self,
        api_client_id: uuid.UUID,
        user_id: uuid.UUID,
        endpoint: str,
        is_successful: bool,
        cost: Optional[Decimal] = None,
    ) -> None:
        """
        Creates and persists a record of an API call.

        Args:
            api_client_id: The ID of the API key used for the call.
            user_id: The ID of the user associated with the API key.
            endpoint: A key identifying the API endpoint that was called.
            is_successful: A boolean indicating if the call was successful.
            cost: The cost associated with the call, if applicable.
        """
        usage_record = APIUsageRecord(
            api_client_id=api_client_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            endpoint=endpoint,
            cost=cost,
            is_successful=is_successful,
        )
        await self.usage_repo.add_record(usage_record)

    async def get_usage_summary(
        self, api_client_id: uuid.UUID, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> usage_schemas.UsageSummaryResponseSchema:
        """
        Generates a usage summary for a given API client within a date range.

        Args:
            api_client_id: The ID of the API client.
            user_id: The ID of the user owning the client.
            start_date: The start date of the reporting period.
            end_date: The end date of the reporting period.

        Returns:
            A DTO containing the usage summary.
        """
        summary_data = await self.usage_repo.get_summary_for_client(
            api_client_id, start_date, end_date
        )

        total_calls = 0
        total_cost = Decimal("0.0")

        for item in summary_data:
            total_calls += item.call_count
            if item.cost:
                total_cost += item.cost

        return usage_schemas.UsageSummaryResponseSchema(
            api_client_id=api_client_id,
            user_id=user_id,
            period_start=start_date,
            period_end=end_date,
            total_calls=total_calls,
            total_cost=total_cost,
            detailed_usage=summary_data,
        )