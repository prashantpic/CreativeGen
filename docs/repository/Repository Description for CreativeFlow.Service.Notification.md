# Repository Specification

# 1. Name
CreativeFlow.Service.Notification


---

# 2. Description
A dedicated backend service responsible for managing and delivering real-time updates and notifications to users. It handles WebSocket connections for web clients and coordinates with APNS/FCM for push notifications to mobile clients. This service consumes messages from RabbitMQ or Redis Pub/Sub, which are published by other backend services (e.g., AI Generation Orchestrator upon task completion, Collaboration Service for updates). It translates these internal events into user-facing notifications.


---

# 3. Type
NotificationService


---

# 4. Namespace
CreativeFlow.Service


---

# 5. Output Path
services/notification_service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python, FastAPI, WebSockets (e.g., `websockets` library), APNS SDK, FCM SDK, Pika (RabbitMQ client), Redis client


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- websockets
- apns2
- firebase-admin
- pika
- redis


---

# 10. Dependencies

- REPO-INFRA-RABBITMQ-CONFIG-001
- REPO-INFRA-REDIS-CONFIG-001
- REPO-SERVICE-COREBUSINESS-ODOO-001


---

# 11. Layer Ids

- layer.application.service


---

# 12. Requirements

- **Requirement Id:** REQ-020 (Push notifications)  
- **Requirement Id:** Section 5.2.2 (Notification Service Component)  
- **Requirement Id:** REQ-007.1 (User notification on AI errors)  
- **Requirement Id:** Section 5.3.1 (n8n informs Notification Service)  
- **Requirement Id:** REQ-013 (Collaboration updates notification)  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
Microservices


---

# 16. Id
REPO-SERVICE-NOTIFICATION-001


---

# 17. Architecture_Map

- archmap.service.notification


---

# 18. Components_Map

- comp.service.notification
- comp.service.notification.websocket
- comp.service.notification.pushgateway


---

# 19. Requirements_Map

- REQ-020 (Push Notifications)
- Section 5.2.2 (Notification Service Component)
- Section 5.3.1 (n8n informs Notification Service)


---

