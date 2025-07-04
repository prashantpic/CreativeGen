```python
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.usage import Quota
from domain.repositories.quota_repository import IQuotaRepository
from infrastructure.database.models.quota_model import QuotaModel


class SqlAlchemyQuotaRepository(IQuotaRepository):
    """
    SQLAlchemy implementation of the Quota repository interface.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def _to_domain(self, model: QuotaModel) -> Quota:
        """Converts an ORM model to a domain model."""
        return Quota.model_validate(model)

    async def save_quota(self, quota: Quota) -> None:
        """
        Saves or updates a quota. This is an admin-level operation typically.
        """
        # Check if a quota already exists for the client
        existing = await self.get_quota_by_client_id(quota.api_client_id)
        if existing:
            # Update existing
            stmt = select(QuotaModel).where(QuotaModel.id == existing.id)
            result = await self.db.execute(stmt)
            model_to_update = result.scalar_one()

            update_data = quota.model_dump(exclude={"id"})
            for key, value in update_data.items():
                setattr(model_to_update, key, value)
        else:
            # Add new
            model = QuotaModel(**quota.model_dump())
            self.db.add(model)
        
        await self.db.flush()

    async def get_quota_by_client_id(self, api_client_id: uuid.UUID) -> Optional[Quota]:
        stmt = select(QuotaModel).where(QuotaModel.api_client_id == api_client_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
```