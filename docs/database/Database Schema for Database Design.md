# Specification

# 1. Entities

## 1.1. User
Represents a registered user account. Caching strategy: Cache `fullName`, `subscriptionTier`, `languagePreference`, `timezone`, `creditBalance` in a suitable caching layer (e.g., Redis); invalidate cache on updates to these fields.

### 1.1.3. Attributes

### 1.1.3.1. id
#### 1.1.3.1.2. Type
uuid

#### 1.1.3.1.3. Is Required
True

#### 1.1.3.1.4. Is Primary Key
True

### 1.1.3.2. email
#### 1.1.3.2.2. Type
varchar

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Size
255

#### 1.1.3.2.5. Is Unique
True

### 1.1.3.3. passwordHash
#### 1.1.3.3.2. Type
varchar

#### 1.1.3.3.3. Is Required
False

#### 1.1.3.3.4. Size
255

### 1.1.3.4. isEmailVerified
#### 1.1.3.4.2. Type
boolean

#### 1.1.3.4.3. Is Required
True

#### 1.1.3.4.4. Default Value
false

### 1.1.3.5. fullName
#### 1.1.3.5.2. Type
varchar

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
100

### 1.1.3.6. username
#### 1.1.3.6.2. Type
varchar

#### 1.1.3.6.3. Is Required
False

#### 1.1.3.6.4. Size
50

#### 1.1.3.6.5. Is Unique
True

### 1.1.3.7. profilePictureUrl
#### 1.1.3.7.2. Type
varchar

#### 1.1.3.7.3. Is Required
False

#### 1.1.3.7.4. Size
255

### 1.1.3.8. languagePreference
#### 1.1.3.8.2. Type
varchar

#### 1.1.3.8.3. Is Required
True

#### 1.1.3.8.4. Size
10

#### 1.1.3.8.5. Default Value
'en-US'

### 1.1.3.9. timezone
#### 1.1.3.9.2. Type
varchar

#### 1.1.3.9.3. Is Required
True

#### 1.1.3.9.4. Size
50

#### 1.1.3.9.5. Default Value
'UTC'

### 1.1.3.10. subscriptionTier
#### 1.1.3.10.2. Type
varchar

#### 1.1.3.10.3. Is Required
True

#### 1.1.3.10.4. Size
20

#### 1.1.3.10.5. Constraints

- CHECK (subscriptionTier IN ('Free','Pro','Team','Enterprise'))

### 1.1.3.11. creditBalance
#### 1.1.3.11.2. Type
decimal

#### 1.1.3.11.3. Is Required
True

#### 1.1.3.11.4. Precision
10

#### 1.1.3.11.5. Scale
2

#### 1.1.3.11.6. Default Value
0

### 1.1.3.12. createdAt
#### 1.1.3.12.2. Type
timestamp

#### 1.1.3.12.3. Is Required
True

### 1.1.3.13. updatedAt
#### 1.1.3.13.2. Type
timestamp

#### 1.1.3.13.3. Is Required
True

### 1.1.3.14. isDeleted
#### 1.1.3.14.2. Type
boolean

#### 1.1.3.14.3. Is Required
True

#### 1.1.3.14.4. Default Value
false


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints

### 1.1.5.1. uq_user_email
#### 1.1.5.1.2. Columns

- email

### 1.1.5.2. uq_user_username
#### 1.1.5.2.2. Columns

- username


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


## 1.2. BrandKit
Collection of brand assets and preferences

### 1.2.3. Attributes

### 1.2.3.1. id
#### 1.2.3.1.2. Type
uuid

#### 1.2.3.1.3. Is Required
True

#### 1.2.3.1.4. Is Primary Key
True

### 1.2.3.2. userId
#### 1.2.3.2.2. Type
uuid

#### 1.2.3.2.3. Is Required
True

#### 1.2.3.2.4. Is Foreign Key
True

#### 1.2.3.2.5. Constraints

- REFERENCES User(id)

### 1.2.3.3. name
#### 1.2.3.3.2. Type
varchar

#### 1.2.3.3.3. Is Required
True

#### 1.2.3.3.4. Size
100

### 1.2.3.4. colors
#### 1.2.3.4.2. Type
json

#### 1.2.3.4.3. Is Required
True

### 1.2.3.5. fonts
#### 1.2.3.5.2. Type
json

#### 1.2.3.5.3. Is Required
True

### 1.2.3.6. logos
#### 1.2.3.6.2. Type
json

#### 1.2.3.6.3. Is Required
False

### 1.2.3.7. isDefault
#### 1.2.3.7.2. Type
boolean

#### 1.2.3.7.3. Is Required
True

#### 1.2.3.7.4. Default Value
false

