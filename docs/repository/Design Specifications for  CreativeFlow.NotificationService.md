# Software Design Specification: CreativeFlow.NotificationService

## 1. Introduction

### 1.1 Purpose
This document outlines the software design for the CreativeFlow Notification Service (`CreativeFlow.NotificationService`). This service is responsible for managing and delivering real-time updates and notifications to users of the CreativeFlow AI platform. It handles WebSocket connections for web frontend updates and sends push notifications to mobile applications (iOS and Android) via Apple Push Notification Service (APNS) and Firebase Cloud Messaging (FCM).

### 1.2 Scope
The scope of this document is limited to the design of the `CreativeFlow.NotificationService`. This includes:
*   Receiving notification requests from other backend services via message queues (RabbitMQ) or Pub/Sub (Redis).
*   Managing WebSocket connections with web clients.
*   Broadcasting real-time updates to connected web clients.
*   Sending push notifications to iOS devices via APNS.
*   Sending push notifications to Android devices via FCM.
*   Configuration management for service parameters and third-party credentials.
*   Logging and error handling within the service.

The following are out of scope for this specific service:
*   Business logic for determining *when* a notification should be sent (this resides in other services).
*   User preference management for notifications (assumed to be handled by User Account & Profile Service and queried if needed, or notification payload contains targeting info).
*   Persistent storage of notification history (though logs will be kept).

### 1.3 Definitions and Acronyms
*   **SDS**: Software Design Specification
*   **PWA**: Progressive Web Application
*   **API**: Application Programming Interface
*   **APNS**: Apple Push Notification Service
*   **FCM**: Firebase Cloud Messaging
*   **WebSocket**: A communication protocol providing full-duplex communication channels over a single TCP connection.
*   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pika**: Python AMQP 0-9-1 client library for RabbitMQ.
*   **Redis**: In-memory data structure store, used as a cache, message broker, and database.
*   **Pydantic**: Data validation and settings management using Python type annotations.
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **RabbitMQ**: Open-source message broker.
*   **Pub/Sub**: Publish/Subscribe messaging pattern.
*   **SDK**: Software Development Kit

## 2. System Overview
The Notification Service is a lightweight, standalone microservice designed for high throughput and low-latency delivery of real-time messages. It serves two primary functions:
1.  **WebSocket Server**: Establishes and maintains persistent WebSocket connections with authenticated web clients. When other backend services (e.g., AI Generation Orchestration Service, Collaboration Service) trigger an event, they publish a message to a queue/channel. The Notification Service consumes these messages and broadcasts relevant updates to the targeted WebSocket clients.
2.  **Push Notification Gateway**: Consumes notification events (potentially from the same queues/channels or dedicated ones) intended for mobile users who may not have an active WebSocket connection. It then formats and dispatches these notifications to the appropriate mobile platform's push notification service (APNS for iOS, FCM for Android).

The service is designed to be horizontally scalable to handle a large number of concurrent WebSocket connections and a high volume of notification dispatches.

## 3. Architectural Design

### 3.1 Architectural Style
The Notification Service follows a **Microservice Architecture**. It is a distinct, independently deployable service focused solely on notification delivery. Internally, it employs event-driven patterns for consuming messages and a layered approach for organizing its logic.

### 3.2 Key Components
The service is composed of the following logical components:
1.  **API Layer (`api`)**: Exposes WebSocket endpoints for client connections.
2.  **Core Logic Layer (`core`)**: Contains the main business logic for managing connections, processing notification requests, and dispatching them.
    *   `WebSocketManager`: Manages active WebSocket connections.
    *   `PushNotificationService`: Orchestrates sending push notifications to APNS/FCM.
    *   `NotificationManager`: Central dispatcher for notifications to appropriate channels.
3.  **Channels Layer (`channels`)**: Adapters for specific push notification providers.
    *   `APNSClient`: Interacts with APNS.
    *   `FCMClient`: Interacts with FCM.
4.  **Messaging Layer (`messaging`)**: Consumes messages from external message brokers.
    *   `MessageHandler`: Common logic for processing consumed messages.
    *   `RabbitMQConsumer`: Listens to RabbitMQ queues.
    *   `RedisConsumer`: Listens to Redis Pub/Sub channels.
5.  **Configuration & Shared Utilities (`config`, `shared`)**: Handles settings, logging, and custom exceptions.

### 3.3 Technology Stack
*   **Language**: Python 3.12.4
*   **Framework**: FastAPI 0.111.0 (for WebSocket server and potentially health check endpoints)
*   **WebSocket Library**: `websockets` 12.0 (Python library, used by FastAPI)
*   **Message Queue Clients**:
    *   `pika` 1.3.2 (for RabbitMQ)
    *   `redis` 5.0.7 (for Redis Pub/Sub)
*   **Push Notification Libraries**:
    *   `apns2` 2.5.0 (for APNS)
    *   `pyfcm` 1.5.4 (for FCM)
