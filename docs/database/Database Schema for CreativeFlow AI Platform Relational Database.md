# Specification

# 1. Database Design

## 1.1. User
Represents a registered user account. Caching strategy: Cache fullName, subscriptionTier, languagePreference, timezone, creditBalance in a suitable caching layer (e.g., Redis); invalidate cache on updates to these fields.

### 1.1.3. Attributes

### 1.1.3.1. id
#### 1.1.3.1.2. Type
UUID

#### 1.1.3.1.3. Is Required
True

#### 1.1.3.1.4. Is Primary Key
True

### 1.1.3.2. email
#### 1.1.3.2.2. Type
VARCHAR

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Size
255

#### 1.1.3.2.5. Is Unique
True

### 1.1.3.3. passwordHash
#### 1.1.3.3.2. Type
VARCHAR

#### 1.1.3.3.3. Is Required
False

#### 1.1.3.3.4. Size
255

#### 1.1.3.3.5. Security

- **Hash:** True

#### 1.1.3.3.6. Notes
Required if using email/password authentication.

### 1.1.3.4. socialProvider
#### 1.1.3.4.2. Type
VARCHAR

#### 1.1.3.4.3. Is Required
False

#### 1.1.3.4.4. Size
50

#### 1.1.3.4.5. Constraints

- CHECK (socialProvider IN ('google', 'facebook', 'apple'))

#### 1.1.3.4.6. Notes
Used if signed up via social login.

### 1.1.3.5. socialProviderId
#### 1.1.3.5.2. Type
VARCHAR

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
255

#### 1.1.3.5.5. Notes
Unique ID from the social provider.

### 1.1.3.6. isEmailVerified
#### 1.1.3.6.2. Type
BOOLEAN

#### 1.1.3.6.3. Is Required
True

#### 1.1.3.6.4. Default Value
false

### 1.1.3.7. emailVerificationToken
#### 1.1.3.7.2. Type
VARCHAR

#### 1.1.3.7.3. Is Required
False

#### 1.1.3.7.4. Size
255

#### 1.1.3.7.5. Notes
Token for email verification process.

### 1.1.3.8. passwordResetToken
#### 1.1.3.8.2. Type
VARCHAR

#### 1.1.3.8.3. Is Required
False

#### 1.1.3.8.4. Size
255

#### 1.1.3.8.5. Notes
Token for password reset process.

### 1.1.3.9. passwordResetExpires
#### 1.1.3.9.2. Type
DateTime

#### 1.1.3.9.3. Is Required
False

#### 1.1.3.9.4. Notes
Expiration timestamp for password reset token.

### 1.1.3.10. fullName
#### 1.1.3.10.2. Type
VARCHAR

#### 1.1.3.10.3. Is Required
False

#### 1.1.3.10.4. Size
100

### 1.1.3.11. username
#### 1.1.3.11.2. Type
VARCHAR

#### 1.1.3.11.3. Is Required
False

#### 1.1.3.11.4. Size
50

#### 1.1.3.11.5. Is Unique
True

### 1.1.3.12. profilePictureUrl
#### 1.1.3.12.2. Type
VARCHAR

#### 1.1.3.12.3. Is Required
False

#### 1.1.3.12.4. Size
1024

### 1.1.3.13. languagePreference
#### 1.1.3.13.2. Type
VARCHAR

#### 1.1.3.13.3. Is Required
True

#### 1.1.3.13.4. Size
10

#### 1.1.3.13.5. Default Value
'en-US'

#### 1.1.3.13.6. Indexed
True

### 1.1.3.14. timezone
#### 1.1.3.14.2. Type
VARCHAR

#### 1.1.3.14.3. Is Required
True

#### 1.1.3.14.4. Size
50

#### 1.1.3.14.5. Default Value
'UTC'

### 1.1.3.15. mfaEnabled
#### 1.1.3.15.2. Type
BOOLEAN

#### 1.1.3.15.3. Is Required
True

#### 1.1.3.15.4. Default Value
false

### 1.1.3.16. mfaSecret
#### 1.1.3.16.2. Type
VARCHAR

#### 1.1.3.16.3. Is Required
False

#### 1.1.3.16.4. Size
255

#### 1.1.3.16.5. Security

- **Encryption:** True

#### 1.1.3.16.6. Notes
For authenticator apps (e.g., TOTP).

### 1.1.3.17. subscriptionTier
#### 1.1.3.17.2. Type
VARCHAR

#### 1.1.3.17.3. Is Required
True

#### 1.1.3.17.4. Size
20

#### 1.1.3.17.5. Default Value
'Free'

#### 1.1.3.17.6. Constraints

- CHECK (subscriptionTier IN ('Free','Pro','Team','Enterprise'))

#### 1.1.3.17.7. Indexed
True

### 1.1.3.18. creditBalance
#### 1.1.3.18.2. Type
DECIMAL

#### 1.1.3.18.3. Is Required
True

#### 1.1.3.18.4. Precision
10

#### 1.1.3.18.5. Scale
2

#### 1.1.3.18.6. Default Value
0.00

#### 1.1.3.18.7. Notes
Synced from Odoo, stored here for quick access.

### 1.1.3.19. lastLoginAt
#### 1.1.3.19.2. Type
DateTime

#### 1.1.3.19.3. Is Required
False

### 1.1.3.20. createdAt
#### 1.1.3.20.2. Type
DateTime

#### 1.1.3.20.3. Is Required
True

#### 1.1.3.20.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.21. updatedAt
#### 1.1.3.21.2. Type
DateTime

#### 1.1.3.21.3. Is Required
True

#### 1.1.3.21.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.22. deletedAt
#### 1.1.3.22.2. Type
DateTime

#### 1.1.3.22.3. Is Required
False

#### 1.1.3.22.4. Notes
Timestamp for soft delete.


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints

### 1.1.5.1. uq_user_email
#### 1.1.5.1.2. Columns

- email

### 1.1.5.2. uq_user_username
#### 1.1.5.2.2. Columns

- username

### 1.1.5.3. uq_user_social
#### 1.1.5.3.2. Columns

- socialProvider
- socialProviderId

#### 1.1.5.3.3. Condition
socialProvider IS NOT NULL AND socialProviderId IS NOT NULL


### 1.1.6. Indexes

### 1.1.6.1. idx_user_email_unique
#### 1.1.6.1.2. Columns

- email

#### 1.1.6.1.3. Type
BTree

#### 1.1.6.1.4. Is Unique
True

### 1.1.6.2. idx_user_username_unique
#### 1.1.6.2.2. Columns

- username

#### 1.1.6.2.3. Type
BTree

#### 1.1.6.2.4. Is Unique
True

#### 1.1.6.2.5. Condition
username IS NOT NULL

### 1.1.6.3. idx_user_social_unique
#### 1.1.6.3.2. Columns

- socialProvider
- socialProviderId

#### 1.1.6.3.3. Type
BTree

#### 1.1.6.3.4. Is Unique
True

#### 1.1.6.3.5. Condition
socialProvider IS NOT NULL AND socialProviderId IS NOT NULL

### 1.1.6.4. idx_user_subscriptiontier
#### 1.1.6.4.2. Columns

- subscriptionTier

#### 1.1.6.4.3. Type
BTree

### 1.1.6.5. idx_user_deletedat
#### 1.1.6.5.2. Columns

- deletedAt

#### 1.1.6.5.3. Type
BTree

#### 1.1.6.5.4. Condition
deletedAt IS NOT NULL


## 1.2. BrandKit
Collection of brand assets and preferences. Can belong to a user or a team.

### 1.2.3. Attributes

### 1.2.3.1. id
#### 1.2.3.1.2. Type
UUID

#### 1.2.3.1.3. Is Required
True

#### 1.2.3.1.4. Is Primary Key
True

### 1.2.3.2. userId
#### 1.2.3.2.2. Type
UUID

#### 1.2.3.2.3. Is Required
True

#### 1.2.3.2.4. Is Foreign Key
True

#### 1.2.3.2.5. Notes
User who owns this brand kit. For team brand kits, this might be the creator or the owning team's owner.

#### 1.2.3.2.6. On Delete
CASCADE

#### 1.2.3.2.7. On Update
NO ACTION

### 1.2.3.3. teamId
#### 1.2.3.3.2. Type
UUID

#### 1.2.3.3.3. Is Required
False

#### 1.2.3.3.4. Is Foreign Key
True

#### 1.2.3.3.5. Notes
Optional: Team this brand kit belongs to.

#### 1.2.3.3.6. On Delete
CASCADE

#### 1.2.3.3.7. On Update
NO ACTION

### 1.2.3.4. name
#### 1.2.3.4.2. Type
VARCHAR

#### 1.2.3.4.3. Is Required
True

#### 1.2.3.4.4. Size
100

### 1.2.3.5. colors
#### 1.2.3.5.2. Type
JSONB

#### 1.2.3.5.3. Is Required
True

#### 1.2.3.5.4. Notes
JSON array of color definitions, e.g., [{ "name": "Primary", "hex": "#FF0000", "variable": "--color-primary" }].

### 1.2.3.6. fonts
#### 1.2.3.6.2. Type
JSONB

#### 1.2.3.6.3. Is Required
True

#### 1.2.3.6.4. Notes
JSON array of font definitions, e.g., [{ "name": "Heading", "family": "Arial", "url": "..." }].

### 1.2.3.7. logos
#### 1.2.3.7.2. Type
JSONB

#### 1.2.3.7.3. Is Required
False

#### 1.2.3.7.4. Notes
JSON array of logo asset references (MinIO paths), e.g., [{ "name": "Main Logo", "path": "minio_path", "format": "png" }].

### 1.2.3.8. stylePreferences
#### 1.2.3.8.2. Type
JSONB

#### 1.2.3.8.3. Is Required
False

#### 1.2.3.8.4. Notes
JSON object for default style preferences like tone, industry hints etc.

### 1.2.3.9. isDefault
#### 1.2.3.9.2. Type
BOOLEAN

#### 1.2.3.9.3. Is Required
True

#### 1.2.3.9.4. Default Value
false

### 1.2.3.10. createdAt
#### 1.2.3.10.2. Type
DateTime

#### 1.2.3.10.3. Is Required
True

