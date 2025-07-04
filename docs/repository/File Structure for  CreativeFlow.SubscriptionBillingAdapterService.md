# Specification

# 1. Files

- **Path:** src/creativeflow/services/subbilling/__init__.py  
**Description:** Initializes the subbilling service module.  
**Template:** Python Module Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'subbilling' directory a Python package.  
**Logic Description:** This file can be empty or can be used to make submodules available at the package level.  
**Documentation:**
    
    - **Summary:** Package initializer for the subbilling service.
    
**Namespace:** creativeflow.services.subbilling  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/subbilling/core/__init__.py  
**Description:** Initializes the core configuration and utilities module.  
**Template:** Python Module Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/core  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'core' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for core functionalities.
    
**Namespace:** creativeflow.services.subbilling.core  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/subbilling/core/config.py  
**Description:** Handles application configuration settings, including Odoo connection details, payment gateway keys (if used directly by adapter), and database connection strings for user context.  
**Template:** Python Configuration  
**Dependency Level:** 0  
**Name:** config  
**Type:** Configuration  
**Relative Path:** creativeflow/services/subbilling/core  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - ConfigurationProvider
    
**Members:**
    
    - **Name:** ODOO_URL  
**Type:** str  
**Attributes:** public|static  
    - **Name:** ODOO_DB  
**Type:** str  
**Attributes:** public|static  
    - **Name:** ODOO_USERNAME  
**Type:** str  
**Attributes:** public|static  
    - **Name:** ODOO_PASSWORD  
**Type:** str  
**Attributes:** public|static|secret  
    - **Name:** DATABASE_URL  
**Type:** str  
**Attributes:** public|static|secret  
**Notes:** For connecting to main app DB to read User context  
    - **Name:** STRIPE_API_KEY  
**Type:** str  
**Attributes:** public|static|secret  
**Notes:** If direct Stripe interaction is needed beyond Odoo orchestration  
    - **Name:** PAYPAL_CLIENT_ID  
**Type:** str  
**Attributes:** public|static|secret  
**Notes:** If direct PayPal interaction is needed  
    - **Name:** PAYPAL_CLIENT_SECRET  
**Type:** str  
**Attributes:** public|static|secret  
**Notes:** If direct PayPal interaction is needed  
    
**Methods:**
    
    - **Name:** load_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Configuration Management
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Provides centralized access to application settings loaded from environment variables or configuration files.  
**Logic Description:** Uses Pydantic's BaseSettings or a similar mechanism to load and validate configuration from environment variables. Defines settings for Odoo connection, database connection, and potentially payment gateway credentials if this adapter interacts directly (though Odoo is primary).  
**Documentation:**
    
    - **Summary:** Manages all external configurations for the service.
    
**Namespace:** creativeflow.services.subbilling.core.config  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/subbilling/core/security.py  
**Description:** Contains security-related utility functions, such as API key validation for internal service-to-service communication if needed.  
**Template:** Python Security Utilities  
**Dependency Level:** 1  
**Name:** security  
**Type:** Utility  
**Relative Path:** creativeflow/services/subbilling/core  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** verify_internal_api_key  
**Parameters:**
    
    - api_key: str
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Internal API Security
    
**Requirement Ids:**
    
    
**Purpose:** Provides helper functions for securing internal API endpoints if the API gateway doesn't handle all auth.  
**Logic Description:** Implements functions for tasks like validating an API key passed in a header for internal service communication. This might be a simple check or involve more complex token validation depending on the internal security model.  
**Documentation:**
    
    - **Summary:** Security utilities for the service, primarily for internal API authentication/authorization.
    
**Namespace:** creativeflow.services.subbilling.core.security  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/__init__.py  
**Description:** Initializes the infrastructure module containing clients for external services and database access.  
**Template:** Python Module Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/infrastructure  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'infrastructure' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for infrastructure components (external clients, DB).
    
**Namespace:** creativeflow.services.subbilling.infrastructure  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/odoo_client.py  
**Description:** Client for interacting with the Odoo ERP system using OdooRPC library. Handles connections and method calls to Odoo for subscription, billing, and credit management.  
**Template:** Python Odoo Client  
**Dependency Level:** 1  
**Name:** odoo_client  
**Type:** Client  
**Relative Path:** creativeflow/services/subbilling/infrastructure  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** odoo  
**Type:** odoorpc.ODOO  
**Attributes:** private  
    - **Name:** config  
**Type:** Settings  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - config: Settings
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** connect  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** get_subscription_details  
**Parameters:**
    
    - user_id: str
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** update_subscription  
**Parameters:**
    
    - user_id: str
    - plan_id: str
    - action: str
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** get_credit_balance  
**Parameters:**
    
    - user_id: str
    
**Return Type:** float  
**Attributes:** public  
    - **Name:** deduct_credits  
**Parameters:**
    
    - user_id: str
    - amount: float
    - reason: str
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** add_credits  
**Parameters:**
    
    - user_id: str
    - amount: float
    - reason: str
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** trigger_invoice_generation  
**Parameters:**
    
    - user_id: str
    - order_id: str
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** get_invoices  
**Parameters:**
    
    - user_id: str
    