*   **Configuration**: Pydantic (implicitly via FastAPI or directly)
*   **Runtime Environment**: Docker container, running with Uvicorn.

### 3.4 Integration Points
*   **Web Clients (CreativeFlow.WebApp.PWA)**: Connect via WebSockets to receive real-time updates.
*   **RabbitMQ Broker (REPO-RABBITMQ-BROKER-001)**: Consumes messages from specific queues (e.g., `ai_generation_updates`, `collaboration_events`).
*   **Redis Cache (REPO-REDIS-CACHE-001)**: Optionally consumes messages via Redis Pub/Sub channels.
*   **APNS (Apple)**: Sends push notifications to iOS devices.
*   **FCM (Google)**: Sends push notifications to Android devices.
*   **Shared Libraries (REPO-SHARED-LIBS-001)**: May use common logging, exception, or utility classes.

## 4. Detailed Design

This section details the design of each Python module defined in the repository structure.

### 4.1 `src/creativeflow/services/notification/main.py`
*   **Purpose**: Main application entry point. Initializes and runs the FastAPI application.
*   **Key Class**: `FastAPI` app instance.
*   **Functions**:
    *   `app = FastAPI()`: Global FastAPI application instance.
    *   `async def startup_event()`:
        *   **Logic**:
            1.  Initialize `config.Settings`.
            2.  Initialize `MessageHandler` (injecting `NotificationManager`).
            3.  If `config.Settings.ENABLE_RABBITMQ_CONSUMER` is true:
                *   Initialize `RabbitMQConsumer` (injecting `config.Settings`, `MessageHandler`).
                *   Call `rabbitmq_consumer.connect()`.
                *   Start `rabbitmq_consumer.start_consuming(queue_name=config.Settings.RABBITMQ_QUEUE_NAME_AI_UPDATES)` in a background task (e.g., separate thread or asyncio task).
            4.  If `config.Settings.ENABLE_REDIS_CONSUMER` is true:
                *   Initialize `RedisConsumer` (injecting `config.Settings`, `MessageHandler`).
                *   Call `redis_consumer.connect()`.
                *   Start `redis_consumer.subscribe_and_listen(channel_name=config.Settings.REDIS_PUBSUB_CHANNEL_NAME)` as an asyncio task.
            5.  Log service startup.
    *   `async def shutdown_event()`:
        *   **Logic**:
            1.  If RabbitMQ consumer was started, signal it to stop and close connections gracefully.
            2.  If Redis consumer was started, signal it to stop and close connections gracefully.
            3.  Log service shutdown.
*   **Setup**:
    *   `app.include_router(websocket_endpoints.router)`: Includes WebSocket API routes.
    *   `app.add_event_handler("startup", startup_event)`
    *   `app.add_event_handler("shutdown", shutdown_event)`
    *   Basic logging configuration using `shared.logger`.
*   **Health Check (Optional but Recommended)**:
    *   `@app.get("/health") async def health_check(): return {"status": "ok"}`

### 4.2 `src/creativeflow/services/notification/config.py`
*   **Purpose**: Manages application configuration.
*   **Key Class**: `Settings(BaseModel)` (Pydantic model).
    *   **Attributes**:
        *   `RABBITMQ_URL: str`
        *   `RABBITMQ_QUEUE_NAME_AI_UPDATES: str = "ai_updates_notifications"`
        *   `REDIS_URL: str`
        *   `REDIS_PUBSUB_CHANNEL_NAME: str = "general_notifications"`
        *   `APNS_KEY_ID: str` (Required if `ENABLE_APNS_PUSH` is true)
        *   `APNS_TEAM_ID: str` (Required if `ENABLE_APNS_PUSH` is true)
        *   `APNS_CERT_FILE: str` (Path to .p8 key file, required if `ENABLE_APNS_PUSH` is true)
        *   `APNS_USE_SANDBOX: bool = False`
        *   `FCM_API_KEY: str` (Required if `ENABLE_FCM_PUSH` is true)
        *   `LOG_LEVEL: str = "INFO"`
        *   `ENABLE_RABBITMQ_CONSUMER: bool = True`
        *   `ENABLE_REDIS_CONSUMER: bool = False`
        *   `ENABLE_APNS_PUSH: bool = True`
        *   `ENABLE_FCM_PUSH: bool = True`
    *   **Pydantic Validators**: Add validators to ensure required fields are present if their corresponding feature toggle is enabled. E.g., if `ENABLE_APNS_PUSH` is true, `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_CERT_FILE` must be provided.
*   **Function**:
    *   `@lru_cache() def get_settings() -> Settings: return Settings()`
        *   **Logic**: Loads settings from environment variables. Returns a cached instance.

### 4.3 `src/creativeflow/services/notification/api/websocket_endpoints.py`
*   **Purpose**: Defines WebSocket endpoints.
*   **Global Variables**:
    *   `router = APIRouter()`
    *   `settings: Settings = get_settings()` (from `config`)
    *   `websocket_manager = WebSocketManager()` (Singleton or injected instance)