#### 1.2.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.2.3.11. updatedAt
#### 1.2.3.11.2. Type
DateTime

#### 1.2.3.11.3. Is Required
True

#### 1.2.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.2.4. Primary Keys

- id

### 1.2.5. Unique Constraints


### 1.2.6. Indexes

### 1.2.6.1. idx_brandkit_userid
#### 1.2.6.1.2. Columns

- userId

#### 1.2.6.1.3. Type
BTree

### 1.2.6.2. idx_brandkit_teamid
#### 1.2.6.2.2. Columns

- teamId

#### 1.2.6.2.3. Type
BTree

### 1.2.6.3. idx_brandkit_colors_gin
#### 1.2.6.3.2. Columns

- colors

#### 1.2.6.3.3. Type
GIN

### 1.2.6.4. idx_brandkit_fonts_gin
#### 1.2.6.4.2. Columns

- fonts

#### 1.2.6.4.3. Type
GIN


## 1.3. Workbench
Container for organizing creative projects.

### 1.3.3. Attributes

### 1.3.3.1. id
#### 1.3.3.1.2. Type
UUID

#### 1.3.3.1.3. Is Required
True

#### 1.3.3.1.4. Is Primary Key
True

### 1.3.3.2. userId
#### 1.3.3.2.2. Type
UUID

#### 1.3.3.2.3. Is Required
True

#### 1.3.3.2.4. Is Foreign Key
True

#### 1.3.3.2.5. On Delete
CASCADE

#### 1.3.3.2.6. On Update
NO ACTION

### 1.3.3.3. name
#### 1.3.3.3.2. Type
VARCHAR

#### 1.3.3.3.3. Is Required
True

#### 1.3.3.3.4. Size
100

### 1.3.3.4. defaultBrandKitId
#### 1.3.3.4.2. Type
UUID

#### 1.3.3.4.3. Is Required
False

#### 1.3.3.4.4. Is Foreign Key
True

#### 1.3.3.4.5. Notes
Optional default brand kit for new projects in this workbench.

#### 1.3.3.4.6. On Delete
SET NULL

#### 1.3.3.4.7. On Update
CASCADE

### 1.3.3.5. createdAt
#### 1.3.3.5.2. Type
DateTime

#### 1.3.3.5.3. Is Required
True

#### 1.3.3.5.4. Default Value
CURRENT_TIMESTAMP

### 1.3.3.6. updatedAt
#### 1.3.3.6.2. Type
DateTime

#### 1.3.3.6.3. Is Required
True

#### 1.3.3.6.4. Default Value
CURRENT_TIMESTAMP


### 1.3.4. Primary Keys

- id

### 1.3.5. Unique Constraints


### 1.3.6. Indexes

### 1.3.6.1. idx_workbench_userid
#### 1.3.6.1.2. Columns

- userId

#### 1.3.6.1.3. Type
BTree


## 1.4. Project
Creative project containing assets and generation requests.

### 1.4.3. Attributes

### 1.4.3.1. id
#### 1.4.3.1.2. Type
UUID

#### 1.4.3.1.3. Is Required
True

#### 1.4.3.1.4. Is Primary Key
True

### 1.4.3.2. workbenchId
#### 1.4.3.2.2. Type
UUID

#### 1.4.3.2.3. Is Required
True

#### 1.4.3.2.4. Is Foreign Key
True

#### 1.4.3.2.5. On Delete
CASCADE

#### 1.4.3.2.6. On Update
NO ACTION

### 1.4.3.3. userId
#### 1.4.3.3.2. Type
UUID

#### 1.4.3.3.3. Is Required
True

#### 1.4.3.3.4. Is Foreign Key
True

#### 1.4.3.3.5. On Delete
CASCADE

#### 1.4.3.3.6. On Update
NO ACTION

#### 1.4.3.3.7. Notes
Denormalized from Workbench for query performance. Application logic should ensure consistency with Workbench.userId.

### 1.4.3.4. templateId
#### 1.4.3.4.2. Type
UUID

#### 1.4.3.4.3. Is Required
False

#### 1.4.3.4.4. Is Foreign Key
True

#### 1.4.3.4.5. On Delete
SET NULL

#### 1.4.3.4.6. On Update
NO ACTION

### 1.4.3.5. brandKitId
#### 1.4.3.5.2. Type
UUID

#### 1.4.3.5.3. Is Required
False

#### 1.4.3.5.4. Is Foreign Key
True

#### 1.4.3.5.5. Notes
Optional brand kit override for this project.

#### 1.4.3.5.6. On Delete
SET NULL

#### 1.4.3.5.7. On Update
CASCADE

### 1.4.3.6. name
#### 1.4.3.6.2. Type
VARCHAR

#### 1.4.3.6.3. Is Required
True

#### 1.4.3.6.4. Size
100

### 1.4.3.7. targetPlatform
#### 1.4.3.7.2. Type
VARCHAR

#### 1.4.3.7.3. Is Required
False

#### 1.4.3.7.4. Size
50

#### 1.4.3.7.5. Notes
Primary target platform for this project, e.g., 'InstagramStory', 'TikTok'.

### 1.4.3.8. collaborationState
#### 1.4.3.8.2. Type
JSONB

#### 1.4.3.8.3. Is Required
False

#### 1.4.3.8.4. Notes
JSON representation of the creative canvas state, potentially using CRDT representation for collaborative projects.

### 1.4.3.9. lastCollaboratedAt
#### 1.4.3.9.2. Type
DateTime

#### 1.4.3.9.3. Is Required
False

#### 1.4.3.9.4. Notes
Timestamp of the last change in a collaborative session.

### 1.4.3.10. createdAt
#### 1.4.3.10.2. Type
DateTime

#### 1.4.3.10.3. Is Required
True

#### 1.4.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.4.3.11. updatedAt
#### 1.4.3.11.2. Type
DateTime

#### 1.4.3.11.3. Is Required
True

#### 1.4.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.4.3.12. deletedAt
#### 1.4.3.12.2. Type
DateTime

#### 1.4.3.12.3. Is Required
False

#### 1.4.3.12.4. Notes
Timestamp for soft delete.


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints


### 1.4.6. Indexes

### 1.4.6.1. idx_project_workbenchid
#### 1.4.6.1.2. Columns

- workbenchId

#### 1.4.6.1.3. Type
BTree

### 1.4.6.2. idx_project_userid
#### 1.4.6.2.2. Columns

- userId

#### 1.4.6.2.3. Type
BTree

### 1.4.6.3. idx_project_updatedat
#### 1.4.6.3.2. Columns

- updatedAt

#### 1.4.6.3.3. Type
BTree


## 1.5. Asset
Represents a specific creative asset file (uploaded or AI-generated).

### 1.5.3. Attributes

### 1.5.3.1. id
#### 1.5.3.1.2. Type
UUID

#### 1.5.3.1.3. Is Required
True

#### 1.5.3.1.4. Is Primary Key
True

### 1.5.3.2. projectId
#### 1.5.3.2.2. Type
UUID

#### 1.5.3.2.3. Is Required
False

#### 1.5.3.2.4. Is Foreign Key
True

#### 1.5.3.2.5. On Delete
SET NULL

#### 1.5.3.2.6. On Update
NO ACTION

#### 1.5.3.2.7. Notes
Asset can exist independently of a project (e.g., uploaded to user library).

### 1.5.3.3. userId
#### 1.5.3.3.2. Type
UUID

#### 1.5.3.3.3. Is Required
True

#### 1.5.3.3.4. Is Foreign Key
True

#### 1.5.3.3.5. On Delete
CASCADE

#### 1.5.3.3.6. On Update
NO ACTION

#### 1.5.3.3.7. Notes
Owner of the asset.

### 1.5.3.4. generationRequestId
#### 1.5.3.4.2. Type
UUID

#### 1.5.3.4.3. Is Required
False

#### 1.5.3.4.4. Is Foreign Key
True

#### 1.5.3.4.5. On Delete
SET NULL

#### 1.5.3.4.6. On Update
NO ACTION

#### 1.5.3.4.7. Notes
Link to the generation request if this asset was AI-generated.

### 1.5.3.5. name
#### 1.5.3.5.2. Type
VARCHAR

#### 1.5.3.5.3. Is Required
True

#### 1.5.3.5.4. Size
255

### 1.5.3.6. type
#### 1.5.3.6.2. Type
VARCHAR

#### 1.5.3.6.3. Is Required
True

#### 1.5.3.6.4. Size
20

#### 1.5.3.6.5. Constraints

- CHECK (type IN ('Uploaded','AIGenerated','Derived'))

#### 1.5.3.6.6. Notes
'Derived' for assets created by editing existing ones.

### 1.5.3.7. filePath
#### 1.5.3.7.2. Type
VARCHAR

#### 1.5.3.7.3. Is Required
True

#### 1.5.3.7.4. Size
1024

#### 1.5.3.7.5. Notes
Path in MinIO object storage.

### 1.5.3.8. mimeType
#### 1.5.3.8.2. Type
VARCHAR

#### 1.5.3.8.3. Is Required
True

#### 1.5.3.8.4. Size
50

### 1.5.3.9. format
#### 1.5.3.9.2. Type
VARCHAR

#### 1.5.3.9.3. Is Required
True

#### 1.5.3.9.4. Size
10

### 1.5.3.10. resolution
#### 1.5.3.10.2. Type
VARCHAR

#### 1.5.3.10.3. Is Required
False

#### 1.5.3.10.4. Size
20

#### 1.5.3.10.5. Notes
e.g., '1920x1080', '512x512'. Might be null for non-image assets.

### 1.5.3.11. isFinal
#### 1.5.3.11.2. Type
BOOLEAN

#### 1.5.3.11.3. Is Required
True

#### 1.5.3.11.4. Default Value
false

#### 1.5.3.11.5. Notes
True if this is the user-selected final asset from a generation or a completed edited version.

### 1.5.3.12. metadata
#### 1.5.3.12.2. Type
JSONB

#### 1.5.3.12.3. Is Required
False

#### 1.5.3.12.4. Notes
Optional metadata (e.g., dominant colors, tags, source generation parameters if AI-generated).

### 1.5.3.13. createdAt
#### 1.5.3.13.2. Type
DateTime

#### 1.5.3.13.3. Is Required
True

#### 1.5.3.13.4. Default Value
CURRENT_TIMESTAMP

### 1.5.3.14. updatedAt
#### 1.5.3.14.2. Type
DateTime

#### 1.5.3.14.3. Is Required
True

#### 1.5.3.14.4. Default Value
CURRENT_TIMESTAMP

### 1.5.3.15. deletedAt
#### 1.5.3.15.2. Type
DateTime

#### 1.5.3.15.3. Is Required
False

#### 1.5.3.15.4. Notes
Timestamp for soft delete.


### 1.5.4. Primary Keys

- id

### 1.5.5. Unique Constraints


### 1.5.6. Indexes

### 1.5.6.1. idx_asset_projectid_createdat
#### 1.5.6.1.2. Columns

- projectId
- createdAt

#### 1.5.6.1.3. Type
BTree

### 1.5.6.2. idx_asset_userid
#### 1.5.6.2.2. Columns

- userId

#### 1.5.6.2.3. Type
BTree

### 1.5.6.3. idx_asset_generationrequestid
#### 1.5.6.3.2. Columns

- generationRequestId

#### 1.5.6.3.3. Type
BTree

### 1.5.6.4. idx_asset_type
#### 1.5.6.4.2. Columns

- type

#### 1.5.6.4.3. Type
BTree


## 1.6. AssetVersion
Version history for creative assets or project states.

### 1.6.3. Attributes

### 1.6.3.1. id
#### 1.6.3.1.2. Type
UUID

#### 1.6.3.1.3. Is Required
True

#### 1.6.3.1.4. Is Primary Key
True

### 1.6.3.2. assetId
#### 1.6.3.2.2. Type
UUID

#### 1.6.3.2.3. Is Required
False

#### 1.6.3.2.4. Is Foreign Key
True

#### 1.6.3.2.5. On Delete
SET NULL

#### 1.6.3.2.6. On Update
NO ACTION

#### 1.6.3.2.7. Notes
Link to the parent Asset this version belongs to.

### 1.6.3.3. projectId
#### 1.6.3.3.2. Type
UUID

#### 1.6.3.3.3. Is Required
False

#### 1.6.3.3.4. Is Foreign Key
True

#### 1.6.3.3.5. On Delete
CASCADE

#### 1.6.3.3.6. On Update
NO ACTION

#### 1.6.3.3.7. Notes
Link to the Project this version belongs to (could be a project state version).

### 1.6.3.4. versionNumber
#### 1.6.3.4.2. Type
INTEGER

#### 1.6.3.4.3. Is Required
True

### 1.6.3.5. filePath
#### 1.6.3.5.2. Type
VARCHAR

#### 1.6.3.5.3. Is Required
False

#### 1.6.3.5.4. Size
1024

#### 1.6.3.5.5. Notes
Path in MinIO object storage if this version saves a specific file state.

### 1.6.3.6. stateData
#### 1.6.3.6.2. Type
JSONB

#### 1.6.3.6.3. Is Required
False

#### 1.6.3.6.4. Notes
JSON data representing the project or asset state at this version point.

### 1.6.3.7. description
#### 1.6.3.7.2. Type
TEXT

#### 1.6.3.7.3. Is Required
False

### 1.6.3.8. createdByUserId
#### 1.6.3.8.2. Type
UUID

#### 1.6.3.8.3. Is Required
False

#### 1.6.3.8.4. Is Foreign Key
True

#### 1.6.3.8.5. On Delete
SET NULL

#### 1.6.3.8.6. On Update
NO ACTION

#### 1.6.3.8.7. Notes
User who created this version.

### 1.6.3.9. createdAt
#### 1.6.3.9.2. Type
DateTime

#### 1.6.3.9.3. Is Required
True

#### 1.6.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.6.4. Primary Keys

- id

### 1.6.5. Unique Constraints


### 1.6.6. Indexes

### 1.6.6.1. idx_assetversion_assetid
#### 1.6.6.1.2. Columns

- assetId

#### 1.6.6.1.3. Type
BTree

### 1.6.6.2. idx_assetversion_projectid
#### 1.6.6.2.2. Columns

- projectId

#### 1.6.6.2.3. Type
BTree

### 1.6.6.3. idx_assetversion_assetid_version
#### 1.6.6.3.2. Columns

- assetId
- versionNumber

#### 1.6.6.3.3. Type
BTree

### 1.6.6.4. idx_assetversion_projectid_version
#### 1.6.6.4.2. Columns

- projectId
- versionNumber

#### 1.6.6.4.3. Type
BTree


## 1.7. GenerationRequest
AI creative generation request details and results.

### 1.7.3. Attributes

### 1.7.3.1. id
#### 1.7.3.1.2. Type
UUID

#### 1.7.3.1.3. Is Required
True

#### 1.7.3.1.4. Is Primary Key
True

### 1.7.3.2. userId
#### 1.7.3.2.2. Type
UUID

#### 1.7.3.2.3. Is Required
True

#### 1.7.3.2.4. Is Foreign Key
True

#### 1.7.3.2.5. On Delete
RESTRICT

#### 1.7.3.2.6. On Update
NO ACTION

#### 1.7.3.2.7. Notes
Restrict user deletion if requests exist for audit/billing.

### 1.7.3.3. projectId
#### 1.7.3.3.2. Type
UUID

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Is Foreign Key
True

#### 1.7.3.3.5. On Delete
SET NULL

#### 1.7.3.3.6. On Update
NO ACTION

### 1.7.3.4. inputPrompt
#### 1.7.3.4.2. Type
TEXT

#### 1.7.3.4.3. Is Required
True

### 1.7.3.5. styleGuidance
#### 1.7.3.5.2. Type
TEXT

#### 1.7.3.5.3. Is Required
False

### 1.7.3.6. inputParameters
#### 1.7.3.6.2. Type
JSONB

#### 1.7.3.6.3. Is Required
False

#### 1.7.3.6.4. Notes
JSON object including format, resolution hints, input assets references, etc.

### 1.7.3.7. status
#### 1.7.3.7.2. Type
VARCHAR

#### 1.7.3.7.3. Is Required
True

#### 1.7.3.7.4. Size
50

#### 1.7.3.7.5. Default Value
'Pending'

#### 1.7.3.7.6. Constraints

- CHECK (status IN ('Pending','ProcessingSamples','AwaitingSelection','ProcessingFinal','Completed','Failed','Cancelled','ContentRejected'))

#### 1.7.3.7.7. Indexed
True

### 1.7.3.8. errorMessage
#### 1.7.3.8.2. Type
TEXT

#### 1.7.3.8.3. Is Required
False

#### 1.7.3.8.4. Notes
Details if status is 'Failed' or 'ContentRejected'.

### 1.7.3.9. sampleAssets
#### 1.7.3.9.2. Type
JSONB

#### 1.7.3.9.3. Is Required
False

#### 1.7.3.9.4. Notes
JSON array of sample asset metadata (e.g., [{ 'id': 'asset_uuid_ref', 'url': 'minio_path', 'resolution': '512x512' }]). Reference to Asset entity.

### 1.7.3.10. selectedSampleId
#### 1.7.3.10.2. Type
UUID

#### 1.7.3.10.3. Is Required
False

#### 1.7.3.10.4. Notes
ID of the selected sample from sampleAssets for final generation (references Asset entity).

### 1.7.3.11. finalAssetId
#### 1.7.3.11.2. Type
UUID

#### 1.7.3.11.3. Is Required
False

#### 1.7.3.11.4. Is Foreign Key
True

#### 1.7.3.11.5. On Delete
SET NULL

#### 1.7.3.11.6. On Update
NO ACTION

#### 1.7.3.11.7. Notes
Link to the final generated Asset entity.

### 1.7.3.12. creditsCostSample
#### 1.7.3.12.2. Type
DECIMAL

#### 1.7.3.12.3. Is Required
False

#### 1.7.3.12.4. Precision
10

#### 1.7.3.12.5. Scale
2

#### 1.7.3.12.6. Notes
Credits cost for sample generation phase.

### 1.7.3.13. creditsCostFinal
#### 1.7.3.13.2. Type
DECIMAL

#### 1.7.3.13.3. Is Required
False

#### 1.7.3.13.4. Precision
10

#### 1.7.3.13.5. Scale
2

#### 1.7.3.13.6. Notes
Credits cost for final generation phase.

### 1.7.3.14. aiModelUsed
#### 1.7.3.14.2. Type
VARCHAR

#### 1.7.3.14.3. Is Required
False

#### 1.7.3.14.4. Size
100

#### 1.7.3.14.5. Notes
Identifier of the AI model or workflow used.

### 1.7.3.15. processingTimeMs
#### 1.7.3.15.2. Type
INTEGER

#### 1.7.3.15.3. Is Required
False

#### 1.7.3.15.4. Notes
Total time taken for the generation process in milliseconds.

### 1.7.3.16. createdAt
#### 1.7.3.16.2. Type
DateTime

#### 1.7.3.16.3. Is Required
True

#### 1.7.3.16.4. Default Value
CURRENT_TIMESTAMP

#### 1.7.3.16.5. Indexed
True

### 1.7.3.17. updatedAt
#### 1.7.3.17.2. Type
DateTime

#### 1.7.3.17.3. Is Required
True

#### 1.7.3.17.4. Default Value
CURRENT_TIMESTAMP


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints


### 1.7.6. Indexes

### 1.7.6.1. idx_generationrequest_userid
#### 1.7.6.1.2. Columns

- userId

#### 1.7.6.1.3. Type
BTree

### 1.7.6.2. idx_generationrequest_projectid
#### 1.7.6.2.2. Columns

- projectId

#### 1.7.6.2.3. Type
BTree

### 1.7.6.3. idx_generationrequest_status_createdat
#### 1.7.6.3.2. Columns

- status
- createdAt

#### 1.7.6.3.3. Type
BTree


## 1.8. SocialMediaConnection
User's connected social media accounts.

### 1.8.3. Attributes

### 1.8.3.1. id
#### 1.8.3.1.2. Type
UUID

#### 1.8.3.1.3. Is Required
True

#### 1.8.3.1.4. Is Primary Key
True

### 1.8.3.2. userId
#### 1.8.3.2.2. Type
UUID

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

