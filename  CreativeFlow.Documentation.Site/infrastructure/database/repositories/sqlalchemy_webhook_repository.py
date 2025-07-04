```python
import uuid
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.webhook import Webhook, WebhookEvent
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.database.models.webhook_model import WebhookModel


class SqlAlchemyWebhookRepository(IWebhookRepository):
    """
    SQLAlchemy implementation of the Webhook repository interface.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def _to_domain(self, model: WebhookModel) -> Webhook:
        """Converts an ORM model to a domain model."""
        return Webhook.model_validate(model)

    async def add(self, webhook: Webhook) -> None:
        # Pydantic's HttpUrl needs to be converted to a string for the DB
        webhook_data = webhook.model_dump()
        webhook_data["target_url"] = str(webhook.target_url)
        model = WebhookModel(**webhook_data)
        self.db.add(model)
        await self.db.flush()

    async def get_by_id(self, webhook_id: uuid.UUID) -> Optional[Webhook]:
        stmt = select(WebhookModel).where(WebhookModel.id == webhook_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_user_id(self, user_id: uuid.UUID) -> List[Webhook]:
        stmt = select(WebhookModel).where(WebhookModel.user_id == user_id).order_by(WebhookModel.created_at.desc())
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def list_by_user_id_and_event_type(
        self, user_id: uuid.UUID, event_type: WebhookEvent
    ) -> List[Webhook]:
        stmt = (
            select(WebhookModel)
            .where(
                WebhookModel.user_id == user_id,
                WebhookModel.event_types.any(event_type.value),
                WebhookModel.is_active == True,
            )
        )
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def update(self, webhook: Webhook) -> None:
        stmt = select(WebhookModel).where(WebhookModel.id == webhook.id)
        result = await self.db.execute(stmt)
        model_to_update = result.scalar_one()

        update_data = webhook.model_dump(exclude_unset=True)
        update_data["target_url"] = str(webhook.target_url)
        
        for key, value in update_data.items():
            setattr(model_to_update, key, value)
        
        await self.db.flush()

    async def delete(self, webhook_id: uuid.UUID) -> None:
        stmt = delete(WebhookModel).where(WebhookModel.id == webhook_id)
        await self.db.execute(stmt)
        await self.db.flush()
```