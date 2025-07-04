# Specification

# 1. Files

- **Path:** database/postgresql-schema-migrations/alembic.ini  
**Description:** Configuration file for Alembic database migration tool. Specifies database connection URL, migration script locations, and other settings.  
**Template:** INI Configuration  
**Dependency Level:** 0  
**Name:** alembic  
**Type:** Configuration  
**Relative Path:** alembic.ini  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alembic Configuration
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To configure the Alembic migration environment, including the database connection and script directory.  
**Logic Description:** Contains sections for Alembic settings, logger configurations, and the path to migration scripts. The sqlalchemy.url key defines the database connection string.  
**Documentation:**
    
    - **Summary:** Main configuration file for Alembic. Defines how Alembic connects to the database and finds migration scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** database/postgresql-schema-migrations/env.py  
**Description:** Alembic environment script. Configures the migration context, database connection, and how schema changes are detected or defined, typically by importing SQLAlchemy models.  
**Template:** Python Alembic Environment  
**Dependency Level:** 1  
**Name:** env  
**Type:** Configuration  
**Relative Path:** env.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** run_migrations_offline  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** run_migrations_online  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Alembic Migration Context Setup
    - SQLAlchemy Model Integration for Migrations
    
**Requirement Ids:**
    
    - DEP-003
    - Section 7
    
**Purpose:** To set up the runtime environment for Alembic migrations, linking SQLAlchemy models to the migration generation process.  
**Logic Description:** Imports necessary Alembic and SQLAlchemy components. Defines `target_metadata` by importing all SQLAlchemy models from `app.models`. Configures the `context` for offline and online migration modes. The online mode establishes a database connection and uses the `target_metadata` to autogenerate migration differences or to apply scripted migrations.  
**Documentation:**
    
    - **Summary:** Python script that configures the Alembic migration environment. It's executed when Alembic commands are run.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Migration
    
- **Path:** database/postgresql-schema-migrations/script.py.mako  
**Description:** Mako template file used by Alembic to generate new migration script files. Defines the structure of newly created migration scripts.  
**Template:** Mako Template  
**Dependency Level:** 0  
**Name:** script.py  
**Type:** Template  
**Relative Path:** script.py.mako  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alembic Migration Script Template
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To provide a standard template for new Alembic migration files, ensuring consistency.  
**Logic Description:** Contains Mako templating directives to insert revision IDs, creation date, and placeholders for `upgrade` and `downgrade` functions. Imports `alembic.op` and `sqlalchemy.sa`.  
**Documentation:**
    
    - **Summary:** Template used by `alembic revision` command to generate new migration files.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Migration
    
- **Path:** database/postgresql-schema-migrations/app/__init__.py  
**Description:** Initializes the 'app' Python package.  
**Template:** Python Package Initializer  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** app/__init__.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** To mark the 'app' directory as a Python package.  
**Logic Description:** This file can be empty or can contain package-level initializations if needed.  
**Documentation:**
    
    - **Summary:** Makes the 'app' directory a Python package.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** database/postgresql-schema-migrations/app/db/__init__.py  
**Description:** Initializes the 'db' Python sub-package.  
**Template:** Python Package Initializer  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** app/db/__init__.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** To mark the 'db' directory as a Python sub-package.  
**Logic Description:** This file can be empty.  
**Documentation:**
    
    - **Summary:** Makes the 'db' directory a Python sub-package.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.db  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** database/postgresql-schema-migrations/app/db/base.py  
**Description:** Defines the SQLAlchemy declarative base for ORM models. All model classes will inherit from this base.  
**Template:** Python SQLAlchemy Base  
**Dependency Level:** 0  
**Name:** base  
**Type:** Configuration  
**Relative Path:** app/db/base.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** Base  
**Type:** DeclarativeMeta  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - SQLAlchemy Declarative Base Setup
    
**Requirement Ids:**
    
    - Section 7
    