#### 1.8.3.2.5. On Delete
CASCADE

#### 1.8.3.2.6. On Update
NO ACTION

### 1.8.3.3. platform
#### 1.8.3.3.2. Type
VARCHAR

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Size
20

#### 1.8.3.3.5. Constraints

- CHECK (platform IN ('Instagram','Facebook','LinkedIn','Twitter','Pinterest','TikTok'))

### 1.8.3.4. externalUserId
#### 1.8.3.4.2. Type
VARCHAR

#### 1.8.3.4.3. Is Required
True

#### 1.8.3.4.4. Size
100

#### 1.8.3.4.5. Notes
User ID on the social media platform.

### 1.8.3.5. accessToken
#### 1.8.3.5.2. Type
TEXT

#### 1.8.3.5.3. Is Required
True

#### 1.8.3.5.4. Security

- **Encryption:** True

#### 1.8.3.5.5. Notes
OAuth token for accessing the platform API, encrypted at rest.

### 1.8.3.6. refreshToken
#### 1.8.3.6.2. Type
TEXT

#### 1.8.3.6.3. Is Required
False

#### 1.8.3.6.4. Security

- **Encryption:** True

#### 1.8.3.6.5. Notes
OAuth refresh token, encrypted at rest.

### 1.8.3.7. expiresAt
#### 1.8.3.7.2. Type
DateTime

#### 1.8.3.7.3. Is Required
False

#### 1.8.3.7.4. Notes
Expiration timestamp for the access token.

### 1.8.3.8. createdAt
#### 1.8.3.8.2. Type
DateTime

#### 1.8.3.8.3. Is Required
True

#### 1.8.3.8.4. Default Value
CURRENT_TIMESTAMP

### 1.8.3.9. updatedAt
#### 1.8.3.9.2. Type
DateTime

#### 1.8.3.9.3. Is Required
True

#### 1.8.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints

### 1.8.5.1. uq_socialconnection_user_platform
#### 1.8.5.1.2. Columns

- userId
- platform


### 1.8.6. Indexes

### 1.8.6.1. idx_socialconnection_userid_platform
#### 1.8.6.1.2. Columns

- userId
- platform

#### 1.8.6.1.3. Type
BTree


## 1.9. APIClient
API access credentials for developers.

### 1.9.3. Attributes

### 1.9.3.1. id
#### 1.9.3.1.2. Type
UUID

#### 1.9.3.1.3. Is Required
True

#### 1.9.3.1.4. Is Primary Key
True

### 1.9.3.2. userId
#### 1.9.3.2.2. Type
UUID

#### 1.9.3.2.3. Is Required
True

#### 1.9.3.2.4. Is Foreign Key
True

#### 1.9.3.2.5. On Delete
CASCADE

#### 1.9.3.2.6. On Update
NO ACTION

### 1.9.3.3. name
#### 1.9.3.3.2. Type
VARCHAR

#### 1.9.3.3.3. Is Required
True

#### 1.9.3.3.4. Size
100

#### 1.9.3.3.5. Notes
User-defined name for the API key.

### 1.9.3.4. apiKey
#### 1.9.3.4.2. Type
VARCHAR

#### 1.9.3.4.3. Is Required
True

#### 1.9.3.4.4. Size
100

#### 1.9.3.4.5. Is Unique
True

#### 1.9.3.4.6. Notes
Public API key identifier.

### 1.9.3.5. secretHash
#### 1.9.3.5.2. Type
VARCHAR

#### 1.9.3.5.3. Is Required
True

#### 1.9.3.5.4. Size
255

#### 1.9.3.5.5. Security

- **Hash:** True

#### 1.9.3.5.6. Notes
Hashed API secret.

### 1.9.3.6. permissions
#### 1.9.3.6.2. Type
JSONB

#### 1.9.3.6.3. Is Required
False

#### 1.9.3.6.4. Notes
JSON object defining granular permissions for this key.

### 1.9.3.7. isActive
#### 1.9.3.7.2. Type
BOOLEAN

#### 1.9.3.7.3. Is Required
True

#### 1.9.3.7.4. Default Value
true

### 1.9.3.8. createdAt
#### 1.9.3.8.2. Type
DateTime

#### 1.9.3.8.3. Is Required
True

#### 1.9.3.8.4. Default Value
CURRENT_TIMESTAMP

### 1.9.3.9. updatedAt
#### 1.9.3.9.2. Type
DateTime

#### 1.9.3.9.3. Is Required
True

#### 1.9.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints

### 1.9.5.1. uq_apiclient_apikey
#### 1.9.5.1.2. Columns

- apiKey


### 1.9.6. Indexes

### 1.9.6.1. idx_apiclient_apikey_unique
#### 1.9.6.1.2. Columns

- apiKey

#### 1.9.6.1.3. Type
BTree

#### 1.9.6.1.4. Is Unique
True

### 1.9.6.2. idx_apiclient_userid
#### 1.9.6.2.2. Columns

- userId

#### 1.9.6.2.3. Type
BTree


## 1.10. Subscription
User subscription details, synced with Odoo.

### 1.10.3. Attributes

### 1.10.3.1. id
#### 1.10.3.1.2. Type
UUID

#### 1.10.3.1.3. Is Required
True

#### 1.10.3.1.4. Is Primary Key
True

### 1.10.3.2. userId
#### 1.10.3.2.2. Type
UUID

#### 1.10.3.2.3. Is Required
True

#### 1.10.3.2.4. Is Foreign Key
True

#### 1.10.3.2.5. On Delete
CASCADE

#### 1.10.3.2.6. On Update
NO ACTION

### 1.10.3.3. odooSaleOrderId
#### 1.10.3.3.2. Type
VARCHAR

#### 1.10.3.3.3. Is Required
True

#### 1.10.3.3.4. Size
255

#### 1.10.3.3.5. Is Unique
True

#### 1.10.3.3.6. Notes
Reference to the Odoo Sale Order/Subscription record.

### 1.10.3.4. planId
#### 1.10.3.4.2. Type
VARCHAR

#### 1.10.3.4.3. Is Required
True

#### 1.10.3.4.4. Size
50

#### 1.10.3.4.5. Notes
Identifier for the subscription plan (e.g., 'pro_monthly', 'team_annual').

### 1.10.3.5. status
#### 1.10.3.5.2. Type
VARCHAR

#### 1.10.3.5.3. Is Required
True

#### 1.10.3.5.4. Size
20

#### 1.10.3.5.5. Default Value
'Active'

#### 1.10.3.5.6. Constraints

- CHECK (status IN ('Active','Trial','Suspended','Cancelled','Expired'))

### 1.10.3.6. currentPeriodStart
#### 1.10.3.6.2. Type
DateTime

#### 1.10.3.6.3. Is Required
True

### 1.10.3.7. currentPeriodEnd
#### 1.10.3.7.2. Type
DateTime

#### 1.10.3.7.3. Is Required
True

### 1.10.3.8. paymentProvider
#### 1.10.3.8.2. Type
VARCHAR

#### 1.10.3.8.3. Is Required
True

#### 1.10.3.8.4. Size
50

#### 1.10.3.8.5. Constraints

- CHECK (paymentProvider IN ('Stripe', 'PayPal', 'OdooManual'))

### 1.10.3.9. paymentProviderSubscriptionId
#### 1.10.3.9.2. Type
VARCHAR

#### 1.10.3.9.3. Is Required
False

#### 1.10.3.9.4. Size
255

#### 1.10.3.9.5. Notes
Reference to the subscription ID in the payment provider (e.g., Stripe, PayPal).

### 1.10.3.10. paymentMethodId
#### 1.10.3.10.2. Type
VARCHAR

#### 1.10.3.10.3. Is Required
False

#### 1.10.3.10.4. Size
255

#### 1.10.3.10.5. Notes
Reference to the default payment method ID in the payment provider.

### 1.10.3.11. createdAt
#### 1.10.3.11.2. Type
DateTime

#### 1.10.3.11.3. Is Required
True

#### 1.10.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.10.3.12. updatedAt
#### 1.10.3.12.2. Type
DateTime

#### 1.10.3.12.3. Is Required
True

#### 1.10.3.12.4. Default Value
CURRENT_TIMESTAMP


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints

### 1.10.5.1. uq_subscription_odoo_so
#### 1.10.5.1.2. Columns

- odooSaleOrderId


### 1.10.6. Indexes

### 1.10.6.1. idx_subscription_userid_status
#### 1.10.6.1.2. Columns

- userId
- status

#### 1.10.6.1.3. Type
BTree

### 1.10.6.2. idx_subscription_currentperiodend
#### 1.10.6.2.2. Columns

- currentPeriodEnd

#### 1.10.6.2.3. Type
BTree


## 1.11. CreditTransaction
Credit usage and purchase records, synced from Odoo.

### 1.11.3. Attributes

### 1.11.3.1. id
#### 1.11.3.1.2. Type
UUID

#### 1.11.3.1.3. Is Required
True

#### 1.11.3.1.4. Is Primary Key
True

### 1.11.3.2. userId
#### 1.11.3.2.2. Type
UUID

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Is Foreign Key
True

#### 1.11.3.2.5. On Delete
CASCADE

#### 1.11.3.2.6. On Update
NO ACTION

### 1.11.3.3. odooInvoiceId
#### 1.11.3.3.2. Type
VARCHAR

#### 1.11.3.3.3. Is Required
False

#### 1.11.3.3.4. Size
255

#### 1.11.3.3.5. Notes
Reference to the Odoo Invoice record if applicable.

### 1.11.3.4. generationRequestId
#### 1.11.3.4.2. Type
UUID

#### 1.11.3.4.3. Is Required
False

#### 1.11.3.4.4. Is Foreign Key
True

#### 1.11.3.4.5. On Delete
SET NULL

#### 1.11.3.4.6. On Update
NO ACTION

### 1.11.3.5. apiCallId
#### 1.11.3.5.2. Type
VARCHAR

#### 1.11.3.5.3. Is Required
False

#### 1.11.3.5.4. Size
255

#### 1.11.3.5.5. Notes
Reference to API call log if applicable (e.g., for API usage credits).

### 1.11.3.6. amount
#### 1.11.3.6.2. Type
DECIMAL

