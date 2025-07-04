# Software Design Specification (SDS) for CreativeFlow.Service.Notification

## 1. Introduction

### 1.1. Purpose

This document provides a detailed software design specification for the **CreativeFlow.Service.Notification** (`notification_service`). This microservice is a core component of the CreativeFlow AI platform, responsible for delivering real-time updates and asynchronous notifications to users across web and mobile platforms. It is designed to be highly available, scalable, and extensible to support various notification types and channels.

### 1.2. Scope

The scope of this service includes:
- Managing persistent WebSocket connections for web application clients.
- Consuming events from a central message broker (RabbitMQ).
- Dispatching notifications to the appropriate channel(s) based on the event payload and user preferences.
- Integrating with third-party push notification providers: Apple Push Notification Service (APNS) for iOS and Firebase Cloud Messaging (FCM) for Android.
- Providing a robust, decoupled, and scalable notification infrastructure.

## 2. System Architecture & Design

The service is built as a standalone Python FastAPI application. It follows a layered, event-driven architecture to ensure loose coupling and high performance.

### 2.1. Architectural Style

- **Microservice:** A self-contained service with a single responsibility: managing and delivering notifications.
- **Event-Driven:** The primary entry point for triggering notifications is through consuming events from a RabbitMQ message queue. This decouples the notification service from the event producers (e.g., AI Generation Service, Collaboration Service).

### 2.2. Key Design Patterns

- **Strategy Pattern:** Used for notification channels. A base `NotificationChannel` interface is defined, with concrete strategies for `WebSocketChannel` and `PushNotificationChannel`. This allows the `NotificationDispatcher` to select the appropriate channel at runtime without being coupled to its implementation.
- **Adapter Pattern:** Used for push notification providers. A base `PushProvider` interface abstracts the details of specific providers. Concrete `APNSProvider` and `FCMProvider` classes adapt this interface to the specific SDKs of APNS and FCM.
- **Singleton / Shared Instance:** Key manager classes like `ConnectionManager` and provider clients (APNS, FCM) will be instantiated once at application startup and shared across the application to manage state and resources efficiently.
- **Data Transfer Object (DTO):** Pydantic schemas are used as DTOs to define clear, validated data contracts for all incoming messages from the message queue, ensuring data integrity and a formal service interface.

## 3. Core Components & Logic

### 3.1. Configuration (`core/config.py`)

A Pydantic `Settings` class will manage all application configuration, loaded from environment variables.