### 1.2.3.8. createdAt
#### 1.2.3.8.2. Type
timestamp

#### 1.2.3.8.3. Is Required
True


### 1.2.4. Primary Keys

- id

### 1.2.5. Unique Constraints


### 1.2.6. Indexes

### 1.2.6.1. idx_brandkit_colors_gin
#### 1.2.6.1.2. Columns

- colors

#### 1.2.6.1.3. Type
GIN


## 1.3. Workbench
Container for organizing creative projects

### 1.3.3. Attributes

### 1.3.3.1. id
#### 1.3.3.1.2. Type
uuid

#### 1.3.3.1.3. Is Required
True

#### 1.3.3.1.4. Is Primary Key
True

### 1.3.3.2. userId
#### 1.3.3.2.2. Type
uuid

#### 1.3.3.2.3. Is Required
True

#### 1.3.3.2.4. Is Foreign Key
True

#### 1.3.3.2.5. Constraints

- REFERENCES User(id)

### 1.3.3.3. name
#### 1.3.3.3.2. Type
varchar

#### 1.3.3.3.3. Is Required
True

#### 1.3.3.3.4. Size
100

### 1.3.3.4. defaultBrandKitId
#### 1.3.3.4.2. Type
uuid

#### 1.3.3.4.3. Is Required
False

#### 1.3.3.4.4. Is Foreign Key
True

#### 1.3.3.4.5. Constraints

- REFERENCES BrandKit(id)

### 1.3.3.5. createdAt
#### 1.3.3.5.2. Type
timestamp

#### 1.3.3.5.3. Is Required
True


### 1.3.4. Primary Keys

- id

### 1.3.5. Unique Constraints


### 1.3.6. Indexes


## 1.4. Project
Creative project containing assets

### 1.4.3. Attributes

### 1.4.3.1. id
#### 1.4.3.1.2. Type
uuid

#### 1.4.3.1.3. Is Required
True

#### 1.4.3.1.4. Is Primary Key
True

### 1.4.3.2. workbenchId
#### 1.4.3.2.2. Type
uuid

#### 1.4.3.2.3. Is Required
True

#### 1.4.3.2.4. Is Foreign Key
True

#### 1.4.3.2.5. Constraints

- REFERENCES Workbench(id)

### 1.4.3.3. userId
#### 1.4.3.3.2. Type
uuid

#### 1.4.3.3.3. Is Required
True

#### 1.4.3.3.4. Is Foreign Key
True

#### 1.4.3.3.5. Constraints

- REFERENCES User(id)

#### 1.4.3.3.6. Notes
Denormalized from Workbench for query performance. Ensure consistency with Workbench.userId via application logic or triggers.

### 1.4.3.4. name
#### 1.4.3.4.2. Type
varchar

#### 1.4.3.4.3. Is Required
True

#### 1.4.3.4.4. Size
100

### 1.4.3.5. brandKitId
#### 1.4.3.5.2. Type
uuid

#### 1.4.3.5.3. Is Required
False

#### 1.4.3.5.4. Is Foreign Key
True

#### 1.4.3.5.5. Constraints

- REFERENCES BrandKit(id)

### 1.4.3.6. targetPlatform
#### 1.4.3.6.2. Type
varchar

#### 1.4.3.6.3. Is Required
False

#### 1.4.3.6.4. Size
20

### 1.4.3.7. createdAt
#### 1.4.3.7.2. Type
timestamp

#### 1.4.3.7.3. Is Required
True

### 1.4.3.8. updatedAt
#### 1.4.3.8.2. Type
timestamp

#### 1.4.3.8.3. Is Required
True


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints


### 1.4.6. Indexes


## 1.5. Asset
Creative asset (uploaded or AI-generated)

### 1.5.3. Attributes

### 1.5.3.1. id
#### 1.5.3.1.2. Type
uuid

#### 1.5.3.1.3. Is Required
True

#### 1.5.3.1.4. Is Primary Key
True

### 1.5.3.2. projectId
#### 1.5.3.2.2. Type
uuid

#### 1.5.3.2.3. Is Required
True

#### 1.5.3.2.4. Is Foreign Key
True

#### 1.5.3.2.5. Constraints

- REFERENCES Project(id)

### 1.5.3.3. name
#### 1.5.3.3.2. Type
varchar

#### 1.5.3.3.3. Is Required
True

#### 1.5.3.3.4. Size
100

### 1.5.3.4. type
#### 1.5.3.4.2. Type
varchar

#### 1.5.3.4.3. Is Required
True

#### 1.5.3.4.4. Size
20

#### 1.5.3.4.5. Constraints