#### 1.11.3.6.3. Is Required
True

#### 1.11.3.6.4. Precision
10

#### 1.11.3.6.5. Scale
2

#### 1.11.3.6.6. Notes
Credit amount (+ for purchase/refund, - for usage).

### 1.11.3.7. actionType
#### 1.11.3.7.2. Type
VARCHAR

#### 1.11.3.7.3. Is Required
True

#### 1.11.3.7.4. Size
50

#### 1.11.3.7.5. Notes
e.g., 'purchase', 'sample_generation', 'final_generation', 'export_hd', 'api_generation', 'refund'.

### 1.11.3.8. description
#### 1.11.3.8.2. Type
TEXT

#### 1.11.3.8.3. Is Required
False

### 1.11.3.9. createdAt
#### 1.11.3.9.2. Type
DateTime

#### 1.11.3.9.3. Is Required
True

#### 1.11.3.9.4. Default Value
CURRENT_TIMESTAMP

### 1.11.3.10. syncedAt
#### 1.11.3.10.2. Type
DateTime

#### 1.11.3.10.3. Is Required
True

#### 1.11.3.10.4. Default Value
CURRENT_TIMESTAMP

#### 1.11.3.10.5. Notes
Timestamp when this record was synced from Odoo.


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints


### 1.11.6. Indexes

### 1.11.6.1. idx_credittransaction_userid_createdat
#### 1.11.6.1.2. Columns

- userId
- createdAt

#### 1.11.6.1.3. Type
BTree

### 1.11.6.2. idx_credittransaction_actiontype
#### 1.11.6.2.2. Columns

- actionType

#### 1.11.6.2.3. Type
BTree


### 1.11.7. Partitioning

- **Type:** range
- **Columns:**
  
  - createdAt
  
- **Strategy Details:** Partition by range on createdAt, likely monthly or quarterly, depending on data volume and query patterns.

## 1.12. UsageLog
Detailed log of billable or trackable user actions.

### 1.12.3. Attributes

### 1.12.3.1. id
#### 1.12.3.1.2. Type
BIGSERIAL

#### 1.12.3.1.3. Is Required
True

#### 1.12.3.1.4. Is Primary Key
True

### 1.12.3.2. userId
#### 1.12.3.2.2. Type
UUID

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Is Foreign Key
True

#### 1.12.3.2.5. On Delete
SET NULL

#### 1.12.3.2.6. On Update
NO ACTION

### 1.12.3.3. generationRequestId
#### 1.12.3.3.2. Type
UUID

#### 1.12.3.3.3. Is Required
False

#### 1.12.3.3.4. Is Foreign Key
True

#### 1.12.3.3.5. On Delete
SET NULL

#### 1.12.3.3.6. On Update
NO ACTION

#### 1.12.3.3.7. Notes
Link to generation request if applicable.

### 1.12.3.4. apiClientId
#### 1.12.3.4.2. Type
UUID

#### 1.12.3.4.3. Is Required
False

#### 1.12.3.4.4. Is Foreign Key
True

#### 1.12.3.4.5. On Delete
SET NULL

#### 1.12.3.4.6. On Update
NO ACTION

#### 1.12.3.4.7. Notes
Link to API client if action via API.

### 1.12.3.5. actionType
#### 1.12.3.5.2. Type
VARCHAR

#### 1.12.3.5.3. Is Required
True

#### 1.12.3.5.4. Size
100

#### 1.12.3.5.5. Notes
e.g., 'sample_generation_initiated', 'final_generation_completed', 'asset_uploaded', 'asset_exported', 'api_call_success', 'login_success', 'subscription_change'.

### 1.12.3.6. details
#### 1.12.3.6.2. Type
JSONB

#### 1.12.3.6.3. Is Required
False

#### 1.12.3.6.4. Notes
Additional context for the action (e.g., file format, resolution, API endpoint, duration).

### 1.12.3.7. creditsCost
#### 1.12.3.7.2. Type
DECIMAL

#### 1.12.3.7.3. Is Required
False

#### 1.12.3.7.4. Precision
10

#### 1.12.3.7.5. Scale
2

#### 1.12.3.7.6. Notes
Credits consumed by this specific action step if any.

### 1.12.3.8. timestamp
#### 1.12.3.8.2. Type
DateTime

#### 1.12.3.8.3. Is Required
True

#### 1.12.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes

### 1.12.6.1. idx_usagelog_userid_timestamp
#### 1.12.6.1.2. Columns

- userId
- timestamp

#### 1.12.6.1.3. Type
BTree

### 1.12.6.2. idx_usagelog_actiontype
#### 1.12.6.2.2. Columns

- actionType

#### 1.12.6.2.3. Type
BTree

### 1.12.6.3. idx_usagelog_generationrequestid
#### 1.12.6.3.2. Columns

- generationRequestId

#### 1.12.6.3.3. Type
BTree

### 1.12.6.4. idx_usagelog_apiclientid
#### 1.12.6.4.2. Columns

- apiClientId

#### 1.12.6.4.3. Type
BTree


## 1.13. Team
Collaboration group for team accounts.

### 1.13.3. Attributes

### 1.13.3.1. id
#### 1.13.3.1.2. Type
UUID

#### 1.13.3.1.3. Is Required
True

#### 1.13.3.1.4. Is Primary Key
True

### 1.13.3.2. name
#### 1.13.3.2.2. Type
VARCHAR

#### 1.13.3.2.3. Is Required
True

#### 1.13.3.2.4. Size
100

### 1.13.3.3. ownerId
#### 1.13.3.3.2. Type
UUID

#### 1.13.3.3.3. Is Required
True

#### 1.13.3.3.4. Is Foreign Key
True

#### 1.13.3.3.5. On Delete
RESTRICT

#### 1.13.3.3.6. On Update
NO ACTION

#### 1.13.3.3.7. Notes
The primary owner of the team. Restrict deletion if team still exists.

### 1.13.3.4. createdAt
#### 1.13.3.4.2. Type
DateTime

#### 1.13.3.4.3. Is Required
True

#### 1.13.3.4.4. Default Value
CURRENT_TIMESTAMP

### 1.13.3.5. updatedAt
#### 1.13.3.5.2. Type
DateTime

#### 1.13.3.5.3. Is Required
True

#### 1.13.3.5.4. Default Value
CURRENT_TIMESTAMP


### 1.13.4. Primary Keys

- id

### 1.13.5. Unique Constraints


### 1.13.6. Indexes

### 1.13.6.1. idx_team_ownerid
#### 1.13.6.1.2. Columns

- ownerId

#### 1.13.6.1.3. Type
BTree


## 1.14. TeamMember
Association between users and teams.

### 1.14.3. Attributes

### 1.14.3.1. id
#### 1.14.3.1.2. Type
UUID

#### 1.14.3.1.3. Is Required
True

#### 1.14.3.1.4. Is Primary Key
True

### 1.14.3.2. teamId
#### 1.14.3.2.2. Type
UUID

#### 1.14.3.2.3. Is Required
True

#### 1.14.3.2.4. Is Foreign Key
True

#### 1.14.3.2.5. On Delete
CASCADE

#### 1.14.3.2.6. On Update
NO ACTION

### 1.14.3.3. userId
#### 1.14.3.3.2. Type
UUID

#### 1.14.3.3.3. Is Required
True

#### 1.14.3.3.4. Is Foreign Key
True

#### 1.14.3.3.5. On Delete
CASCADE

#### 1.14.3.3.6. On Update
NO ACTION

### 1.14.3.4. role
#### 1.14.3.4.2. Type
VARCHAR

#### 1.14.3.4.3. Is Required
True

#### 1.14.3.4.4. Size
20

#### 1.14.3.4.5. Constraints

- CHECK (role IN ('Owner','Admin','Editor','Viewer'))

#### 1.14.3.4.6. Indexed
True

### 1.14.3.5. joinedAt
#### 1.14.3.5.2. Type
DateTime

#### 1.14.3.5.3. Is Required
True

#### 1.14.3.5.4. Default Value
CURRENT_TIMESTAMP


### 1.14.4. Primary Keys

- id

### 1.14.5. Unique Constraints

### 1.14.5.1. uq_teammember_team_user
#### 1.14.5.1.2. Columns

- teamId
- userId


### 1.14.6. Indexes

### 1.14.6.1. idx_teammember_userid_role
#### 1.14.6.1.2. Columns

- userId
- role

#### 1.14.6.1.3. Type
BTree

### 1.14.6.2. idx_teammember_teamid
#### 1.14.6.2.2. Columns

- teamId

#### 1.14.6.2.3. Type
BTree


## 1.15. Session
User authentication sessions.

### 1.15.3. Attributes

### 1.15.3.1. id
#### 1.15.3.1.2. Type
UUID

#### 1.15.3.1.3. Is Required
True

#### 1.15.3.1.4. Is Primary Key
True

### 1.15.3.2. userId
#### 1.15.3.2.2. Type
UUID

#### 1.15.3.2.3. Is Required
True

#### 1.15.3.2.4. Is Foreign Key
True

#### 1.15.3.2.5. On Delete
CASCADE

#### 1.15.3.2.6. On Update
NO ACTION

### 1.15.3.3. deviceInfo
#### 1.15.3.3.2. Type
VARCHAR

#### 1.15.3.3.3. Is Required
True

#### 1.15.3.3.4. Size
255

### 1.15.3.4. ipAddress
#### 1.15.3.4.2. Type
VARCHAR

#### 1.15.3.4.3. Is Required
True

#### 1.15.3.4.4. Size
45

#### 1.15.3.4.5. Notes
Supports IPv4 and IPv6.

### 1.15.3.5. userAgent
#### 1.15.3.5.2. Type
TEXT

#### 1.15.3.5.3. Is Required
False

#### 1.15.3.5.4. Notes
Full user agent string for device identification.

### 1.15.3.6. lastActivity
#### 1.15.3.6.2. Type
DateTime

#### 1.15.3.6.3. Is Required
True

#### 1.15.3.6.4. Default Value
CURRENT_TIMESTAMP

#### 1.15.3.6.5. Indexed
True

### 1.15.3.7. expiresAt
#### 1.15.3.7.2. Type
DateTime

#### 1.15.3.7.3. Is Required
True

