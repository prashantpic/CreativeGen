# Specification

# 1. Files

- **Path:** src/creativeflow/services/notification/__init__.py  
**Description:** Initializes the notification service Python package, making its modules accessible.  
**Template:** Python Package Initializer  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file can be empty or can expose selected classes/functions from the package.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file.
    
**Namespace:** creativeflow.services.notification  
**Metadata:**
    
    - **Category:** Packaging
    
- **Path:** src/creativeflow/services/notification/main.py  
**Description:** Main application entry point for the FastAPI Notification Service. Initializes the FastAPI app, includes API routers, and sets up startup/shutdown event handlers for resources like message queue consumers.  
**Template:** Python FastAPI Main Application  
**Dependency Level:** 7  
**Name:** main  
**Type:** ApplicationEntrypoint  
**Relative Path:** main.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** startup_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|private  
**Notes:** Handles startup logic like connecting to message brokers.  
    - **Name:** shutdown_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|private  
**Notes:** Handles shutdown logic like closing connections.  
    
**Implemented Features:**
    
    - WebSocket Server
    - Message Consumer Management
    - Application Lifecycle
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Initializes and runs the FastAPI application, including WebSocket endpoints and message consumer background tasks.  
**Logic Description:** Creates a FastAPI instance. Registers WebSocket routers from api.websocket_endpoints. Sets up event handlers to start and stop message consumers (RabbitMQ, Redis Pub/Sub) in the background. Configures logging and any global middleware.  
**Documentation:**
    
    - **Summary:** The main executable for the Notification Service, responsible for setting up and running the FastAPI server.
    
**Namespace:** creativeflow.services.notification  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/services/notification/config.py  
**Description:** Handles application configuration loading and validation using Pydantic. Loads settings from environment variables or configuration files for RabbitMQ, Redis, APNS, FCM, and other service parameters.  
**Template:** Python Pydantic Configuration  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** config.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** RABBITMQ_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** REDIS_URL  
**Type:** str  
**Attributes:** public  
    - **Name:** APNS_KEY_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** APNS_TEAM_ID  
**Type:** str  
**Attributes:** public  
    - **Name:** APNS_CERT_FILE  
**Type:** str  
**Attributes:** public  
    - **Name:** APNS_USE_SANDBOX  
**Type:** bool  
**Attributes:** public  
    - **Name:** FCM_API_KEY  
**Type:** str  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static  
**Notes:** Returns a cached instance of the Settings model.  
    
**Implemented Features:**
    
    - Configuration Management
    - Settings Validation
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Provides a centralized and validated way to access application settings.  
**Logic Description:** Defines a Pydantic BaseModel class `Settings` to hold all configuration variables. Loads values from environment variables, potentially with default values. Implements validation rules for critical settings.  
**Documentation:**
    
    - **Summary:** Manages all application configuration settings, ensuring they are present and valid at startup.
    
**Namespace:** creativeflow.services.notification.config  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/creativeflow/services/notification/api/__init__.py  
**Description:** Initializes the api module.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** api/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the API module.
    
**Namespace:** creativeflow.services.notification.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/notification/api/websocket_endpoints.py  
**Description:** Defines FastAPI WebSocket endpoints for client connections. Handles WebSocket lifecycle events (connect, disconnect) and message passing between clients and the WebSocketManager.  
**Template:** Python FastAPI WebSocket Endpoint  
**Dependency Level:** 2  
**Name:** websocket_endpoints  
**Type:** Controller  
**Relative Path:** api/websocket_endpoints.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    - **Name:** websocket_manager  
**Type:** WebSocketManager  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** websocket_endpoint  
**Parameters:**
    
    - websocket: WebSocket
    - user_id: str
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Handles incoming WebSocket connections and messages for a user.  
    
**Implemented Features:**
    
    - Real-time Client Communication
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    - Section 5.3.1 (Role in AI generation pipeline notifications for user updates)
    
