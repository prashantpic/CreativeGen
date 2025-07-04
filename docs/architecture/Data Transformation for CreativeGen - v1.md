# Specification

# 1. Data Transformation Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-18
  - **Technology Stack:**
    
    - Python (FastAPI/Flask)
    - Node.js (n8n, Notification Service)
    - Odoo 18+
    - RabbitMQ
    - PostgreSQL 16+
    - Redis
    - MinIO
    - React 19+
    - TypeScript
    - Flutter 3.19+
    - Dart
    - Kubernetes (K3s/RKE2/K8s)
    - Docker
    - Nginx
    - Cloudflare
    - Ansible
    - OpenAI API
    - Stability AI API
    - Stripe SDK
    - PayPal SDK
    - HashiCorp Vault
    - Prometheus
    - Grafana
    - ELK/Loki
    - OpenTelemetry
    - Yjs
    
  - **Service Interfaces:**
    
    - WebApp/MobileApp to API Gateway (REST/GraphQL)
    - API Gateway to Backend Microservices (REST/gRPC)
    - Inter-Microservice Communication (REST, RabbitMQ events)
    - n8n to AI Services (HTTP/SDK)
    - Services to Databases (SQL, S3 API, Redis API)
    - Services to Odoo (XML-RPC/JSON-RPC)
    - Services to Payment Gateways (SDK/HTTP)
    - Services to Social Media APIs (SDK/HTTP)
    - Services to Analytics Platforms (SDK/HTTP)
    
  - **Data Models:**
    
    - User
    - BrandKit
    - Workbench
    - Project
    - Asset
    - AssetVersion
    - GenerationRequest
    - GenerationResult
    - SocialMediaConnection
    - APIClient
    - Subscription
    - CreditTransaction
    - Team
    - TeamMember
    - Session
    - Notification
    - Template (DB models)
    - Event Payloads (RabbitMQ)
    - API DTOs (REST/GraphQL)
    
  
- **Data Mapping Strategy:**
  
  - **Essential Mappings:**
    
    - **Mapping Id:** M001  
**Source:** Odoo (Generation Job Data)  
**Target:** n8n Workflow (AIGenerationJobRequested Event)  
**Transformation:** direct  
**Configuration:**
    
    - **Source Format:** Odoo internal representation or BillingAPI DTO
    - **Target Format:** JSON (AIGenerationJobRequested schema)
    
**Mapping Technique:** Object-to-object mapping, potentially via an adapter service.  
**Justification:** REQ-3-010: Odoo backend publishes a job message to RabbitMQ for n8n.  
**Complexity:** medium  
    - **Mapping Id:** M002  
**Source:** n8n Workflow (Sample Generation Output)  
**Target:** Notification Service & Odoo (AIGenerationSamplesReady Event)  
**Transformation:** direct  
**Configuration:**
    
    - **Source Format:** n8n internal output structure
    - **Target Format:** JSON (AIGenerationSamplesReady schema)
    
**Mapping Technique:** Object-to-object mapping within n8n or an intermediary service.  
**Justification:** REQ-3-011: n8n informs Notification Service and Odoo backend about samples.  
**Complexity:** medium  
    - **Mapping Id:** M003  
**Source:** n8n Workflow (Final Asset Output)  
**Target:** MinIO & PostgreSQL (Asset/GenerationResult entities)  
**Transformation:** direct  
**Configuration:**
    
    - **Source Format:** n8n internal output for final asset
    - **Target Format:** Asset binary to MinIO, metadata to PostgreSQL Asset/GenerationResult tables
    
**Mapping Technique:** File storage and object-to-object mapping for metadata.  
**Justification:** REQ-3-012: Final asset stored in MinIO, metadata in DB.  
**Complexity:** medium  
    - **Mapping Id:** M004  
**Source:** User Profile UI (Web/Mobile)  
**Target:** User Account & Profile Service (Update DTO)  
**Transformation:** direct  
**Configuration:**
    
    - **Source Format:** UI form data
    - **Target Format:** JSON (UserProfileUpdateDTO)
    
**Mapping Technique:** Direct field mapping.  
**Justification:** UAPM-1-003: Users manage their profile.  
**Complexity:** simple  
    - **Mapping Id:** M005  
**Source:** Odoo (Subscription Change Data)  
**Target:** Platform Services (SubscriptionTierChanged Event)  
**Transformation:** direct  
**Configuration:**
    
    - **Source Format:** Odoo subscription model
    - **Target Format:** JSON (SubscriptionTierChanged schema)
    
**Mapping Technique:** Object-to-object mapping via Subscription & Billing Service adapter.  
**Justification:** REQ-6-006: Subscription lifecycle management communicated to platform.  
**Complexity:** medium  
    - **Mapping Id:** M006  
**Source:** Platform Internal Events (User Activity, Revenue)  
**Target:** Third-Party Analytics (GA4, Mixpanel/Amplitude, Firebase Schemas)  
**Transformation:** adapter  
**Configuration:**
    
    - **Source Format:** Internal event/data structures
    - **Target Format:** Specific schemas for each analytics platform SDK
    
