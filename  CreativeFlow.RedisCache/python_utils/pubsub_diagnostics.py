#
# CreativeFlow.RedisCache - pubsub_diagnostics.py
#
# Provides diagnostic tools for administrators to monitor Redis Pub/Sub channels,
# which are crucial for the Notification Service.
#

from .redis_connector import get_redis_connection

class PubSubAdmin:
    """A collection of tools for diagnosing Redis Pub/Sub functionality."""

    def __init__(self, redis_host=None, redis_port=None, redis_password=None, pubsub_db_index=2):
        """
        Initializes the Pub/Sub admin tools.

        Note: PUBSUB commands are not tied to a specific database index; they are global
        to the Redis instance. The `pubsub_db_index` is used for connector consistency
        if other commands were to be added to this tool.

        Args:
            redis_host (str, optional): Redis server host.
            redis_port (int, optional): Redis server port.
            redis_password (str, optional): Redis server password.
            pubsub_db_index (int, optional): A Redis DB index for the connector. Defaults to 2.
        
        Raises:
            ConnectionError: If a connection to Redis cannot be established.
        """
        self.redis_client = get_redis_connection(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=pubsub_db_index,
            use_pool=False
        )
        if not self.redis_client:
            raise ConnectionError("Failed to connect to Redis for PubSubAdmin.")

    def list_active_channels(self, pattern="*"):
        """
        Lists active Pub/Sub channels, optionally matching a pattern.

        Args:
            pattern (str, optional): A glob-style pattern to match channel names. Defaults to "*".

        Returns:
            list: A list of active channel names.
        """
        try:
            return self.redis_client.pubsub_channels(pattern=pattern)
        except Exception as e:
            print(f"Error listing active channels with pattern '{pattern}': {e}")
            return []

    def get_channel_subscriber_count(self, channel_name):
        """
        Gets the number of subscribers for one or more specific channels.

        Args:
            channel_name (str or list): A single channel name or a list of channel names.

        Returns:
            dict or None: A dictionary mapping channel names to their subscriber counts, or None on error.
                          If a single channel name string is passed, returns an int.
        """
        try:
            # PUBSUB NUMSUB returns a list of [channel, count, channel2, count2, ...]
            is_single = isinstance(channel_name, str)
            channels = [channel_name] if is_single else channel_name
            
            result = self.redis_client.pubsub_numsub(*channels)
            
            # Convert the flat list [ch1, count1, ch2, count2] to a dict {ch1: count1, ...}
            sub_counts = {result[i]: result[i+1] for i in range(0, len(result), 2)}

            if is_single:
                return sub_counts.get(channel_name, 0)
            return sub_counts
        except Exception as e:
            print(f"Error getting subscriber count for channel(s) '{channel_name}': {e}")
            return None

    def publish_test_message(self, channel_name, message="This is a test message from PubSubAdmin."):
        """
        Publishes a test message to a specified channel for diagnostic purposes.

        Args:
            channel_name (str): The name of the channel to publish to.
            message (str, optional): The message to send.

        Returns:
            int or None: The number of clients that received the message, or None on error.
        """
        try:
            return self.redis_client.publish(channel_name, message)
        except Exception as e:
            print(f"Error publishing test message to channel '{channel_name}': {e}")
            return None