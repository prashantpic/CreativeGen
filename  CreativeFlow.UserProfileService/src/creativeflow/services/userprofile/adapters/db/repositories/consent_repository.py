"""
SQLAlchemy repository for Consent data.
"""
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Consent, ConsentType
from ....domain.repositories import IConsentRepository
from ..sqlalchemy_models import ConsentSQL


class SQLAlchemyConsentRepository(IConsentRepository):
    """
    Handles database operations for Consent domain entities using SQLAlchemy.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain(self, orm_consent: ConsentSQL) -> Consent:
        """Maps an ORM object to a domain model."""
        return Consent(
            id=orm_consent.id,
            auth_user_id=orm_consent.auth_user_id,
            consent_type=ConsentType(orm_consent.consent_type),
            is_granted=orm_consent.is_granted,
            version=orm_consent.version,
            timestamp=orm_consent.timestamp,
        )

    async def get_by_user_and_type(
        self, auth_user_id: str, consent_type: ConsentType
    ) -> Optional[Consent]:
        stmt = select(ConsentSQL).where(
            ConsentSQL.auth_user_id == auth_user_id,
            ConsentSQL.consent_type == consent_type.value,
        )
        result = await self.db_session.execute(stmt)
        orm_consent = result.scalars().first()
        return self._to_domain(orm_consent) if orm_consent else None

    async def get_all_by_user(self, auth_user_id: str) -> List[Consent]:
        stmt = select(ConsentSQL).where(ConsentSQL.auth_user_id == auth_user_id)
        result = await self.db_session.execute(stmt)
        orm_consents = result.scalars().all()
        return [self._to_domain(c) for c in orm_consents]

    async def save(self, consent: Consent) -> Consent:
        orm_consent = ConsentSQL(
            id=consent.id,
            auth_user_id=consent.auth_user_id,
            consent_type=consent.consent_type.value,
            is_granted=consent.is_granted,
            version=consent.version,
            timestamp=consent.timestamp,
        )
        # merge() handles both INSERT and UPDATE based on primary key
        merged_consent = await self.db_session.merge(orm_consent)
        await self.db_session.commit()
        await self.db_session.refresh(merged_consent)
        return self._to_domain(merged_consent)

    async def delete_by_user_and_type(
        self, auth_user_id: str, consent_type: ConsentType
    ) -> None:
        stmt = delete(ConsentSQL).where(
            ConsentSQL.auth_user_id == auth_user_id,
            ConsentSQL.consent_type == consent_type.value,
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()