"""
Custom exception classes for the CreativeFlow Notification Service.

This module defines a hierarchy of custom exceptions to allow for more granular
and meaningful error handling throughout the service. Using specific exceptions
improves code clarity and debugging by pinpointing the exact nature of an error.
"""
from typing import Any


class NotificationServiceError(Exception):
    """Base exception class for all errors in the notification service."""
    pass


class NotificationDispatchError(NotificationServiceError):
    """
    Raised when there is a general error dispatching a notification.
    This could be due to issues with channel selection or payload processing
    before sending to a specific provider.
    """
    pass


class PushProviderError(NotificationDispatchError):
    """
    Raised when a specific push notification provider (e.g., APNS, FCM)
    returns an error during a send operation.
    """
    def __init__(self, provider_name: str, original_error: Any):
        """
        Initializes the PushProviderError.

        Args:
            provider_name: The name of the push provider that failed (e.g., 'APNS', 'FCM').
            original_error: The underlying error or response from the provider's library.
        """
        self.provider_name = provider_name
        self.original_error = original_error
        message = f"Push provider '{provider_name}' failed with error: {original_error}"
        super().__init__(message)


class InvalidMessageFormatError(ValueError, NotificationServiceError):
    """

    Raised when an incoming message from a message broker (RabbitMQ, Redis)
    cannot be parsed, decoded, or validated against the expected schema.
    This helps in identifying malformed messages and preventing them from
    being processed repeatedly.
    """
    pass