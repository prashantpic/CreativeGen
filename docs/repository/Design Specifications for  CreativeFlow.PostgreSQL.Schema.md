# Software Design Specification: CreativeFlow.PostgreSQL.Schema

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.PostgreSQL.Schema` repository. Its primary purpose is to define the complete database schema for the CreativeFlow AI platform's PostgreSQL 16+ database, including all table structures, data types, constraints, relationships, and indexes. It also outlines the strategy for managing database schema evolution using Alembic and SQLAlchemy. This specification will guide the creation and maintenance of the database DDL and migration scripts.

### 1.2 Scope
This SDS covers:
*   The logical and physical design of the PostgreSQL database schema.
*   Detailed specifications for all tables, columns, data types, primary keys, foreign keys, unique constraints, check constraints, and default values.
*   Indexing strategies for performance optimization.
*   The setup and configuration of Alembic for managing database migrations.
*   The structure of SQLAlchemy ORM models that represent the database tables and are used by Alembic for autogeneration and migration tasks.
*   The organization of DDL scripts for reference.

Actual data access logic, business logic, and application-level security measures (like encryption/hashing of specific fields) are outside the scope of this repository but are considered in the schema design to accommodate them.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **DDL**: Data Definition Language
*   **ORM**: Object-Relational Mapper
*   **PK**: Primary Key
*   **FK**: Foreign Key
*   **ERD**: Entity-Relationship Diagram
*   **SDS**: Software Design Specification
*   **SRS**: Software Requirements Specification
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **PWA**: Progressive Web Application
*   **GDPR**: General Data Protection Regulation
*   **CCPA**: California Consumer Privacy Act
*   **PII**: Personally Identifiable Information
*   **JSONB**: JSON Binary (PostgreSQL data type)
*   **UUID**: Universally Unique Identifier
*   **RPO**: Recovery Point Objective
*   **RTO**: Recovery Time Objective
*   **NFR**: Non-Functional Requirement
*   **KMS**: Key Management Service

## 2. System Overview
The `CreativeFlow.PostgreSQL.Schema` repository is a foundational component of the CreativeFlow AI platform. It provides the persistent storage layer for all structured application data. This includes user account information, creative project data, AI generation requests and results, subscription details, usage logs, and more. The schema is designed to support all functional and non-functional requirements of the platform, ensuring data integrity, consistency, scalability, and enabling efficient data retrieval and manipulation by various backend services, including the Odoo ERP system.

## 3. Design Goals
*   **Data Integrity**: Ensure accuracy and consistency of data through appropriate constraints (PK, FK, UNIQUE, NOT NULL, CHECK).
*   **Consistency**: Provide a single source of truth for structured data, reflected accurately across the application.
*   **Support Application Features**: Design the schema to efficiently support all features outlined in the SRS (Section 7 and related requirements).
*   **Scalability**: Design for potential growth in data volume and user load, supporting mechanisms like read replicas and future sharding considerations (NFR-005).
*   **Maintainability**: Create a well-documented and logically structured schema that is easy to understand, modify, and evolve over time using automated migration tools.
*   **Performance**: Optimize for common query patterns through appropriate indexing and data type selection.
*   **Security**: Accommodate storage of sensitive data by design, enabling application-level security measures (e.g., fields for hashed passwords, encrypted tokens).
*   **Compliance**: Support data retention policies and GDPR/CCPA requirements (e.g., soft deletes, clear PII distinction).

## 4. Architectural Design

### 4.1 Technology Stack
*   **Database**: PostgreSQL 16.3 (or latest stable at development start)
*   **Migration Tool**: Alembic 1.13.1
*   **ORM (for Alembic integration)**: SQLAlchemy (version compatible with Alembic and Python 3.11)
*   **Migration Scripting Language**: Python 3.11.9
*   **DDL Language**: SQL (PostgreSQL dialect)

### 4.2 Directory Structure (as per `file_structure_json`)
The repository is structured to separate Alembic configuration, migration scripts, SQLAlchemy models, and raw DDL scripts:
*   `alembic.ini`: Alembic configuration file.
*   `env.py`: Alembic environment setup script.
*   `script.py.mako`: Template for new migration scripts.
*   `app/`: Contains Python code for models.
    *   `app/db/base.py`: SQLAlchemy declarative base.
    *   `app/models/`: Directory for SQLAlchemy ORM model definitions (e.g., `user_model.py`, `project_model.py`).
        *   `app/models/__init__.py`: Imports all models for Alembic discoverability.
*   `versions/`: Directory containing Alembic migration scripts (e.g., `0001_create_initial_tables.py`).
*   `ddl/tables/`: Directory for raw SQL DDL scripts (e.g., `001_create_users.sql`), primarily for reference.
*   `docs/diagrams/`: Directory for database diagrams (e.g., ERDs).

### 4.3 Migration Strategy
Database schema evolution will be managed using Alembic.
*   **Model-Driven Migrations**: SQLAlchemy ORM models defined in `app/models/` will serve as the "source of truth" for the desired schema state.
*   **Autogeneration**: Alembic's `revision -autogenerate` command will be used to detect changes between the current database schema and the `target_metadata` (derived from SQLAlchemy models) and generate draft migration scripts.
*   **Manual Review and Customization**: Autogenerated scripts will be reviewed and potentially customized by developers to ensure correctness, handle complex data migrations, and add any necessary raw SQL operations not easily expressed via SQLAlchemy schema changes.
*   **Versioned Scripts**: Each migration script in the `versions/` directory represents an atomic, versioned change to the database schema. Scripts will have `upgrade()` and `downgrade()` functions.
*   **CI/CD Integration**: Database migrations will be applied automatically as part of the deployment pipeline (DEP-003, REQ-DA-014, PMDT-005), ensuring consistency across environments.
*   **Idempotency**: Migration scripts should be written to be idempotent where possible.

### 4.4 Data Modeling Approach
*   **Relational Model**: A relational database model will be used, leveraging PostgreSQL's features.
*   **Normalization**: The schema will generally follow database normalization principles (e.g., 3NF) to reduce data redundancy and improve data integrity, with strategic denormalization where beneficial for performance (e.g., denormalizing `userId` in `Project` table from `Workbench`).
*   **SQLAlchemy ORM**: SQLAlchemy models will be used to define tables, columns, data types, relationships, and constraints programmatically in Python. These models are primarily for Alembic's schema management and may also be used by Python-based services interacting with the database if they choose to use SQLAlchemy.
*   **UUIDs for Primary Keys**: Most primary keys will be UUIDs to ensure global uniqueness, beneficial for distributed systems and data replication. `UsageLog` uses `BIGSERIAL` for high-volume append-only logging.
*   **JSONB for Flexible Data**: PostgreSQL's `JSONB` data type will be used for storing semi-structured or flexible data like brand kit colors/fonts, style preferences, input parameters for AI generation, asset metadata, and API client permissions.
*   **Timestamps**: Standard `createdAt` and `updatedAt` timestamp columns will be included in most tables for auditing and tracking changes. `deletedAt` will be used for soft deletes to support data recovery and GDPR/CCPA compliance.

## 5. Detailed Schema Design
This section details the design for each table based on the `databaseDesign` input and corresponding requirements from the SRS.

### 5.1 `User` Table (users)
*   **Purpose**: Represents a registered user account, storing authentication details, profile information, preferences, and links to user-specific data. (SRS 7.1.1)
*   **SQLAlchemy Model**: `app/models/user_model.py` (`User` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `email` (VARCHAR(255), UNIQUE, NOT NULL, INDEXED)
    *   `passwordHash` (VARCHAR(255), NULLABLE) - Hashed at application layer.
    *   `socialProvider` (VARCHAR(50), NULLABLE, CHECK IN ('google', 'facebook', 'apple'))
    *   `socialProviderId` (VARCHAR(255), NULLABLE) - Unique with `socialProvider` when not NULL.
    *   `isEmailVerified` (BOOLEAN, NOT NULL, DEFAULT false)
    *   `emailVerificationToken` (VARCHAR(255), NULLABLE)
    *   `passwordResetToken` (VARCHAR(255), NULLABLE)
    *   `passwordResetExpires` (DateTime, NULLABLE)
    *   `fullName` (VARCHAR(100), NULLABLE)
    *   `username` (VARCHAR(50), UNIQUE, NULLABLE, INDEXED if NOT NULL)
    *   `profilePictureUrl` (VARCHAR(1024), NULLABLE)
    *   `languagePreference` (VARCHAR(10), NOT NULL, DEFAULT 'en-US', INDEXED)
    *   `timezone` (VARCHAR(50), NOT NULL, DEFAULT 'UTC')
    *   `mfaEnabled` (BOOLEAN, NOT NULL, DEFAULT false)
    *   `mfaSecret` (VARCHAR(255), NULLABLE) - Encrypted at application layer.
    *   `subscriptionTier` (VARCHAR(20), NOT NULL, DEFAULT 'Free', CHECK IN ('Free','Pro','Team','Enterprise'), INDEXED)
    *   `creditBalance` (DECIMAL(10, 2), NOT NULL, DEFAULT 0.00)
    *   `lastLoginAt` (DateTime, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
    *   `deletedAt` (DateTime, NULLABLE, INDEXED if NOT NULL)
*   **Relationships**:
    *   One-to-Many with `BrandKit` (`brand_kits` backref)
    *   One-to-Many with `Workbench` (`workbenches` backref)
    *   One-to-Many with `Project` (`projects` backref, direct for ownership, also via Workbench)
    *   One-to-Many with `Asset` (`assets` backref)
    *   One-to-Many with `GenerationRequest` (`generation_requests` backref)
    *   One-to-Many with `SocialMediaConnection` (`social_media_connections` backref)
    *   One-to-Many with `APIClient` (`api_clients` backref)
    *   One-to-One with `Subscription` (`subscription` backref)
    *   One-to-Many with `CreditTransaction` (`credit_transactions` backref)
    *   One-to-Many with `UsageLog` (`usage_logs` backref)
    *   One-to-Many with `Team` (as owner, `owned_teams` backref)
    *   Many-to-Many with `Team` via `TeamMember` (`team_memberships` backref)
    *   One-to-Many with `Session` (`sessions` backref)
    *   One-to-Many with `Notification` (`notifications` backref)
    *   One-to-Many with `Template` (as creator, `created_templates` backref)
    *   One-to-Many with `AIModelFeedback` (`ai_model_feedbacks` backref)
*   **Indexes**:
    *   `idx_user_email_unique` ON `users` (`email`)
    *   `idx_user_username_unique` ON `users` (`username`) WHERE `username` IS NOT NULL
    *   `idx_user_social_unique` ON `users` (`socialProvider`, `socialProviderId`) WHERE `socialProvider` IS NOT NULL AND `socialProviderId` IS NOT NULL
    *   `idx_user_subscriptiontier` ON `users` (`subscriptionTier`)
    *   `idx_user_deletedat` ON `users` (`deletedAt`) WHERE `deletedAt` IS NOT NULL
    *   `idx_user_languagepreference` ON `users` (`languagePreference`)

### 5.2 `BrandKit` Table (brand_kits)
*   **Purpose**: Stores brand assets (colors, fonts, logos) and preferences for users or teams. (SRS 7.1.2, UAPM-1-004)
*   **SQLAlchemy Model**: `app/models/brand_kit_model.py` (`BrandKit` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `teamId` (UUID, FK to `teams.id`, NULLABLE, INDEXED)
    *   `name` (VARCHAR(100), NOT NULL)
    *   `colors` (JSONB, NOT NULL) - Example: `[{"name": "Primary", "hex": "#FF0000"}]`
    *   `fonts` (JSONB, NOT NULL) - Example: `[{"name": "Heading", "family": "Arial", "url": "minio_path_or_external_url"}]`
    *   `logos` (JSONB, NULLABLE) - Example: `[{"name": "Main Logo", "path": "minio_path", "format": "png"}]`
    *   `stylePreferences` (JSONB, NULLABLE)
    *   `isDefault` (BOOLEAN, NOT NULL, DEFAULT false)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `Team` (`team` backref)
    *   One-to-Many with `Workbench` (as default brand kit)
    *   One-to-Many with `Project` (as override brand kit)
*   **Indexes**:
    *   `idx_brandkit_userid` ON `brand_kits` (`userId`)
    *   `idx_brandkit_teamid` ON `brand_kits` (`teamId`)
    *   `idx_brandkit_colors_gin` ON `brand_kits` USING GIN (`colors`)
    *   `idx_brandkit_fonts_gin` ON `brand_kits` USING GIN (`fonts`)

### 5.3 `Workbench` Table (workbenches)
*   **Purpose**: A container for organizing creative projects. (REQ-4-001)
*   **SQLAlchemy Model**: `app/models/workbench_model.py` (`Workbench` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `name` (VARCHAR(100), NOT NULL)
    *   `defaultBrandKitId` (UUID, FK to `brand_kits.id`, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `BrandKit` (optional default)
    *   One-to-Many with `Project` (`projects` backref)
*   **Indexes**:
    *   `idx_workbench_userid` ON `workbenches` (`userId`)

### 5.4 `Project` Table (projects)
*   **Purpose**: Represents a creative project containing assets and generation requests. (REQ-4-002)
*   **SQLAlchemy Model**: `app/models/project_model.py` (`Project` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `workbenchId` (UUID, FK to `workbenches.id`, NOT NULL, INDEXED)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED) - Denormalized from Workbench for query performance.
    *   `templateId` (UUID, FK to `templates.id`, NULLABLE)
    *   `brandKitId` (UUID, FK to `brand_kits.id`, NULLABLE)
    *   `name` (VARCHAR(100), NOT NULL)
    *   `targetPlatform` (VARCHAR(50), NULLABLE)
    *   `collaborationState` (JSONB, NULLABLE) - Stores CRDT state for real-time collaboration.
    *   `lastCollaboratedAt` (DateTime, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP, INDEXED)
    *   `deletedAt` (DateTime, NULLABLE)
*   **Relationships**:
    *   Many-to-One with `Workbench` (`workbench` backref)
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `Template` (optional, `template` backref in Template model)
    *   Many-to-One with `BrandKit` (optional override)
    *   One-to-Many with `Asset` (`assets` backref)
    *   One-to-Many with `AssetVersion` (`versions` backref)
    *   One-to-Many with `GenerationRequest` (`generation_requests` backref)
*   **Indexes**:
    *   `idx_project_workbenchid` ON `projects` (`workbenchId`)
    *   `idx_project_userid` ON `projects` (`userId`)
    *   `idx_project_updatedat` ON `projects` (`updatedAt`)

### 5.5 `Asset` Table (assets)
*   **Purpose**: Represents uploaded or AI-generated creative asset files. (SRS 7.2.1, REQ-4-004, REQ-4-005)
*   **SQLAlchemy Model**: `app/models/asset_model.py` (`Asset` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `projectId` (UUID, FK to `projects.id`, NULLABLE, INDEXED)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `generationRequestId` (UUID, FK to `generation_requests.id`, NULLABLE, INDEXED)
    *   `name` (VARCHAR(255), NOT NULL)
    *   `type` (VARCHAR(20), NOT NULL, CHECK IN ('Uploaded','AIGenerated','Derived'), INDEXED)
    *   `filePath` (VARCHAR(1024), NOT NULL) - Path in MinIO.
    *   `mimeType` (VARCHAR(50), NOT NULL)
    *   `format` (VARCHAR(10), NOT NULL)
    *   `resolution` (VARCHAR(20), NULLABLE)
    *   `isFinal` (BOOLEAN, NOT NULL, DEFAULT false)
    *   `metadata` (JSONB, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED on (projectId, createdAt))
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
    *   `deletedAt` (DateTime, NULLABLE)
*   **Relationships**:
    *   Many-to-One with `Project` (`project` backref)
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `GenerationRequest` (if AI-generated source, `generation_request_source` backref in GenerationRequest)
    *   One-to-One with `GenerationRequest` (if this is the final output, `final_generation_output_of` backref in GenerationRequest)
    *   One-to-Many with `AssetVersion` (`versions` backref)
*   **Indexes**:
    *   `idx_asset_projectid_createdat` ON `assets` (`projectId`, `createdAt`)
    *   `idx_asset_userid` ON `assets` (`userId`)
    *   `idx_asset_generationrequestid` ON `assets` (`generationRequestId`)
    *   `idx_asset_type` ON `assets` (`type`)

### 5.6 `AssetVersion` Table (asset_versions)
*   **Purpose**: Stores version history for creative assets or project states. (SRS 7.2.1, REQ-4-006)
*   **SQLAlchemy Model**: `app/models/asset_version_model.py` (`AssetVersion` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `assetId` (UUID, FK to `assets.id`, NULLABLE, INDEXED)
    *   `projectId` (UUID, FK to `projects.id`, NULLABLE, INDEXED)
    *   `versionNumber` (INTEGER, NOT NULL)
    *   `filePath` (VARCHAR(1024), NULLABLE) - MinIO path if a file state.
    *   `stateData` (JSONB, NULLABLE) - CRDT/JSON state if a project/canvas state.
    *   `description` (TEXT, NULLABLE)
    *   `createdByUserId` (UUID, FK to `users.id`, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `Asset` (`asset` backref)
    *   Many-to-One with `Project` (`project` backref)
    *   Many-to-One with `User` (creator)
*   **Indexes**:
    *   `idx_assetversion_assetid` ON `asset_versions` (`assetId`)
    *   `idx_assetversion_projectid` ON `asset_versions` (`projectId`)
    *   `idx_assetversion_assetid_version` ON `asset_versions` (`assetId`, `versionNumber`)
    *   `idx_assetversion_projectid_version` ON `asset_versions` (`projectId`, `versionNumber`)

### 5.7 `GenerationRequest` Table (generation_requests)
*   **Purpose**: Tracks AI creative generation requests, inputs, status, and outputs. (SRS 7.2.1, REQ-3-010 to REQ-3-012)
*   **SQLAlchemy Model**: `app/models/generation_request_model.py` (`GenerationRequest` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED, ON DELETE RESTRICT)
    *   `projectId` (UUID, FK to `projects.id`, NOT NULL, INDEXED, ON DELETE SET NULL)
    *   `inputPrompt` (TEXT, NOT NULL)
    *   `styleGuidance` (TEXT, NULLABLE)
    *   `inputParameters` (JSONB, NULLABLE)
    *   `status` (VARCHAR(50), NOT NULL, DEFAULT 'Pending', CHECK IN (...), INDEXED)
    *   `errorMessage` (TEXT, NULLABLE)
    *   `sampleAssets` (JSONB, NULLABLE) - Array of references to `Asset` entities.
    *   `selectedSampleId` (UUID, NULLABLE, FK to `assets.id`)
    *   `finalAssetId` (UUID, FK to `assets.id`, NULLABLE)
    *   `creditsCostSample` (DECIMAL(10, 2), NULLABLE)
    *   `creditsCostFinal` (DECIMAL(10, 2), NULLABLE)
    *   `aiModelUsed` (VARCHAR(100), NULLABLE)
    *   `processingTimeMs` (INTEGER, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `Project` (`project` backref)
    *   One-to-Many with `Asset` (for samples if tracked individually beyond JSONB, or directly via `generationRequestId` on Asset table)
    *   One-to-One with `Asset` (for `selectedSampleId`)
    *   One-to-One with `Asset` (for `finalAssetId`, `final_asset` backref)
    *   One-to-Many with `CreditTransaction` (`credit_transactions` backref)
    *   One-to-Many with `UsageLog`
    *   One-to-Many with `AIModelFeedback` (`feedbacks` backref)
*   **Indexes**:
    *   `idx_generationrequest_userid` ON `generation_requests` (`userId`)
    *   `idx_generationrequest_projectid` ON `generation_requests` (`projectId`)
    *   `idx_generationrequest_status_createdat` ON `generation_requests` (`status`, `createdAt`)

### 5.8 `SocialMediaConnection` Table (social_media_connections)
*   **Purpose**: Stores user's connected social media accounts and OAuth tokens. (SMPIO-007)
*   **SQLAlchemy Model**: `app/models/social_media_connection_model.py` (`SocialMediaConnection` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `platform` (VARCHAR(20), NOT NULL, CHECK IN ('Instagram','Facebook','LinkedIn','Twitter','Pinterest','TikTok'))
    *   `externalUserId` (VARCHAR(100), NOT NULL)
    *   `accessToken` (TEXT, NOT NULL) - Encrypted at application layer.
    *   `refreshToken` (TEXT, NULLABLE) - Encrypted at application layer.
    *   `expiresAt` (DateTime, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
*   **Constraints**:
    *   UNIQUE (`userId`, `platform`)
*   **Indexes**:
    *   `idx_socialconnection_userid_platform` ON `social_media_connections` (`userId`, `platform`)

### 5.9 `APIClient` Table (api_clients)
*   **Purpose**: Stores API access credentials (keys and hashed secrets) for developers/API users. (REQ-7-002)
*   **SQLAlchemy Model**: `app/models/api_client_model.py` (`APIClient` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `name` (VARCHAR(100), NOT NULL)
    *   `apiKey` (VARCHAR(100), UNIQUE, NOT NULL, INDEXED)
    *   `secretHash` (VARCHAR(255), NOT NULL) - Hashed at application layer.
    *   `permissions` (JSONB, NULLABLE)
    *   `isActive` (BOOLEAN, NOT NULL, DEFAULT true)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   One-to-Many with `UsageLog` (optional)
*   **Indexes**:
    *   `idx_apiclient_apikey_unique` ON `api_clients` (`apiKey`)
    *   `idx_apiclient_userid` ON `api_clients` (`userId`)

### 5.10 `Subscription` Table (subscriptions)
*   **Purpose**: Stores user subscription details, typically synced from Odoo. (REQ-6-018)
*   **SQLAlchemy Model**: `app/models/subscription_model.py` (`Subscription` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, UNIQUE, INDEXED) - Assuming one active subscription per user.
    *   `odooSaleOrderId` (VARCHAR(255), UNIQUE, NOT NULL, INDEXED)
    *   `planId` (VARCHAR(50), NOT NULL)
    *   `status` (VARCHAR(20), NOT NULL, DEFAULT 'Active', CHECK IN ('Active','Trial','Suspended','Cancelled','Expired'), INDEXED)
    *   `currentPeriodStart` (DateTime, NOT NULL)
    *   `currentPeriodEnd` (DateTime, NOT NULL, INDEXED)
    *   `paymentProvider` (VARCHAR(50), NOT NULL, CHECK IN ('Stripe', 'PayPal', 'OdooManual'))
    *   `paymentProviderSubscriptionId` (VARCHAR(255), NULLABLE)
    *   `paymentMethodId` (VARCHAR(255), NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   One-to-One with `User` (`user` backref)
*   **Indexes**:
    *   `idx_subscription_userid_status` ON `subscriptions` (`userId`, `status`)
    *   `idx_subscription_currentperiodend` ON `subscriptions` (`currentPeriodEnd`)
    *   `idx_subscription_odoosaleorderid` ON `subscriptions` (`odooSaleOrderId`)

### 5.11 `CreditTransaction` Table (credit_transactions)
*   **Purpose**: Logs credit purchases, refunds, and consumption for billing and auditing. (Related to SRS 7.3.1)
*   **SQLAlchemy Model**: `app/models/credit_transaction_model.py` (`CreditTransaction` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `odooInvoiceId` (VARCHAR(255), NULLABLE)
    *   `generationRequestId` (UUID, FK to `generation_requests.id`, NULLABLE, INDEXED)
    *   `apiCallId` (VARCHAR(255), NULLABLE)
    *   `amount` (DECIMAL(10, 2), NOT NULL)
    *   `actionType` (VARCHAR(50), NOT NULL, INDEXED, e.g., 'purchase', 'sample_generation')
    *   `description` (TEXT, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
    *   `syncedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `GenerationRequest` (optional, `generation_request` backref)
