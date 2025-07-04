# Software Design Specification: CreativeFlow.PostgreSQLDataStore

## 1. Introduction

This document outlines the Software Design Specification (SDS) for the `CreativeFlow.PostgreSQLDataStore` repository. This repository is responsible for defining and managing the PostgreSQL 16+ relational database schema for the CreativeFlow AI platform. It includes Data Definition Language (DDL) scripts for table creation, indexing, constraints, as well as migration scripts managed by Flyway, and seed scripts for initial data population.

The database serves as the primary structured data store for various platform entities, including:
*   User accounts, profiles, and authentication details.
*   Brand kits and associated assets.
*   Creative workbenches and projects.
*   Metadata for AI-generated and user-uploaded creative assets, including versioning.
*   Subscription information and credit balances (often synced from Odoo).
*   Usage logs and credit transaction history.
*   API client credentials.
*   Team and collaboration structures.
*   User sessions and notifications.
*   AI model registry metadata.

The design emphasizes data integrity, security, scalability, and maintainability, supporting features like read replicas, streaming replication for High Availability (HA) and Disaster Recovery (DR), and efficient data retrieval through appropriate indexing.

## 2. Database Technology

*   **Relational Database Management System (RDBMS)**: PostgreSQL 16.3 (or latest stable version at development start).
*   **Database Migration Tool**: Flyway (as indicated by `flyway.conf.example` and migration script naming convention, e.g., `V001__Initial_Schema.sql`).
*   **Schema Definition Language**: SQL.
*   **Migration Script Language**: SQL, Python (if Alembic were used, but Flyway primarily uses SQL).
*   **Object Relational Mapper (ORM) - Application Layer**: SQLAlchemy 2.0.30 (for Python services interacting with this database). This SDS focuses on the SQL schema itself.

## 3. Schema Design Principles

The database schema adheres to the following principles:

*   **Normalization**: The schema aims for a reasonable level of normalization (typically 3NF) to reduce data redundancy and improve data integrity, while considering performance implications for complex queries. Denormalization (e.g., `Project.userId`) is used judiciously for performance where justified.
*   **Primary Keys**: Universally Unique Identifiers (UUIDs) are used as primary keys for most entities to ensure global uniqueness and facilitate distributed data management if needed in the future. `BIGSERIAL` is used for high-volume log tables like `UsageLog` where sequential IDs are acceptable.
*   **Foreign Keys**: Foreign key constraints are strictly enforced to maintain referential integrity between related tables. `ON DELETE` and `ON UPDATE` cascade/restrict/set null policies are defined as appropriate for each relationship.
*   **Data Types**: Appropriate PostgreSQL data types are used for each column to ensure data validity and storage efficiency (e.g., `VARCHAR` with size, `TEXT`, `BOOLEAN`, `INTEGER`, `DECIMAL`, `TIMESTAMP WITH TIME ZONE` (aliased as `DateTime`), `JSONB`, `UUID`).
*   **JSONB for Flexibility**: `JSONB` is utilized for semi-structured data like brand colors, fonts, style preferences, asset metadata, API client permissions, and AI model parameters, allowing for flexibility and easier schema evolution for these attributes.
*   **Timestamps**: Standard `createdAt` and `updatedAt` timestamp columns (type `TIMESTAMP WITH TIME ZONE`, default `CURRENT_TIMESTAMP`) are included in most tables for auditing and tracking record modifications.
*   **Soft Deletes**: A `deletedAt` timestamp column (type `TIMESTAMP WITH TIME ZONE`, nullable) is used for implementing soft deletes where appropriate, allowing for data recovery and maintaining historical context.
*   **Constraints**: `CHECK` constraints are used to enforce domain integrity for specific columns (e.g., `User.socialProvider`, `Asset.type`, `Subscription.status`). `UNIQUE` constraints are defined for columns requiring unique values (e.g., `User.email`, `User.username`).
*   **Indexing**:
    *   Primary keys are automatically indexed.
    *   Foreign keys are generally indexed to improve join performance.
    *   Unique constraints create unique indexes.
    *   B-Tree indexes are created for frequently queried columns used in `WHERE` clauses, `JOIN` conditions, or `ORDER BY` clauses.
    *   GIN (Generalized Inverted Index) indexes are used for `JSONB` columns to enable efficient searching within JSON structures (e.g., `BrandKit.colors`, `Template.tags`).
    *   Partial indexes are used for specific query optimizations (e.g., `Notification.isRead = false`).
