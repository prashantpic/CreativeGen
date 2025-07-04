# Repository Specification

# 1. Name
CreativeFlow.SharedLibraries.Common


---

# 2. Description
A collection of shared libraries and common utilities used across multiple backend microservices (primarily Python). This includes modules for standardized logging (DEP-005), security helpers (input validation, output encoding based on SEC-005), internationalization utilities (date/time/number formatting as per UI-006), common Data Transfer Objects (DTOs) if applicable for inter-service communication, custom exception classes, and common business logic helpers. These libraries promote code reuse, consistency, and adherence to NFRs like NFR-008 (Code Quality).


---

# 3. Type
SharedLibraries


---

# 4. Namespace
CreativeFlow.Shared


---

# 5. Output Path
libs/creativeflow-shared-python


---

# 6. Framework
N/A


---

# 7. Language
Python


---

# 8. Technology
Python 3.11+, Pydantic (for DTOs/validation), standard Python logging, security libraries (e.g., bleach)


---

# 9. Thirdparty Libraries

- pydantic
- python-json-logger
- bleach
- babel


---

# 10. Dependencies



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
Microservices


---

# 16. Id
REPO-SHAREDLIBS-COMMON-001


---

# 17. Architecture_Map

- layer.crosscutting.sharedlibs


---

# 18. Components_Map



---

# 19. Requirements_Map

- NFR-008 (Code Quality - implies shared conventions)
- NFR-009 (Modularity implies well-defined interfaces, some could be shared)
- NFR-011 (Testability often improved by shared mocks/test utils)
- DEP-005 (Standardized log format implies shared logging config/lib)
- UI-006 (Backend aspects of I18n)
- SEC-005 (Input validation helpers)


---