- CHECK (type IN ('Uploaded','AIGenerated'))

### 1.5.3.5. filePath
#### 1.5.3.5.2. Type
varchar

#### 1.5.3.5.3. Is Required
True

#### 1.5.3.5.4. Size
255

### 1.5.3.6. format
#### 1.5.3.6.2. Type
varchar

#### 1.5.3.6.3. Is Required
True

#### 1.5.3.6.4. Size
10

### 1.5.3.7. resolution
#### 1.5.3.7.2. Type
varchar

#### 1.5.3.7.3. Is Required
True

#### 1.5.3.7.4. Size
20

### 1.5.3.8. isFinal
#### 1.5.3.8.2. Type
boolean

#### 1.5.3.8.3. Is Required
True

#### 1.5.3.8.4. Default Value
false

### 1.5.3.9. createdAt
#### 1.5.3.9.2. Type
timestamp

#### 1.5.3.9.3. Is Required
True


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


## 1.6. AssetVersion
Version history for creative assets

### 1.6.3. Attributes

### 1.6.3.1. id
#### 1.6.3.1.2. Type
uuid

#### 1.6.3.1.3. Is Required
True

#### 1.6.3.1.4. Is Primary Key
True

### 1.6.3.2. assetId
#### 1.6.3.2.2. Type
uuid

#### 1.6.3.2.3. Is Required
True

#### 1.6.3.2.4. Is Foreign Key
True

#### 1.6.3.2.5. Constraints

- REFERENCES Asset(id)

### 1.6.3.3. versionNumber
#### 1.6.3.3.2. Type
integer

#### 1.6.3.3.3. Is Required
True

### 1.6.3.4. filePath
#### 1.6.3.4.2. Type
varchar

#### 1.6.3.4.3. Is Required
True

#### 1.6.3.4.4. Size
255

### 1.6.3.5. description
#### 1.6.3.5.2. Type
text

#### 1.6.3.5.3. Is Required
False

### 1.6.3.6. createdAt
#### 1.6.3.6.2. Type
timestamp

#### 1.6.3.6.3. Is Required
True


### 1.6.4. Primary Keys

- id

### 1.6.5. Unique Constraints


### 1.6.6. Indexes


## 1.7. GenerationRequest
AI creative generation request

### 1.7.3. Attributes

### 1.7.3.1. id
#### 1.7.3.1.2. Type
uuid

#### 1.7.3.1.3. Is Required
True

#### 1.7.3.1.4. Is Primary Key
True

### 1.7.3.2. userId
#### 1.7.3.2.2. Type
uuid

#### 1.7.3.2.3. Is Required
True

#### 1.7.3.2.4. Is Foreign Key
True

#### 1.7.3.2.5. Constraints

- REFERENCES User(id)

### 1.7.3.3. projectId
#### 1.7.3.3.2. Type
uuid

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Is Foreign Key
True

#### 1.7.3.3.5. Constraints

- REFERENCES Project(id)

### 1.7.3.4. prompt
#### 1.7.3.4.2. Type
text

#### 1.7.3.4.3. Is Required
True

### 1.7.3.5. styleGuidance
#### 1.7.3.5.2. Type
text

#### 1.7.3.5.3. Is Required
False

### 1.7.3.6. status
#### 1.7.3.6.2. Type
varchar

#### 1.7.3.6.3. Is Required
True

#### 1.7.3.6.4. Size
20

#### 1.7.3.6.5. Default Value
'Pending'

#### 1.7.3.6.6. Constraints

- CHECK (status IN ('Pending','Processing','Completed','Failed'))

### 1.7.3.7. creditCost
#### 1.7.3.7.2. Type
decimal

#### 1.7.3.7.3. Is Required
False

#### 1.7.3.7.4. Precision
5

#### 1.7.3.7.5. Scale
2

### 1.7.3.8. createdAt
#### 1.7.3.8.2. Type
timestamp

#### 1.7.3.8.3. Is Required
True


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints


### 1.7.6. Indexes

### 1.7.6.1. idx_generationrequest_status_createdat
#### 1.7.6.1.2. Columns

- status
- createdAt

#### 1.7.6.1.3. Type
BTree


## 1.8. GenerationResult
Output from AI generation request

### 1.8.3. Attributes

### 1.8.3.1. id
#### 1.8.3.1.2. Type
uuid

#### 1.8.3.1.3. Is Required
True

#### 1.8.3.1.4. Is Primary Key
True

### 1.8.3.2. generationRequestId
#### 1.8.3.2.2. Type
uuid

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

#### 1.8.3.2.5. Constraints

- REFERENCES GenerationRequest(id)

### 1.8.3.3. assetId
#### 1.8.3.3.2. Type
uuid

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Is Foreign Key
True