*   **Function**:
    *   `@router.websocket("/ws/{user_id}") async def websocket_endpoint(websocket: WebSocket, user_id: str):`
        *   **Logic**:
            1.  `await websocket_manager.connect(websocket, user_id)`
            2.  `logger.info(f"WebSocket connected for user: {user_id}")`
            3.  Try:
                *   Loop indefinitely: `await websocket.receive_text()` (or `receive_json()`).
                *   Log any received messages (though this service is primarily server-to-client, client pings or specific requests could be handled).
            4.  Except `WebSocketDisconnect`:
                *   `websocket_manager.disconnect(websocket, user_id)`
                *   `logger.info(f"WebSocket disconnected for user: {user_id}")`
            5.  Except Exception as e:
                *   `logger.error(f"WebSocket error for user {user_id}: {e}")`
                *   `websocket_manager.disconnect(websocket, user_id)` (ensure cleanup)

### 4.4 `src/creativeflow/services/notification/core/schemas.py`
*   **Purpose**: Defines data structures for internal use and communication.
*   **Classes (Pydantic `BaseModel`)**:
    *   `class NotificationPayload(BaseModel):`
        *   `user_id: str` (Target user for WebSocket, or for context if push)
        *   `event_type: str` (e.g., "ai_generation_progress", "collaboration_update", "new_comment")
        *   `data: Dict[str, Any]` (Actual payload, flexible structure based on `event_type`)
        *   `target_channels: List[str] = Field(default_factory=list)` (e.g., ["websocket"], ["push_ios"], ["push_android", "websocket"])
        *   `device_token: Optional[str] = None` (For push notifications if not in `data`)
        *   `device_type: Optional[str] = None` (e.g., "ios", "android", for push if not in `data`)
    *   `class WebSocketMessage(BaseModel):`
        *   `type: str` (Corresponds to `NotificationPayload.event_type` or a more generic UI event type)
        *   `content: Dict[str, Any]` (The `data` from `NotificationPayload` or a transformed version)
    *   `class PushNotificationContent(BaseModel):`
        *   `title: Optional[str] = None`
        *   `body: str`
        *   `data: Optional[Dict[str, Any]] = None` (Custom data for the app to handle)
        *   `deep_link_url: Optional[str] = None`

### 4.5 `src/creativeflow/services/notification/core/notification_manager.py`
*   **Purpose**: Central dispatcher for notifications.
*   **Class**: `NotificationManager`
    *   **`__init__(self, websocket_manager: WebSocketManager, push_service: PushNotificationService)`**:
        *   Store injected dependencies.
    *   **`async def send_notification(self, payload: NotificationPayload)`**:
        *   **Logic**:
            1.  Log receipt of notification payload.
            2.  Iterate `payload.target_channels`:
                *   If "websocket" in `payload.target_channels`:
                    *   Create `WebSocketMessage` from `payload.event_type` and `payload.data`.
                    *   Call `await self.websocket_manager.send_to_user(payload.user_id, ws_message)`.
                    *   Log WebSocket dispatch attempt.
                *   If "push_ios" in `payload.target_channels` and `payload.device_token` (or `payload.data.get('device_token')`) and `settings.ENABLE_APNS_PUSH`:
                    *   Construct `PushNotificationContent` from `payload.data` (extract title, body, custom data, deep_link).
                    *   Call `await self.push_service.send_push(device_token=payload.device_token or payload.data['device_token'], device_type="ios", content=push_content)`.
                    *   Log APNS dispatch attempt.
                *   If "push_android" in `payload.target_channels` and `payload.device_token` (or `payload.data.get('device_token')`) and `settings.ENABLE_FCM_PUSH`:
                    *   Construct `PushNotificationContent` from `payload.data`.
                    *   Call `await self.push_service.send_push(device_token=payload.device_token or payload.data['device_token'], device_type="android", content=push_content)`.
                    *   Log FCM dispatch attempt.
            3.  Handle exceptions from dispatchers (e.g., `PushProviderError`) and log them.

