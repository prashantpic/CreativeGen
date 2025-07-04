"""
Pydantic data models for the CreativeFlow Notification Service.

This module defines the data structures used for communication and internal processing.
These schemas ensure that all data flowing through the service is well-structured,
validated, and type-safe.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class NotificationPayload(BaseModel):
    """
    Represents the structure of a notification request received from a message queue.
    This is the canonical format that producers should use to send notifications.
    """
    user_id: str = Field(..., description="Target user for WebSocket, or for context if push.")
    event_type: str = Field(..., description="Type of event, e.g., 'ai_generation_progress'.")
    data: Dict[str, Any] = Field(..., description="The actual payload, flexible based on event_type.")
    target_channels: List[str] = Field(
        default_factory=list,
        description="List of target channels, e.g., ['websocket', 'push_ios', 'push_android']."
    )
    device_token: Optional[str] = Field(None, description="Device token for push notifications.")
    device_type: Optional[str] = Field(None, description="Device type ('ios' or 'android') for push notifications.")


class WebSocketMessage(BaseModel):
    """
    Represents the structure of a message sent to a client over a WebSocket connection.
    """
    type: str = Field(..., description="The event type to be handled by the frontend.")
    content: Dict[str, Any] = Field(..., description="The data associated with the event.")


class PushNotificationContent(BaseModel):
    """
    Represents a structured, provider-agnostic push notification message.
    This is used internally to construct provider-specific payloads.
    """
    title: Optional[str] = Field(None, description="The title of the push notification.")
    body: str = Field(..., description="The main text content of the push notification.")
    data: Optional[Dict[str, Any]] = Field(None, description="Custom data payload for the client app to handle.")
    deep_link_url: Optional[str] = Field(None, description="A deep link URL for the client app to open.")