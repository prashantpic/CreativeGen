# Repository Specification

# 1. Name
CreativeFlow.SocialPublishingService


---

# 2. Description
A microservice responsible for integrating with various social media platform APIs (Instagram, Facebook, LinkedIn, Twitter/X, Pinterest, TikTok). It enables users to connect their social accounts securely via OAuth 2.0, and then directly publish or schedule creative content generated on the platform. It handles secure storage and refresh of OAuth tokens and manages API error handling and rate limits from social platforms. Exposes internal REST APIs.


---

# 3. Type
Microservice


---

# 4. Namespace
CreativeFlow.Services.SocialPublishing


---

# 5. Output Path
services/socialpublishing-service


---

# 6. Framework
FastAPI


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, FastAPI, Pydantic, SQLAlchemy, Social Media SDKs (e.g., facebook-sdk, python-linkedin, tweepy)


---

# 9. Thirdparty Libraries

- fastapi
- uvicorn
- pydantic
- sqlalchemy
- psycopg2-binary
- httpx
- cryptography


---

# 10. Dependencies

- REPO-POSTGRES-DB-001
- REPO-AUTH-SERVICE-001
- REPO-SHARED-LIBS-001


---

# 11. Layer Ids

- layer.service.social


---

# 12. Requirements

- **Requirement Id:** INT-001  
- **Requirement Id:** INT-002  
- **Requirement Id:** Section 9.1  


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
REPO-SOCIALPUB-SERVICE-001


---

# 17. Architecture_Map

- layer.service.social


---

# 18. Components_Map

- comp.datastore.postgres


---

# 19. Requirements_Map

- INT-001
- INT-002
- Section 9.1 (Social Media Platform Integration)


---

