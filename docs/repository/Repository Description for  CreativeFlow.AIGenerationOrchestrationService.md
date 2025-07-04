# Repository Specification

# 1. Name
CreativeFlow.AIGenerationOrchestrationService


---

# 2. Description
A microservice that orchestrates the AI creative generation pipeline. It receives generation requests (often originating from Odoo business logic), validates them, checks user credits/subscriptions, prepares job parameters, and publishes jobs to RabbitMQ for consumption by the n8n Workflow Engine. It also tracks generation status, handles results from n8n (samples, final assets), and triggers notifications. Exposes internal APIs for initiating and monitoring generation tasks.


---

# 3. Type
Microservice


---

# 4. Namespace
CreativeFlow.Services.AIGeneration


---

# 5. Output Path
services/aigen-orchestration-service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, FastAPI, Pydantic, Pika (RabbitMQ client)


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- pydantic
- pika


---

# 10. Dependencies

- REPO-RABBITMQ-BROKER-001
- REPO-N8N-WORKFLOW-ENGINE-001
- REPO-POSTGRES-DB-001
- REPO-SUBBILLING-ADAPTER-001
- REPO-NOTIFICATION-SERVICE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.application


---

# 12. Requirements

- **Requirement Id:** REQ-005  
- **Requirement Id:** REQ-006  
- **Requirement Id:** REQ-007  
- **Requirement Id:** REQ-007.1  
- **Requirement Id:** REQ-008  
- **Requirement Id:** REQ-009  
- **Requirement Id:** REQ-016 (Credit deduction coordination)  
- **Requirement Id:** Section 3.2  
- **Requirement Id:** Section 5.3.1 (Creative Generation Pipeline)  


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
REPO-AIGEN-ORCH-SERVICE-001


---

# 17. Architecture_Map

- layer.service.application


---

# 18. Components_Map

- comp.messaging.rabbitmq
- comp.workflow.n8n
- comp.datastore.postgres
- comp.backend.odoo (as originator of jobs)


---

# 19. Requirements_Map

- REQ-005
- REQ-006
- REQ-007
- REQ-007.1
- REQ-008
- REQ-009
- REQ-016 (Credit deduction coordination)
- Section 3.2 (Creative Generation Engine)
- Section 5.3.1 (Creative Generation Pipeline role)


---

