```python
from typing import AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.api_key_service import APIKeyService
from application.services.asset_proxy_service import AssetProxyService
from application.services.generation_proxy_service import GenerationProxyService
from application.services.quota_management_service import QuotaManagementService
from application.services.rate_limiting_service import RateLimitingService
from application.services.usage_tracking_service import UsageTrackingService
from application.services.user_team_proxy_service import UserTeamProxyService
from application.services.webhook_service import WebhookService
from core.config import get_settings
from domain.repositories.api_key_repository import IApiKeyRepository
from domain.repositories.quota_repository import IQuotaRepository
from domain.repositories.usage_repository import IUsageRepository
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.cache.redis_client import redis_client
from infrastructure.database.repositories.sqlalchemy_api_key_repository import (
    SqlAlchemyApiKeyRepository,
)
from infrastructure.database.repositories.sqlalchemy_quota_repository import (
    SqlAlchemyQuotaRepository,
)
from infrastructure.database.repositories.sqlalchemy_usage_repository import (
    SqlAlchemyUsageRepository,
)
from infrastructure.database.repositories.sqlalchemy_webhook_repository import (
    SqlAlchemyWebhookRepository,
)
from infrastructure.database.session import get_async_db_session
from infrastructure.external_clients.ai_generation_client import (
    AIGenerationClient,
    ai_generation_client,
)
from infrastructure.external_clients.asset_management_client import (
    AssetManagementClient,
    asset_management_client,
)
from infrastructure.external_clients.user_team_client import (
    UserTeamClient,
    user_team_client,
)
from infrastructure.messaging.rabbitmq_client import RabbitMQClient, rabbitmq_client
from infrastructure.messaging.webhook_publisher import IWebhookPublisher, WebhookPublisher


# --- Infrastructure Layer Dependencies ---

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session for a single request."""
    async for session in get_async_db_session():
        yield session


async def get_rabbitmq_client() -> RabbitMQClient:
    """Provides the singleton RabbitMQ client instance."""
    return rabbitmq_client


async def get_redis_client() -> Redis:
    """Provides the singleton Redis client instance's connection."""
    return await redis_client.get_client()


def get_ai_generation_client() -> AIGenerationClient:
    """Provides the singleton AI Generation HTTP client instance."""
    return ai_generation_client


def get_asset_management_client() -> AssetManagementClient:
    """Provides the singleton Asset Management HTTP client instance."""
    return asset_management_client


def get_user_team_client() -> UserTeamClient:
    """Provides the singleton User/Team Management HTTP client instance."""
    return user_team_client


# --- Repository Dependencies ---

def get_api_key_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IApiKeyRepository:
    """Provides an instance of the API Key repository."""
    return SqlAlchemyApiKeyRepository(db_session=db_session)


def get_webhook_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IWebhookRepository:
    """Provides an instance of the Webhook repository."""
    return SqlAlchemyWebhookRepository(db_session=db_session)


def get_usage_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IUsageRepository:
    """Provides an instance of the Usage repository."""
    return SqlAlchemyUsageRepository(db_session=db_session)


def get_quota_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IQuotaRepository:
    """Provides an instance of the Quota repository."""
    return SqlAlchemyQuotaRepository(db_session=db_session)


# --- Messaging Dependencies ---

def get_webhook_publisher(
    rabbitmq_cli: RabbitMQClient = Depends(get_rabbitmq_client),
) -> IWebhookPublisher:
    """Provides an instance of the Webhook publisher."""
    settings = get_settings()
    return WebhookPublisher(
        rabbitmq_client=rabbitmq_cli,
        exchange_name=settings.RABBITMQ_WEBHOOK_EXCHANGE_NAME,
        routing_key_prefix=settings.RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX,
    )


# --- Application Service Dependencies ---

def get_api_key_service(
    api_key_repo: IApiKeyRepository = Depends(get_api_key_repository),
) -> APIKeyService:
    """Provides an instance of the API Key service."""
    return APIKeyService(api_key_repo=api_key_repo)


def get_webhook_service(
    webhook_repo: IWebhookRepository = Depends(get_webhook_repository),
    webhook_publisher: IWebhookPublisher = Depends(get_webhook_publisher),
) -> WebhookService:
    """Provides an instance of the Webhook service."""
    return WebhookService(webhook_repo=webhook_repo, webhook_publisher=webhook_publisher)


def get_usage_tracking_service(
    usage_repo: IUsageRepository = Depends(get_usage_repository),
) -> UsageTrackingService:
    """Provides an instance of the Usage Tracking service."""
    return UsageTrackingService(usage_repo=usage_repo)


def get_quota_management_service(
    quota_repo: IQuotaRepository = Depends(get_quota_repository),
    usage_repo: IUsageRepository = Depends(get_usage_repository),
) -> QuotaManagementService:
    """Provides an instance of the Quota Management service."""
    return QuotaManagementService(quota_repo=quota_repo, usage_repo=usage_repo)


def get_rate_limiting_service(
    redis_cli: Redis = Depends(get_redis_client),
) -> RateLimitingService:
    """Provides an instance of the Rate Limiting service."""
    return RateLimitingService(redis_client=redis_cli)


def get_generation_proxy_service(
    ai_gen_client: AIGenerationClient = Depends(get_ai_generation_client),
) -> GenerationProxyService:
    """Provides an instance of the Generation Proxy service."""
    return GenerationProxyService(ai_gen_client=ai_gen_client)


def get_asset_proxy_service(
    asset_mgmt_client: AssetManagementClient = Depends(get_asset_management_client),
) -> AssetProxyService:
    """Provides an instance of the Asset Proxy service."""
    return AssetProxyService(asset_mgmt_client=asset_mgmt_client)


def get_user_team_proxy_service(
    user_team_cli: UserTeamClient = Depends(get_user_team_client),
) -> UserTeamProxyService:
    """Provides an instance of the User/Team Proxy service."""
    return UserTeamProxyService(user_team_client=user_team_cli)
```