**Mapping Technique:** Service adapter per analytics platform, mapping internal events to platform-specific event structures.  
**Justification:** REQ-11-001 to REQ-11-005: Integration with various analytics platforms.  
**Complexity:** medium  
    
  - **Object To Object Mappings:**
    
    - **Source Object:** GenerationRequest (DB Entity)  
**Target Object:** AIGenerationJobRequested (Event Payload)  
**Field Mappings:**
    
    - **Source Field:** id  
**Target Field:** generationRequestId  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    - **Source Field:** userId  
**Target Field:** userId  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    - **Source Field:** projectId  
**Target Field:** projectId  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    - **Source Field:** prompt  
**Target Field:** prompt  
**Transformation:** direct  
**Data Type Conversion:** text_to_string  
    
    - **Source Object:** User (DB Entity)  
**Target Object:** UserProfileDTO (API Response)  
**Field Mappings:**
    
    - **Source Field:** id  
**Target Field:** id  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    - **Source Field:** fullName  
**Target Field:** fullName  
**Transformation:** direct  
**Data Type Conversion:** varchar_to_string  
    - **Source Field:** email  
**Target Field:** email  
**Transformation:** direct  
**Data Type Conversion:** varchar_to_string  
    - **Source Field:** subscriptionTier  
**Target Field:** subscriptionTier  
**Transformation:** direct  
**Data Type Conversion:** varchar_to_string  
    - **Source Field:** creditBalance  
**Target Field:** creditBalance  
**Transformation:** direct  
**Data Type Conversion:** decimal_to_number_or_string  
    
    - **Source Object:** WebhookEventData (Internal)  
**Target Object:** ExternalWebhookPayload (HTTP POST to User)  
**Field Mappings:**
    
    - **Source Field:** jobId  
**Target Field:** job_id  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    - **Source Field:** status  
**Target Field:** status  
**Transformation:** direct  
**Data Type Conversion:** string_to_string  
    - **Source Field:** assetUrl  
**Target Field:** asset_url  
**Transformation:** direct  
**Data Type Conversion:** string_to_string  
    
    
  - **Data Type Conversions:**
    
    - **From:** DB:timestamp  
**To:** JSON:string (ISO8601 UTC)  
**Conversion Method:** Standard library date/time formatting.  
**Validation Required:** False  
    - **From:** DB:uuid  
**To:** JSON:string  
**Conversion Method:** UUID to string conversion.  
**Validation Required:** False  
    - **From:** DB:json  
**To:** Application:dict/object (Python/JS)  
**Conversion Method:** JSON parsing.  
**Validation Required:** True  
    - **From:** DB:decimal  
**To:** JSON:number or string  
**Conversion Method:** Decimal to number/string, ensuring precision for currency.  
**Validation Required:** False  
    
  - **Bidirectional Mappings:**
    
    - **Entity:** User  
**Forward Mapping:** M004 (UI to Service)  
**Reverse Mapping:** DBUserToUserProfileDTO  
**Consistency Strategy:** Service layer updates DB, cache invalidation updates cached views.  
    - **Entity:** BrandKit  
**Forward Mapping:** UI form data to BrandKit DTO  
**Reverse Mapping:** BrandKit DB entity to BrandKit DTO  
**Consistency Strategy:** Service layer updates DB.  
    
  
- **Schema Validation Requirements:**
  
  - **Field Level Validations:**
    
    - **Field:** User.email  
**Rules:**
    
    - required
    - unique
    - valid_email_format
    - max_length:255
    
**Priority:** critical  
**Error Message:** Invalid or already registered email address.  
    - **Field:** User.passwordHash (on registration)  
**Rules:**
    
    - required_if_not_social_login
    - min_length:12
    - complexity_rules (uppercase, lowercase, number, special_char)
    
**Priority:** critical  
**Error Message:** Password does not meet complexity requirements.  
    - **Field:** GenerationRequest.prompt  
**Rules:**
    
    - required
    - max_length:4000 (example)
    
**Priority:** high  
**Error Message:** Prompt is required and cannot exceed 4000 characters.  
    - **Field:** BrandKit.name  
**Rules:**
    
    - required
    - max_length:100
    
**Priority:** high  
**Error Message:** Brand kit name is required.  
    - **Field:** Subscription.status  
**Rules:**
    
    - enum:Active,Trial,Suspended,Cancelled,Expired
    
**Priority:** critical  
**Error Message:** Invalid subscription status.  
    - **Field:** CreditTransaction.amount  
**Rules:**
    
    - numeric
    - precision:5,2
    
**Priority:** critical  
**Error Message:** Invalid credit amount.  
    - **Field:** APIClient.apiKey  
**Rules:**
    
    - required
    - unique
    - fixed_length:64 (example)
    
**Priority:** critical  
**Error Message:** Invalid or duplicate API key.  
    
  - **Cross Field Validations:**
    
    - **Validation Id:** V001  
**Fields:**
    
    - User.isEmailVerified
    - User.subscriptionTier
    
**Rule:** If subscriptionTier is not 'Free', isEmailVerified must be true.  
**Condition:** User attempts to access paid features.  
**Error Handling:** Block access, prompt for email verification (UAPM-1-001).  
    - **Validation Id:** V002  
