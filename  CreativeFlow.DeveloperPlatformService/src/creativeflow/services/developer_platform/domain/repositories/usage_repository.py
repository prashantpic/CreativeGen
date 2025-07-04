from datetime import date
from decimal import Decimal
from typing import List, Optional, Protocol
from uuid import UUID

from ..models.usage import APIUsageRecord
from ...api.schemas.usage_schemas import UsageSummaryDataPoint


class IUsageRepository(Protocol):
    """
    Interface for APIUsageRecord repository defining data access methods.
    This contract is responsible for persisting and retrieving API usage data.
    """

    async def add_record(self, usage_record: APIUsageRecord) -> None:
        """
        Adds a new API usage record to the data store.

        Args:
            usage_record: The APIUsageRecord domain model instance to persist.
        """
        ...

    async def get_summary_for_client(
        self, api_client_id: UUID, start_date: date, end_date: date
    ) -> List[UsageSummaryDataPoint]:
        """
        Retrieves an aggregated summary of API usage for a specific client
        within a given time period, grouped by endpoint.

        Args:
            api_client_id: The UUID of the API client (from the APIKey).
            start_date: The start date of the reporting period.
            end_date: The end date of the reporting period.

        Returns:
            A list of data points summarizing usage per endpoint.
        """
        ...

    async def get_count_for_period(
        self,
        api_client_id: UUID,
        period_start: date,
        period_end: date,
        action_type_prefix: str,
    ) -> int:
        """
        Gets the total count of a specific type of action for a client
        within a time period. Used for quota checking.

        Args:
            api_client_id: The UUID of the API client.
            period_start: The start datetime of the quota period.
            period_end: The end datetime of the quota period.
            action_type_prefix: The prefix of the action to count (e.g., 'proxy/v1/generations').

        Returns:
            The total count of matching actions in the period.
        """
        ...