#
# CreativeFlow.RedisCache - cache_admin_tools.py
#
# Provides administrative utilities for managing general-purpose caches
# (e.g., resolved templates, user preferences, API responses) stored in Redis.
#

from .redis_connector import get_redis_connection

class CacheAdmin:
    """A collection of tools for administering general-purpose caches in Redis."""

    def __init__(self, redis_host=None, redis_port=None, redis_password=None, cache_db_index=1):
        """
        Initializes the cache admin tools.

        Args:
            redis_host (str, optional): Redis server host.
            redis_port (int, optional): Redis server port.
            redis_password (str, optional): Redis server password.
            cache_db_index (int, optional): The Redis DB index for the cache. Defaults to 1.
        
        Raises:
            ConnectionError: If a connection to Redis cannot be established.
        """
        self.redis_client = get_redis_connection(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=cache_db_index,
            use_pool=False
        )
        if not self.redis_client:
            raise ConnectionError("Failed to connect to Redis for CacheAdmin.")

    def list_cache_keys(self, pattern="cache:*", count=1000):
        """
        Lists cache keys matching a pattern using the safe SCAN command.

        Args:
            pattern (str, optional): The glob-style pattern to match. Defaults to "cache:*".
            count (int, optional): The approximate number of keys to return. Set to 0 for all keys (use with caution).

        Returns:
            list: A list of cache keys matching the pattern.
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

    def get_cache_value(self, key):
        """
        Retrieves the raw value of a cache key.

        Note: The value might be serialized (e.g., JSON, Pickle). This method returns
        the raw string/bytes as stored in Redis.

        Args:
            key (str): The cache key to retrieve.

        Returns:
            str or None: The value of the cache key, or None if it doesn't exist.
        """
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print(f"Error getting cache value for key '{key}': {e}")
            return None

    def get_cache_ttl(self, key):
        """
        Gets the Time To Live (TTL) for a cache key in seconds.

        Args:
            key (str): The cache key to check.

        Returns:
            int or None: The TTL in seconds. Returns -1 if the key exists but has no expiry.
                         Returns -2 if the key does not exist. Returns None on error.
        """
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            print(f"Error getting TTL for key '{key}': {e}")
            return None

    def delete_cache_key(self, key):
        """
        Deletes a specific cache key.

        Args:
            key (str): The cache key to delete.

        Returns:
            bool: True if the key was deleted, False otherwise.
        """
        try:
            deleted_count = self.redis_client.delete(key)
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting cache key '{key}': {e}")
            return False

    def flush_cache_by_pattern(self, pattern="cache:*"):
        """
        Deletes all keys matching a given pattern.
        
        WARNING: This can be a slow and blocking operation on a production database
        if the pattern matches a very large number of keys. Use with extreme caution.
        Prefer targeted deletion or rely on Redis eviction policies where possible.

        Args:
            pattern (str, optional): The glob-style pattern for keys to delete. Defaults to "cache:*".

        Returns:
            int: The number of keys deleted.
        """
        deleted_count = 0
        try:
            keys_to_delete = list(self.redis_client.scan_iter(match=pattern))
            if keys_to_delete:
                # For a very large number of keys, it's better to pipeline the deletes
                # to reduce round-trip time.
                pipe = self.redis_client.pipeline()
                for key in keys_to_delete:
                    pipe.delete(key)
                results = pipe.execute()
                deleted_count = sum(results)
            return deleted_count
        except Exception as e:
            print(f"Error flushing cache with pattern '{pattern}': {e}")
            return 0