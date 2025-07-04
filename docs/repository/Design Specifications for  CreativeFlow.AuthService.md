# Software Design Specification: CreativeFlow.AuthService

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `CreativeFlow.AuthService`. This microservice is a critical component of the CreativeFlow AI platform, responsible for managing all aspects of user authentication and authorization. Its functionalities include user registration (email/password and social logins), email verification, multi-factor authentication (MFA), secure password management, session management using JSON Web Tokens (JWTs), and Role-Based Access Control (RBAC).

### 1.2 Scope
The scope of this document covers the design of the `CreativeFlow.AuthService` including:
- API endpoints for authentication, registration, MFA, password, and session management.
- Internal service logic for handling these operations.
- Data models and interactions with the PostgreSQL database and Redis cache.
- Integration with notification services for email and SMS.
- Security mechanisms for password hashing, token management, and MFA.
- Configuration management.

### 1.3 Definitions, Acronyms, and Abbreviations
- **API:** Application Programming Interface
- **CRUD:** Create, Read, Update, Delete
- **DB:** Database
- **DR:** Disaster Recovery
- **EDA:** Event-Driven Architecture
- **GDPR:** General Data Protection Regulation
- **JWT:** JSON Web Token
- **JTI:** JWT ID
- **KMS:** Key Management Service
- **MFA:** Multi-Factor Authentication
- **OAuth:** Open Authorization
- **OIDC:** OpenID Connect
- **ORM:** Object-Relational Mapping
- **OTP:** One-Time Password
- **PII:** Personally Identifiable Information
- **PWA:** Progressive Web Application
- **RBAC:** Role-Based Access Control
- **RDBMS:** Relational Database Management System
- **REST:** Representational State Transfer
- **RPO:** Recovery Point Objective
- **RTO:** Recovery Time Objective
- **SDS:** Software Design Specification
- **SMS:** Short Message Service
- **SoC:** Separation of Concerns
- **SQL:** Structured Query Language
- **SRS:** Software Requirements Specification
- **SSD:** Solid State Drive
- **TOTP:** Time-based One-Time Password
- **TTL:** Time To Live
- **UI:** User Interface
- **URI:** Uniform Resource Identifier
- **URL:** Uniform Resource Locator
- **UUID:** Universally Unique Identifier
- **WYSIWYG:** What You See Is What You Get

### 1.4 References
- CreativeFlow AI Software Requirements Specification (SRS) document.
- CreativeFlow AI Architecture Design document.
- CreativeFlow AI Database Design document.
- Sequence Diagram: SD-CF-001 "User Email-Based Registration and Initial Login".

### 1.5 Overview
This document is organized into sections detailing the overall architecture, data design, component design, API specifications, and security considerations for the `CreativeFlow.AuthService`.

## 2. System Overview

The `CreativeFlow.AuthService` is a Python FastAPI-based microservice. It interacts with a PostgreSQL database for persistent storage of user and authentication-related data, and with Redis for session management and caching of frequently accessed data like OTPs or token blacklists. It exposes internal RESTful APIs for use by the API Gateway.

Key functionalities include:
- **User Registration:** Email/password and social logins (Google, Facebook, Apple).
- **Email Verification:** Token-based email confirmation.
- **Authentication:** Secure login, JWT (access and refresh token) issuance and validation.
- **Password Management:** Hashing (bcrypt), secure reset, change password.
- **Multi-Factor Authentication (MFA):** TOTP, SMS, Email OTP methods for Pro+ users, recovery codes.
- **Session Management:** Creation, validation, revocation, device tracking, concurrent session limits.
- **Authorization:** RBAC based on user roles and subscription tiers (roles fetched, tier info available).

## 3. Design Considerations

### 3.1 Assumptions
- The API Gateway will handle initial request validation and routing.
- Odoo is the master for user profile information beyond core auth attributes, and for subscription/billing details. This service will maintain essential auth-related user data and may query/sync subscription tier for RBAC.
- Notification services (email/SMS) are available and abstracted via an interface.
- Secure external storage for secrets (e.g., HashiCorp Vault) will be used for production; environment variables are for local/CI.

### 3.2 Constraints
- Technology stack: Python 3.11+, FastAPI, SQLAlchemy, Pydantic, python-jose, passlib, Redis.
- Database: PostgreSQL 16+.
- Adherence to specified security requirements (SEC-001, SEC-002, NFR-006).
- Compliance with GDPR for data handling.

## 4. System Architecture
The service follows a layered architecture internally:
- **API Layer (`api/`):** FastAPI routers and Pydantic schemas for request/response handling.
- **Service Layer (`core/services/`):** Contains core business logic, orchestrating operations.
- **Domain Layer (`core/domain/`):** Defines domain models (SQLAlchemy), enums, and custom exceptions.
- **Security Layer (`core/security/`):** Handles password hashing, JWT management, TOTP.
- **Infrastructure Layer (`infrastructure/`):**
    - **Repositories (`repositories/`):** Data access logic (SQLAlchemy for DB, Redis client for cache).
    - **Notifications (`notifications/`):** Implementations for sending emails/SMS.
    - **Database (`database/`):** DB connection, session management, Alembic migrations.
- **Utilities (`utils/`):** Helper functions.
- **Configuration (`config.py`, `dependencies.py`):** Application settings and common dependencies.

## 5. Detailed Component Design

This section details the design for each file specified in the repository's `file_structure_json`.

---

**Path:** `services/auth-service/pyproject.toml`
- **Purpose:** Defines project structure, dependencies, and build/tooling configurations.
- **LogicDescription:**
    - Specifies Python version: `^3.11`.
    - Dependencies:
        - `fastapi = "^0.111.0"`
        - `uvicorn[standard] = "^0.20.0"`
        - `sqlalchemy = "^2.0.30"`
        - `psycopg2-binary = "^2.9.9"` (or `asyncpg` if async SQLAlchemy is used)
        - `pydantic = "^2.7.4"`
        - `pydantic-settings = "^2.0.0"`
        - `python-jose[cryptography] = "^3.3.0"`
        - `passlib[bcrypt] = "^1.7.4"`
        - `bcrypt = "^4.0.1"`
        - `python-multipart = "^0.0.7"` (for form data)
        - `itsdangerous = "^2.1.2"` (for timed tokens if not solely JWT)
        - `redis = "^5.0.0"`
        - `httpx = "^0.25.0"` (for OAuth client calls)
        - `alembic = "^1.12.0"`
        - `pyotp = "^2.9.0"` (for TOTP)
        - `email-validator = "^2.0.0"` (for Pydantic email validation)
    - Dev Dependencies:
        - `pytest = "^7.0.0"`
        - `pytest-cov = "^4.0.0"`
        - `flake8 = "^6.0.0"`
        - `black = "^23.0.0"`
        - `mypy = "^1.0.0"`
        - `httpx = "^0.25.0"` (for testing API calls)
    - Tool Configurations:
        - `[tool.poetry.scripts]` for entry points if any.
        - `[tool.black]`, `[tool.flake8]`, `[tool.mypy]`, `[tool.pytest.ini_options]`.
