import pika
import json
import logging
from typing import Dict, Any

from creativeflow.services.aigeneration.core.error_handlers import GenerationJobPublishError

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    A client for publishing messages (generation jobs) to RabbitMQ.
    Handles connection management and durable message publishing.
    
    Note: This implementation uses the synchronous `pika.BlockingConnection`.
    For a fully non-blocking async application, consider using a library like `aio-pika`
    or running this blocking code in a separate thread pool. For simplicity in this
    context, we assume calls are fast enough or the trade-off is acceptable.
    """

    def __init__(self, amqp_url: str, exchange_name: str, queue_name: str, routing_key: str):
        self._amqp_url = amqp_url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._routing_key = routing_key
        self._connection = None
        self._channel = None

    def connect(self):
        """Establishes a connection and channel to RabbitMQ."""
        if self._connection and self._connection.is_open:
            logger.debug("RabbitMQ connection is already open.")
            return

        try:
            logger.info("Connecting to RabbitMQ...")
            params = pika.URLParameters(self._amqp_url)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            self._setup_broker()
            logger.info("Successfully connected to RabbitMQ and set up broker objects.")
        except Exception as e:
            logger.exception("Could not connect to RabbitMQ.")
            self._connection = None
            self._channel = None
            raise ConnectionError("Failed to establish RabbitMQ connection.") from e

    def _setup_broker(self):
        """Declares the necessary exchange and queue, and binds them."""
        if not self._channel:
            raise ConnectionError("Cannot set up broker, channel is not available.")
            
        # Declare a durable, direct exchange
        logger.info(f"Declaring exchange '{self._exchange_name}'...")
        self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type='direct',
            durable=True
        )
        
        # Declare a durable queue
        logger.info(f"Declaring queue '{self._queue_name}'...")
        self._channel.queue_declare(
            queue=self._queue_name,
            durable=True
        )
        
        # Bind the queue to the exchange with the routing key
        logger.info(f"Binding queue '{self._queue_name}' to exchange '{self._exchange_name}' with key '{self._routing_key}'...")
        self._channel.queue_bind(
            queue=self._queue_name,
            exchange=self._exchange_name,
            routing_key=self._routing_key
        )

    def publish_generation_job(self, job_payload: Dict[str, Any]):
        """

        Publishes a generation job payload to the configured RabbitMQ exchange.
        Ensures the message is persistent.
        """
        if not self._channel or not self._connection or not self._connection.is_open:
            logger.warning("RabbitMQ connection not available. Attempting to reconnect...")
            self.connect()

        try:
            message_body = json.dumps(job_payload, default=str) # Use default=str to handle UUIDs, datetimes etc.

            self._channel.basic_publish(
                exchange=self._exchange_name,
                routing_key=self._routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            request_id = job_payload.get("generation_request_id", "N/A")
            logger.info(f"Successfully published message for request ID {request_id}")

        except Exception as e:
            logger.exception("Failed to publish message to RabbitMQ.")
            # In a real-world scenario, you might want to implement a retry mechanism.
            raise GenerationJobPublishError("Failed to publish generation job to the message queue.") from e

    def close(self):
        """Closes the connection to RabbitMQ."""
        if self._connection and self._connection.is_open:
            logger.info("Closing RabbitMQ connection.")
            try:
                self._connection.close()
            except Exception as e:
                logger.error(f"Error while closing RabbitMQ connection: {e}")
        self._connection = None
        self._channel = None