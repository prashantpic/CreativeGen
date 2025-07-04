"""
Caching mechanism for platform insights using Redis or an in-memory cache with TTL.
"""

import json
import logging
from typing import Any, Optional

import redis.asyncio as aioredis
from cachetools import TTLCache

logger = logging.getLogger(__name__)


class PlatformInsightsCache:
    """
    Caches platform insights to reduce API calls to social media platforms
    and improve response times.

    It uses Redis if a client is provided, otherwise falls back to a simple
    in-memory TTLCache.
    """

    def __init__(
        self,
        redis_client: Optional[aioredis.Redis] = None,
        default_ttl_seconds: int = 3600,
    ):
        """
        Initializes the cache client.

        Args:
            redis_client: An optional asynchronous Redis client instance.
            default_ttl_seconds: The default time-to-live for cache entries in seconds.
        """
        self.redis_client = redis_client
        self.default_ttl_seconds = default_ttl_seconds
        self.in_memory_cache = TTLCache(maxsize=1000, ttl=default_ttl_seconds)
        if self.redis_client:
            logger.info("PlatformInsightsCache initialized with Redis.")
        else:
            logger.warning("PlatformInsightsCache initialized with in-memory TTL cache (fallback).")

    def _generate_cache_key(
        self, platform: str, insight_type: str, context_key: str
    ) -> str:
        """Generates a standardized cache key."""
        return f"insights:{platform}:{insight_type}:{context_key}"

    async def get_insights(
        self, platform: str, insight_type: str, context_key: str
    ) -> Optional[Any]:
        """
        Retrieves insights data from the cache.

        Args:
            platform: The social media platform.
            insight_type: The type of insight (e.g., 'hashtags').
            context_key: A unique key representing the context of the request
                         (e.g., a hash of keywords).

        Returns:
            The cached data if found and not stale, otherwise None.
        """
        key = self._generate_cache_key(platform, insight_type, context_key)
        
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    logger.debug("Cache hit from Redis for key: %s", key)
                    return json.loads(cached_data)
            except Exception as e:
                logger.error("Failed to get data from Redis for key %s: %s", key, e)
                # Fallback to in-memory or just return None
        else:
            cached_data = self.in_memory_cache.get(key)
            if cached_data:
                logger.debug("Cache hit from in-memory cache for key: %s", key)
                return cached_data

        logger.debug("Cache miss for key: %s", key)
        return None

    async def set_insights(
        self, platform: str, insight_type: str, context_key: str, data: Any
    ) -> None:
        """
        Stores insights data in the cache.

        Args:
            platform: The social media platform.
            insight_type: The type of insight.
            context_key: A unique key for the request context.
            data: The data to be cached (must be JSON-serializable).
        """
        key = self._generate_cache_key(platform, insight_type, context_key)
        
        try:
            serialized_data = json.dumps(data)
        except TypeError as e:
            logger.error("Failed to serialize data for caching (key: %s): %s", key, e)
            return

        if self.redis_client:
            try:
                await self.redis_client.set(key, serialized_data, ex=self.default_ttl_seconds)
                logger.debug("Cached data in Redis for key: %s", key)
            except Exception as e:
                logger.error("Failed to set data in Redis for key %s: %s", key, e)
        else:
            self.in_memory_cache[key] = data
            logger.debug("Cached data in in-memory cache for key: %s", key)