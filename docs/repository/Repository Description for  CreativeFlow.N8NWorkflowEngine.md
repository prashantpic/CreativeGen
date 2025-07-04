# Repository Specification

# 1. Name
CreativeFlow.N8NWorkflowEngine


---

# 2. Description
The n8n workflow engine instance, responsible for orchestrating the AI creative generation and image processing jobs. It consumes job messages from RabbitMQ, executes defined workflows involving data pre-processing, AI model selection, interaction with AI models (custom on Kubernetes or third-party APIs like OpenAI/Stability AI), and communicates results to the Notification Service and Odoo (asynchronously). This repository conceptually covers the configuration and custom n8n nodes/workflows specific to CreativeFlow.


---

# 3. Type
WorkflowEngine


---

# 4. Namespace
CreativeFlow.N8N


---

# 5. Output Path
workflows/n8n-creativeflow


---

# 6. Framework
n8n


---

# 7. Language
Node.js


---

# 8. Technology
n8n, RabbitMQ client, HTTP clients, Kubernetes client (for custom nodes if any)


---

# 9. Thirdparty Libraries

- Various n8n community/core nodes


---

# 10. Dependencies

- REPO-RABBITMQ-BROKER-001
- REPO-K8S-AI-SERVING-001
- REPO-MINIO-STORAGE-001
- REPO-NOTIFICATION-SERVICE-001


---

# 11. Layer Ids

- layer.workflow.n8n


---

# 12. Requirements

- **Requirement Id:** Section 1.1 (n8n workflow engine use)  
- **Requirement Id:** Section 2.1 (n8n for AI processing)  
- **Requirement Id:** Section 3.2 (n8n based workflow)  
- **Requirement Id:** Section 5.2.2 (AI Processing Orchestration component)  
- **Requirement Id:** Section 5.3.1 (n8n role in pipeline)  
- **Requirement Id:** INT-005  
- **Requirement Id:** INT-006  


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
REPO-N8N-WORKFLOW-ENGINE-001


---

# 17. Architecture_Map

- layer.workflow.n8n


---

# 18. Components_Map

- comp.workflow.n8n
- comp.messaging.rabbitmq
- comp.infra.aiprocessing.k8s
- comp.datastore.minio


---

# 19. Requirements_Map

- Section 1.1 (n8n workflow engine use reference)
- Section 2.1 (n8n for AI processing orchestration)
- Section 3.2 (Creative Generation Engine based on n8n workflow)
- Section 5.2.2 (AI Processing Orchestration component as n8n)
- Section 5.3.1 (n8n role in Creative Generation Pipeline)
- INT-005
- INT-006


---