**Return Type:** list  
**Attributes:** public  
    - **Name:** calculate_tax  
**Parameters:**
    
    - order_details: dict
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** handle_failed_payment  
**Parameters:**
    
    - payment_id: str
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Odoo Integration
    - Subscription Management via Odoo
    - Credit Management via Odoo
    - Billing Operations via Odoo
    
**Requirement Ids:**
    
    - INT-003
    - REQ-014
    - REQ-015
    - REQ-016
    
**Purpose:** Provides a dedicated interface for all communications with the Odoo ERP system.  
**Logic Description:** Uses the 'odoorpc' library to establish a connection to Odoo using credentials from config. Implements methods for specific Odoo models and methods related to sales, subscriptions, invoicing, and custom credit modules. Handles Odoo API exceptions and potentially retries. Maps parameters and results between the adapter's domain and Odoo's.  
**Documentation:**
    
    - **Summary:** Handles all RPC calls to the Odoo backend for subscription, billing, and credit operations.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.odoo_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/stripe_client.py  
**Description:** Client for interacting with the Stripe API. Used if the adapter needs to directly handle tokenization or specific Stripe interactions not fully managed by Odoo. Otherwise, this might be minimal.  
**Template:** Python Stripe Client  
**Dependency Level:** 1  
**Name:** stripe_client  
**Type:** Client  
**Relative Path:** creativeflow/services/subbilling/infrastructure  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** api_key  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - api_key: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** create_payment_intent  
**Parameters:**
    
    - amount: int
    - currency: str
    - customer_id: str
    - payment_method_id: str
    
**Return Type:** dict  
**Attributes:** public  
**Notes:** Example method, may not be needed if Odoo handles all.  
    - **Name:** update_payment_method_link  
**Parameters:**
    
    - user_id: str
    
**Return Type:** str  
**Attributes:** public  
**Notes:** Generates a link to Stripe's portal for updating payment methods.  
    
**Implemented Features:**
    
    - Stripe Integration (Conditional)
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Provides an interface for Stripe API calls, primarily for tasks Odoo might not directly expose or if frontend needs to interact with Stripe.js then pass tokens.  
**Logic Description:** Uses the official Stripe Python SDK. Initializes with API key from config. Implements methods for actions like creating payment intents, managing payment methods (if not done via Odoo directly), or handling webhooks if this service is the direct recipient. For an adapter role, direct interaction might be limited to tokenization or fetching setup intents.  
**Documentation:**
    
    - **Summary:** Manages communication with Stripe for payment processing, if direct interaction is required.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.stripe_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/paypal_client.py  
**Description:** Client for interacting with the PayPal API. Similar to Stripe client, used if direct interaction is necessary beyond Odoo's orchestration.  
**Template:** Python PayPal Client  
**Dependency Level:** 1  
**Name:** paypal_client  
**Type:** Client  
**Relative Path:** creativeflow/services/subbilling/infrastructure  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** client_id  
**Type:** str  
**Attributes:** private  
    - **Name:** client_secret  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - client_id: str
    - client_secret: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** create_payment  
**Parameters:**
    
    - order_details: dict
    
**Return Type:** dict  
**Attributes:** public  
**Notes:** Example method, may not be needed if Odoo handles all.  
    - **Name:** update_payment_method_link  
**Parameters:**
    
    - user_id: str
    
**Return Type:** str  
**Attributes:** public  
**Notes:** Generates a link to PayPal's portal for updating payment methods.  
    
**Implemented Features:**
    
    - PayPal Integration (Conditional)
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Provides an interface for PayPal API calls if the adapter needs to handle parts of the PayPal flow directly.  
**Logic Description:** Uses the official PayPal Python SDK. Initializes with client ID and secret. Implements methods for creating payments, managing subscriptions, or handling webhooks related to PayPal if not managed by Odoo. Adapter role suggests Odoo might handle most of this.  
**Documentation:**
    
    - **Summary:** Manages communication with PayPal, if direct interaction is required.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.paypal_client  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/db/__init__.py  
**Description:** Initializes the database interaction module.  
**Template:** Python Module Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/infrastructure/db  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'db' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for database interaction components.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.db  
**Metadata:**
    
    - **Category:** Infrastructure
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/db/database.py  
**Description:** Handles database connection and session management for PostgreSQL using SQLAlchemy.  
**Template:** Python SQLAlchemy Setup  
**Dependency Level:** 1  
**Name:** database  
**Type:** DatabaseSetup  
**Relative Path:** creativeflow/services/subbilling/infrastructure/db  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SQLALCHEMY_DATABASE_URL  
**Type:** str  
**Attributes:** private|static  
    - **Name:** engine  
**Type:** Engine  
**Attributes:** private|static  
    - **Name:** SessionLocal  
**Type:** sessionmaker  
**Attributes:** public|static  
    
**Methods:**
    
    - **Name:** get_db  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Database Connection Management
    
