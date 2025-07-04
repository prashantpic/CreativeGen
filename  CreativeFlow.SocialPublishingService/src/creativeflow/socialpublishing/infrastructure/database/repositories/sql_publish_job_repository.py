"""
SQLAlchemy implementation of the IPublishJobRepository interface.
"""
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models.publish_job import PublishJob, PublishJobStatus
from ....domain.repositories.publish_job_repository import IPublishJobRepository
from ..sqlalchemy_models import PublishJobSQL


class SQLPublishJobRepository(IPublishJobRepository):
    """
    Provides concrete data access logic for PublishJob entities
    using SQLAlchemy and a PostgreSQL database.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @staticmethod
    def _map_to_domain(db_job: PublishJobSQL) -> PublishJob:
        """Maps a SQLAlchemy model instance to a domain model."""
        return PublishJob.model_validate(db_job)

    @staticmethod
    def _map_to_db_model(
        domain_job: PublishJob, db_job_sql: Optional[PublishJobSQL] = None
    ) -> PublishJobSQL:
        """Maps a domain model to a SQLAlchemy model for saving."""
        if db_job_sql is None:
            db_job_sql = PublishJobSQL()
            
        data = domain_job.model_dump()
        for key, value in data.items():
            if isinstance(value, Enum): # Handle Enum serialization
                 setattr(db_job_sql, key, value.value)
            else:
                 setattr(db_job_sql, key, value)
        return db_job_sql

    async def get_by_id(self, job_id: UUID) -> Optional[PublishJob]:
        stmt = select(PublishJobSQL).where(PublishJobSQL.id == job_id)
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()
        return self._map_to_domain(db_model) if db_model else None

    async def list_by_user_id(
        self, user_id: str, platform: Optional[str] = None, status: Optional[str] = None
    ) -> List[PublishJob]:
        stmt = select(PublishJobSQL).where(PublishJobSQL.user_id == user_id)
        if platform:
            stmt = stmt.where(PublishJobSQL.platform == platform)
        if status:
            stmt = stmt.where(PublishJobSQL.status == status)
        
        result = await self.db_session.execute(stmt)
        db_models = result.scalars().all()
        return [self._map_to_domain(db_model) for db_model in db_models]

    async def save(self, job: PublishJob) -> PublishJob:
        is_new = False
        stmt = select(PublishJobSQL).where(PublishJobSQL.id == job.id)
        result = await self.db_session.execute(stmt)
        db_model = result.scalars().first()
        
        if db_model is None:
            is_new = True
            db_model = PublishJobSQL(id=job.id, created_at=datetime.now(timezone.utc))

        db_model = self._map_to_db_model(job, db_model)
        db_model.updated_at = datetime.now(timezone.utc)

        if is_new:
            self.db_session.add(db_model)
            
        await self.db_session.flush()
        await self.db_session.refresh(db_model)
        
        return self._map_to_domain(db_model)

    async def find_pending_scheduled_jobs(self, limit: int = 100) -> List[PublishJob]:
        now_utc = datetime.now(timezone.utc)
        stmt = (
            select(PublishJobSQL)
            .where(
                PublishJobSQL.status == PublishJobStatus.SCHEDULED.value,
                PublishJobSQL.scheduled_at <= now_utc,
            )
            .order_by(PublishJobSQL.scheduled_at)
            .limit(limit)
        )
        result = await self.db_session.execute(stmt)
        db_models = result.scalars().all()
        return [self._map_to_domain(db_model) for db_model in db_models]