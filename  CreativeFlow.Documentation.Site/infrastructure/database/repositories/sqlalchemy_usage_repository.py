```python
import uuid
from datetime import date, datetime, time
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.usage import APIUsageRecord
from domain.repositories.usage_repository import IUsageRepository, UsageSummaryRow
from infrastructure.database.models.usage_model import UsageRecordModel


class SqlAlchemyUsageRepository(IUsageRepository):
    """SQLAlchemy implementation of the API Usage repository interface."""

    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def add_record(self, usage_record: APIUsageRecord) -> None:
        orm_record = self._to_orm(usage_record)
        self.session.add(orm_record)
        await self.session.flush()

    async def get_summary_for_client(
        self, api_client_id: uuid.UUID, start_date: date, end_date: date
    ) -> List[UsageSummaryRow]:
        """
        Retrieves aggregated usage data for a client within a date range.
        """
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
        
        stmt = (
            select(
                UsageRecordModel.user_id,
                UsageRecordModel.endpoint,
                func.count(UsageRecordModel.id).label("call_count"),
                func.sum(UsageRecordModel.cost).label("total_cost")
            )
            .where(
                UsageRecordModel.api_client_id == api_client_id,
                UsageRecordModel.timestamp.between(start_datetime, end_datetime)
            )
            .group_by(UsageRecordModel.user_id, UsageRecordModel.endpoint)
            .order_by(func.count(UsageRecordModel.id).desc())
        )
        
        result = await self.session.execute(stmt)
        rows = result.mappings().all()
        
        return [UsageSummaryRow(**row) for row in rows]

    async def get_count_for_period(
        self, user_id: uuid.UUID, period_start: datetime
    ) -> int:
        """
        Counts billable actions for a user since the start of the quota period.
        'Billable' is defined here as successful calls to the generation endpoint.
        This could be made more generic if needed.
        """
        stmt = (
            select(func.count(UsageRecordModel.id))
            .where(
                UsageRecordModel.user_id == user_id,
                UsageRecordModel.timestamp >= period_start,
                UsageRecordModel.is_successful == True,
                # This condition makes it specific to generations.
                UsageRecordModel.endpoint.like("/proxy/v1/generations%")
            )
        )
        
        result = await self.session.execute(stmt)
        count = result.scalar_one_or_none()
        return count or 0

    def _to_orm(self, domain_record: APIUsageRecord) -> UsageRecordModel:
        """Converts a domain model instance to an ORM model."""
        return UsageRecordModel(
            id=domain_record.id,
            api_client_id=domain_record.api_client_id,
            user_id=domain_record.user_id,
            timestamp=domain_record.timestamp,
            endpoint=domain_record.endpoint,
            is_successful=domain_record.is_successful,
            cost=domain_record.cost,
        )
```