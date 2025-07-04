# Repository Specification

# 1. Name
CreativeFlow.Service.CoreBusiness.Odoo


---

# 2. Description
This repository contains the Odoo 18+ backend application and all custom-developed Odoo modules that implement the core business logic for CreativeFlow AI. This includes User Management (profiles, roles), Subscription and Billing management (plans, payments, credit system integration via Odoo Sales/CRM/Invoicing), Content Management (workbench organization, project metadata - though assets themselves are in MinIO), and the Customer Support system (Helpdesk and Knowledge Base modules). It exposes functionalities via REST APIs (consumed by the API Gateway or other services) and interacts asynchronously via RabbitMQ for tasks like initiating AI generation jobs. This is a central hub for business rules and data.


---

# 3. Type
BusinessLogic


---

# 4. Namespace
CreativeFlow.Service.Odoo


---

# 5. Output Path
services/odoo_creativeflow


---

# 6. Framework
Odoo


---

# 7. Language
Python


---

# 8. Technology
Odoo 18+, Python, XML (Odoo views/data), PostgreSQL (Odoo's DB), RabbitMQ integration


---

# 9. Thirdparty Libraries

- Odoo Core Libraries
- pika (for RabbitMQ)
- stripe
- paypal (Odoo connectors or custom integration code)


---

# 10. Dependencies

- REPO-DB-POSTGRESQL-SCHEMA-001
- REPO-INFRA-RABBITMQ-CONFIG-001
- REPO-PAYMENT-STRIPE-INTEGRATION-IMPLICIT-001
- REPO-PAYMENT-PAYPAL-INTEGRATION-IMPLICIT-001


---

# 11. Layer Ids

- layer.application.service
- layer.domain.core


---

# 12. Requirements

- **Requirement Id:** Section 2.1 (Backend: Odoo 18+)  
- **Requirement Id:** Section 3.1 (User Management System)  
- **Requirement Id:** Section 3.4 (Subscription and Billing)  
- **Requirement Id:** Section 3.7 (Support and Help System)  
- **Requirement Id:** Section 5.2.2 (Business Logic: Odoo)  
- **Requirement Id:** REQ-001  
- **Requirement Id:** REQ-002  
- **Requirement Id:** REQ-003  
- **Requirement Id:** REQ-004  
- **Requirement Id:** REQ-014  
- **Requirement Id:** REQ-015  
- **Requirement Id:** REQ-016  
- **Requirement Id:** REQ-021  
- **Requirement Id:** INT-003 (Tax calculation via Odoo)  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
ServiceOriented


---

# 16. Id
REPO-SERVICE-COREBUSINESS-ODOO-001


---

# 17. Architecture_Map

- archmap.backend.odoo


---

# 18. Components_Map

- comp.backend.odoo.businesslogic
- comp.backend.odoo.usermgmt
- comp.backend.odoo.billing
- comp.backend.odoo.contentmgmt
- comp.backend.odoo.helpdesk
- comp.backend.odoo.custommodules


---

# 19. Requirements_Map

- Section 2.1 (Odoo Backend)
- Section 3.1 (User Mgmt)
- Section 3.4 (Subscription/Billing)
- Section 3.7 (Support System)
- REQ-016 (Credit System Logic)


---