**Fields:**
    
    - GenerationRequest.creditCost
    - User.creditBalance
    
**Rule:** User.creditBalance must be >= GenerationRequest.creditCost (if action is credit-based and user not on unlimited plan for this action).  
**Condition:** Before initiating a credit-consuming AI generation.  
**Error Handling:** Prevent action, prompt to buy credits or upgrade (REQ-6-008).  
    
  - **Business Rule Validations:**
    
    - **Rule Id:** BR001  
**Description:** Free tier monthly generation limit.  
**Fields:**
    
    - User.subscriptionTier
    - User.monthlyGenerationCount (hypothetical tracking field or derived from usage_logs)
    
**Logic:** If User.subscriptionTier is 'Free', ensure User.monthlyGenerationCount < 100.  
**Priority:** high  
    - **Rule Id:** BR002  
**Description:** Brand Kit access for Pro+ users only.  
**Fields:**
    
    - User.subscriptionTier
    - BrandKit.userId
    
**Logic:** If User.subscriptionTier is 'Free', deny Brand Kit creation/modification.  
**Priority:** high  
    - **Rule Id:** BR003  
**Description:** MFA enabled for Pro+ accounts requires MFA verification at login.  
**Fields:**
    
    - User.subscriptionTier
    - User.isMFAEnabled
    - LoginAttempt.mfaToken
    
**Logic:** If User.isMFAEnabled is true (and tier is Pro+), mfaToken must be valid.  
**Priority:** critical  
    
  - **Conditional Validations:**
    
    - **Condition:** User.subscriptionTier == 'Free'  
**Applicable Fields:**
    
    - Export.resolution
    
**Validation Rules:**
    
    - max_resolution:HD_watermarked (example)
    
    - **Condition:** AI Generation Request.outputFormat == 'Custom'  
**Applicable Fields:**
    
    - AI Generation Request.customDimensions.width
    - AI Generation Request.customDimensions.height
    
**Validation Rules:**
    
    - required
    - integer
    - min:50
    - max:4096
    
    
  - **Validation Groups:**
    
    - **Group Name:** UserRegistration  
**Validations:**
    
    - User.email
    - User.passwordHash (if applicable)
    
**Execution Order:** 1  
**Stop On First Failure:** True  
    - **Group Name:** AIGenerationStart  
**Validations:**
    
    - GenerationRequest.prompt
    - V002 (credit check)
    
**Execution Order:** 1  
**Stop On First Failure:** True  
    
  
- **Transformation Pattern Evaluation:**
  
  - **Selected Patterns:**
    
    - **Pattern:** adapter  
**Use Case:** Integrating with external services (Odoo, Payment Gateways, Social Media APIs, AI Models, Analytics Platforms).  
**Implementation:** Dedicated service modules or classes that translate requests and responses between the internal system and the external API's contract.  
**Justification:** Necessary for decoupling the core system from the specifics of external APIs (REQ-6-019, AISIML-001, SMPIO-001 etc., REQ-11-001 etc.).  
    - **Pattern:** converter  
**Use Case:** Data type transformations (e.g., DB timestamp to JSON ISO8601 string, UUID to string) and simple DTO to Entity mapping.  
**Implementation:** Utility functions or built-in features of ORMs/serialization libraries.  
**Justification:** Common requirement for data exchange between layers and systems.  
    - **Pattern:** pipeline  
**Use Case:** AI Creative Generation Workflow.  
**Implementation:** n8n workflow engine orchestrating multiple steps: data preprocessing, AI model calls, result processing, notification.  
**Justification:** REQ-3-001 to REQ-3-013 explicitly describe a multi-step generation process managed by n8n.  
    
  - **Pipeline Processing:**
    
    - **Required:** True
    - **Stages:**
      
      - **Stage:** RequestValidation (Odoo/AI Orchestration Service)  
**Transformation:** Validate user inputs, credits, subscription.  
**Dependencies:**
    
    
      - **Stage:** JobDispatch (Odoo/AI Orchestration Service)  
**Transformation:** Format job payload for n8n.  
**Dependencies:**
    
    - RequestValidation
    
      - **Stage:** N8N_DataPreprocessing  
**Transformation:** Prepare inputs for AI model.  
**Dependencies:**
    
    - JobDispatch
    
      - **Stage:** N8N_AIModelInteraction  
**Transformation:** Call external/internal AI model(s).  
**Dependencies:**
    
    - N8N_DataPreprocessing
    
      - **Stage:** N8N_SampleProcessing  
**Transformation:** Generate low-res previews, store metadata.  
**Dependencies:**
    
    - N8N_AIModelInteraction
    
      - **Stage:** N8N_FinalAssetProcessing (if sample selected)  
