# Repository Specification

# 1. Name
CreativeFlow.RabbitMQBroker


---

# 2. Description
Configuration and management scripts for the RabbitMQ message broker cluster. RabbitMQ manages asynchronous job queues between Odoo, n8n, AI generation services, and other backend components, ensuring reliable, asynchronous task processing and high availability of queues and messages.


---

# 3. Type
Messaging


---

# 4. Namespace
CreativeFlow.Messaging.RabbitMQ


---

# 5. Output Path
messaging/rabbitmq-config


---

# 6. Framework
RabbitMQCTL


---

# 7. Language
Shell, Python (for scripts)


---

# 8. Technology
RabbitMQ


---

# 9. Thirdparty Libraries



---

# 10. Dependencies



---

# 11. Layer Ids

- layer.messaging.queue


---

# 12. Requirements

- **Requirement Id:** Section 2.1 (RabbitMQ for async)  
- **Requirement Id:** Section 5.1 (RabbitMQ in Arch)  
- **Requirement Id:** Section 5.2.2 (Job Queue Management component)  
- **Requirement Id:** Section 5.3.1 (RabbitMQ in pipeline)  
- **Requirement Id:** NFR-005 (Asynchronous processing via queues)  
- **Requirement Id:** DEP-001 (RabbitMQ Server specs)  


---

# 13. Generate Tests
False


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
LayeredArchitecture


---

# 16. Id
REPO-RABBITMQ-BROKER-001


---

# 17. Architecture_Map

- layer.messaging.queue


---

# 18. Components_Map

- comp.messaging.rabbitmq


---

# 19. Requirements_Map

- Section 2.1 (RabbitMQ for asynchronous messaging queues)
- Section 5.1 (RabbitMQ in Architecture Diagram)
- Section 5.2.2 (Job Queue Management component as RabbitMQ)
- Section 5.3.1 (RabbitMQ role in Creative Generation Pipeline)
- NFR-005 (Asynchronous processing via message queues)
- DEP-001 (Message Queue Server infrastructure reqs)


---