**Purpose:** To provide a common base class for all SQLAlchemy model definitions.  
**Logic Description:** Imports `declarative_base` from `sqlalchemy.ext.declarative`. Creates an instance of `declarative_base()` named `Base`. This `Base` will be imported by all model files.  
**Documentation:**
    
    - **Summary:** Sets up the SQLAlchemy declarative system.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.db  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/__init__.py  
**Description:** Initializes the 'models' Python sub-package and potentially imports all model classes to make them available for Alembic's `target_metadata`.  
**Template:** Python Package Initializer  
**Dependency Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** app/models/__init__.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Aggregation for Alembic
    
**Requirement Ids:**
    
    - Section 7
    - DEP-003
    
**Purpose:** To mark 'models' as a package and ensure all defined SQLAlchemy models are discoverable by Alembic.  
**Logic Description:** Imports all model classes from the individual model files within this directory (e.g., `from .user_model import User`). This allows `env.py` to easily access all models via `app.models.Base.metadata`.  
**Documentation:**
    
    - **Summary:** Makes 'models' a Python package and consolidates model imports for Alembic.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/user_model.py  
**Description:** SQLAlchemy model definition for the 'User' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** user_model  
**Type:** Model  
**Relative Path:** app/models/user_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** email  
**Type:** Column(String(255), unique=True, nullable=False, index=True)  
**Attributes:**   
    - **Name:** passwordHash  
**Type:** Column(String(255))  
**Attributes:**   
    - **Name:** socialProvider  
**Type:** Column(String(50))  
**Attributes:**   
    - **Name:** socialProviderId  
**Type:** Column(String(255))  
**Attributes:**   
    - **Name:** isEmailVerified  
**Type:** Column(Boolean, default=False, nullable=False)  
**Attributes:**   
    - **Name:** subscriptionTier  
**Type:** Column(String(20), default='Free', nullable=False, index=True)  
**Attributes:**   
    - **Name:** creditBalance  
**Type:** Column(Numeric(10, 2), default=0.00, nullable=False)  
**Attributes:**   
    - **Name:** createdAt  
**Type:** Column(DateTime, default=func.now(), nullable=False)  
**Attributes:**   
    - **Name:** updatedAt  
**Type:** Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  
**Attributes:**   
    - **Name:** brand_kits  
**Type:** relationship('BrandKit', back_populates='user')  
**Attributes:**   
    - **Name:** workbenches  
**Type:** relationship('Workbench', back_populates='user')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for User entity
    
**Requirement Ids:**
    
    - Section 7.1.1
    
**Purpose:** To define the structure, columns, types, constraints, and relationships for the 'users' table using SQLAlchemy ORM.  
**Logic Description:** Defines a Python class `User` inheriting from `app.db.base.Base`. Specifies `__tablename__` as 'users'. Defines all columns as per SRS 7.1.1 (id, email, passwordHash, etc.) using `sqlalchemy.Column` with appropriate types (UUID, String, Boolean, DateTime, Numeric) and constraints (primary_key, unique, nullable, default, index). Defines relationships to other models like BrandKit, Workbench, etc., using `sqlalchemy.orm.relationship`.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for the 'users' table, representing user accounts and their attributes.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/brand_kit_model.py  
**Description:** SQLAlchemy model definition for the 'BrandKit' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** brand_kit_model  
**Type:** Model  
**Relative Path:** app/models/brand_kit_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** teamId  
**Type:** Column(UUID, ForeignKey('teams.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** colors  
**Type:** Column(JSONB, nullable=False)  
**Attributes:**   
    - **Name:** fonts  
**Type:** Column(JSONB, nullable=False)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='brand_kits')  
**Attributes:**   
    - **Name:** team  
**Type:** relationship('Team', back_populates='brand_kits')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for BrandKit entity
    
**Requirement Ids:**
    
    - Section 7.1.2
    
**Purpose:** To define the structure for the 'brand_kits' table using SQLAlchemy ORM.  
**Logic Description:** Defines class `BrandKit` inheriting `Base`. Specifies `__tablename__`. Defines columns like `id`, `userId`, `name`, `colors`, `fonts`, `logos` (JSONB for flexible structures). Includes ForeignKeys and relationships.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for brand kits.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/workbench_model.py  
**Description:** SQLAlchemy model definition for the 'Workbench' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** workbench_model  
**Type:** Model  
**Relative Path:** app/models/workbench_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** defaultBrandKitId  
**Type:** Column(UUID, ForeignKey('brand_kits.id'), nullable=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='workbenches')  
**Attributes:**   
    - **Name:** projects  
**Type:** relationship('Project', back_populates='workbench')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Workbench entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-4-001, 4-002)
    
