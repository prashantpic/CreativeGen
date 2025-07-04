# Repository Specification

# 1. Name
CreativeFlow.AuthService


---

# 2. Description
A microservice responsible for user authentication and authorization. Handles user registration (email/password, social logins via OAuth 2.0/OpenID Connect), email verification, multi-factor authentication (MFA) for Pro+ accounts, secure password management (hashing, reset), session management using JWTs (access and refresh tokens), and Role-Based Access Control (RBAC) based on user roles and subscription tiers. Exposes internal REST APIs consumed by the API Gateway and other services.


---

# 3. Type
AuthenticationService


---

# 4. Namespace
CreativeFlow.Services.Auth


---

# 5. Output Path
services/auth-service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, FastAPI, SQLAlchemy, Pydantic, python-jose (JWT), passlib (bcrypt), OAuthlib, Redis (sessions)


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- pydantic
- python-jose
- passlib
- bcrypt
- python-multipart
- itsdangerous
- redis
- httpx


---

# 10. Dependencies

- REPO-POSTGRES-DB-001
- REPO-REDIS-CACHE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.application


---

# 12. Requirements

- **Requirement Id:** REQ-001  
- **Requirement Id:** REQ-002  
- **Requirement Id:** REQ-003  
- **Requirement Id:** SEC-001  
- **Requirement Id:** SEC-002  
- **Requirement Id:** NFR-006 (Data protection for credentials)  
- **Requirement Id:** Section 3.1.1  
- **Requirement Id:** Section 8.1  


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
REPO-AUTH-SERVICE-001


---

# 17. Architecture_Map

- layer.service.application


---

# 18. Components_Map

- comp.backend.odoo.userMgmtModule (indirectly, as Odoo might hold primary user record)
- comp.datastore.postgres
- comp.datastore.redis


---

# 19. Requirements_Map

- REQ-001
- REQ-002
- REQ-003
- SEC-001
- SEC-002
- NFR-006 (Data protection of credentials)
- Section 3.1.1 (User Registration and Authentication)
- Section 8.1 (Authentication and Authorization security reqs)


---