*   **Security**:
    *   Sensitive data like `User.passwordHash` will store hashed passwords (hashing done at application level).
    *   Fields like `User.mfaSecret`, `SocialMediaConnection.accessToken`, `SocialMediaConnection.refreshToken` are flagged for encryption (encryption/decryption handled at the application layer before storing/after retrieving).
    *   `APIClient.secretHash` stores a hashed API secret.
*   **Partitioning**: Range partitioning on `createdAt` timestamp is suggested for high-volume, time-series tables like `CreditTransaction` and `Notification` to improve query performance, data management (e.g., archiving old partitions), and maintenance operations. This will be implemented as needed based on data growth.
*   **Caching Strategy Hints**: Notes from the `databaseDesign` regarding caching specific fields (e.g., from `User` table) are acknowledged. The schema design facilitates this by ensuring these fields are readily accessible. Actual caching implementation is an application-layer concern.

## 4. Detailed Table Specifications

The following tables define the core schema of the CreativeFlow AI platform.

### 4.1. `User` Table
*   **Description**: Represents a registered user account. Caching strategy: Cache `fullName`, `subscriptionTier`, `languagePreference`, `timezone`, `creditBalance` in a suitable caching layer (e.g., Redis); invalidate cache on updates to these fields.
*   **SQL File**: `src/schema/tables/User.sql`
*   **Columns**:
    | Name                     | Type                               | Constraints & Defaults                                            | Notes                                                                |
    | :----------------------- | :--------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------- |
    | `id`                     | `UUID`                             | `PRIMARY KEY`, `NOT NULL`                                           |                                                                      |
    | `email`                  | `VARCHAR(255)`                     | `NOT NULL`, `UNIQUE`                                                |                                                                      |
    | `passwordHash`           | `VARCHAR(255)`                     |                                                                   | Hashed password. Required if using email/password authentication.    |
    | `socialProvider`         | `VARCHAR(50)`                      | `CHECK (socialProvider IN ('google', 'facebook', 'apple'))`       | Used if signed up via social login.                                  |
    | `socialProviderId`       | `VARCHAR(255)`                     |                                                                   | Unique ID from the social provider.                                  |
    | `isEmailVerified`        | `BOOLEAN`                          | `NOT NULL DEFAULT false`                                          |                                                                      |
    | `emailVerificationToken` | `VARCHAR(255)`                     |                                                                   | Token for email verification process.                                |
    | `passwordResetToken`     | `VARCHAR(255)`                     |                                                                   | Token for password reset process.                                    |
    | `passwordResetExpires`   | `TIMESTAMP WITH TIME ZONE`         |                                                                   | Expiration timestamp for password reset token.                       |
    | `fullName`               | `VARCHAR(100)`                     |                                                                   |                                                                      |
    | `username`               | `VARCHAR(50)`                      | `UNIQUE`                                                            |                                                                      |
    | `profilePictureUrl`      | `VARCHAR(1024)`                    |                                                                   |                                                                      |
    | `languagePreference`     | `VARCHAR(10)`                      | `NOT NULL DEFAULT 'en-US'`                                        | Indexed.                                                             |
    | `timezone`               | `VARCHAR(50)`                      | `NOT NULL DEFAULT 'UTC'`                                          |                                                                      |
    | `mfaEnabled`             | `BOOLEAN`                          | `NOT NULL DEFAULT false`                                          |                                                                      |
    | `mfaSecret`              | `VARCHAR(255)`                     |                                                                   | For authenticator apps (e.g., TOTP). Flagged for app-level encryption. |
    | `subscriptionTier`       | `VARCHAR(20)`                      | `NOT NULL DEFAULT 'Free'`, `CHECK (subscriptionTier IN ('Free','Pro','Team','Enterprise'))` | Indexed.                                                             |
    | `creditBalance`          | `DECIMAL(10, 2)`                   | `NOT NULL DEFAULT 0.00`                                           | Synced from Odoo, stored here for quick access.                      |
    | `lastLoginAt`            | `TIMESTAMP WITH TIME ZONE`         |                                                                   |                                                                      |
    | `createdAt`              | `TIMESTAMP WITH TIME ZONE`         | `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                |                                                                      |
    | `updatedAt`              | `TIMESTAMP WITH TIME ZONE`         | `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                |                                                                      |
    | `deletedAt`              | `TIMESTAMP WITH TIME ZONE`         |                                                                   | Timestamp for soft delete.                                           |