**Purpose:** To define the structure for the 'workbenches' table.  
**Logic Description:** Defines class `Workbench` inheriting `Base`. Defines columns for workbench attributes and relationships to User and Projects.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for workbenches.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/project_model.py  
**Description:** SQLAlchemy model definition for the 'Project' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** project_model  
**Type:** Model  
**Relative Path:** app/models/project_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** workbenchId  
**Type:** Column(UUID, ForeignKey('workbenches.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** templateId  
**Type:** Column(UUID, ForeignKey('templates.id'), nullable=True)  
**Attributes:**   
    - **Name:** brandKitId  
**Type:** Column(UUID, ForeignKey('brand_kits.id'), nullable=True)  
**Attributes:**   
    - **Name:** collaborationState  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** workbench  
**Type:** relationship('Workbench', back_populates='projects')  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='projects')  
**Attributes:**   
    - **Name:** assets  
**Type:** relationship('Asset', back_populates='project')  
**Attributes:**   
    - **Name:** generation_requests  
**Type:** relationship('GenerationRequest', back_populates='project')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Project entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-4-002, 4-010)
    
**Purpose:** To define the structure for the 'projects' table.  
**Logic Description:** Defines class `Project` inheriting `Base`. Defines columns for project attributes and relationships.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for projects.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/asset_model.py  
**Description:** SQLAlchemy model definition for the 'Asset' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** asset_model  
**Type:** Model  
**Relative Path:** app/models/asset_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** projectId  
**Type:** Column(UUID, ForeignKey('projects.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** generationRequestId  
**Type:** Column(UUID, ForeignKey('generation_requests.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(255), nullable=False)  
**Attributes:**   
    - **Name:** type  
**Type:** Column(String(20), nullable=False)  
**Attributes:**   
    - **Name:** filePath  
**Type:** Column(String(1024), nullable=False)  
**Attributes:**   
    - **Name:** project  
**Type:** relationship('Project', back_populates='assets')  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='assets')  
**Attributes:**   
    - **Name:** generation_request_source  
**Type:** relationship('GenerationRequest', foreign_keys='[Asset.generationRequestId]', back_populates='source_asset_if_any')  
**Attributes:**   
    - **Name:** final_generation_output_of  
**Type:** relationship('GenerationRequest', foreign_keys='[GenerationRequest.finalAssetId]', back_populates='final_asset')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Asset entity
    
**Requirement Ids:**
    
    - Section 7.2.1
    
**Purpose:** To define the structure for the 'assets' table.  
**Logic Description:** Defines class `Asset` inheriting `Base`. Defines columns for asset attributes.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for assets.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/asset_version_model.py  
**Description:** SQLAlchemy model definition for the 'AssetVersion' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** asset_version_model  
**Type:** Model  
**Relative Path:** app/models/asset_version_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** assetId  
**Type:** Column(UUID, ForeignKey('assets.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** projectId  
**Type:** Column(UUID, ForeignKey('projects.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** versionNumber  
**Type:** Column(Integer, nullable=False)  
**Attributes:**   
    - **Name:** asset  
**Type:** relationship('Asset', back_populates='versions')  
**Attributes:**   
    - **Name:** project  
**Type:** relationship('Project', back_populates='versions')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AssetVersion entity
    
**Requirement Ids:**
    
    - Section 7.2.1
    
**Purpose:** To define the structure for the 'asset_versions' table.  
**Logic Description:** Defines class `AssetVersion` inheriting `Base`. Defines columns for asset version attributes.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for asset versions.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/generation_request_model.py  
**Description:** SQLAlchemy model definition for the 'GenerationRequest' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** generation_request_model  
**Type:** Model  
**Relative Path:** app/models/generation_request_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** projectId  
**Type:** Column(UUID, ForeignKey('projects.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** inputPrompt  
**Type:** Column(Text, nullable=False)  
**Attributes:**   
    - **Name:** status  
**Type:** Column(String(50), default='Pending', nullable=False, index=True)  
**Attributes:**   
    - **Name:** finalAssetId  
**Type:** Column(UUID, ForeignKey('assets.id'), nullable=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='generation_requests')  
**Attributes:**   
    - **Name:** project  
**Type:** relationship('Project', back_populates='generation_requests')  
**Attributes:**   
    - **Name:** source_asset_if_any  
**Type:** relationship('Asset', foreign_keys='[Asset.generationRequestId]', back_populates='generation_request_source', uselist=False)  
**Attributes:**   
    - **Name:** final_asset  
**Type:** relationship('Asset', foreign_keys='[GenerationRequest.finalAssetId]', back_populates='final_generation_output_of', uselist=False)  
**Attributes:**   
    - **Name:** feedbacks  
**Type:** relationship('AIModelFeedback', back_populates='generation_request')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for GenerationRequest entity
    
**Requirement Ids:**
    
    - Section 7.2.1
    
**Purpose:** To define the structure for the 'generation_requests' table.  
**Logic Description:** Defines class `GenerationRequest` inheriting `Base`. Defines columns for generation request attributes.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI generation requests.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/social_media_connection_model.py  
**Description:** SQLAlchemy model for 'SocialMediaConnection' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** social_media_connection_model  
**Type:** Model  
**Relative Path:** app/models/social_media_connection_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** platform  
**Type:** Column(String(20), nullable=False)  
**Attributes:**   
    - **Name:** externalUserId  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** accessToken  
**Type:** Column(Text, nullable=False)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='social_media_connections')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for SocialMediaConnection entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by SMPIO-007)
    
**Purpose:** To define schema for storing user's social media account connections.  
**Logic Description:** Defines `SocialMediaConnection` model with user ID, platform name, external user ID, and encrypted tokens.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Social Media Connections.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/api_client_model.py  
**Description:** SQLAlchemy model for 'APIClient' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** api_client_model  
**Type:** Model  
**Relative Path:** app/models/api_client_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** apiKey  
**Type:** Column(String(100), unique=True, nullable=False, index=True)  
**Attributes:**   
    - **Name:** secretHash  
**Type:** Column(String(255), nullable=False)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='api_clients')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for APIClient entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-7-002)
    
**Purpose:** To define schema for developer API client credentials.  
**Logic Description:** Defines `APIClient` model with user ID, key name, API key, hashed secret, and status.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for API Clients.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/subscription_model.py  
**Description:** SQLAlchemy model for 'Subscription' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** subscription_model  
**Type:** Model  
**Relative Path:** app/models/subscription_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True, unique=True)  
**Attributes:**   
    - **Name:** odooSaleOrderId  
**Type:** Column(String(255), unique=True, nullable=False, index=True)  
**Attributes:**   
    - **Name:** planId  
**Type:** Column(String(50), nullable=False)  
**Attributes:**   
    - **Name:** status  
**Type:** Column(String(20), default='Active', nullable=False, index=True)  
**Attributes:**   
    - **Name:** currentPeriodEnd  
**Type:** Column(DateTime, nullable=False, index=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='subscription', uselist=False)  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Subscription entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-6-018)
    
**Purpose:** To define schema for user subscription details, synced from Odoo.  
**Logic Description:** Defines `Subscription` model with user ID, Odoo SO ID, plan details, status, and billing period.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Subscriptions.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/credit_transaction_model.py  
**Description:** SQLAlchemy model for 'CreditTransaction' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** credit_transaction_model  
**Type:** Model  
**Relative Path:** app/models/credit_transaction_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** generationRequestId  
**Type:** Column(UUID, ForeignKey('generation_requests.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** amount  
**Type:** Column(Numeric(10,2), nullable=False)  
**Attributes:**   
    - **Name:** actionType  
**Type:** Column(String(50), nullable=False, index=True)  
**Attributes:**   
    - **Name:** createdAt  
**Type:** Column(DateTime, default=func.now(), nullable=False, index=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='credit_transactions')  
**Attributes:**   
    - **Name:** generation_request  
**Type:** relationship('GenerationRequest', back_populates='credit_transactions')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for CreditTransaction entity
    
**Requirement Ids:**
    
    - Section 7.3.1 (related)
    
**Purpose:** To define schema for credit usage and purchase records.  
**Logic Description:** Defines `CreditTransaction` model with user ID, related request/API call, amount, type, and timestamp.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Credit Transactions.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/usage_log_model.py  
**Description:** SQLAlchemy model for 'UsageLog' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** usage_log_model  
**Type:** Model  
**Relative Path:** app/models/usage_log_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(BigInteger, primary_key=True, autoincrement=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** actionType  
**Type:** Column(String(100), nullable=False, index=True)  
**Attributes:**   
    - **Name:** details  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** timestamp  
**Type:** Column(DateTime, default=func.now(), nullable=False, index=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='usage_logs')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for UsageLog entity
    
**Requirement Ids:**
    
    - Section 7.3.1
    
**Purpose:** To define schema for detailed logging of billable or trackable user actions.  
**Logic Description:** Defines `UsageLog` model with user ID, action type, contextual details, and timestamp.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Usage Logs.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/team_model.py  
**Description:** SQLAlchemy model definition for the 'Team' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** team_model  
**Type:** Model  
**Relative Path:** app/models/team_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** ownerId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** owner  
**Type:** relationship('User', back_populates='owned_teams')  
**Attributes:**   
    - **Name:** members  
**Type:** relationship('TeamMember', back_populates='team')  
**Attributes:**   
    - **Name:** brand_kits  
**Type:** relationship('BrandKit', back_populates='team')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Team entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-003, UAPM-1-010)
    
**Purpose:** To define the structure for the 'teams' table.  
**Logic Description:** Defines class `Team` inheriting `Base`. Defines columns for team attributes and relationships.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for teams.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/team_member_model.py  
**Description:** SQLAlchemy model definition for the 'TeamMember' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** team_member_model  
**Type:** Model  
**Relative Path:** app/models/team_member_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** teamId  
**Type:** Column(UUID, ForeignKey('teams.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** role  
**Type:** Column(String(20), nullable=False, index=True)  
**Attributes:**   
    - **Name:** team  
**Type:** relationship('Team', back_populates='members')  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='team_memberships')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for TeamMember entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by REQ-003, UAPM-1-010)
    
**Purpose:** To define the structure for the 'team_members' table.  
**Logic Description:** Defines class `TeamMember` inheriting `Base`. Junction table for Users and Teams with a role.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for team memberships.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/session_model.py  
**Description:** SQLAlchemy model for 'Session' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** session_model  
**Type:** Model  
**Relative Path:** app/models/session_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** deviceInfo  
**Type:** Column(String(255), nullable=False)  
**Attributes:**   
    - **Name:** ipAddress  
**Type:** Column(String(45), nullable=False)  
**Attributes:**   
    - **Name:** lastActivity  
**Type:** Column(DateTime, default=func.now(), nullable=False, index=True)  
**Attributes:**   
    - **Name:** expiresAt  
**Type:** Column(DateTime, nullable=False, index=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='sessions')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Session entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by UAPM-1-008, REQ-2-006)
    
**Purpose:** To define schema for user authentication sessions.  
**Logic Description:** Defines `Session` model with user ID, device info, IP, activity, and expiration.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for user Sessions.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/notification_model.py  
**Description:** SQLAlchemy model for 'Notification' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** notification_model  
**Type:** Model  
**Relative Path:** app/models/notification_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** type  
**Type:** Column(String(50), nullable=False)  
**Attributes:**   
    - **Name:** message  
**Type:** Column(Text, nullable=False)  
**Attributes:**   
    - **Name:** isRead  
**Type:** Column(Boolean, default=False, nullable=False, index=True)  
**Attributes:**   
    - **Name:** createdAt  
**Type:** Column(DateTime, default=func.now(), nullable=False, index=True)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='notifications')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Notification entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by various notification needs)
    
**Purpose:** To define schema for system notifications for users.  
**Logic Description:** Defines `Notification` model with user ID, type, message, read status, and timestamps.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Notifications.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/template_model.py  
**Description:** SQLAlchemy model for 'Template' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** template_model  
**Type:** Model  
**Relative Path:** app/models/template_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), nullable=False)  
**Attributes:**   
    - **Name:** category  
