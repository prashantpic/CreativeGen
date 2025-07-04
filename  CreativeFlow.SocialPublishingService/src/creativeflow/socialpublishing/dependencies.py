"""
FastAPI dependency injection setup.

Defines reusable dependencies for providing database sessions, service clients,
authentication, etc., to path operation functions.
"""
import logging
from typing import AsyncGenerator, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .application.exceptions import SocialPublishingBaseError
from .application.services import (InsightsAggregationService,
                                   OAuthOrchestrationService,
                                   PublishingOrchestrationService)
from .config import Settings, get_settings
from .domain.repositories import IPublishJobRepository, ISocialConnectionRepository
from .domain.services import ITokenEncryptionService, PlatformPolicyValidator
from .infrastructure.caching.platform_insights_cache import PlatformInsightsCache
from .infrastructure.clients.base_social_client import BaseSocialClient
# Import specific clients if you have them, for now we can use a factory pattern
from .infrastructure.database.repositories import (SQLPublishJobRepository,
                                                   SQLSocialConnectionRepository)
from .infrastructure.database.session_manager import DBSessionManager
from .infrastructure.security.aes_gcm_encryption_service import \
    AESGCMTokenEncryptionService

logger = logging.getLogger(__name__)

# This is a placeholder. In a real system, the tokenUrl would point to the
# authentication service's token endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Placeholder dependency to get the current user ID.

    In a real implementation, this would:
    1. Validate the JWT `token`.
    2. Communicate with an Authentication service or use a shared library
       to decode the token and verify its signature and claims.
    3. Extract the `user_id` from the token payload.

    For this SDS, we'll simulate a valid token and return a hardcoded user ID.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # --- Placeholder Logic ---
    # In a real app, you would decode and validate the token here.
    # For example: user_id = await auth_service_client.validate_token(token)
    if token == "invalid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Simulate extracting user_id from a valid token
    return "user-123-abc"


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a database session."""
    async for session in DBSessionManager.get_session():
        yield session

# --- Singleton-like Dependencies ---

def get_token_encryption_service(
    settings: Settings = Depends(get_settings),
) -> ITokenEncryptionService:
    """Dependency to get the token encryption service."""
    try:
        return AESGCMTokenEncryptionService(settings.AES_KEY)
    except ValueError as e:
        logger.critical("Failed to initialize TokenEncryptionService: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error for encryption.",
        ) from e

# --- Repository Dependencies ---

def get_social_connection_repo(
    db: AsyncSession = Depends(get_db_session),
) -> ISocialConnectionRepository:
    """Dependency to get the social connection repository implementation."""
    return SQLSocialConnectionRepository(db)


def get_publish_job_repo(
    db: AsyncSession = Depends(get_db_session),
) -> IPublishJobRepository:
    """Dependency to get the publish job repository implementation."""
    return SQLPublishJobRepository(db)

# --- Caching and Client Dependencies ---

async def get_redis_client(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator[Redis, None]:
    """Dependency to get a Redis client if configured."""
    if not settings.REDIS_URL:
        yield None
        return

    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()


def get_insights_cache(
    redis_client: Redis = Depends(get_redis_client),
    settings: Settings = Depends(get_settings),
) -> PlatformInsightsCache:
    """Dependency to get the platform insights cache."""
    return PlatformInsightsCache(redis_client, settings.INSIGHTS_CACHE_TTL_SECONDS)


def get_platform_clients() -> Dict[str, BaseSocialClient]:
    """Dependency to get a dictionary of all platform API clients."""
    # In a real application, you'd initialize these properly,
    # likely with a shared httpx.AsyncClient instance.
    # For now, this is a factory function returning placeholders.
    from .infrastructure.clients import (
        FacebookClient, InstagramClient, LinkedInClient,
        PinterestClient, TikTokClient, TwitterClient
    )
    # Here you would instantiate with a real client and config
    # settings = get_settings()
    # http_client = httpx.AsyncClient()
    return {
        "instagram": InstagramClient(None, None),
        "facebook": FacebookClient(None, None),
        "linkedin": LinkedInClient(None, None),
        "twitter": TwitterClient(None, None),
        "pinterest": PinterestClient(None, None),
        "tiktok": TikTokClient(None, None),
    }

# --- Application Service Dependencies ---

def get_oauth_orchestration_service(
    repo: ISocialConnectionRepository = Depends(get_social_connection_repo),
    encryption_service: ITokenEncryptionService = Depends(get_token_encryption_service),
    settings: Settings = Depends(get_settings),
    platform_clients: Dict[str, BaseSocialClient] = Depends(get_platform_clients),
) -> OAuthOrchestrationService:
    """Dependency to get the OAuth orchestration service."""
    return OAuthOrchestrationService(
        social_connection_repo=repo,
        token_encryption_service=encryption_service,
        config=settings,
        platform_clients=platform_clients,
    )


def get_publishing_orchestration_service(
    publish_job_repo: IPublishJobRepository = Depends(get_publish_job_repo),
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
    settings: Settings = Depends(get_settings),
    platform_clients: Dict[str, BaseSocialClient] = Depends(get_platform_clients),
) -> PublishingOrchestrationService:
    """Dependency to get the Publishing orchestration service."""
    return PublishingOrchestrationService(
        publish_job_repo=publish_job_repo,
        oauth_service=oauth_service,
        policy_validator=PlatformPolicyValidator(), # Simple instantiation
        config=settings,
        platform_clients=platform_clients,
    )


def get_insights_aggregation_service(
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
    cache: PlatformInsightsCache = Depends(get_insights_cache),
    settings: Settings = Depends(get_settings),
    platform_clients: Dict[str, BaseSocialClient] = Depends(get_platform_clients),
) -> InsightsAggregationService:
    """Dependency to get the Insights aggregation service."""
    return InsightsAggregationService(
        oauth_service=oauth_service,
        insights_cache=cache,
        config=settings,
        platform_clients=platform_clients,
    )