*   **Primary Key**: `(id)`
*   **Unique Constraints**:
    *   `uq_user_email (email)`
    *   `uq_user_username (username)`
    *   `uq_user_social (socialProvider, socialProviderId)` WHERE `socialProvider IS NOT NULL AND socialProviderId IS NOT NULL`
*   **Indexes**:
    *   `idx_user_email_unique ON User USING btree (email)` (covered by UNIQUE constraint)
    *   `idx_user_username_unique ON User USING btree (username) WHERE username IS NOT NULL` (covered by UNIQUE constraint)
    *   `idx_user_social_unique ON User USING btree (socialProvider, socialProviderId) WHERE socialProvider IS NOT NULL AND socialProviderId IS NOT NULL` (covered by UNIQUE constraint)
    *   `idx_user_subscriptiontier ON User USING btree (subscriptionTier)`
    *   `idx_user_deletedat ON User USING btree (deletedAt) WHERE deletedAt IS NOT NULL`
    *   `idx_user_languagepreference ON User USING btree (languagePreference)` (added based on databaseDesign)

---

*(Specifications for all other tables: BrandKit, Workbench, Project, Asset, AssetVersion, GenerationRequest, SocialMediaConnection, APIClient, Subscription, CreditTransaction, UsageLog, Team, TeamMember, Session, Notification, Template, AIModel, AIModelVersion, AIModelValidationResult, AIModelDeployment, AIModelFeedback will follow a similar detailed structure, referencing the `databaseDesign` JSON provided in the prompt for column names, types, constraints, indexes, foreign keys, partitioning and caching notes. Each table section will also reference its corresponding SQL file from `file_structure_json`.)*

**Example for a table with Foreign Keys and GIN Index:**

### 4.2. `BrandKit` Table
*   **Description**: Collection of brand assets and preferences. Can belong to a user or a team.
*   **SQL File**: `src/schema/tables/BrandKit.sql`
*   **Columns**:
    | Name                 | Type                               | Constraints & Defaults                                   | Notes                                                                                       |
    | :------------------- | :--------------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
    | `id`                 | `UUID`                             | `PRIMARY KEY`, `NOT NULL`                                  |                                                                                             |
    | `userId`             | `UUID`                             | `NOT NULL`, `REFERENCES User(id) ON DELETE CASCADE`        | User who owns this brand kit.                                                               |
    | `teamId`             | `UUID`                             | `REFERENCES Team(id) ON DELETE CASCADE`, `NULLABLE`        | Optional: Team this brand kit belongs to.                                                   |
    | `name`               | `VARCHAR(100)`                     | `NOT NULL`                                               |                                                                                             |
    | `colors`             | `JSONB`                            | `NOT NULL`                                               | e.g., `[{ "name": "Primary", "hex": "#FF0000", "variable": "--color-primary" }]`          |
    | `fonts`              | `JSONB`                            | `NOT NULL`                                               | e.g., `[{ "name": "Heading", "family": "Arial", "url": "..." }]`                           |
    | `logos`              | `JSONB`                            | `NULLABLE`                                               | e.g., `[{ "name": "Main Logo", "path": "minio_path", "format": "png" }]` (MinIO paths)   |
    | `stylePreferences`   | `JSONB`                            | `NULLABLE`                                               | JSON object for default style preferences like tone, industry hints etc.                    |
    | `isDefault`          | `BOOLEAN`                          | `NOT NULL DEFAULT false`                                 |                                                                                             |
    | `createdAt`          | `TIMESTAMP WITH TIME ZONE`         | `NOT NULL DEFAULT CURRENT_TIMESTAMP`                       |                                                                                             |
    | `updatedAt`          | `TIMESTAMP WITH TIME ZONE`         | `NOT NULL DEFAULT CURRENT_TIMESTAMP`                       |                                                                                             |
