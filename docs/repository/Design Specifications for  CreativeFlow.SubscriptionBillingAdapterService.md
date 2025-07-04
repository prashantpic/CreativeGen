# Software Design Specification: CreativeFlow.SubscriptionBillingAdapterService

## 1. Introduction

### 1.1. Purpose

This document outlines the software design for the `CreativeFlow.SubscriptionBillingAdapterService`. This microservice acts as an adapter layer between the CreativeFlow AI platform's internal services and the Odoo ERP system. Its primary responsibilities include:
*   Managing user subscription lifecycles (upgrades, downgrades, cancellations) by orchestrating calls to Odoo.
*   Handling the platform's credit system (balance inquiries, deductions, refunds) via Odoo.
*   Facilitating payment processing through Odoo's integration with Stripe and PayPal.
*   Triggering invoice generation and managing tax calculations via Odoo.
*   Exposing internal RESTful APIs for other platform services to interact with these billing and subscription functionalities.

### 1.2. Scope

This SDS covers the design of the Python FastAPI application, including its API endpoints, internal domain logic, infrastructure clients (Odoo, Stripe, PayPal, PostgreSQL), data models, and configuration. It details how the service will fulfill requirements REQ-014, REQ-015, REQ-016, and INT-003. The actual business rules for subscription tiers, credit costs, payment processing details, invoice content, and tax rules are assumed to be implemented and managed within the Odoo ERP platform. This service adapts and orchestrates those functionalities.

### 1.3. Definitions, Acronyms, and Abbreviations

*   **API**: Application Programming Interface
*   **CRUD**: Create, Read, Update, Delete
*   **CSRF**: Cross-Site Request Forgery
*   **DB**: Database
*   **DTO**: Data Transfer Object
*   **ERP**: Enterprise Resource Planning
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **GDPR**: General Data Protection Regulation
*   **HTTP**: Hypertext Transfer Protocol
*   **JWT**: JSON Web Token
*   **JSON**: JavaScript Object Notation
*   **ORM**: Object-Relational Mapper
*   **Pydantic**: A data validation and settings management library using Python type annotations.
*   **OdooRPC**: Python library for communicating with Odoo via XML-RPC or JSON-RPC.
*   **REQ**: Requirement
*   **REST**: Representational State Transfer
*   **SDK**: Software Development Kit
*   **SDS**: Software Design Specification
*   **SQLAlchemy**: SQL toolkit and Object-Relational Mapper for Python.
*   **UUID**: Universally Unique Identifier

## 2. System Overview

The Subscription & Billing Adapter Service is a Python FastAPI microservice. It serves as a crucial link between the core CreativeFlow platform and the Odoo ERP system, which is the source of truth for all subscription, billing, credit, and financial data.

**High-Level Interaction Flow:**
1.  Other CreativeFlow microservices (e.g., User Management, AI Generation Orchestration) make requests to this adapter's internal REST API.
2.  The adapter validates the request and, if necessary, fetches user context (e.g., current subscription tier, user ID) from the main application's PostgreSQL database.
3.  The adapter's domain services orchestrate the required business logic, primarily by translating the request into appropriate calls to the Odoo ERP system via the `OdooClient`.
4.  The `OdooClient` uses OdooRPC to communicate with Odoo's specific models and methods.
5.  Odoo performs the core business operations (e.g., updates subscription, deducts credits, processes payment via its Stripe/PayPal integration, generates invoices).
6.  The `OdooClient` receives the response from Odoo.
7.  The adapter's domain services process the Odoo response, potentially mapping it to internal domain models.
8.  The API layer formats the response and sends it back to the calling microservice.

Direct interaction with Stripe or PayPal SDKs by this adapter will be minimal and conditional, primarily if Odoo's orchestration requires the adapter to handle specific tokenization steps or generate UI links not provided by Odoo.

## 3. Detailed Design

This section details the design of each component and file within the `CreativeFlow.SubscriptionBillingAdapterService` repository.

### 3.1. `src/creativeflow/services/subbilling/__init__.py`
*   **Purpose**: Initializes the `subbilling` Python package.
*   **Logic**: Can be empty or used to expose key components at the package level.
    python
    # Example:
    # from .main import app
    # from .domain.services.subscription_service import SubscriptionService
    # from .domain.services.credit_service import CreditService
    

### 3.2. `src/creativeflow/services/subbilling/core/__init__.py`
*   **Purpose**: Initializes the `core` sub-package.
*   **Logic**: Empty.

### 3.3. `src/creativeflow/services/subbilling/core/config.py`
*   **Purpose**: Provides centralized application configuration.
*   **Class**: `Settings(BaseSettings)` from Pydantic.
*   **Attributes**:
    *   `ODOO_URL: str`
    *   `ODOO_DB: str`
    *   `ODOO_USERNAME: str`
    *   `ODOO_PASSWORD: SecretStr`
    *   `DATABASE_URL: SecretStr` (For PostgreSQL connection)
    *   `STRIPE_API_KEY: Optional[SecretStr] = None`
    *   `PAYPAL_CLIENT_ID: Optional[SecretStr] = None`
    *   `PAYPAL_CLIENT_SECRET: Optional[SecretStr] = None`
    *   `INTERNAL_SERVICE_API_KEY: Optional[SecretStr] = None` (For securing internal API calls to this service)
    *   `LOG_LEVEL: str = "INFO"`
*   **Method**: `load_settings()`: Implicitly handled by Pydantic's `BaseSettings` loading from environment variables.
*   **Logic**: Loads settings from environment variables. Uses `SecretStr` for sensitive values.
    python
    from pydantic import SecretStr
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from typing import Optional

    class Settings(BaseSettings):
        ODOO_URL: str
        ODOO_DB: str
        ODOO_USERNAME: str
        ODOO_PASSWORD: SecretStr
        DATABASE_URL: SecretStr # For main app DB User context
        
        STRIPE_API_KEY: Optional[SecretStr] = None
        PAYPAL_CLIENT_ID: Optional[SecretStr] = None
        PAYPAL_CLIENT_SECRET: Optional[SecretStr] = None
        
        INTERNAL_SERVICE_API_KEY: Optional[SecretStr] = None # For API security if needed
        LOG_LEVEL: str = "INFO"

        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    settings = Settings()
    