### 4.6 `src/creativeflow/services/notification/core/websocket_manager.py`
*   **Purpose**: Manages WebSocket client connections.
*   **Class**: `WebSocketManager`
    *   **`__init__(self)`**:
        *   `self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)`
    *   **`async def connect(self, websocket: WebSocket, user_id: str)`**:
        *   `await websocket.accept()`
        *   `self.active_connections[user_id].append(websocket)`
    *   **`def disconnect(self, websocket: WebSocket, user_id: str)`**:
        *   `if user_id in self.active_connections and websocket in self.active_connections[user_id]:`
            *   `self.active_connections[user_id].remove(websocket)`
            *   `if not self.active_connections[user_id]: del self.active_connections[user_id]`
    *   **`async def send_to_user(self, user_id: str, message: WebSocketMessage)`**:
        *   `if user_id in self.active_connections:`
            *   `disconnected_sockets = []`
            *   `for connection in self.active_connections[user_id]:`
                *   Try `await connection.send_text(message.model_dump_json())` (or `send_json`)
                *   Except `WebSocketException` (or specific send errors):
                    *   `logger.warning(f"Failed to send to a WebSocket for user {user_id}, marking for removal.")`
                    *   `disconnected_sockets.append(connection)`
            *   `for sock in disconnected_sockets: self.disconnect(sock, user_id)`
    *   **`async def broadcast(self, message: WebSocketMessage)`**: (Use sparingly)
        *   `all_sockets = [conn for conns_list in self.active_connections.values() for conn in conns_list]`
        *   `for connection in all_sockets:`
            *   Try `await connection.send_text(message.model_dump_json())`
            *   Except `WebSocketException`:
                *   `logger.warning("Failed to broadcast to a WebSocket, it might be disconnected.")`
                *   (Consider a mechanism to find its user_id and call `disconnect` if this happens often)

### 4.7 `src/creativeflow/services/notification/core/push_notification_service.py`
*   **Purpose**: Dispatches push notifications to appropriate providers.
*   **Class**: `PushNotificationService`
    *   **`__init__(self, apns_client: APNSClient, fcm_client: FCMClient, settings: Settings)`**:
        *   Store injected dependencies.
    *   **`async def send_push(self, device_token: str, device_type: str, content: PushNotificationContent)`**:
        *   **Logic**:
            1.  `logger.info(f"Attempting to send push to {device_type} device: {device_token}")`
            2.  If `device_type.lower() == "ios"` and `self.settings.ENABLE_APNS_PUSH`:
                *   Try `await self.apns_client.send(device_token, content)`
                *   Except `Exception as e`:
                    *   `logger.error(f"APNS send failed for token {device_token}: {e}")`
                    *   Raise `PushProviderError(f"APNS Error: {e}")`
            3.  Else if `device_type.lower() == "android"` and `self.settings.ENABLE_FCM_PUSH`:
                *   Try `await self.fcm_client.send(device_token, content)`
                *   Except `Exception as e`:
                    *   `logger.error(f"FCM send failed for token {device_token}: {e}")`
                    *   Raise `PushProviderError(f"FCM Error: {e}")`
            4.  Else:
                *   `logger.warning(f"Unsupported device_type '{device_type}' or provider disabled for token {device_token}")`

### 4.8 `src/creativeflow/services/notification/channels/push/base_push_provider.py`
*   **Purpose**: Defines the interface for push notification providers.
*   **Class**: `BasePushProvider(ABC)`
    *   **`@abstractmethod async def send(self, device_token: str, payload: PushNotificationContent) -> None:`**
        *   Pass.

### 4.9 `src/creativeflow/services/notification/channels/push/apns_client.py`
*   **Purpose**: Sends push notifications via APNS.
*   **Class**: `APNSClient(BasePushProvider)`
    *   **`__init__(self, config: Settings)`**:
        *   `self.config = config`
        *   If `config.ENABLE_APNS_PUSH`:
            *   Try to initialize `self.apns_client_instance = APNsClient(key=config.APNS_CERT_FILE, use_sandbox=config.APNS_USE_SANDBOX, team_id=config.APNS_TEAM_ID, key_id=config.APNS_KEY_ID)`
            *   Log success or failure of initialization.
        *   Else `self.apns_client_instance = None`
    *   **`async def send(self, device_token: str, payload: PushNotificationContent) -> None:`**:
        *   **Logic**:
            1.  If not `self.apns_client_instance` or not `self.config.ENABLE_APNS_PUSH`:
                *   `logger.info("APNS client not initialized or disabled.")`
                *   Return
            2.  Construct `apns_payload = Payload(alert={"title": payload.title, "body": payload.body}, sound="default", custom=payload.data or {})`
            3.  If `payload.deep_link_url`, add to `custom` data or APNS-specific field if available.
            4.  `notification = Notification(payload=apns_payload, token=device_token)`
            5.  Try `response = await asyncio.to_thread(self.apns_client_instance.send_notification, notification)`
                *   `# Note: apns2.send_notification might be synchronous. Wrap in asyncio.to_thread if it is.`
                *   If `response.is_successful`: `logger.info("APNS push sent successfully.")`
                *   Else `logger.error(f"APNS push failed: {response.status_code} - {response.description}")`
                     `raise PushProviderError(f"APNS Error: {response.description}")`
            6.  Catch APNS-specific exceptions from `apns2` and re-raise as `PushProviderError`.