**Purpose:** Manages WebSocket connections for real-time communication with web clients.  
**Logic Description:** Creates a FastAPI APIRouter. Defines a WebSocket endpoint (e.g., /ws/{user_id}). On connection, registers the client with the WebSocketManager. Listens for incoming messages from the client (if any). On disconnect, unregisters the client. Relies on WebSocketManager for broadcasting messages.  
**Documentation:**
    
    - **Summary:** Provides WebSocket endpoints for clients to connect and receive real-time updates.
    
**Namespace:** creativeflow.services.notification.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/notification/core/__init__.py  
**Description:** Initializes the core logic module.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** core/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the core services module.
    
**Namespace:** creativeflow.services.notification.core  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/services/notification/core/schemas.py  
**Description:** Defines Pydantic models for data structures used within the notification service, such as incoming message payloads from queues, WebSocket message formats, and push notification content structures.  
**Template:** Python Pydantic Models  
**Dependency Level:** 0  
**Name:** schemas  
**Type:** Model  
**Relative Path:** core/schemas.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** NotificationPayload  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** For messages from RabbitMQ/Redis.  
    - **Name:** WebSocketMessage  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** For messages sent over WebSockets.  
    - **Name:** PushNotificationContent  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** For structured push notification data.  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Validation
    - Data Serialization
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Defines and validates the structure of data flowing through the notification service.  
**Logic Description:** Contains Pydantic BaseModel classes for: NotificationPayload (e.g., user_id, event_type, data), WebSocketMessage (e.g., type, content), and PushNotificationContent (e.g., title, body, device_token, deep_link_url). These models ensure type safety and data integrity.  
**Documentation:**
    
    - **Summary:** Provides Pydantic models for data interchange and validation within the notification service.
    
**Namespace:** creativeflow.services.notification.core  
**Metadata:**
    
    - **Category:** DataModel
    
- **Path:** src/creativeflow/services/notification/core/notification_manager.py  
**Description:** Central service orchestrating the dispatch of notifications. Receives processed notification requests (e.g., from message consumers) and routes them to the appropriate channel managers (WebSocketManager or PushNotificationService).  
**Template:** Python Service Class  
**Dependency Level:** 4  
**Name:** notification_manager  
**Type:** Service  
**Relative Path:** core/notification_manager.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - FacadePattern
    
**Members:**
    
    - **Name:** websocket_manager  
**Type:** WebSocketManager  
**Attributes:** private  
**Notes:** Injected dependency  
    - **Name:** push_service  
**Type:** PushNotificationService  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** send_notification  
**Parameters:**
    
    - payload: NotificationPayload
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Determines target channels and dispatches.  
    
**Implemented Features:**
    
    - Notification Orchestration
    - Channel Routing
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Acts as a central dispatcher for all notifications, deciding which channels to use.  
**Logic Description:** The `send_notification` method takes a NotificationPayload. Based on the payload's event_type or user preferences (if accessible), it decides whether to send a WebSocket message via WebSocketManager and/or a push notification via PushNotificationService. Logs dispatch attempts and outcomes.  
**Documentation:**
    
    - **Summary:** Orchestrates sending notifications through various channels based on the incoming request.
    
**Namespace:** creativeflow.services.notification.core  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/services/notification/core/websocket_manager.py  
**Description:** Manages active WebSocket connections. Provides methods to register/unregister clients, and broadcast messages to specific users or groups of users.  
**Template:** Python WebSocket Manager Class  
**Dependency Level:** 1  
**Name:** websocket_manager  
**Type:** Service  
**Relative Path:** core/websocket_manager.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** active_connections  
**Type:** Dict[str, List[WebSocket]]  
**Attributes:** private  
**Notes:** Maps user_id to list of their active WebSockets.  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    - websocket: WebSocket
    - user_id: str
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** disconnect  
**Parameters:**
    
    - websocket: WebSocket
    - user_id: str
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** send_to_user  
**Parameters:**
    
    - user_id: str
    - message: WebSocketMessage
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** broadcast  
**Parameters:**
    
    - message: WebSocketMessage
    
**Return Type:** None  
**Attributes:** async|public  
    
**Implemented Features:**
    
    - WebSocket Connection Management
    - Real-time Message Broadcasting
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    - Section 5.3.1 (Role in AI generation pipeline notifications for user updates)
    
