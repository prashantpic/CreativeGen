"""
SQLAlchemy repository for DataPrivacyRequest data.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import (DataPrivacyRequest, DataPrivacyRequestStatus,
                               DataPrivacyRequestType)
from ....domain.repositories import IDataPrivacyRequestRepository
from ..sqlalchemy_models import DataPrivacyRequestSQL


class SQLAlchemyDataPrivacyRequestRepository(IDataPrivacyRequestRepository):
    """
    Handles database operations for DataPrivacyRequest domain entities.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain(self, orm_request: DataPrivacyRequestSQL) -> DataPrivacyRequest:
        """Maps an ORM object to a domain model."""
        return DataPrivacyRequest(
            id=orm_request.id,
            auth_user_id=orm_request.auth_user_id,
            request_type=DataPrivacyRequestType(orm_request.request_type),
            status=DataPrivacyRequestStatus(orm_request.status),
            details=orm_request.details,
            created_at=orm_request.created_at,
            updated_at=orm_request.updated_at,
            processed_at=orm_request.processed_at,
            response_data_path=orm_request.response_data_path,
        )

    async def get_by_id(self, request_id: UUID) -> Optional[DataPrivacyRequest]:
        stmt = select(DataPrivacyRequestSQL).where(DataPrivacyRequestSQL.id == request_id)
        result = await self.db_session.execute(stmt)
        orm_request = result.scalars().first()
        return self._to_domain(orm_request) if orm_request else None

    async def save(self, request: DataPrivacyRequest) -> DataPrivacyRequest:
        orm_request = DataPrivacyRequestSQL(
            id=request.id,
            auth_user_id=request.auth_user_id,
            request_type=request.request_type.value,
            status=request.status.value,
            details=request.details,
            created_at=request.created_at,
            updated_at=request.updated_at,
            processed_at=request.processed_at,
            response_data_path=request.response_data_path,
        )
        self.db_session.add(orm_request)
        await self.db_session.commit()
        await self.db_session.refresh(orm_request)
        return self._to_domain(orm_request)

    async def update(self, request: DataPrivacyRequest) -> DataPrivacyRequest:
        stmt = select(DataPrivacyRequestSQL).where(DataPrivacyRequestSQL.id == request.id)
        result = await self.db_session.execute(stmt)
        orm_request = result.scalars().one()

        orm_request.status = request.status.value
        orm_request.details = request.details
        orm_request.updated_at = request.updated_at
        orm_request.processed_at = request.processed_at
        orm_request.response_data_path = request.response_data_path
        
        await self.db_session.commit()
        await self.db_session.refresh(orm_request)
        return self._to_domain(orm_request)

    async def get_by_user_and_type(
        self,
        auth_user_id: Optional[str],
        request_type: DataPrivacyRequestType,
        status: Optional[DataPrivacyRequestStatus] = None,
    ) -> List[DataPrivacyRequest]:
        stmt = select(DataPrivacyRequestSQL).where(
            DataPrivacyRequestSQL.request_type == request_type.value
        )
        if auth_user_id:
            stmt = stmt.where(DataPrivacyRequestSQL.auth_user_id == auth_user_id)
        if status:
            stmt = stmt.where(DataPrivacyRequestSQL.status == status.value)
        
        result = await self.db_session.execute(stmt)
        orm_requests = result.scalars().all()
        return [self._to_domain(req) for req in orm_requests]