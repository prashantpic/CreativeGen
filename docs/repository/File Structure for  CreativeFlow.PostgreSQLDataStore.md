# Specification

# 1. Files

- **Path:** src/schema/tables/User.sql  
**Description:** Defines the schema for the 'User' table, storing registered user account details, authentication information, preferences, and subscription status. Includes fields for email, password hash, social login details, email verification, profile information, MFA settings, subscription tier, and credit balance. Designed with caching considerations for frequently accessed fields.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 0  
**Name:** User  
**Type:** Schema  
**Relative Path:** schema/tables/User.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Account Storage
    - Authentication Fields
    - Profile Preferences
    - Subscription Tier Tracking
    - Credit Balance Storage
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.1.1
    
**Purpose:** To persist core user account data, enabling authentication, personalization, and access control based on subscription.  
**Logic Description:** Contains the CREATE TABLE statement for 'User'. Defines columns like id (UUID, PK), email (VARCHAR, UNIQUE), passwordHash, socialProvider, isEmailVerified, fullName, username (UNIQUE), profilePictureUrl, languagePreference, timezone, mfaEnabled, mfaSecret, subscriptionTier, creditBalance, lastLoginAt, createdAt, updatedAt, deletedAt. Includes CHECK constraints for socialProvider and subscriptionTier. Specifies indexes for email, username, subscriptionTier, and socialProvider details.  
**Documentation:**
    
    - **Summary:** SQL script for creating the User table and its associated constraints and indexes.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/BrandKit.sql  
**Description:** Defines the schema for the 'BrandKit' table, storing brand assets (colors, fonts, logos) and preferences for users or teams.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** BrandKit  
**Type:** Schema  
**Relative Path:** schema/tables/BrandKit.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Brand Asset Storage
    - Default Brand Kit Flag
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.1.2
    
**Purpose:** To store collections of brand assets that users can apply to their creative projects.  
**Logic Description:** Contains the CREATE TABLE statement for 'BrandKit'. Defines columns like id (UUID, PK), userId (UUID, FK to User), teamId (UUID, FK to Team, nullable), name (VARCHAR), colors (JSONB), fonts (JSONB), logos (JSONB), stylePreferences (JSONB), isDefault (BOOLEAN), createdAt, updatedAt. Includes GIN indexes for JSONB fields (colors, fonts).  
**Documentation:**
    
    - **Summary:** SQL script for creating the BrandKit table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Workbench.sql  
**Description:** Defines the schema for the 'Workbench' table, acting as a container for creative projects.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Workbench  
**Type:** Schema  
**Relative Path:** schema/tables/Workbench.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Organization
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To allow users to organize their creative projects into logical groups.  
**Logic Description:** Contains the CREATE TABLE statement for 'Workbench'. Defines columns like id (UUID, PK), userId (UUID, FK to User), name (VARCHAR), defaultBrandKitId (UUID, FK to BrandKit, nullable), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Workbench table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Project.sql  
**Description:** Defines the schema for the 'Project' table, representing individual creative projects.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 2  
**Name:** Project  
**Type:** Schema  
**Relative Path:** schema/tables/Project.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Creative Project Storage
    - Collaboration State
    - Brand Kit Association
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To store details and state for user's creative projects, including collaboration aspects.  
**Logic Description:** Contains the CREATE TABLE statement for 'Project'. Defines columns like id (UUID, PK), workbenchId (UUID, FK to Workbench), userId (UUID, FK to User), templateId (UUID, FK to Template, nullable), brandKitId (UUID, FK to BrandKit, nullable), name (VARCHAR), targetPlatform (VARCHAR), collaborationState (JSONB), lastCollaboratedAt (DateTime), createdAt, updatedAt, deletedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Project table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Asset.sql  
**Description:** Defines the schema for the 'Asset' table, representing uploaded or AI-generated creative asset files.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 3  
**Name:** Asset  
**Type:** Schema  
**Relative Path:** schema/tables/Asset.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Metadata Storage
    - Link to MinIO Path
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.2.1
    
