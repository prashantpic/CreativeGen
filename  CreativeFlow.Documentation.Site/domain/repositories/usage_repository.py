```python
import uuid
from datetime import date
from typing import Dict, Any, Protocol

from domain.models.usage import APIUsageRecord


class IUsageRepository(Protocol):
    """
    Interface for API Usage Record data persistence operations.
    """

    async def add_record(self, usage_record: APIUsageRecord) -> None:
        """Saves a new API usage record."""
        ...

    async def get_summary_for_client(
        self, api_client_id: uuid.UUID, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """
        Retrieves and aggregates usage data for a client within a date range.
        The implementation should return a dictionary that can be used to
        populate a UsageSummary DTO.
        """
        ...

    async def get_count_for_period(
        self, api_client_id: uuid.UUID, period_start: date, action_type: str
    ) -> int:
        """
        Counts the number of specific actions (e.g., 'generation') for a client
        since the start of their current quota period.
        """
        ...
```