**Purpose:** Manages and facilitates real-time communication with connected WebSocket clients.  
**Logic Description:** Maintains a dictionary of active connections, typically mapping user IDs to WebSocket objects. `connect` adds a client. `disconnect` removes a client. `send_to_user` sends a message to all WebSockets associated with a user_id. `broadcast` sends to all connected clients (use with caution). Handles WebSocket send errors gracefully.  
**Documentation:**
    
    - **Summary:** Handles the lifecycle and message broadcasting for WebSocket connections.
    
**Namespace:** creativeflow.services.notification.core  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/services/notification/core/push_notification_service.py  
**Description:** Abstract service for sending push notifications. It selects the appropriate provider (APNS or FCM) based on device type or other criteria and delegates the sending task to the respective client.  
**Template:** Python Service Class  
**Dependency Level:** 3  
**Name:** push_notification_service  
**Type:** Service  
**Relative Path:** core/push_notification_service.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - StrategyPattern
    - AdapterPattern
    
**Members:**
    
    - **Name:** apns_client  
**Type:** APNSClient  
**Attributes:** private  
**Notes:** Injected dependency  
    - **Name:** fcm_client  
**Type:** FCMClient  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** send_push  
**Parameters:**
    
    - device_token: str
    - device_type: str
    - content: PushNotificationContent
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** device_type could be 'ios' or 'android'.  
    
**Implemented Features:**
    
    - Push Notification Dispatching
    - Provider Selection
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications part)
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Manages the sending of push notifications to mobile devices via APNS or FCM.  
**Logic Description:** The `send_push` method receives device token, device type (e.g., 'ios', 'android'), and push content. Based on `device_type`, it routes the request to either APNSClient or FCMClient. Handles provider-specific formatting if necessary. Logs sending attempts and results. Implements retry logic for transient errors from providers.  
**Documentation:**
    
    - **Summary:** Handles the logic for sending push notifications, abstracting away the specific provider details.
    
**Namespace:** creativeflow.services.notification.core  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/services/notification/channels/__init__.py  
**Description:** Initializes the channels module.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** channels/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the channels module.
    
**Namespace:** creativeflow.services.notification.channels  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/channels/push/__init__.py  
**Description:** Initializes the push notification channel module.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** channels/push/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the push notification providers module.
    
**Namespace:** creativeflow.services.notification.channels.push  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/channels/push/base_push_provider.py  
**Description:** Abstract base class or interface (using ABC) defining the contract for push notification providers (APNS, FCM). Ensures a consistent interface for the PushNotificationService to interact with different providers.  
**Template:** Python Abstract Base Class  
**Dependency Level:** 1  
**Name:** base_push_provider  
**Type:** Interface  
**Relative Path:** channels/push/base_push_provider.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - StrategyPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** send  
**Parameters:**
    
    - device_token: str
    - payload: PushNotificationContent
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - Push Provider Abstraction
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications part)
    
**Purpose:** Defines a common interface for all push notification provider clients.  
**Logic Description:** Contains an abstract base class `BasePushProvider` with an abstract method `send(device_token, payload)`. Concrete provider clients (APNSClient, FCMClient) will implement this interface.  
**Documentation:**
    
    - **Summary:** Abstracts the common functionality required by push notification providers.
    
**Namespace:** creativeflow.services.notification.channels.push  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/channels/push/apns_client.py  
**Description:** Client for interacting with Apple Push Notification Service (APNS). Uses the 'apns2' library to send push notifications to iOS devices.  
**Template:** Python APNS Client  
**Dependency Level:** 2  
**Name:** apns_client  
**Type:** Adapter  
**Relative Path:** channels/push/apns_client.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** apns_client_instance  
**Type:** APNsClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - config: Settings
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** send  
**Parameters:**
    
    - device_token: str
    - payload: PushNotificationContent
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Implements BasePushProvider.  
    
**Implemented Features:**
    
    - APNS Push Notification Sending
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications part)
    