**Purpose:** To store metadata for all creative assets, whether user-uploaded or AI-generated.  
**Logic Description:** Contains the CREATE TABLE statement for 'Asset'. Defines columns like id (UUID, PK), projectId (UUID, FK to Project, nullable), userId (UUID, FK to User), generationRequestId (UUID, FK to GenerationRequest, nullable), name (VARCHAR), type (VARCHAR), filePath (VARCHAR for MinIO path), mimeType (VARCHAR), format (VARCHAR), resolution (VARCHAR), isFinal (BOOLEAN), metadata (JSONB), createdAt, updatedAt, deletedAt. Includes CHECK constraint for asset type.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Asset table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AssetVersion.sql  
**Description:** Defines the schema for the 'AssetVersion' table, tracking version history for assets or project states.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 4  
**Name:** AssetVersion  
**Type:** Schema  
**Relative Path:** schema/tables/AssetVersion.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Versioning
    - Project State Versioning
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.2.1
    
**Purpose:** To maintain a history of changes to creative assets or project states.  
**Logic Description:** Contains the CREATE TABLE statement for 'AssetVersion'. Defines columns like id (UUID, PK), assetId (UUID, FK to Asset, nullable), projectId (UUID, FK to Project, nullable), versionNumber (INTEGER), filePath (VARCHAR, MinIO path, nullable), stateData (JSONB, nullable), description (TEXT), createdByUserId (UUID, FK to User, nullable), createdAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the AssetVersion table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/GenerationRequest.sql  
**Description:** Defines the schema for the 'GenerationRequest' table, storing details of AI creative generation requests and their outcomes.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 2  
**Name:** GenerationRequest  
**Type:** Schema  
**Relative Path:** schema/tables/GenerationRequest.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Generation Tracking
    - Status Management
    - Credit Cost Logging
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.2.1
    
**Purpose:** To track AI generation tasks, their inputs, status, outputs, and associated costs.  
**Logic Description:** Contains the CREATE TABLE statement for 'GenerationRequest'. Defines columns like id (UUID, PK), userId (UUID, FK to User), projectId (UUID, FK to Project), inputPrompt (TEXT), styleGuidance (TEXT), inputParameters (JSONB), status (VARCHAR, with CHECK constraint), errorMessage (TEXT), sampleAssets (JSONB), selectedSampleId (UUID), finalAssetId (UUID, FK to Asset, nullable), creditsCostSample (DECIMAL), creditsCostFinal (DECIMAL), aiModelUsed (VARCHAR), processingTimeMs (INTEGER), createdAt, updatedAt. Includes indexes on status and createdAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the GenerationRequest table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/SocialMediaConnection.sql  
**Description:** Defines the schema for the 'SocialMediaConnection' table, storing user's connected social media account details and OAuth tokens.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** SocialMediaConnection  
**Type:** Schema  
**Relative Path:** schema/tables/SocialMediaConnection.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Social Media Account Linking
    - Secure OAuth Token Storage
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To manage user connections to external social media platforms for content publishing.  
**Logic Description:** Contains the CREATE TABLE statement for 'SocialMediaConnection'. Defines columns like id (UUID, PK), userId (UUID, FK to User), platform (VARCHAR, with CHECK constraint), externalUserId (VARCHAR), accessToken (TEXT, encrypted), refreshToken (TEXT, encrypted, nullable), expiresAt (DateTime), createdAt, updatedAt. Includes a UNIQUE constraint on (userId, platform).  
**Documentation:**
    
    - **Summary:** SQL script for creating the SocialMediaConnection table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/APIClient.sql  