- **Documentation:** Core project definition file for managing dependencies and development environment settings.

---

**Path:** `services/auth-service/.env.example`
- **Purpose:** Serves as a template for developers to set up their local environment variables and for CI/CD to configure deployment environments.
- **LogicDescription:**
    - `DATABASE_URL="postgresql://user:password@host:port/dbname"`
    - `REDIS_URL="redis://localhost:6379/0"`
    - `JWT_SECRET_KEY="your-super-secret-key"`
    - `JWT_ALGORITHM="HS256"`
    - `ACCESS_TOKEN_EXPIRE_MINUTES=30`
    - `REFRESH_TOKEN_EXPIRE_DAYS=7`
    - `EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=72`
    - `PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1`
    - `MFA_OTP_EXPIRE_SECONDS=300` (e.g., for email/SMS OTPs)
    - `TOTP_ISSUER_NAME="CreativeFlow AI"`
    - `CONCURRENT_SESSION_LIMIT=5`
    - `SOCIAL_GOOGLE_CLIENT_ID=""`
    - `SOCIAL_GOOGLE_CLIENT_SECRET=""`
    - `SOCIAL_GOOGLE_REDIRECT_URI="http://localhost:8000/api/v1/register/social/google/callback"`
    - `SOCIAL_FACEBOOK_CLIENT_ID=""` (if implemented)
    - `SOCIAL_FACEBOOK_CLIENT_SECRET=""` (if implemented)
    - `SOCIAL_FACEBOOK_REDIRECT_URI=""` (if implemented)
    - `SOCIAL_APPLE_CLIENT_ID=""` (if implemented)
    - `SOCIAL_APPLE_TEAM_ID=""` (if implemented)
    - `SOCIAL_APPLE_KEY_ID=""` (if implemented)
    - `SOCIAL_APPLE_PRIVATE_KEY_PATH=""` (or direct key content if manageable)
    - `EMAIL_HOST="smtp.example.com"`
    - `EMAIL_PORT=587`
    - `EMAIL_USERNAME=""`
    - `EMAIL_PASSWORD=""`
    - `EMAIL_USE_TLS=true`
    - `EMAIL_FROM_ADDRESS="noreply@creativeflow.ai"`
    - `SMS_PROVIDER_API_KEY=""` (e.g., Twilio SID)
    - `SMS_PROVIDER_AUTH_TOKEN=""` (e.g., Twilio Auth Token)
    - `SMS_PROVIDER_SENDER_ID=""` (e.g., Twilio phone number)
    - `FRONTEND_URL="http://localhost:3000"` (for email links)
- **Documentation:** Template for environment-specific configuration variables. Actual secrets are managed externally (e.g., HashiCorp Vault in production).

---

**Path:** `services/auth-service/alembic.ini`
- **Purpose:** Configures Alembic settings.
- **LogicDescription:**
    - `sqlalchemy.url = %(DATABASE_URL)s` (to be interpolated from environment or settings)
    - `script_location = src/creativeflow/authservice/infrastructure/database/alembic`
    - `file_template = %%(rev)s_%%(slug)s`
- **Documentation:** Main configuration file for Alembic database migrations.

---

**Path:** `services/auth-service/src/creativeflow/authservice/__init__.py`
- **Purpose:** Marks the directory as a Python package.
- **LogicDescription:** Can be empty.
- **Documentation:** Package initializer for the authservice.

---

**Path:** `services/auth-service/src/creativeflow/authservice/config.py`
- **Purpose:** Defines and loads all application settings from environment variables.
- **Class `Settings(BaseSettings)`:**
    - Attributes:
        - `DATABASE_URL: str`
        - `REDIS_URL: str`
        - `JWT_SECRET_KEY: str`
        - `JWT_ALGORITHM: str = "HS256"`
        - `ACCESS_TOKEN_EXPIRE_MINUTES: int = 30`
        - `REFRESH_TOKEN_EXPIRE_DAYS: int = 7`
        - `EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 72`
        - `PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1`
        - `MFA_OTP_EXPIRE_SECONDS: int = 300`
        - `TOTP_ISSUER_NAME: str = "CreativeFlow AI"`
        - `CONCURRENT_SESSION_LIMIT: int = 5`
        - `SOCIAL_GOOGLE_CLIENT_ID: Optional[str] = None`
        - `SOCIAL_GOOGLE_CLIENT_SECRET: Optional[str] = None`
        - `SOCIAL_GOOGLE_REDIRECT_URI: Optional[str] = None`
        - `SOCIAL_FACEBOOK_CLIENT_ID: Optional[str] = None` (if implemented)
        - `SOCIAL_FACEBOOK_CLIENT_SECRET: Optional[str] = None` (if implemented)
        - `SOCIAL_FACEBOOK_REDIRECT_URI: Optional[str] = None` (if implemented)
        - `SOCIAL_APPLE_CLIENT_ID: Optional[str] = None` (if implemented)
        - `SOCIAL_APPLE_TEAM_ID: Optional[str] = None` (if implemented)
        - `SOCIAL_APPLE_KEY_ID: Optional[str] = None` (if implemented)
        - `SOCIAL_APPLE_PRIVATE_KEY: Optional[str] = None` (if implemented)
        - `EMAIL_HOST: str`
        - `EMAIL_PORT: int = 587`
        - `EMAIL_USERNAME: Optional[str] = None`
        - `EMAIL_PASSWORD: Optional[str] = None`
        - `EMAIL_USE_TLS: bool = True`
        - `EMAIL_FROM_ADDRESS: EmailStr`
        - `SMS_PROVIDER: Optional[str] = None` (e.g., "twilio")
        - `SMS_PROVIDER_ACCOUNT_SID: Optional[str] = None`
        - `SMS_PROVIDER_AUTH_TOKEN: Optional[str] = None`
        - `SMS_PROVIDER_SENDER_ID: Optional[str] = None`
        - `FRONTEND_URL: str = "http://localhost:3000"`
    - `model_config = SettingsConfigDict(env_file=".env", extra="ignore")`
- **Function `get_settings() -> Settings`:**
    - `@lru_cache()`
    - Returns an instance of `Settings`.