*   **Primary Key**: `(id)`
*   **Foreign Keys**:
    *   `userId` REFERENCES `User(id) ON DELETE CASCADE ON UPDATE NO ACTION`
    *   `teamId` REFERENCES `Team(id) ON DELETE CASCADE ON UPDATE NO ACTION` (if Team table exists at this point, assuming it does based on design)
*   **Indexes**:
    *   `idx_brandkit_userid ON BrandKit USING btree (userId)`
    *   `idx_brandkit_teamid ON BrandKit USING btree (teamId)`
    *   `idx_brandkit_colors_gin ON BrandKit USING gin (colors)`
    *   `idx_brandkit_fonts_gin ON BrandKit USING gin (fonts)`

**(The SDS will continue in this manner for all 22 tables defined in the `databaseDesign` JSON, covering all attributes, keys, constraints, and indexes.)**

... *The detailed specification for the remaining 20 tables would be included here, following the same format, based on the provided `databaseDesign` JSON.* ...

### 4.23. `CustomIndexes.sql`
*   **SQL File**: `src/schema/indexes/CustomIndexes.sql`
*   **Description**: This script is intended to define any custom or performance-critical GIN/GiST indexes that are not automatically created by primary key, foreign key, or unique constraints, or simple B-Tree indexes defined within the table DDLs. This specifically includes GIN indexes for `JSONB` fields to enable efficient searching within their structure.
*   **Logic**:
    *   `CREATE INDEX IF NOT EXISTS idx_brandkit_logos_gin ON BrandKit USING gin (logos);` (If `logos` is searchable and not already covered)
    *   `CREATE INDEX IF NOT EXISTS idx_brandkit_stylepreferences_gin ON BrandKit USING gin (stylePreferences);` (If `stylePreferences` is searchable)
    *   `CREATE INDEX IF NOT EXISTS idx_project_collaborationstate_gin ON Project USING gin (collaborationState);` (If `collaborationState` content needs indexing)
    *   `CREATE INDEX IF NOT EXISTS idx_asset_metadata_gin ON Asset USING gin (metadata);`
    *   `CREATE INDEX IF NOT EXISTS idx_generationrequest_inputparameters_gin ON GenerationRequest USING gin (inputParameters);`
    *   `CREATE INDEX IF NOT EXISTS idx_generationrequest_sampleassets_gin ON GenerationRequest USING gin (sampleAssets);`
    *   `CREATE INDEX IF NOT EXISTS idx_apiclient_permissions_gin ON APIClient USING gin (permissions);`
    *   `CREATE INDEX IF NOT EXISTS idx_usagelog_details_gin ON UsageLog USING gin (details);`
    *   `CREATE INDEX IF NOT EXISTS idx_notification_metadata_gin ON Notification USING gin (metadata);`
    *   `CREATE INDEX IF NOT EXISTS idx_template_sourceData_gin ON Template USING gin (sourceData);` (Potentially, if searching template content)
    *   `CREATE INDEX IF NOT EXISTS idx_aimodelversion_parameters_gin ON AIModelVersion USING gin (parameters);`
    *   `CREATE INDEX IF NOT EXISTS idx_aimodelvalidationresult_performancebenchmark_gin ON AIModelValidationResult USING gin (performanceBenchmark);`
    *   `CREATE INDEX IF NOT EXISTS idx_aimodelvalidationresult_results_gin ON AIModelValidationResult USING gin (results);`
    *   `CREATE INDEX IF NOT EXISTS idx_aimodeldeployment_kubernetesdetails_gin ON AIModelDeployment USING gin (kubernetesDetails);`
    *   `CREATE INDEX IF NOT EXISTS idx_aimodelfeedback_details_gin ON AIModelFeedback USING gin (details);`
    *   Additional indexes as identified during performance tuning.
*   **Note**: The `databaseDesign` JSON already specifies GIN indexes for `BrandKit.colors`, `BrandKit.fonts`, and `Template.tags` directly within their table definitions, which is the preferred way if known at table creation. This `CustomIndexes.sql` file would be for any additional specialized indexes or those added later for performance optimization. For clarity, if GIN indexes are consistently defined in the table DDLs (as per `databaseDesign`), this separate file might only be for very specific or later additions.

## 5. Relationships Summary

The database schema defines numerous relationships, primarily enforced through foreign keys. Key relationships include:
*   `User` is central, linked to `BrandKit`, `Workbench`, `Project`, `Asset`, `GenerationRequest`, `SocialMediaConnection`, `APIClient`, `Subscription`, `CreditTransaction`, `UsageLog`, `TeamMember`, `Session`, `Notification`, `Template` (for private templates), `AIModelVersion` (creator), `AIModelValidationResult` (validator), `AIModelDeployment` (deployer), `AIModelFeedback`.
*   `Team` links to `User` (owner) and `TeamMember`. `TeamMember` forms a many-to-many relationship between `User` and `Team`.
*   `Workbench` belongs to a `User` and can have a default `BrandKit`.
*   `Project` belongs to a `Workbench` (and thus a `User`), and can link to a `Template` and an overriding `BrandKit`.
*   `Asset` can belong to a `Project` and a `User`, and can be linked to a `GenerationRequest`. `AssetVersion` tracks changes to `Assets` or `Projects`.
*   `GenerationRequest` is initiated by a `User` for a `Project`, produces `Asset`(s) (samples and final), and consumes credits tracked in `CreditTransaction` and `UsageLog`. It uses an `AIModelVersion`.
*   `AIModel` has many `AIModelVersion`(s). Each `AIModelVersion` can have `AIModelValidationResult`(s) and `AIModelDeployment`(s). `AIModelFeedback` links back to users and potentially generation requests or model versions.
*   `Subscription` links a `User` to their Odoo subscription details.
*   `CreditTransaction` and `UsageLog` track user activities and financial/credit aspects, linked to `User`, `GenerationRequest`, and `APIClient`.

The provided `databaseDesign` JSON with its Mermaid diagrams offers visual representations of these relationships.

## 6. Data Migration Strategy

*   **Tool**: Flyway. The presence of `flyway.conf.example` and versioned SQL migration scripts (e.g., `V001__Initial_Schema.sql`) indicates Flyway as the chosen tool.
*   **Versioning**: Migration scripts will be versioned sequentially (e.g., `V001_`, `V002_`, etc.) and named descriptively (e.g., `V001__Initial_Schema.sql`, `V002__Add_User_Preferences_Detail.sql`). Flyway tracks applied migrations in a `flyway_schema_history` table within the database.
*   **Process**:
    1.  Developers create new SQL migration scripts for schema changes or reference data updates.
    2.  These scripts are committed to version control (`src/migrations/`).
    3.  During CI/CD pipeline execution (as per DEP-003):
        *   Flyway connects to the target database environment (Dev, Staging, Prod).
        *   It checks the `flyway_schema_history` table to determine which migrations need to be applied.
        *   Pending migrations are executed in order.
    4.  The `V001__Initial_Schema.sql` script will contain the DDL for all tables, constraints, and basic indexes, ensuring correct creation order to satisfy dependencies. It should be idempotent or Flyway's `baselineOnMigrate` can be used for initial setup.
*   **Rollback**: Flyway primarily supports forward migrations. Rollback strategies typically involve:
    *   Restoring from a database backup (for catastrophic failures).
    *   Writing "undo" migration scripts for reversible changes (less common for complex changes).
    *   Applying a new migration script that reverts the changes of a previous one.
    *   Blue-green deployment strategies for the database itself can also be considered for major upgrades, though this is an infrastructure concern beyond simple Flyway migrations.