### 3.4. `src/creativeflow/services/subbilling/core/security.py`
*   **Purpose**: Security utility functions, primarily for internal API authentication.
*   **Function**: `verify_internal_api_key(api_key_header: Optional[str] = Header(None))`
    *   **Parameters**: `api_key_header: Optional[str]` (from HTTP Header `X-Internal-API-Key`)
    *   **Returns**: `bool` (or raises `HTTPException` if invalid)
    *   **Logic**:
        1.  Retrieves `settings.INTERNAL_SERVICE_API_KEY`.
        2.  If `settings.INTERNAL_SERVICE_API_KEY` is set:
            *   Checks if `api_key_header` is provided. If not, raise `HTTPException(status_code=401, detail="Internal API Key required")`.
            *   Compares `api_key_header` with `settings.INTERNAL_SERVICE_API_KEY.get_secret_value()`. If mismatch, raise `HTTPException(status_code=403, detail="Invalid Internal API Key")`.
        3.  If `settings.INTERNAL_SERVICE_API_KEY` is not set, this check is skipped (assuming security is handled at gateway or another layer).
        4.  Returns `True` if valid or skipped.
    python
    from fastapi import HTTPException, Header, Depends
    from typing import Optional
    from .config import settings # Assuming settings is instantiated in config.py

    async def verify_internal_api_key(api_key_header: Optional[str] = Header(None, alias="X-Internal-API-Key")):
        if settings.INTERNAL_SERVICE_API_KEY:
            if not api_key_header:
                raise HTTPException(status_code=401, detail="Internal API Key required")
            if api_key_header != settings.INTERNAL_SERVICE_API_KEY.get_secret_value():
                raise HTTPException(status_code=403, detail="Invalid Internal API Key")
        return True # Or some other indicator if needed, or just let it pass if no key configured
    

### 3.5. `src/creativeflow/services/subbilling/infrastructure/__init__.py`
*   **Purpose**: Initializes the `infrastructure` sub-package.
*   **Logic**: Empty.

### 3.6. `src/creativeflow/services/subbilling/infrastructure/odoo_client.py`
*   **Purpose**: Client for interacting with Odoo ERP.
*   **Class**: `OdooClient`
    *   **`__init__(self, config: Settings)`**:
        *   Stores `config`.
        *   Initializes `self.odoo: Optional[odoorpc.ODOO] = None`.
        *   Calls `self._connect()`.
    *   **`_connect(self)`**:
        *   Establishes connection to Odoo using `odoorpc.ODOO(config.ODOO_URL, protocol='jsonrpc', port=80)` (or appropriate port from URL).
        *   Logs in using `self.odoo.login(config.ODOO_DB, config.ODOO_USERNAME, config.ODOO_PASSWORD.get_secret_value())`.
        *   Handles connection errors and logs them.
    *   **`_ensure_connection(self)`**:
        *   Checks if `self.odoo` is connected; if not, calls `self._connect()`.
        *   Implements retry logic for connection failures.
    *   **`_execute_kw(self, model: str, method: str, args: list, kwargs: Optional[dict] = None)`**:
        *   A private helper to wrap `self.odoo.execute_kw` with error handling and connection checks.
        *   Calls `self._ensure_connection()`.
        *   Executes the Odoo method.
        *   Handles `odoorpc.error.RPCError` and other potential exceptions, logging details and re-raising as custom service exceptions if necessary.
    *   **Subscription Methods (examples, actual model/method names depend on Odoo customization):**
        *   `get_subscription_details(self, user_id_cf: str) -> dict`:
            *   Finds Odoo `res.partner` linked to `user_id_cf` (e.g., via a custom field).
            *   Finds related `sale.subscription` records for that partner.
            *   Returns relevant subscription data (plan, status, dates).
        *   `update_subscription(self, user_id_cf: str, new_plan_odoo_id: int, action: str) -> dict`:
            *   `action` could be 'upgrade', 'downgrade', 'cancel'.
            *   Locates user's partner and current subscription.
            *   Calls Odoo methods to process the subscription change (e.g., create new subscription, close old one, update stage).
        *   `get_current_user_plan_info(self, user_id_cf: str) -> Optional[dict]`:
            * Fetches the user's `res.partner` record in Odoo using `user_id_cf`.
            * Queries active `sale.subscription` associated with the partner.
            * Returns details like plan name, start/end dates, status.
    *   **Credit Methods (examples):**
        *   `get_credit_balance(self, user_id_cf: str) -> float`:
            *   Locates Odoo `res.partner`.
            *   Reads custom credit balance field from partner or related credit model.
        *   `deduct_credits(self, user_id_cf: str, amount: float, reason: str, reference_id: Optional[str] = None) -> bool`:
            *   Locates Odoo `res.partner`.
            *   Calls Odoo method/workflow to deduct credits, creating a credit transaction log in Odoo.
        *   `add_credits(self, user_id_cf: str, amount: float, reason: str, reference_id: Optional[str] = None) -> bool`:
            *   Similar to `deduct_credits` but for adding credits (e.g., refunds).
    *   **Billing/Invoice/Tax Methods (examples):**
        *   `trigger_invoice_generation_for_subscription(self, subscription_odoo_id: int) -> str`:
            *   Calls Odoo method to generate an invoice for a given subscription. Returns Odoo invoice ID.
        *   `get_invoices_for_user(self, user_id_cf: str, limit: int = 10) -> list`:
            *   Finds partner, then related `account.move` (invoices). Returns list of invoice details.
        *   `get_payment_portal_link_for_user(self, user_id_cf: str) -> Optional[str]`:
            * Calls Odoo method to get a portal link for the user to manage their subscriptions/payments if Odoo provides this.
        *   `calculate_tax_for_order(self, order_details: dict) -> dict`:
            *   `order_details` might include product IDs, quantities, user location.
            *   Calls Odoo methods to calculate taxes based on its configured tax engine.
    *   **Failed Payment Handling (example):**
        *   `process_dunning_notification(self, subscription_odoo_id: int, failure_reason: str) -> dict`:
            *   Calls Odoo methods to update subscription status (e.g., 'suspended') and trigger dunning workflows in Odoo.
*   **Error Handling**: Implement robust error handling for Odoo RPC calls, network issues, and authentication failures. Map Odoo errors to appropriate service-level exceptions.

### 3.7. `src/creativeflow/services/subbilling/infrastructure/stripe_client.py`
*   **Purpose**: Conditional Stripe API interaction. Primarily, Odoo will handle Stripe. This client exists for specific, limited use cases if Odoo cannot cover them directly for the adapter's needs (e.g., frontend needs a direct Stripe SetupIntent for SCA, or managing payment methods directly via Stripe if not through Odoo's portal).
*   **Class**: `StripeClient`
    *   `__init__(self, api_key: Optional[str])`: Initializes Stripe SDK if `api_key` is provided.
    *   `get_payment_method_update_session_url(self, customer_stripe_id: str, return_url: str) -> Optional[str]`:
        *   Uses `stripe.billing_portal.Session.create` to generate a URL for Stripe's customer billing portal for updating payment methods.
        *   Requires `customer_stripe_id` (which Odoo should store).
    *   Other methods will be added *only if* Odoo's integration proves insufficient for a specific flow required by the platform.