#### 1.8.3.3.5. Constraints

- REFERENCES Asset(id)

### 1.8.3.4. isSelected
#### 1.8.3.4.2. Type
boolean

#### 1.8.3.4.3. Is Required
True

#### 1.8.3.4.4. Default Value
false

### 1.8.3.5. resolution
#### 1.8.3.5.2. Type
varchar

#### 1.8.3.5.3. Is Required
True

#### 1.8.3.5.4. Size
20


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints


### 1.8.6. Indexes


## 1.9. SocialMediaConnection
User's connected social media accounts

### 1.9.3. Attributes

### 1.9.3.1. id
#### 1.9.3.1.2. Type
uuid

#### 1.9.3.1.3. Is Required
True

#### 1.9.3.1.4. Is Primary Key
True

### 1.9.3.2. userId
#### 1.9.3.2.2. Type
uuid

#### 1.9.3.2.3. Is Required
True

#### 1.9.3.2.4. Is Foreign Key
True

#### 1.9.3.2.5. Constraints

- REFERENCES User(id)

### 1.9.3.3. platform
#### 1.9.3.3.2. Type
varchar

#### 1.9.3.3.3. Is Required
True

#### 1.9.3.3.4. Size
20

#### 1.9.3.3.5. Constraints

- CHECK (platform IN ('Instagram','Facebook','LinkedIn','Twitter','Pinterest','TikTok'))

### 1.9.3.4. accessToken
#### 1.9.3.4.2. Type
text

#### 1.9.3.4.3. Is Required
True

### 1.9.3.5. externalUserId
#### 1.9.3.5.2. Type
varchar

#### 1.9.3.5.3. Is Required
True

#### 1.9.3.5.4. Size
100

### 1.9.3.6. createdAt
#### 1.9.3.6.2. Type
timestamp

#### 1.9.3.6.3. Is Required
True

### 1.9.3.7. updatedAt
#### 1.9.3.7.2. Type
timestamp

#### 1.9.3.7.3. Is Required
True


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints


### 1.9.6. Indexes


## 1.10. APIClient
API access credentials for developers

### 1.10.3. Attributes

### 1.10.3.1. id
#### 1.10.3.1.2. Type
uuid

#### 1.10.3.1.3. Is Required
True

#### 1.10.3.1.4. Is Primary Key
True

### 1.10.3.2. userId
#### 1.10.3.2.2. Type
uuid

#### 1.10.3.2.3. Is Required
True

#### 1.10.3.2.4. Is Foreign Key
True

#### 1.10.3.2.5. Constraints

- REFERENCES User(id)

### 1.10.3.3. apiKey
#### 1.10.3.3.2. Type
varchar

#### 1.10.3.3.3. Is Required
True

#### 1.10.3.3.4. Size
100

#### 1.10.3.3.5. Is Unique
True

### 1.10.3.4. secret
#### 1.10.3.4.2. Type
varchar

#### 1.10.3.4.3. Is Required
True

#### 1.10.3.4.4. Size
100

### 1.10.3.5. isActive
#### 1.10.3.5.2. Type
boolean

#### 1.10.3.5.3. Is Required
True

#### 1.10.3.5.4. Default Value
true

### 1.10.3.6. createdAt
#### 1.10.3.6.2. Type
timestamp

#### 1.10.3.6.3. Is Required
True


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints

### 1.10.5.1. uq_apiclient_apikey
#### 1.10.5.1.2. Columns

- apiKey


### 1.10.6. Indexes

### 1.10.6.1. idx_apiclient_apikey_unique
#### 1.10.6.1.2. Columns

- apiKey

#### 1.10.6.1.3. Type
BTree

#### 1.10.6.1.4. Is Unique
True


## 1.11. Subscription
User subscription details

### 1.11.3. Attributes

### 1.11.3.1. id
#### 1.11.3.1.2. Type
uuid

#### 1.11.3.1.3. Is Required
True

#### 1.11.3.1.4. Is Primary Key
True

### 1.11.3.2. userId
#### 1.11.3.2.2. Type
uuid

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Is Foreign Key
True

#### 1.11.3.2.5. Constraints

- REFERENCES User(id)

### 1.11.3.3. planId
#### 1.11.3.3.2. Type
varchar

#### 1.11.3.3.3. Is Required
True

#### 1.11.3.3.4. Size
50

### 1.11.3.4. status
#### 1.11.3.4.2. Type
varchar

#### 1.11.3.4.3. Is Required
True

#### 1.11.3.4.4. Size
20

#### 1.11.3.4.5. Default Value
'Active'

#### 1.11.3.4.6. Constraints