python
# src/creativeflow/service/notification/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application configuration settings.
    """
    # Service
    LOG_LEVEL: str = "INFO"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    NOTIFICATION_QUEUE_NAME: str = "notification_events"

    # Apple Push Notification Service (APNS)
    APNS_ENABLED: bool = True
    APNS_KEY_ID: str
    APNS_TEAM_ID: str
    APNS_AUTH_KEY_PATH: str  # Path to the .p8 key file
    APNS_TOPIC: str          # Typically the app's bundle ID
    APNS_USE_SANDBOX: bool = False

    # Firebase Cloud Messaging (FCM)
    FCM_ENABLED: bool = True
    FCM_PROJECT_ID: str
    FCM_CREDENTIALS_PATH: str # Path to the service account JSON file

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()


### 3.2. Data Contracts (`shared/schemas.py`)

Pydantic models will define the structure of incoming event payloads from RabbitMQ.

python
# src/creativeflow/service/notification/shared/schemas.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Literal, List

class RecipientDevice(BaseModel):
    """
    Represents a single device for push notifications.
    """
    platform: Literal["apns", "fcm"]
    token: str

class NotificationPayload(BaseModel):
    """
    The main schema for messages consumed from the message queue.
    """
    user_id: str = Field(..., description="The unique identifier of the recipient user.")
    event_type: str = Field(..., description="The type of event, e.g., 'ai.generation.completed'.")
    devices: List[RecipientDevice] = Field([], description="List of devices for push notifications.")
    data: Dict[str, Any] = Field(..., description="The actual message content and metadata.")

    # Example `data` for event_type 'ai.generation.completed':
    # { "status": "success", "project_id": "...", "asset_url": "...", "message": "Your creative is ready!" }
    
    # Example `data` for event_type 'collaboration.update':
    # { "project_id": "...", "updated_by": "...", "message": "User X commented on Project Y" }


### 3.3. Notification Dispatcher (`core/dispatcher.py`)

The central orchestrator. It will receive a validated `NotificationPayload` and route it to the correct channel(s).

- **`NotificationDispatcher` class:**
    - `__init__(self, websocket_manager, apns_provider, fcm_provider)`: Initializes with instances of the connection manager and push providers.
    - `async def dispatch_notification(self, payload: NotificationPayload)`:
        1. Log the incoming notification request.
        2. **WebSocket Dispatch:** Call `websocket_manager.send_to_user()` with `payload.user_id` and `payload.data`.
        3. **Push Notification Dispatch:**
           - Iterate through `payload.devices`.
           - If `device.platform == 'apns'`, call `apns_provider.send_push()`.
           - If `device.platform == 'fcm'`, call `fcm_provider.send_push()`.
           - Format the push message title and body from `payload.data`.

## 4. Communication Channels

### 4.1. Base Interfaces (`channels/base.py`, `channels/push/providers/base.py`)

- **`NotificationChannel` (ABC):** Defines `async def send(self, recipient, payload)`.
- **`PushProvider` (ABC):** Defines `async def send_push(self, device_token, title, body, data)`.

### 4.2. WebSocket Channel (`channels/websocket/`)

- **`ConnectionManager` (`manager.py`):**
    - A thread-safe class to manage active WebSocket connections.
    - `active_connections: Dict[str, Set[WebSocket]]`: A dictionary mapping a `user_id` to a `Set` of active WebSocket objects for that user. This supports multiple connections (e.g., multiple browser tabs).
    - `async def connect(self, user_id: str, websocket: WebSocket)`: Adds a websocket to the user's set.
    - `def disconnect(self, user_id: str, websocket: WebSocket)`: Removes a websocket from the user's set.
    - `async def send_to_user(self, user_id: str, message: dict)`: Iterates through the set of websockets for a user and sends the JSON-serialized message to each.

- **`WebSocketChannel` (`channel.py`):**
    - Implements the `NotificationChannel` interface.
    - Its `send` method calls the `ConnectionManager.send_to_user`.

### 4.3. Push Notification Channel (`channels/push/`)

- **`PushNotificationChannel` (`channel.py`):**
    - Implements `NotificationChannel`.
    - Acts as a facade, delegating to the appropriate provider based on device platform information in the `recipient` data.

- **`APNSProvider` (`providers/apns.py`):**
    - Implements `PushProvider`.
    - Initializes the `apns2.APNsClient` with credentials from `config.py`.
    - The `send_push` method will construct a `Notification` object with the `Alert` payload and send it using the client. It will handle APNS-specific features like `sound`, `badge`, `thread-id`, and `custom` data.

- **`FCMProvider` (`providers/fcm.py`):**
    - Implements `PushProvider`.
    - Initializes the `firebase_admin` SDK.
    - The `send_push` method will construct a `firebase_admin.messaging.Message` with `notification` (title, body) and `data` payloads and send it using `firebase_admin.messaging.send()`.

## 5. Service Entrypoints

### 5.1. API Entrypoint (`entrypoints/api.py`)

- **FastAPI `APIRouter`:**
    - **`GET /health`:** A simple health check endpoint that returns `{"status": "ok"}`.
    - **`WebSocket /ws/{user_id}`:**
        - This endpoint will handle WebSocket connections.
        - **Authentication:** It should expect a JWT token to be passed as a query parameter or subprotocol header during the connection handshake. The token will be validated to authenticate the user.
        - **Connection:** Upon successful authentication, it calls `connection_manager.connect(user_id, websocket)`.
        - **Lifecycle:** It enters a loop to `await websocket.receive_text()`, primarily to detect client disconnects. On `websockets.exceptions.ConnectionClosed`, it calls `connection_manager.disconnect(user_id, websocket)`.

### 5.2. Message Consumer Entrypoint (`entrypoints/consumers.py`)

- **`RabbitMQConsumer` class:**
    - `__init__(self, amqp_url: str, queue_name: str, dispatcher: NotificationDispatcher)`: Initializes connection parameters and the dispatcher.
    - `run(self)`: Main loop to connect to RabbitMQ, declare the queue, and start consuming messages. It should include connection retry logic with exponential backoff.
    - `on_message_callback(self, ch, method, properties, body)`:
        1. Decode the message `body`.
        2. Use a `try...except` block to parse the JSON body into a `NotificationPayload` Pydantic model. If parsing fails, log the error and `nack` the message.
        3. If parsing succeeds, call `await self.dispatcher.dispatch_notification(payload)`.
        4. On successful dispatch, `ack` the message to remove it from the queue.

## 6. Application Lifecycle (`main.py`)

- A single, globally accessible instance of `ConnectionManager`, `APNSProvider`, `FCMProvider`, and `NotificationDispatcher` will be created.
- **`@app.on_event("startup")`:**
    1. `setup_logging()` is called.
    2. Instantiate the `ConnectionManager`.
    3. Instantiate the push providers (`APNSProvider`, `FCMProvider`), checking the `enabled` flag from config.
    4. Instantiate the `NotificationDispatcher` with the manager and providers.
    5. Create an instance of the `RabbitMQConsumer`.
    6. Start the consumer in a background task using `asyncio.create_task(consumer.run())`.

- **`@app.on_event("shutdown")`:**
    1. Gracefully stop the RabbitMQ consumer and close its connection.
    2. Close any other persistent connections (e.g., push provider clients if they require it).

## 7. Logging (`shared/logging.py`)

- Use `python-json-logger` to configure a `JSONFormatter`.
- Logs should include standard fields: `timestamp`, `level`, `name` (logger name), `message`.
- Where possible (if a trace ID is passed in message headers), include a `trace_id` for distributed tracing.

## 8. Deployment (`Dockerfile`)

- **Stage 1 (Builder):**
    - Start from a `python:3.12` base image.
    - Install `poetry` or `pip`.
    - Copy `pyproject.toml` and `poetry.lock`.
    - Install dependencies into a virtual environment (e.g., `/opt/venv`).
- **Stage 2 (Final):**
    - Start from a `python:3.12-slim` base image.
    - Copy the virtual environment from the builder stage.
    - Copy the `src` directory containing the application code.
    - Set `WORKDIR`.
    - Set the `CMD` to run the application: `["/opt/venv/bin/python", "-m", "uvicorn", "creativeflow.service.notification.main:app", "--host", "0.0.0.0", "--port", "8000"]`.
    - Run as a non-root user for security.