**Transformation:** Generate high-res asset, store.  
**Dependencies:**
    
    - N8N_AIModelInteraction (or selected sample data)
    
      
    - **Parallelization:** True
    
  - **Processing Mode:**
    
    - **Real Time:**
      
      - **Required:** True
      - **Scenarios:**
        
        - User authentication & authorization
        - User profile updates
        - Real-time collaboration edits
        - API Gateway request processing
        - Notification delivery (WebSocket)
        
      - **Latency Requirements:** <200ms for UI interactions, <500ms for API calls (REQ-WCI-002, REQ-SSPE-003)
      
    - **Batch:**
      
      - **Required:** False
      - **Batch Size:** 0
      - **Frequency:** 
      - **Notes:** While daily backups (SREDRP-008) and DR sync (CPIO-020) happen, they are more operational tasks than core data transformations for this analysis. Analytics aggregation might be batch, but event forwarding is primary.
      
    - **Streaming:**
      
      - **Required:** False
      - **Streaming Framework:** 
      - **Notes:** Not explicitly required for core data transformations based on current SRS.
      
    
  - **Canonical Data Model:**
    
    - **Applicable:** False
    - **Scope:**
      
      
    - **Benefits:**
      
      
    - **Justification:** While beneficial for very large, complex systems, the current microservice architecture with well-defined event schemas and API DTOs should suffice for the initial phases. Introducing a canonical model would add overhead without clear immediate essential justification from the requirements.
    
  
- **Version Handling Strategy:**
  
  - **Schema Evolution:**
    
    - **Strategy:** Additive changes for non-breaking updates. New event type versions (e.g., `event_v2`) or API versions (e.g., `/v2/endpoint`) for breaking changes.
    - **Versioning Scheme:** Integer for event versions (e.g., `AIGenerationJobRequested_v1`), Semantic Versioning (Major.Minor) for APIs (e.g. `/api/v1/users`).
    - **Compatibility:**
      
      - **Backward:** True
      - **Forward:** False
      - **Reasoning:** Consumers should tolerate new, optional fields. Forward compatibility is complex and not an initial priority.
      
    
  - **Transformation Versioning:**
    
    - **Mechanism:** n8n workflows versioned in Git. Adapter service code versioned in Git.
    - **Version Identification:** Git commit hashes and release tags.
    - **Migration Strategy:** Deploy new versions of n8n workflows or adapter services. For DB schema, use Flyway/Liquibase (REQ-DA-014).
    
  - **Data Model Changes:**
    
    - **Migration Path:** Automated schema migrations using Flyway/Liquibase (REQ-DA-014). Data migration scripts for complex data transformations if needed.
    - **Rollback Strategy:** Automated rollback for application deployments (REQ-20-006). Database migration rollbacks are complex; focus on forward-only migrations with thorough testing. Manual intervention for critical DB rollback if absolutely necessary.
    - **Validation Strategy:** Testing migrations in staging, pre-deployment data validation checks.
    
  - **Schema Registry:**
    
    - **Required:** False
    - **Technology:** 
    - **Governance:** 
    - **Justification:** Not essential for the initial scope given the number of distinct event types and services. Can be considered later if event-driven complexity significantly increases.
    
  
- **Performance Optimization:**
  
  - **Critical Requirements:**
    
    - **Operation:** AI Sample Generation Transformation (Odoo to n8n job, n8n to SamplesReady event)  
**Max Latency:** Part of the <30s P90 (REQ-SSPE-001)  
**Throughput Target:** Part of 1000 gen req/min (REQ-SSPE-005)  
**Justification:** User-facing, critical path for core functionality.  
    - **Operation:** API Gateway Request/Response Transformation (if any complex aggregation)  
**Max Latency:** Part of <500ms API response (REQ-SSPE-003)  
**Throughput Target:** 10,000 concurrent users (REQ-SSPE-005)  
**Justification:** Impacts all API consumers.  
    
  - **Parallelization Opportunities:**
    
    - **Transformation:** n8n AI Generation Workflows  
**Parallelization Strategy:** Multiple n8n workers consuming from RabbitMQ queue.  
**Expected Gain:** Improved throughput for AI generation.  
    - **Transformation:** Analytics Event Forwarding (M006)  
**Parallelization Strategy:** Asynchronous processing of internal events to forward to multiple analytics platforms.  
**Expected Gain:** Decoupling and resilience in analytics data pipeline.  
    
  - **Caching Strategies:**
    
    - **Cache Type:** Redis  
**Cache Scope:** User Profile (partial - UAPM-1-005), Frequently Accessed Templates, Session Data (REQ-DA-003)  
**Eviction Policy:** LRU/TTL  
**Applicable Transformations:**
    
    - DBUserToUserProfileDTO (cached DTO)
    - Template DB Entity to Template DTO
    
    
  - **Memory Optimization:**
    
    - **Techniques:**
      
      - Efficient data structures in Python/Node.js services
      - Streaming for large file processing in n8n (if handling direct uploads for AI)
      - Optimized JSON serialization/deserialization
      
    - **Thresholds:** Monitor service memory usage against defined limits (CPIO-003, DEP-001)
    - **Monitoring Required:** True
    
  - **Lazy Evaluation:**
    
    - **Applicable:** False
    - **Scenarios:**
      
      
    - **Implementation:** 
    - **Justification:** Not identified as an essential optimization for core transformations in the initial phase.
    
  - **Bulk Processing:**
    
    - **Required:** False
    - **Batch Sizes:**
      
      - **Optimal:** 0
      - **Maximum:** 0
      
    - **Parallelism:** 0
    - **Justification:** No explicit bulk data transformation tasks are central to the described system's core workflows that would require specific bulk transformation patterns beyond standard DB batch operations or file processing.
    
  
