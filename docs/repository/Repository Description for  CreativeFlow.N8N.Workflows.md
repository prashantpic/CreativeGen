# Repository Specification

# 1. Name
CreativeFlow.N8N.Workflows


---

# 2. Description
This repository contains all n8n workflow definitions (JSON format) used by the CreativeFlow AI platform for AI orchestration (REQ-3-010). It includes workflows for AI creative generation, image processing, error handling logic within n8n, and communication with other services (e.g., Notification Service, Odoo via RabbitMQ). If any custom n8n nodes are developed (Python/Node.js), their source code would also reside here or in a linked sub-repository.


---

# 3. Type
WorkflowEngine


---

# 4. Namespace
CreativeFlow.N8N.Workflows


---

# 5. Output Path
workflows/n8n-creativeflow-workflows


---

# 6. Framework
n8n


---

# 7. Language
JSON (for workflows), Node.js/Python (for custom nodes)


---

# 8. Technology
n8n, RabbitMQ client nodes, HTTP request nodes, Kubernetes job submission nodes (if custom)


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- REPO-RABBITMQ-CONFIGURATION-001
- REPO-K8S-AISERVINGMANIFESTS-001
- REPO-MINIO-CONFIGURATION-001
- REPO-NOTIFICATION-SERVICE-001
- REPO-SECRETS-MANAGEMENT-001


---

# 11. Layer Ids



---

# 12. Requirements



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
REPO-N8N-WORKFLOWS-001


---

# 17. Architecture_Map

- layer.workflow.n8n


---

# 18. Components_Map

- n8n Workflow Engine & AI Orchestration Layer


---

# 19. Requirements_Map

- Section 1.1 (n8n workflow engine)
- Section 2.1 (n8n for AI processing)
- Section 3.2 (n8n based workflow)
- Section 5.2.2 (AI Processing Orchestration component as n8n)
- Section 5.3.1 (n8n role in pipeline)
- INT-005 (n8n interacts with AI services)
- INT-006 (n8n handles API keys for external AI)
- Appendix B (n8n Workflow Design Patterns)


---