**Requirement Ids:**
    
    
**Purpose:** Establishes and manages connections to the PostgreSQL database used for reading user context or caching.  
**Logic Description:** Initializes SQLAlchemy engine and session factory based on DATABASE_URL from config. Provides a dependency (`get_db`) for FastAPI to inject database sessions into route handlers and services.  
**Documentation:**
    
    - **Summary:** Manages database connections and sessions for PostgreSQL interactions.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.db.database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/db/models_db.py  
**Description:** Defines SQLAlchemy ORM models, primarily a read-only projection of the main application's User table to fetch context like subscription_tier and credit_balance. May also include models for local caching if used.  
**Template:** Python SQLAlchemy Models  
**Dependency Level:** 0  
**Name:** models_db  
**Type:** Model  
**Relative Path:** creativeflow/services/subbilling/infrastructure/db  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** User  
**Type:** SQLAlchemyTable  
**Attributes:** public  
**Notes:** Represents a projection of the main User table, fields like id, email, subscription_tier, credit_balance.  
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Data Model (Read-Only Projection)
    
**Requirement Ids:**
    
    - REQ-014
    - REQ-015
    
**Purpose:** Defines data structures for interacting with the PostgreSQL database for user context.  
**Logic Description:** Contains SQLAlchemy model definitions. The `User` model will reflect relevant fields from the main application's user table needed by this adapter (e.g., `id`, `subscription_tier`, `credit_balance`). Other models might be for caching Odoo data if a DB cache is implemented.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM models for database entities, primarily for reading User context.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.db.models_db  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/db/repositories/__init__.py  
**Description:** Initializes the repositories module.  
**Template:** Python Module Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/infrastructure/db/repositories  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'repositories' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for data access repositories.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.db.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/services/subbilling/infrastructure/db/repositories/user_repository.py  
**Description:** Repository for accessing User data from the main application's PostgreSQL database. Provides methods to fetch user details like subscription tier and credit balance for context.  
**Template:** Python Repository  
**Dependency Level:** 2  
**Name:** user_repository  
**Type:** Repository  
**Relative Path:** creativeflow/services/subbilling/infrastructure/db/repositories  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** db  
**Type:** Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - db: Session
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_user_context_by_id  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** Optional[UserDBModel]  
**Attributes:** public  
    
**Implemented Features:**
    
    - User Data Access (Read-Only)
    
**Requirement Ids:**
    
    - REQ-014
    - REQ-015
    
**Purpose:** Handles read operations for User entity context from the main database.  
**Logic Description:** Implements methods to query the `User` table (projection) using SQLAlchemy. Primarily focused on fetching data needed for validation or enriching requests to Odoo, such as current subscription tier or credit balance.  
**Documentation:**
    
    - **Summary:** Provides data access methods for retrieving user context information from PostgreSQL.
    
**Namespace:** creativeflow.services.subbilling.infrastructure.db.repositories.user_repository  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/creativeflow/services/subbilling/domain/__init__.py  
**Description:** Initializes the domain logic module.  
**Template:** Python Module Init  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/domain  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'domain' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for domain logic and services.
    
**Namespace:** creativeflow.services.subbilling.domain  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/models/__init__.py  
**Description:** Initializes the domain models module.  
**Template:** Python Module Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/domain/models  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'models' directory under 'domain' a Python package.  
**Logic Description:** Empty or exports models for convenience.  
**Documentation:**
    
    - **Summary:** Package initializer for internal domain models.
    
**Namespace:** creativeflow.services.subbilling.domain.models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/models/subscription_models.py  
**Description:** Defines internal domain models (Pydantic or dataclasses) for subscription-related concepts used within the service logic, potentially distinct from API schemas for transformation purposes.  
**Template:** Python Pydantic Models  
**Dependency Level:** 1  
**Name:** subscription_models  
**Type:** Model  
**Relative Path:** creativeflow/services/subbilling/domain/models  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SubscriptionTierInfo  
**Type:** PydanticBaseModel  
**Attributes:** public  
**Notes:** Fields: id, name, features_summary  
    - **Name:** UserSubscriptionStatus  
**Type:** PydanticBaseModel  
**Attributes:** public  
**Notes:** Fields: user_id, plan_id, status, current_period_end, features  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Subscription Domain Models
    
**Requirement Ids:**
    
    - REQ-014
    - INT-003
    
**Purpose:** Internal data structures for handling subscription information within the business logic.  
**Logic Description:** Contains Pydantic models that represent subscription-related data as processed by the domain services. These models might be richer or structured differently than the API request/response schemas, especially if complex mapping to/from Odoo is involved.  
**Documentation:**
    
    - **Summary:** Internal domain models for subscription entities.
    
**Namespace:** creativeflow.services.subbilling.domain.models.subscription_models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/models/credit_models.py  
**Description:** Defines internal domain models (Pydantic or dataclasses) for credit-related concepts.  
**Template:** Python Pydantic Models  
**Dependency Level:** 1  
**Name:** credit_models  
**Type:** Model  
**Relative Path:** creativeflow/services/subbilling/domain/models  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** CreditBalance  
**Type:** PydanticBaseModel  
**Attributes:** public  
**Notes:** Fields: user_id, balance, last_updated  
    - **Name:** CreditDeductionRequest  
