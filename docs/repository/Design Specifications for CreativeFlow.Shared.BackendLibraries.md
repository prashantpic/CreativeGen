# Software Design Specification (SDS) for CreativeFlow.Shared.BackendLibraries

## 1. Introduction

### 1.1. Purpose
This document outlines the detailed software design for the `CreativeFlow.Shared.BackendLibraries` repository. This repository provides a centralized, version-controlled Python library of common code, utilities, and data contracts to be shared across all backend microservices of the CreativeFlow AI platform.

The primary goals of this shared library are:
- **Promote Code Reusability:** Avoid code duplication across microservices.
- **Enforce Consistency:** Ensure standardized error handling, logging, data structures, and security practices.
- **Improve Maintainability:** Centralize updates to common logic and contracts.
- **Support Modularity:** Facilitate loose coupling between services by providing stable, versioned interfaces and DTOs.

### 1.2. Scope
This specification covers the design of the following shared components:
- Core utilities for custom exceptions and structured logging.
- API Data Transfer Objects (DTOs) using Pydantic.
- Asynchronous messaging event schemas for RabbitMQ.
- Shared security utilities for authentication and authorization.
- Common data validation functions.

## 2. General Design Principles
The library will be designed following these principles:
- **DRY (Don't Repeat Yourself):** Core logic used in more than one service should be centralized here.
- **Single Responsibility Principle (SRP):** Each module within the library will have a single, well-defined responsibility.
- **Loose Coupling:** The library will provide abstractions (like DTOs and event schemas) that decouple services from each other's internal implementations.
- **Statelessness:** Shared utilities will be stateless to ensure they can be used safely in concurrent environments.
- **Pydantic-Driven Contracts:** Pydantic models will be the source of truth for all data contracts (API DTOs, messaging events), providing runtime validation and static analysis benefits.

## 3. Core Modules Specification

### 3.1. `core.exceptions` Module
This module defines a standardized hierarchy of custom exceptions for consistent error handling across all backend services. This allows middleware in the API Gateway or individual services to catch specific exceptions and generate predictable HTTP responses.

python
# src/creativeflow/shared/core/exceptions.py

from typing import Any, Dict, Optional

class BaseAPIException(Exception):
    """Base class for all custom API exceptions."""
    status_code: int = 500
    detail: str = "An internal server error occurred."
    
    def __init__(self, detail: Optional[str] = None, **kwargs: Any) -> None:
        self.detail = detail or self.detail
        self.extra_info = kwargs

    def to_dict(self) -> Dict[str, Any]:
        response = {"detail": self.detail}
        if self.extra_info:
            response.update(self.extra_info)
        return response

class NotFoundException(BaseAPIException):
    """Raised when a resource is not found (HTTP 404)."""
    status_code = 404
    detail = "Resource not found."

class ValidationException(BaseAPIException):
    """Raised for data validation errors (HTTP 422)."""
    status_code = 422
    detail = "Validation error."
    
    def __init__(self, errors: Any, detail: Optional[str] = None) -> None:
        super().__init__(detail=detail or self.detail, errors=errors)

class AuthenticationException(BaseAPIException):
    """Raised for authentication failures (HTTP 401)."""
    status_code = 401
    detail = "Authentication failed."
    headers = {"WWW-Authenticate": "Bearer"}

class PermissionDeniedException(BaseAPIException):
    """Raised when an authenticated user lacks permissions (HTTP 403)."""
    status_code = 403
    detail = "Permission denied."

class ConflictException(BaseAPIException):
    """Raised when an action conflicts with the current state of a resource (HTTP 409)."""
    status_code = 409
    detail = "Conflict with existing resource."

class ServiceUnavailableException(BaseAPIException):
    """Raised when a downstream service is unavailable (HTTP 503)."""
    status_code = 503
    detail = "A required downstream service is currently unavailable."


### 3.2. `core.logging` Module
This module provides a utility to configure standardized, structured JSON logging for any service that imports it.

python
# src/creativeflow/shared/core/logging.py
import logging
import sys
import json
from contextvars import ContextVar
from typing import Optional

# Context variable to hold the correlation ID for a request
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

class JsonFormatter(logging.Formatter):
    """Formats log records as JSON."""
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service_name", "unknown"),
            "correlation_id": correlation_id_var.get(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def configure_logging(service_name: str, log_level: str = "INFO") -> None:
    """
    Configures root logger for structured JSON logging.
    
    Args:
        service_name: The name of the service for log records.
        log_level: The minimum log level to output.
    """
    # ... Implementation to set up logger, handler, and JsonFormatter ...
    # It will add a 'service_name' filter to inject the service name into records.
    # It will clear existing handlers to avoid duplicate logs.


## 4. API Data Transfer Objects (DTOs) Specification
DTOs define the data contracts for API endpoints. They are built using Pydantic for data validation, serialization, and documentation generation.

### 4.1. `api.dtos.base` Module
Provides a common base for all API DTOs.

python
# src/creativeflow/shared/api/dtos/base.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    """Base DTO with common configuration."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BaseResponseDTO(BaseDTO):
    """Base DTO for responses, including common entity fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


### 4.2. `api.dtos.user` Module
Defines DTOs for user registration, profile management, and authentication.

python
# src/creativeflow/shared/api/dtos/user.py
from pydantic import EmailStr, Field
from typing import Optional
from .base import BaseDTO, BaseResponseDTO
from ..validation.validators import validate_password_complexity

# Request DTOs
class UserCreateDTO(BaseDTO):
    email: EmailStr
    password: str = Field(..., min_length=12)
    _validate_password = validator('password', allow_reuse=True)(validate_password_complexity)

class UserLoginDTO(BaseDTO):
    email: EmailStr
    password: str

class UserUpdateDTO(BaseDTO):
    full_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    # ... other updatable fields

# Response DTOs
class UserResponseDTO(BaseResponseDTO):
    email: EmailStr
    full_name: Optional[str]
    username: Optional[str]
    subscription_tier: str
    credit_balance: float

class TokenResponseDTO(BaseDTO):
    access_token: str
    token_type: str = "bearer"


### 4.3. DTOs for Other Domains
Similar DTO modules will be created for other domains, following the same pattern of separating create, update, and response models.
- **`api.dtos.project`**: `BrandKitCreateDTO`, `BrandKitUpdateDTO`, `BrandKitResponseDTO`, `ProjectCreateDTO`, `ProjectResponseDTO`, etc.
- **`api.dtos.generation`**: `GenerationCreateRequestDTO`, `GenerationStatusResponseDTO`.
- **`api.dtos.team`**: `TeamCreateDTO`, `TeamMemberInviteDTO`, `TeamResponseDTO`.

## 5. Asynchronous Messaging Contracts

### 5.1. `messaging.events` Module
Defines the Pydantic schemas for all domain events transmitted via RabbitMQ. This ensures strict validation of message payloads between services.

python
# src/creativeflow/shared/messaging/events.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

class BaseEvent(BaseModel):
    """Base model for all domain events."""
    event_id: UUID = Field(default_factory=uuid.uuid4)
    event_type: str
    correlation_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Dict[str, Any]

class UserRegisteredEvent(BaseEvent):
    event_type: Literal["user.registered"] = "user.registered"
    payload: Dict[str, Any] # e.g., {"user_id": "...", "email": "...", "verification_token": "..."}

class GenerationCompletedEvent(BaseEvent):
    event_type: Literal["generation.completed"] = "generation.completed"
    payload: Dict[str, Any] # e.g., {"generation_id": "...", "user_id": "...", "status": "Completed", "final_asset_id": "..."}


## 6. Shared Security Utilities

### 6.1. `security.auth` Module
Provides reusable dependencies for FastAPI services to handle authentication and authorization.

python
# src/creativeflow/shared/security/auth.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
# ... import custom exceptions and user DTOs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class TokenPayload(BaseModel):
    sub: str # User ID
    roles: list[str] = []
    # ... other claims

# --- JWT Handling Functions (internal to the module) ---
# create_access_token(...)
# ...

# --- FastAPI Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    # Logic to decode JWT token using a secret key
    # Handles JWTError, raises AuthenticationException on failure
    # Returns a TokenPayload object
    pass

def require_role(required_role: str):
    """
    Factory for a FastAPI dependency that checks for a specific role.
    """
    async def role_checker(current_user: TokenPayload = Depends(get_current_user)):
        if required_role not in current_user.roles:
            raise PermissionDeniedException(detail=f"User lacks required role: {required_role}")
        return current_user
    return role_checker


## 7. Shared Validation Utilities

### 7.1. `validation.validators` Module
Contains common, reusable Pydantic validators.

python
# src/creativeflow/shared/validation/validators.py
import re

def validate_password_complexity(password: str) -> str:
    """
    Validator to enforce password complexity rules.
    - At least 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    # ... regex implementation ...
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$', password):
        raise ValueError("Password does not meet complexity requirements.")
    return password

def validate_username_format(username: str) -> str:
    """
    Validator to enforce username format.
    - 3-50 characters
    - Alphanumeric and underscores only
    """
    if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
        raise ValueError("Username can only contain alphanumeric characters and underscores.")
    return username


## 8. Project Configuration (`pyproject.toml`)

This file will be configured to manage the library as a formal Python package.

toml
# pyproject.toml

[tool.poetry] # Or [project] for standard PEP 621
name = "creativeflow-shared-backend"
version = "0.1.0"
description = "Shared libraries for the CreativeFlow AI backend."
authors = ["CreativeFlow AI Team <dev@creativeflow.ai>"]

[tool.poetry.dependencies]
python = "^3.11"
pydantic = {extras = ["email"], version = "^2.7.0"}
fastapi = "^0.110.0" # For dependency injection system
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
python-multipart = "^0.0.9" # For FastAPI

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-cov = "^4.1.0"
black = "^24.0.0"
flake8 = "^7.0.0"
mypy = "^1.8.0"
isort = "^5.12.0"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.mypy]
strict = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=src --cov-report=term-missing"
testpaths = ["tests"]


## 9. Testing Strategy
- **Unit Tests:** Every utility function, validator, exception, and DTO model with custom logic will have comprehensive unit tests using `pytest`.
- **Coverage:** The test suite must maintain a minimum of 95% code coverage, enforced by the CI pipeline (`pytest-cov`).
- **Automation:** All tests will be executed automatically on every commit and merge request as part of the CI pipeline defined in the DevOps repository.