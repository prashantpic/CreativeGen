# Repository Specification

# 1. Name
CreativeFlow.UserProfileService


---

# 2. Description
A microservice managing user profiles, preferences, and data privacy compliance. Handles creation and updates to user profile information, management of UI preferences, progressive profiling, implementation of GDPR/CCPA data subject rights (access, portability, erasure), and consent management for data processing activities. Exposes internal REST APIs.


---

# 3. Type
Microservice


---

# 4. Namespace
CreativeFlow.Services.UserProfile


---

# 5. Output Path
services/userprofile-service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, FastAPI, SQLAlchemy, Pydantic


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- pydantic


---

# 10. Dependencies

- REPO-POSTGRES-DB-001
- REPO-AUTH-SERVICE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.application


---

# 12. Requirements

- **Requirement Id:** REQ-004  
- **Requirement Id:** SEC-004 (Privacy compliance)  
- **Requirement Id:** NFR-006 (Data protection)  
- **Requirement Id:** Section 3.1.2  
- **Requirement Id:** Section 7.1.1  
- **Requirement Id:** Section 7.5  


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
REPO-USERPROFILE-SERVICE-001


---

# 17. Architecture_Map

- layer.service.application


---

# 18. Components_Map

- comp.backend.odoo.userMgmtModule (indirectly)
- comp.datastore.postgres


---

# 19. Requirements_Map

- REQ-004
- SEC-004 (Privacy compliance features like data deletion)
- NFR-006 (Data protection of profile info)
- Section 3.1.2 (User Profile Management)
- Section 7.1.1 (User Profile Data)
- Section 7.5 (Data Retention for user data)


---