**Type:** PydanticBaseModel  
**Attributes:** public  
**Notes:** Fields: user_id, amount, reason, action_id  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Domain Models
    
**Requirement Ids:**
    
    - REQ-015
    - REQ-016
    
**Purpose:** Internal data structures for handling credit information.  
**Logic Description:** Contains Pydantic models for representing credit balance, deduction requests, and other credit-related operations internally.  
**Documentation:**
    
    - **Summary:** Internal domain models for credit management entities.
    
**Namespace:** creativeflow.services.subbilling.domain.models.credit_models  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/services/__init__.py  
**Description:** Initializes the domain services module.  
**Template:** Python Module Init  
**Dependency Level:** 3  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/domain/services  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'services' directory under 'domain' a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for business logic services.
    
**Namespace:** creativeflow.services.subbilling.domain.services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/services/subscription_service.py  
**Description:** Contains business logic for managing subscriptions, interacting with Odoo via OdooClient. Handles freemium model logic, upgrades, downgrades, cancellations, and tier feature enforcement.  
**Template:** Python Service  
**Dependency Level:** 3  
**Name:** subscription_service  
**Type:** Service  
**Relative Path:** creativeflow/services/subbilling/domain/services  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - ServiceLayerPattern
    
**Members:**
    
    - **Name:** odoo_client  
**Type:** OdooClient  
**Attributes:** private  
    - **Name:** user_repo  
**Type:** UserRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - odoo_client: OdooClient
    - user_repo: UserRepository
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_user_subscription_status  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** UserSubscriptionStatus  
**Attributes:** public  
    - **Name:** process_subscription_upgrade  
**Parameters:**
    
    - user_id: UUID
    - new_plan_id: str
    
**Return Type:** UserSubscriptionStatus  
**Attributes:** public  
    - **Name:** process_subscription_downgrade  
**Parameters:**
    
    - user_id: UUID
    - new_plan_id: str
    
**Return Type:** UserSubscriptionStatus  
**Attributes:** public  
    - **Name:** process_subscription_cancellation  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** UserSubscriptionStatus  
**Attributes:** public  
    - **Name:** get_freemium_limits  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** check_feature_access  
**Parameters:**
    
    - user_id: UUID
    - feature_key: str
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Subscription Lifecycle Management
    - Freemium Model Logic
    - Tier-based Feature Access Control
    
**Requirement Ids:**
    
    - REQ-014
    - INT-003
    
**Purpose:** Encapsulates all business logic related to user subscriptions and plan management.  
**Logic Description:** Interacts with OdooClient to reflect subscription changes in Odoo. Fetches current user tier from UserRepository for quick checks or uses Odoo as single source of truth. Implements logic to determine feature availability based on subscription tier (e.g., Pro+ features, free tier limits as per REQ-014). Manages the flow for upgrades, downgrades, and cancellations.  
**Documentation:**
    
    - **Summary:** Service layer for handling subscription management logic.
    
**Namespace:** creativeflow.services.subbilling.domain.services.subscription_service  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/services/credit_service.py  
**Description:** Manages user credit balances, deductions, and overage protection, coordinating with Odoo for actual credit state.  
**Template:** Python Service  
**Dependency Level:** 3  
**Name:** credit_service  
**Type:** Service  
**Relative Path:** creativeflow/services/subbilling/domain/services  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - ServiceLayerPattern
    
**Members:**
    
    - **Name:** odoo_client  
**Type:** OdooClient  
**Attributes:** private  
    - **Name:** user_repo  
**Type:** UserRepository  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - odoo_client: OdooClient
    - user_repo: UserRepository
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_user_credit_balance  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** CreditBalance  
**Attributes:** public  
    - **Name:** deduct_credits_for_action  
**Parameters:**
    
    - user_id: UUID
    - action_type: str
    - reference_id: Optional[UUID]
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** get_credit_cost  
**Parameters:**
    
    - action_type: str
    
**Return Type:** float  
**Attributes:** public  
    - **Name:** check_sufficient_credits  
**Parameters:**
    
    - user_id: UUID
    - action_type: str
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** handle_credit_overage  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** refund_credits_for_failed_action  
**Parameters:**
    
    - user_id: UUID
    - amount: float
    - original_action_id: UUID
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Credit Balance Management
    - Credit Deduction Logic
    - Overage Protection
    - Flexible Credit Allocation
    - Usage Analytics Data Points
    
**Requirement Ids:**
    
    - REQ-015
    - REQ-016
    
**Purpose:** Encapsulates business logic for user credit management.  
**Logic Description:** Determines credit cost for various actions based on REQ-016. Interacts with OdooClient to deduct/refund credits. Reads current credit balance (potentially cached via UserRepository or direct from Odoo) to check for sufficiency. Implements overage protection logic (REQ-015), prompting for upgrades if credits are insufficient.  
**Documentation:**
    
    - **Summary:** Service layer for managing user credits and related operations.
    