### 4.10 `src/creativeflow/services/notification/channels/push/fcm_client.py`
*   **Purpose**: Sends push notifications via FCM.
*   **Class**: `FCMClient(BasePushProvider)`
    *   **`__init__(self, config: Settings)`**:
        *   `self.config = config`
        *   If `config.ENABLE_FCM_PUSH`:
            *   Try to initialize `self.fcm_service_instance = FCMNotification(api_key=config.FCM_API_KEY)`
            *   Log success or failure.
        *   Else `self.fcm_service_instance = None`
    *   **`async def send(self, device_token: str, payload: PushNotificationContent) -> None:`**:
        *   **Logic**:
            1.  If not `self.fcm_service_instance` or not `self.config.ENABLE_FCM_PUSH`:
                *   `logger.info("FCM client not initialized or disabled.")`
                *   Return
            2.  Prepare message parameters: `message_title=payload.title`, `message_body=payload.body`, `data_message=payload.data` (include `deep_link_url` here if needed by client app).
            3.  Try:
                *   Define a function `_send_sync()` that calls `self.fcm_service_instance.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body, data_message=data_message, ...)`
                *   `result = await asyncio.to_thread(_send_sync)`
                *   `# pyfcm is typically synchronous. Wrap in asyncio.to_thread.`
                *   If `result.get("success")`: `logger.info("FCM push sent successfully.")`
                *   Else `logger.error(f"FCM push failed: {result.get('failure')} errors. Results: {result.get('results')}")`
                     `raise PushProviderError(f"FCM Error: {result.get('results')}")`
            4.  Catch FCM-specific exceptions from `pyfcm` and re-raise as `PushProviderError`.

### 4.11 `src/creativeflow/services/notification/messaging/message_handler.py`
*   **Purpose**: Processes messages from queues before dispatching.
*   **Class**: `MessageHandler`
    *   **`__init__(self, notification_manager: NotificationManager)`**:
        *   Store injected dependency.
    *   **`async def handle_message(self, raw_message_body: bytes | str, message_source: str)`**:
        *   **Logic**:
            1.  `logger.debug(f"Received message from {message_source}: {raw_message_body}")`
            2.  Try:
                *   If `isinstance(raw_message_body, bytes)`: `decoded_body = raw_message_body.decode('utf-8')`
                *   Else: `decoded_body = raw_message_body`
                *   `message_data = json.loads(decoded_body)`
                *   `payload = NotificationPayload(**message_data)`
            3.  Except `(json.JSONDecodeError, ValidationError) as e`:
                *   `logger.error(f"Failed to parse or validate message from {message_source}: {e}. Message: {raw_message_body}")`
                *   Raise `InvalidMessageFormatError(f"Invalid message from {message_source}: {e}")`
                *   Return (or handle error acknowledgement appropriately if this is a direct callback)
            4.  `await self.notification_manager.send_notification(payload)`

### 4.12 `src/creativeflow/services/notification/messaging/rabbitmq_consumer.py`
*   **Purpose**: Consumes messages from RabbitMQ.
*   **Class**: `RabbitMQConsumer`
    *   **`__init__(self, config: Settings, message_handler: MessageHandler)`**:
        *   Store dependencies. `self.connection = None`, `self.channel = None`.
    *   **`def connect(self)`**:
        *   **Logic**:
            1.  Try to establish `pika.BlockingConnection` using `config.RABBITMQ_URL`.
            2.  `self.channel = self.connection.channel()`
            3.  Log success.
            4.  Handle connection errors and implement retry logic (e.g., exponential backoff, max retries).
    *   **`def _setup_channel_and_queue(self, queue_name: str)`**:
        *   **Logic**:
            1.  Ensure connection and channel exist.
            2.  `self.channel.queue_declare(queue=queue_name, durable=True)` (or as per producer config)
            3.  Potentially declare exchange and bind queue if using exchanges.
    *   **`def _on_message_callback(self, ch, method, properties, body)`**:
        *   **Logic**:
            1.  Try `asyncio.run(self.message_handler.handle_message(body, "RabbitMQ"))`
                *   `# Since pika callbacks are often synchronous, and handle_message is async, run it in an event loop.`
                *   `# Alternatively, use an async pika library or manage an asyncio event loop within the consumer thread.`
                *   `ch.basic_ack(delivery_tag=method.delivery_tag)`
            2.  Except `InvalidMessageFormatError` or other processing errors:
                *   `logger.error("Error processing RabbitMQ message. NACKing or dead-lettering.")`
                *   `ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)` (to avoid infinite loops on bad messages; consider dead-letter exchange).
            3.  Except `Exception as e`: (Generic catch for unexpected issues)
                *   `logger.exception("Unexpected error processing RabbitMQ message. NACKing.")`
                *   `ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)`
    *   **`def start_consuming(self, queue_name: str)`**: (This method will block or run in a thread)
        *   **Logic**:
            1.  If not `self.config.ENABLE_RABBITMQ_CONSUMER`: `logger.info("RabbitMQ consumer disabled."); return`
            2.  Ensure connection.
            3.  `self._setup_channel_and_queue(queue_name)`
            4.  `self.channel.basic_qos(prefetch_count=1)` (for fair dispatch if multiple consumers)
            5.  `self.channel.basic_consume(queue=queue_name, on_message_callback=self._on_message_callback)`
            6.  `logger.info(f"Starting RabbitMQ consumer on queue: {queue_name}")`
            7.  `self.channel.start_consuming()` (This is blocking)
    *   **`def stop_consuming(self)`**:
        *   If `self.channel` and `self.channel.is_open`: `self.channel.stop_consuming()`
        *   If `self.connection` and `self.connection.is_open`: `self.connection.close()`
        *   Log stopping.

