```python
import logging
from typing import Optional

import redis.asyncio as redis

logger = logging.getLogger(__name__)


class RedisClient:
    """Manages a connection pool to a Redis server."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self, redis_url: str):
        """
        Establishes a connection pool to Redis.
        """
        if self.client:
            logger.warning("Redis client already connected.")
            return
        
        try:
            self.client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
            await self.client.ping()
            logger.info("Successfully connected to Redis.")
        except Exception as e:
            logger.critical(f"Failed to connect to Redis: {e}", exc_info=True)
            raise

    async def close(self):
        """Closes the Redis connection pool."""
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Redis connection pool closed.")

    def get_client(self) -> redis.Redis:
        """
        Returns the active Redis client instance.

        Raises:
            ConnectionError: If the client is not connected.
        """
        if not self.client:
            raise ConnectionError("Redis client is not connected.")
        return self.client


# Create a singleton instance
redis_client = RedisClient()
```