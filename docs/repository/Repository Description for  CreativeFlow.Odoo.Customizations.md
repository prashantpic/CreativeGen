# Repository Specification

# 1. Name
CreativeFlow.Odoo.Customizations


---

# 2. Description
This repository houses all custom Odoo 18+ modules developed for the CreativeFlow AI platform. This includes modules for specialized platform logic related to brand kit management extensions, workbench organization rules, the credit system logic (REQ-016), specific subscription handling rules beyond standard Odoo Sales, and any necessary customizations to Odoo's Helpdesk and Knowledge modules (REQ-021) to align with CreativeFlow's branding and workflows. These modules extend Odoo's core functionality.


---

# 3. Type
BusinessLogic


---

# 4. Namespace
CreativeFlow.Odoo.Custom


---

# 5. Output Path
erp/odoo-creativeflow-custom


---

# 6. Framework
Odoo


---

# 7. Language
Python


---

# 8. Technology
Odoo 18+ (or latest stable), XML (for views and data), JavaScript (for Odoo frontend extensions)


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- REPO-POSTGRESQL-SCHEMA-001 (Odoo's own DB)


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
Monolithic


---

# 16. Id
REPO-ODOO-CUSTOMIZATIONS-001


---

# 17. Architecture_Map

- layer.business.odoo


---

# 18. Components_Map

- Odoo 18+ Backend (Business Logic)
- User Management (Odoo Mod.)
- Billing & Subscription (Odoo Mod.)
- Content Management (Odoo Mod.)


---

# 19. Requirements_Map

- Section 2.1 (Odoo for business logic)
- Section 3.4 (Subscription logic in Odoo)
- Section 3.7 (Helpdesk in Odoo)
- Section 5.2.2 (Business Logic component, Custom Odoo Modules)
- REQ-016 (Credit system logic potentially in Odoo)
- REQ-021 (Odoo Helpdesk/Knowledge module leverage)


---

