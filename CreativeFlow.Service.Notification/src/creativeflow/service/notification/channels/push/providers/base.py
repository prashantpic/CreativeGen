from abc import ABC, abstractmethod
from typing import Any, Dict

class PushProvider(ABC):
    """
    Abstract Base Class for a push notification provider.

    This class defines the common interface for third-party push notification
    services like Apple Push Notification Service (APNS) and Firebase Cloud
    Messaging (FCM). This enforces the Adapter Pattern, decoupling the
    PushNotificationChannel from the specific SDKs and APIs of each provider.
    """

    @abstractmethod
    async def send_push(self, device_token: str, title: str, body: str, data: Dict[str, Any]) -> None:
        """
        Sends a single push notification to a specific device.

        Args:
            device_token: The unique token identifying the target device.
            title: The title of the push notification.
            body: The main message body of the push notification.
            data: A dictionary of custom data to be sent with the notification.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError