# Specification

# 1. Files

- **Path:** src/creativeflow/service/notification/__init__.py  
**Description:** Initializes the 'notification' Python package, making it a recognizable package.  
**Template:** Python Service Template  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** creativeflow/service/notification  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python package structure
    
**Requirement Ids:**
    
    
**Purpose:** Defines the directory as a Python package, enabling imports of modules within it.  
**Logic Description:** This file is typically empty and serves only to mark the directory as a Python package.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer for the notification service.
    
**Namespace:** creativeflow.service.notification  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/main.py  
**Description:** The main entry point for the Notification Service application. It initializes the FastAPI application, sets up middleware, includes API routers, and defines startup and shutdown event handlers for connecting to message brokers and other resources.  
**Template:** Python Service Template  
**Dependency Level:** 5  
**Name:** main  
**Type:** Application Entrypoint  
**Relative Path:** creativeflow/service/notification  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Layered Architecture
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** global  
    
**Methods:**
    
    - **Name:** startup_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** shutdown_event  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - FastAPI Application Bootstrap
    - WebSocket Endpoint Routing
    - Message Queue Consumer Lifecycle Management
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component)
    
**Purpose:** To bootstrap and run the FastAPI-based Notification Service, configuring all necessary components and lifecycle events.  
**Logic Description:** Initializes a FastAPI instance. Includes the WebSocket router from the 'api' module. Defines a 'startup_event' to initialize and start the RabbitMQ consumer and Redis connection. Defines a 'shutdown_event' to gracefully close connections to the message broker and other resources. This ensures a clean lifecycle for the service.  
**Documentation:**
    
    - **Summary:** This file is the main executable for the Notification Service. It sets up the web server, WebSocket endpoints, and background consumers for processing notification events from message queues.
    
**Namespace:** creativeflow.service.notification  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/core/config.py  
**Description:** Handles all application configuration using Pydantic's BaseSettings. It loads settings from environment variables, providing a single, typed source of truth for all configurable parameters like database URLs, message broker connection details, and third-party API keys.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** config  
**Type:** Configuration  
**Relative Path:** creativeflow/service/notification/core  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** RABBITMQ_URL  
**Type:** str  
**Attributes:**   
    - **Name:** NOTIFICATION_QUEUE_NAME  
**Type:** str  
**Attributes:**   
    - **Name:** APNS_KEY_ID  
**Type:** str  
**Attributes:**   
    - **Name:** APNS_TEAM_ID  
**Type:** str  
**Attributes:**   
    - **Name:** APNS_AUTH_KEY_PATH  
**Type:** str  
**Attributes:**   
    - **Name:** FCM_PROJECT_ID  
**Type:** str  
**Attributes:**   
    - **Name:** FCM_CREDENTIALS_PATH  
**Type:** str  
**Attributes:**   
    - **Name:** LOG_LEVEL  
**Type:** str  
**Attributes:**   
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** lru_cache  
    
**Implemented Features:**
    
    - Centralized Configuration Management
    - Environment Variable Loading
    
**Requirement Ids:**
    
    
**Purpose:** To provide a centralized and validated configuration object for the entire application.  
**Logic Description:** Define a Pydantic 'Settings' class that inherits from BaseSettings. Each configuration parameter is defined as a class attribute with a type hint. Pydantic will automatically read these values from environment variables. A cached 'get_settings' function ensures the settings are loaded only once.  
**Documentation:**
    
    - **Summary:** This module defines and loads all necessary configuration for the Notification Service, ensuring that settings like connection strings and API keys are managed centrally and securely.
    
**Namespace:** creativeflow.service.notification.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/service/notification/core/dispatcher.py  
**Description:** The core component responsible for orchestrating the notification dispatch process. It receives an internal notification request, determines the appropriate channel(s) (WebSocket, Push), and delegates the sending task to the respective channel handlers.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** dispatcher  
**Type:** Service  
**Relative Path:** creativeflow/service/notification/core  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Strategy Pattern
    
**Members:**
    
    - **Name:** channel_handlers  
**Type:** Dict[str, NotificationChannel]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** dispatch_notification  
**Parameters:**
    
    - payload: NotificationPayload
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - Notification Orchestration
    - Channel Selection Logic
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications)
    - REQ-007.1 (User notification on AI errors)
    - REQ-013 (Collaboration updates notification)
    
**Purpose:** To decouple the event consumption logic from the specifics of how a notification is sent, allowing for flexible routing and handling.  
**Logic Description:** The 'NotificationDispatcher' class is initialized with a dictionary of available channel handlers (e.g., {'websocket': WebSocketChannel, 'push': PushNotificationChannel}). The 'dispatch_notification' method takes a payload, which includes recipient information and the message content. Based on the payload's metadata or recipient's device information, it selects the appropriate channel handler(s) and calls their 'send' method.  
**Documentation:**
    
    - **Summary:** This module contains the central dispatcher that routes incoming notification requests to the correct communication channel, such as WebSockets or mobile push services.
    
**Namespace:** creativeflow.service.notification.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/service/notification/shared/schemas.py  
**Description:** Defines the data contracts for the service. This includes Pydantic models for incoming message queue payloads and any data structures used in API responses. It serves as the formal interface definition for consumers of the service.  
**Template:** Python Service Template  
**Dependency Level:** 1  
**Name:** schemas  
**Type:** Schema  
**Relative Path:** creativeflow/service/notification/shared  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Data Transfer Object (DTO)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Validation
    - Service Contracts
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n informs Notification Service)
    
**Purpose:** To provide strongly-typed, validated data structures for all data entering or leaving the service, ensuring data integrity and clear contracts.  
**Logic Description:** Define Pydantic models for different event types. For example, 'AIGenerationCompletedPayload' with fields like 'user_id', 'status', 'asset_url'. Another could be 'CollaborationUpdatePayload' with 'project_id', 'updated_by_user', 'message'. These schemas are used by consumers and the API layer to parse and validate incoming data.  
**Documentation:**
    
    - **Summary:** Contains Pydantic schemas that define the structure and validation rules for data payloads consumed from message queues and used within the service's APIs.
    
**Namespace:** creativeflow.service.notification.shared  
**Metadata:**
    
    - **Category:** Shared
    
- **Path:** src/creativeflow/service/notification/channels/base.py  
**Description:** Defines the abstract base class (ABC) for all notification channels. This ensures that every channel implementation (WebSocket, Push, etc.) adheres to a common interface, promoting polymorphism and making the system extensible.  
**Template:** Python Service Template  
**Dependency Level:** 2  
**Name:** base  
**Type:** Interface  
**Relative Path:** creativeflow/service/notification/channels  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Strategy Pattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** send  
**Parameters:**
    
    - recipient: Recipient
    - payload: dict
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - Channel Abstraction
    
**Requirement Ids:**
    
    
**Purpose:** To enforce a consistent contract for all notification channels, facilitating a plug-and-play architecture.  
**Logic Description:** Define an abstract base class `NotificationChannel` using Python's `abc` module. It contains a single abstract async method `send` that takes recipient information and a message payload. All concrete channel classes must implement this method.  
**Documentation:**
    
    - **Summary:** This module provides the abstract base class that defines the common interface for all notification dispatch channels.
    
**Namespace:** creativeflow.service.notification.channels  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/channels/websocket/manager.py  
**Description:** Manages the state of all active WebSocket connections. Provides methods to connect, disconnect, and broadcast messages to specific users or all connected clients. This is a critical component for the real-time web UI updates.  
**Template:** Python Service Template  
**Dependency Level:** 3  
**Name:** manager  
**Type:** Manager  
**Relative Path:** creativeflow/service/notification/channels/websocket  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** active_connections  
**Type:** Dict[str, WebSocket]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** connect  
**Parameters:**
    
    - user_id: str
    - websocket: WebSocket
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** disconnect  
**Parameters:**
    
    - user_id: str
    
**Return Type:** None  
**Attributes:**   
    - **Name:** send_to_user  
**Parameters:**
    
    - user_id: str
    - message: str
    
**Return Type:** None  
**Attributes:** async  
    
**Implemented Features:**
    
    - WebSocket Connection Management
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component)
    
**Purpose:** To maintain a registry of active client connections, enabling targeted real-time communication.  
**Logic Description:** Implement a `ConnectionManager` class. It will use a dictionary to map user IDs to their active WebSocket connection objects. The 'connect' method adds a user's connection, 'disconnect' removes it. The 'send_to_user' method retrieves a user's connection from the dictionary and sends a message through it.  
**Documentation:**
    
    - **Summary:** Manages the pool of active WebSocket connections, allowing the service to send real-time messages to specific authenticated users connected via the web application.
    
**Namespace:** creativeflow.service.notification.channels.websocket  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/channels/websocket/channel.py  
**Description:** The concrete implementation of the NotificationChannel for WebSockets. It uses the ConnectionManager to deliver real-time messages to connected web clients.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** channel  
**Type:** Channel Implementation  
**Relative Path:** creativeflow/service/notification/channels/websocket  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** manager  
**Type:** ConnectionManager  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send  
**Parameters:**
    
    - recipient: Recipient
    - payload: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - WebSocket Message Dispatch
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component)
    
**Purpose:** To integrate WebSocket communication into the service's standard dispatch mechanism.  
**Logic Description:** Implement the `WebSocketChannel` class, inheriting from `NotificationChannel`. The constructor will take an instance of `ConnectionManager`. The `send` method will extract the user ID from the recipient, serialize the payload to a JSON string, and call the connection manager's `send_to_user` method.  
**Documentation:**
    
    - **Summary:** Implements the notification channel for sending real-time updates to users via WebSockets, utilizing the ConnectionManager.
    
**Namespace:** creativeflow.service.notification.channels.websocket  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/channels/push/channel.py  
**Description:** The concrete implementation of the NotificationChannel for mobile push notifications. It acts as a facade, delegating the actual sending to the appropriate provider (APNS or FCM) based on the recipient's device token type.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** channel  
**Type:** Channel Implementation  
**Relative Path:** creativeflow/service/notification/channels/push  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Facade Pattern
    
**Members:**
    
    - **Name:** apns_provider  
**Type:** APNSProvider  
**Attributes:** private  
    - **Name:** fcm_provider  
**Type:** FCMProvider  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send  
**Parameters:**
    
    - recipient: Recipient
    - payload: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Push Notification Dispatch Logic
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications)
    
**Purpose:** To provide a single entry point for sending push notifications, abstracting away the specifics of different mobile platforms.  
**Logic Description:** Implement the `PushNotificationChannel` class, inheriting from `NotificationChannel`. The `send` method will check the recipient's device information (e.g., a token prefix or device OS field) to determine if it's an iOS (APNS) or Android (FCM) device. It will then call the corresponding provider's `send_push` method, passing the formatted message.  
**Documentation:**
    
    - **Summary:** Implements the notification channel for sending mobile push notifications. It determines the target platform (iOS or Android) and uses the appropriate provider to dispatch the message.
    
**Namespace:** creativeflow.service.notification.channels.push  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** src/creativeflow/service/notification/channels/push/providers/base.py  
**Description:** Defines the abstract base class for all push notification providers (e.g., APNS, FCM). This ensures that new providers can be added easily by adhering to a consistent interface.  
**Template:** Python Service Template  
**Dependency Level:** 3  
**Name:** base  
**Type:** Interface  
**Relative Path:** creativeflow/service/notification/channels/push/providers  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Adapter Pattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** send_push  
**Parameters:**
    
    - device_token: str
    - title: str
    - body: str
    - data: dict
    
**Return Type:** None  
**Attributes:** public|abstractmethod|async  
    
**Implemented Features:**
    
    - Push Provider Abstraction
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications)
    
**Purpose:** To create a common contract for all third-party push notification services, decoupling the push channel from specific SDKs.  
**Logic Description:** Define an abstract base class `PushProvider` using Python's `abc` module. It contains a single abstract async method `send_push` that takes a device token and message components. Concrete provider classes will implement this method.  
**Documentation:**
    
    - **Summary:** This module provides the abstract base class that defines the common interface for all push notification provider adapters (e.g., APNS, FCM).
    
**Namespace:** creativeflow.service.notification.channels.push.providers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/notification/channels/push/providers/apns.py  
**Description:** Adapter for sending push notifications to iOS devices via Apple Push Notification Service (APNS). This class encapsulates the logic and SDK usage for communicating with APNS.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** apns  
**Type:** Provider Adapter  
**Relative Path:** creativeflow/service/notification/channels/push/providers  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Adapter Pattern
    
**Members:**
    
    - **Name:** client  
**Type:** APNsClient  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** send_push  
**Parameters:**
    
    - device_token: str
    - title: str
    - body: str
    - data: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - APNS Integration
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications)
    
**Purpose:** To handle all interactions with Apple's push notification service.  
**Logic Description:** Implement the `APNSProvider` class, inheriting from `PushProvider`. The constructor initializes the `APNsClient` from the `apns2` library using credentials from the central config. The `send_push` method constructs the APNS payload (alert title, body, sound, badge, custom data) and uses the client to send the notification to the provided device token.  
**Documentation:**
    
    - **Summary:** An adapter that implements the push provider interface for Apple Push Notification Service (APNS), handling the specifics of sending notifications to iOS devices.
    
**Namespace:** creativeflow.service.notification.channels.push.providers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/notification/channels/push/providers/fcm.py  
**Description:** Adapter for sending push notifications to Android devices via Firebase Cloud Messaging (FCM). This class encapsulates the logic and SDK usage for communicating with FCM.  
**Template:** Python Service Template  
**Dependency Level:** 4  
**Name:** fcm  
**Type:** Provider Adapter  
**Relative Path:** creativeflow/service/notification/channels/push/providers  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Adapter Pattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** send_push  
**Parameters:**
    
    - device_token: str
    - title: str
    - body: str
    - data: dict
    
**Return Type:** None  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - FCM Integration
    
**Requirement Ids:**
    
    - REQ-020 (Push notifications)
    
**Purpose:** To handle all interactions with Google's Firebase Cloud Messaging service.  
**Logic Description:** Implement the `FCMProvider` class, inheriting from `PushProvider`. The constructor initializes the Firebase Admin SDK using credentials from the central config. The `send_push` method constructs the FCM message payload (notification title, body, custom data) and uses the `firebase_admin.messaging` module to send the notification to the provided device token.  
**Documentation:**
    
    - **Summary:** An adapter that implements the push provider interface for Firebase Cloud Messaging (FCM), handling the specifics of sending notifications to Android devices.
    
**Namespace:** creativeflow.service.notification.channels.push.providers  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/notification/entrypoints/api.py  
**Description:** Defines the FastAPI API endpoints for the service. This primarily includes the WebSocket endpoint for real-time client connections and a health check endpoint.  
**Template:** Python Service Template  
**Dependency Level:** 5  
**Name:** api  
**Type:** Controller  
**Relative Path:** creativeflow/service/notification/entrypoints  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:**   
    - **Name:** connection_manager  
**Type:** ConnectionManager  
**Attributes:**   
    
**Methods:**
    
    - **Name:** websocket_endpoint  
**Parameters:**
    
    - websocket: WebSocket
    - user_id: str
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** health_check  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** sync  
    
**Implemented Features:**
    
    - WebSocket Gateway
    - Health Check API
    
**Requirement Ids:**
    
    - Section 5.2.2 (Notification Service Component)
    
**Purpose:** To expose the service's real-time communication capabilities and provide a basic health check for monitoring.  
**Logic Description:** Create a FastAPI `APIRouter`. Define a WebSocket endpoint at a path like '/ws/{user_id}'. This function will accept a new connection, add it to the `ConnectionManager`, and then loop indefinitely, listening for any messages from the client (though in this service, communication is primarily server-to-client). It must handle client disconnects gracefully by removing them from the manager. Also include a simple GET endpoint for health checks.  
**Documentation:**
    
    - **Summary:** This module sets up the FastAPI router, defining the WebSocket endpoint for clients to connect for real-time notifications and a standard health check endpoint.
    
**Namespace:** creativeflow.service.notification.entrypoints  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** src/creativeflow/service/notification/entrypoints/consumers.py  
**Description:** Contains the logic for consuming messages from asynchronous message brokers like RabbitMQ. It listens for events published by other microservices, parses them, and passes them to the core dispatcher for handling.  
**Template:** Python Service Template  
**Dependency Level:** 5  
**Name:** consumers  
**Type:** Message Consumer  
**Relative Path:** creativeflow/service/notification/entrypoints  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    - Event-Driven Architecture (EDA)
    
**Members:**
    
    
**Methods:**
    
    - **Name:** start_rabbitmq_consumer  
**Parameters:**
    
    - dispatcher: NotificationDispatcher
    
**Return Type:** None  
**Attributes:** async  
    - **Name:** on_message_callback  
**Parameters:**
    
    - channel
    - method
    - properties
    - body
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - RabbitMQ Message Consumption
    - Event-Driven Notification Trigger
    
**Requirement Ids:**
    
    - Section 5.3.1 (n8n informs Notification Service)
    - REQ-007.1 (User notification on AI errors)
    - REQ-013 (Collaboration updates notification)
    
**Purpose:** To act as the primary asynchronous entry point, decoupling the Notification Service from its producers.  
**Logic Description:** Implement a function or class to manage the RabbitMQ connection using the 'pika' library. The 'start_rabbitmq_consumer' function connects to the broker, declares the queue specified in the config, and registers the 'on_message_callback' function. The callback function receives the raw message body, decodes it, parses it into the appropriate Pydantic schema from 'shared.schemas', and then calls the dispatcher's 'dispatch_notification' method. It also handles message acknowledgements (ack/nack) for reliability.  
**Documentation:**
    
    - **Summary:** Handles consumption of events from RabbitMQ. This module listens for messages published by other services (e.g., AI generation complete, collaboration update), validates them, and triggers the notification dispatch process.
    
**Namespace:** creativeflow.service.notification.entrypoints  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/service/notification/shared/logging.py  
**Description:** Configures the application's logging framework. It sets up structured logging (e.g., JSON format) to ensure logs are machine-parseable and can be easily ingested and searched by a central logging system like ELK or Loki.  
**Template:** Python Service Template  
**Dependency Level:** 2  
**Name:** logging  
**Type:** Utility  
**Relative Path:** creativeflow/service/notification/shared  
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logging  
**Parameters:**
    
    - log_level: str
    
**Return Type:** None  
**Attributes:**   
    
**Implemented Features:**
    
    - Structured Logging
    
**Requirement Ids:**
    
    
**Purpose:** To standardize logging across the entire service for better observability and troubleshooting.  
**Logic Description:** A `setup_logging` function configures the root logger. It removes any default handlers and adds a new handler that uses a specialized formatter (like `python-json-logger`) to output logs in a structured JSON format. The log level is set based on the application's configuration. This ensures consistency in log output.  
**Documentation:**
    
    - **Summary:** Provides a centralized function to configure structured (JSON) logging for the application, ensuring consistent and machine-readable log output across all modules.
    
**Namespace:** creativeflow.service.notification.shared  
**Metadata:**
    
    - **Category:** Shared
    
- **Path:** pyproject.toml  
**Description:** Defines project metadata, dependencies, and build system configuration for the Python project, following PEP 517/518 standards. Managed by a tool like Poetry or standard setuptools.  
**Template:** Python Service Template  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Metadata
    - Dependency Management
    - Build Configuration
    
**Requirement Ids:**
    
    
**Purpose:** To declare the project's dependencies and configuration in a standardized way, enabling reproducible builds and development environments.  
**Logic Description:** This file will contain sections for `[tool.poetry]` or `[project]` to define the project name, version, and authors. The `[tool.poetry.dependencies]` section will list all required libraries like `fastapi`, `uvicorn`, `websockets`, `pika`, `redis`, `apns2`, `firebase-admin`, and `pydantic` with their version constraints.  
**Documentation:**
    
    - **Summary:** Standard Python project definition file, specifying metadata, dependencies, and tool configurations for the Notification Service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** Dockerfile  
**Description:** A multi-stage Dockerfile to build a production-ready, optimized, and secure container image for the Notification Service. It handles dependency installation, copies the application code, and defines the final runtime environment.  
**Template:** Python Service Template  
**Dependency Level:** 6  
**Name:** Dockerfile  
**Type:** Build Configuration  
**Relative Path:**   
**Repository Id:** REPO-SERVICE-NOTIFICATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization
    - Production Build
    
**Requirement Ids:**
    
    
**Purpose:** To create a standardized, reproducible, and portable container for deploying the Notification Service.  
**Logic Description:** The Dockerfile will use a multi-stage build. The first stage ('builder') uses a full Python image to install dependencies from `pyproject.toml` (or `requirements.txt`). The final stage uses a slim Python base image, copies the installed dependencies from the 'builder' stage, and then copies the application source code. It sets a working directory, exposes the necessary port (e.g., 8000), and defines the `CMD` to run the application using `uvicorn`.  
**Documentation:**
    
    - **Summary:** Defines the steps to build a Docker container image for deploying the Notification Service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableWebSocketChannel
  - enablePushNotificationChannel
  
- **Database Configs:**
  
  


---