*   **Feature Toggle**: Usage of this client's methods should be gated by `settings.ENABLE_DIRECT_STRIPE_CALLS` and `settings.STRIPE_API_KEY` presence.

### 3.8. `src/creativeflow/services/subbilling/infrastructure/paypal_client.py`
*   **Purpose**: Conditional PayPal API interaction. Similar to `StripeClient`, Odoo is primary.
*   **Class**: `PayPalClient`
    *   `__init__(self, client_id: Optional[str], client_secret: Optional[str])`: Initializes PayPal SDK if credentials provided.
    *   `get_payment_method_update_portal_url(self, user_paypal_subscription_id: str) -> Optional[str]`:
        *   If PayPal offers a direct portal link for users to manage recurring payment methods tied to a subscription ID, this method would construct/retrieve it.
    *   Other methods added *only if* specific direct PayPal interactions are unavoidable by Odoo.
*   **Feature Toggle**: Usage gated by `settings.ENABLE_DIRECT_PAYPAL_CALLS` and PayPal credential presence.

### 3.9. `src/creativeflow/services/subbilling/infrastructure/db/__init__.py`
*   **Purpose**: Initializes the `db` sub-package.
*   **Logic**: Empty.

### 3.10. `src/creativeflow/services/subbilling/infrastructure/db/database.py`
*   **Purpose**: SQLAlchemy setup for PostgreSQL.
*   **Variables**:
    *   `SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.get_secret_value()`
    *   `engine = create_engine(SQLALCHEMY_DATABASE_URL)`
    *   `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`
*   **Function**: `get_db() -> Generator[Session, None, None]`:
    *   Yields a SQLAlchemy `Session` for dependency injection.
    *   Ensures session is closed after use.
    python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession # Alias to avoid naming conflict
    from typing import Generator
    from ....core.config import settings # Adjust import path

    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.get_secret_value()

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db() -> Generator[SQLAlchemySession, None, None]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    

### 3.11. `src/creativeflow/services/subbilling/infrastructure/db/models_db.py`
*   **Purpose**: SQLAlchemy ORM models for reading user context.
*   **Base**: `Base = declarative_base()`
*   **Class**: `User(Base)`
    *   `__tablename__ = "users"` (Matches the main application's user table name)
    *   `id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)`
    *   `email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)`
    *   `subscription_tier: Mapped[str] = mapped_column(String(20), nullable=False, default='Free')`
    *   `credit_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)`
    *   `odoo_partner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)` (Crucial for linking to Odoo)
    *   *(Other fields as needed for context, e.g., `is_active`)*
    *   **Note**: This model is primarily for *reading* context. Writes to user data are handled by the User Management service or Odoo.
    python
    from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Uuid, Integer
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    from sqlalchemy.orm import declarative_base, Mapped, mapped_column
    from decimal import Decimal
    from typing import Optional
    import uuid # For UUID type hinting if needed directly

    Base = declarative_base()

    class User(Base):
        __tablename__ = "users" # Ensure this matches the actual users table name

        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        # email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) # May not be needed by this service
        subscription_tier: Mapped[str] = mapped_column(String(50), nullable=False, default='Free')
        credit_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
        odoo_partner_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, index=True, nullable=True)
        # Add other fields that this adapter might need quick read access to, e.g. user_id_cf for Odoo mapping if different from odoo_partner_id
    

### 3.12. `src/creativeflow/services/subbilling/infrastructure/db/repositories/__init__.py`
*   **Purpose**: Initializes the `repositories` sub-package.
*   **Logic**: Empty.

### 3.13. `src/creativeflow/services/subbilling/infrastructure/db/repositories/user_repository.py`
*   **Purpose**: Data access for User entity context.
*   **Class**: `UserRepository`
    *   `__init__(self, db: SQLAlchemySession)`: Stores `db` session.
    *   `get_user_context_by_id(self, user_id: uuid.UUID) -> Optional[models_db.User]`:
        *   Queries `User` table by `id`. Returns `User` ORM model or `None`.
    *   `get_user_by_odoo_partner_id(self, odoo_partner_id: int) -> Optional[models_db.User]`:
        *   Queries `User` table by `odoo_partner_id`.
    *   `update_user_billing_info_from_odoo(self, user_id: uuid.UUID, subscription_tier: str, credit_balance: Decimal) -> Optional[models_db.User]`:
        *   Updates the local projection of `subscription_tier` and `credit_balance`. This is for optimization/caching; Odoo is the source of truth.
    python
    from sqlalchemy.orm import Session as SQLAlchemySession
    from typing import Optional
    import uuid
    from .. import models_db # Adjust relative import

    class UserRepository:
        def __init__(self, db: SQLAlchemySession):
            self.db = db

        def get_user_context_by_id(self, user_id: uuid.UUID) -> Optional[models_db.User]:
            return self.db.query(models_db.User).filter(models_db.User.id == user_id).first()

        def get_user_by_odoo_partner_id(self, odoo_partner_id: int) -> Optional[models_db.User]:
            return self.db.query(models_db.User).filter(models_db.User.odoo_partner_id == odoo_partner_id).first()
        
        def get_odoo_partner_id(self, user_id: uuid.UUID) -> Optional[int]:
            user = self.get_user_context_by_id(user_id)
            return user.odoo_partner_id if user else None

        # This method assumes this service MIGHT update a local cache/projection.
        # However, Odoo remains the source of truth. This update should ideally be triggered
        # by events from Odoo or a sync process if deemed necessary for performance.
        # For an adapter, it's often better to fetch fresh from Odoo.
        # def update_user_billing_info_projection(self, user_id: uuid.UUID, subscription_tier: str, credit_balance: Decimal) -> Optional[models_db.User]:
        #     user = self.get_user_context_by_id(user_id)
        #     if user:
        #         user.subscription_tier = subscription_tier
        #         user.credit_balance = credit_balance
        #         self.db.commit()
        #         self.db.refresh(user)
        #     return user
    

### 3.14. `src/creativeflow/services/subbilling/domain/__init__.py`
*   **Purpose**: Initializes the `domain` sub-package.
*   **Logic**: Empty.

### 3.15. `src/creativeflow/services/subbilling/domain/models/__init__.py`
*   **Purpose**: Initializes the `domain.models` sub-package.
*   **Logic**: Empty or exports domain models.