**Description:** Defines the schema for the 'APIClient' table, storing API access credentials (keys and hashed secrets) for developer users.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** APIClient  
**Type:** Schema  
**Relative Path:** schema/tables/APIClient.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Key Management
    - Secure Secret Storage
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To manage API keys for third-party integrations and programmatic access.  
**Logic Description:** Contains the CREATE TABLE statement for 'APIClient'. Defines columns like id (UUID, PK), userId (UUID, FK to User), name (VARCHAR), apiKey (VARCHAR, UNIQUE), secretHash (VARCHAR), permissions (JSONB), isActive (BOOLEAN), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the APIClient table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Subscription.sql  
**Description:** Defines the schema for the 'Subscription' table, storing user subscription details, typically synced from Odoo.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Subscription  
**Type:** Schema  
**Relative Path:** schema/tables/Subscription.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Subscription Plan Tracking
    - Billing Cycle Management
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To maintain a local cache or reference of user subscription status and details for quick access.  
**Logic Description:** Contains the CREATE TABLE statement for 'Subscription'. Defines columns like id (UUID, PK), userId (UUID, FK to User), odooSaleOrderId (VARCHAR, UNIQUE), planId (VARCHAR), status (VARCHAR, with CHECK constraint), currentPeriodStart (DateTime), currentPeriodEnd (DateTime), paymentProvider (VARCHAR), paymentProviderSubscriptionId (VARCHAR), paymentMethodId (VARCHAR), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Subscription table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/CreditTransaction.sql  
**Description:** Defines the schema for the 'CreditTransaction' table, recording credit purchases and usage, often synced from Odoo.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 4  
**Name:** CreditTransaction  
**Type:** Schema  
**Relative Path:** schema/tables/CreditTransaction.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Usage Tracking
    - Credit Purchase Logging
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.3.1
    
**Purpose:** To provide an audit trail for all credit-related transactions.  
**Logic Description:** Contains the CREATE TABLE statement for 'CreditTransaction'. Defines columns like id (UUID, PK), userId (UUID, FK to User), odooInvoiceId (VARCHAR, nullable), generationRequestId (UUID, FK to GenerationRequest, nullable), apiClientId (UUID, FK to APIClient, nullable), amount (DECIMAL), actionType (VARCHAR), description (TEXT), createdAt, syncedAt. Suggests RANGE partitioning on createdAt for performance on large datasets as per databaseDesign notes.  
**Documentation:**
    
    - **Summary:** SQL script for creating the CreditTransaction table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/UsageLog.sql  
**Description:** Defines the schema for the 'UsageLog' table, providing a detailed log of billable or otherwise trackable user actions.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 4  
**Name:** UsageLog  
**Type:** Schema  
**Relative Path:** schema/tables/UsageLog.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Action Logging
    - Feature Usage Tracking
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    - Section 7.3.1
    
**Purpose:** To log user interactions and system events for analytics, billing, and auditing.  
**Logic Description:** Contains the CREATE TABLE statement for 'UsageLog'. Defines columns like id (BIGSERIAL, PK), userId (UUID, FK to User), generationRequestId (UUID, FK to GenerationRequest, nullable), apiClientId (UUID, FK to APIClient, nullable), actionType (VARCHAR), details (JSONB), creditsCost (DECIMAL, nullable), timestamp (DateTime).  
**Documentation:**
    
    - **Summary:** SQL script for creating the UsageLog table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Team.sql  
**Description:** Defines the schema for the 'Team' table, representing collaboration groups for team accounts.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Team  
**Type:** Schema  
**Relative Path:** schema/tables/Team.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Team Entity Storage
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To store information about teams created within the platform.  
**Logic Description:** Contains the CREATE TABLE statement for 'Team'. Defines columns like id (UUID, PK), name (VARCHAR), ownerId (UUID, FK to User), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Team table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/TeamMember.sql  
**Description:** Defines the schema for the 'TeamMember' table, associating users with teams and their roles within those teams.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 2  
**Name:** TeamMember  
**Type:** Schema  
**Relative Path:** schema/tables/TeamMember.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Team Membership Management
    - Role Assignment
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To manage the relationship between users and teams, including their roles.  
**Logic Description:** Contains the CREATE TABLE statement for 'TeamMember'. Defines columns like id (UUID, PK), teamId (UUID, FK to Team), userId (UUID, FK to User), role (VARCHAR, with CHECK constraint), joinedAt (DateTime). Includes a UNIQUE constraint on (teamId, userId).  
**Documentation:**
    
    - **Summary:** SQL script for creating the TeamMember table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Session.sql  