### 4.13 `src/creativeflow/services/notification/messaging/redis_consumer.py`
*   **Purpose**: Consumes messages from Redis Pub/Sub.
*   **Class**: `RedisConsumer`
    *   **`__init__(self, config: Settings, message_handler: MessageHandler)`**:
        *   Store dependencies. `self.redis_client = None`, `self.pubsub = None`.
    *   **`async def connect(self)`**:
        *   **Logic**:
            1.  Try `self.redis_client = redis.asyncio.from_url(self.config.REDIS_URL)`
            2.  `await self.redis_client.ping()`
            3.  Log success.
            4.  Handle connection errors and implement retry logic.
    *   **`async def subscribe_and_listen(self, channel_name: str)`**:
        *   **Logic**:
            1.  If not `self.config.ENABLE_REDIS_CONSUMER`: `logger.info("Redis consumer disabled."); return`
            2.  Ensure connection.
            3.  `self.pubsub = self.redis_client.pubsub()`
            4.  `await self.pubsub.subscribe(channel_name)`
            5.  `logger.info(f"Subscribed to Redis channel: {channel_name}")`
            6.  Loop:
                *   Try `message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)`
                *   If `message and message.get('type') == 'message'`:
                    *   `await self.message_handler.handle_message(message['data'], "Redis Pub/Sub")`
                *   Handle task cancellation/shutdown signals to break loop.
            7.  Finally:
                *   If `self.pubsub`: `await self.pubsub.unsubscribe(channel_name)`
                *   `await self.pubsub.close()`
    *   **`async def stop_listening(self)`**:
        *   If `self.pubsub`: `await self.pubsub.unsubscribe()` and `await self.pubsub.close()`
        *   If `self.redis_client`: `await self.redis_client.close()`
        *   Log stopping.

### 4.14 `src/creativeflow/services/notification/shared/logger.py`
*   **Purpose**: Standardized logging setup.
*   **Function**:
    *   `def get_logger(name: str, level: str = "INFO") -> logging.Logger:`
        *   **Logic**:
            1.  `logger = logging.getLogger(name)`
            2.  `logger.setLevel(logging.getLevelName(level.upper()))`
            3.  If not `logger.hasHandlers()`: (to avoid duplicate handlers)
                *   `handler = logging.StreamHandler(sys.stdout)`
                *   `formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')`
                *   `handler.setFormatter(formatter)`
                *   `logger.addHandler(handler)`
            4.  Return `logger`.
*   **Global Setup (e.g., in `main.py` or when `get_settings` is first called)**:
    *   `settings = get_settings()`
    *   `# Call get_logger with a root name and settings.LOG_LEVEL to initialize default level`
    *   `# logger = get_logger("creativeflow.notification", settings.LOG_LEVEL)`

### 4.15 `src/creativeflow/services/notification/shared/exceptions.py`
*   **Purpose**: Custom exceptions for the service.
*   **Classes**:
    *   `class NotificationServiceError(Exception): pass` (Base exception for this service)
    *   `class NotificationDispatchError(NotificationServiceError): pass`
    *   `class PushProviderError(NotificationDispatchError): def __init__(self, provider_name: str, original_error: Any): self.provider_name = provider_name; self.original_error = original_error; super().__init__(f"{provider_name} error: {original_error}")`
    *   `class InvalidMessageFormatError(ValueError, NotificationServiceError): pass`

### 4.16 `requirements.txt`
*   **Content**:
    
    fastapi==0.111.0
    uvicorn[standard]==0.29.0  # Or specific version
    websockets==12.0
    pika==1.3.2
    redis==5.0.7
    apns2==2.5.0
    pyfcm==1.5.4
    pydantic==2.7.1 # FastAPI will bring this, but good to pin
    # Add any other direct dependencies
    