- **Documentation:** Manages application-wide configuration settings loaded from environment variables.

---

**Path:** `services/auth-service/src/creativeflow/authservice/main.py`
- **Purpose:** Initializes the FastAPI application, configures global middleware, and includes all API routers.
- **Code Structure:**
    python
    from fastapi import FastAPI, Request, status
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from .api.v1.routers import auth_router, registration_router, mfa_router, password_router, session_router, user_router
    from .core.domain.exceptions import AuthServiceException # Import all custom exceptions
    from .config import get_settings

    settings = get_settings()
    app = FastAPI(title="CreativeFlow Auth Service")

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler for custom exceptions
    @app.exception_handler(AuthServiceException)
    async def auth_service_exception_handler(request: Request, exc: AuthServiceException):
        # Map specific exceptions to status codes
        status_code = status.HTTP_400_BAD_REQUEST
        if isinstance(exc, UserNotFoundException) or isinstance(exc, InvalidCredentialsException):
            status_code = status.HTTP_401_UNAUTHORIZED
        # ... other mappings
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
        )
    
    # Include Routers
    app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(registration_router.router, prefix="/api/v1/register", tags=["Registration"])
    app.include_router(user_router.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(password_router.router, prefix="/api/v1/password", tags=["Password Management"])
    app.include_router(mfa_router.router, prefix="/api/v1/mfa", tags=["MFA Management"])
    app.include_router(session_router.router, prefix="/api/v1/sessions", tags=["Session Management"])

    @app.get("/health", tags=["Health Check"])
    async def health_check():
        return {"status": "ok"}
    
- **Documentation:** The main entry point for the FastAPI application, responsible for app setup, middleware, and routing.

---

**Path:** `services/auth-service/src/creativeflow/authservice/utils/token_generator.py`
- **Purpose:** Provides functions to generate cryptographically secure random strings.
- **Functions:**
    - `generate_secure_token(length: int = 32) -> str`:
        - Logic: Uses `secrets.token_urlsafe(length)`.
    - `generate_otp_code(length: int = 6) -> str`:
        - Logic: Generates a string of `length` random digits using `secrets.choice(string.digits)`.
- **Documentation:** Utility for generating secure random tokens and OTP codes.

---

**Path:** `services/auth-service/src/creativeflow/authservice/utils/time_utils.py`
- **Purpose:** Provides helper functions for common time-related operations.
- **Functions:**
    - `get_current_utc_time() -> datetime`:
        - Logic: Returns `datetime.now(timezone.utc)`.
    - `is_token_expired(expires_at: datetime) -> bool`:
        - Logic: Returns `get_current_utc_time() >= expires_at`.
    - `get_future_time(delta: timedelta) -> datetime`:
        - Logic: Returns `get_current_utc_time() + delta`.
- **Documentation:** Utility functions for handling date and time operations, primarily focusing on UTC.

---

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/enums.py`
- **Purpose:** Provides enumerations for domain-specific concepts.
- **Enums:**
    - `SocialProvider(str, Enum)`:
        - `GOOGLE = "google"`
        - `FACEBOOK = "facebook"`
        - `APPLE = "apple"`
    - `MFAMethod(str, Enum)`:
        - `SMS = "sms"`
        - `TOTP = "totp"`
        - `EMAIL = "email"`
    - `UserRole(str, Enum)`: (As defined by SRS REQ-003, e.g., Owner, Admin, Editor, Viewer)
        - `OWNER = "owner"`
        - `ADMIN = "admin"`
        - `EDITOR = "editor"`
        - `VIEWER = "viewer"`
        - `FREE_USER = "free_user"`
        - `PRO_USER = "pro_user"`
        - `TEAM_USER = "team_user"` // These might be subscription tiers used for role-like checks
        - `ENTERPRISE_USER = "enterprise_user"`
- **Documentation:** Contains enumerations used throughout the authentication domain.

---

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/exceptions.py`
- **Purpose:** Defines custom exceptions for specific error conditions.
- **Classes:**
    - `AuthServiceException(Exception)`: Base exception.
    - `UserNotFoundException(AuthServiceException)`
    - `InvalidCredentialsException(AuthServiceException)`
    - `TokenExpiredException(AuthServiceException)`
    - `InvalidTokenException(AuthServiceException)`
    - `MFAChallengeRequiredException(AuthServiceException)`: May carry `available_methods: List[MFAMethod]`.
    - `MFAInvalidCodeException(AuthServiceException)`
    - `EmailAlreadyExistsException(AuthServiceException)`
    - `EmailNotVerifiedException(AuthServiceException)`
    - `InactiveUserException(AuthServiceException)`
    - `MFAMethodAlreadySetupException(AuthServiceException)`
    - `MFAMethodNotSetupException(AuthServiceException)`
    - `MaxSessionsReachedException(AuthServiceException)`
    - `InvalidRecoveryCodeException(AuthServiceException)`
    - `OAuthIntegrationException(AuthServiceException)`
- **Documentation:** Provides custom exceptions for clear and specific error handling.

---

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/notifications/interface.py`
- **Purpose:** Abstracts the sending of notifications.
- **Class `NotificationService(ABC)`:**
    - Methods:
        - `@abstractmethod async def send_email(self, to_email: str, subject: str, html_content: str) -> None:`
        - `@abstractmethod async def send_sms(self, to_phone: str, message: str) -> None:`
- **Documentation:** Interface for notification sending services.

---
#### `core/domain/models/`

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/models/user_model.py`
- **Purpose:** Defines the database schema for the `users` table.
- **Class `User(Base)`:** (inherits from `infrastructure.database.base.Base`)
    - `__tablename__ = "users"`
    - `id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)`
    - `email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)`
    - `hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)`
    - `full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)`
    - `is_active: Mapped[bool] = mapped_column(Boolean, default=True)`
    - `is_verified: Mapped[bool] = mapped_column(Boolean, default=False)`
    - `verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)`
    - `verification_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)`
    - `password_reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)`
    - `password_reset_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)`
    - `social_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)`
    - `social_provider_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)`
    - `last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)`
    - `created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())`
    - `updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())`
    - `subscription_tier: Mapped[str] = mapped_column(String(20), default='Free', nullable=False)` // Required for RBAC checks
    - `mfa_factors: Mapped[List["MFAModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")`
    - `recovery_codes: Mapped[List["RecoveryCodeModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")`
    - `roles: Mapped[List["RoleModel"]] = relationship(secondary="user_roles", back_populates="users")`
    - `__table_args__ = (UniqueConstraint('social_provider', 'social_provider_id', name='uq_user_social_provider_id'),)`
- **Documentation:** SQLAlchemy model for user accounts.

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/models/mfa_model.py`
- **Purpose:** Defines schema for storing MFA configurations.
- **Class `MFAModel(Base)`:**
    - `__tablename__ = "mfa_factors"`
    - `id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)`
    - `user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)`
    - `method: Mapped[str] = mapped_column(String(50), nullable=False)` // e.g., "TOTP", "SMS", "EMAIL"
    - `secret_key_encrypted: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)` // For TOTP secret, encrypted
    - `phone_number_encrypted: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)` // For SMS, encrypted
    - `email_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)` // For Email OTP target
    - `is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)`
    - `created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())`
    - `user: Mapped["User"] = relationship(back_populates="mfa_factors")`
- **Documentation:** SQLAlchemy model for user MFA methods.

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/models/role_model.py`
- **Purpose:** Defines schema for user roles.
- **Table `user_roles_table`:** (Association Table)
    python
    user_roles_table = Table(
        "user_roles",
        Base.metadata,
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
        Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    )
    
