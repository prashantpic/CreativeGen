"""
Abstract base class for push notification providers.

This module defines the interface that all push notification provider clients
(e.g., APNS, FCM) must implement. This abstraction allows the PushNotificationService
to interact with different providers through a consistent contract, following the
Strategy and Adapter design patterns.
"""
from abc import ABC, abstractmethod

from creativeflow.services.notification.core.schemas import PushNotificationContent


class BasePushProvider(ABC):
    """
    Abstract interface for a push notification provider.

    Concrete implementations of this class will handle the specifics of
    communicating with a particular push service like APNS or FCM.
    """

    @abstractmethod
    async def send(self, device_token: str, payload: PushNotificationContent) -> None:
        """
        Sends a push notification to a specific device.

        Args:
            device_token: The unique token identifying the target device.
            payload: A structured object containing the notification content.

        Raises:
            PushProviderError: If the provider fails to send the notification.
        """
        pass