- CHECK (status IN ('Active','Trial','Suspended','Cancelled','Expired'))

### 1.11.3.5. currentPeriodEnd
#### 1.11.3.5.2. Type
timestamp

#### 1.11.3.5.3. Is Required
True

### 1.11.3.6. paymentProviderId
#### 1.11.3.6.2. Type
varchar

#### 1.11.3.6.3. Is Required
True

#### 1.11.3.6.4. Size
100

### 1.11.3.7. createdAt
#### 1.11.3.7.2. Type
timestamp

#### 1.11.3.7.3. Is Required
True

### 1.11.3.8. updatedAt
#### 1.11.3.8.2. Type
timestamp

#### 1.11.3.8.3. Is Required
True


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints


### 1.11.6. Indexes

### 1.11.6.1. idx_subscription_userid_currentperiodend
#### 1.11.6.1.2. Columns

- userId
- currentPeriodEnd

#### 1.11.6.1.3. Type
BTree


## 1.12. CreditTransaction
Credit usage and purchase records

### 1.12.3. Attributes

### 1.12.3.1. id
#### 1.12.3.1.2. Type
uuid

#### 1.12.3.1.3. Is Required
True

#### 1.12.3.1.4. Is Primary Key
True

### 1.12.3.2. userId
#### 1.12.3.2.2. Type
uuid

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Is Foreign Key
True

#### 1.12.3.2.5. Constraints

- REFERENCES User(id)

### 1.12.3.3. amount
#### 1.12.3.3.2. Type
decimal

#### 1.12.3.3.3. Is Required
True

#### 1.12.3.3.4. Precision
5

#### 1.12.3.3.5. Scale
2

### 1.12.3.4. actionType
#### 1.12.3.4.2. Type
varchar

#### 1.12.3.4.3. Is Required
True

#### 1.12.3.4.4. Size
50

### 1.12.3.5. generationRequestId
#### 1.12.3.5.2. Type
uuid

#### 1.12.3.5.3. Is Required
False

#### 1.12.3.5.4. Is Foreign Key
True

#### 1.12.3.5.5. Constraints

- REFERENCES GenerationRequest(id)

### 1.12.3.6. createdAt
#### 1.12.3.6.2. Type
timestamp

#### 1.12.3.6.3. Is Required
True


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes


### 1.12.7. Partitioning

- **Type:** range
- **Columns:**
  
  - createdAt
  
- **Strategy Details:** monthly or quarterly

## 1.13. Team
Collaboration group for team accounts

### 1.13.3. Attributes

### 1.13.3.1. id
#### 1.13.3.1.2. Type
uuid

#### 1.13.3.1.3. Is Required
True

#### 1.13.3.1.4. Is Primary Key
True

### 1.13.3.2. name
#### 1.13.3.2.2. Type
varchar

#### 1.13.3.2.3. Is Required
True

#### 1.13.3.2.4. Size
100

### 1.13.3.3. ownerId
#### 1.13.3.3.2. Type
uuid

#### 1.13.3.3.3. Is Required
True

#### 1.13.3.3.4. Is Foreign Key
True

#### 1.13.3.3.5. Constraints

- REFERENCES User(id)

### 1.13.3.4. createdAt
#### 1.13.3.4.2. Type
timestamp

#### 1.13.3.4.3. Is Required
True


### 1.13.4. Primary Keys

- id

### 1.13.5. Unique Constraints


### 1.13.6. Indexes


## 1.14. TeamMember
Association between users and teams

### 1.14.3. Attributes

### 1.14.3.1. id
#### 1.14.3.1.2. Type
uuid

#### 1.14.3.1.3. Is Required
True

#### 1.14.3.1.4. Is Primary Key
True

### 1.14.3.2. teamId
#### 1.14.3.2.2. Type
uuid

#### 1.14.3.2.3. Is Required
True

#### 1.14.3.2.4. Is Foreign Key
True

#### 1.14.3.2.5. Constraints

- REFERENCES Team(id)

### 1.14.3.3. userId
#### 1.14.3.3.2. Type
uuid

#### 1.14.3.3.3. Is Required
True

#### 1.14.3.3.4. Is Foreign Key
True

#### 1.14.3.3.5. Constraints

- REFERENCES User(id)

### 1.14.3.4. role
#### 1.14.3.4.2. Type
varchar

#### 1.14.3.4.3. Is Required
True

#### 1.14.3.4.4. Size
20

#### 1.14.3.4.5. Constraints

- CHECK (role IN ('Owner','Admin','Editor','Viewer'))

### 1.14.3.5. joinedAt
#### 1.14.3.5.2. Type
timestamp

#### 1.14.3.5.3. Is Required
True