- **Error Handling And Recovery:**
  
  - **Error Handling Strategies:**
    
    - **Error Type:** External AI Service API Error (e.g., OpenAI, Stability AI)  
**Strategy:** Retry (with exponential backoff), fallback to alternative provider/model (if configured in n8n/AISIML-002), log error, notify user with actionable message (AISIML-005, REQ-3-006).  
**Fallback Action:** Use alternative AI model or inform user of feature unavailability.  
**Escalation Path:**
    
    - n8n workflow log
    - AI Orchestration Service log
    - Alert to Ops/Dev (MON-013)
    
    - **Error Type:** Payment Gateway Error (Stripe/PayPal)  
**Strategy:** Log error, inform user, retry for transient errors, manage via Odoo failed payment logic (REQ-6-016).  
**Fallback Action:** Subscription status update (e.g., to suspended), dunning process.  
**Escalation Path:**
    
    - Odoo/Subscription Service log
    - Alert to Finance/Support Team
    
    - **Error Type:** RabbitMQ Message Processing Failure (in consumer)  
**Strategy:** Acknowledge failure after max retries, move to DLQ.  
**Fallback Action:** Message investigated from DLQ, manual intervention or re-queue after fix.  
**Escalation Path:**
    
    - Consumer service log
    - DLQ monitoring alert to Ops/Dev (MON-012)
    
    - **Error Type:** Data Validation Error (API input, event payload)  
**Strategy:** Reject request/event, log error, return specific error message to client/producer.  
**Fallback Action:** Client/producer handles error (e.g., display validation message to user).  
**Escalation Path:**
    
    - Service log
    - Potentially track high rates of specific validation errors.
    
    
  - **Logging Requirements:**
    
    - **Log Level:** Configurable per environment (INFO for prod, DEBUG for dev/staging) - MON-005.
    - **Included Data:**
      
      - Timestamp
      - Correlation ID
      - Service Name
      - User ID (if applicable)
      - Event/Request details (anonymized PII)
      - Error message
      - Stack trace (for errors)
      
    - **Retention Period:** As per system-wide log retention policies (MON-007, Section 7.5).
    - **Alerting:** True
    
  - **Partial Success Handling:**
    
    - **Strategy:** For AI sample generation (REQ-3-008), if some samples succeed but others fail, return successful samples and indicate failures for others. For Sagas, implement compensating transactions.
    - **Reporting Mechanism:** Return partial results with error details for failed parts; log comprehensively.
    - **Recovery Actions:**
      
      - User can retry failed parts if applicable
      - Compensating transactions for failed Saga steps.
      
    
  - **Circuit Breaking:**
    
    - **Dependency:** OpenAI API  
**Threshold:** 5 consecutive errors or >50% error rate in 1 minute  
**Timeout:** 30 seconds  
**Fallback Strategy:** Switch to Stability AI (if configured for task) or return error (AISIML-005).  
    - **Dependency:** Stripe API  
**Threshold:** 3 consecutive errors  
**Timeout:** 60 seconds  
**Fallback Strategy:** Log error, mark payment as pending investigation, notify admin (REQ-6-016).  
    
  - **Retry Strategies:**
    
    - **Operation:** Call to external AI model (n8n)  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Retry Conditions:**
    
    - Transient HTTP errors (502, 503, 504)
    - Rate limit exceeded (with appropriate delay)
    
    - **Operation:** Message consumption from RabbitMQ (by consumer)  
**Max Retries:** 2  
**Backoff Strategy:** fixed  
**Retry Conditions:**
    
    - Transient database connection error
    - Temporary downstream service unavailability
    
    - **Operation:** Webhook delivery (REQ-7-004)  
**Max Retries:** 5  
**Backoff Strategy:** exponential  
**Retry Conditions:**
    
    - HTTP errors from user's endpoint (5xx, timeout)
    
    
  - **Error Notifications:**
    
    - **Condition:** DLQ message count > 0 for critical queues  
**Recipients:**
    
    - DevOps On-Call
    - Relevant Dev Team
    
**Severity:** critical  
**Channel:** PagerDuty/Slack (MON-012)  
    - **Condition:** AI Generation failure rate > 5% in 1 hour  
**Recipients:**
    
    - AI/ML Team
    - DevOps On-Call
    
**Severity:** high  
**Channel:** PagerDuty/Slack (MON-013)  
    - **Condition:** External API (OpenAI, Stripe) sustained error rate > 10% for 15 mins  
**Recipients:**
    
    - DevOps On-Call
    - Integration Team
    
