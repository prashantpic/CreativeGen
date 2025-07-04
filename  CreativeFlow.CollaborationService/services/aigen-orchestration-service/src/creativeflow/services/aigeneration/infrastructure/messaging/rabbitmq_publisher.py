import pika
import json
import logging
from typing import Dict, Any

from creativeflow.services.aigeneration.core.config import Settings
from creativeflow.services.aigeneration.core.error_handlers import GenerationJobPublishError

logger = logging.getLogger(__name__)

# NOTE: The 'pika' library's BlockingConnection is not inherently async-friendly or thread-safe.
# For a high-concurrency FastAPI service, 'aio-pika' is a much better choice.
# This implementation uses pika as specified and manages the connection state simply.
# The connection is established on startup and closed on shutdown (managed in main.py).

class RabbitMQPublisher:
    """
    Client for publishing messages (generation jobs) to RabbitMQ.
    """
    def __init__(self, settings: Settings):
        self._settings = settings
        self._connection: pika.BlockingConnection = None
        self._channel: pika.channel.Channel = None
        self.is_connected = False

    def connect(self) -> None:
        """
        Establishes a connection to RabbitMQ and declares the exchange.
        This should be called at application startup.
        """
        if self.is_connected and self._connection and self._connection.is_open:
            logger.info("RabbitMQ connection already established.")
            return

        try:
            logger.info(f"Connecting to RabbitMQ at {self._settings.RABBITMQ_URL}...")
            params = pika.URLParameters(self._settings.RABBITMQ_URL)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            
            logger.info("Declaring RabbitMQ exchange...")
            self._channel.exchange_declare(
                exchange=self._settings.RABBITMQ_GENERATION_EXCHANGE,
                exchange_type='direct',
                durable=True
            )
            self.is_connected = True
            logger.info(f"RabbitMQ connection successful. Exchange '{self._settings.RABBITMQ_GENERATION_EXCHANGE}' is ready.")
        except pika.exceptions.AMQPConnectionError as e:
            logger.critical(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            self.is_connected = False
            # In a real app, you might want a retry mechanism here.
            raise ConnectionError("Could not connect to RabbitMQ.") from e

    def close(self) -> None:
        """
        Gracefully closes the connection to RabbitMQ.
        This should be called at application shutdown.
        """
        if self._connection and self._connection.is_open:
            logger.info("Closing RabbitMQ connection.")
            self._connection.close()
        self.is_connected = False

    def publish_generation_job(self, job_payload: Dict[str, Any]) -> None:
        """
        Publishes a generation job payload to the configured RabbitMQ exchange.

        :param job_payload: A dictionary representing the job to be sent.
        :raises GenerationJobPublishError: If the message cannot be published.
        """
        if not self.is_connected or not self._channel or not self._channel.is_open:
            logger.error("Cannot publish message: RabbitMQ is not connected. Attempting to reconnect.")
            try:
                self.connect()
            except ConnectionError as e:
                raise GenerationJobPublishError("RabbitMQ is disconnected and reconnect failed.") from e

        try:
            message_body = json.dumps(job_payload, default=str) # Use default=str to handle UUID, datetime etc.

            self._channel.basic_publish(
                exchange=self._settings.RABBITMQ_GENERATION_EXCHANGE,
                routing_key=self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # Make message persistent
                    content_type='application/json',
                )
            )
            logger.info(f"Published job for request_id '{job_payload.get('generation_request_id')}' with routing key '{self._settings.RABBITMQ_N8N_JOB_ROUTING_KEY}'")
        except (pika.exceptions.UnroutableError, pika.exceptions.AMQPChannelError, Exception) as e:
            logger.critical(f"Failed to publish message to RabbitMQ: {e}", exc_info=True)
            # Potentially try to reconnect and retry here, or just fail fast.
            raise GenerationJobPublishError(f"Failed to publish message: {e}") from e