**Type:** Column(String(50), nullable=False, index=True)  
**Attributes:**   
    - **Name:** previewUrl  
**Type:** Column(String(1024), nullable=False)  
**Attributes:**   
    - **Name:** sourceData  
**Type:** Column(JSONB, nullable=False)  
**Attributes:**   
    - **Name:** tags  
**Type:** Column(JSONB)  
**Attributes:**   
    - **Name:** isPublic  
**Type:** Column(Boolean, default=True, nullable=False)  
**Attributes:**   
    - **Name:** user_creator  
**Type:** relationship('User', back_populates='created_templates')  
**Attributes:**   
    - **Name:** projects_using_template  
**Type:** relationship('Project', back_populates='template')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for Template entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by UI-003, REQ-4-003)
    
**Purpose:** To define schema for predefined or user-saved creative templates.  
**Logic Description:** Defines `Template` model with creator ID (optional), name, category, preview, source data, and public status.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for Templates.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/ai_model_model.py  
**Description:** SQLAlchemy model for 'AIModel' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_model  
**Type:** Model  
**Relative Path:** app/models/ai_model_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** name  
**Type:** Column(String(100), unique=True, nullable=False, index=True)  
**Attributes:**   
    - **Name:** provider  
**Type:** Column(String(50), nullable=False)  
**Attributes:**   
    - **Name:** taskType  