**Severity:** high  
**Channel:** PagerDuty/Slack  
    
  
- **Project Specific Transformations:**
  
  ### .1. Odoo Job to n8n AI Generation Event
  Transforms data from Odoo (likely via AI Generation Orchestration Service) representing an AI creative generation request into a structured event message for consumption by the n8n workflow engine.

  #### .1.1. Transformation Id
  PST-001

  #### .1.4. Source
  
  - **Service:** business.odoo (via services.aigeneration)
  - **Model:** Odoo Job Data / Internal DTO
  - **Fields:**
    
    - userId
    - projectId
    - promptText
    - stylePreferences
    - brandKitDetails
    - outputFormatRequirements
    - maxSamples
    - initialResolution
    
  
  #### .1.5. Target
  
  - **Service:** workflow.n8n
  - **Model:** AIGenerationJobRequested Event (RabbitMQ JSON payload)
  - **Fields:**
    
    - userId
    - projectId
    - generationRequestId
    - prompt
    - styleGuidance
    - brandKitId
    - outputFormats
    - customDimensions
    - uploadedImageReferences
    - maxSamples
    - initialResolution
    
  
  #### .1.6. Transformation
  
  - **Type:** nested
  - **Logic:** Map Odoo fields to the AIGenerationJobRequested event schema. Complex objects like brandKitDetails might need to be transformed into simpler references (brandKitId) or structured JSON. Output formats may need parsing and structuring.
  - **Configuration:**
    
    - **Field Mappings:**
      
      - **User Id:** userId
      - **Project Id:** projectId
      - **Prompt Text:** prompt
      
    - **Complex Mappings:**
      
      - **Brand Kit Details:** brandKitId (lookup or pass-through)
      - **Output Format Requirements:** outputFormats (array of objects)
      
    
  
  #### .1.7. Frequency
  real-time (event-driven)

  #### .1.8. Criticality
  critical

  #### .1.9. Dependencies
  
  - REQ-3-010
  - services.aigeneration
  
  #### .1.10. Validation
  
  - **Pre Transformation:**
    
    - Odoo data validation (user credits, subscription status)
    
  - **Post Transformation:**
    
    - RabbitMQ message schema validation (against AIGenerationJobRequested schema)
    
  
  #### .1.11. Performance
  
  - **Expected Volume:** Up to 1000 requests/min (REQ-SSPE-005)
  - **Latency Requirement:** Low (part of initial API response or quick handoff to async process)
  - **Optimization Strategy:** Efficient serialization, minimal blocking operations in adapter.
  
  ### .2. n8n AI Sample Output to Platform Event
  Transforms the raw output from an n8n AI sample generation workflow (which includes paths to generated sample images in MinIO and metadata) into a structured AIGenerationSamplesReady event.

  #### .2.1. Transformation Id
  PST-002

  #### .2.4. Source
  
  - **Service:** workflow.n8n
  - **Model:** n8n Workflow Output (JSON or internal object)
  - **Fields:**
    
    - generationRequestId
    - userId
    - projectId
    - generatedSamplePaths (MinIO)
    - sampleMetadata (resolution, format)
    - creditsConsumedEstimate
    
  
  #### .2.5. Target
  
  - **Service:** services.notification, business.odoo (via services.aigeneration)
  - **Model:** AIGenerationSamplesReady Event (RabbitMQ JSON payload)
  - **Fields:**
    
    - generationRequestId
    - userId
    - projectId
    - sampleAssetIds
    - samplePreviews
    - creditsConsumed
    
  
  #### .2.6. Transformation
  
  - **Type:** nested
  - **Logic:** Map n8n output fields to the AIGenerationSamplesReady event schema. Create Asset entities in DB for samples and get their UUIDs for sampleAssetIds. Construct preview URLs from MinIO paths.
  - **Configuration:**
    
    - **Field Mappings:**
      
      - **Generation Request Id:** generationRequestId
      
    - **Complex Mappings:**
      
      - **Generated Sample Paths + Sample Metadata:** sampleAssetIds (after DB insert), samplePreviews (array of objects)
      
    
  
  #### .2.7. Frequency
  real-time (event-driven)

  #### .2.8. Criticality
  critical

  #### .2.9. Dependencies
  
  - REQ-3-011
  - workflow.n8n
  
  #### .2.10. Validation
  
  - **Pre Transformation:**
    
    - n8n workflow success validation
    
  - **Post Transformation:**
    
    - RabbitMQ message schema validation
    
  
  #### .2.11. Performance
  
  - **Expected Volume:** Up to 1000 events/min (tied to generation requests)
  - **Latency Requirement:** Low (for timely user notification)
  - **Optimization Strategy:** Efficient metadata processing, batch DB inserts for samples if possible (though likely per-request).
  
  ### .3. User Registration Input to Auth Service
  Transforms user input from web/mobile registration forms into a structured request for the Authentication Service.

  #### .3.1. Transformation Id
  PST-003

  #### .3.4. Source
  
  - **Service:** presentation.webapp / presentation.mobileapp
  - **Model:** UI Registration Form Data
  - **Fields:**
    
    - email
    - password
    - fullName (optional)
    - socialProvider (optional)
    - socialToken (optional)
    
  
  #### .3.5. Target
  
  - **Service:** services.auth
  - **Model:** UserRegistrationRequest DTO
  - **Fields:**
    
    - email
    - password
    - fullName
    - isSocialLogin
    - socialProvider
    - socialAccessToken
    
  
  #### .3.6. Transformation
  
  - **Type:** direct
  - **Logic:** Direct mapping of UI fields to Auth Service DTO. Handles conditional logic for social vs. email registration.
  - **Configuration:**
    
    - **Field Mappings:**
      
      - **Email:** email
      - **Password:** password
      
    
  
  #### .3.7. Frequency
  real-time

  #### .3.8. Criticality
  critical

  #### .3.9. Dependencies
  
  - UAPM-1-001
  - REQ-2-001
  
  #### .3.10. Validation
  
  - **Pre Transformation:**
    
    - Client-side form validation (basic)
    
  - **Post Transformation:**
    
    - Auth Service input DTO validation (comprehensive)
    
  
  #### .3.11. Performance
  
  - **Expected Volume:** High during peak registration periods
  - **Latency Requirement:** <200ms for UI submission, <500ms for Auth service processing
  - **Optimization Strategy:** Efficient request serialization.
  
  ### .4. Odoo Subscription Data to Platform Subscription Event
  Transforms subscription data changes from Odoo (e.g., tier change, renewal, cancellation) into a SubscriptionTierChanged event for internal platform services.

  #### .4.1. Transformation Id
  PST-004

  #### .4.4. Source
  
  - **Service:** business.odoo (via services.subscriptionbilling adapter)
  - **Model:** Odoo Subscription Object / Internal DTO
  - **Fields:**
    
    - userId (mapped)
    - newPlanId
    - oldPlanId
    - status
    - effectiveDate
    - reasonCode
    
  
  #### .4.5. Target
  
  - **Service:** services.auth, services.usermanagement, services.notification
  - **Model:** SubscriptionTierChanged Event (RabbitMQ JSON payload)
  - **Fields:**
    
    - userId
    - oldSubscriptionTier
    - newSubscriptionTier
    - changeEffectiveDate
    - reason
    
  
  #### .4.6. Transformation
  
  - **Type:** direct
  - **Logic:** Map Odoo subscription fields (possibly via an adapter service that translates Odoo plan IDs to platform tier names) to the standardized SubscriptionTierChanged event schema.
  - **Configuration:**
    
    - **Field Mappings:**
      
      - **User Id:** userId
      - **New Plan Id:** newSubscriptionTier (with mapping logic)
      
    
  
  #### .4.7. Frequency
  real-time (event-driven on Odoo changes)

  #### .4.8. Criticality
  critical

  #### .4.9. Dependencies
  
  - REQ-6-006
  - services.subscriptionbilling
  
  #### .4.10. Validation
  
  - **Pre Transformation:**
    
    - Validation of Odoo data integrity
    
  - **Post Transformation:**
    
    - RabbitMQ message schema validation
    
  
  #### .4.11. Performance
  
  - **Expected Volume:** Medium
  - **Latency Requirement:** Low for timely permission updates and notifications
  - **Optimization Strategy:** Efficient event publishing.
  
  ### .5. Platform Event to Analytics Event (Generic Adapter)
  Generic transformation pattern representing mapping internal platform events (e.g., 'CreativeGenerated', 'UserSubscribed') to the specific event schemas required by third-party analytics platforms (GA4, Mixpanel/Amplitude, Firebase).

  #### .5.1. Transformation Id
  PST-005

  #### .5.4. Source
  
  - **Service:** various internal services (e.g., services.aigeneration, services.subscriptionbilling)
  - **Model:** Internal Platform Event (JSON)
  - **Fields:**
    
    - eventType
    - timestamp
    - userId
    - eventData (map/object)
    
  
  #### .5.5. Target
  
  - **Service:** services.analyticsforwarding (then to external platforms)
  - **Model:** Analytics Platform Specific Event Schema (e.g., GA4 event, Mixpanel event)
  - **Fields:**
    
    - Varies per platform: e.g., GA4: event_name, params{...}; Mixpanel: event, properties{...}
    
  
  #### .5.6. Transformation
  
  - **Type:** adapter
  - **Logic:** Each analytics platform integration will have its own adapter logic. This involves: 1. Identifying relevant internal events. 2. Mapping internal event names and data to the target analytics platform's event naming conventions and property structures. 3. Handling any data type or format conversions required by the analytics SDK. 4. Ensuring PII is not sent unless explicitly configured and compliant (REQ-11-001 to REQ-11-005).
  - **Configuration:**
    
    - **Platform Specific Mappings:**
      
      - **Ga4:**
        
        - **Internal Event Name A:** ga4_event_x
        - **Internal Property1:** ga4_param_y
        
      - **Mixpanel:**
        
        - **Internal Event Name B:** mixpanel_event_z
        - **Internal Property2:** mixpanel_prop_w
        
      
    
  
  #### .5.7. Frequency
  real-time (event-driven)

  #### .5.8. Criticality
  medium

  #### .5.9. Dependencies
  
  - REQ-11-001
  - REQ-11-002
  - REQ-11-003
  - REQ-11-004
  - REQ-11-005
  - services.analyticsforwarding
  
  #### .5.10. Validation
  
  - **Pre Transformation:**
    
    - Internal event data validation
    
  - **Post Transformation:**
    
    - Validation against analytics platform SDKs (often implicit via SDK usage)
    
  
  #### .5.11. Performance
  
  - **Expected Volume:** High (many user interactions)
  - **Latency Requirement:** Non-blocking to core user flows; async forwarding preferred.
  - **Optimization Strategy:** Asynchronous event forwarding, batching if supported by analytics SDKs and appropriate.
  
  