### 3.16. `src/creativeflow/services/subbilling/domain/models/subscription_models.py`
*   **Purpose**: Internal domain models for subscriptions.
*   **Pydantic Models**:
    *   `SubscriptionTier(str, Enum)`: `FREE = "Free"`, `PRO = "Pro"`, `TEAM = "Team"`, `ENTERPRISE = "Enterprise"`
    *   `SubscriptionStatus(str, Enum)`: `ACTIVE = "Active"`, `TRIAL = "Trial"`, `SUSPENDED = "Suspended"`, `CANCELLED = "Cancelled"`, `EXPIRED = "Expired"`
    *   `FreemiumLimits(BaseModel)`:
        *   `monthly_generations_limit: int = 100`
        *   `generations_used_this_month: int`
        *   `watermarked_exports: bool = True`
        *   `basic_templates_only: bool = True`
    *   `PlanFeatures(BaseModel)`:
        *   `name: str`
        *   `price_monthly: Optional[Decimal] = None`
        *   `unlimited_standard_generations: bool = False`
        *   `brand_kit_access: bool = False`
        *   `hd_exports: bool = False`
        *   `priority_support: bool = False`
        *   `collaboration_tools: bool = False`
        *   `team_management: bool = False`
        *   `advanced_analytics: bool = False`
        *   `sso_access: bool = False`
        *   `custom_branding: bool = False`
        *   `dedicated_account_manager: bool = False`
    *   `UserSubscriptionDomain(BaseModel)`:
        *   `user_id: UUID`
        *   `odoo_subscription_id: Optional[str] = None`
        *   `current_plan_id: str` # e.g. "pro_monthly"
        *   `current_plan_name: str` # e.g. "Pro Monthly"
        *   `status: SubscriptionStatus`
        *   `current_period_start: Optional[datetime] = None`
        *   `current_period_end: Optional[datetime] = None`
        *   `features: PlanFeatures`
        *   `freemium_limits: Optional[FreemiumLimits] = None` (if on Free tier)
*   **Requirement Mapping**: REQ-014, INT-003.

### 3.17. `src/creativeflow/services/subbilling/domain/models/credit_models.py`
*   **Purpose**: Internal domain models for credits.
*   **Pydantic Models**:
    *   `CreditBalanceDomain(BaseModel)`:
        *   `user_id: UUID`
        *   `balance: Decimal`
        *   `last_updated_at: datetime`
    *   `CreditDeductionRequestDomain(BaseModel)`:
        *   `user_id: UUID`
        *   `amount: Decimal`
        *   `action_type: str` (e.g., "sample_generation", "final_generation_hd")
        *   `reference_id: Optional[str] = None` (e.g., generation_request_id)
        *   `description: Optional[str] = None`
    *   `CreditCost(BaseModel)`:
        *   `action_type: str`
        *   `cost: Decimal`
        *   `is_variable: bool = False`
*   **Requirement Mapping**: REQ-015, REQ-016.

### 3.18. `src/creativeflow/services/subbilling/domain/services/__init__.py`
*   **Purpose**: Initializes the `domain.services` sub-package.
*   **Logic**: Empty.

### 3.19. `src/creativeflow/services/subbilling/domain/services/subscription_service.py`
*   **Purpose**: Business logic for subscription management.
*   **Class**: `SubscriptionService`
    *   `__init__(self, odoo_client: OdooClient, user_repo: UserRepository, odoo_map_service: OdooMappingService)`
    *   `async def get_user_subscription_status(self, user_id: UUID) -> UserSubscriptionDomain`:
        1.  Get `odoo_partner_id` from `user_repo` using `user_id`. If not found, handle appropriately (e.g., user not synced to Odoo).
        2.  Call `odoo_client.get_subscription_details(odoo_partner_id)`.
        3.  Map Odoo response to `UserSubscriptionDomain` using `odoo_map_service`.
        4.  Enrich with plan features based on plan ID.
        5.  If Free tier, calculate and add `FreemiumLimits`.
    *   `async def process_subscription_change(self, user_id: UUID, new_plan_id: str, action: str) -> UserSubscriptionDomain`:
        *   `action` can be "upgrade", "downgrade", "cancel".
        *   Get `odoo_partner_id`.
        *   Determine `odoo_product_id` for `new_plan_id`.
        *   Call `odoo_client.update_subscription(odoo_partner_id, odoo_product_id, action)`.
        *   Handle Odoo response (success/failure).
        *   Fetch and return updated `UserSubscriptionDomain`.
        *   Handles logic for immediate upgrade vs. end-of-cycle downgrade/cancellation as per REQ-6-006.
    *   `async def check_feature_access(self, user_id: UUID, feature_key: str) -> bool`:
        1.  Get user's subscription status (`get_user_subscription_status`).
        2.  Check if `feature_key` is permitted by their `PlanFeatures`.
    *   `async def get_freemium_usage(self, user_id: UUID) -> FreemiumLimits`:
        1. Get `odoo_partner_id`.
        2. Call Odoo client method to fetch current month's generation count for this user.
        3. Return `FreemiumLimits` object.
*   **Requirement Mapping**: REQ-014, INT-003, REQ-6-001 to REQ-6-006.

### 3.20. `src/creativeflow/services/subbilling/domain/services/credit_service.py`
*   **Purpose**: Business logic for credit management.
*   **Class**: `CreditService`
    *   `__init__(self, odoo_client: OdooClient, user_repo: UserRepository, odoo_map_service: OdooMappingService)`
    *   `CREDIT_COSTS = { "sample_generation": Decimal("0.25"), "standard_generation": Decimal("1.00"), "hd_export": Decimal("2.00"), ... }` (from REQ-016)
    *   `async def get_user_credit_balance(self, user_id: UUID) -> CreditBalanceDomain`:
        1.  Get `odoo_partner_id`.
        2.  Call `odoo_client.get_credit_balance(odoo_partner_id)`.
        3.  Map to `CreditBalanceDomain`.
    *   `async def get_credit_cost_for_action(self, action_type: str, user_tier: Optional[str] = None, advanced_params: Optional[dict] = None) -> Decimal`:
        1.  Implement logic from REQ-016.
        2.  Check if `user_tier` (e.g., "Pro") has unlimited standard generations. If so, sample/standard cost is 0.
        3.  For "advanced_ai_feature", price might be dynamic based on `advanced_params` or fetched from a config/Odoo.
        4.  Return cost from `CREDIT_COSTS` or calculated dynamic cost.
    *   `async def check_sufficient_credits(self, user_id: UUID, action_type: str, advanced_params: Optional[dict] = None) -> bool`:
        1.  Get user context (`user_repo` for tier, `odoo_partner_id`).
        2.  Get current balance (`get_user_credit_balance`).
        3.  Get cost for action (`get_credit_cost_for_action` passing tier and params).
        4.  Return `balance >= cost`.
    *   `async def deduct_credits_for_action(self, user_id: UUID, action_type: str, reference_id: Optional[str] = None, advanced_params: Optional[dict] = None) -> bool`:
        1.  Get `odoo_partner_id`.
        2.  Get cost for action (`get_credit_cost_for_action`).
        3.  If cost > 0:
            *   Call `odoo_client.deduct_credits(odoo_partner_id, cost, action_type, reference_id)`.
            *   Log in `UsageLog` (via another service or direct DB write if simple).
        4.  Handle success/failure response from Odoo.
    *   `async def handle_overage_or_insufficient_credits(self, user_id: UUID, action_type: str) -> dict`: (REQ-6-008)
        1.  Determine if it's a Free tier limit or credit insufficiency.
        2.  Return structured response indicating issue and suggesting upgrade/purchase options.
    *   `async def refund_credits_for_system_error(self, user_id: UUID, amount: Decimal, original_action_id: str, reason: str) -> bool`: (REQ-6-012)
        1. Get `odoo_partner_id`.
        2. Call `odoo_client.add_credits(odoo_partner_id, amount, reason, original_action_id)`.