#### 1.15.3.7.4. Indexed
True

### 1.15.3.8. createdAt
#### 1.15.3.8.2. Type
DateTime

#### 1.15.3.8.3. Is Required
True

#### 1.15.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.15.4. Primary Keys

- id

### 1.15.5. Unique Constraints


### 1.15.6. Indexes

### 1.15.6.1. idx_session_userid_expiresat
#### 1.15.6.1.2. Columns

- userId
- expiresAt

#### 1.15.6.1.3. Type
BTree

### 1.15.6.2. idx_session_expiresat
#### 1.15.6.2.2. Columns

- expiresAt

#### 1.15.6.2.3. Type
BTree

#### 1.15.6.2.4. Notes
For cleaning up expired sessions.

### 1.15.6.3. idx_session_lastactivity
#### 1.15.6.3.2. Columns

- lastActivity

#### 1.15.6.3.3. Type
BTree


## 1.16. Notification
System notifications for users.

### 1.16.3. Attributes

### 1.16.3.1. id
#### 1.16.3.1.2. Type
UUID

#### 1.16.3.1.3. Is Required
True

#### 1.16.3.1.4. Is Primary Key
True

### 1.16.3.2. userId
#### 1.16.3.2.2. Type
UUID

#### 1.16.3.2.3. Is Required
True

#### 1.16.3.2.4. Is Foreign Key
True

#### 1.16.3.2.5. On Delete
CASCADE

#### 1.16.3.2.6. On Update
NO ACTION

### 1.16.3.3. type
#### 1.16.3.3.2. Type
VARCHAR

#### 1.16.3.3.3. Is Required
True

#### 1.16.3.3.4. Size
50

#### 1.16.3.3.5. Notes
e.g., 'generation_complete', 'collaboration_invite', 'billing_alert', 'system_update'.

### 1.16.3.4. message
#### 1.16.3.4.2. Type
TEXT

#### 1.16.3.4.3. Is Required
True

### 1.16.3.5. metadata
#### 1.16.3.5.2. Type
JSONB

#### 1.16.3.5.3. Is Required
False

#### 1.16.3.5.4. Notes
JSON object with context (e.g., links to project/asset/team, generation status).

### 1.16.3.6. isRead
#### 1.16.3.6.2. Type
BOOLEAN

#### 1.16.3.6.3. Is Required
True

#### 1.16.3.6.4. Default Value
false

#### 1.16.3.6.5. Indexed
True

### 1.16.3.7. createdAt
#### 1.16.3.7.2. Type
DateTime

#### 1.16.3.7.3. Is Required
True

#### 1.16.3.7.4. Default Value
CURRENT_TIMESTAMP

#### 1.16.3.7.5. Indexed
True

### 1.16.3.8. updatedAt
#### 1.16.3.8.2. Type
DateTime

#### 1.16.3.8.3. Is Required
True

#### 1.16.3.8.4. Default Value
CURRENT_TIMESTAMP

#### 1.16.3.8.5. Notes
Can track when marked as read.


### 1.16.4. Primary Keys

- id

### 1.16.5. Unique Constraints


### 1.16.6. Indexes

### 1.16.6.1. idx_notification_userid_isread_createdat
#### 1.16.6.1.2. Columns

- userId
- isRead
- createdAt

#### 1.16.6.1.3. Type
BTree

### 1.16.6.2. idx_notification_userid_isread_unread
#### 1.16.6.2.2. Columns

- userId
- isRead

#### 1.16.6.2.3. Type
BTree

#### 1.16.6.2.4. Condition
isRead = false

#### 1.16.6.2.5. Notes
Partial index for quick lookup of unread notifications.


### 1.16.7. Partitioning

- **Type:** range
- **Columns:**
  
  - createdAt
  
- **Strategy Details:** Partition by range on createdAt, likely monthly or quarterly, depending on data volume and query patterns.

## 1.17. Template
Predefined or user-saved creative templates.

### 1.17.3. Attributes

### 1.17.3.1. id
#### 1.17.3.1.2. Type
UUID

#### 1.17.3.1.3. Is Required
True

#### 1.17.3.1.4. Is Primary Key
True

### 1.17.3.2. userId
#### 1.17.3.2.2. Type
UUID

#### 1.17.3.2.3. Is Required
False

#### 1.17.3.2.4. Is Foreign Key
True

#### 1.17.3.2.5. On Delete
SET NULL

#### 1.17.3.2.6. On Update
NO ACTION

#### 1.17.3.2.7. Notes
Null for system templates. User ID for private templates.

### 1.17.3.3. name
#### 1.17.3.3.2. Type
VARCHAR

#### 1.17.3.3.3. Is Required
True

#### 1.17.3.3.4. Size
100

### 1.17.3.4. description
#### 1.17.3.4.2. Type
TEXT

#### 1.17.3.4.3. Is Required
False

### 1.17.3.5. category
#### 1.17.3.5.2. Type
VARCHAR

#### 1.17.3.5.3. Is Required
True

#### 1.17.3.5.4. Size
50

#### 1.17.3.5.5. Indexed
True

### 1.17.3.6. previewUrl
#### 1.17.3.6.2. Type
VARCHAR

#### 1.17.3.6.3. Is Required
True

#### 1.17.3.6.4. Size
1024

#### 1.17.3.6.5. Notes
MinIO path or external URL for preview image.

### 1.17.3.7. sourceData
#### 1.17.3.7.2. Type
JSONB

#### 1.17.3.7.3. Is Required
True

#### 1.17.3.7.4. Notes
JSON structure defining the template content and layout for the editor.

### 1.17.3.8. tags
#### 1.17.3.8.2. Type
JSONB

#### 1.17.3.8.3. Is Required
False

#### 1.17.3.8.4. Notes
JSON array of strings for search keywords.

#### 1.17.3.8.5. Searchable
True

### 1.17.3.9. isPublic
#### 1.17.3.9.2. Type
BOOLEAN

#### 1.17.3.9.3. Is Required
True

#### 1.17.3.9.4. Default Value
true

#### 1.17.3.9.5. Notes
True for system templates, false for private user templates.

### 1.17.3.10. createdAt
#### 1.17.3.10.2. Type
DateTime

#### 1.17.3.10.3. Is Required
True

#### 1.17.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.17.3.11. updatedAt
#### 1.17.3.11.2. Type
DateTime

#### 1.17.3.11.3. Is Required
True

#### 1.17.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.17.4. Primary Keys

- id

### 1.17.5. Unique Constraints


### 1.17.6. Indexes

### 1.17.6.1. idx_template_category_ispublic
#### 1.17.6.1.2. Columns

- category
- isPublic

#### 1.17.6.1.3. Type
BTree

### 1.17.6.2. idx_template_userid
#### 1.17.6.2.2. Columns

- userId

#### 1.17.6.2.3. Type
BTree

### 1.17.6.3. idx_template_tags_gin
#### 1.17.6.3.2. Columns

- tags

#### 1.17.6.3.3. Type
GIN


## 1.18. AIModel
Metadata for AI models available on the platform.

### 1.18.3. Attributes

### 1.18.3.1. id
#### 1.18.3.1.2. Type
UUID

#### 1.18.3.1.3. Is Required
True

#### 1.18.3.1.4. Is Primary Key
True

### 1.18.3.2. name
#### 1.18.3.2.2. Type
VARCHAR

#### 1.18.3.2.3. Is Required
True

#### 1.18.3.2.4. Size
100

#### 1.18.3.2.5. Is Unique
True

### 1.18.3.3. description
#### 1.18.3.3.2. Type
TEXT

#### 1.18.3.3.3. Is Required
False

### 1.18.3.4. provider
#### 1.18.3.4.2. Type
VARCHAR

#### 1.18.3.4.3. Is Required
True

#### 1.18.3.4.4. Size
50

#### 1.18.3.4.5. Notes
e.g., 'Internal', 'OpenAI', 'StabilityAI', 'OtherProvider'.

### 1.18.3.5. taskType
#### 1.18.3.5.2. Type
VARCHAR

#### 1.18.3.5.3. Is Required
True

#### 1.18.3.5.4. Size
50

#### 1.18.3.5.5. Constraints

- CHECK (taskType IN ('ImageGeneration', 'TextGeneration', 'ImageTransformation', 'StyleTransfer', 'ContentSafety'))

#### 1.18.3.5.6. Indexed
True

### 1.18.3.6. isActive
#### 1.18.3.6.2. Type
BOOLEAN

#### 1.18.3.6.3. Is Required
True

#### 1.18.3.6.4. Default Value
true

#### 1.18.3.6.5. Indexed
True

### 1.18.3.7. createdAt
#### 1.18.3.7.2. Type
DateTime

#### 1.18.3.7.3. Is Required
True

#### 1.18.3.7.4. Default Value
CURRENT_TIMESTAMP

### 1.18.3.8. updatedAt
#### 1.18.3.8.2. Type
DateTime

#### 1.18.3.8.3. Is Required
True

#### 1.18.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.18.4. Primary Keys

- id

### 1.18.5. Unique Constraints

### 1.18.5.1. uq_aimodel_name
#### 1.18.5.1.2. Columns

- name


### 1.18.6. Indexes

### 1.18.6.1. idx_aimodel_provider_tasktype
#### 1.18.6.1.2. Columns

- provider
- taskType

#### 1.18.6.1.3. Type
BTree


## 1.19. AIModelVersion
Specific versions of AI models.

### 1.19.3. Attributes

### 1.19.3.1. id
#### 1.19.3.1.2. Type
UUID

#### 1.19.3.1.3. Is Required
True

#### 1.19.3.1.4. Is Primary Key
True

### 1.19.3.2. modelId
#### 1.19.3.2.2. Type
UUID

#### 1.19.3.2.3. Is Required
True

#### 1.19.3.2.4. Is Foreign Key
True

#### 1.19.3.2.5. On Delete
CASCADE

#### 1.19.3.2.6. On Update
NO ACTION

### 1.19.3.3. versionNumber
#### 1.19.3.3.2. Type
VARCHAR

#### 1.19.3.3.3. Is Required
True

#### 1.19.3.3.4. Size
50

#### 1.19.3.3.5. Notes
e.g., '1.0', '2023-10-26', 'DALL-E 3'.