**Description:** Defines the schema for the 'Session' table, storing active user authentication sessions.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Session  
**Type:** Schema  
**Relative Path:** schema/tables/Session.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Session Tracking
    - Device Information Logging
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To manage user sessions for authentication and activity tracking.  
**Logic Description:** Contains the CREATE TABLE statement for 'Session'. Defines columns like id (UUID, PK), userId (UUID, FK to User), deviceInfo (VARCHAR), ipAddress (VARCHAR), userAgent (TEXT), lastActivity (DateTime), expiresAt (DateTime), createdAt. Includes indexes for efficient querying and cleanup.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Session table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Notification.sql  
**Description:** Defines the schema for the 'Notification' table, storing system-generated notifications for users.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Notification  
**Type:** Schema  
**Relative Path:** schema/tables/Notification.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Notification Storage
    - Read Status Tracking
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To store and manage notifications sent to users regarding platform events.  
**Logic Description:** Contains the CREATE TABLE statement for 'Notification'. Defines columns like id (UUID, PK), userId (UUID, FK to User), type (VARCHAR), message (TEXT), metadata (JSONB), isRead (BOOLEAN), createdAt, updatedAt. Includes partial index for unread notifications. Suggests RANGE partitioning on createdAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Notification table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/Template.sql  
**Description:** Defines the schema for the 'Template' table, storing predefined system templates and user-saved private templates.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** Template  
**Type:** Schema  
**Relative Path:** schema/tables/Template.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Creative Template Storage
    - Template Categorization and Tagging
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To provide a library of reusable creative templates.  
**Logic Description:** Contains the CREATE TABLE statement for 'Template'. Defines columns like id (UUID, PK), userId (UUID, FK to User, nullable for system templates), name (VARCHAR), description (TEXT), category (VARCHAR), previewUrl (VARCHAR), sourceData (JSONB), tags (JSONB), isPublic (BOOLEAN), createdAt, updatedAt. Includes GIN index for tags.  
**Documentation:**
    
    - **Summary:** SQL script for creating the Template table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AIModel.sql  
**Description:** Defines the schema for the 'AIModel' table, storing metadata about AI models available on the platform.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 0  
**Name:** AIModel  
**Type:** Schema  
**Relative Path:** schema/tables/AIModel.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Registry Core
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To catalog available AI models, their providers, and intended tasks.  
**Logic Description:** Contains the CREATE TABLE statement for 'AIModel'. Defines columns like id (UUID, PK), name (VARCHAR, UNIQUE), description (TEXT), provider (VARCHAR), taskType (VARCHAR, with CHECK constraint), isActive (BOOLEAN), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the AIModel table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AIModelVersion.sql  
**Description:** Defines the schema for the 'AIModelVersion' table, tracking specific versions of AI models.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 1  
**Name:** AIModelVersion  
**Type:** Schema  
**Relative Path:** schema/tables/AIModelVersion.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Versioning
    - Link to Validation Results
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To manage different versions of AI models, their source, and lifecycle status.  
**Logic Description:** Contains the CREATE TABLE statement for 'AIModelVersion'. Defines columns like id (UUID, PK), modelId (UUID, FK to AIModel), versionNumber (VARCHAR), sourcePath (VARCHAR, nullable), format (VARCHAR, nullable), parameters (JSONB), status (VARCHAR, with CHECK constraint), validationResultId (UUID, FK to AIModelValidationResult, nullable), createdByUserId (UUID, FK to User, nullable), releaseNotes (TEXT), createdAt, updatedAt. Includes UNIQUE constraint on (modelId, versionNumber).  
**Documentation:**
    
    - **Summary:** SQL script for creating the AIModelVersion table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AIModelValidationResult.sql  