### 1.14.4. Primary Keys

- id

### 1.14.5. Unique Constraints


### 1.14.6. Indexes

### 1.14.6.1. idx_teammember_userid_role
#### 1.14.6.1.2. Columns

- userId
- role

#### 1.14.6.1.3. Type
BTree


## 1.15. Session
User authentication sessions

### 1.15.3. Attributes

### 1.15.3.1. id
#### 1.15.3.1.2. Type
uuid

#### 1.15.3.1.3. Is Required
True

#### 1.15.3.1.4. Is Primary Key
True

### 1.15.3.2. userId
#### 1.15.3.2.2. Type
uuid

#### 1.15.3.2.3. Is Required
True

#### 1.15.3.2.4. Is Foreign Key
True

#### 1.15.3.2.5. Constraints

- REFERENCES User(id)

### 1.15.3.3. deviceInfo
#### 1.15.3.3.2. Type
varchar

#### 1.15.3.3.3. Is Required
True

#### 1.15.3.3.4. Size
100

### 1.15.3.4. ipAddress
#### 1.15.3.4.2. Type
varchar

#### 1.15.3.4.3. Is Required
True

#### 1.15.3.4.4. Size
45

### 1.15.3.5. lastActivity
#### 1.15.3.5.2. Type
timestamp

#### 1.15.3.5.3. Is Required
True

### 1.15.3.6. expiresAt
#### 1.15.3.6.2. Type
timestamp

#### 1.15.3.6.3. Is Required
True


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


## 1.16. Notification
System notifications for users

### 1.16.3. Attributes

### 1.16.3.1. id
#### 1.16.3.1.2. Type
uuid

#### 1.16.3.1.3. Is Required
True

#### 1.16.3.1.4. Is Primary Key
True

### 1.16.3.2. userId
#### 1.16.3.2.2. Type
uuid

#### 1.16.3.2.3. Is Required
True

#### 1.16.3.2.4. Is Foreign Key
True

#### 1.16.3.2.5. Constraints

- REFERENCES User(id)

### 1.16.3.3. type
#### 1.16.3.3.2. Type
varchar

#### 1.16.3.3.3. Is Required
True

#### 1.16.3.3.4. Size
50

### 1.16.3.4. message
#### 1.16.3.4.2. Type
text

#### 1.16.3.4.3. Is Required
True

### 1.16.3.5. isRead
#### 1.16.3.5.2. Type
boolean

#### 1.16.3.5.3. Is Required
True

#### 1.16.3.5.4. Default Value
false

### 1.16.3.6. createdAt
#### 1.16.3.6.2. Type
timestamp

#### 1.16.3.6.3. Is Required
True


### 1.16.4. Primary Keys

- id

### 1.16.5. Unique Constraints


### 1.16.6. Indexes

### 1.16.6.1. idx_notification_userid_isread_unread
#### 1.16.6.1.2. Columns

- userId
- isRead

#### 1.16.6.1.3. Type
BTree

#### 1.16.6.1.4. Condition
isRead = false


### 1.16.7. Partitioning

- **Type:** range
- **Columns:**
  
  - createdAt
  
- **Strategy Details:** monthly

## 1.17. Template
Predefined creative templates

### 1.17.3. Attributes

### 1.17.3.1. id
#### 1.17.3.1.2. Type
uuid

#### 1.17.3.1.3. Is Required
True

#### 1.17.3.1.4. Is Primary Key
True

### 1.17.3.2. name
#### 1.17.3.2.2. Type
varchar

#### 1.17.3.2.3. Is Required
True

#### 1.17.3.2.4. Size
100

### 1.17.3.3. category
#### 1.17.3.3.2. Type
varchar

#### 1.17.3.3.3. Is Required
True

#### 1.17.3.3.4. Size
50

### 1.17.3.4. previewUrl
#### 1.17.3.4.2. Type
varchar

#### 1.17.3.4.3. Is Required
True

#### 1.17.3.4.4. Size
255

### 1.17.3.5. isPublic
#### 1.17.3.5.2. Type
boolean

#### 1.17.3.5.3. Is Required
True

#### 1.17.3.5.4. Default Value
true

### 1.17.3.6. createdAt
#### 1.17.3.6.2. Type
timestamp

#### 1.17.3.6.3. Is Required
True


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




---

# 2. Relations

## 2.1. UserBrandKits
### 2.1.2. Source Entity
User

### 2.1.3. Target Entity
BrandKit

### 2.1.4. Type
OneToMany

### 2.1.5. Source Multiplicity
1

### 2.1.6. Target Multiplicity
*

### 2.1.7. Cascade Delete
True

### 2.1.8. Is Identifying
True

