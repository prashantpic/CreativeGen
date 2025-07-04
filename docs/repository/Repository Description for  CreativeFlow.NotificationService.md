# Repository Specification

# 1. Name
CreativeFlow.NotificationService


---

# 2. Description
A dedicated lightweight microservice managing and delivering real-time updates and notifications. It handles WebSocket connections for web frontend updates (e.g., AI generation progress, collaboration updates) and sends push notifications via APNS/FCM for mobile applications. It consumes messages from RabbitMQ or Redis Pub/Sub triggered by other backend services. Exposes WebSocket endpoints and interacts with push notification gateways.


---

# 3. Type
NotificationService


---

# 4. Namespace
CreativeFlow.Services.Notification


---

# 5. Output Path
services/notification-service


---

# 6. Framework
FastAPI (WebSockets) or Node.js (Socket.IO)


---

# 7. Language
Python or Node.js


---

# 8. Technology
Python 3.11+/FastAPI with WebSockets or Node.js/Express with Socket.IO, APNS SDK, FCM SDK, Pika/Redis client


---

# 9. Thirdparty Libraries

- fastapi
- websockets
- uvicorn
- pika
- redis
- apns2
- pyfcm
- socket.io


---

# 10. Dependencies

- REPO-RABBITMQ-BROKER-001
- REPO-REDIS-CACHE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.notification


---

# 12. Requirements

- **Requirement Id:** REQ-020 (Push notifications)  
- **Requirement Id:** Section 5.2.2 (Notification Service Component)  
- **Requirement Id:** Section 5.3.1 (Role in AI gen pipeline notifications)  


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
REPO-NOTIFICATION-SERVICE-001


---

# 17. Architecture_Map

- layer.service.notification


---

# 18. Components_Map

- comp.service.notification
- comp.messaging.rabbitmq
- comp.datastore.redis


---

# 19. Requirements_Map

- REQ-020 (Push notifications part)
- Section 5.2.2 (Notification Service Component description)
- Section 5.3.1 (Role in AI generation pipeline notifications for user updates)


---

