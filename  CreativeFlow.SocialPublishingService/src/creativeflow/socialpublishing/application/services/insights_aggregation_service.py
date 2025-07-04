"""
Fetches and aggregates insights like trending hashtags and best times to post
from social platforms.
"""
import hashlib
import json
import logging
from typing import Dict

from ....api.v1.schemas import insights_schemas
from ....config import Settings
from ...infrastructure.caching.platform_insights_cache import \
    PlatformInsightsCache
from ...infrastructure.clients.base_social_client import BaseSocialClient
from ..exceptions import ConnectionNotFoundError, InsufficientPermissionsError
from .oauth_orchestration_service import OAuthOrchestrationService

logger = logging.getLogger(__name__)


class InsightsAggregationService:
    """
    Provides content optimization insights by interacting with social media
    platform APIs and a caching layer.
    """

    def __init__(
        self,
        oauth_service: OAuthOrchestrationService,
        insights_cache: PlatformInsightsCache,
        config: Settings,
        platform_clients: Dict[str, BaseSocialClient],
    ):
        self.oauth_service = oauth_service
        self.cache = insights_cache
        self.config = config
        self.platform_clients = platform_clients

    def _get_platform_client(self, platform: str) -> BaseSocialClient:
        client = self.platform_clients.get(platform.lower())
        if not client:
            raise ValueError(f"Platform '{platform}' is not supported.")
        return client

    async def get_trending_hashtags(
        self,
        user_id: str,
        platform: str,
        request_payload: insights_schemas.HashtagRequest,
    ) -> insights_schemas.HashtagResponse:
        """
        Fetches hashtag suggestions, utilizing a cache-aside strategy.
        """
        # Generate a cache key based on the request parameters
        context_str = f"{request_payload.keywords}:{request_payload.industry}:{request_payload.limit}"
        context_key = hashlib.md5(context_str.encode()).hexdigest()
        
        cached_data = await self.cache.get_insights(platform, "hashtags", context_key)
        if cached_data:
            return insights_schemas.HashtagResponse(suggestions=cached_data)

        client = self._get_platform_client(platform)
        try:
            # Some platforms might not need a user token for this
            suggestions = await client.get_trending_hashtags(
                access_token=None,  # Or fetch if needed
                keywords=request_payload.keywords,
                industry=request_payload.industry,
                limit=request_payload.limit,
            )
            await self.cache.set_insights(platform, "hashtags", context_key, suggestions)
            return insights_schemas.HashtagResponse(suggestions=suggestions)
        except NotImplementedError:
             raise InsufficientPermissionsError(f"Hashtag insights are not available for platform '{platform}'.")
        except Exception as e:
            logger.error("Failed to fetch hashtags for platform %s: %s", platform, e)
            raise

    async def get_best_times_to_post(
        self, user_id: str, platform: str, connection_id: str
    ) -> insights_schemas.BestTimeToPostResponse:
        """
        Fetches best times to post for a user's connected account, using a
        cache-aside strategy.
        """
        connection = await self.oauth_service.repo.get_by_id(connection_id)
        if not connection or connection.user_id != user_id:
            raise ConnectionNotFoundError("Invalid connection ID provided.")

        context_key = connection.external_user_id
        cached_data = await self.cache.get_insights(platform, "best-times", context_key)
        if cached_data:
            return insights_schemas.BestTimeToPostResponse(**cached_data)

        client = self._get_platform_client(platform)
        try:
            access_token = await self.oauth_service.get_valid_access_token(
                connection_id, user_id
            )
            suggestions = await client.get_best_post_times(access_token)
            
            response_data = {
                "suggested_times": suggestions,
                "confidence": "high" # Placeholder
            }

            await self.cache.set_insights(platform, "best-times", context_key, response_data)
            return insights_schemas.BestTimeToPostResponse(**response_data)
        except NotImplementedError:
            raise InsufficientPermissionsError(f"Best time to post insights are not available for platform '{platform}'.")
        except Exception as e:
            logger.error("Failed to fetch best times for connection %s: %s", connection_id, e)
            raise