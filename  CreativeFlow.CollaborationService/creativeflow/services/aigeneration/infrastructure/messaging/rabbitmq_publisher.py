import json
import logging
import pika
from pika.exceptions import AMQPConnectionError, ChannelError

from creativeflow.services.aigeneration.application.exceptions import GenerationJobPublishError

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    A client for publishing messages (generation jobs) to RabbitMQ.
    Note: The 'pika' library is blocking. For a high-performance asyncio application,
    'aio-pika' would be a better choice. This implementation uses 'pika' as specified
    and is suitable for scenarios where publishing latency is not the primary bottleneck.
    Connection management (connect/close) should be handled by the application's
    lifespan events.
    """

    def __init__(self, amqp_url: str):
        self._amqp_url = amqp_url
        self._connection: pika.BlockingConnection | None = None
        self._channel: pika.channel.Channel | None = None

    def connect(self):
        """Establishes a connection and a channel to RabbitMQ."""
        if self._connection and self._connection.is_open:
            return
        try:
            logger.info("Connecting to RabbitMQ at %s", self._amqp_url)
            self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
            self._channel = self._connection.channel()
            logger.info("Successfully connected to RabbitMQ.")
        except AMQPConnectionError as e:
            logger.critical("Failed to connect to RabbitMQ: %s", e)
            raise ConnectionError("Could not establish connection to RabbitMQ.") from e

    def close(self):
        """Closes the connection to RabbitMQ."""
        if self._channel and self._channel.is_open:
            self._channel.close()
        if self._connection and self._connection.is_open:
            self._connection.close()
        logger.info("RabbitMQ connection closed.")

    def publish_generation_job(self, job_payload: dict, routing_key: str, exchange_name: str):
        """
        Publishes a generation job payload to the specified exchange.

        :param job_payload: A dictionary representing the job.
        :param routing_key: The routing key for the message.
        :param exchange_name: The name of the exchange to publish to.
        :raises GenerationJobPublishError: If publishing fails.
        """
        if not self._channel or not self._connection or not self._connection.is_open:
            logger.error("Cannot publish message, RabbitMQ connection is not open.")
            raise GenerationJobPublishError("RabbitMQ connection is not available.")

        try:
            # Declare the exchange to ensure it exists. Type 'direct' is a common choice.
            self._channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
            
            # Serialize payload to JSON string
            message_body = json.dumps(job_payload, ensure_ascii=False)

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
            logger.info(
                "Successfully published job with ID %s to exchange '%s' with routing key '%s'.",
                job_payload.get('generation_request_id'), exchange_name, routing_key
            )
        except (ChannelError, AMQPConnectionError) as e:
            logger.error(
                "Failed to publish job to RabbitMQ for request ID %s: %s",
                job_payload.get('generation_request_id'), e, exc_info=True
            )
            # A real-world app might attempt to reconnect here.
            raise GenerationJobPublishError(f"Failed to publish message to RabbitMQ: {e}") from e
        except Exception as e:
            logger.error(
                "An unexpected error occurred during message publishing for request ID %s: %s",
                job_payload.get('generation_request_id'), e, exc_info=True
            )
            raise GenerationJobPublishError(f"An unexpected error occurred during publishing: {e}") from e