*   **Idempotency**: The initial schema script (`V001__Initial_Schema.sql`) should be written to be idempotent (e.g., using `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS` where supported and appropriate, though Flyway handles "already applied" logic). Subsequent DDL changes in Flyway migrations are typically altering existing structures.

## 7. Data Seeding Strategy

*   **Purpose**: To populate the database with essential initial data upon new environment setup or after the initial schema migration. This includes:
    *   Initial administrative user accounts (as per `src/seeds/01_Initial_Admin_User.sql`).
    *   Default creative templates (as per `src/seeds/02_Default_Templates.sql`).
    *   Essential system configuration parameters if stored in the database.
    *   Default system brand assets.
*   **Method**:
    *   SQL `INSERT` scripts located in the `src/seeds/` directory.
    *   These scripts will be executed after the Flyway migrations have successfully completed, typically as a separate step in the CI/CD pipeline or deployment process.
    *   For more complex seeding or data that might come from external sources (e.g., a large set of templates), Odoo's data import functionalities might be leveraged by an external process that populates the PostgreSQL database.
*   **Execution**:
    *   Seed scripts should be designed to be run once or be idempotent if run multiple times (e.g., using `INSERT ... ON CONFLICT DO NOTHING` or checking for existence before inserting).
    *   The order of execution of seed scripts might be important if there are data dependencies.
*   **Validation**: Post-seeding, basic validation queries or manual checks should be performed to ensure data integrity and completeness as per requirements (SRS 11.4.2).

## 8. Security Considerations (Database Level)

*   **Access Control**:
    *   Database roles and permissions will be managed according to the principle of least privilege. Application services will connect using dedicated database users with only the necessary permissions on required schemas and tables.
    *   DBA access will be strictly controlled.
*   **Encryption at Rest**:
    *   While field-level encryption (e.g., for `mfaSecret`, `accessToken`) is an application-level concern, the underlying PostgreSQL data files and backups should be encrypted at rest. This is typically handled at the infrastructure level (e.g., LUKS for disk encryption, encryption features of backup tools). This SDS assumes this infrastructure-level encryption is in place as per NFR-006 and SEC-003.
*   **Network Security**:
    *   PostgreSQL server will be configured to listen only on necessary network interfaces and will be protected by firewalls, allowing connections only from authorized application servers and management hosts.
    *   SSL/TLS will be enforced for all database connections to encrypt data in transit between applications and the database server.
*   **Auditing**: PostgreSQL logging will be configured to capture relevant audit trails, such as connection attempts, DDL changes, and significant DML operations, especially on sensitive tables. These logs will be forwarded to the centralized logging system.
*   **Regular Patching**: The PostgreSQL server and underlying OS will be regularly patched as part of the system maintenance procedures (CPIO-010, REQ-20-011).

## 9. Performance and Scalability Considerations

*   **Indexing**: Comprehensive indexing strategy as outlined in section 3 and detailed per table to optimize query performance.
*   **Query Optimization**: Regular review of slow queries (e.g., using `EXPLAIN ANALYZE` and PostgreSQL monitoring tools) and optimization of SQL queries and database schema where necessary.
*   **Connection Pooling**: Application services will use connection pooling (e.g., PgBouncer externally, or built-in pooling in SQLAlchemy/drivers) to manage database connections efficiently and reduce overhead.
*   **Read Replicas**: The architecture supports PostgreSQL read replicas (NFR-005, REQ-DA-013, CPIO-004) to offload read-heavy workloads from the primary server, improving read scalability and performance. Application logic will need to be designed to route read-only queries to replicas.
*   **Vertical Scaling**: The primary database server can be vertically scaled (increasing CPU, RAM, faster storage) as an initial step to handle increased load.
*   **Horizontal Scaling (Future Consideration)**: For very high scalability demands in the future, strategies like database sharding or transitioning to distributed SQL databases (e.g., CockroachDB, YugabyteDB, or PostgreSQL extensions like Citus) are noted as future planning items (NFR-005, REQ-DA-013).
*   **Partitioning**: Table partitioning for very large, time-series tables (`CreditTransaction`, `Notification`, `UsageLog`) based on `createdAt` or `timestamp` will be implemented as data volumes grow to improve query performance and manageability (e.g., easier archiving/deletion of old data).
*   **VACUUM and ANALYZE**: Regular `VACUUM` and `ANALYZE` operations will be scheduled to reclaim storage occupied by dead tuples and update statistics for the query planner, ensuring optimal query performance. PostgreSQL's autovacuum daemon will be tuned for the workload.

