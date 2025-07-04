#
# CreativeFlow.RedisCache - rate_limit_utils.py
#
# Offers administrative utilities for inspecting and managing rate limit
# counters stored in Redis.
#

from .redis_connector import get_redis_connection

class RateLimitAdmin:
    """A collection of tools for administering rate limit counters in Redis."""

    def __init__(self, redis_host=None, redis_port=None, redis_password=None, rate_limit_db_index=3):
        """
        Initializes the rate limit admin tools.

        Args:
            redis_host (str, optional): Redis server host.
            redis_port (int, optional): Redis server port.
            redis_password (str, optional): Redis server password.
            rate_limit_db_index (int, optional): The Redis DB index for rate limit counters. Defaults to 3.
        
        Raises:
            ConnectionError: If a connection to Redis cannot be established.
        """
        self.redis_client = get_redis_connection(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=rate_limit_db_index,
            use_pool=False
        )
        if not self.redis_client:
            raise ConnectionError("Failed to connect to Redis for RateLimitAdmin.")

    def get_rate_limit_value(self, counter_key):
        """
        Gets the current integer value of a rate limit counter.

        Args:
            counter_key (str): The key for the rate limit counter.

        Returns:
            int or None: The current value of the counter, or None if the key doesn't exist or an error occurs.
        """
        try:
            value = self.redis_client.get(counter_key)
            return int(value) if value is not None else None
        except (ValueError, TypeError) as e:
            print(f"Error converting value for counter '{counter_key}' to int: {e}")
            return None
        except Exception as e:
            print(f"Error getting rate limit value for '{counter_key}': {e}")
            return None

    def reset_rate_limit_counter(self, counter_key):
        """
        Resets a specific rate limit counter by deleting its key.

        Args:
            counter_key (str): The key of the counter to reset.

        Returns:
            bool: True if the counter key was deleted, False otherwise.
        """
        try:
            deleted_count = self.redis_client.delete(counter_key)
            return deleted_count > 0
        except Exception as e:
            print(f"Error resetting rate limit counter '{counter_key}': {e}")
            return False

    def list_rate_limit_keys(self, pattern="ratelimit:*", count=1000):
        """
        Lists rate limit keys matching a pattern using the safe SCAN command.

        Args:
            pattern (str, optional): The glob-style pattern to match. Defaults to "ratelimit:*".
            count (int, optional): The approximate number of keys to return. Set to 0 for all keys.

        Returns:
            list: A list of rate limit keys matching the pattern.
        """
        if count == 0: # Get all keys
            return list(self.redis_client.scan_iter(match=pattern))
        
        keys_found = []
        cursor = '0'
        while cursor != 0:
            cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern, count=count)
            keys_found.extend(keys)
            if len(keys_found) >= count:
                break
        return keys_found[:count]