import json
import logging
import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker
import time

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    Client for publishing messages (generation jobs) to RabbitMQ.
    
    Note: `pika` is a blocking library. In a high-throughput async application,
    it's recommended to use an async-native library like `aio_pika` or run
    these blocking operations in a thread pool executor.
    This implementation uses a simple blocking connection management for clarity.
    """
    _instance = None
    
    def __init__(self, rabbitmq_url: str):
        self._rabbitmq_url = rabbitmq_url
        self._connection = None
        self._channel = None
        self.connect()

    @classmethod
    def get_instance(cls):
        """Singleton pattern to manage a single publisher instance."""
        if cls._instance is None:
            cls._instance = cls(rabbitmq_url=settings.RABBITMQ_URL)
        return cls._instance

    def connect(self):
        """Establishes a connection to RabbitMQ and creates a channel."""
        if self.is_connected():
            logger.debug("RabbitMQ connection already active.")
            return

        logger.info("Connecting to RabbitMQ...")
        params = pika.URLParameters(self._rabbitmq_url)
        try:
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            logger.info("Successfully connected to RabbitMQ.")
            self.setup_exchange(settings.RABBITMQ_GENERATION_EXCHANGE)
        except AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self._connection = None
            self._channel = None
            raise

    def is_connected(self) -> bool:
        """Checks if the connection and channel are open."""
        return self._connection is not None and self._connection.is_open and \
               self._channel is not None and self._channel.is_open

    def setup_exchange(self, exchange_name: str):
        """Declares a durable exchange."""
        if not self.is_connected():
            self.connect()
        logger.info(f"Declaring RabbitMQ exchange '{exchange_name}'...")
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )

    async def publish_generation_job(self, job_payload: dict) -> None:
        """
        Publishes a generation job to RabbitMQ.
        Handles connection retries.
        """
        if not self.is_connected():
            try:
                self.connect()
            except Exception as e:
                logger.error("RabbitMQ connection failed on publish attempt. Cannot publish message.", exc_info=True)
                raise ConnectionError("Failed to connect to RabbitMQ to publish job.") from e

        message_body = json.dumps(job_payload, default=str)
        request_id = job_payload.get('generation_request_id', 'N/A')
        logger.info(f"Publishing job for request {request_id} to exchange '{settings.RABBITMQ_GENERATION_EXCHANGE}' with routing key '{settings.RABBITMQ_N8N_JOB_ROUTING_KEY}'")

        try:
            self._channel.basic_publish(
                exchange=settings.RABBITMQ_GENERATION_EXCHANGE,
                routing_key=settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    content_type='application/json'
                )
            )
            logger.debug(f"Successfully published job for request {request_id}.")
        except (ChannelClosedByBroker, AMQPConnectionError) as e:
            logger.error(f"RabbitMQ connection lost while publishing. Attempting to reconnect. Error: {e}")
            self.close()
            self.connect()
            # Retry publishing after reconnecting
            self._channel.basic_publish(
                exchange=settings.RABBITMQ_GENERATION_EXCHANGE,
                routing_key=settings.RABBITMQ_N8N_JOB_ROUTING_KEY,
                body=message_body,
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
            logger.info(f"Successfully published job for request {request_id} after reconnecting.")
        except Exception as e:
            logger.critical(f"An unexpected error occurred during RabbitMQ publish for request {request_id}", exc_info=True)
            raise

    def close(self):
        """Closes the connection to RabbitMQ."""
        if self._connection and self._connection.is_open:
            logger.info("Closing RabbitMQ connection.")
            self._connection.close()
        self._connection = None
        self._channel = None