**Type:** Column(String(50), nullable=False, index=True)  
**Attributes:**   
    - **Name:** isActive  
**Type:** Column(Boolean, default=True, nullable=False, index=True)  
**Attributes:**   
    - **Name:** versions  
**Type:** relationship('AIModelVersion', back_populates='ai_model_parent')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AIModel entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by INT-007)
    
**Purpose:** To define schema for metadata of AI models available on the platform.  
**Logic Description:** Defines `AIModel` model with name, provider, task type, and active status.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI Models.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/ai_model_version_model.py  
**Description:** SQLAlchemy model for 'AIModelVersion' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_version_model  
**Type:** Model  
**Relative Path:** app/models/ai_model_version_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** modelId  
**Type:** Column(UUID, ForeignKey('ai_models.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** versionNumber  
**Type:** Column(String(50), nullable=False)  
**Attributes:**   
    - **Name:** status  
**Type:** Column(String(50), default='Staged', nullable=False, index=True)  
**Attributes:**   
    - **Name:** validationResultId  
**Type:** Column(UUID, ForeignKey('ai_model_validation_results.id'), nullable=True)  
**Attributes:**   
    - **Name:** ai_model_parent  
**Type:** relationship('AIModel', back_populates='versions')  
**Attributes:**   
    - **Name:** validation_result  
**Type:** relationship('AIModelValidationResult', back_populates='model_version', uselist=False)  
**Attributes:**   
    - **Name:** deployments  
**Type:** relationship('AIModelDeployment', back_populates='model_version')  
**Attributes:**   
    - **Name:** feedbacks  
**Type:** relationship('AIModelFeedback', back_populates='model_version')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AIModelVersion entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by INT-007)
    
**Purpose:** To define schema for specific versions of AI models.  
**Logic Description:** Defines `AIModelVersion` model with model ID, version number, source path, status, and links to validation/deployment.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI Model Versions.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/ai_model_validation_result_model.py  
**Description:** SQLAlchemy model for 'AIModelValidationResult' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_validation_result_model  
**Type:** Model  
**Relative Path:** app/models/ai_model_validation_result_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** modelVersionId  
**Type:** Column(UUID, ForeignKey('ai_model_versions.id'), nullable=False, unique=True, index=True)  
**Attributes:**   
    - **Name:** validationTimestamp  
**Type:** Column(DateTime, default=func.now(), nullable=False)  
**Attributes:**   
    - **Name:** securityScanStatus  
**Type:** Column(String(50), nullable=False)  
**Attributes:**   
    - **Name:** model_version  
**Type:** relationship('AIModelVersion', back_populates='validation_result', uselist=False)  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AIModelValidationResult entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by INT-007)
    
