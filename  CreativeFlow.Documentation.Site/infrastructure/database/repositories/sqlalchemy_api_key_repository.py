```python
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.api_key import APIKey
from domain.repositories.api_key_repository import IApiKeyRepository
from infrastructure.database.models.api_key_model import APIKeyModel


class SqlAlchemyApiKeyRepository(IApiKeyRepository):
    """
    SQLAlchemy implementation of the API Key repository interface.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def _to_domain(self, model: APIKeyModel) -> APIKey:
        """Converts an ORM model to a domain model."""
        return APIKey.model_validate(model)

    async def add(self, api_key: APIKey) -> None:
        model = APIKeyModel(**api_key.model_dump())
        self.db.add(model)
        await self.db.flush()

    async def get_by_id(self, api_key_id: uuid.UUID) -> Optional[APIKey]:
        stmt = select(APIKeyModel).where(APIKeyModel.id == api_key_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_key_prefix(self, key_prefix: str) -> Optional[APIKey]:
        stmt = select(APIKeyModel).where(APIKeyModel.key_prefix == key_prefix)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_user_id(self, user_id: uuid.UUID) -> List[APIKey]:
        stmt = select(APIKeyModel).where(APIKeyModel.user_id == user_id, APIKeyModel.revoked_at.is_(None)).order_by(APIKeyModel.created_at.desc())
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def update(self, api_key: APIKey) -> None:
        stmt = select(APIKeyModel).where(APIKeyModel.id == api_key.id)
        result = await self.db.execute(stmt)
        model_to_update = result.scalar_one()

        update_data = api_key.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model_to_update, key, value)
        
        await self.db.flush()
```