# -*- coding: utf-8 -*-
"""
SQLAlchemy implementation of the IWebhookRepository interface.
Provides concrete data access methods for Webhook entities using SQLAlchemy.
"""
import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.database.models.webhook_model import WebhookModel

logger = logging.getLogger(__name__)


def _to_domain(db_model: WebhookModel) -> Webhook:
    """Maps a WebhookModel ORM object to a Webhook domain model."""
    return Webhook(
        id=db_model.id,
        user_id=db_model.user_id,
        target_url=db_model.target_url,
        event_types=[event for event in db_model.event_types],
        hashed_secret=db_model.hashed_secret,
        is_active=db_model.is_active,
        created_at=db_model.created_at,
    )


def _to_db_model(domain_model: Webhook) -> WebhookModel:
    """Maps a Webhook domain model to a WebhookModel ORM object."""
    return WebhookModel(
        id=domain_model.id,
        user_id=domain_model.user_id,
        target_url=str(domain_model.target_url),
        event_types=[str(event.value) for event in domain_model.event_types],
        hashed_secret=domain_model.hashed_secret,
        is_active=domain_model.is_active,
        created_at=domain_model.created_at,
    )


class SqlAlchemyWebhookRepository(IWebhookRepository):
    """SQLAlchemy implementation for Webhook data persistence."""

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an async database session.

        :param db_session: The SQLAlchemy AsyncSession.
        """
        self.db_session = db_session

    async def add(self, webhook_domain: Webhook) -> None:
        """Adds a new Webhook to the database."""
        db_model = _to_db_model(webhook_domain)
        try:
            self.db_session.add(db_model)
            await self.db_session.flush()
            logger.info("Added new Webhook with ID: %s", webhook_domain.id)
        except SQLAlchemyError as e:
            logger.error("Error adding Webhook to database: %s", e, exc_info=True)
            await self.db_session.rollback()
            raise

    async def get_by_id(self, webhook_id: UUID) -> Optional[Webhook]:
        """Retrieves a Webhook by its UUID."""
        try:
            stmt = select(WebhookModel).where(WebhookModel.id == webhook_id)
            result = await self.db_session.execute(stmt)
            db_model = result.scalar_one_or_none()
            return _to_domain(db_model) if db_model else None
        except SQLAlchemyError as e:
            logger.error(
                "Error retrieving Webhook by ID %s: %s", webhook_id, e, exc_info=True
            )
            raise

    async def list_by_user_id(self, user_id: UUID) -> List[Webhook]:
        """Lists all Webhooks for a given user."""
        try:
            stmt = (
                select(WebhookModel)
                .where(WebhookModel.user_id == user_id)
                .order_by(WebhookModel.created_at.desc())
            )
            result = await self.db_session.execute(stmt)
            db_models = result.scalars().all()
            return [_to_domain(model) for model in db_models]
        except SQLAlchemyError as e:
            logger.error(
                "Error listing Webhooks for user ID %s: %s", user_id, e, exc_info=True
            )
            raise

    async def list_by_user_id_and_event_type(
        self, user_id: UUID, event_type: str
    ) -> List[Webhook]:
        """Lists all active webhooks for a user subscribed to a specific event type."""
        try:
            stmt = (
                select(WebhookModel)
                .where(
                    WebhookModel.user_id == user_id,
                    WebhookModel.is_active == True,
                    WebhookModel.event_types.contains([event_type]),
                )
                .order_by(WebhookModel.created_at.desc())
            )
            result = await self.db_session.execute(stmt)
            db_models = result.scalars().all()
            return [_to_domain(model) for model in db_models]
        except SQLAlchemyError as e:
            logger.error(
                "Error listing Webhooks for user %s and event %s: %s",
                user_id,
                event_type,
                e,
                exc_info=True,
            )
            raise

    async def update(self, webhook_domain: Webhook) -> None:
        """Updates an existing Webhook in the database."""
        try:
            existing_model = await self.db_session.get(WebhookModel, webhook_domain.id)
            if not existing_model:
                logger.warning(
                    "Attempted to update non-existent Webhook with ID: %s",
                    webhook_domain.id,
                )
                return

            update_data = _to_db_model(webhook_domain)
            existing_model.target_url = update_data.target_url
            existing_model.event_types = update_data.event_types
            existing_model.hashed_secret = update_data.hashed_secret
            existing_model.is_active = update_data.is_active

            await self.db_session.flush()
            logger.info("Updated Webhook with ID: %s", webhook_domain.id)
        except SQLAlchemyError as e:
            logger.error(
                "Error updating Webhook with ID %s: %s",
                webhook_domain.id,
                e,
                exc_info=True,
            )
            await self.db_session.rollback()
            raise

    async def delete(self, webhook_id: UUID) -> None:
        """Deletes a Webhook from the database."""
        try:
            stmt = sqlalchemy_delete(WebhookModel).where(WebhookModel.id == webhook_id)
            await self.db_session.execute(stmt)
            await self.db_session.flush()
            logger.info("Deleted Webhook with ID: %s", webhook_id)
        except SQLAlchemyError as e:
            logger.error(
                "Error deleting Webhook with ID %s: %s", webhook_id, e, exc_info=True
            )
            await self.db_session.rollback()
            raise