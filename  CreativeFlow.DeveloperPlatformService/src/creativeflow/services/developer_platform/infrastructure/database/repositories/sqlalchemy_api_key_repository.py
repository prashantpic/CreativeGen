# -*- coding: utf-8 -*-
"""
SQLAlchemy implementation of the IApiKeyRepository interface.
Provides concrete data access methods for APIKey entities using SQLAlchemy and PostgreSQL.
"""
import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.api_key import APIKey, APIKeyPermissions
from domain.repositories.api_key_repository import IApiKeyRepository
from infrastructure.database.models.api_key_model import APIKeyModel

logger = logging.getLogger(__name__)


def _to_domain(db_model: APIKeyModel) -> APIKey:
    """Maps an APIKeyModel ORM object to an APIKey domain model."""
    return APIKey(
        id=db_model.id,
        user_id=db_model.user_id,
        name=db_model.name,
        key_prefix=db_model.key_prefix,
        secret_hash=db_model.secret_hash,
        permissions=APIKeyPermissions(**db_model.permissions)
        if db_model.permissions
        else APIKeyPermissions(),
        is_active=db_model.is_active,
        created_at=db_model.created_at,
        revoked_at=db_model.revoked_at,
    )


def _to_db_model(domain_model: APIKey) -> APIKeyModel:
    """Maps an APIKey domain model to an APIKeyModel ORM object."""
    return APIKeyModel(
        id=domain_model.id,
        user_id=domain_model.user_id,
        name=domain_model.name,
        key_prefix=domain_model.key_prefix,
        secret_hash=domain_model.secret_hash,
        permissions=domain_model.permissions.model_dump(),
        is_active=domain_model.is_active,
        created_at=domain_model.created_at,
        revoked_at=domain_model.revoked_at,
    )


class SqlAlchemyApiKeyRepository(IApiKeyRepository):
    """SQLAlchemy implementation for APIKey data persistence."""

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an async database session.

        :param db_session: The SQLAlchemy AsyncSession.
        """
        self.db_session = db_session

    async def add(self, api_key_domain: APIKey) -> None:
        """Adds a new API Key to the database."""
        db_model = _to_db_model(api_key_domain)
        try:
            self.db_session.add(db_model)
            await self.db_session.flush()
            logger.info("Added new API Key with ID: %s", api_key_domain.id)
        except SQLAlchemyError as e:
            logger.error("Error adding API Key to database: %s", e, exc_info=True)
            await self.db_session.rollback()
            raise

    async def get_by_id(self, api_key_id: UUID) -> Optional[APIKey]:
        """Retrieves an API Key by its UUID."""
        try:
            stmt = select(APIKeyModel).where(APIKeyModel.id == api_key_id)
            result = await self.db_session.execute(stmt)
            db_model = result.scalar_one_or_none()
            return _to_domain(db_model) if db_model else None
        except SQLAlchemyError as e:
            logger.error(
                "Error retrieving API Key by ID %s: %s", api_key_id, e, exc_info=True
            )
            raise

    async def get_by_key_prefix(self, key_prefix: str) -> Optional[APIKey]:
        """Retrieves an API Key by its unique key prefix."""
        try:
            stmt = select(APIKeyModel).where(APIKeyModel.key_prefix == key_prefix)
            result = await self.db_session.execute(stmt)
            db_model = result.scalar_one_or_none()
            return _to_domain(db_model) if db_model else None
        except SQLAlchemyError as e:
            logger.error(
                "Error retrieving API Key by prefix %s: %s", key_prefix, e, exc_info=True
            )
            raise

    async def list_by_user_id(self, user_id: UUID) -> List[APIKey]:
        """Lists all API Keys for a given user."""
        try:
            stmt = (
                select(APIKeyModel)
                .where(APIKeyModel.user_id == user_id)
                .order_by(APIKeyModel.created_at.desc())
            )
            result = await self.db_session.execute(stmt)
            db_models = result.scalars().all()
            return [_to_domain(model) for model in db_models]
        except SQLAlchemyError as e:
            logger.error(
                "Error listing API Keys for user ID %s: %s", user_id, e, exc_info=True
            )
            raise

    async def update(self, api_key_domain: APIKey) -> None:
        """Updates an existing API Key in the database."""
        try:
            # Fetch existing model to merge into
            existing_model = await self.db_session.get(APIKeyModel, api_key_domain.id)
            if not existing_model:
                logger.warning(
                    "Attempted to update non-existent API Key with ID: %s",
                    api_key_domain.id,
                )
                return

            update_data = _to_db_model(api_key_domain)
            # Merge fields
            existing_model.name = update_data.name
            existing_model.permissions = update_data.permissions
            existing_model.is_active = update_data.is_active
            existing_model.revoked_at = update_data.revoked_at

            await self.db_session.flush()
            logger.info("Updated API Key with ID: %s", api_key_domain.id)
        except SQLAlchemyError as e:
            logger.error(
                "Error updating API Key with ID %s: %s",
                api_key_domain.id,
                e,
                exc_info=True,
            )
            await self.db_session.rollback()
            raise