- **Class `RoleModel(Base)`:**
    - `__tablename__ = "roles"`
    - `id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)`
    - `name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)`
    - `description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)`
    - `users: Mapped[List["User"]] = relationship(secondary=user_roles_table, back_populates="roles")`
- **Documentation:** SQLAlchemy model for user roles and their association with users.

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/models/recovery_code_model.py`
- **Purpose:** Defines schema for storing hashed MFA recovery codes.
- **Class `RecoveryCodeModel(Base)`:**
    - `__tablename__ = "recovery_codes"`
    - `id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)`
    - `user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)`
    - `hashed_code: Mapped[str] = mapped_column(String(255), nullable=False)`
    - `is_used: Mapped[bool] = mapped_column(Boolean, default=False, index=True)`
    - `created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())`
    - `user: Mapped["User"] = relationship(back_populates="recovery_codes")`
- **Documentation:** SQLAlchemy model for MFA recovery codes.

**Path:** `services/auth-service/src/creativeflow/authservice/core/domain/models/token_revocation_model.py`
- **Purpose:** Defines schema for storing identifiers of revoked JWTs (primarily for refresh tokens or session-bound access tokens if needed).
- **Note:** This is often better handled entirely in Redis due to performance and TTL needs. If using DB, ensure efficient cleanup.
- **Class `TokenRevocationModel(Base)`:**
    - `__tablename__ = "token_revocations"`
    - `jti: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)` // JWT ID
    - `expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)` // Original expiry of the token
    - `revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())`
- **Documentation:** SQLAlchemy model for persisting revoked JWT identifiers. Consider Redis for primary blacklist.

---
#### `core/security/`

**Path:** `services/auth-service/src/creativeflow/authservice/core/security/password_manager.py`
- **Purpose:** Handles password hashing and verification.
- **Code Structure:**
    python
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class PasswordManager:
        @staticmethod
        def get_password_hash(password: str) -> str:
            return pwd_context.hash(password)

        @staticmethod
        def verify_password(plain_password: str, hashed_password: str) -> bool:
            return pwd_context.verify(plain_password, hashed_password)
    
- **Documentation:** Manages secure hashing and verification of user passwords using bcrypt.

**Path:** `services/auth-service/src/creativeflow/authservice/core/security/jwt_manager.py`
- **Purpose:** Manages JWT lifecycle.
- **Class `JWTManager`:**
    - Constructor: `__init__(self, settings: Settings)` (takes config settings)
    - `create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str`:
        - Logic: Adds expiry (`exp`), issued at (`iat`), JWT ID (`jti`). Encodes using `jose.jwt.encode`.
    - `create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str`:
        - Logic: Similar to access token, but with longer expiry from config. Also includes JTI.
    - `decode_token(self, token: str) -> Optional[dict]`:
        - Logic: Decodes using `jose.jwt.decode`. Handles `ExpiredSignatureError`, `JWTError`. Returns payload or None.
    - `_generate_jti() -> str`:
        - Logic: `uuid.uuid4().hex`
- **Documentation:** Provides functionalities for creating, signing, and validating JWTs.

**Path:** `services/auth-service/src/creativeflow/authservice/core/security/permissions.py`
- **Purpose:** FastAPI dependencies for RBAC and authenticated user.
- **Code Structure:**
    python
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from jose import JWTError
    from sqlalchemy.orm import Session
    from typing import List

    from ..domain.models.user_model import User as UserModel
    from ..domain.enums import UserRole
    from ...api.v1.schemas.user_schemas import UserResponseSchema # Or a core User DTO
    from ...infrastructure.database.db_config import get_db
    from .jwt_manager import JWTManager
    from ...config import get_settings
    from ..services.user_service import UserService # To fetch user roles

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
    settings = get_settings()
    jwt_manager = JWTManager(settings)

    async def get_current_user_model(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ) -> UserModel:
        # Decode token, get user_id from payload['sub']
        # Fetch user from db by id
        # Raise HTTPException if token invalid or user not found/inactive
        # Return UserModel instance
        pass

    async def get_current_active_user(
        current_user_model: UserModel = Depends(get_current_user_model)
    ) -> UserModel: # Or UserResponseSchema if preferred for API layer
        if not current_user_model.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        return current_user_model

    def require_roles(required_roles: List[UserRole]):
        async def role_checker(
            current_user: UserModel = Depends(get_current_active_user),
            db: Session = Depends(get_db)
        ) -> UserModel:
            user_service = UserService(db) # Example: or inject UserRepository
            user_actual_roles = await user_service.get_user_roles(current_user.id) # Assuming this method exists
            if not any(role.name in [r.value for r in required_roles] for role in user_actual_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            return current_user
        return role_checker
    
- **Documentation:** Defines FastAPI dependencies for authentication and role-based authorization.

**Path:** `services/auth-service/src/creativeflow/authservice/core/security/totp_handler.py`
- **Purpose:** Manages TOTP operations.
- **Class `TOTPHandler`:**
    - `generate_totp_secret() -> str`:
        - Logic: Uses `pyotp.random_base32()`.
    - `get_totp_uri(secret: str, issuer_name: str, account_name: str) -> str`:
        - Logic: Uses `pyotp.TOTP(secret).provisioning_uri(name=account_name, issuer_name=issuer_name)`.
    - `verify_totp_code(secret: str, code: str) -> bool`:
        - Logic: Uses `pyotp.TOTP(secret).verify(code)`.
- **Documentation:** Manages Time-based One-Time Password (TOTP) operations.

---
#### `infrastructure/database/`

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/database/db_config.py`
- **Purpose:** SQLAlchemy database engine and session setup.
- **Code Structure:**
    python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from typing import Iterator
    from ...config import get_settings

    settings = get_settings()
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

    engine = create_engine(SQLALCHEMY_DATABASE_URL) # Add pool_pre_ping=True for production
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db() -> Iterator[Session]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
- **Documentation:** Sets up SQLAlchemy database connection and session management.

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/database/base.py`
- **Purpose:** Provides SQLAlchemy declarative base.
- **Code Structure:**
    python
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    # Import all models here to ensure Alembic discovers them
    from ...core.domain.models.user_model import User
    from ...core.domain.models.mfa_model import MFAModel
    from ...core.domain.models.role_model import RoleModel, user_roles_table
    from ...core.domain.models.recovery_code_model import RecoveryCodeModel
    from ...core.domain.models.token_revocation_model import TokenRevocationModel
    
- **Documentation:** Defines the base for SQLAlchemy ORM models and ensures models are discoverable.

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/database/redis_config.py`
- **Purpose:** Redis client connection setup.
- **Code Structure:**
    python
    import redis.asyncio as redis # Using async version for FastAPI
    from ...config import get_settings

    settings = get_settings()
    
    async def get_redis_client() -> redis.Redis:
        # Consider connection pooling for Redis if using redis-py directly
        # For redis.asyncio, it handles connection pooling internally.
        client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        try:
            yield client
        finally:
            await client.close() # Ensure connection is closed for async

    # For synchronous use cases or background tasks, a separate sync client might be needed
    # Or pass the async client and use await.
    
