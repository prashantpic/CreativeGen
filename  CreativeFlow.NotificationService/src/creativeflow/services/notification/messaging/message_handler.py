"""
Unified message handler for processing messages from message brokers.

This module provides the `MessageHandler` class, which is responsible for
decoding, parsing, and validating incoming raw messages from sources like
RabbitMQ or Redis. Once a message is validated against the `NotificationPayload`
schema, it is forwarded to the `NotificationManager` for dispatching.
"""
import json
from typing import Union

from pydantic import ValidationError

from creativeflow.services.notification.core.notification_manager import NotificationManager
from creativeflow.services.notification.core.schemas import NotificationPayload
from creativeflow.services.notification.shared.exceptions import InvalidMessageFormatError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class MessageHandler:
    """
    Processes raw messages from queues, validates them, and triggers notifications.
    """

    def __init__(self, notification_manager: NotificationManager):
        """
        Initializes the MessageHandler.

        Args:
            notification_manager: An instance of the central NotificationManager.
        """
        self.notification_manager = notification_manager

    async def handle_message(self, raw_message_body: Union[bytes, str], message_source: str):
        """
        Parses, validates, and processes a single message.

        Args:
            raw_message_body: The raw message content from the queue.
            message_source: A string indicating the origin (e.g., 'RabbitMQ', 'Redis Pub/Sub').

        Raises:
            InvalidMessageFormatError: If the message is malformed or fails validation.
        """
        logger.debug(f"Received message from {message_source}: {raw_message_body!r}")
        try:
            decoded_body = raw_message_body.decode('utf-8') if isinstance(raw_message_body, bytes) else raw_message_body
            message_data = json.loads(decoded_body)
            payload = NotificationPayload(**message_data)

        except (json.JSONDecodeError, ValidationError) as e:
            error_msg = f"Failed to parse or validate message from {message_source}: {e}"
            logger.error(f"{error_msg}. Message body: {raw_message_body!r}")
            # Raise exception to allow the consumer to NACK the message
            raise InvalidMessageFormatError(error_msg)
        
        except Exception as e:
            error_msg = f"An unexpected error occurred while processing message from {message_source}: {e}"
            logger.exception(error_msg)
            raise InvalidMessageFormatError(error_msg)

        # If parsing and validation succeed, dispatch the notification.
        await self.notification_manager.send_notification(payload)