**Description:** Defines the schema for the 'AIModelValidationResult' table, storing results from validating AI model versions.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 2  
**Name:** AIModelValidationResult  
**Type:** Schema  
**Relative Path:** schema/tables/AIModelValidationResult.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Validation Logging
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To record the outcomes of security, functional, and performance validation for AI models.  
**Logic Description:** Contains the CREATE TABLE statement for 'AIModelValidationResult'. Defines columns like id (UUID, PK), modelVersionId (UUID, FK to AIModelVersion), validationTimestamp (DateTime), securityScanStatus (VARCHAR), functionalStatus (VARCHAR), performanceBenchmark (JSONB), results (JSONB), validatedByUserId (UUID, FK to User, nullable), createdAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the AIModelValidationResult table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AIModelDeployment.sql  
**Description:** Defines the schema for the 'AIModelDeployment' table, recording deployments of AI model versions to various environments.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 2  
**Name:** AIModelDeployment  
**Type:** Schema  
**Relative Path:** schema/tables/AIModelDeployment.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Deployment Tracking
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To track the deployment status and history of AI models across different environments.  
**Logic Description:** Contains the CREATE TABLE statement for 'AIModelDeployment'. Defines columns like id (UUID, PK), modelVersionId (UUID, FK to AIModelVersion), environment (VARCHAR), status (VARCHAR), deploymentStrategy (VARCHAR), endpoint (VARCHAR), kubernetesDetails (JSONB), deployedByUserId (UUID, FK to User, nullable), deploymentTimestamp (DateTime), createdAt, updatedAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the AIModelDeployment table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/tables/AIModelFeedback.sql  
**Description:** Defines the schema for the 'AIModelFeedback' table, storing user feedback on outputs from specific AI models.  
**Template:** PostgreSQL Table DDL  
**Dependency Level:** 3  
**Name:** AIModelFeedback  
**Type:** Schema  
**Relative Path:** schema/tables/AIModelFeedback.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Output Feedback Collection
    
**Requirement Ids:**
    
    - Section 7 (Data Requirements)
    
**Purpose:** To capture user ratings and comments on the quality of AI-generated content.  
**Logic Description:** Contains the CREATE TABLE statement for 'AIModelFeedback'. Defines columns like id (UUID, PK), userId (UUID, FK to User), generationRequestId (UUID, FK to GenerationRequest, nullable), modelVersionId (UUID, FK to AIModelVersion, nullable), rating (INTEGER, nullable), comment (TEXT, nullable), feedbackTimestamp (DateTime), details (JSONB), createdAt.  
**Documentation:**
    
    - **Summary:** SQL script for creating the AIModelFeedback table.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/schema/indexes/CustomIndexes.sql  
**Description:** Defines custom or performance-critical GIN/GiST indexes not included in table DDLs, for fields like JSONB or full-text search capabilities.  
**Template:** PostgreSQL Index DDL  
**Dependency Level:** 5  
**Name:** CustomIndexes  
**Type:** Schema  
**Relative Path:** schema/indexes/CustomIndexes.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Performance Optimization via Indexing
    
**Requirement Ids:**
    
    - NFR-005
    
**Purpose:** To enhance query performance on specific columns or data types.  
**Logic Description:** Contains CREATE INDEX statements for GIN indexes on BrandKit.colors, BrandKit.fonts, Template.tags as specified in the databaseDesign. May include other performance-critical indexes identified during development.  
**Documentation:**
    
    - **Summary:** SQL script for creating custom GIN/GiST indexes.
    
**Namespace:** CreativeFlow.Data.Schema  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/migrations/V001__Initial_Schema.sql  
**Description:** Flyway migration script to create the initial database schema, including all tables, primary keys, foreign keys, basic indexes, and constraints.  
**Template:** Flyway SQL Migration  
**Dependency Level:** 6  
**Name:** V001__Initial_Schema  
**Type:** Migration  
**Relative Path:** migrations/V001__Initial_Schema.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Database Schema Initialization
    
**Requirement Ids:**
    
    - DEP-003
    - Section 7 (Data Requirements)
    
**Purpose:** To set up the complete initial database structure for the CreativeFlow AI platform.  
**Logic Description:** Combines or references all DDL scripts from 'src/schema/tables/' to create the full schema. Ensures correct order of table creation to satisfy foreign key dependencies. This script should be idempotent if possible for initial setup scenarios.  
**Documentation:**
    
    - **Summary:** Initial Flyway migration script that creates all tables and their relationships.
    