- **Documentation:** Manages Redis client connection. Using `redis.asyncio` for FastAPI compatibility.

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/database/alembic/env.py`
- **Purpose:** Alembic environment configuration.
- **Key Logic:**
    - Sets `target_metadata = Base.metadata` (from `infrastructure.database.base`).
    - Configures `context.configure(connection=connection, target_metadata=target_metadata)`.
    - Loads database URL from application config (`settings.DATABASE_URL`).
- **Documentation:** Alembic script for database migration environment.

**Path:** `services/auth-service/src/creativeflow/authservice/infrastructure/database/alembic/script.py.mako`
- **Purpose:** Template for new Alembic migration scripts.
- **Content:** Standard Alembic Mako template.
- **Documentation:** Template file for Alembic migration scripts.

---
#### `dependencies.py`

**Path:** `services/auth-service/src/creativeflow/authservice/dependencies.py`
- **Purpose:** Common FastAPI dependency injection functions.
- **Functions:**
    - `get_db_session = Depends(get_db)` (from `infrastructure.database.db_config`)
    - `get_redis_client_dependency = Depends(get_redis_client)` (from `infrastructure.database.redis_config`)
    - `get_current_user_dependency = Depends(get_current_active_user)` (from `core.security.permissions`)
    - `def get_notification_service_dependency() -> NotificationService:`
        - Logic: Instantiates `EmailService` (or a combined service based on config).
        - `from .infrastructure.notifications.email_service import EmailService`
        - `from .config import get_settings`
        - `settings = get_settings()`
        - `return EmailService(settings=settings)`
    - `def get_auth_service_dependency(db: Session = get_db_session, redis: redis.Redis = get_redis_client_dependency) -> AuthService:`
        - Logic: Instantiates `AuthService` with its dependencies (repos, other services).
    - Similarly for other services (`RegistrationService`, `TokenService`, `MFAService`, `PasswordService`, `SessionService`, `UserService`, `OTPService`, `OAuthService`). Each will take necessary repository/service dependencies.
- **Documentation:** Centralizes common FastAPI dependencies.

---
#### `api/v1/schemas/`

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/common_schemas.py`
- **Purpose:** Pydantic schemas for common API responses.
- **Models:**
    - `MessageResponse(BaseModel)`: `message: str`
    - `ErrorDetail(BaseModel)`: `loc: List[Union[str, int]]`, `msg: str`, `type: str`
    - `ErrorResponse(BaseModel)`: `detail: Union[str, List[ErrorDetail]]`
- **Documentation:** Pydantic models for common API response structures.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/user_schemas.py`
- **Purpose:** Pydantic schemas for user operations.
- **Models:**
    - `UserBase(BaseModel)`: `email: EmailStr`, `full_name: Optional[str] = None`
    - `UserCreateSchema(UserBase)`: `password: str`
    - `UserResponseSchema(UserBase)`: `id: uuid.UUID`, `is_active: bool`, `is_verified: bool`, `subscription_tier: str`, `roles: List[str] = []`, `model_config = ConfigDict(from_attributes=True)`
    - `EmailVerificationRequestSchema(BaseModel)`: `token: str`
    - `SocialLoginRequestSchema(BaseModel)`: `token: str` (provider token/code)
- **Documentation:** Pydantic models for user data transfer.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/token_schemas.py`
- **Purpose:** Pydantic schemas for token responses.
- **Models:**
    - `TokenDataBase(BaseModel)`: `jti: Optional[str] = None`
    - `AccessToken(TokenDataBase)`: `access_token: str`, `token_type: str = "bearer"`
    - `RefreshToken(TokenDataBase)`: `refresh_token: str`, `token_type: str = "bearer"`
    - `TokenResponseSchema(BaseModel)`: `access_token_data: AccessToken`, `refresh_token_data: RefreshToken`
    - `RefreshTokenRequestSchema(BaseModel)`: `refresh_token: str`
- **Documentation:** Pydantic models for JWT responses.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/mfa_schemas.py`
- **Purpose:** Pydantic schemas for MFA operations.
- **Models:**
    - `MFASetupRequestSchema(BaseModel)`: `method: MFAMethod` (from enums), `value: Optional[str] = None` (e.g., phone number for SMS)
    - `MFASetupResponseSchema(BaseModel)`: `method: MFAMethod`, `setup_key: Optional[str] = None` (e.g., TOTP secret or provisioning URI)
    - `MFAVerifyRequestSchema(BaseModel)`: `method: MFAMethod`, `code: str`
    - `RecoveryCodesResponseSchema(BaseModel)`: `recovery_codes: List[str]`
    - `MFAStatusResponseSchema(BaseModel)`: `is_mfa_enabled: bool`, `enabled_methods: List[MFAMethod]`
- **Documentation:** Pydantic models for MFA API operations.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/password_schemas.py`
- **Purpose:** Pydantic schemas for password management.
- **Models:**
    - `ForgotPasswordRequestSchema(BaseModel)`: `email: EmailStr`
    - `ResetPasswordRequestSchema(BaseModel)`: `token: str`, `new_password: str` (with validation for complexity)
    - `ChangePasswordRequestSchema(BaseModel)`: `current_password: str`, `new_password: str` (with validation)
