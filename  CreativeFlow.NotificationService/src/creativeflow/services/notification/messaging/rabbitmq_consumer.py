"""
RabbitMQ message consumer using the `pika` library.

This module provides a class to connect to a RabbitMQ broker, consume messages
from a specified queue, and process them. It is designed to run in a separate
thread to avoid blocking the main application's async event loop.
"""
import asyncio
import threading
import time

import pika
from pika.exceptions import AMQPConnectionError

from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.messaging.message_handler import MessageHandler
from creativeflow.services.notification.shared.exceptions import InvalidMessageFormatError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class RabbitMQConsumer:
    """
    Consumes messages from a RabbitMQ queue and processes them.
    """

    def __init__(self, config: Settings, message_handler: MessageHandler):
        """
        Initializes the RabbitMQConsumer.

        Args:
            config: The application settings.
            message_handler: The message handler for processing messages.
        """
        self.config = config
        self.message_handler = message_handler
        self.connection = None
        self.channel = None
        self._stopping = False

    def _connect(self):
        """Establishes a connection to RabbitMQ with retry logic."""
        retry_delay = 5
        while not self._stopping:
            try:
                logger.info(f"Attempting to connect to RabbitMQ at {self.config.RABBITMQ_URL}")
                params = pika.URLParameters(self.config.RABBITMQ_URL)
                self.connection = pika.BlockingConnection(params)
                self.channel = self.connection.channel()
                logger.info("RabbitMQ connection established successfully.")
                return True
            except AMQPConnectionError as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        return False

    def _setup_channel_and_queue(self, queue_name: str):
        """Declares the queue, ensuring it exists and is durable."""
        if self.channel:
            self.channel.queue_declare(queue=queue_name, durable=True)
            logger.info(f"Queue '{queue_name}' declared as durable.")

    def _on_message_callback(self, ch, method, properties, body):
        """
        Callback executed when a message is received.
        It runs the async message handler and acks/nacks the message.
        """
        logger.debug(f"Received RabbitMQ message with delivery tag {method.delivery_tag}")
        try:
            # Since this callback is synchronous, we run our async handler in a new event loop.
            asyncio.run(self.message_handler.handle_message(body, "RabbitMQ"))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.debug(f"Successfully processed and ACKed message {method.delivery_tag}.")
        except InvalidMessageFormatError:
            logger.error(f"Invalid message format. NACKing message {method.delivery_tag} without requeue.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.exception(f"Unexpected error processing message {method.delivery_tag}. NACKing. Error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self, queue_name: str):
        """
        Starts the message consumption loop. This is a blocking method
        and should be run in a separate thread.
        """
        if not self.config.ENABLE_RABBITMQ_CONSUMER:
            logger.info("RabbitMQ consumer is disabled. Will not start.")
            return

        if not self._connect():
            return  # Could not connect, and stopping was signaled

        self._setup_channel_and_queue(queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self._on_message_callback)

        logger.info(f"Starting RabbitMQ consumer on queue: '{queue_name}'. Waiting for messages.")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Stopping consumer.")
        except Exception as e:
            logger.error(f"Consumer loop stopped unexpectedly: {e}")
        finally:
            if self.connection and self.connection.is_open:
                self.connection.close()
            logger.info("RabbitMQ consumer has stopped.")

    def stop_consuming(self):
        """Stops the consumer gracefully. Can be called from another thread."""
        if not self.config.ENABLE_RABBITMQ_CONSUMER:
            return
            
        logger.info("Stopping RabbitMQ consumer...")
        self._stopping = True
        if self.channel and self.channel.is_open:
            try:
                # This is thread-safe and will cause start_consuming() to exit
                self.channel.stop_consuming()
                logger.info("Consumer stopped.")
            except Exception as e:
                logger.error(f"Error while stopping consumer: {e}")

        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ connection closed.")