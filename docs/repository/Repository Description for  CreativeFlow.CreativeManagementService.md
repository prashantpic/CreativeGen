# Repository Specification

# 1. Name
CreativeFlow.CreativeManagementService


---

# 2. Description
A microservice responsible for managing core creative elements: Brand Kits (colors, fonts, logos), Workbenches for project organization, individual Creative Projects, user-uploaded assets, AI-generated asset metadata, version control for creatives, and project templates. Interacts with object storage (MinIO) for asset files and PostgreSQL for metadata. Exposes internal REST APIs.


---

# 3. Type
Microservice


---

# 4. Namespace
CreativeFlow.Services.CreativeManagement


---

# 5. Output Path
services/creativemgmt-service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, FastAPI, SQLAlchemy, Pydantic, MinIO SDK


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- pydantic
- minio


---

# 10. Dependencies

- REPO-POSTGRES-DB-001
- REPO-MINIO-STORAGE-001
- REPO-AUTH-SERVICE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.application


---

# 12. Requirements

- **Requirement Id:** REQ-004 (Brand kit management)  
- **Requirement Id:** REQ-010  
- **Requirement Id:** REQ-011  
- **Requirement Id:** REQ-012  
- **Requirement Id:** Section 3.2 (Creative Engine - asset metadata aspect)  
- **Requirement Id:** Section 3.3  
- **Requirement Id:** Section 7.2  
- **Requirement Id:** Section 7.4.1  


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
REPO-CREATIVEMGMT-SERVICE-001


---

# 17. Architecture_Map

- layer.service.application


---

# 18. Components_Map

- comp.datastore.postgres
- comp.datastore.minio
- comp.backend.odoo.contentMgmtModule (indirectly if Odoo has related logic)


---

# 19. Requirements_Map

- REQ-004 (Brand kit management part)
- REQ-010
- REQ-011
- REQ-012
- Section 3.3 (Workbench System)
- Section 7.2 (Creative Asset Management data)
- Section 7.4.1 (Object Storage Organization)


---

