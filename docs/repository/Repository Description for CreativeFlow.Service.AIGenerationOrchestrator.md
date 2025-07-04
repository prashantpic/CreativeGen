# Repository Specification

# 1. Name
CreativeFlow.Service.AIGenerationOrchestrator


---

# 2. Description
A central backend service that orchestrates the AI creative generation process. It receives requests from the API Gateway, validates them against user subscriptions and credits (by coordinating with the Odoo Backend / CoreBusiness Service), prepares job parameters, and then publishes these jobs to RabbitMQ for consumption by the n8n Workflow Engine. It also tracks the status of ongoing generation requests, processes results returned asynchronously from n8n (e.g., sample previews, final asset URLs), updates the database, and triggers notifications to users via the Notification Service. This service acts as the primary coordinator for the complex AI generation pipeline, decoupling the frontend/API Gateway from the intricacies of n8n and AI model interactions.


---

# 3. Type
ApplicationService


---

# 4. Namespace
CreativeFlow.Service


---

# 5. Output Path
services/ai_generation_orchestrator


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python, FastAPI, SQLAlchemy (for tracking generation requests), Pika (RabbitMQ client), Redis client (for status tracking/caching potentially)


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- sqlalchemy
- pika
- redis


---

# 10. Dependencies

- REPO-GATEWAY-API-001
- REPO-SERVICE-COREBUSINESS-ODOO-001
- REPO-INFRA-RABBITMQ-CONFIG-001
- REPO-SERVICE-AIORCH-N8N-001
- REPO-SERVICE-NOTIFICATION-001
- REPO-DB-POSTGRESQL-SCHEMA-001


---

# 11. Layer Ids

- layer.application.service


---

# 12. Requirements

- **Requirement Id:** Section 5.3.1 (Steps 2, 3, 4, 6, 7, 10 involving Odoo interaction, job publishing, status updates)  
- **Requirement Id:** REQ-007.1 (Error handling for AI generation)  
- **Requirement Id:** REQ-016 (Credit deduction coordination)  


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
REPO-SERVICE-AIGEN-ORCH-001


---

# 17. Architecture_Map

- archmap.service.aigenorchestrator


---

# 18. Components_Map

- comp.service.aigenorchestrator
- comp.service.aigenorchestrator.requestvalidator
- comp.service.aigenorchestrator.jobdispatcher
- comp.service.aigenorchestrator.statustracker


---

# 19. Requirements_Map

- Section 5.3.1 (Coordination Role)
- REQ-007.1 (AI Error Handling)
- REQ-016 (Credit Deduction)


---