**Namespace:** creativeflow.services.subbilling.domain.services.credit_service  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/services/payment_orchestration_service.py  
**Description:** Orchestrates payment-related operations by interacting with Odoo, which in turn interacts with Stripe/PayPal. Handles invoice generation triggers and tax calculation requests via Odoo.  
**Template:** Python Service  
**Dependency Level:** 3  
**Name:** payment_orchestration_service  
**Type:** Service  
**Relative Path:** creativeflow/services/subbilling/domain/services  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - ServiceLayerPattern
    
**Members:**
    
    - **Name:** odoo_client  
**Type:** OdooClient  
**Attributes:** private  
    - **Name:** stripe_client  
**Type:** Optional[StripeClient]  
**Attributes:** private  
    - **Name:** paypal_client  
**Type:** Optional[PayPalClient]  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - odoo_client: OdooClient
    - stripe_client: Optional[StripeClient]
    - paypal_client: Optional[PayPalClient]
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_user_invoices_link  
**Parameters:**
    
    - user_id: UUID
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** process_payment_method_update_request  
**Parameters:**
    
    - user_id: UUID
    - provider: str
    
**Return Type:** str  
**Attributes:** public  
**Notes:** Returns a URL to the provider's portal if Odoo doesn't manage this directly.  
    - **Name:** handle_payment_success_webhook  
**Parameters:**
    
    - provider: str
    - payload: dict
    
**Return Type:** void  
**Attributes:** public  
**Notes:** If this service directly receives webhooks, otherwise Odoo handles.  
    - **Name:** handle_failed_payment_scenario  
**Parameters:**
    
    - user_id: UUID
    - payment_attempt_id: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_tax_information_for_purchase  