**Purpose:** Handles the specifics of sending push notifications via APNS.  
**Logic Description:** Initializes the `APNsClient` from the `apns2` library using configuration (cert, key_id, team_id, sandbox/production). The `send` method constructs the APNS notification payload from `PushNotificationContent` and sends it to the specified `device_token`. Handles APNS-specific error responses and logging.  
**Documentation:**
    
    - **Summary:** Provides functionality to send push notifications to iOS devices using APNS.
    
**Namespace:** creativeflow.services.notification.channels.push  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/channels/push/fcm_client.py  
**Description:** Client for interacting with Firebase Cloud Messaging (FCM). Uses the 'pyfcm' library to send push notifications to Android devices.  
**Template:** Python FCM Client  
**Dependency Level:** 2  
**Name:** fcm_client  
**Type:** Adapter  
**Relative Path:** channels/push/fcm_client.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** fcm_service_instance  
**Type:** FCMNotification  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - config: Settings
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** send  
**Parameters:**
    
    - device_token: str
    - payload: PushNotificationContent
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Implements BasePushProvider.  
    
**Implemented Features:**
    
    - FCM Push Notification Sending
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications part)
    
**Purpose:** Handles the specifics of sending push notifications via FCM.  
**Logic Description:** Initializes the `FCMNotification` service from the `pyfcm` library using the FCM API key from configuration. The `send` method constructs the FCM message payload from `PushNotificationContent` and sends it to the specified `device_token` (registration ID). Handles FCM-specific error responses and logging.  
**Documentation:**
    
    - **Summary:** Provides functionality to send push notifications to Android devices using FCM.
    
**Namespace:** creativeflow.services.notification.channels.push  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/messaging/__init__.py  
**Description:** Initializes the messaging consumers module.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** messaging/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the messaging consumers module.
    
**Namespace:** creativeflow.services.notification.messaging  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/messaging/message_handler.py  
**Description:** Contains common logic for processing messages received from various queues (RabbitMQ, Redis Pub/Sub). Parses messages, validates them against schemas, and forwards them to the NotificationManager for dispatch.  
**Template:** Python Message Handler  
**Dependency Level:** 5  
**Name:** message_handler  
**Type:** Service  
**Relative Path:** messaging/message_handler.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** notification_manager  
**Type:** NotificationManager  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** handle_message  
**Parameters:**
    
    - raw_message_body: bytes | str
    - message_source: str
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Processes a raw message, converting it to NotificationPayload.  
    
**Implemented Features:**
    
    - Message Parsing
    - Message Validation
    - Notification Triggering
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    - Section 5.3.1 (Role in AI generation pipeline notifications for user updates)
    
**Purpose:** Central point for processing incoming messages from queues before dispatching notifications.  
**Logic Description:** The `handle_message` method takes a raw message body. It attempts to parse the message (e.g., JSON decode), then validate it against the `NotificationPayload` schema. If valid, it calls `NotificationManager.send_notification`. Handles parsing/validation errors and logs them. `message_source` can be used for logging or context.  
**Documentation:**
    
    - **Summary:** Decodes, validates, and processes messages received from message queues, triggering notifications.
    
**Namespace:** creativeflow.services.notification.messaging  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** src/creativeflow/services/notification/messaging/rabbitmq_consumer.py  
**Description:** Consumes messages from RabbitMQ queues. Uses the 'pika' library to connect to RabbitMQ, declare queues/exchanges, and process incoming messages by forwarding them to the MessageHandler.  
**Template:** Python RabbitMQ Consumer  
**Dependency Level:** 6  
**Name:** rabbitmq_consumer  
**Type:** Adapter  
**Relative Path:** messaging/rabbitmq_consumer.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - MessageConsumer
    
**Members:**
    
    - **Name:** connection  
**Type:** pika.BlockingConnection  
**Attributes:** private  
    - **Name:** channel  
**Type:** pika.channel.Channel  
**Attributes:** private  
    - **Name:** message_handler  
**Type:** MessageHandler  
**Attributes:** private  
**Notes:** Injected dependency  
    - **Name:** config  
**Type:** Settings  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** start_consuming  
**Parameters:**
    
    - queue_name: str
    
