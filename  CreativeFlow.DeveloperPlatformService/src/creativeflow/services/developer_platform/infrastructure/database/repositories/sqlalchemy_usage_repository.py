# -*- coding: utf-8 -*-
"""
SQLAlchemy implementation of the IUsageRepository interface.
Provides concrete data access methods for APIUsageRecord entities.
"""
import logging
from datetime import date, datetime
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.usage import APIUsageRecord
from domain.repositories.usage_repository import IUsageRepository
from infrastructure.database.models.usage_model import UsageRecordModel

logger = logging.getLogger(__name__)


def _to_domain(db_model: UsageRecordModel) -> APIUsageRecord:
    """Maps a UsageRecordModel ORM object to an APIUsageRecord domain model."""
    return APIUsageRecord(
        id=db_model.id,
        api_client_id=db_model.api_client_id,
        user_id=db_model.user_id,
        timestamp=db_model.timestamp,
        endpoint=db_model.endpoint,
        cost=db_model.cost,
        is_successful=db_model.is_successful,
    )


def _to_db_model(domain_model: APIUsageRecord) -> UsageRecordModel:
    """Maps an APIUsageRecord domain model to a UsageRecordModel ORM object."""
    return UsageRecordModel(
        id=domain_model.id,
        api_client_id=domain_model.api_client_id,
        user_id=domain_model.user_id,
        timestamp=domain_model.timestamp,
        endpoint=domain_model.endpoint,
        cost=domain_model.cost,
        is_successful=domain_model.is_successful,
    )


class SqlAlchemyUsageRepository(IUsageRepository):
    """SQLAlchemy implementation for API usage record persistence."""

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an async database session.

        :param db_session: The SQLAlchemy AsyncSession.
        """
        self.db_session = db_session

    async def add_record(self, usage_record_domain: APIUsageRecord) -> None:
        """Adds a new API usage record to the database."""
        db_model = _to_db_model(usage_record_domain)
        try:
            self.db_session.add(db_model)
            await self.db_session.flush()
        except SQLAlchemyError as e:
            logger.error(
                "Error adding API usage record to database: %s", e, exc_info=True
            )
            await self.db_session.rollback()
            raise

    async def get_summary_for_client(
        self, api_client_id: UUID, start_date: date, end_date: date
    ) -> List[Tuple[str, int]]:
        """
        Retrieves an aggregated summary of API usage for a client within a date range.
        Returns a list of tuples: (endpoint, call_count).
        """
        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())

            stmt = (
                select(
                    UsageRecordModel.endpoint,
                    func.count(UsageRecordModel.id).label("call_count"),
                )
                .where(
                    UsageRecordModel.api_client_id == api_client_id,
                    UsageRecordModel.timestamp >= start_datetime,
                    UsageRecordModel.timestamp <= end_datetime,
                )
                .group_by(UsageRecordModel.endpoint)
                .order_by(func.count(UsageRecordModel.id).desc())
            )
            result = await self.db_session.execute(stmt)
            return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(
                "Error getting usage summary for client %s: %s",
                api_client_id,
                e,
                exc_info=True,
            )
            raise

    async def get_count_for_period(
        self, api_client_id: UUID, period_start: datetime, action_prefix: str
    ) -> int:
        """
        Counts the number of successful API calls for a specific action type
        within a time period (e.g., since the last quota reset).
        """
        try:
            stmt = select(func.count(UsageRecordModel.id)).where(
                and_(
                    UsageRecordModel.api_client_id == api_client_id,
                    UsageRecordModel.timestamp >= period_start,
                    UsageRecordModel.is_successful == True,
                    UsageRecordModel.endpoint.like(f"{action_prefix}%"),
                )
            )
            result = await self.db_session.execute(stmt)
            count = result.scalar_one_or_none()
            return count or 0
        except SQLAlchemyError as e:
            logger.error(
                "Error getting usage count for client %s and action %s: %s",
                api_client_id,
                action_prefix,
                e,
                exc_info=True,
            )
            raise