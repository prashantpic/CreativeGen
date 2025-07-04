# Repository Specification

# 1. Name
CreativeFlow.Infrastructure.IaC.Ansible


---

# 2. Description
This repository contains Infrastructure-as-Code (IaC) scripts, primarily using Ansible (DEP-004.1), to automate the provisioning, configuration, and ongoing management of all self-hosted Linux servers and their software stacks (OS, Nginx, PostgreSQL, Odoo, n8n, MinIO, Redis, RabbitMQ, Kubernetes cluster components, AI tools, monitoring agents like Prometheus exporters). These Ansible playbooks and roles ensure consistency, enable automated updates, track changes, and facilitate environment recreation across all environments (dev, staging, prod, DR as per DEP-004). Integrated into the CI/CD pipeline (DEP-003).


---

# 3. Type
InfrastructureAsCode


---

# 4. Namespace
CreativeFlow.Infrastructure.IaC


---

# 5. Output Path
infrastructure/ansible-iac-creativeflow


---

# 6. Framework
Ansible


---

# 7. Language
YAML, Python (for custom Ansible modules if any)


---

# 8. Technology
Ansible (Core 2.15+), Jinja2


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- REPO-SECRETS-MANAGEMENT-VAULT-001


---

# 11. Layer Ids



---

# 12. Requirements



---

# 13. Generate Tests
False


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
CloudNative


---

# 16. Id
REPO-INFRASTRUCTURE-IAC-ANSIBLE-001


---

# 17. Architecture_Map

- layer.infrastructure.hosting
- layer.infrastructure.cicd


---

# 18. Components_Map

- Self-hosted Linux servers
- Load Balancer (Nginx)
- Kubernetes Cluster (components)


---

# 19. Requirements_Map

- DEP-003 (IaC integration with CI/CD)
- DEP-004 (Consistent environments via IaC)
- DEP-004.1 (Ansible for IaC)
- DEP-005 (Maintenance procedures automated via Ansible)
- NFR-010 (Technical Documentation - deployment procedures part of IaC)


---