### 1.19.3.4. sourcePath
#### 1.19.3.4.2. Type
VARCHAR

#### 1.19.3.4.3. Is Required
False

#### 1.19.3.4.4. Size
1024

#### 1.19.3.4.5. Notes
MinIO path for internal model artifacts. Null for external models.

### 1.19.3.5. format
#### 1.19.3.5.2. Type
VARCHAR

#### 1.19.3.5.3. Is Required
False

#### 1.19.3.5.4. Size
50

#### 1.19.3.5.5. Notes
e.g., 'ONNX', 'TensorFlow SavedModel', 'API'.

### 1.19.3.6. parameters
#### 1.19.3.6.2. Type
JSONB

#### 1.19.3.6.3. Is Required
False

#### 1.19.3.6.4. Notes
JSON object of model-specific parameters or configuration.

### 1.19.3.7. status
#### 1.19.3.7.2. Type
VARCHAR

#### 1.19.3.7.3. Is Required
True

#### 1.19.3.7.4. Size
50

#### 1.19.3.7.5. Default Value
'Staged'

#### 1.19.3.7.6. Constraints

- CHECK (status IN ('Staged','Production','Deprecated','Archived','Failed'))

#### 1.19.3.7.7. Indexed
True

### 1.19.3.8. validationResultId
#### 1.19.3.8.2. Type
UUID

#### 1.19.3.8.3. Is Required
False

#### 1.19.3.8.4. Is Foreign Key
True

#### 1.19.3.8.5. On Delete
SET NULL

#### 1.19.3.8.6. On Update
NO ACTION

### 1.19.3.9. createdByUserId
#### 1.19.3.9.2. Type
UUID

#### 1.19.3.9.3. Is Required
False

#### 1.19.3.9.4. Is Foreign Key
True

#### 1.19.3.9.5. On Delete
SET NULL

#### 1.19.3.9.6. On Update
NO ACTION

#### 1.19.3.9.7. Notes
User (admin/enterprise) who uploaded/created this version.

### 1.19.3.10. releaseNotes
#### 1.19.3.10.2. Type
TEXT

#### 1.19.3.10.3. Is Required
False

### 1.19.3.11. createdAt
#### 1.19.3.11.2. Type
DateTime

#### 1.19.3.11.3. Is Required
True

#### 1.19.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.19.3.12. updatedAt
#### 1.19.3.12.2. Type
DateTime

#### 1.19.3.12.3. Is Required
True

#### 1.19.3.12.4. Default Value
CURRENT_TIMESTAMP


### 1.19.4. Primary Keys

- id

### 1.19.5. Unique Constraints

### 1.19.5.1. uq_aimodelversion_model_version
#### 1.19.5.1.2. Columns

- modelId
- versionNumber


### 1.19.6. Indexes

### 1.19.6.1. idx_aimodelversion_modelid
#### 1.19.6.1.2. Columns

- modelId

#### 1.19.6.1.3. Type
BTree

### 1.19.6.2. idx_aimodelversion_status
#### 1.19.6.2.2. Columns

- status

#### 1.19.6.2.3. Type
BTree


## 1.20. AIModelValidationResult
Results from validating an AI model version.

### 1.20.3. Attributes

### 1.20.3.1. id
#### 1.20.3.1.2. Type
UUID

#### 1.20.3.1.3. Is Required
True

#### 1.20.3.1.4. Is Primary Key
True

### 1.20.3.2. modelVersionId
#### 1.20.3.2.2. Type
UUID

#### 1.20.3.2.3. Is Required
True

#### 1.20.3.2.4. Is Foreign Key
True

#### 1.20.3.2.5. On Delete
CASCADE

#### 1.20.3.2.6. On Update
NO ACTION

### 1.20.3.3. validationTimestamp
#### 1.20.3.3.2. Type
DateTime

#### 1.20.3.3.3. Is Required
True

#### 1.20.3.3.4. Default Value
CURRENT_TIMESTAMP

### 1.20.3.4. securityScanStatus
#### 1.20.3.4.2. Type
VARCHAR

#### 1.20.3.4.3. Is Required
True

#### 1.20.3.4.4. Size
50

#### 1.20.3.4.5. Constraints

- CHECK (securityScanStatus IN ('Passed','Failed','Pending','Skipped'))

### 1.20.3.5. functionalStatus
#### 1.20.3.5.2. Type
VARCHAR

#### 1.20.3.5.3. Is Required
True

#### 1.20.3.5.4. Size
50

#### 1.20.3.5.5. Constraints

- CHECK (functionalStatus IN ('Passed','Failed','Pending','Skipped'))

### 1.20.3.6. performanceBenchmark
#### 1.20.3.6.2. Type
JSONB

#### 1.20.3.6.3. Is Required
False

#### 1.20.3.6.4. Notes
JSON object with benchmark data (latency, throughput, quality metrics).

### 1.20.3.7. results
#### 1.20.3.7.2. Type
JSONB

#### 1.20.3.7.3. Is Required
False

#### 1.20.3.7.4. Notes
Full results log from validation tools.

### 1.20.3.8. validatedByUserId
#### 1.20.3.8.2. Type
UUID

#### 1.20.3.8.3. Is Required
False

#### 1.20.3.8.4. Is Foreign Key
True

#### 1.20.3.8.5. On Delete
SET NULL

#### 1.20.3.8.6. On Update
NO ACTION

#### 1.20.3.8.7. Notes
User or system account that triggered validation.

### 1.20.3.9. createdAt
#### 1.20.3.9.2. Type
DateTime

#### 1.20.3.9.3. Is Required
True

#### 1.20.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.20.4. Primary Keys

- id

### 1.20.5. Unique Constraints


### 1.20.6. Indexes

### 1.20.6.1. idx_aimodelvalidationresult_versionid
#### 1.20.6.1.2. Columns

- modelVersionId

#### 1.20.6.1.3. Type
BTree

### 1.20.6.2. idx_aimodelvalidationresult_timestamp
#### 1.20.6.2.2. Columns

- validationTimestamp

#### 1.20.6.2.3. Type
BTree


## 1.21. AIModelDeployment
Record of AI model version deployments.

### 1.21.3. Attributes

### 1.21.3.1. id
#### 1.21.3.1.2. Type
UUID

#### 1.21.3.1.3. Is Required
True

#### 1.21.3.1.4. Is Primary Key
True

### 1.21.3.2. modelVersionId
#### 1.21.3.2.2. Type
UUID

#### 1.21.3.2.3. Is Required
True

#### 1.21.3.2.4. Is Foreign Key
True

#### 1.21.3.2.5. On Delete
CASCADE

#### 1.21.3.2.6. On Update
NO ACTION

### 1.21.3.3. environment
#### 1.21.3.3.2. Type
VARCHAR

#### 1.21.3.3.3. Is Required
True

#### 1.21.3.3.4. Size
50

#### 1.21.3.3.5. Constraints

- CHECK (environment IN ('staging','production','testing'))

#### 1.21.3.3.6. Indexed
True

### 1.21.3.4. status
#### 1.21.3.4.2. Type
VARCHAR

#### 1.21.3.4.3. Is Required
True

#### 1.21.3.4.4. Size
50

#### 1.21.3.4.5. Default Value
'Initiated'

#### 1.21.3.4.6. Constraints

- CHECK (status IN ('Initiated','Deploying','Active','Inactive','Failed','RolledBack'))

#### 1.21.3.4.7. Indexed
True

### 1.21.3.5. deploymentStrategy
#### 1.21.3.5.2. Type
VARCHAR

#### 1.21.3.5.3. Is Required
False

#### 1.21.3.5.4. Size
50

#### 1.21.3.5.5. Notes
e.g., 'blue_green', 'canary', 'rolling_update'.

### 1.21.3.6. endpoint
#### 1.21.3.6.2. Type
VARCHAR

#### 1.21.3.6.3. Is Required
False

#### 1.21.3.6.4. Size
255

#### 1.21.3.6.5. Notes
Internal endpoint for accessing the deployed model.

### 1.21.3.7. kubernetesDetails
#### 1.21.3.7.2. Type
JSONB

#### 1.21.3.7.3. Is Required
False

#### 1.21.3.7.4. Notes
JSON object with K8s deployment name, namespace, pod counts, etc.

### 1.21.3.8. deployedByUserId
#### 1.21.3.8.2. Type
UUID

#### 1.21.3.8.3. Is Required
False

#### 1.21.3.8.4. Is Foreign Key
True

#### 1.21.3.8.5. On Delete
SET NULL

#### 1.21.3.8.6. On Update
NO ACTION

#### 1.21.3.8.7. Notes
User or system account that triggered deployment.

### 1.21.3.9. deploymentTimestamp
#### 1.21.3.9.2. Type
DateTime

#### 1.21.3.9.3. Is Required
True

#### 1.21.3.9.4. Default Value
CURRENT_TIMESTAMP

### 1.21.3.10. createdAt
#### 1.21.3.10.2. Type
DateTime

#### 1.21.3.10.3. Is Required
True

#### 1.21.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.21.3.11. updatedAt
#### 1.21.3.11.2. Type
DateTime

#### 1.21.3.11.3. Is Required
True

#### 1.21.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.21.4. Primary Keys

- id

### 1.21.5. Unique Constraints


### 1.21.6. Indexes

### 1.21.6.1. idx_aimodeldeployment_versionid_env
#### 1.21.6.1.2. Columns

- modelVersionId
- environment

#### 1.21.6.1.3. Type
BTree

### 1.21.6.2. idx_aimodeldeployment_status
#### 1.21.6.2.2. Columns

- status

#### 1.21.6.2.3. Type
BTree


## 1.22. AIModelFeedback
User feedback on outputs from specific AI models.

### 1.22.3. Attributes

### 1.22.3.1. id
#### 1.22.3.1.2. Type
UUID

#### 1.22.3.1.3. Is Required
True

#### 1.22.3.1.4. Is Primary Key
True

### 1.22.3.2. userId
#### 1.22.3.2.2. Type
UUID

#### 1.22.3.2.3. Is Required
True

#### 1.22.3.2.4. Is Foreign Key
True

#### 1.22.3.2.5. On Delete
SET NULL

#### 1.22.3.2.6. On Update
NO ACTION