### 4.17 `pyproject.toml`
*   **Purpose**: Project metadata and build system configuration.
*   **Content (Example for Poetry)**:
    toml
    [tool.poetry]
    name = "creativeflow-notification-service"
    version = "0.1.0"
    description = "CreativeFlow AI Notification Service"
    authors = ["Your Name <you@example.com>"]
    readme = "README.md"
    packages = [{include = "creativeflow", from = "src"}]

    [tool.poetry.dependencies]
    python = "^3.11" # Aligned with tech stack, but problem states 3.12.4, adjust as needed.
    fastapi = "0.111.0"
    uvicorn = {extras = ["standard"], version = "^0.29.0"}
    websockets = "12.0"
    pika = "1.3.2"
    redis = "5.0.7"
    apns2 = "2.5.0"
    pyfcm = "1.5.4"
    pydantic = "2.7.1"

    [tool.poetry.group.dev.dependencies]
    pytest = "^7.0"
    pytest-asyncio = "^0.21.0"
    httpx = "^0.25.0" # For testing FastAPI endpoints

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    
    *(Note: Pydantic version specified, but FastAPI usually manages its compatible Pydantic version. Version specified in file structure is Pydantic v2.0.0, but FastAPI 0.111.0 would use a more recent Pydantic v2. Adjusted to 2.7.1)*
    *Python version from current repository: 3.12.4. `^3.11` in pyproject.toml is compatible but can be set to `^3.12`.*

### 4.18 `.env.example`
*   **Content**:
    env
    # General
    LOG_LEVEL=INFO

    # RabbitMQ Consumer (if enabled)
    ENABLE_RABBITMQ_CONSUMER=True
    RABBITMQ_URL="amqp://guest:guest@localhost:5672/%2F"
    RABBITMQ_QUEUE_NAME_AI_UPDATES="ai_updates_notifications"

    # Redis Pub/Sub Consumer (if enabled)
    ENABLE_REDIS_CONSUMER=False
    REDIS_URL="redis://localhost:6379/0"
    REDIS_PUBSUB_CHANNEL_NAME="general_notifications"

    # APNS (Apple Push Notification Service) (if enabled)
    ENABLE_APNS_PUSH=True
    APNS_KEY_ID="YOUR_APNS_KEY_ID"
    APNS_TEAM_ID="YOUR_APPLE_TEAM_ID"
    APNS_CERT_FILE="./certs/AuthKey_YOUR_APNS_KEY_ID.p8" # Path to your .p8 key file
    APNS_USE_SANDBOX=True # True for development, False for production

    # FCM (Firebase Cloud Messaging) (if enabled)
    ENABLE_FCM_PUSH=True
    FCM_API_KEY="YOUR_FCM_SERVER_KEY"
    

## 5. Data Management
This service is primarily stateless regarding user notifications.
*   **Message Payloads**: Defined by `core.schemas.NotificationPayload`, `WebSocketMessage`, and `PushNotificationContent`. These dictate the structure of data received and sent.
*   **Connection State**: `core.websocket_manager.WebSocketManager` holds the state of active WebSocket connections in memory (a dictionary). This is volatile and lost on service restart. For scalability across multiple instances, this state would need to be externalized (e.g., using Redis to track user_id to service instance mapping, or a shared Pub/Sub for broadcasting to all instances which then filter by local connections). *Initial design assumes single instance or simple load balancing without shared WebSocket state for simplicity, but this is a key scalability consideration.*

## 6. Interfaces

### 6.1 WebSocket API
*   **Endpoint**: `/ws/{user_id}`
*   **Protocol**: WebSocket (WSS in production)
*   **Purpose**: Allows authenticated web clients to establish a persistent connection to receive real-time updates.
*   **Messages (Server to Client)**: JSON objects conforming to `core.schemas.WebSocketMessage`.
    *   `type`: String indicating the event type (e.g., "ai_generation_progress", "new_message").
    *   `content`: Dictionary containing the specific data for the event.
*   **Messages (Client to Server)**: Generally, this service does not expect significant messages from clients, but could handle pings or acknowledgements if designed.

### 6.2 Message Queue Consumer Interfaces
*   **RabbitMQ**:
    *   Consumes JSON messages from configured queues (e.g., `ai_updates_notifications`).
    *   Expected message format: `core.schemas.NotificationPayload`.
*   **Redis Pub/Sub**:
    *   Subscribes to configured channels (e.g., `general_notifications`).
    *   Expected message format: JSON string parsable to `core.schemas.NotificationPayload`.

### 6.3 Push Notification Gateway Interfaces
*   **APNS**: Uses `apns2` library to communicate with Apple's APNS servers.
*   **FCM**: Uses `pyfcm` library to communicate with Google's FCM servers.

## 7. Configuration Management
Configuration is managed via environment variables, loaded and validated by `config.py` using Pydantic.
*   **Key Configurations**:
    *   Message Broker URLs and queue/channel names (`RABBITMQ_URL`, `REDIS_URL`, etc.)
    *   Push Notification Provider credentials (`APNS_KEY_ID`, `FCM_API_KEY`, etc.)
    *   Feature Toggles (`ENABLE_RABBITMQ_CONSUMER`, `ENABLE_APNS_PUSH`, etc.)
    *   Logging Level (`LOG_LEVEL`)
*   An `.env.example` file provides a template for required variables.