- **Documentation:** Pydantic models for password management API operations.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/session_schemas.py`
- **Purpose:** Pydantic schemas for session management.
- **Models:**
    - `SessionInfoSchema(BaseModel)`: `id: str`, `ip_address: str`, `user_agent: str`, `last_activity: datetime`, `created_at: datetime`
    - `ActiveSessionListResponseSchema(BaseModel)`: `sessions: List[SessionInfoSchema]`
- **Documentation:** Pydantic models for API responses related to user sessions.

**Path:** `services/auth-service/src/creativeflow/authservice/api/v1/schemas/auth_schemas.py`
- **Purpose:** Pydantic schemas for authentication requests.
- **Models:**
    - `LoginRequestSchema(BaseModel)`: `email: EmailStr`, `password: str`
    - `MFAChallengeData(BaseModel)`: `user_id: uuid.UUID`, `available_methods: List[MFAMethod]`, `temp_mfa_token: str` // Token to proceed with MFA verify
    - `MFAChallengeResponseSchema(BaseModel)`: `mfa_required: bool = True`, `challenge_data: MFAChallengeData`
- **Documentation:** Pydantic models for user login and MFA challenge responses.

---
#### `core/services/` (Detailed Logic)

**`AuthService`** (`auth_service.py`):
- `__init__`: Takes `UserRepository`, `PasswordManager`, `TokenService`, `SessionService`, `MFAService`.
- `authenticate_user(email, password, ip_address, user_agent)`:
    1. Get user by email from `UserRepository`. Raise `InvalidCredentialsException` if not found or inactive.
    2. Verify password using `PasswordManager`. Raise `InvalidCredentialsException` if invalid.
    3. Check if user has MFA enabled using `MFAService.get_user_mfa_status`.
    4. If MFA enabled:
        - Generate a temporary MFA challenge token (short-lived, stored in Redis perhaps, or a stateless signed token).
        - Raise `MFAChallengeRequiredException` with `user_id`, available MFA methods, and the temp token.
    5. If MFA not enabled:
        - Create session using `SessionService.create_session`.
        - Generate access and refresh tokens using `TokenService.generate_auth_tokens`.
        - Update last login time using `UserRepository`.
        - Return tokens and user object.
- `logout_user(refresh_token_jti, session_id)`:
    1. If `refresh_token_jti`, revoke it using `TokenService.revoke_refresh_token_by_jti`.
    2. If `session_id`, revoke session using `SessionService.revoke_session`.
- `verify_mfa_and_login(user_id, mfa_code, mfa_method, ip_address, user_agent)`:
    1. Fetch user using `UserRepository`.
    2. Verify MFA code using `MFAService.verify_mfa_code`. Raise `MFAInvalidCodeException` if invalid.
    3. If valid, create session using `SessionService.create_session`.
    4. Generate access and refresh tokens using `TokenService.generate_auth_tokens`.
    5. Update last login time.
    6. Return tokens.

**`RegistrationService`** (`registration_service.py`):
- `__init__`: Takes `UserRepository`, `PasswordManager`, `NotificationService`, `OAuthService`.
- `register_new_user(user_create_data)`:
    1. Check if email exists using `UserRepository`. Raise `EmailAlreadyExistsException`.
    2. Hash password using `PasswordManager`.
    3. Create user in DB using `UserRepository` (status: inactive, unverified).
    4. Generate email verification token (e.g., `itsdangerous.URLSafeTimedSerializer`). Store token and expiry with user.
    5. Send verification email via `NotificationService` (with link including token and `FRONTEND_URL`).
    6. Return created `User` object.
- `verify_email_address(token)`:
    1. Deserialize and validate token (check signature, expiry). Raise `InvalidTokenException` or `TokenExpiredException`.
    2. Get user ID from token payload. Fetch user using `UserRepository`.
    3. Mark user as verified and active. Clear verification token. Save user.
    4. Return user.
- `resend_verification_email(email)`:
    1. Fetch user by email. Ensure not already verified.
    2. Generate new token, update user, send email (similar to registration).
- `handle_social_login(provider, auth_code_or_token, ip_address, user_agent)`:
    1. Get social user info (email, social_id, name) from `OAuthService.get_social_user_info`.
    2. Try to find user by `social_provider_id` and `provider` using `UserRepository`.
    3. If user exists:
        - Update last login, potentially sync profile info.
    4. If user does not exist by social ID, try by email:
        - If email exists and no social ID, link account (optional, requires user confirmation).
        - If email does not exist, create new user with social details, mark as verified.
    5. Create session, generate tokens. Return tokens and user.

**`TokenService`** (`token_service.py`):
- `__init__`: Takes `JWTManager`, `UserRepository`, `TokenRevocationRepository` (Redis-backed).
- `generate_auth_tokens(user_id, roles, subscription_tier)`:
    1. Prepare data for access token: `{"sub": str(user_id), "roles": roles, "tier": subscription_tier, "type": "access"}`.
    2. Prepare data for refresh token: `{"sub": str(user_id), "type": "refresh"}`.
    3. Create access token using `JWTManager.create_access_token`.
    4. Create refresh token using `JWTManager.create_refresh_token`.
    5. Return access token object and refresh token object (containing token string and JTI).
- `refresh_access_token(refresh_token_str)`:
    1. Decode refresh token using `JWTManager.decode_token`. Get `sub` (user_id) and `jti`.
    2. Check if JTI is blacklisted using `TokenRevocationRepository.is_blacklisted`. Raise `InvalidTokenException` if blacklisted.
    3. Fetch user by ID. Raise `UserNotFoundException` if not found.
    4. Generate new access token.
    5. **Refresh Token Rotation:**
        - Blacklist the used refresh token JTI using `TokenRevocationRepository.add_to_blacklist`.
        - Generate a *new* refresh token.
    6. Return new access token object and new refresh token object.
- `validate_token_and_get_user_id(token_str, token_type="access")`:
    1. Decode token. Ensure `type` claim matches `token_type`.
    2. Check JTI against blacklist if it's a refresh token or if access token revocation is supported.
    3. Return `user_id` from `sub` claim.
- `revoke_refresh_token_by_jti(jti, expires_at)`:
    1. Add `jti` to blacklist using `TokenRevocationRepository.add_to_blacklist` with its original expiry.

**`MFAService`** (`mfa_service.py`):
- `__init__`: Takes `UserRepository`, `MFARepository`, `OTPService` (for email/SMS OTPs), `TOTPHandler`, `NotificationService`, `Settings`.
- `setup_mfa_method(user_id, method, value)`:
    1. Fetch user. Check if method already setup.
    2. If `method == MFAMethod.TOTP`:
        - Generate secret using `TOTPHandler.generate_totp_secret`.
        - Encrypt and store secret with user in `MFARepository`.
        - Return provisioning URI using `TOTPHandler.get_totp_uri`.
    3. If `method == MFAMethod.SMS`:
        - Validate `value` (phone number). Encrypt and store.
        - Generate OTP using `OTPService.generate_and_store_otp("sms_mfa_setup", user_id)`.
        - Send OTP via `NotificationService.send_sms`.
    4. If `method == MFAMethod.EMAIL`:
        - `value` is user's email. Store it.
        - Generate OTP using `OTPService.generate_and_store_otp("email_mfa_setup", user_id)`.
        - Send OTP via `NotificationService.send_email`.
    5. Mark factor as pending verification initially.
- `verify_mfa_code(user_id, method, code)`:
    1. Fetch user and their MFA factor for `method` from `MFARepository`.
    2. If `method == MFAMethod.TOTP`: Verify using `TOTPHandler.verify_totp_code`.
    3. If `method == MFAMethod.SMS` or `MFAMethod.EMAIL`: Verify using `OTPService.verify_otp`.
    4. If verified and factor was pending, mark it as `is_enabled=True` in `MFARepository`. Update user's global `mfaEnabled` flag if it's the first enabled factor.
    5. Return `True` or `False`.
- `disable_mfa_method(user_id, method)`:
    1. Fetch user. Find MFA factor for `method`.
    2. Mark factor as `is_enabled=False` or delete it via `MFARepository`.
    3. If no other MFA methods are enabled, update user's global `mfaEnabled` to `False`.
- `generate_recovery_codes(user_id)`:
    1. Generate N (e.g., 10) unique recovery codes (`token_generator.generate_secure_token(length=10)`).
    2. Hash each code using `PasswordManager.get_password_hash`.
    3. Delete old codes and store new hashed codes in `RecoveryCodeModel` via `MFARepository`.
    4. Return plain text codes to user *once*.
- `verify_recovery_code(user_id, code)`:
    1. Iterate through user's active recovery codes from `MFARepository`.
    2. For each stored hashed code, use `PasswordManager.verify_password(code, hashed_code)`.
    3. If a match is found, mark that recovery code as used via `MFARepository`. Return `True`.
    4. If no match, return `False`.
- `get_user_mfa_status(user_id)`:
    1. Fetch user. Fetch all enabled MFA factors for user from `MFARepository`.
    2. Return a dict like `{"is_mfa_enabled": user.mfaEnabled, "enabled_methods": [factor.method for factor in factors]}`.

**`PasswordService`** (`password_service.py`):
- `__init__`: Takes `UserRepository`, `PasswordManager`, `NotificationService`, `Settings`.
- `request_password_reset(email)`:
    1. Fetch user by email. Raise `UserNotFoundException` if not found or inactive/unverified.
    2. Generate password reset token (`itsdangerous` or `token_generator`).
    3. Store hashed token and expiry with user via `UserRepository`.
    4. Send password reset email via `NotificationService` (link with token and `FRONTEND_URL`).
- `reset_password(token, new_password)`:
    1. Deserialize and validate token. Get user ID.
    2. Fetch user. Check token validity/expiry against stored token. Raise `InvalidTokenException`.
    3. Hash `new_password` using `PasswordManager`.
    4. Update user's password, clear reset token via `UserRepository`.
- `change_password(user_id, current_password, new_password)`:
    1. Fetch user by ID.
    2. Verify `current_password` against user's stored hash using `PasswordManager`. Raise `InvalidCredentialsException`.
    3. Hash `new_password`.
    4. Update user's password via `UserRepository`.

**`SessionService`** (`session_service.py`):
- `__init__`: Takes `SessionRepository` (Redis), `UserRepository`, `Settings`.
- `create_session(user_id, ip_address, user_agent)`:
    1. Fetch current active sessions for user from `SessionRepository.get_user_sessions`.
    2. If count >= `settings.CONCURRENT_SESSION_LIMIT`, raise `MaxSessionsReachedException` or revoke oldest.
    3. Generate unique session ID (e.g., `uuid.uuid4().hex`).
    4. Prepare session data: `{"user_id": str(user_id), "ip_address": ip_address, "user_agent": user_agent, "created_at": now_utc_iso, "last_activity": now_utc_iso}`.
    5. Store session in Redis via `SessionRepository.store_session` with TTL (e.g., `REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60`).
    6. Return session ID.
- `get_session_data(session_id)`:
    1. Retrieve from `SessionRepository`.
- `revoke_session(session_id)`:
    1. Delete from `SessionRepository`.
- `revoke_all_user_sessions(user_id, except_session_id)`:
    1. Get all sessions for `user_id`.
    2. Iterate and delete via `SessionRepository` if `session_id != except_session_id`.
- `list_user_sessions(user_id)`:
    1. Retrieve from `SessionRepository`. Return list of `SessionInfoSchema`-like dicts.
- `update_session_activity(session_id)`:
    1. Update `last_activity` timestamp.
    2. Extend TTL in Redis via `SessionRepository.update_session_ttl`.

**`UserService`** (`user_service.py`):
- `__init__`: Takes `UserRepository`.
- `get_user_by_id(user_id)`: Calls `UserRepository`.
- `get_user_by_email(email)`: Calls `UserRepository`.
- `update_user_last_login(user_id)`: Fetches user, updates `last_login_at`, saves via `UserRepository`.
- `get_user_roles(user_id)`: Fetches user with `roles` relationship eager-loaded or queries roles separately.

**`OTPService`** (`otp_service.py`):
- `__init__`: Takes Redis client (`get_redis_client_dependency`), `Settings`.
- `generate_and_store_otp(key_prefix, identifier)`:
    1. Generate OTP code using `token_generator.generate_otp_code()`.
    2. Construct Redis key: `f"otp:{key_prefix}:{identifier}"`.
    3. Store OTP in Redis with TTL from `settings.MFA_OTP_EXPIRE_SECONDS`.
    4. Return OTP code.
- `verify_otp(key_prefix, identifier, otp_code)`:
    1. Construct Redis key.
    2. Get stored OTP from Redis.
    3. If stored OTP exists and matches `otp_code`:
        - Delete OTP from Redis.
        - Return `True`.
    4. Return `False`.

**`OAuthService`** (`oauth_service.py`):
- `__init__`: Takes `httpx.AsyncClient`, `Settings`.
- `async get_social_user_info(provider, token_or_code)`:
    1. Based on `provider`:
        - **Google:**
            - If `token_or_code` is auth code, exchange it for access token using `settings.SOCIAL_GOOGLE_CLIENT_ID`, `_SECRET`, `_REDIRECT_URI`.
            - Use access token to call Google People API (`https://www.googleapis.com/oauth2/v3/userinfo` or similar) to get email, name, sub (provider_id).
        - **Facebook:** Similar flow with Facebook Graph API.
        - **Apple:** More complex, involves validating identity token (JWT) from Apple.
    2. Handle API errors from providers, raise `OAuthIntegrationException`.
    3. Return `{"email": ..., "social_id": ..., "full_name": ...}`.

