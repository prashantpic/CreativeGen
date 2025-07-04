# -*- coding: utf-8 -*-
"""
SQLAlchemy implementation of the IQuotaRepository interface.
Provides concrete data access methods for Quota entities.
Note: This repository manages the Quota *configuration*. Calculating current
usage is done via the UsageRepository.
"""
import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.usage import Quota
from domain.repositories.quota_repository import IQuotaRepository
from infrastructure.database.models.quota_model import QuotaModel

logger = logging.getLogger(__name__)


def _to_domain(db_model: QuotaModel) -> Quota:
    """Maps a QuotaModel ORM object to a Quota domain model."""
    return Quota(
        id=db_model.id,
        api_client_id=db_model.api_client_id,
        user_id=db_model.user_id,
        limit_amount=db_model.limit_amount,
        period=db_model.period,
        last_reset_at=db_model.last_reset_at,
    )


def _to_db_model(domain_model: Quota) -> QuotaModel:
    """Maps a Quota domain model to a QuotaModel ORM object."""
    return QuotaModel(
        id=domain_model.id,
        api_client_id=domain_model.api_client_id,
        user_id=domain_model.user_id,
        limit_amount=domain_model.limit_amount,
        period=str(domain_model.period.value),
        last_reset_at=domain_model.last_reset_at,
    )


class SqlAlchemyQuotaRepository(IQuotaRepository):
    """SQLAlchemy implementation for API Quota configuration persistence."""

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an async database session.

        :param db_session: The SQLAlchemy AsyncSession.
        """
        self.db_session = db_session

    async def add(self, quota_domain: Quota) -> None:
        """Adds a new Quota configuration to the database."""
        db_model = _to_db_model(quota_domain)
        try:
            self.db_session.add(db_model)
            await self.db_session.flush()
            logger.info("Added new Quota with ID: %s", quota_domain.id)
        except SQLAlchemyError as e:
            logger.error("Error adding Quota to database: %s", e, exc_info=True)
            await self.db_session.rollback()
            raise

    async def get_by_client_id(self, api_client_id: UUID) -> Optional[Quota]:
        """Retrieves a Quota configuration by the API Client's ID."""
        try:
            stmt = select(QuotaModel).where(QuotaModel.api_client_id == api_client_id)
            result = await self.db_session.execute(stmt)
            db_model = result.scalar_one_or_none()
            return _to_domain(db_model) if db_model else None
        except SQLAlchemyError as e:
            logger.error(
                "Error retrieving Quota by client ID %s: %s",
                api_client_id,
                e,
                exc_info=True,
            )
            raise

    async def update(self, quota_domain: Quota) -> None:
        """Updates an existing Quota configuration in the database."""
        try:
            existing_model = await self.db_session.get(QuotaModel, quota_domain.id)
            if not existing_model:
                logger.warning(
                    "Attempted to update non-existent Quota with ID: %s",
                    quota_domain.id,
                )
                return

            update_data = _to_db_model(quota_domain)
            existing_model.limit_amount = update_data.limit_amount
            existing_model.period = update_data.period
            existing_model.last_reset_at = update_data.last_reset_at

            await self.db_session.flush()
            logger.info("Updated Quota with ID: %s", quota_domain.id)
        except SQLAlchemyError as e:
            logger.error(
                "Error updating Quota with ID %s: %s",
                quota_domain.id,
                e,
                exc_info=True,
            )
            await self.db_session.rollback()
            raise