### 1.22.3.3. generationRequestId
#### 1.22.3.3.2. Type
UUID

#### 1.22.3.3.3. Is Required
False

#### 1.22.3.3.4. Is Foreign Key
True

#### 1.22.3.3.5. On Delete
SET NULL

#### 1.22.3.3.6. On Update
NO ACTION

#### 1.22.3.3.7. Notes
Link to the specific generation request the feedback is about.

### 1.22.3.4. modelVersionId
#### 1.22.3.4.2. Type
UUID

#### 1.22.3.4.3. Is Required
False

#### 1.22.3.4.4. Is Foreign Key
True

#### 1.22.3.4.5. On Delete
SET NULL

#### 1.22.3.4.6. On Update
NO ACTION

#### 1.22.3.4.7. Notes
Link to the model version the feedback pertains to.

### 1.22.3.5. rating
#### 1.22.3.5.2. Type
INTEGER

#### 1.22.3.5.3. Is Required
False

#### 1.22.3.5.4. Constraints

- CHECK (rating >= 1 AND rating <= 5)

#### 1.22.3.5.5. Notes
Optional rating (e.g., 1-5 stars).

### 1.22.3.6. comment
#### 1.22.3.6.2. Type
TEXT

#### 1.22.3.6.3. Is Required
False

### 1.22.3.7. feedbackTimestamp
#### 1.22.3.7.2. Type
DateTime

#### 1.22.3.7.3. Is Required
True

#### 1.22.3.7.4. Default Value
CURRENT_TIMESTAMP

### 1.22.3.8. details
#### 1.22.3.8.2. Type
JSONB

#### 1.22.3.8.3. Is Required
False

#### 1.22.3.8.4. Notes
Additional structured feedback data.

### 1.22.3.9. createdAt
#### 1.22.3.9.2. Type
DateTime

#### 1.22.3.9.3. Is Required
True

#### 1.22.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.22.4. Primary Keys

- id

### 1.22.5. Unique Constraints


### 1.22.6. Indexes

### 1.22.6.1. idx_aimodelfeedback_userid
#### 1.22.6.1.2. Columns

- userId

#### 1.22.6.1.3. Type
BTree

### 1.22.6.2. idx_aimodelfeedback_generationrequestid
#### 1.22.6.2.2. Columns

- generationRequestId

#### 1.22.6.2.3. Type
BTree

### 1.22.6.3. idx_aimodelfeedback_modelversionid
#### 1.22.6.3.2. Columns

- modelVersionId

#### 1.22.6.3.3. Type
BTree




---

# 2. Diagrams

- **Diagram_Title:** User, Account, and Authentication  
**Diagram_Area:** User Management and Authentication  
**Explanation:** This diagram focuses on the core user entity and its related authentication mechanisms, account details, and communication channels like sessions, social connections, API access, subscriptions, and notifications. It illustrates how various account-level features are linked directly to a user.  
**Mermaid_Text:** erDiagram

    User {
        UUID id PK
        VARCHAR email
        VARCHAR username
        VARCHAR subscriptionTier
        DECIMAL creditBalance
        DateTime createdAt
    }

    Session {
        UUID id PK
        UUID userId FK
        VARCHAR deviceInfo
        DateTime expiresAt
        DateTime createdAt
    }

    SocialMediaConnection {
        UUID id PK
        UUID userId FK
        VARCHAR platform
        VARCHAR externalUserId
        DateTime expiresAt
    }

    APIClient {
        UUID id PK
        UUID userId FK
        VARCHAR name
        VARCHAR apiKey
        BOOLEAN isActive
    }

    Subscription {
        UUID id PK
        UUID userId FK
        VARCHAR odooSaleOrderId
        VARCHAR planId
        VARCHAR status
        DateTime currentPeriodEnd
    }

    Notification {
        UUID id PK
        UUID userId FK
        VARCHAR type
        TEXT message
        BOOLEAN isRead
        DateTime createdAt
    }

    User ||--o{ Session : "has"
    User ||--o{ SocialMediaConnection : "connected to"
    User ||--o{ APIClient : "manages"
    User ||--o{ Subscription : "has"
    User ||--o{ Notification : "receives"
  
- **Diagram_Title:** Creative Workflow, Projects, and Assets  
**Diagram_Area:** Creative Projects and Asset Management  
**Explanation:** This diagram illustrates the core creative workflow entities: Workbenches organize Projects, Projects contain Assets and link to Templates and BrandKits. It shows the relationships between users, teams, brand kits, projects, and assets, including versioning.  
**Mermaid_Text:** erDiagram

    User {
        UUID id PK
        VARCHAR fullName
        VARCHAR username
    }

    Team {
        UUID id PK
        UUID ownerId FK
        VARCHAR name
    }

    TeamMember {
        UUID id PK
        UUID teamId FK
        UUID userId FK
        VARCHAR role
    }

    BrandKit {
        UUID id PK
        UUID userId FK
        UUID teamId FK
        VARCHAR name
        BOOLEAN isDefault
    }

    Workbench {
        UUID id PK
        UUID userId FK
        UUID defaultBrandKitId FK
        VARCHAR name
    }

    Project {
        UUID id PK
        UUID workbenchId FK
        UUID userId FK "Denormalized"
        UUID templateId FK
        UUID brandKitId FK
        VARCHAR name
    }

    Asset {
        UUID id PK
        UUID projectId FK
        UUID userId FK
        UUID generationRequestId FK "See AI Diagram"
        VARCHAR name
        VARCHAR type
        VARCHAR filePath
        BOOLEAN isFinal
    }

    AssetVersion {
        UUID id PK
        UUID assetId FK
        UUID projectId FK
        UUID createdByUserId FK
        INTEGER versionNumber
        TEXT description
        DateTime createdAt
    }

    Template {
        UUID id PK
        UUID userId FK
        VARCHAR name
        VARCHAR category
        BOOLEAN isPublic
    }

    User ||--o{ Team : "owns"
    User ||--o{ TeamMember : "is member of"
    Team ||--o{ TeamMember : "has member"
    TeamMember }|--|| User : "member of"
    TeamMember }|--|| Team : "has"
    User ||--o{ BrandKit : "owns"
    Team o|--o{ BrandKit : "has"
    User ||--o{ Workbench : "owns"
    Workbench ||--o{ Project : "contains"
    Project }|--|| Workbench : "part of"
    Workbench o|--o| BrandKit : "uses default"
    Project o|--o| BrandKit : "uses override"
    User ||--o{ Project : "owns"
    User ||--o{ Asset : "owns"
    Project o|--o{ Asset : "includes"
    Asset o|--o{ AssetVersion : "has versions"
    Project o|--o{ AssetVersion : "has versions"
    User o|--o{ AssetVersion : "created by"
    User o|--o{ Template : "created"
    Template o|--o{ Project : "uses"
  
- **Diagram_Title:** AI Generation, Models, Usage, and Billing  
**Diagram_Area:** AI Generation and Billing/Usage Tracking  
**Explanation:** This diagram details the AI generation process, linking user requests to projects, AI models used, generated assets, and the associated credit costs and usage logs. It also shows the lifecycle of AI models, including versions, validation, deployment, and user feedback.  
**Mermaid_Text:** erDiagram

    User {
        UUID id PK
        VARCHAR email
        DECIMAL creditBalance
    }

    Project {
        UUID id PK
        VARCHAR name
    }

    Asset {
        UUID id PK
        VARCHAR name
        VARCHAR type
        VARCHAR filePath
    }

    GenerationRequest {
        UUID id PK
        UUID userId FK
        UUID projectId FK
        UUID finalAssetId FK
        TEXT inputPrompt
        VARCHAR status
        DECIMAL creditsCostSample
        DECIMAL creditsCostFinal
        VARCHAR aiModelUsed
    }

    CreditTransaction {
        UUID id PK
        UUID userId FK
        UUID generationRequestId FK
        DECIMAL amount
        VARCHAR actionType
        DateTime createdAt
    }

    UsageLog {
        BIGSERIAL id PK
        UUID userId FK
        UUID generationRequestId FK
        UUID apiClientId FK "See Account Diagram"
        VARCHAR actionType
        DECIMAL creditsCost
        DateTime timestamp
    }

    AIModel {
        UUID id PK
        VARCHAR name
        VARCHAR taskType
        BOOLEAN isActive
    }

    AIModelVersion {
        UUID id PK
        UUID modelId FK
        UUID validationResultId FK "Latest result?"
        UUID createdByUserId FK
        VARCHAR versionNumber
        VARCHAR status
    }

    AIModelValidationResult {
        UUID id PK
        UUID modelVersionId FK
        UUID validatedByUserId FK
        DateTime validationTimestamp
        VARCHAR securityScanStatus
        VARCHAR functionalStatus
    }

    AIModelDeployment {
        UUID id PK
        UUID modelVersionId FK
        UUID deployedByUserId FK
        VARCHAR environment
        VARCHAR status
    }

    AIModelFeedback {
        UUID id PK
        UUID userId FK
        UUID generationRequestId FK
        UUID modelVersionId FK
        INTEGER rating
        TEXT comment
    }

    User ||--o{ GenerationRequest : "requests"
    User ||--o{ CreditTransaction : "has"
    User o|--o{ UsageLog : "logged actions"
    User o|--o{ AIModelVersion : "created"
    User o|--o{ AIModelValidationResult : "validated by"
    User o|--o{ AIModelDeployment : "deployed by"
    User o|--o{ AIModelFeedback : "provided by"

    Project o|--o{ GenerationRequest : "has"
    GenerationRequest o|--o| Asset : "resulted in" 
    Asset o|--|| GenerationRequest : "source/sample for" 
    GenerationRequest o|--o{ CreditTransaction : "cost"
    GenerationRequest o|--o{ UsageLog : "logged as"
    GenerationRequest o|--o{ AIModelFeedback : "feedback on"
    
    AIModel ||--o{ AIModelVersion : "has version"
    AIModelVersion ||--o{ AIModelValidationResult : "validated by"
    AIModelVersion ||--o{ AIModelDeployment : "deployed as"
    AIModelVersion o|--o{ AIModelFeedback : "feedback on"
    
    UsageLog o|--|| APIClient : "via"
  


---