---
#### `infrastructure/repositories/` (Key Methods)

**`UserRepository`**:
- `create_user(user_model_instance)`: Adds and commits.
- `get_user_by_id(user_id)`: Queries `UserModel`.
- `get_user_by_email(email)`: Queries `UserModel`.
- `get_user_by_social_id(provider, social_id)`: Queries `UserModel`.
- `update_user(user_model_instance, update_data_dict)`: Updates fields, commits.
- `add_role_to_user(user, role_name)`: Finds/creates `RoleModel`, appends to `user.roles`.
- `get_user_with_roles(user_id)`: Fetches user with `roles` relationship loaded.

**`MFARepository`**:
- `add_mfa_factor(user_id, method, secret_encrypted, phone_encrypted, email)`: Creates and saves `MFAModel`.
- `get_mfa_factors_for_user(user_id)`: Queries `MFAModel`.
- `get_mfa_factor_by_method(user_id, method)`: Queries `MFAModel`.
- `update_mfa_factor(mfa_factor, update_data)`: Updates, commits.
- `delete_mfa_factor(mfa_factor)`: Deletes, commits.
- `add_recovery_codes(user_id, hashed_codes_list)`: Deletes old, adds new `RecoveryCodeModel` instances.
- `find_and_use_recovery_code(user_id, hashed_code_attempt)`: This logic is tricky with hashes. Better: `get_recovery_code_by_user_and_hash(user_id, hashed_code) -> Optional[RecoveryCodeModel]`, then service marks as used. Or iterate and verify in service, then tell repo to mark specific ID as used. Simpler: `get_active_recovery_codes_for_user(user_id) -> List[RecoveryCodeModel]`, service does verification loop, then `mark_recovery_code_used(code_id)`.