**Return Type:** None  
**Attributes:** public  
**Notes:** Runs in a separate thread or asyncio task.  
    - **Name:** callback  
**Parameters:**
    
    - ch
    - method
    - properties
    - body
    
**Return Type:** None  
**Attributes:** private  
**Notes:** Message processing callback for pika.  
    
**Implemented Features:**
    
    - RabbitMQ Message Consumption
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Listens to specified RabbitMQ queues and processes incoming messages.  
**Logic Description:** Establishes a connection to RabbitMQ using connection URL from config. Declares necessary queues and exchanges (e.g., for AI generation updates). The `start_consuming` method registers a `callback` function for a specific queue. The `callback` function receives messages, acknowledges them (if processing is successful), and passes the message body to `MessageHandler.handle_message`. Implements connection retry logic and graceful shutdown.  
**Documentation:**
    
    - **Summary:** Handles consuming messages from RabbitMQ queues and processing them.
    
**Namespace:** creativeflow.services.notification.messaging  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/messaging/redis_consumer.py  
**Description:** Consumes messages from Redis Pub/Sub channels. Uses the 'redis' library (async version) to subscribe to channels and process incoming messages by forwarding them to the MessageHandler.  
**Template:** Python Redis PubSub Consumer  
**Dependency Level:** 6  
**Name:** redis_consumer  
**Type:** Adapter  
**Relative Path:** messaging/redis_consumer.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    - MessageConsumer
    - ObserverPattern
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.asyncio.Redis  
**Attributes:** private  
    - **Name:** pubsub  
**Type:** redis.asyncio.client.PubSub  
**Attributes:** private  
    - **Name:** message_handler  
**Type:** MessageHandler  
**Attributes:** private  
**Notes:** Injected dependency  
    - **Name:** config  
**Type:** Settings  
**Attributes:** private  
**Notes:** Injected dependency  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async|public  
    - **Name:** subscribe_and_listen  
**Parameters:**
    
    - channel_name: str
    
**Return Type:** None  
**Attributes:** async|public  
**Notes:** Runs as an asyncio task.  
    
**Implemented Features:**
    
    - Redis Pub/Sub Message Consumption
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component description)
    
**Purpose:** Listens to specified Redis Pub/Sub channels and processes incoming messages.  
**Logic Description:** Establishes an asynchronous connection to Redis using URL from config. The `subscribe_and_listen` method subscribes to a given channel using `redis_client.pubsub()`. It then continuously listens for messages. When a message is received, its data is passed to `MessageHandler.handle_message`. Implements connection retry logic and graceful shutdown.  
**Documentation:**
    
    - **Summary:** Handles consuming messages from Redis Pub/Sub channels and processing them.
    
**Namespace:** creativeflow.services.notification.messaging  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** src/creativeflow/services/notification/shared/__init__.py  
**Description:** Initializes the shared utilities module.  
**Template:** Python Package Initializer  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** shared/__init__.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the directory as a Python package.  
**Logic Description:** This file is typically empty.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer file for the shared utilities module.
    
**Namespace:** creativeflow.services.notification.shared  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/creativeflow/services/notification/shared/logger.py  
**Description:** Configures and provides a standardized logger instance for the application. Uses Python's built-in logging module, potentially with custom formatting and handlers.  
**Template:** Python Logger Configuration  
**Dependency Level:** 0  
**Name:** logger  
**Type:** Utility  
**Relative Path:** shared/logger.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_logger  
**Parameters:**
    
    - name: str
    
**Return Type:** logging.Logger  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Centralized Logging Setup
    
**Requirement Ids:**
    
    
**Purpose:** Provides a consistent logging interface throughout the application.  
**Logic Description:** Sets up a root logger or application-specific logger with desired formatting (e.g., timestamp, level, module name, message) and output handlers (e.g., console, file). The `get_logger` function returns a configured logger instance.  
**Documentation:**
    
    - **Summary:** Configures and provides access to the application logger.
    
