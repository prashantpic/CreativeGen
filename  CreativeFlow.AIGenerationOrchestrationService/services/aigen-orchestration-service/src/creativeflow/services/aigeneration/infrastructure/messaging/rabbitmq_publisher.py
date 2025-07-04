import json
import logging
import pika
import time
from typing import Optional

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """
    Client for publishing messages (generation jobs) to RabbitMQ.
    Encapsulates the logic for connecting to RabbitMQ and publishing messages.
    
    Note: This implementation uses the blocking `pika` library. In a fully async
    application using a library like `aio-pika` is preferred. If using `pika`,
    publishing methods should be run in a separate thread to avoid blocking
    the main asyncio event loop (e.g., via `asyncio.to_thread`).
    """
    def __init__(self, connection_url: str):
        self._connection_url = connection_url
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
        self.is_connected = False

    def connect(self):
        """

        Establishes a connection to the RabbitMQ server and creates a channel.
        This method is blocking and should be called at application startup.
        """
        if self.is_connected and self._connection and self._connection.is_open:
            logger.info("RabbitMQ connection is already active.")
            return

        logger.info("Connecting to RabbitMQ...")
        try:
            params = pika.URLParameters(self._connection_url)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            self.is_connected = True
            logger.info("Successfully connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            self.is_connected = False
            raise

    def _ensure_connection(self):
        """Ensures the connection is active, trying to reconnect if necessary."""
        if self.is_connected and self._channel and self._channel.is_open:
            return
        
        logger.warning("RabbitMQ connection lost. Attempting to reconnect...")
        self.is_connected = False
        self.connect() # This will raise an exception if reconnect fails

    def publish_generation_job(self, job_payload: dict, routing_key: str, exchange_name: str):
        """
        Publishes a generation job message to a specific exchange.

        Args:
            job_payload: A dictionary representing the job parameters.
            routing_key: The routing key for the message.
            exchange_name: The name of the exchange to publish to.
        """
        if not self.is_connected:
            logger.error("Cannot publish job, RabbitMQ is not connected.")
            raise ConnectionError("RabbitMQ publisher is not connected.")

        try:
            self._ensure_connection()
            
            # Declare the exchange (idempotent operation)
            self._channel.exchange_declare(
                exchange=exchange_name,
                exchange_type='direct',
                durable=True
            )

            message_body = json.dumps(job_payload, default=str)
            
            self._channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    content_type='application/json'
                )
            )
            logger.info(f"Published message to exchange '{exchange_name}' with routing key '{routing_key}'.")
        except (pika.exceptions.AMQPError, ConnectionError) as e:
            logger.error(f"Failed to publish message to RabbitMQ: {e}", exc_info=True)
            self.is_connected = False # Mark as disconnected to force reconnect on next call
            raise
    
    def close(self):
        """
        Gracefully closes the channel and connection to RabbitMQ.
        This should be called at application shutdown.
        """
        if self._connection and self._connection.is_open:
            logger.info("Closing RabbitMQ connection.")
            try:
                self._connection.close()
                self.is_connected = False
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}", exc_info=True)
        else:
            logger.info("RabbitMQ connection already closed.")