## 8. Error Handling and Logging
*   **Custom Exceptions**: Defined in `shared.exceptions.py` for domain-specific errors (e.g., `PushProviderError`, `InvalidMessageFormatError`).
*   **Logging**: Standardized Python `logging` module, configured via `shared.logger.py`. Logs include timestamps, severity levels, module names, and contextual information. `LOG_LEVEL` is configurable.
*   **Message Processing**: Errors during message parsing or validation in `MessageHandler` will be logged, and messages might be NACKed (RabbitMQ) or ignored (Redis) to prevent processing loops, potentially with dead-lettering.
*   **Push Notifications**: Errors from APNS/FCM clients will be caught, logged, and potentially retried (simple retry for transient errors could be added in `PushNotificationService` or specific clients).
*   **WebSockets**: Connection errors and send errors are logged. Disconnected clients are removed from the active list.

## 9. Scalability and Performance
*   **WebSocket Connections**: FastAPI with Uvicorn (using `websockets`) is capable of handling many concurrent WebSocket connections per instance. For very large scale, multiple instances of the Notification Service would be run behind a load balancer that supports WebSocket sticky sessions (if client-specific state is held locally) or a stateless approach where messages are broadcast to all instances via a Pub/Sub system (like Redis) and each instance then filters and sends to its connected clients. *The current `WebSocketManager` design is instance-local; for true horizontal scaling, a shared mechanism (e.g., Redis Pub/Sub for broadcasting to all notification service instances) would be needed to inform all instances about messages for specific users.*
*   **Message Consumption**:
    *   RabbitMQ consumers can be scaled by running multiple instances of the service. Pika's `basic_qos(prefetch_count=1)` helps distribute messages.
    *   Redis Pub/Sub inherently broadcasts to all subscribers; filtering happens at the consumer.
*   **Push Notification Dispatch**: Sending push notifications is I/O bound. `asyncio` and `async/await` are used to handle these operations concurrently. The number of service instances can be scaled.
*   **Asynchronous Operations**: All I/O-bound operations (network calls to APNS/FCM, message queue interactions) are asynchronous.

## 10. Security Considerations
*   **WebSocket Security (WSS)**: In production, WebSockets must use WSS (WebSocket Secure) which runs over TLS. This is typically handled at the reverse proxy/load balancer level (e.g., Nginx).
*   **Credential Management**:
    *   APNS certificate/key and FCM server key are sensitive. They are loaded from configuration (environment variables) and should be managed securely in deployment environments (e.g., using HashiCorp Vault, Kubernetes Secrets).
    *   Message broker credentials (`RABBITMQ_URL`, `REDIS_URL`) also need secure management.
*   **Input Validation**: Incoming messages from queues are validated against Pydantic schemas (`NotificationPayload`) in `MessageHandler`.
*   **User Identification**: WebSocket endpoints use `user_id` from the path parameter. Authentication of this `user_id` (e.g., validating a JWT passed in headers during WebSocket handshake) is assumed to be handled by an API Gateway or directly in the WebSocket connection logic if necessary. *The current `websocket_endpoints.py` design doesn't explicitly show JWT validation during handshake, which is a critical security addition.*
    *   **Refinement**: The WebSocket endpoint should validate an auth token (e.g., JWT) passed by the client during connection setup to securely associate the WebSocket with the `user_id`.
*   **Rate Limiting**: While this service dispatches notifications, rate limiting on incoming notification *requests* (if exposed via an API) or on outgoing push notifications (to avoid overwhelming APNS/FCM) might be considered, though primary rate limiting is usually on the services *generating* the notification events.

## 11. Deployment
*   The service will be packaged as a Docker container.
*   It will be run using Uvicorn, a ASGI server.
*   Deployment will be managed via Kubernetes or a similar orchestration platform.
*   Environment variables will be used for configuration.
*   Horizontal scaling will be achieved by running multiple instances of the container.

## 12. Future Considerations / Refinements
*   **Shared WebSocket State for Scalability**: For robust horizontal scaling of WebSocket connections, implement a shared state mechanism (e.g., using Redis Pub/Sub to broadcast messages to all Notification Service instances, which then filter for their locally connected users).
*   **Dead Letter Queues (DLQ)**: For RabbitMQ, configure DLQs to handle messages that cannot be processed after multiple retries, allowing for investigation and manual reprocessing.
*   **Advanced Retry Logic**: Implement more sophisticated retry mechanisms (e.g., with exponential backoff and jitter) for push notification sending and message queue connections.
*   **Notification Preferences**: If user-specific notification preferences (e.g., "don't send push for X event type") are needed, this service might need to query a User Preference service or receive preference information in the `NotificationPayload`.
*   **Metrics and Monitoring**: Integrate with Prometheus/Grafana for metrics like number of active WebSocket connections, messages processed, push notifications sent/failed, queue lengths.
*   **WebSocket Authentication**: Implement robust authentication for WebSocket connections (e.g., JWT validation during handshake).