*   **Requirement Mapping**: REQ-015, REQ-016, REQ-3-007, REQ-6-007, REQ-6-008, REQ-6-010, REQ-6-011, REQ-6-012.

### 3.21. `src/creativeflow/services/subbilling/domain/services/payment_orchestration_service.py`
*   **Purpose**: Orchestrates payment, invoicing, tax.
*   **Class**: `PaymentOrchestrationService`
    *   `__init__(self, odoo_client: OdooClient, stripe_client: Optional[StripeClient], paypal_client: Optional[PayPalClient], odoo_map_service: OdooMappingService)`
    *   `async def get_user_invoices_portal_url(self, user_id: UUID) -> Optional[str]`:
        1.  Get `odoo_partner_id`.
        2.  Call `odoo_client.get_payment_portal_link_for_user(odoo_partner_id)`. This might be an Odoo portal link.
    *   `async def get_payment_method_update_url(self, user_id: UUID, provider: str) -> Optional[str]`: (REQ-6-005.6)
        1.  Get `odoo_partner_id`. Fetch related Stripe customer ID or PayPal agreement ID from Odoo.
        2.  If `provider == "stripe"` and `stripe_client` is available and `settings.ENABLE_DIRECT_STRIPE_CALLS`:
            *   Call `stripe_client.get_payment_method_update_session_url()`.
        3.  Else if `provider == "paypal"` and `paypal_client` ...
        4.  Else, try to get a generic portal link from Odoo if it manages this.
    *   `async def trigger_invoice_for_subscription(self, odoo_subscription_id: int) -> str`: (REQ-6-015)
        1.  Call `odoo_client.trigger_invoice_generation_for_subscription(odoo_subscription_id)`.
    *   `async def get_tax_information_for_purchase(self, user_id: UUID, purchase_details: dict) -> dict`: (REQ-6-017)
        1. Get `odoo_partner_id`.
        2. Prepare `order_details` for Odoo (map `purchase_details`).
        3. Call `odoo_client.calculate_tax_for_order(odoo_mapped_order_details)`.
    *   `async def handle_failed_payment(self, user_id: UUID, odoo_subscription_id: int, failure_reason: str)`: (REQ-6-016)
        1. Call `odoo_client.process_dunning_notification(odoo_subscription_id, failure_reason)`.
*   **Requirement Mapping**: INT-003, REQ-6-005, REQ-6-015, REQ-6-016, REQ-6-017.