**Namespace:** creativeflow.services.notification.shared.logging  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/creativeflow/services/notification/shared/exceptions.py  
**Description:** Defines custom exception classes specific to the notification service domain. This helps in handling errors more granularly and providing specific feedback.  
**Template:** Python Custom Exceptions  
**Dependency Level:** 0  
**Name:** exceptions  
**Type:** Utility  
**Relative Path:** shared/exceptions.py  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** NotificationDispatchError  
**Type:** Exception  
**Attributes:** public  
**Notes:** Base for dispatch errors.  
    - **Name:** PushProviderError  
**Type:** NotificationDispatchError  
**Attributes:** public  
**Notes:** For errors from APNS/FCM.  
    - **Name:** InvalidMessageFormatError  
**Type:** ValueError  
**Attributes:** public  
**Notes:** For malformed incoming messages.  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Error Handling
    
**Requirement Ids:**
    
    
**Purpose:** Provides custom exception types for better error management within the service.  
**Logic Description:** Defines a set of custom exception classes inheriting from Python's base `Exception` or more specific built-in exceptions. These are used to signal specific error conditions within the notification service's logic.  
**Documentation:**
    
    - **Summary:** Contains custom exception classes for the notification service.
    
**Namespace:** creativeflow.services.notification.shared.exceptions  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** requirements.txt  
**Description:** Lists all Python package dependencies for the Notification Service, along with their versions, for pip installation.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyManagement  
**Relative Path:** ../requirements.txt  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Declaration
    
**Requirement Ids:**
    
    
**Purpose:** Specifies project dependencies for reproducibility and environment setup.  
**Logic Description:** A plain text file listing required packages, one per line. Versions should be pinned for stable builds (e.g., fastapi==0.100.0, pika==1.3.2, redis==5.0.0, apns2==1.3.2, pyfcm==1.5.6, uvicorn==0.23.2, pydantic==2.0.0).  
**Documentation:**
    
    - **Summary:** Defines all external Python libraries required by the Notification Service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** pyproject.toml  
**Description:** Project metadata and build system configuration file, typically used with tools like Poetry or PDM. Defines project name, version, dependencies, and scripts.  
**Template:** Python Pyproject.toml  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** BuildConfiguration  
**Relative Path:** ../pyproject.toml  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Build Configuration
    - Dependency Management (if using Poetry/PDM)
    
**Requirement Ids:**
    
    
**Purpose:** Standard Python project definition file for modern packaging and build tools.  
**Logic Description:** Contains sections for [tool.poetry] or [project] defining metadata like name, version, authors, description. Specifies dependencies under [tool.poetry.dependencies] or [project.dependencies]. May include script definitions for running the application or tests.  
**Documentation:**
    
    - **Summary:** Defines project structure, dependencies, and build configurations for tools like Poetry or PDM.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment variable file showing the required configuration variables for running the Notification Service. Actual values should be in a .env file (not committed) or set in the deployment environment.  
**Template:** Environment Variables Example File  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:** ../.env.example  
**Repository Id:** REPO-NOTIFICATION-SERVICE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Guidance
    
**Requirement Ids:**
    
    
**Purpose:** Provides a template for developers and deployment scripts on required environment variables.  
**Logic Description:** A plain text file listing environment variables like RABBITMQ_URL, REDIS_URL, APNS_KEY_ID, APNS_TEAM_ID, APNS_CERT_PATH, APNS_USE_SANDBOX, FCM_API_KEY, LOG_LEVEL, etc., with placeholder or example values.  
**Documentation:**
    
    - **Summary:** Lists example environment variables needed to configure the Notification Service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - ENABLE_RABBITMQ_CONSUMER
  - ENABLE_REDIS_CONSUMER
  - ENABLE_APNS_PUSH
  - ENABLE_FCM_PUSH
  
- **Database Configs:**
  
  - RABBITMQ_URL
  - RABBITMQ_QUEUE_NAME_AI_UPDATES
  - REDIS_URL
  - REDIS_PUBSUB_CHANNEL_NAME
  - APNS_KEY_ID
  - APNS_TEAM_ID
  - APNS_CERT_FILE_PATH
  - APNS_USE_SANDBOX
  - FCM_API_KEY
  - LOG_LEVEL
  


---

