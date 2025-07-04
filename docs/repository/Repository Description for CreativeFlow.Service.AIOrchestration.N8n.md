# Repository Specification

# 1. Name
CreativeFlow.Service.AIOrchestration.N8n


---

# 2. Description
Contains all n8n workflow definitions, custom n8n nodes (if any), and configurations for the AI Processing Orchestration layer. This repository manages the sequence of AI tasks including prompt engineering, AI model selection (OpenAI, Stability AI, custom models), interaction with GPU-accelerated models via Kubernetes, image post-processing, and communication of results to the Notification Service and Odoo (asynchronously via RabbitMQ). These workflows are triggered by messages from RabbitMQ, originating from the Odoo backend or AI Generation Orchestrator service.


---

# 3. Type
WorkflowEngine


---

# 4. Namespace
CreativeFlow.Service.N8n


---

# 5. Output Path
services/n8n_workflows_creativeflow


---

# 6. Framework
n8n


---

# 7. Language
JSON (n8n workflows), JavaScript/TypeScript (custom nodes)


---

# 8. Technology
n8n, RabbitMQ consumer nodes, HTTP request nodes, Kubernetes job submission nodes (custom or community), MinIO interaction nodes


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- REPO-INFRA-RABBITMQ-CONFIG-001
- REPO-INFRA-KUBERNETES-CONFIG-001
- REPO-INFRA-MINIO-CONFIG-001
- REPO-SERVICE-NOTIFICATION-001
- REPO-OPENAI-API-INTEGRATION-IMPLICIT-001
- REPO-STABILITYAI-API-INTEGRATION-IMPLICIT-001


---

# 11. Layer Ids

- layer.workflow
- layer.application.service


---

# 12. Requirements

- **Requirement Id:** Section 2.1 (n8n for AI processing orchestration)  
- **Requirement Id:** Section 3.2 (Creative Generation Engine)  
- **Requirement Id:** Section 5.2.2 (AI Processing Orchestration: n8n)  
- **Requirement Id:** Section 5.3.1 (Creative Generation Pipeline details)  
- **Requirement Id:** REQ-005  
- **Requirement Id:** REQ-006  
- **Requirement Id:** REQ-007  
- **Requirement Id:** REQ-008  
- **Requirement Id:** REQ-009  
- **Requirement Id:** INT-005  
- **Requirement Id:** INT-007  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
EventDriven


---

# 16. Id
REPO-SERVICE-AIORCH-N8N-001


---

# 17. Architecture_Map

- archmap.backend.n8n


---

# 18. Components_Map

- comp.backend.n8n.aiorchestration
- comp.backend.n8n.workflows
- comp.backend.n8n.customnodes


---

# 19. Requirements_Map

- Section 2.1 (n8n Orchestration)
- Section 3.2 (Creative Gen Engine)
- Section 5.3.1 (Pipeline Details)
- REQ-005
- REQ-008
- INT-005


---