**Namespace:** CreativeFlow.Data.Migrations  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/migrations/V002__Add_User_Preferences_Detail.sql  
**Description:** Example Flyway migration script to add a new JSONB column 'ui_settings' to the 'User' table for more detailed UI preferences.  
**Template:** Flyway SQL Migration  
**Dependency Level:** 7  
**Name:** V002__Add_User_Preferences_Detail  
**Type:** Migration  
**Relative Path:** migrations/V002__Add_User_Preferences_Detail.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Schema Evolution Example
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To demonstrate an incremental schema change using Flyway.  
**Logic Description:** Contains an ALTER TABLE statement to add the 'ui_settings' JSONB column to the 'User' table. This is an example of how future schema changes will be managed.  
**Documentation:**
    
    - **Summary:** Example Flyway migration script illustrating a schema alteration.
    
**Namespace:** CreativeFlow.Data.Migrations  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/seeds/01_Initial_Admin_User.sql  
**Description:** SQL script to seed an initial administrative user account. To be run after initial schema setup. Ensure password is a placeholder or managed securely if used in automated seeding.  
**Template:** SQL Seed Script  
**Dependency Level:** 7  
**Name:** 01_Initial_Admin_User  
**Type:** Seed  
**Relative Path:** seeds/01_Initial_Admin_User.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Initial Admin Account Setup
    
**Requirement Ids:**
    
    - Section 11.4.2 (Initial Data Seeding)
    
**Purpose:** To create a default administrator account for initial platform access.  
**Logic Description:** Contains INSERT INTO User statement to create an admin user. Password hash should be for a known temporary password or managed via environment variables for seeding.  
**Documentation:**
    
    - **Summary:** Seeds an initial admin user.
    
**Namespace:** CreativeFlow.Data.Seeds  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** src/seeds/02_Default_Templates.sql  
**Description:** SQL script to seed default creative templates into the 'Template' table. To be run after initial schema setup.  
**Template:** SQL Seed Script  
**Dependency Level:** 7  
**Name:** 02_Default_Templates  
**Type:** Seed  
**Relative Path:** seeds/02_Default_Templates.sql  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Initial Template Population
    
**Requirement Ids:**
    
    - Section 11.4.2 (Initial Data Seeding)
    
**Purpose:** To populate the platform with an initial set of creative templates.  
**Logic Description:** Contains multiple INSERT INTO Template statements for system-provided templates. 'sourceData' would be JSON structures. 'previewUrl' would point to pre-uploaded MinIO paths or placeholders.  
**Documentation:**
    
    - **Summary:** Seeds default templates.
    
**Namespace:** CreativeFlow.Data.Seeds  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** config/flyway.conf.example  
**Description:** Example configuration file for Flyway database migration tool, demonstrating connection parameters and migration script locations. Actual secrets should be managed externally.  
**Template:** Configuration File  
**Dependency Level:** 0  
**Name:** flyway.conf.example  
**Type:** Configuration  
**Relative Path:** config/flyway.conf.example  
**Repository Id:** REPO-POSTGRES-DB-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Migration Tool Configuration
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To guide the setup of Flyway for database migrations.  
**Logic Description:** Key-value pairs for Flyway settings. Includes flyway.url, flyway.user, flyway.password (as placeholder), flyway.schemas, flyway.locations (pointing to src/migrations), flyway.baselineOnMigrate, flyway.baselineVersion.  
**Documentation:**
    
    - **Summary:** Example Flyway configuration. Sensitive values like passwords should be injected via environment variables or a secrets manager in CI/CD.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DataAccess
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - POSTGRES_HOST
  - POSTGRES_PORT
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - FLYWAY_LOCATIONS
  - FLYWAY_SCHEMAS
  - FLYWAY_BASELINE_VERSION
  - FLYWAY_BASELINE_ON_MIGRATE
  


---

