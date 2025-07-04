import time
import uuid
from typing import Optional

import redis.asyncio as aioredis


class RateLimitingService:
    """
    Manages and enforces API rate limits using Redis.

    This implementation uses the sliding window log algorithm.
    """

    def __init__(
        self,
        redis_client: aioredis.Redis,
        requests: int,
        period_seconds: int
    ):
        """
        Initializes the RateLimitingService.

        Args:
            redis_client: An asynchronous Redis client instance.
            requests: The number of allowed requests in the time window.
            period_seconds: The time window duration in seconds.
        """
        self.redis = redis_client
        self.requests = requests
        self.period_seconds = period_seconds

    async def is_rate_limited(self, key: str) -> bool:
        """
        Checks if a given key (e.g., API client ID) has exceeded its rate limit.

        This method implements the sliding window log algorithm. It logs each request's
        timestamp in a Redis sorted set. It then removes old timestamps and counts
        the remaining ones to see if the limit is exceeded.

        Args:
            key: A unique identifier for the entity being rate-limited
                 (e.g., `rate_limit:client_id:endpoint`).

        Returns:
            True if the request should be blocked (rate limit exceeded),
            False otherwise.
        """
        now = time.time()
        window_start = now - self.period_seconds

        # Use a MULTI/EXEC transaction for atomicity
        async with self.redis.pipeline() as pipe:
            # 1. Remove timestamps older than the current window
            pipe.zremrangebyscore(key, 0, window_start)
            # 2. Add the current request's timestamp
            # Use a unique member for each request to avoid overwriting
            pipe.zadd(key, {f"{now}:{uuid.uuid4()}": now})
            # 3. Count the number of requests in the window
            pipe.zcard(key)
            # 4. Set an expiry on the key to auto-clean if traffic stops
            pipe.expire(key, self.period_seconds)

            results = await pipe.execute()

        current_requests = results[2]

        return current_requests > self.requests