### 3.22. `src/creativeflow/services/subbilling/domain/services/odoo_mapping_service.py`
*   **Purpose**: Maps data between service models and Odoo formats.
*   **Class**: `OdooMappingService`
    *   Methods will be static or instance methods.
    *   `to_odoo_partner_search_criteria(self, user_id_cf: Optional[UUID] = None, email: Optional[str] = None) -> list`:
        *   Constructs Odoo domain filter list to find `res.partner`.
    *   `from_odoo_partner_to_user_context(self, odoo_partner_data: dict) -> dict`:
        *   Extracts relevant fields (e.g., name, email, custom credit field, subscription state) for internal use.
    *   `from_odoo_subscription_to_domain(self, odoo_subscription_data: dict) -> UserSubscriptionDomain`:
        *   Maps fields like `stage_id`, `plan_id` (Odoo's product/template for subscription), `date_start`, `recurring_next_date`.
    *   `from_odoo_plan_product_to_features(self, odoo_product_data: dict) -> PlanFeatures`:
        *   Maps Odoo product attributes/template details to `PlanFeatures` model.
    *   *(Other mappers as needed for credits, invoices, etc.)*
*   **Requirement Mapping**: INT-003.

### 3.23. `src/creativeflow/services/subbilling/api/__init__.py`
*   **Purpose**: Initializes the `api` sub-package.
*   **Logic**: Empty.

### 3.24. `src/creativeflow/services/subbilling/api/v1/__init__.py`
*   **Purpose**: Initializes the `v1` API sub-package.
*   **Logic**:
    python
    from fastapi import APIRouter
    from .endpoints import subscriptions, credits, payments

    api_v1_router = APIRouter(prefix="/api/v1")
    api_v1_router.include_router(subscriptions.router, tags=["Subscriptions"])
    api_v1_router.include_router(credits.router, tags=["Credits"])
    api_v1_router.include_router(payments.router, tags=["Payments"])
    

### 3.25. `src/creativeflow/services/subbilling/api/v1/schemas.py`
*   **Purpose**: API request/response Pydantic models.
*   **Models**:
    *   `UserIdentifier(BaseModel)`: `user_id: UUID`
    *   **Subscription Schemas (REQ-014, INT-003):**
        *   `SubscriptionPlanInfoSchema(BaseModel)`: (Corresponds to `PlanFeatures` domain model)
            `name: str`, `price_monthly: Optional[Decimal]`, `unlimited_standard_generations: bool`, etc.
        *   `UserSubscriptionResponseSchema(BaseModel)`: (Corresponds to `UserSubscriptionDomain`)
            `user_id: UUID`, `current_plan_id: str`, `current_plan_name: str`, `status: str`, `current_period_end: Optional[datetime]`, `features: SubscriptionPlanInfoSchema`, `freemium_generations_remaining: Optional[int]`
        *   `SubscriptionUpdateRequestSchema(BaseModel)`: `new_plan_id: str` (e.g., "pro_monthly")
    *   **Credit Schemas (REQ-015, REQ-016):**
        *   `CreditBalanceResponseSchema(BaseModel)`: `user_id: UUID`, `balance: Decimal`, `currency: str = "USD"` (or fetched based on context)
        *   `CreditDeductRequestSchema(BaseModel)`: `action_type: str`, `reference_id: Optional[str] = None`, `amount_override: Optional[Decimal] = None` (for variable priced advanced features)
        *   `CreditDeductResponseSchema(BaseModel)`: `success: bool`, `new_balance: Decimal`, `message: Optional[str] = None`
        *   `CreditCostResponseSchema(BaseModel)`: `action_type: str`, `cost: Decimal`
        *   `InsufficientCreditsResponseSchema(BaseModel)`: `message: str`, `required_credits: Decimal`, `current_balance: Decimal`, `upgrade_options: list`
    *   **Payment Schemas (INT-003):**
        *   `PaymentMethodUpdateLinkResponseSchema(BaseModel)`: `update_url: str`
        *   `InvoiceSummarySchema(BaseModel)`: `invoice_id: str`, `date: date`, `total_amount: Decimal`, `status: str`, `pdf_url: Optional[str]`
        *   `InvoiceListResponseSchema(BaseModel)`: `invoices: List[InvoiceSummarySchema]`
        *   `TaxCalculationRequestSchema(BaseModel)`: `items: List[dict]`, `customer_address: dict` (simplified)
        *   `TaxCalculationResponseSchema(BaseModel)`: `subtotal: Decimal`, `tax_amount: Decimal`, `total_amount: Decimal`, `tax_breakdown: List[dict]`
*   **Requirement Mapping**: REQ-014, REQ-015, REQ-016, INT-003.

### 3.26. `src/creativeflow/services/subbilling/api/v1/endpoints/__init__.py`
*   **Purpose**: Initializes the `endpoints` sub-package.
*   **Logic**: Empty.

### 3.27. `src/creativeflow/services/subbilling/api/v1/endpoints/subscriptions.py`
*   **Purpose**: FastAPI router for subscription endpoints.
*   **APIRouter**: `router = APIRouter(prefix="/users/{user_id}/subscription")`
*   **Endpoints**:
    *   `GET /` -> `get_subscription_status_for_user(user_id: UUID, sub_service: SubscriptionService = Depends(get_subscription_service)) -> schemas.UserSubscriptionResponseSchema`:
        *   Calls `sub_service.get_user_subscription_status(user_id)`.
    *   `PUT /` -> `update_user_subscription(user_id: UUID, request: schemas.SubscriptionUpdateRequestSchema, sub_service: SubscriptionService = Depends(get_subscription_service)) -> schemas.UserSubscriptionResponseSchema`:
        *   Determine action ('upgrade', 'downgrade') based on current vs. new plan.
        *   Calls `sub_service.process_subscription_change(user_id, request.new_plan_id, action)`.
    *   `DELETE /` -> `cancel_user_subscription(user_id: UUID, sub_service: SubscriptionService = Depends(get_subscription_service)) -> schemas.UserSubscriptionResponseSchema`:
        *   Calls `sub_service.process_subscription_change(user_id, current_plan_id, "cancel")`.
    *   `GET /freemium-limits` -> `get_user_freemium_limits(user_id: UUID, sub_service: SubscriptionService = Depends(get_subscription_service)) -> domain_models.FreemiumLimits`: (REQ-6-001)
        * Calls `sub_service.get_freemium_usage(user_id)`.
*   **Security**: Endpoints should be protected (e.g., by API Gateway checking JWT for `user_id` match or internal service key).

### 3.28. `src/creativeflow/services/subbilling/api/v1/endpoints/credits.py`
*   **Purpose**: FastAPI router for credit endpoints.
*   **APIRouter**: `router = APIRouter(prefix="/users/{user_id}/credits")`
*   **Endpoints**:
    *   `GET /balance` -> `get_credit_balance_for_user(user_id: UUID, credit_service: CreditService = Depends(get_credit_service)) -> schemas.CreditBalanceResponseSchema`:
        *   Calls `credit_service.get_user_credit_balance(user_id)`.
    *   `POST /deduct` -> `deduct_credits_for_action(user_id: UUID, request: schemas.CreditDeductRequestSchema, credit_service: CreditService = Depends(get_credit_service), sub_service: SubscriptionService = Depends(get_subscription_service)) -> schemas.CreditDeductResponseSchema`:
        1.  Fetch user's current subscription tier using `sub_service`.
        2.  Calculate actual `cost` using `credit_service.get_credit_cost_for_action(request.action_type, user_tier, request.advanced_params_if_any)`.
        3.  Check sufficient credits: `await credit_service.check_sufficient_credits(user_id, effective_cost)`.
        4.  If not sufficient: call `credit_service.handle_overage_or_insufficient_credits(user_id, request.action_type)` and return appropriate error/prompt.
        5.  If sufficient: call `credit_service.deduct_credits_for_action(user_id, request.action_type, request.reference_id, effective_cost)`.
        6.  Return `CreditDeductResponseSchema`.
    *   `GET /cost` -> `get_action_credit_cost(action_type: str = Query(...), user_id: Optional[UUID] = Query(None), credit_service: CreditService = Depends(get_credit_service), sub_service: SubscriptionService = Depends(get_subscription_service)) -> schemas.CreditCostResponseSchema`:
        *   If `user_id` provided, fetch tier to account for "unlimited" features.
        *   Calls `credit_service.get_credit_cost_for_action(action_type, user_tier_if_available)`.
*   **Security**: Protected.

### 3.29. `src/creativeflow/services/subbilling/api/v1/endpoints/payments.py`
*   **Purpose**: FastAPI router for payment utility endpoints.
*   **APIRouter**: `router = APIRouter(prefix="/users/{user_id}/payments")`
*   **Endpoints**:
    *   `GET /manage-methods-url` -> `get_payment_method_update_url(user_id: UUID, provider: str = Query(default="stripe", enum=["stripe", "paypal"]), payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)) -> schemas.PaymentMethodUpdateLinkResponseSchema`: (REQ-6-005.6)
        *   Calls `payment_service.get_payment_method_update_url(user_id, provider)`.
    *   `GET /invoices` -> `list_user_invoices(user_id: UUID, limit: int = Query(10, ge=1, le=50), payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)) -> schemas.InvoiceListResponseSchema`: (REQ-6-005.3, REQ-6-015)
        *   Get `odoo_partner_id` from `user_repo`.
        *   Call `odoo_client.get_invoices_for_user(odoo_partner_id, limit)`.
        *   Map Odoo response to `InvoiceListResponseSchema`.
    *   `POST /tax-preview` -> `get_tax_info_for_purchase_preview(user_id: UUID, request: schemas.TaxCalculationRequestSchema, payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)) -> schemas.TaxCalculationResponseSchema`: (REQ-6-017)
        *   Calls `payment_service.get_tax_information_for_purchase(user_id, request.model_dump())`.
*   **Security**: Protected.

### 3.30. `src/creativeflow/services/subbilling/dependencies.py`
*   **Purpose**: FastAPI dependency injectors.
*   **Functions**:
    *   `def get_settings() -> Settings: return Settings()`
    *   `def get_db_session() -> Generator[SQLAlchemySession, None, None]: ...` (as in 3.10)
    *   `def get_odoo_client(settings_dep: Settings = Depends(get_settings)) -> OdooClient: return OdooClient(config=settings_dep)`
    *   `def get_stripe_client(settings_dep: Settings = Depends(get_settings)) -> Optional[StripeClient]: ...`
    *   `def get_paypal_client(settings_dep: Settings = Depends(get_settings)) -> Optional[PayPalClient]: ...`
    *   `def get_user_repository(db: SQLAlchemySession = Depends(get_db_session)) -> UserRepository: return UserRepository(db=db)`
    *   `def get_odoo_mapping_service() -> OdooMappingService: return OdooMappingService()`
    *   `def get_subscription_service(...) -> SubscriptionService: ...` (injects OdooClient, UserRepository, OdooMappingService)
    *   `def get_credit_service(...) -> CreditService: ...` (injects OdooClient, UserRepository, OdooMappingService)
    *   `def get_payment_orchestration_service(...) -> PaymentOrchestrationService: ...` (injects OdooClient, StripeClient, PayPalClient, OdooMappingService)

### 3.31. `src/creativeflow/services/subbilling/main.py`
*   **Purpose**: Service entry point.
*   **FastAPI App Initialization**:
    *   `app = FastAPI(title="CreativeFlow Subscription & Billing Adapter", version="1.0.0")`
    *   Include `api_v1_router` from `api.v1`.
    *   Configure CORS middleware.
    *   Add custom exception handlers.
    *   Define startup event (e.g., to initialize OdooClient connection pool or check DB connection) and shutdown event.
    python
    from fastapi import FastAPI
    from .api.v1 import api_v1_router
    from .core.config import settings # To access LOG_LEVEL for uvicorn if run programmatically
    # from .dependencies import init_global_odoo_client # if using a global client
    import logging

    # Configure logging
    logging.basicConfig(level=settings.LOG_LEVEL.upper())
    logger = logging.getLogger(__name__)

    app = FastAPI(
        title="CreativeFlow Subscription & Billing Adapter Service",
        description="Adapts subscription, billing, and credit management functionalities from Odoo ERP.",
        version="1.0.0"
    )

    # @app.on_event("startup")
    # async def startup_event():
    #     logger.info("Subscription & Billing Adapter starting up...")
    #     # Initialize global Odoo client pool or other startup tasks
    #     # init_global_odoo_client(settings)
    #     pass

    # @app.on_event("shutdown")
    # async def shutdown_event():
    #     logger.info("Subscription & Billing Adapter shutting down...")
    #     # Cleanup resources
    #     pass

    app.include_router(api_v1_router)

    # Basic health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        # Add checks for Odoo connectivity, DB connectivity if used extensively
        return {"status": "healthy"}
    

### 3.32. `pyproject.toml`
*   **Purpose**: Project metadata and dependencies.
*   **Key Sections**:
    *   `[tool.poetry]`: name, version, description, authors, license, python version.
    *   `[tool.poetry.dependencies]`:
        *   `python = "^3.11"`
        *   `fastapi = "^0.111.0"`
        *   `uvicorn = {extras = ["standard"], version = "^0.29.0"}`
        *   `pydantic = "^2.7.1"`
        *   `pydantic-settings = "^2.2.1"`
        *   `odoorpc = "^0.8.0"`
        *   `stripe = "^9.0.0"` (Adjust to specific version used, e.g. 9.15.0)
        *   `paypalrestsdk = "^1.13.1"`
        *   `SQLAlchemy = "^2.0.29"`
        *   `psycopg2-binary = "^2.9.9"` (For PostgreSQL)
        *   `python-jose = {extras = ["cryptography"], version = "^3.3.0"}` (If handling JWTs directly)
        *   `passlib = {extras = ["bcrypt"], version = "^1.7.4"}` (If handling passwords, though unlikely for adapter)
    *   `[tool.poetry.group.dev.dependencies]`: pytest, httpx (for testing FastAPI), pytest-asyncio, black, ruff, mypy.
    *   `[build-system]`: requires, build-backend.

### 3.33. `requirements.txt`
*   **Purpose**: Alternative dependency listing.
*   **Logic**: Generated from `poetry export -f requirements.txt --output requirements.txt` if using Poetry.

### 3.34. `Dockerfile`
*   **Purpose**: Build Docker image.
*   **Content**:
    dockerfile
    FROM python:3.11-slim

    WORKDIR /app

    # Create a non-root user
    RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

    # Install poetry (or copy requirements.txt and pip install)
    # Using poetry as an example
    RUN pip install poetry==1.8.2
    COPY pyproject.toml poetry.lock* ./
    RUN poetry config virtualenvs.create false && \
        poetry install --no-dev --no-interaction --no-ansi

    # Copy application code
    COPY ./src ./src

    USER appuser
    ENV PYTHONPATH=/app

    EXPOSE 8000

    # CMD ["uvicorn", "src.creativeflow.services.subbilling.main:app", "--host", "0.0.0.0", "--port", "8000"]
    # Or using a gunicorn setup for more robustness:
    # COPY ./gunicorn_conf.py .
    CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./gunicorn_conf.py", "src.creativeflow.services.subbilling.main:app"]
    # (Requires adding gunicorn_conf.py and gunicorn to dependencies)
    
    *Need a `gunicorn_conf.py` if using Gunicorn:*
    python
    # gunicorn_conf.py
    import multiprocessing

    bind = "0.0.0.0:8000"
    workers = multiprocessing.cpu_count() * 2 + 1
    worker_class = "uvicorn.workers.UvicornWorker"
    loglevel = "info"
    accesslog = "-"  # STDOUT
    errorlog = "-"   # STDERR
    # timeout = 120 # If some Odoo calls are very long
    # keepalive = 5
    

### 3.35. `.env.example`
*   **Purpose**: Example environment variables.
*   **Content**:
    env
    ODOO_URL=http://localhost:8069
    ODOO_DB=your_odoo_db
    ODOO_USERNAME=admin
    ODOO_PASSWORD=your_odoo_password
    DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/creativeflow_db
    # STRIPE_API_KEY=sk_test_yourstripekey (Only if ENABLE_DIRECT_STRIPE_CALLS=true)
    # PAYPAL_CLIENT_ID=your_paypal_client_id (Only if ENABLE_DIRECT_PAYPAL_CALLS=true)
    # PAYPAL_CLIENT_SECRET=your_paypal_client_secret (Only if ENABLE_DIRECT_PAYPAL_CALLS=true)
    # INTERNAL_SERVICE_API_KEY=a_very_secret_internal_key (Optional, for service-to-service auth)
    LOG_LEVEL=INFO

    # Feature Toggles
    # ENABLE_DIRECT_STRIPE_CALLS=false
    # ENABLE_DIRECT_PAYPAL_CALLS=false
    # ENABLE_ODOO_RESPONSE_CACHING=false
    

## 4. Data Design

The primary data stores are:
1.  **Odoo ERP**: Source of truth for subscriptions, customer financial data, products (plans), invoices, credit balances, tax rules. This service interacts with Odoo via RPC.
2.  **CreativeFlow PostgreSQL DB (Main Application DB)**: This service will have *read-only* access to a projection of the `users` table to fetch context like `user_id`, `odoo_partner_id`, current `subscription_tier`, and current `credit_balance`. This local projection can serve as a cache to reduce direct Odoo calls for non-transactional checks, but Odoo remains authoritative for actual billing operations. Updates to these projected fields in the main DB would ideally be driven by events from Odoo or a periodic sync, managed by a separate process or this adapter if responsible for syncing.

Refer to `models_db.py` for the SQLAlchemy model projection. Domain models (`subscription_models.py`, `credit_models.py`) define Pydantic structures for internal service logic. API schemas (`schemas.py`) define the external contract.

## 5. Interface Design

### 5.1. Internal REST API (Exposed by this Service)

Base path: `/api/v1`

*   **Subscriptions:** (Managed under `/users/{user_id}/subscription`)
    *   `GET /`: Get current subscription status.
    *   `PUT /`: Update subscription (upgrade/downgrade).
    *   `DELETE /`: Cancel subscription.
    *   `GET /freemium-limits`: Get current freemium usage/limits.
*   **Credits:** (Managed under `/users/{user_id}/credits`)
    *   `GET /balance`: Get current credit balance.
    *   `POST /deduct`: Deduct credits for a specific action.
    *   `GET /cost?action_type=<type>`: Get credit cost for an action.
*   **Payments & Billing Utilities:** (Managed under `/users/{user_id}/payments`)
    *   `GET /manage-methods-url?provider=<stripe|paypal>`: Get URL to manage payment methods.
    *   `GET /invoices?limit=<N>`: List user invoices.
    *   `POST /tax-preview`: Get tax calculation preview for a purchase.

### 5.2. External Interfaces (Consumed by this Service)

*   **Odoo ERP API**:
    *   Protocol: JSON-RPC (preferred) or XML-RPC.
    *   Authentication: Username/password.
    *   Key Odoo Models for Interaction (examples, actual names depend on Odoo modules):
        *   `res.partner`: For customer data, credit balance, linking CF user to Odoo customer.
        *   `sale.subscription` (or `sale.order` if subscriptions are managed as recurring sales orders): For subscription lifecycle, plan details, start/end dates.
        *   `product.template` / `product.product`: For subscription plan definitions and pricing.
        *   `account.move`: For invoices.
        *   Custom Odoo models for credit ledger/transactions if implemented.
        *   Odoo's tax calculation engine.
*   **Stripe API (Conditional)**:
    *   Protocol: REST API via Stripe Python SDK.
    *   Authentication: API Key.
*   **PayPal API (Conditional)**:
    *   Protocol: REST API via PayPal Python SDK.
    *   Authentication: OAuth 2.0 Client ID & Secret.
*   **CreativeFlow PostgreSQL DB API**:
    *   Protocol: SQL via SQLAlchemy.
    *   Authentication: Database credentials.

## 6. Error Handling and Logging

*   **Error Handling**:
    *   FastAPI exception handlers will be used to catch common errors and return standardized JSON error responses.
    *   Custom exceptions (e.g., `OdooRPCError`, `InsufficientCreditsError`, `SubscriptionUpdateError`) will be defined in the domain layer and mapped to appropriate HTTP status codes in the API layer.
    *   Errors from Odoo RPC calls will be caught by the `OdooClient`, logged, and translated.
    *   Logic for retrying transient Odoo connection errors will be implemented in `OdooClient`.
*   **Logging**:
    *   Standard Python `logging` module, configured in `main.py` based on `LOG_LEVEL` from `config.py`.
    *   Logs will be structured (e.g., JSON) for easier parsing by a centralized logging system (e.g., ELK/Loki).
    *   Key information to log: request details, Odoo call parameters/responses (potentially summarized or with sensitive data redacted), errors with stack traces, credit deductions, subscription changes.
    *   Correlation IDs should be used if provided by upstream services or generated by this service to trace requests.

## 7. Security Considerations

*   **Odoo Credentials**: Stored securely in environment variables and accessed via Pydantic's `SecretStr`.
*   **Payment Gateway Credentials**: Handled similarly if direct interaction is enabled.
*   **Internal API Security**: If calls to this adapter service need protection, the `X-Internal-API-Key` mechanism in `core/security.py` can be used. This key should be strong and managed securely.
*   **Data Exposure**: The API only exposes necessary data. Sensitive payment details (full card numbers, etc.) are *never* handled or stored by this adapter; Odoo and the payment gateways are responsible.
*   **Dependency Vulnerabilities**: Regularly scan dependencies (`pyproject.toml`) for known vulnerabilities.
*   **Input Validation**: Pydantic models automatically validate API request data.

## 8. Deployment Considerations

*   **Containerization**: The service will be containerized using the provided `Dockerfile`.
*   **Configuration**: All configurations (Odoo URL, DB URL, API keys) will be managed via environment variables.
*   **Scalability**: The service is designed to be stateless (session management is external or handled by Odoo/calling service tokens), allowing for horizontal scaling.
*   **Health Checks**: A `/health` endpoint is provided for load balancers and orchestration platforms.

## 9. Future Considerations / Extensions
*   **Caching Odoo Responses**: For frequently requested, non-volatile data from Odoo (e.g., plan details), caching (e.g., using Redis) could be implemented via `OdooClient` or a caching layer in domain services, gated by `ENABLE_ODOO_RESPONSE_CACHING`.
*   **Webhook Handling**: If this service needs to directly receive webhooks from Stripe/PayPal (e.g., for payment confirmations not immediately reflected by Odoo), dedicated webhook endpoints would be added.
*   **More Granular User Context Caching**: If fetching user context from the main app DB becomes a bottleneck, a more robust caching strategy might be needed.