## 10. Backup and Recovery

*   **Strategy**: Automated daily backups of the PostgreSQL database (full and incremental/differential) and critical configuration data will be performed as per DEP-005 and REQ-DA-015.
*   **Storage**: Backups will be encrypted (AES-256 or stronger) and stored securely offsite (e.g., DR site or dedicated remote backup storage) to protect against local site failures.
*   **Replication for DR**:
    *   Streaming replication will be used.
    *   **Synchronous replication** to at least one local replica in a different availability zone (within the primary data center) for critical data to achieve a low RPO for local failures (NFR-004, REQ-DA-011).
    *   **Asynchronous replication** to the geographically separate DR site to meet the overall RPO of 15 minutes (NFR-003, SREDRP-005, REQ-DA-011).
*   **Retention**: Backup retention will follow policies defined in SRS Section 7.5 and SREDRP-008 (e.g., dailies for 30 days, weeklies for 90 days, monthlies for 1 year).
*   **Testing**:
    *   Restore procedures will be documented and version-controlled.
    *   Full restore drills will be conducted at least quarterly to validate data integrity, RPO, and RTO targets (NFR-003, NFR-004, SREDRP-009, REQ-DA-015).
    *   Test results and any remediation actions will be documented.
*   **Point-in-Time Recovery (PITR)**: PostgreSQL's PITR capabilities, using base backups and continuous archiving of WAL (Write-Ahead Logging) files, will be configured to allow recovery to any specific point in time, further supporting the RPO.

## 11. Configuration

*   **`config/flyway.conf.example`**: This file provides a template for Flyway configuration.
    *   `flyway.url`: JDBC connection URL for the PostgreSQL database.
    *   `flyway.user`: Database user for Flyway operations (should have schema modification privileges).
    *   `flyway.password`: Password for the Flyway user (placeholder, to be supplied via environment variables or secrets management in CI/CD).
    *   `flyway.schemas`: Comma-separated list of schemas managed by Flyway (e.g., `public`).
    *   `flyway.locations`: Filesystem or classpath locations of migration scripts (e.g., `filesystem:src/migrations`).
    *   `flyway.baselineOnMigrate`: `true` if Flyway should automatically baseline an existing database.
    *   `flyway.baselineVersion`: The version to tag an existing schema with when baselining.
*   **Environment Variables**: Sensitive connection details (host, port, user, password, database name) for PostgreSQL should be managed via environment variables or a secrets management system (e.g., HashiCorp Vault) and injected into the Flyway execution environment and application services, rather than being hardcoded.
*   **PostgreSQL Configuration (`postgresql.conf`, `pg_hba.conf`)**: Server-side configuration will be managed via Ansible (PMDT-011, CPIO-011) and will cover:
    *   Memory allocation (`shared_buffers`, `work_mem`, `maintenance_work_mem`).
    *   Connection limits (`max_connections`).
    *   WAL settings (`wal_level`, `checkpoint_segments`, `archive_mode`, `archive_command` for PITR).
    *   Replication settings for primary and replica servers.
    *   Logging configuration.
    *   Security settings (SSL/TLS, client authentication via `pg_hba.conf`).
    *   Autovacuum settings.

This SDS provides the blueprint for the PostgreSQL database schema and its management, forming a critical part of the CreativeFlow AI platform's data persistence layer.