import asyncio
import json
import logging
import aio_pika
import aio_pika.abc
from pydantic import ValidationError

from ..core.dispatcher import NotificationDispatcher
from ..shared.schemas import NotificationPayload

logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    """
    A robust RabbitMQ consumer for handling incoming notification events.

    This class manages the connection to RabbitMQ, consumes messages from a
    specified queue, and passes them to the NotificationDispatcher for processing.
    It includes logic for connection retries with exponential backoff to ensure
    resilience against broker unavailability.
    """
    def __init__(self, amqp_url: str, queue_name: str, dispatcher: NotificationDispatcher):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.dispatcher = dispatcher
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        logger.info(f"RabbitMQConsumer initialized for queue '{queue_name}'.")

    async def _on_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        """

        Callback to process a single message from the queue.
        It handles message parsing, validation, and dispatching.
        """
        async with message.process(ignore_processed=True): # auto-ack on success, nack on exception
            try:
                body = message.body.decode('utf-8')
                logger.debug(f"Received raw message: {body}")
                
                payload_dict = json.loads(body)
                payload = NotificationPayload.model_validate(payload_dict)
                
                logger.info(f"Successfully parsed message for user '{payload.user_id}', event '{payload.event_type}'.")
                await self.dispatcher.dispatch_notification(payload)

            except (json.JSONDecodeError, ValidationError) as e:
                logger.error(f"Message validation/parsing failed: {e}. Message will be rejected. Body: {message.body.decode(errors='ignore')}")
                # The context manager will automatically nack without requeueing
                # because an exception was raised. This prevents poison pills.
                await message.reject(requeue=False)

            except Exception as e:
                logger.critical(f"Unexpected error processing message: {e}", exc_info=True)
                # Reject but don't requeue to avoid potential processing loops
                await message.reject(requeue=False)

    async def run(self):
        """
        The main loop for the consumer.

        Connects to RabbitMQ and starts consuming messages. Includes a retry
        mechanism with exponential backoff to handle connection failures.
        """
        retry_delay = 5
        while True:
            try:
                logger.info(f"Attempting to connect to RabbitMQ at {self.amqp_url}")
                connection = await aio_pika.connect_robust(self.amqp_url)
                self._connection = connection

                async with connection:
                    logger.info("RabbitMQ connection successful.")
                    retry_delay = 5  # Reset delay on successful connection

                    channel = await connection.channel()
                    await channel.set_qos(prefetch_count=10) # Process up to 10 messages concurrently

                    queue = await channel.declare_queue(
                        self.queue_name, 
                        durable=True # Ensure queue survives broker restarts
                    )

                    logger.info(f"[*] Waiting for messages in queue '{self.queue_name}'. To exit press CTRL+C")
                    await queue.consume(self._on_message)
                    
                    # Keep the consumer running
                    await asyncio.Future()

            except asyncio.CancelledError:
                logger.info("Consumer run task cancelled. Shutting down.")
                break
            except Exception as e:
                logger.error(f"RabbitMQ connection failed: {e}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60) # Exponential backoff up to 60s
    
    async def stop(self):
        """Gracefully stops the consumer connection."""
        if self._connection and not self._connection.is_closed:
            logger.info("Closing RabbitMQ connection.")
            await self._connection.close()