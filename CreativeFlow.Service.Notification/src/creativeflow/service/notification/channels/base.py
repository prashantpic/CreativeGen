from abc import ABC, abstractmethod
from typing import Any, Dict
from creativeflow.service.notification.shared.schemas import NotificationPayload

class NotificationChannel(ABC):
    """
    Abstract Base Class for a notification channel.

    This class defines the common interface that all notification channel
    implementations (e.g., WebSocket, Push, Email) must adhere to.
    This enforces the Strategy Pattern, allowing the NotificationDispatcher
    to use any channel polymorphically.
    """

    @abstractmethod
    async def send(self, payload: NotificationPayload) -> None:
        """
        Sends a notification through the specific channel.

        Args:
            payload: A validated data object containing the recipient's user ID,
                     device information, and the message content.
        
        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError