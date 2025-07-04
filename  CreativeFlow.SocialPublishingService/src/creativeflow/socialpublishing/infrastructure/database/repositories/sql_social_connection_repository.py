"""
SQLAlchemy implementation of the ISocialConnectionRepository interface.
"""
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models.social_connection import SocialConnection
from ....domain.repositories.social_connection_repository import \
    ISocialConnectionRepository
from ..sqlalchemy_models import SocialConnectionSQL


class SQLSocialConnectionRepository(ISocialConnectionRepository):
    """
    Provides concrete data access logic for SocialConnection entities
    using SQLAlchemy and a PostgreSQL database.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @staticmethod
    def _map_to_domain(db_conn: SocialConnectionSQL) -> SocialConnection:
        """Maps a SQLAlchemy model instance to a domain model."""
        return SocialConnection.model_validate(db_conn)

    @staticmethod
    def _map_to_db_model(
        domain_conn: SocialConnection, db_conn_sql: Optional[SocialConnectionSQL] = None
    ) -> SocialConnectionSQL:
        """Maps a domain model to a SQLAlchemy model for saving."""
        if db_conn_sql is None:
            db_conn_sql = SocialConnectionSQL()

        data = domain_conn.model_dump()
        for key, value in data.items():
            setattr(db_conn_sql, key, value)
        return db_conn_sql

    async def get_by_id(self, connection_id: UUID) -> Optional[SocialConnection]:
        stmt = select(SocialConnectionSQL).where(SocialConnectionSQL.id == connection_id)
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()
        return self._map_to_domain(db_model) if db_model else None

    async def get_by_user_and_platform(
        self, user_id: str, platform: str
    ) -> Optional[SocialConnection]:
        stmt = select(SocialConnectionSQL).where(
            SocialConnectionSQL.user_id == user_id,
            SocialConnectionSQL.platform == platform,
        )
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()
        return self._map_to_domain(db_model) if db_model else None

    async def list_by_user_id(self, user_id: str) -> List[SocialConnection]:
        stmt = select(SocialConnectionSQL).where(SocialConnectionSQL.user_id == user_id)
        result = await self.db_session.execute(stmt)
        db_models = result.scalars().all()
        return [self._map_to_domain(db_model) for db_model in db_models]

    async def save(self, connection: SocialConnection) -> SocialConnection:
        is_new = False
        stmt = select(SocialConnectionSQL).where(SocialConnectionSQL.id == connection.id)
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()

        if db_model is None:
            is_new = True
            db_model = SocialConnectionSQL(id=connection.id, created_at=datetime.now(timezone.utc))

        # Update all fields from domain model
        db_model = self._map_to_db_model(connection, db_model)
        db_model.updated_at = datetime.now(timezone.utc)


        if is_new:
            self.db_session.add(db_model)
        
        await self.db_session.flush()
        await self.db_session.refresh(db_model)

        return self._map_to_domain(db_model)

    async def delete(self, connection_id: UUID) -> None:
        stmt = select(SocialConnectionSQL).where(SocialConnectionSQL.id == connection_id)
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()
        if db_model:
            await self.db_session.delete(db_model)
            await self.db_session.flush()