#
# CreativeFlow.RedisCache - redis_connector.py
#
# Provides a centralized and reusable way to establish connections to Redis
# for other Python scripts within this repository.
#

import os
import sys
import redis

# Global connection pool instance. It's lazily initialized on first use.
_connection_pool = None

def get_redis_connection(host=None, port=None, password=None, db=0, use_pool=True, decode_responses=True):
    """
    Establishes and returns a Redis client instance.

    This function provides a consistent way to connect to Redis. It can use a
    shared connection pool for efficiency in applications making many short-lived
    connections.

    Args:
        host (str, optional): Redis server host. Defaults to REDIS_HOST env var or 'localhost'.
        port (int, optional): Redis server port. Defaults to REDIS_PORT env var or 6379.
        password (str, optional): Redis password. Defaults to REDIS_PASSWORD env var or None.
        db (int, optional): Redis database index to use. Defaults to 0.
        use_pool (bool, optional): If True, uses a shared connection pool. If False, creates
                                a new direct connection. Defaults to True.
        decode_responses (bool, optional): If True, responses from Redis are decoded
                                        from bytes to UTF-8 strings. Defaults to True.

    Returns:
        redis.Redis or None: A connected Redis client instance, or None if connection fails.
    """
    global _connection_pool

    # Resolve connection parameters, prioritizing arguments over environment variables.
    resolved_host = host or os.getenv('REDIS_HOST', 'localhost')
    resolved_port = int(port or os.getenv('REDIS_PORT', 6379))
    resolved_password = password or os.getenv('REDIS_PASSWORD', None)

    if use_pool:
        # Check if the pool needs to be created or recreated. This happens if the pool
        # doesn't exist or if the connection parameters have changed since it was created.
        pool_kwargs = _connection_pool.connection_kwargs if _connection_pool else {}
        if not _connection_pool or \
           pool_kwargs.get('host') != resolved_host or \
           pool_kwargs.get('port') != resolved_port or \
           pool_kwargs.get('password') != resolved_password or \
           pool_kwargs.get('db') != db:
            
            try:
                _connection_pool = redis.ConnectionPool(
                    host=resolved_host,
                    port=resolved_port,
                    password=resolved_password,
                    db=db,
                    decode_responses=decode_responses,
                    socket_connect_timeout=2,  # seconds
                    socket_timeout=2           # seconds
                )
            except Exception as e:
                print(f"Error: Could not create Redis connection pool for {resolved_host}:{resolved_port}. {e}", file=sys.stderr)
                return None

        return redis.Redis(connection_pool=_connection_pool)
    else:
        # Create a direct, non-pooled connection.
        try:
            r = redis.Redis(
                host=resolved_host,
                port=resolved_port,
                password=resolved_password,
                db=db,
                decode_responses=decode_responses,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            r.ping()  # Verify the connection is active.
            return r
        except redis.exceptions.AuthenticationError as e:
            print(f"Error: Authentication failed for Redis at {resolved_host}:{resolved_port}. {e}", file=sys.stderr)
            return None
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            print(f"Error: Could not connect to Redis at {resolved_host}:{resolved_port}. {e}", file=sys.stderr)
            return None