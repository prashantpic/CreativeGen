#
# CreativeFlow.RedisCache - session_utils.py
#
# Provides administrative and diagnostic utilities for managing user sessions
# stored in Redis. These tools are intended for use by system administrators
# via CLI or scripts, not for the main application's session handling logic.
#

import json
from .redis_connector import get_redis_connection

class SessionAdminTools:
    """A collection of tools for administering user sessions in Redis."""

    def __init__(self, redis_host=None, redis_port=None, redis_password=None, session_db_index=0):
        """
        Initializes the session admin tools.

        Args:
            redis_host (str, optional): Redis server host.
            redis_port (int, optional): Redis server port.
            redis_password (str, optional): Redis server password.
            session_db_index (int, optional): The Redis DB index where sessions are stored. Defaults to 0.
        
        Raises:
            ConnectionError: If a connection to Redis cannot be established.
        """
        self.redis_client = get_redis_connection(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=session_db_index,
            use_pool=False  # For admin tools, direct connection is simpler and safer
        )
        if not self.redis_client:
            raise ConnectionError("Failed to connect to Redis for SessionAdminTools.")

    def count_active_sessions(self, session_key_prefix="session:"):
        """
        Counts active sessions by scanning for keys with a given prefix.
        Uses SCAN for performance and safety in production environments.

        Args:
            session_key_prefix (str, optional): The prefix for session keys. Defaults to "session:".

        Returns:
            int: The total number of active sessions found.
        """
        count = 0
        # SCAN is an iterator, which is memory-efficient for large key spaces.
        for _ in self.redis_client.scan_iter(match=f"{session_key_prefix}*"):
            count += 1
        return count

    def get_session_details(self, session_id_full_key):
        """
        Retrieves and attempts to decode session data for a given full session key.

        Args:
            session_id_full_key (str): The full Redis key for the session (e.g., "session:user-123-abc").

        Returns:
            dict or str or None: The decoded session data (if JSON), the raw string data, or None if the key does not exist.
        """
        try:
            session_data_raw = self.redis_client.get(session_id_full_key)
            if session_data_raw:
                try:
                    # Attempt to decode as JSON, as this is a common format for session data.
                    return json.loads(session_data_raw)
                except json.JSONDecodeError:
                    # If not JSON, return the raw data as a string.
                    return session_data_raw
            return None
        except Exception as e:
            print(f"Error getting session details for {session_id_full_key}: {e}")
            return None

    def list_sessions_by_pattern(self, pattern="session:*", count=100):
        """
        Lists session keys matching a pattern, using SCAN for safety.

        Args:
            pattern (str, optional): The glob-style pattern to match. Defaults to "session:*".
            count (int, optional): The approximate number of keys to return. Set to 0 for all keys (use with caution).

        Returns:
            list: A list of session keys matching the pattern.
        """
        sessions = []
        # Use scan_iter for a memory-efficient way to get all keys if count is 0.
        if count == 0:
            return list(self.redis_client.scan_iter(match=pattern))
        
        # Otherwise, use SCAN with a limit.
        cursor = '0'
        while cursor != 0:
            cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern, count=count)
            sessions.extend(keys)
            if len(sessions) >= count:
                break
        return sessions[:count]

    def clear_session(self, session_id_full_key):
        """
        Deletes a specific session by its full key.

        Args:
            session_id_full_key (str): The full Redis key of the session to delete.

        Returns:
            bool: True if the session was deleted, False otherwise.
        """
        try:
            deleted_count = self.redis_client.delete(session_id_full_key)
            return deleted_count > 0
        except Exception as e:
            print(f"Error clearing session {session_id_full_key}: {e}")
            return False

# Example usage block for testing or direct CLI interaction.
if __name__ == '__main__':
    print("--- Session Admin Tools Example ---")
    try:
        # Assumes Redis is running locally on the default port without a password.
        admin_tools = SessionAdminTools()
        print(f"Connected to Redis DB {admin_tools.redis_client.connection_pool.connection_kwargs['db']}")

        # Setup some test data
        test_session_key = "session:test-user-123"
        test_session_data = json.dumps({"user_id": "123", "role": "admin", "login_time": "2023-10-27T10:00:00Z"})
        admin_tools.redis_client.set(test_session_key, test_session_data, ex=300) # 5-min expiry
        print(f"\nCreated test session: {test_session_key}")

        # Count sessions
        total_sessions = admin_tools.count_active_sessions()
        print(f"Total active sessions found: {total_sessions}")
        
        # List some sessions
        some_sessions = admin_tools.list_sessions_by_pattern(count=5)
        print(f"\nListing up to 5 session keys: {some_sessions}")
        
        # Get details for the test session
        if test_session_key in some_sessions:
            details = admin_tools.get_session_details(test_session_key)
            print(f"\nDetails for '{test_session_key}': {details}")
            
        # Clear the test session
        print(f"\nClearing session '{test_session_key}'...")
        was_cleared = admin_tools.clear_session(test_session_key)
        print(f"Session cleared successfully: {was_cleared}")
        
        details_after_clear = admin_tools.get_session_details(test_session_key)
        print(f"Details for '{test_session_key}' after clearing: {details_after_clear}")

    except ConnectionError as e:
        print(f"\nCould not run example: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")