### 2.1.9. On Delete
Cascade

### 2.1.10. On Update
NoAction

## 2.2. UserWorkbenches
### 2.2.2. Source Entity
User

### 2.2.3. Target Entity
Workbench

### 2.2.4. Type
OneToMany

### 2.2.5. Source Multiplicity
1

### 2.2.6. Target Multiplicity
*

### 2.2.7. Cascade Delete
True

### 2.2.8. Is Identifying
True

### 2.2.9. On Delete
Cascade

### 2.2.10. On Update
NoAction

## 2.3. WorkbenchProjects
### 2.3.2. Source Entity
Workbench

### 2.3.3. Target Entity
Project

### 2.3.4. Type
OneToMany

### 2.3.5. Source Multiplicity
1

### 2.3.6. Target Multiplicity
*

### 2.3.7. Cascade Delete
True

### 2.3.8. Is Identifying
True

### 2.3.9. On Delete
Cascade

### 2.3.10. On Update
NoAction

## 2.4. ProjectAssets
### 2.4.2. Source Entity
Project

### 2.4.3. Target Entity
Asset

### 2.4.4. Type
OneToMany

### 2.4.5. Source Multiplicity
1

### 2.4.6. Target Multiplicity
*

### 2.4.7. Cascade Delete
True

### 2.4.8. Is Identifying
True

### 2.4.9. On Delete
Cascade

### 2.4.10. On Update
NoAction

## 2.5. AssetVersions
### 2.5.2. Source Entity
Asset

### 2.5.3. Target Entity
AssetVersion

### 2.5.4. Type
OneToMany

### 2.5.5. Source Multiplicity
1

### 2.5.6. Target Multiplicity
*

### 2.5.7. Cascade Delete
True

### 2.5.8. Is Identifying
True

### 2.5.9. On Delete
Cascade

### 2.5.10. On Update
NoAction

## 2.6. UserGenerationRequests
### 2.6.2. Source Entity
User

### 2.6.3. Target Entity
GenerationRequest

### 2.6.4. Type
OneToMany

### 2.6.5. Source Multiplicity
1

### 2.6.6. Target Multiplicity
*

### 2.6.7. Cascade Delete
True

### 2.6.8. Is Identifying
True

### 2.6.9. On Delete
Cascade

### 2.6.10. On Update
NoAction

## 2.7. ProjectGenerationRequests
### 2.7.2. Source Entity
Project

### 2.7.3. Target Entity
GenerationRequest

### 2.7.4. Type
OneToMany

### 2.7.5. Source Multiplicity
1

### 2.7.6. Target Multiplicity
*

### 2.7.7. Cascade Delete
True

### 2.7.8. Is Identifying
True

### 2.7.9. On Delete
Cascade

### 2.7.10. On Update
NoAction

## 2.8. GenerationRequestResults
### 2.8.2. Source Entity
GenerationRequest

### 2.8.3. Target Entity
GenerationResult

### 2.8.4. Type
OneToMany

### 2.8.5. Source Multiplicity
1

### 2.8.6. Target Multiplicity
*

### 2.8.7. Cascade Delete
True

### 2.8.8. Is Identifying
True

### 2.8.9. On Delete
Cascade

### 2.8.10. On Update
NoAction

## 2.9. GenerationResultAsset
### 2.9.2. Source Entity
GenerationResult

### 2.9.3. Target Entity
Asset

### 2.9.4. Type
OneToOne

### 2.9.5. Source Multiplicity
1

### 2.9.6. Target Multiplicity
1

### 2.9.7. Cascade Delete
True

### 2.9.8. Is Identifying
True

### 2.9.9. On Delete
Cascade

### 2.9.10. On Update
NoAction

## 2.10. UserSocialMediaConnections
### 2.10.2. Source Entity
User

### 2.10.3. Target Entity
SocialMediaConnection

### 2.10.4. Type
OneToMany

### 2.10.5. Source Multiplicity
1

### 2.10.6. Target Multiplicity
*

### 2.10.7. Cascade Delete
True

### 2.10.8. Is Identifying
True

### 2.10.9. On Delete
Cascade

### 2.10.10. On Update
NoAction

## 2.11. UserAPIClients
### 2.11.2. Source Entity
User

### 2.11.3. Target Entity
APIClient

### 2.11.4. Type
OneToMany

### 2.11.5. Source Multiplicity
1

### 2.11.6. Target Multiplicity
*

### 2.11.7. Cascade Delete
True

### 2.11.8. Is Identifying
True

### 2.11.9. On Delete
Cascade

### 2.11.10. On Update
NoAction

## 2.12. UserSubscriptions
### 2.12.2. Source Entity
User