- **Implementation Priority:**
  
  - **Component:** PST-001 (Odoo Job to n8n AI Generation Event)  
**Priority:** high  
**Dependencies:**
    
    - RabbitMQ
    - Odoo
    - n8n
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** PST-002 (n8n AI Sample Output to Platform Event)  
**Priority:** high  
**Dependencies:**
    
    - RabbitMQ
    - n8n
    - Notification Service
    - Odoo
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** PST-003 (User Registration Input to Auth Service)  
**Priority:** high  
**Dependencies:**
    
    - WebApp/MobileApp
    - Auth Service
    
**Estimated Effort:** Low  
**Risk Level:** low  
  - **Component:** PST-004 (Odoo Subscription Data to Platform Subscription Event)  
**Priority:** high  
**Dependencies:**
    
    - RabbitMQ
    - Odoo
    - Auth Service
    - User Management Service
    - Notification Service
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Data Type Converters (Timestamp, UUID, Decimal, JSON)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Low  
**Risk Level:** low  
  - **Component:** Core Field Level Validations (User, GenerationRequest)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Adapter for OpenAI/StabilityAI (within n8n or AI Orchestration)  
**Priority:** high  
**Dependencies:**
    
    - AISIML-001
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** PST-005 (Platform Event to Analytics Event - initial GA4/Mixpanel setup)  
**Priority:** medium  
**Dependencies:**
    
    - Analytics Forwarding Service
    - GA4/Mixpanel SDKs
    
