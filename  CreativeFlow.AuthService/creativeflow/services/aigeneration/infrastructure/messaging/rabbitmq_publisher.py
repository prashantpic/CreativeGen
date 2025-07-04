import logging
import json
import asyncio
import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    A client for publishing messages (generation jobs) to RabbitMQ.
    Note: `pika` is a synchronous library. In a fully async application, `aio_pika` would
    be a better choice. This implementation uses `run_in_executor` to avoid blocking
    the asyncio event loop for publishing.
    """

    def __init__(self, rabbitmq_url: str):
        self._rabbitmq_url = rabbitmq_url
        self._connection: pika.BlockingConnection = None
        self._channel: pika.channel.Channel = None

    async def connect(self):
        """Establishes connection to RabbitMQ. Should be called on application startup."""
        logger.info("Connecting to RabbitMQ...")
        try:
            loop = asyncio.get_running_loop()
            self._connection = await loop.run_in_executor(
                None, 
                lambda: pika.BlockingConnection(pika.URLParameters(self._rabbitmq_url))
            )
            self._channel = await loop.run_in_executor(
                None,
                lambda: self._connection.channel()
            )
            logger.info("Successfully connected to RabbitMQ and opened a channel.")
        except AMQPConnectionError as e:
            logger.critical(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            # In a real app, you might want a retry mechanism here.
            raise

    def is_connected(self) -> bool:
        """Checks if the connection to RabbitMQ is active."""
        return self._connection and self._connection.is_open and self._channel and self._channel.is_open

    async def publish_generation_job(self, job_payload: dict, routing_key: str, exchange_name: str):
        """
        Publishes a generation job payload to a specific exchange.
        This method is async and uses a thread pool to run the blocking pika code.
        """
        if not self.is_connected():
            logger.error("Cannot publish message, RabbitMQ is not connected. Attempting to reconnect.")
            await self.connect()

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None, 
                self._publish_sync, 
                exchange_name, 
                routing_key, 
                job_payload
            )
            logger.info(f"Successfully published job with routing key '{routing_key}' to exchange '{exchange_name}'.")
        except (AMQPConnectionError, ChannelClosedByBroker) as e:
            logger.error(f"RabbitMQ connection error during publish: {e}. Reconnecting...", exc_info=True)
            await self.connect()
            # Retry publishing once after reconnecting
            await loop.run_in_executor(
                None, self._publish_sync, exchange_name, routing_key, job_payload)
        except Exception as e:
            logger.critical(f"An unexpected error occurred during message publishing: {e}", exc_info=True)
            raise

    def _publish_sync(self, exchange_name, routing_key, job_payload):
        """The synchronous part of the publishing logic."""
        # Declare the exchange (idempotent operation)
        self._channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

        message_body = json.dumps(job_payload)

        # Publish the message
        self._channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # Make message persistent
                content_type='application/json'
            )
        )

    async def close(self):
        """Closes the RabbitMQ connection. Should be called on application shutdown."""
        if self.is_connected():
            logger.info("Closing RabbitMQ connection.")
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._connection.close)