**Parameters:**
    
    - user_id: UUID
    - purchase_details: dict
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Payment Processing Orchestration (via Odoo)
    - Invoice Generation Trigger (via Odoo)
    - Tax Calculation (via Odoo)
    - Failed Payment Handling (via Odoo)
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Manages the overall flow of payment, invoicing, and tax operations, primarily by delegating to Odoo.  
**Logic Description:** This service acts as a high-level orchestrator. For payment processing, it would typically tell Odoo to initiate a payment for a subscription or credit purchase. Odoo then handles the interaction with Stripe/PayPal. This service might provide links for users to update payment methods (which could be links to Odoo's portal or directly to Stripe/PayPal portals). It triggers invoice generation and requests tax calculations through the OdooClient.  
**Documentation:**
    
    - **Summary:** Orchestrates payment, invoice, and tax related processes, primarily through Odoo.
    
**Namespace:** creativeflow.services.subbilling.domain.services.payment_orchestration_service  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/domain/services/odoo_mapping_service.py  
**Description:** Provides utility functions for mapping data structures between the adapter's internal domain/API models and Odoo's expected data formats.  
**Template:** Python Utility Service  
**Dependency Level:** 2  
**Name:** odoo_mapping_service  
**Type:** Service  
**Relative Path:** creativeflow/services/subbilling/domain/services  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - DataMapper
    
**Members:**
    
    
**Methods:**
    
    - **Name:** to_odoo_subscription_data  
**Parameters:**
    
    - subscription_request: SubscriptionUpdateRequestSchema
    
**Return Type:** dict  
**Attributes:** public|static  
    - **Name:** from_odoo_subscription_data  
**Parameters:**
    
    - odoo_data: dict
    
**Return Type:** UserSubscriptionStatus  
**Attributes:** public|static  
    - **Name:** to_odoo_credit_deduction_data  
**Parameters:**
    
    - credit_request: CreditDeductionRequest
    
**Return Type:** dict  
**Attributes:** public|static  
    - **Name:** from_odoo_credit_balance_data  
**Parameters:**
    
    - odoo_data: dict
    
**Return Type:** CreditBalance  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Data Mapping for Odoo Integration
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Centralizes data transformation logic required for Odoo communication.  
**Logic Description:** Contains static methods or a class with methods that take platform-specific request objects (e.g., Pydantic models from API or domain) and transform them into the dictionary/list structures expected by Odoo RPC calls. Also handles the reverse: transforming Odoo RPC responses into the adapter's Pydantic or domain models.  
**Documentation:**
    
    - **Summary:** Responsible for translating data formats between this service and Odoo.
    
**Namespace:** creativeflow.services.subbilling.domain.services.odoo_mapping_service  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** src/creativeflow/services/subbilling/api/__init__.py  
**Description:** Initializes the API module.  
**Template:** Python Module Init  
**Dependency Level:** 4  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/api  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'api' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for API related modules.
    
**Namespace:** creativeflow.services.subbilling.api  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/__init__.py  
**Description:** Initializes the v1 API module.  
**Template:** Python Module Init  
**Dependency Level:** 5  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/api/v1  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'v1' API directory a Python package.  
**Logic Description:** This file can be empty or can import routers.  
**Documentation:**
    
    - **Summary:** Package initializer for version 1 of the API.
    
**Namespace:** creativeflow.services.subbilling.api.v1  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/schemas.py  
**Description:** Defines Pydantic models for API request and response validation and serialization. These schemas define the contract for the service's API.  
**Template:** Python Pydantic Schemas  
**Dependency Level:** 1  
**Name:** schemas  
**Type:** Schema  
**Relative Path:** creativeflow/services/subbilling/api/v1  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - DataTransferObject
    
**Members:**
    
    - **Name:** SubscriptionUpdateRequest  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Fields for new_plan_id, etc.  
    - **Name:** SubscriptionResponse  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Fields for current_plan, status, period_end.  
    - **Name:** CreditBalanceResponse  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Fields for balance, currency.  
    - **Name:** CreditDeductRequest  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Fields for action_type, reference_id.  
    - **Name:** CreditDeductResponse  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Fields for success, new_balance.  
    - **Name:** InvoiceLinkResponse  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Field for invoice_portal_url.  
    - **Name:** PaymentMethodUpdateLinkResponse  
**Type:** BaseModel  
**Attributes:** public  
**Notes:** Field for update_url.  
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Data Contracts
    
**Requirement Ids:**
    
    - REQ-014
    - REQ-015
    - REQ-016
    - INT-003
    
**Purpose:** Defines the data structures used for API communication.  
**Logic Description:** Contains Pydantic models for all request bodies and response payloads. These are used by FastAPI for automatic data validation, serialization, and OpenAPI documentation generation.  
**Documentation:**
    
    - **Summary:** Pydantic schemas for API request and response models.
    
**Namespace:** creativeflow.services.subbilling.api.v1.schemas  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/endpoints/__init__.py  
**Description:** Initializes the API endpoints module.  
**Template:** Python Module Init  
**Dependency Level:** 6  
**Name:** __init__  
**Type:** ModuleInit  
**Relative Path:** creativeflow/services/subbilling/api/v1/endpoints  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'endpoints' directory a Python package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Package initializer for API endpoint modules.
    
**Namespace:** creativeflow.services.subbilling.api.v1.endpoints  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/endpoints/subscriptions.py  
**Description:** FastAPI router for subscription-related endpoints. Handles requests for managing user subscriptions and retrieving subscription details.  
**Template:** Python FastAPI Router  
**Dependency Level:** 5  
**Name:** subscriptions_api  
**Type:** Controller  
**Relative Path:** creativeflow/services/subbilling/api/v1/endpoints  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - MVCPattern
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_subscription_status_for_user  
**Parameters:**
    
    - user_id: UUID
    - sub_service: SubscriptionService = Depends(get_subscription_service)
    
**Return Type:** schemas.SubscriptionResponse  
**Attributes:** public|async  
    - **Name:** update_user_subscription  
**Parameters:**
    
    - user_id: UUID
    - request: schemas.SubscriptionUpdateRequest
    - sub_service: SubscriptionService = Depends(get_subscription_service)
    
**Return Type:** schemas.SubscriptionResponse  
**Attributes:** public|async  
    - **Name:** cancel_user_subscription  
**Parameters:**
    
    - user_id: UUID
    - sub_service: SubscriptionService = Depends(get_subscription_service)
    
**Return Type:** schemas.SubscriptionResponse  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Subscription Management API
    - Freemium Model Info API
    
**Requirement Ids:**
    
    - REQ-014
    - INT-003
    
**Purpose:** Exposes HTTP endpoints for managing and querying user subscriptions.  
**Logic Description:** Defines FastAPI routes for subscription operations. Uses dependency injection to get instances of `SubscriptionService`. Validates requests using Pydantic schemas and formats responses. Calls the appropriate service methods to handle the business logic.  
**Documentation:**
    
    - **Summary:** API endpoints for managing user subscriptions.
    
**Namespace:** creativeflow.services.subbilling.api.v1.endpoints.subscriptions  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/endpoints/credits.py  
**Description:** FastAPI router for credit-related endpoints. Handles requests for credit balance inquiries, deductions, and information about credit costs and usage.  
**Template:** Python FastAPI Router  
**Dependency Level:** 5  
**Name:** credits_api  
**Type:** Controller  
**Relative Path:** creativeflow/services/subbilling/api/v1/endpoints  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - MVCPattern
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_credit_balance_for_user  
**Parameters:**
    
    - user_id: UUID
    - credit_service: CreditService = Depends(get_credit_service)
    
**Return Type:** schemas.CreditBalanceResponse  
**Attributes:** public|async  
    - **Name:** deduct_credits_for_action  
**Parameters:**
    
    - user_id: UUID
    - request: schemas.CreditDeductRequest
    - credit_service: CreditService = Depends(get_credit_service)
    
**Return Type:** schemas.CreditDeductResponse  
**Attributes:** public|async  
    - **Name:** get_action_credit_cost  
**Parameters:**
    
    - action_type: str
    - credit_service: CreditService = Depends(get_credit_service)
    
**Return Type:** float  
**Attributes:** public|async  
    - **Name:** handle_insufficient_credits  
**Parameters:**
    
    - user_id: UUID
    - credit_service: CreditService = Depends(get_credit_service)
    
**Return Type:** dict  
**Attributes:** public|async  
**Notes:** Endpoint for frontend to call to get upgrade prompts etc.  
    
**Implemented Features:**
    
    - Credit Balance API
    - Credit Deduction API
    - Overage Protection Prompts API
    
**Requirement Ids:**
    
    - REQ-015
    - REQ-016
    
**Purpose:** Exposes HTTP endpoints for managing and querying user credit information.  
**Logic Description:** Defines FastAPI routes for credit operations. Uses dependency injection for `CreditService`. Validates requests and formats responses with Pydantic schemas. Calls service methods for credit-related business logic.  
**Documentation:**
    
    - **Summary:** API endpoints for managing user credits.
    
**Namespace:** creativeflow.services.subbilling.api.v1.endpoints.credits  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/api/v1/endpoints/payments.py  
**Description:** FastAPI router for payment-related utility endpoints. Handles requests for links to manage payment methods, view invoices, or get tax information (all orchestrated via Odoo).  
**Template:** Python FastAPI Router  
**Dependency Level:** 5  
**Name:** payments_api  
**Type:** Controller  
**Relative Path:** creativeflow/services/subbilling/api/v1/endpoints  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - MVCPattern
    
**Members:**
    
    - **Name:** router  
**Type:** APIRouter  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** get_payment_method_update_url  
**Parameters:**
    
    - user_id: UUID
    - provider: str
    - payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
    
**Return Type:** schemas.PaymentMethodUpdateLinkResponse  
**Attributes:** public|async  
    - **Name:** get_user_invoices_url  
**Parameters:**
    
    - user_id: UUID
    - payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
    
**Return Type:** schemas.InvoiceLinkResponse  
**Attributes:** public|async  
    - **Name:** get_tax_info_for_purchase_preview  
**Parameters:**
    
    - user_id: UUID
    - purchase_details: dict
    - payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
    
**Return Type:** dict  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Payment Method Management Links API
    - Invoice Access Links API
    - Tax Information API
    
**Requirement Ids:**
    
    - INT-003
    
**Purpose:** Exposes utility HTTP endpoints related to payment management, invoice access, and tax information, mostly by providing links or data retrieved via Odoo.  
**Logic Description:** Defines FastAPI routes for payment utility operations. Uses dependency injection for `PaymentOrchestrationService`. These endpoints typically don't process payments directly but interact with the service layer to get URLs (e.g., to Stripe/PayPal/Odoo portals) or pre-calculated tax information from Odoo.  
**Documentation:**
    
    - **Summary:** API endpoints for payment-related utilities like managing payment methods and accessing invoices.
    
**Namespace:** creativeflow.services.subbilling.api.v1.endpoints.payments  
**Metadata:**
    
    - **Category:** API
    
- **Path:** src/creativeflow/services/subbilling/dependencies.py  
**Description:** Defines FastAPI dependency injectors for services, repositories, and clients.  
**Template:** Python FastAPI Dependencies  
**Dependency Level:** 4  
**Name:** dependencies  
**Type:** DependencyInjection  
**Relative Path:** creativeflow/services/subbilling  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    - DependencyInjection
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_settings  
**Parameters:**
    
    
**Return Type:** Settings  
**Attributes:** public  
    - **Name:** get_db_session  
**Parameters:**
    
    
**Return Type:** Generator[Session, None, None]  
**Attributes:** public  
    - **Name:** get_odoo_client  
**Parameters:**
    
    - settings: Settings = Depends(get_settings)
    
**Return Type:** OdooClient  
**Attributes:** public  
    - **Name:** get_stripe_client  
**Parameters:**
    
    - settings: Settings = Depends(get_settings)
    
**Return Type:** Optional[StripeClient]  
**Attributes:** public  
    - **Name:** get_paypal_client  
**Parameters:**
    
    - settings: Settings = Depends(get_settings)
    
**Return Type:** Optional[PayPalClient]  
**Attributes:** public  
    - **Name:** get_user_repository  
**Parameters:**
    
    - db: Session = Depends(get_db_session)
    
**Return Type:** UserRepository  
**Attributes:** public  
    - **Name:** get_subscription_service  
**Parameters:**
    
    - odoo_client: OdooClient = Depends(get_odoo_client)
    - user_repo: UserRepository = Depends(get_user_repository)
    
**Return Type:** SubscriptionService  
**Attributes:** public  
    - **Name:** get_credit_service  
**Parameters:**
    
    - odoo_client: OdooClient = Depends(get_odoo_client)
    - user_repo: UserRepository = Depends(get_user_repository)
    
**Return Type:** CreditService  
**Attributes:** public  
    - **Name:** get_payment_orchestration_service  
**Parameters:**
    
    - odoo_client: OdooClient = Depends(get_odoo_client)
    - stripe_client: Optional[StripeClient] = Depends(get_stripe_client)
    - paypal_client: Optional[PayPalClient] = Depends(get_paypal_client)
    
**Return Type:** PaymentOrchestrationService  
**Attributes:** public  
    
**Implemented Features:**
    
    - Dependency Injection Setup
    
**Requirement Ids:**
    
    
**Purpose:** Manages instantiation and provision of dependencies for FastAPI route handlers.  
**Logic Description:** Contains functions that FastAPI uses to inject dependencies like database sessions, Odoo client instances, and service instances into endpoint functions. This promotes loose coupling and testability.  
**Documentation:**
    
    - **Summary:** Provides dependency injectors for various service components.
    
**Namespace:** creativeflow.services.subbilling.dependencies  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** src/creativeflow/services/subbilling/main.py  
**Description:** Main application file for the FastAPI service. Initializes the FastAPI app, includes routers, and sets up middleware.  
**Template:** Python FastAPI Main  
**Dependency Level:** 6  
**Name:** main  
**Type:** Application  
**Relative Path:** creativeflow/services/subbilling  
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** app  
**Type:** FastAPI  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Entry Point
    - API Routing
    
**Requirement Ids:**
    
    - REQ-014
    - REQ-015
    - REQ-016
    - INT-003
    
**Purpose:** The entry point for the Subscription & Billing Adapter microservice.  
**Logic Description:** Creates the FastAPI application instance. Includes API routers from the `api.v1.endpoints` modules. May configure CORS middleware, exception handlers, and other application-level settings. Defines startup and shutdown events if necessary (e.g., to initialize Odoo client connection pool).  
**Documentation:**
    
    - **Summary:** Initializes and configures the FastAPI application for the subscription and billing adapter service.
    
**Namespace:** creativeflow.services.subbilling.main  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** pyproject.toml  
**Description:** Python project configuration file using Poetry (or similar like setup.py/setup.cfg if not using Poetry). Defines project metadata, dependencies, and build settings.  
**Template:** Python Project Config  
**Dependency Level:** 0  
**Name:** pyproject  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    - Project Build Configuration
    
**Requirement Ids:**
    
    
**Purpose:** Manages project dependencies and packaging information.  
**Logic Description:** Specifies Python version, project name, version, author, and lists all runtime dependencies (e.g., fastapi, uvicorn, pydantic, odoorpc, stripe, paypalrestsdk, sqlalchemy, psycopg2-binary) and development dependencies (e.g., pytest, black, ruff).  
**Documentation:**
    
    - **Summary:** Configuration file for Python project dependencies and packaging using Poetry.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** requirements.txt  
**Description:** Alternative or supplementary file for listing Python dependencies, typically used if not using Poetry or for specific deployment scenarios.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Listing
    
**Requirement Ids:**
    
    
**Purpose:** Lists project dependencies for pip.  
**Logic Description:** A plain text file listing all required Python packages with their versions. Can be generated from pyproject.toml (Poetry) or maintained manually.  
**Documentation:**
    
    - **Summary:** Standard pip requirements file listing project dependencies.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** Dockerfile  
**Description:** Dockerfile for building the container image for the Subscription & Billing Adapter service.  
**Template:** Docker Build File  
**Dependency Level:** 0  
**Name:** Dockerfile  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization
    
**Requirement Ids:**
    
    
**Purpose:** Defines the steps to build a Docker image for the service.  
**Logic Description:** Specifies the base Python image, copies application code, installs dependencies from requirements.txt or pyproject.toml, sets environment variables, exposes the service port (e.g., 8000), and defines the command to run the FastAPI application using Uvicorn.  
**Documentation:**
    
    - **Summary:** Instructions for building a Docker container image for the service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    
- **Path:** .env.example  
**Description:** Example environment file showing required environment variables for local development and configuration.  
**Template:** Environment Variables Example  
**Dependency Level:** 0  
**Name:** .env.example  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-SUBBILLING-ADAPTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Example
    
**Requirement Ids:**
    
    
**Purpose:** Provides a template for developers to set up their local .env file.  
**Logic Description:** Lists all environment variables used by `core/config.py` with placeholder or example values (e.g., ODOO_URL=http://localhost:8069, DATABASE_URL=postgresql://user:pass@host:port/db). Sensitive actual values should not be committed.  
**Documentation:**
    
    - **Summary:** Example file illustrating the required environment variables for the service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - ENABLE_DIRECT_STRIPE_CALLS
  - ENABLE_DIRECT_PAYPAL_CALLS
  - ENABLE_ODOO_RESPONSE_CACHING
  
- **Database Configs:**
  
  - ODOO_URL
  - ODOO_DB
  - ODOO_USERNAME
  - ODOO_PASSWORD
  - DATABASE_URL (for user context/cache)
  - STRIPE_API_KEY
  - PAYPAL_CLIENT_ID
  - PAYPAL_CLIENT_SECRET
  


---