### 2.12.3. Target Entity
Subscription

### 2.12.4. Type
OneToMany

### 2.12.5. Source Multiplicity
1

### 2.12.6. Target Multiplicity
*

### 2.12.7. Cascade Delete
True

### 2.12.8. Is Identifying
True

### 2.12.9. On Delete
Cascade

### 2.12.10. On Update
NoAction

## 2.13. UserCreditTransactions
### 2.13.2. Source Entity
User

### 2.13.3. Target Entity
CreditTransaction

### 2.13.4. Type
OneToMany

### 2.13.5. Source Multiplicity
1

### 2.13.6. Target Multiplicity
*

### 2.13.7. Cascade Delete
True

### 2.13.8. Is Identifying
True

### 2.13.9. On Delete
Cascade

### 2.13.10. On Update
NoAction

## 2.14. TeamMemberships
### 2.14.2. Source Entity
Team

### 2.14.3. Target Entity
User

### 2.14.4. Type
ManyToMany

### 2.14.5. Source Multiplicity
*

### 2.14.6. Target Multiplicity
*

### 2.14.7. Cascade Delete
False

### 2.14.8. Is Identifying
False

### 2.14.9. On Delete
SetNull

### 2.14.10. On Update
Cascade

### 2.14.11. Join Table
### 2.14.11. TeamMember
#### 2.14.11.2. Columns

- **Name:** teamId  
**Type:** UUID  
**References:** Team.id  
- **Name:** userId  
**Type:** UUID  
**References:** User.id  

## 2.15. TeamOwner
### 2.15.2. Source Entity
User

### 2.15.3. Target Entity
Team

### 2.15.4. Type
OneToMany

### 2.15.5. Source Multiplicity
1

### 2.15.6. Target Multiplicity
*

### 2.15.7. Cascade Delete
True

### 2.15.8. Is Identifying
True

### 2.15.9. On Delete
Cascade

### 2.15.10. On Update
NoAction

## 2.16. UserSessions
### 2.16.2. Source Entity
User

### 2.16.3. Target Entity
Session

### 2.16.4. Type
OneToMany

### 2.16.5. Source Multiplicity
1

### 2.16.6. Target Multiplicity
*

### 2.16.7. Cascade Delete
True

### 2.16.8. Is Identifying
True

### 2.16.9. On Delete
Cascade

### 2.16.10. On Update
NoAction

## 2.17. UserNotifications
### 2.17.2. Source Entity
User

### 2.17.3. Target Entity
Notification

### 2.17.4. Type
OneToMany

### 2.17.5. Source Multiplicity
1

### 2.17.6. Target Multiplicity
*

### 2.17.7. Cascade Delete
True

### 2.17.8. Is Identifying
True

### 2.17.9. On Delete
Cascade

### 2.17.10. On Update
NoAction

## 2.18. WorkbenchDefaultBrandKit
### 2.18.2. Source Entity
Workbench

### 2.18.3. Target Entity
BrandKit

### 2.18.4. Type
OneToOne

### 2.18.5. Source Multiplicity
0..1

### 2.18.6. Target Multiplicity
1

### 2.18.7. Cascade Delete
False

### 2.18.8. Is Identifying
False

### 2.18.9. On Delete
SetNull

### 2.18.10. On Update
Cascade

## 2.19. ProjectBrandKit
### 2.19.2. Source Entity
Project

### 2.19.3. Target Entity
BrandKit

### 2.19.4. Type
OneToOne

### 2.19.5. Source Multiplicity
0..1

### 2.19.6. Target Multiplicity
1

### 2.19.7. Cascade Delete
False

### 2.19.8. Is Identifying
False

### 2.19.9. On Delete
SetNull

### 2.19.10. On Update
Cascade

## 2.20. CreditTransactionGeneration
### 2.20.2. Source Entity
CreditTransaction

### 2.20.3. Target Entity
GenerationRequest

### 2.20.4. Type
OneToOne

### 2.20.5. Source Multiplicity
0..1

### 2.20.6. Target Multiplicity
1

### 2.20.7. Cascade Delete
False

### 2.20.8. Is Identifying
False

### 2.20.9. On Delete
SetNull

### 2.20.10. On Update
Cascade

## 2.21. UserProjectsViaDenormalizedLink
### 2.21.3. Source Entity
User

### 2.21.4. Target Entity
Project

### 2.21.5. Type
OneToMany

### 2.21.6. Source Multiplicity
1

### 2.21.7. Target Multiplicity
*

### 2.21.8. Cascade Delete
False

### 2.21.9. Is Identifying
False

### 2.21.10. On Delete
SetNull

### 2.21.11. On Update
Cascade



---