**Purpose:** To define schema for results from validating an AI model version.  
**Logic Description:** Defines `AIModelValidationResult` model with version ID, timestamp, and status of various validation checks.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI Model Validation Results.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/ai_model_deployment_model.py  
**Description:** SQLAlchemy model for 'AIModelDeployment' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_deployment_model  
**Type:** Model  
**Relative Path:** app/models/ai_model_deployment_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** modelVersionId  
**Type:** Column(UUID, ForeignKey('ai_model_versions.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** environment  
**Type:** Column(String(50), nullable=False, index=True)  
**Attributes:**   
    - **Name:** status  
**Type:** Column(String(50), default='Initiated', nullable=False, index=True)  
**Attributes:**   
    - **Name:** model_version  
**Type:** relationship('AIModelVersion', back_populates='deployments')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AIModelDeployment entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by INT-007)
    
**Purpose:** To define schema for recording AI model version deployments.  
**Logic Description:** Defines `AIModelDeployment` model with version ID, environment, status, and deployment details.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI Model Deployments.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/app/models/ai_model_feedback_model.py  
**Description:** SQLAlchemy model for 'AIModelFeedback' table.  
**Template:** Python SQLAlchemy Model  
**Dependency Level:** 1  
**Name:** ai_model_feedback_model  
**Type:** Model  
**Relative Path:** app/models/ai_model_feedback_model.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** __tablename__  
**Type:** str  
**Attributes:** class variable  
    - **Name:** id  
**Type:** Column(UUID, primary_key=True)  
**Attributes:**   
    - **Name:** userId  
**Type:** Column(UUID, ForeignKey('users.id'), nullable=False, index=True)  
**Attributes:**   
    - **Name:** generationRequestId  
**Type:** Column(UUID, ForeignKey('generation_requests.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** modelVersionId  
**Type:** Column(UUID, ForeignKey('ai_model_versions.id'), nullable=True, index=True)  
**Attributes:**   
    - **Name:** rating  
**Type:** Column(Integer)  
**Attributes:**   
    - **Name:** comment  
**Type:** Column(Text)  
**Attributes:**   
    - **Name:** user  
**Type:** relationship('User', back_populates='ai_model_feedbacks')  
**Attributes:**   
    - **Name:** generation_request  
**Type:** relationship('GenerationRequest', back_populates='feedbacks')  
**Attributes:**   
    - **Name:** model_version  
**Type:** relationship('AIModelVersion', back_populates='feedbacks')  
**Attributes:**   
    
**Methods:**
    
    - **Name:** __repr__  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - Schema definition for AIModelFeedback entity
    
**Requirement Ids:**
    
    - Section 7 (Implied by INT-007)
    
**Purpose:** To define schema for user feedback on outputs from specific AI models.  
**Logic Description:** Defines `AIModelFeedback` model with user ID, request ID, model version, rating, and comments.  
**Documentation:**
    
    - **Summary:** SQLAlchemy ORM model for AI Model Feedback.
    
**Namespace:** CreativeFlow.Data.PostgreSQL.Schema.app.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** database/postgresql-schema-migrations/versions/0001_create_initial_tables.py  
**Description:** Alembic migration script for creating initial set of tables (e.g., users, brand_kits, workbenches, projects, etc.).  
**Template:** Python Alembic Migration Script  
**Dependency Level:** 2  
**Name:** 0001_create_initial_tables  
**Type:** MigrationScript  
**Relative Path:** versions/0001_create_initial_tables.py  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** upgrade  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** downgrade  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Initial schema creation for core tables
    
**Requirement Ids:**
    
    - Section 7
    - DEP-003
    
**Purpose:** To apply the initial database schema for multiple core entities as defined by their SQLAlchemy models.  
**Logic Description:** The `upgrade` function will contain `alembic.op.create_table()` calls for User, BrandKit, Workbench, Project, Asset, AssetVersion, GenerationRequest, SocialMediaConnection, APIClient, Subscription, CreditTransaction, UsageLog, Team, TeamMember, Session, Notification, Template, AIModel, AIModelVersion, AIModelValidationResult, AIModelDeployment, and AIModelFeedback tables. Each `create_table` call will define columns, constraints (PK, FK, Unique, Check), and indexes based on the corresponding SQLAlchemy model definitions in `app.models`. The `downgrade` function will contain corresponding `alembic.op.drop_table()` calls in reverse order of creation.  
**Documentation:**
    
    - **Summary:** Alembic migration to create the foundational tables of the CreativeFlow AI database.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Migration
    
- **Path:** database/postgresql-schema-migrations/ddl/tables/001_create_users.sql  
**Description:** DDL script for creating the 'users' table. Provides a raw SQL representation of the table schema.  
**Template:** SQL DDL Script  
**Dependency Level:** 0  
**Name:** 001_create_users  
**Type:** DDLScript  
**Relative Path:** ddl/tables/001_create_users.sql  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DDL for User table
    
**Requirement Ids:**
    
    - Section 7.1.1
    
**Purpose:** To define the 'users' table schema using raw SQL DDL.  
**Logic Description:** Contains a `CREATE TABLE users (...)` statement. Defines columns (id UUID PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, passwordHash VARCHAR(255), etc.) with their data types, primary key, unique constraints, not null constraints, default values, and any explicit CHECK constraints as specified in SRS 7.1.1. Separate CREATE INDEX statements for indexed columns might follow.  
**Documentation:**
    
    - **Summary:** Raw SQL DDL for creating the 'users' table.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DDL
    
- **Path:** database/postgresql-schema-migrations/ddl/tables/002_create_brand_kits.sql  
**Description:** DDL script for creating the 'brand_kits' table.  
**Template:** SQL DDL Script  
**Dependency Level:** 1  
**Name:** 002_create_brand_kits  
**Type:** DDLScript  
**Relative Path:** ddl/tables/002_create_brand_kits.sql  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DDL for BrandKit table
    
**Requirement Ids:**
    
    - Section 7.1.2
    
**Purpose:** To define the 'brand_kits' table schema using raw SQL DDL.  
**Logic Description:** Contains a `CREATE TABLE brand_kits (...)` statement. Defines columns like id, userId (FOREIGN KEY REFERENCES users(id)), name, colors JSONB, fonts JSONB. Includes PK, FKs.  
**Documentation:**
    
    - **Summary:** Raw SQL DDL for creating the 'brand_kits' table.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DDL
    
- **Path:** database/postgresql-schema-migrations/docs/diagrams/creativeflow_ai_erd.png  
**Description:** Main Entity Relationship Diagram (ERD) for the CreativeFlow AI PostgreSQL database.  
**Template:** Image  
**Dependency Level:** 3  
**Name:** creativeflow_ai_erd  
**Type:** Documentation  
**Relative Path:** docs/diagrams/creativeflow_ai_erd.png  
**Repository Id:** REPO-POSTGRESQL-SCHEMA-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Database Schema Visualization
    
**Requirement Ids:**
    
    - Appendix B
    
**Purpose:** To provide a visual representation of the database schema, tables, columns, and relationships.  
**Logic Description:** This is an image file (e.g., PNG, SVG) generated from a diagramming tool, depicting the overall database structure. It should be kept in sync with schema changes.  
**Documentation:**
    
    - **Summary:** Visual ERD of the primary database schema.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - sqlalchemy.url (in alembic.ini)
  


---