**Estimated Effort:** High  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Inconsistent data mapping between services leading to processing errors or data corruption.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Clear schema definitions for events and DTOs, contract testing (REQ-QAS-006), robust validation at consumer side.  
**Contingency Plan:** Manual data correction, re-processing of events from DLQ after fixing mapping logic.  
  - **Risk:** Performance bottlenecks in critical transformation steps affecting user experience or system throughput.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Performance testing of transformation logic, caching strategies for repeatable transformations, asynchronous processing for non-critical path transformations.  
**Contingency Plan:** Optimize transformation code, scale transformation services, implement circuit breakers for slow downstream dependencies.  
  - **Risk:** Schema evolution breaking existing transformations or consumers.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Backward-compatible changes where possible, versioning for events and APIs, consumer tolerance for new fields, phased rollout of changes.  
**Contingency Plan:** Rollback to previous version of service/transformation logic, support multiple event versions temporarily.  
  - **Risk:** Failure to handle errors during transformation leading to data loss or inconsistent state.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Comprehensive error handling, retry mechanisms for transient errors, use of DLQs for unprocessable messages, idempotent operations.  
**Contingency Plan:** Investigate DLQ messages, identify root cause, fix, and reprocess or manually resolve.  
  
- **Recommendations:**
  
  - **Category:** Schema Management  
**Recommendation:** Establish and enforce clear, versioned schemas (e.g., JSON Schema) for all inter-service event payloads and API DTOs. Store these in a shared, accessible location (e.g., Git repository).  
**Justification:** Reduces ambiguity, facilitates easier development and testing of transformations, and helps manage schema evolution. Essential for a microservices architecture.  
**Priority:** high  
**Implementation Notes:** Use code generation from schemas where possible to ensure consistency.  
  - **Category:** Testing  
**Recommendation:** Implement contract testing (e.g., using Pact or Spring Cloud Contract if applicable to stack) for critical service-to-service interactions, especially those involving event transformations.  
**Justification:** Ensures that producers and consumers adhere to agreed-upon data contracts, preventing integration issues when services evolve independently (REQ-QAS-006).  
**Priority:** high  
**Implementation Notes:** Integrate contract tests into CI/CD pipelines.  
  - **Category:** Idempotency  
**Recommendation:** Design all event consumers and transformation handlers to be idempotent, particularly those processing messages from RabbitMQ or handling retries.  
**Justification:** Prevents duplicate processing and data corruption in case of message redelivery or retries, which is crucial for at-least-once delivery guarantees (as per Event Delivery Guarantees).  
**Priority:** high  
**Implementation Notes:** Use unique transaction IDs or check for existing state before processing.  
  - **Category:** Monitoring & Alerting  
**Recommendation:** Implement detailed monitoring and alerting for transformation processes, including error rates, processing latencies, and queue depths for event-driven transformations.  
**Justification:** Enables proactive identification of issues in transformation pipelines, helping to meet performance NFRs and quickly address failures. Aligns with MON-010, MON-011.  
**Priority:** high  
**Implementation Notes:** Utilize Prometheus for metrics and Grafana for dashboards; configure alerts in Alertmanager/Grafana.  
  - **Category:** Simplicity  
**Recommendation:** Favor simpler, direct mappings and stateless transformations where possible. Avoid overly complex transformation logic within a single service or step.  
**Justification:** Improves maintainability, testability, and performance. Complex transformations can often be broken down into smaller, manageable steps in a pipeline (e.g., within n8n).  
**Priority:** medium  
**Implementation Notes:** If a transformation becomes too complex, consider if it indicates a need for a dedicated transformation service or a change in data models.  
  


---