*   **Indexes**:
    *   `idx_credittransaction_userid_createdat` ON `credit_transactions` (`userId`, `createdAt`)
    *   `idx_credittransaction_actiontype` ON `credit_transactions` (`actionType`)
    *   `idx_credittransaction_generationrequestid` ON `credit_transactions` (`generationRequestId`)
*   **Partitioning**: Range partition by `createdAt` (monthly/quarterly).

### 5.12 `UsageLog` Table (usage_logs)
*   **Purpose**: Detailed log of billable or trackable user actions for analytics and auditing. (SRS 7.3.1)
*   **SQLAlchemy Model**: `app/models/usage_log_model.py` (`UsageLog` class)
*   **Attributes**:
    *   `id` (BIGSERIAL, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `generationRequestId` (UUID, FK to `generation_requests.id`, NULLABLE, INDEXED)
    *   `apiClientId` (UUID, FK to `api_clients.id`, NULLABLE, INDEXED)
    *   `actionType` (VARCHAR(100), NOT NULL, INDEXED)
    *   `details` (JSONB, NULLABLE)
    *   `creditsCost` (DECIMAL(10, 2), NULLABLE)
    *   `timestamp` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `GenerationRequest` (optional)
    *   Many-to-One with `APIClient` (optional)
*   **Indexes**:
    *   `idx_usagelog_userid_timestamp` ON `usage_logs` (`userId`, `timestamp`)
    *   `idx_usagelog_actiontype` ON `usage_logs` (`actionType`)
    *   `idx_usagelog_generationrequestid` ON `usage_logs` (`generationRequestId`)
    *   `idx_usagelog_apiclientid` ON `usage_logs` (`apiClientId`)

### 5.13 `Team` Table (teams)
*   **Purpose**: Represents a collaboration group for team accounts. (REQ-003, UAPM-1-010)
*   **SQLAlchemy Model**: `app/models/team_model.py` (`Team` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `name` (VARCHAR(100), NOT NULL)
    *   `ownerId` (UUID, FK to `users.id`, NOT NULL, INDEXED, ON DELETE RESTRICT)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (owner, `owner` backref)
    *   One-to-Many with `TeamMember` (`members` backref)
    *   One-to-Many with `BrandKit` (`brand_kits` backref)
*   **Indexes**:
    *   `idx_team_ownerid` ON `teams` (`ownerId`)

### 5.14 `TeamMember` Table (team_members)
*   **Purpose**: Junction table associating users with teams and their roles. (REQ-003, UAPM-1-010)
*   **SQLAlchemy Model**: `app/models/team_member_model.py` (`TeamMember` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `teamId` (UUID, FK to `teams.id`, NOT NULL, INDEXED)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `role` (VARCHAR(20), NOT NULL, CHECK IN ('Owner','Admin','Editor','Viewer'), INDEXED)
    *   `joinedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `Team` (`team` backref)
    *   Many-to-One with `User` (`user` backref)
*   **Constraints**:
    *   UNIQUE (`teamId`, `userId`)
*   **Indexes**:
    *   `idx_teammember_userid_role` ON `team_members` (`userId`, `role`)
    *   `idx_teammember_teamid` ON `team_members` (`teamId`)

### 5.15 `Session` Table (sessions)
*   **Purpose**: Stores user authentication sessions for web and mobile. (UAPM-1-008, REQ-2-006)
*   **SQLAlchemy Model**: `app/models/session_model.py` (`Session` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `deviceInfo` (VARCHAR(255), NOT NULL)
    *   `ipAddress` (VARCHAR(45), NOT NULL)
    *   `userAgent` (TEXT, NULLABLE)
    *   `lastActivity` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
    *   `expiresAt` (DateTime, NOT NULL, INDEXED)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
*   **Indexes**:
    *   `idx_session_userid_expiresat` ON `sessions` (`userId`, `expiresAt`)
    *   `idx_session_expiresat` ON `sessions` (`expiresAt`)
    *   `idx_session_lastactivity` ON `sessions` (`lastActivity`)

### 5.16 `Notification` Table (notifications)
*   **Purpose**: Stores system-generated notifications for users.
*   **SQLAlchemy Model**: `app/models/notification_model.py` (`Notification` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `type` (VARCHAR(50), NOT NULL)
    *   `message` (TEXT, NOT NULL)
    *   `metadata` (JSONB, NULLABLE)
    *   `isRead` (BOOLEAN, NOT NULL, DEFAULT false, INDEXED)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
*   **Indexes**:
    *   `idx_notification_userid_isread_createdat` ON `notifications` (`userId`, `isRead`, `createdAt`)
    *   `idx_notification_userid_isread_unread` ON `notifications` (`userId`, `isRead`) WHERE `isRead` = false
*   **Partitioning**: Range partition by `createdAt` (monthly/quarterly).

### 5.17 `Template` Table (templates)
*   **Purpose**: Stores predefined system templates and user-saved private templates. (UI-003, REQ-4-003, REQ-WCI-009, REQ-WCI-010)
*   **SQLAlchemy Model**: `app/models/template_model.py` (`Template` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NULLABLE, INDEXED) - NULL for system templates.
    *   `name` (VARCHAR(100), NOT NULL)
    *   `description` (TEXT, NULLABLE)
    *   `category` (VARCHAR(50), NOT NULL, INDEXED)
    *   `previewUrl` (VARCHAR(1024), NOT NULL)
    *   `sourceData` (JSONB, NOT NULL) - Defines template structure.
    *   `tags` (JSONB, NULLABLE) - Array of strings, GIN indexed for search.
    *   `isPublic` (BOOLEAN, NOT NULL, DEFAULT true)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (creator, `user_creator` backref)
    *   One-to-Many with `Project` (`projects_using_template` backref)
*   **Indexes**:
    *   `idx_template_category_ispublic` ON `templates` (`category`, `isPublic`)
    *   `idx_template_userid` ON `templates` (`userId`)
    *   `idx_template_tags_gin` ON `templates` USING GIN (`tags`)

### 5.18 `AIModel` Table (ai_models)
*   **Purpose**: Metadata for AI models available on the platform (internal or external). (INT-007)
*   **SQLAlchemy Model**: `app/models/ai_model_model.py` (`AIModel` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `name` (VARCHAR(100), UNIQUE, NOT NULL, INDEXED)
    *   `description` (TEXT, NULLABLE)
    *   `provider` (VARCHAR(50), NOT NULL)
    *   `taskType` (VARCHAR(50), NOT NULL, CHECK IN (...), INDEXED)
    *   `isActive` (BOOLEAN, NOT NULL, DEFAULT true, INDEXED)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   One-to-Many with `AIModelVersion` (`versions` backref)
*   **Indexes**:
    *   `idx_aimodel_name_unique` ON `ai_models` (`name`)
    *   `idx_aimodel_provider_tasktype` ON `ai_models` (`provider`, `taskType`)
    *   `idx_aimodel_isactive` ON `ai_models` (`isActive`)

### 5.19 `AIModelVersion` Table (ai_model_versions)
*   **Purpose**: Stores specific versions of AI models, their source, and status. (INT-007, AISIML-008)
*   **SQLAlchemy Model**: `app/models/ai_model_version_model.py` (`AIModelVersion` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `modelId` (UUID, FK to `ai_models.id`, NOT NULL, INDEXED)
    *   `versionNumber` (VARCHAR(50), NOT NULL)
    *   `sourcePath` (VARCHAR(1024), NULLABLE) - MinIO path for internal models.
    *   `format` (VARCHAR(50), NULLABLE)
    *   `parameters` (JSONB, NULLABLE)
    *   `status` (VARCHAR(50), NOT NULL, DEFAULT 'Staged', CHECK IN (...), INDEXED)
    *   `validationResultId` (UUID, FK to `ai_model_validation_results.id`, NULLABLE)
    *   `createdByUserId` (UUID, FK to `users.id`, NULLABLE)
    *   `releaseNotes` (TEXT, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `AIModel` (`ai_model_parent` backref)
    *   One-to-One with `AIModelValidationResult` (`validation_result` backref, this side is `ai_model_versions` on `AIModelValidationResult` potentially)
    *   One-to-Many with `AIModelDeployment` (`deployments` backref)
    *   One-to-Many with `AIModelFeedback` (`feedbacks` backref)
    *   Many-to-One with `User` (creator)
*   **Constraints**:
    *   UNIQUE (`modelId`, `versionNumber`)
*   **Indexes**:
    *   `idx_aimodelversion_modelid` ON `ai_model_versions` (`modelId`)
    *   `idx_aimodelversion_status` ON `ai_model_versions` (`status`)

### 5.20 `AIModelValidationResult` Table (ai_model_validation_results)
*   **Purpose**: Stores results from validating an AI model version. (INT-007, AISIML-009)
*   **SQLAlchemy Model**: `app/models/ai_model_validation_result_model.py` (`AIModelValidationResult` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `modelVersionId` (UUID, FK to `ai_model_versions.id`, NOT NULL, UNIQUE, INDEXED)
    *   `validationTimestamp` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED)
    *   `securityScanStatus` (VARCHAR(50), NOT NULL, CHECK IN ('Passed','Failed','Pending','Skipped'))
    *   `functionalStatus` (VARCHAR(50), NOT NULL, CHECK IN ('Passed','Failed','Pending','Skipped'))
    *   `performanceBenchmark` (JSONB, NULLABLE)
    *   `results` (JSONB, NULLABLE) - Full validation log.
    *   `validatedByUserId` (UUID, FK to `users.id`, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   One-to-One with `AIModelVersion` (`model_version` backref)
    *   Many-to-One with `User` (validator)
*   **Indexes**:
    *   `idx_aimodelvalidationresult_versionid` ON `ai_model_validation_results` (`modelVersionId`)
    *   `idx_aimodelvalidationresult_timestamp` ON `ai_model_validation_results` (`validationTimestamp`)

### 5.21 `AIModelDeployment` Table (ai_model_deployments)
*   **Purpose**: Records deployments of AI model versions to various environments. (INT-007, AISIML-010)
*   **SQLAlchemy Model**: `app/models/ai_model_deployment_model.py` (`AIModelDeployment` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `modelVersionId` (UUID, FK to `ai_model_versions.id`, NOT NULL, INDEXED)
    *   `environment` (VARCHAR(50), NOT NULL, CHECK IN ('staging','production','testing'), INDEXED)
    *   `status` (VARCHAR(50), NOT NULL, DEFAULT 'Initiated', CHECK IN (...), INDEXED)
    *   `deploymentStrategy` (VARCHAR(50), NULLABLE)
    *   `endpoint` (VARCHAR(255), NULLABLE)
    *   `kubernetesDetails` (JSONB, NULLABLE)
    *   `deployedByUserId` (UUID, FK to `users.id`, NULLABLE)
    *   `deploymentTimestamp` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `updatedAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `AIModelVersion` (`model_version` backref)
    *   Many-to-One with `User` (deployer)
*   **Indexes**:
    *   `idx_aimodeldeployment_versionid_env` ON `ai_model_deployments` (`modelVersionId`, `environment`)
    *   `idx_aimodeldeployment_status` ON `ai_model_deployments` (`status`)

### 5.22 `AIModelFeedback` Table (ai_model_feedbacks)
*   **Purpose**: Stores user feedback on outputs generated by specific AI models. (INT-007, AISIML-012)
*   **SQLAlchemy Model**: `app/models/ai_model_feedback_model.py` (`AIModelFeedback` class)
*   **Attributes**:
    *   `id` (UUID, PK, NOT NULL)
    *   `userId` (UUID, FK to `users.id`, NOT NULL, INDEXED)
    *   `generationRequestId` (UUID, FK to `generation_requests.id`, NULLABLE, INDEXED)
    *   `modelVersionId` (UUID, FK to `ai_model_versions.id`, NULLABLE, INDEXED)
    *   `rating` (INTEGER, NULLABLE, CHECK (rating >= 1 AND rating <= 5))
    *   `comment` (TEXT, NULLABLE)
    *   `feedbackTimestamp` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    *   `details` (JSONB, NULLABLE)
    *   `createdAt` (DateTime, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
*   **Relationships**:
    *   Many-to-One with `User` (`user` backref)
    *   Many-to-One with `GenerationRequest` (`generation_request` backref)
    *   Many-to-One with `AIModelVersion` (`model_version` backref)
*   **Indexes**:
    *   `idx_aimodelfeedback_userid` ON `ai_model_feedbacks` (`userId`)
    *   `idx_aimodelfeedback_generationrequestid` ON `ai_model_feedbacks` (`generationRequestId`)
    *   `idx_aimodelfeedback_modelversionid` ON `ai_model_feedbacks` (`modelVersionId`)

## 6. Alembic Migration Setup

### 6.1 `alembic.ini`
This file configures the Alembic environment. Key settings:
*   `sqlalchemy.url`: Defines the connection string to the PostgreSQL database. This will be parameterized for different environments (dev, staging, prod).
    Example: `sqlalchemy.url = postgresql+psycopg2://user:password@host:port/dbname`
*   `script_location`: Points to the `versions` directory where migration scripts are stored.
    Example: `script_location = versions`
*   `file_template`: Specifies the template for new migration files (e.g., `%%(rev)s_%%(slug)s`).
*   Logging configurations for Alembic operations.

### 6.2 `env.py`
This script is executed when Alembic commands are run. It sets up the migration context.
*   **Import Base**: Imports `Base` from `app.db.base`.
*   **Import Models**: Imports all model modules from `app.models` (e.g., `from app.models import user_model, project_model, ...`). This makes all defined SQLAlchemy models children of `Base`.
*   **`target_metadata`**: Set to `Base.metadata`. This allows Alembic to compare the current database state against the state defined by the SQLAlchemy models.
*   **`run_migrations_offline()`**: Defines how to generate SQL scripts for offline migration (typically by rendering `target_metadata` to DDL).
*   **`run_migrations_online()`**: Defines how to connect to the database and apply migrations. It will:
    *   Establish a database connection using the URL from `alembic.ini`.
    *   Begin a transaction.
    *   Configure the migration context with the connection and `target_metadata`.
    *   Run migrations.
    *   Commit the transaction.

### 6.3 `script.py.mako`
This Mako template defines the structure of new migration scripts generated by `alembic revision`. It includes:
*   Imports for `alembic.op` and `sqlalchemy as sa`.
*   Placeholders for revision IDs (`%(up_revision)s`, `%(down_revision)s`, `%(branch_labels)s`, `%(depends_on)s`).
*   `upgrade()` function: Contains `op.create_table()`, `op.add_column()`, etc., calls based on autogenerated differences or manually added operations.
*   `downgrade()` function: Contains corresponding `op.drop_table()`, `op.drop_column()`, etc., calls to revert the schema changes.

### 6.4 `versions/` Directory
This directory will contain individual, ordered Python migration scripts. For example, the first migration script might be:
*   `versions/0001_create_initial_tables.py`:
    python
    """create initial tables

    Revision ID: <generated_rev_id>
    Revises: 
    Create Date: <timestamp>

    """
    from alembic import op
    import sqlalchemy as sa
    from sqlalchemy.dialects import postgresql # For UUID and JSONB

    # revision identifiers, used by Alembic.
    revision = '<generated_rev_id>'
    down_revision = None 
    branch_labels = None
    depends_on = None

    def upgrade() -> None:
        # ### commands auto generated by Alembic - please adjust! ###
        op.create_table('users',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            # ... other columns for users table ...
            sa.Column('createdAt', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.Column('updatedAt', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email', name=op.f('uq_user_email')),
            sa.UniqueConstraint('username', name=op.f('uq_user_username')) 
            # Consider uq_user_social if implementing in initial script
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True) # Example index, alembic might generate it from unique=True on column
        # ... op.create_table() for all other tables (BrandKit, Workbench, Project, etc.) ...
        # ... op.create_index() for all other necessary indexes ...
        # ### end Alembic commands ###

    def downgrade() -> None:
        # ### commands auto generated by Alembic - please adjust! ###
        # ... op.drop_index() for all indexes ...
        # ... op.drop_table() for all tables in reverse order of creation ...
        op.drop_table('users')
        # ### end Alembic commands ###
    
    This script will use `alembic.op` functions to create tables, columns, constraints, and indexes based on the definitions in the SQLAlchemy models (from `app.models`). Subsequent migration scripts will handle schema alterations.

## 7. DDL Scripts (Informative)
The `ddl/tables/` directory will contain raw SQL DDL scripts corresponding to each table. These are primarily for reference, documentation, or for manual database setup in specific scenarios (e.g., setting up a read-only analysis database without running migrations). Alembic, driven by SQLAlchemy models, remains the authoritative source for schema management.

Example: `ddl/tables/001_create_users.sql`
sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    social_provider VARCHAR(50) CHECK (social_provider IN ('google', 'facebook', 'apple')),
    social_provider_id VARCHAR(255),
    is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP WITHOUT TIME ZONE,
    full_name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    profile_picture_url VARCHAR(1024),
    language_preference VARCHAR(10) NOT NULL DEFAULT 'en-US',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(255), -- Application layer encryption
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'Free' CHECK (subscription_tier IN ('Free','Pro','Team','Enterprise')),
    credit_balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    last_login_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITHOUT TIME ZONE,
    UNIQUE (social_provider, social_provider_id)
);

CREATE INDEX idx_user_email_unique ON users (email);
CREATE INDEX idx_user_username_unique ON users (username) WHERE username IS NOT NULL;
CREATE INDEX idx_user_social_unique ON users (social_provider, social_provider_id) WHERE social_provider IS NOT NULL AND social_provider_id IS NOT NULL;
CREATE INDEX idx_user_subscriptiontier ON users (subscription_tier);
CREATE INDEX idx_user_deletedat ON users (deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX idx_user_languagepreference ON users (language_preference);

-- Foreign Key constraints will be defined in relevant child table DDLs or as ALTER TABLE statements
-- after all tables are created if preferred for DDL-only setup.

Similar DDL scripts will be created for all other tables, reflecting the columns, types, and constraints defined in their respective SQLAlchemy models and the `databaseDesign` JSON.

## 8. Data Integrity and Constraints
Data integrity is enforced through:
*   **Primary Keys (PK)**: Uniquely identify each row in a table (mostly UUIDs).
*   **Foreign Keys (FK)**: Maintain referential integrity between related tables, defining `ON DELETE` and `ON UPDATE` cascade/restrict/set null behaviors as appropriate.
*   **UNIQUE Constraints**: Ensure specified columns or combinations of columns have unique values (e.g., `users.email`, `users.username`).
*   **NOT NULL Constraints**: Ensure essential columns always have a value.
*   **CHECK Constraints**: Enforce domain-specific rules on column values (e.g., `User.subscriptionTier IN (...)`, `SocialMediaConnection.platform IN (...)`).
*   **Default Values**: Provide sensible defaults for columns where appropriate.

## 9. Indexing Strategy
Indexes are crucial for query performance. The general strategy includes:
*   **Primary Keys**: Automatically indexed.
*   **Foreign Keys**: Indexed to speed up JOIN operations and enforce referential integrity checks.
*   **UNIQUE Constraints**: Automatically create unique indexes.
*   **Frequently Queried Columns**: Columns frequently used in `WHERE` clauses, `ORDER BY`, or `GROUP BY` clauses will be indexed.
*   **JSONB Columns**: GIN indexes will be used for `JSONB` columns where searching within the JSON structure is required (e.g., `BrandKit.colors`, `Template.tags`).
*   **Partial Indexes**: Used where appropriate (e.g., `idx_user_deletedat` on `users(deletedAt)` WHERE `deletedAt` IS NOT NULL).
*   Specific indexes for each table are detailed within their respective sections above and align with the `databaseDesign` input.

## 10. Security Considerations (Schema Level)
*   **Sensitive Data Accommodation**: The schema includes fields for sensitive data (`passwordHash`, `mfaSecret`, `accessToken`, `refreshToken`, `apiKey.secretHash`). The actual hashing and encryption of these fields are handled at the application layer. The database schema simply provides appropriately typed columns (e.g., VARCHAR) to store the processed (hashed/encrypted) values.
*   **Principle of Least Privilege**: Database user roles and permissions for accessing tables/schemas will be managed at the infrastructure/DBA level, separate from the schema definition itself, but are a critical part of overall data security.
*   **Data Segregation**: Logical separation of data by `userId`, `teamId`, `projectId` etc., helps in implementing application-level access controls.

## 11. Scalability and Performance (Schema Impact)
*   **Read Replicas**: The design supports the use of PostgreSQL read replicas by ensuring common read patterns can be directed to them.
*   **Data Types**: Appropriate data types are chosen to optimize storage and performance (e.g., UUID, specific VARCHAR lengths, DECIMAL for currency/credits, JSONB for flexible structured data).
*   **Normalization**: Helps in reducing data redundancy, which can improve write performance and consistency, though it may require more JOINs for reads (mitigated by indexing).
*   **Indexing**: Comprehensive indexing strategy (see Section 9) is vital for query performance.
*   **Partitioning**: For very high-volume tables like `CreditTransaction`, `UsageLog`, and `Notification`, range partitioning by `createdAt` (or `timestamp`) is recommended and specified in the `databaseDesign`. This helps in managing large datasets, improving query performance on recent data, and simplifying data archival/purging. Alembic can be used to manage partitions, though it might require custom operations for more complex partitioning schemes.

## 12. Documentation
*   **Entity-Relationship Diagrams (ERDs)**: A primary ERD (`docs/diagrams/creativeflow_ai_erd.png`) visualizing the overall schema will be maintained. Additional, more focused diagrams for specific domains (User Management, Creative Workflow, AI/Billing) are provided in the architecture documentation and align with this schema.
*   **SQLAlchemy Models**: The Python files in `app/models/` serve as code-based documentation of the schema.
*   **Alembic Migrations**: The `versions/` directory provides a historical record of all schema changes.
*   **DDL Scripts**: The `ddl/` directory provides raw SQL for reference.

## 13. Non-Functional Requirements Mapping
*   **NFR-003 (Availability, RTO/RPO)**: The schema design supports HA and DR through features like UUID PKs (facilitating multi-master or distributed setups if ever needed), and clear separation of data for replication strategies. RPO/RTO are primarily met by infrastructure and backup strategies which this schema is designed to support.
*   **NFR-004 (Fault Tolerance/Data Replication)**: Schema design allows for PostgreSQL streaming replication and MinIO replication by having clear data entities and keys.
*   **NFR-005 (Scalability)**: Supported by indexing, normalization, support for read replicas, and partitioning considerations.
*   **NFR-006 (Data Protection/Security)**: Schema accommodates storage of hashed/encrypted sensitive data and enables application-level enforcement of access controls. Soft deletes and clear data ownership support GDPR/CCPA.
*   **DEP-003 (Database Migration Automation)**: Directly addressed by the use of Alembic and version-controlled migration scripts.

## 14. Future Considerations
*   **Sharding/Distributed SQL**: While not an initial requirement, the use of UUIDs and a modular data design could facilitate future transitions to sharded or distributed SQL databases if extreme scale is required.
*   **Graph Database Integration**: For complex relationships (e.g., social graphs, highly interconnected project data), future integration with a graph database might be considered for specific query patterns, with this PostgreSQL schema remaining the system of record for core entities.
*   **Further Denormalization**: As query patterns evolve under load, specific denormalizations might be introduced strategically for performance, managed via Alembic migrations.
*   **Schema Registry for Events**: If event sourcing becomes more prevalent, a schema registry for event payloads could complement the relational schema.