**`SessionRepository`** (Redis):
- `store_session(session_id, user_id, data_dict, ttl_seconds)`: `redis.set(f"session:{session_id}", json.dumps(data_dict), ex=ttl_seconds)`. Store user's session IDs in a set: `redis.sadd(f"user_sessions:{user_id}", session_id)`.
- `get_session(session_id)`: `redis.get(...)`, then `json.loads(...)`.
- `delete_session(session_id, user_id)`: `redis.delete(...)`. Remove from user's set: `redis.srem(f"user_sessions:{user_id}", session_id)`.
- `get_user_sessions_ids(user_id)`: `redis.smembers(f"user_sessions:{user_id}")`. Service then fetches each session.
- `update_session_ttl(session_id, ttl_seconds)`: `redis.expire(f"session:{session_id}", ttl_seconds)`.

**`TokenRevocationRepository`** (Redis):
- `add_to_blacklist(jti, expires_at_datetime)`: Calculate remaining `ttl_seconds = (expires_at_datetime - now_utc).total_seconds()`. If `ttl_seconds > 0`, `redis.set(f"jti_blacklist:{jti}", "revoked", ex=int(ttl_seconds))`.
- `is_blacklisted(jti)`: `redis.exists(f"jti_blacklist:{jti}")`.

---
#### `infrastructure/notifications/`

**`EmailService`**:
- `__init__(settings: Settings)`
- `async send_email(to_email, subject, html_content)`:
    - Logic: Uses `aiofiles` for templates if complex, or simple string formatting.
    - Uses `smtplib.SMTP_SSL` or `smtplib.SMTP` with `starttls` for SMTP, or `httpx` for an email API.
    - Reads credentials from `settings`.

**`SMSService`**:
- `__init__(settings: Settings)`: Initializes Twilio client or other provider SDK.
- `async send_sms(to_phone, message)`:
    - Logic: Calls provider's API (e.g., `twilio_client.messages.create(...)`).
    - Reads credentials from `settings`.

---
#### `api/v1/routers/` (Key Endpoint Logic)

**`AuthRouter`**:
- `/login` (POST): Calls `AuthService.authenticate_user`. If `MFAChallengeRequiredException`, return 401 with challenge data. Else, set tokens in secure, HttpOnly cookies and return user info.
- `/refresh` (POST): Calls `TokenService.refresh_access_token`. Returns new tokens (in body or cookies).
- `/logout` (POST): Takes refresh token JTI from request (or cookie). Calls `AuthService.logout_user`. Clears cookies.

**`RegistrationRouter`**:
- `/` (POST, for email+pass): Calls `RegistrationService.register_new_user`.
- `/verify-email` (POST): Calls `RegistrationService.verify_email_address`.
- `/resend-verification` (POST): Calls `RegistrationService.resend_verification_email`.
- `/social/{provider}` (POST): Calls `RegistrationService.handle_social_login`. Sets cookies, returns user.

**`MFARouter`**:
- `/setup` (POST): Calls `MFAService.setup_mfa_method`.
- `/verify-setup` (POST): Calls `MFAService.verify_mfa_code` to confirm setup.
- `/disable` (POST): Calls `MFAService.disable_mfa_method`.
- `/recovery-codes` (GET): Calls `MFAService.generate_recovery_codes` (if none exist or regeneration requested).
- `/login/verify` (POST): Takes `temp_mfa_token` from `MFAChallengeResponse` and `mfa_code`. Calls `AuthService.verify_mfa_and_login`.
- `/status` (GET): Calls `MFAService.get_user_mfa_status`.

**`PasswordRouter`**:
- `/forgot` (POST): Calls `PasswordService.request_password_reset`.
- `/reset` (POST): Calls `PasswordService.reset_password`.
- `/change` (POST, authenticated): Calls `PasswordService.change_password`.

**`SessionRouter`**:
- `/` (GET, authenticated): Calls `SessionService.list_user_sessions`.
- `/{session_id}` (DELETE, authenticated): Calls `SessionService.revoke_session`.
- `/revoke-all-others` (POST, authenticated): Calls `SessionService.revoke_all_user_sessions`.

**`UserRouter`**:
- `/me` (GET, authenticated): Returns `current_user` from dependency.

This detailed breakdown should be sufficient for the SDS.