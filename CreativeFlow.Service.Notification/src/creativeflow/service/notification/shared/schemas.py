from pydantic import BaseModel, Field
from typing import Dict, Any, Literal, List

class RecipientDevice(BaseModel):
    """
    Represents a single device token for push notifications.
    This schema ensures that device information is strongly typed, preventing
    errors when routing to different push notification providers.
    """
    platform: Literal["apns", "fcm"] = Field(..., description="The target push notification platform.")
    token: str = Field(..., description="The unique device token provided by the platform.")

class NotificationPayload(BaseModel):
    """
    The main Data Transfer Object (DTO) for messages consumed from the message queue.
    
    This schema defines the formal contract for all events that can trigger a notification.
    It ensures that incoming messages are well-structured and valid before processing,
    decoupling the notification service from the internal data structures of its producers.
    """
    user_id: str = Field(..., description="The unique identifier of the recipient user.")
    event_type: str = Field(..., description="The type of event, e.g., 'ai.generation.completed'.")
    devices: List[RecipientDevice] = Field(
        default=[], 
        description="A list of recipient devices for mobile push notifications. Can be empty."
    )
    data: Dict[str, Any] = Field(..., description="The actual message content and metadata.")

    # Example `data` for event_type 'ai.generation.completed':
    # { 
    #   "title": "Generation Complete!",
    #   "message": "Your creative 'My First Ad' is ready!", 
    #   "project_id": "uuid-goes-here", 
    #   "asset_url": "https://storage/path/to/asset.png" 
    # }
    
    # Example `data` for event_type 'collaboration.update':
    # { 
    #   "title": "New Comment",
    #   "message": "User Jane Doe commented on Project 'Summer Campaign'",
    #   "project_id": "uuid-goes-here", 
    #   "updated_by": "Jane Doe"
    # }