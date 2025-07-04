# Specification

# 1. Event Driven Architecture Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-18
  - **Architecture Type:** Microservices with Event-Driven patterns
  - **Technology Stack:**
    
    - Python (FastAPI/Flask)
    - Node.js (n8n, Notification Service option)
    - Odoo 18+
    - RabbitMQ
    - PostgreSQL
    - Redis
    - React
    - Flutter
    - Kubernetes
    
  - **Bounded Contexts:**
    
    - User Account & Profile Management
    - AI Creative Generation
    - Subscription & Billing
    - Real-time Collaboration
    - Notification Management
    - API Developer Platform
    - Social Media Publishing
    
  
- **Project Specific Events:**
  
  - **Event Id:** EVT-AIGR-001  
**Event Name:** AIGenerationJobRequested  
**Event Type:** command  
**Category:** AI Generation  
**Description:** A request to initiate an AI creative generation workflow, including prompt, user context, and desired output parameters. Published by Odoo/AI Orchestration Service.  
**Trigger Condition:** User submits a creative generation request which is validated by Odoo (REQ-3-010).  
**Source Context:** Odoo Backend (via AI Generation Orchestration Service facade)  
**Target Contexts:**
    
    - n8n Workflow Engine
    
**Payload:**
    
    - **Schema:**
      
      - **User Id:** uuid
      - **Project Id:** uuid
      - **Generation Request Id:** uuid
      - **Prompt:** string
      - **Style Guidance:** string (optional)
      - **Brand Kit Id:** uuid (optional)
      - **Output Formats:**
        
        - **Platform:** string  
**Aspect Ratio:** string  
        
      - **Custom Dimensions:**
        
        - **Width:** integer
        - **Height:** integer
        - **Unit:** px
        
      - **Uploaded Image References:**
        
        - string (MinIO paths)
        
      - **Max Samples:** integer (e.g., 4)
      - **Initial Resolution:** string (e.g., '512x512')
      
    - **Required Fields:**
      
      - userId
      - projectId
      - generationRequestId
      - prompt
      - outputFormats
      - maxSamples
      - initialResolution
      
    - **Optional Fields:**
      
      - styleGuidance
      - brandKitId
      - customDimensions
      - uploadedImageReferences
      
    
**Frequency:** high  
**Business Criticality:** critical  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** GenerationRequest
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** ai.generation.request.new
    - **Exchange:** creativeflow.topic.exchange
    - **Queue:** n8n.ai.generation.queue
    
**Consumers:**
    
    - **Service:** workflow.n8n  
**Handler:** AI Generation Workflow Trigger  
**Processing Type:** async  
    
**Dependencies:**
    
    - UAPM-1-001
    - REQ-016
    - REQ-3-010
    
**Error Handling:**
    
    - **Retry Strategy:** Application-level in n8n (if initial consumption fails, RabbitMQ retries based on ack timeout)
    - **Dead Letter Queue:** n8n.ai.generation.dlq
    - **Timeout Ms:** 300000
    
  - **Event Id:** EVT-AIGR-002  
**Event Name:** AIGenerationSamplesReady  
**Event Type:** domain  
**Category:** AI Generation  
**Description:** Indicates that low-resolution AI-generated samples are ready for user review. Published by n8n.  
**Trigger Condition:** n8n workflow completes sample generation (REQ-3-008, REQ-3-011).  
**Source Context:** n8n Workflow Engine  
**Target Contexts:**
    
    - Notification Service
    - Odoo Backend (via AI Generation Orchestration Service or dedicated consumer)
    
**Payload:**
    
    - **Schema:**
      
      - **Generation Request Id:** uuid
      - **User Id:** uuid
      - **Project Id:** uuid
      - **Sample Asset Ids:**
        
        - uuid
        
      - **Sample Previews:**
        
        - **Asset Id:** uuid  
**Preview Url:** string (MinIO path)  
        
      - **Credits Consumed:** decimal
      
    - **Required Fields:**
      
      - generationRequestId
      - userId
      - projectId
      - sampleAssetIds
      - samplePreviews
      
    - **Optional Fields:**
      
      - creditsConsumed
      
    
**Frequency:** high  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** GenerationResult, Asset
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** ai.generation.samples.ready
    - **Exchange:** creativeflow.topic.exchange
    - **Queue:** notification.service.queue (and) odoo.updates.queue
    
**Consumers:**
    
    - **Service:** services.notification  
**Handler:** NotifyUserOfSamplesHandler  
**Processing Type:** async  
    - **Service:** business.odoo (or services.aigeneration acting as consumer)  
**Handler:** UpdateOdooWithSampleMetadataHandler  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-3-011
    - REQ-016
    
**Error Handling:**
    
    - **Retry Strategy:** Consumer-defined retry logic (e.g., 3 retries with exponential backoff)
    - **Dead Letter Queue:** notification.service.dlq (and) odoo.updates.dlq
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-SUB-001  
**Event Name:** SubscriptionTierChanged  
**Event Type:** domain  
**Category:** Subscription & Billing  
**Description:** Indicates a user's subscription tier has changed (e.g., upgraded, downgraded, cancelled, expired). Published by Odoo/Subscription & Billing Service.  
**Trigger Condition:** User completes subscription change, or automated billing cycle event occurs (REQ-6-006).  
**Source Context:** business.odoo (or services.subscriptionbilling)  
**Target Contexts:**
    
    - Authentication & Authorization Service
    - User Account & Profile Service
    - Notification Service
    
**Payload:**
    
    - **Schema:**
      
      - **User Id:** uuid
      - **Old Subscription Tier:** string
      - **New Subscription Tier:** string
      - **Change Effective Date:** timestamp
      - **Reason:** string (e.g., 'user_upgrade', 'payment_failure_cancellation')
      
    - **Required Fields:**
      
      - userId
      - newSubscriptionTier
      - changeEffectiveDate
      
    - **Optional Fields:**
      
      - oldSubscriptionTier
      - reason
      
    
**Frequency:** medium  
**Business Criticality:** critical  
**Data Source:**
    
    - **Database:** PostgreSQL (synced from Odoo)
    - **Table:** User, Subscription
    - **Operation:** update
    
**Routing:**
    
    - **Routing Key:** user.subscription.changed
    - **Exchange:** creativeflow.topic.exchange
    - **Queue:** auth.service.queue (and) userprofile.service.queue (and) notification.service.queue
    
**Consumers:**
    
    - **Service:** services.auth  
**Handler:** UpdateUserPermissionsHandler  
**Processing Type:** async  
    - **Service:** services.usermanagement  
**Handler:** UpdateUserProfileDisplayHandler  
**Processing Type:** async  
    - **Service:** services.notification  
**Handler:** NotifyUserOfSubscriptionChangeHandler  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-6-006
    - REQ-2-008
    
**Error Handling:**
    
    - **Retry Strategy:** Consumer-defined retry logic (e.g., 3 retries with exponential backoff)
    - **Dead Letter Queue:** domain.events.dlq
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-AUTH-001  
**Event Name:** UserRegisteredNeedsVerification  
**Event Type:** domain  
**Category:** Authentication  
**Description:** A new user has registered via email and requires email verification. Published by Authentication Service.  
**Trigger Condition:** User completes email-based registration form (UAPM-1-001).  
**Source Context:** services.auth  
**Target Contexts:**
    
    - Notification Service
    
**Payload:**
    
    - **Schema:**
      
      - **User Id:** uuid
      - **Email:** string
      - **Verification Token:** string
      - **Full Name:** string (optional)
      
    - **Required Fields:**
      
      - userId
      - email
      - verificationToken
      
    - **Optional Fields:**
      
      - fullName
      
    
**Frequency:** medium  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** User
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** user.auth.verification.required
    - **Exchange:** creativeflow.topic.exchange
    - **Queue:** notification.service.queue
    
**Consumers:**
    
    - **Service:** services.notification  
**Handler:** SendVerificationEmailHandler  
**Processing Type:** async  
    
**Dependencies:**
    
    - UAPM-1-001
    
**Error Handling:**
    
    - **Retry Strategy:** 3 retries with exponential backoff (Notification Service consumer)
    - **Dead Letter Queue:** notification.service.dlq
    - **Timeout Ms:** 120000
    
  
- **Event Types And Schema Design:**
  
  - **Essential Event Types:**
    
    - **Event Name:** AIGenerationLifecycleEvent  
**Category:** domain  
**Description:** Events related to the AI creative generation pipeline (Requested, SamplesReady, FinalAssetReady, Failed).  
**Priority:** high  
    - **Event Name:** UserAccountActivityEvent  
**Category:** domain  
**Description:** Events concerning user account lifecycle (RegisteredNeedsVerification, EmailVerified, PasswordResetTokenGenerated, ProfileUpdated).  
**Priority:** high  
    - **Event Name:** SubscriptionLifecycleEvent  
**Category:** domain  
**Description:** Events related to user subscription changes (TierChanged, PaymentSucceeded, PaymentFailed, InvoiceReadyForUser).  
**Priority:** critical  
    - **Event Name:** CollaborationSessionEvent  
**Category:** integration  
**Description:** Events for notifying users about real-time collaboration updates (e.g., UserJoinedSession, EditConflictRequiresResolution - used by Notification Service, not for direct CRDT sync).  
**Priority:** medium  
    - **Event Name:** APIDeveloperNotificationEvent  
**Category:** integration  
**Description:** Internal event indicating an asynchronous API operation (e.g., AI generation via API) is complete, for triggering external webhooks.  
**Priority:** medium  
    
  - **Schema Design:**
    
    - **Format:** JSON
    - **Reasoning:** Widely supported, human-readable, good compatibility with web technologies (Python, Node.js, RabbitMQ). Specified architecture primarily uses REST APIs internally and externally which commonly use JSON.
    - **Consistency Approach:** Standardized base event structure (eventId, eventType, timestamp, source, version, correlationId) with a specific 'data' payload for each event type.
    
  - **Schema Evolution:**
    
    - **Backward Compatibility:** True
    - **Forward Compatibility:** False
    - **Strategy:** Additive changes preferred. For breaking changes, introduce new event versions (e.g., eventName_v2). Consumers should be tolerant to new, unknown fields.
    
  - **Event Structure:**
    
    - **Standard Fields:**
      
      - eventId (UUID)
      - eventType (string)
      - eventTimestamp (ISO8601 UTC)
      - eventVersion (integer)
      - sourceService (string)
      - correlationId (UUID)
      - userId (UUID, if applicable)
      
    - **Metadata Requirements:**
      
      - Trace context for distributed tracing (OpenTelemetry standard).
      
    
  
- **Event Routing And Processing:**
  
  - **Routing Mechanisms:**
    
    - **Type:** RabbitMQ Topic Exchange  
**Description:** Primary mechanism for asynchronous inter-service communication and task queuing (CPIO-007, REQ-3-010).  
**Use Case:** AI Generation Pipeline, Subscription Updates, User Lifecycle Notifications.  
    - **Type:** Redis Pub/Sub (Optional)  
**Description:** Potential for high-throughput, low-latency notifications if RabbitMQ overhead is too high for specific internal notifications (CPIO-006, CPIO-009). Focus on RabbitMQ for essential.  
**Use Case:** Simple real-time status updates to Notification Service (less critical than core tasks).  
    
  - **Processing Patterns:**
    
    - **Pattern:** sequential  
**Applicable Scenarios:**
    
    - AI creative generation workflow stages managed by n8n (REQ-3-001 to REQ-3-013).
    
**Implementation:** n8n workflow design.  
    - **Pattern:** parallel  
**Applicable Scenarios:**
    
    - Notification Service consuming events to notify multiple users or process different types of notifications independently.
    
**Implementation:** Multiple consumers or concurrent processing within a consumer service.  
    - **Pattern:** saga  
**Applicable Scenarios:**
    
    - User registration (account creation, initial subscription setup, email verification - UAPM-1-001).
    - Subscription management (plan change, payment, invoicing, permission update - REQ-6-006).
    
**Implementation:** Choreographed saga using events published/consumed by Odoo, Subscription & Billing Service, Auth Service, Notification Service.  
    
  - **Filtering And Subscription:**
    
    - **Filtering Mechanism:** RabbitMQ routing keys and binding keys for topic exchanges.
    - **Subscription Model:** Consumers subscribe to specific queues bound to exchanges with relevant routing key patterns.
    - **Routing Keys:**
      
      - e.g., ai.generation.*, user.account.*, billing.subscription.*, notification.trigger.*
      
    
  - **Handler Isolation:**
    
    - **Required:** True
    - **Approach:** Microservices act as isolated handlers. n8n workflows are also isolated processing units.
    - **Reasoning:** Ensures fault tolerance and independent scalability of event consumers as per microservice architecture.
    
  - **Delivery Guarantees:**
    
    - **Level:** at-least-once
    - **Justification:** Ensures no critical business events are lost. Idempotent consumers or robust duplicate detection/handling is required.
    - **Implementation:** RabbitMQ publisher confirms and consumer acknowledgements. Persistent queues.
    
  
- **Event Storage And Replay:**
  
  - **Persistence Requirements:**
    
    - **Required:** True
    - **Duration:** RabbitMQ: Until consumed and acknowledged, or moved to DLQ. Logs/DB: As per data retention policies (Section 7.5, MON-007).
    - **Reasoning:** Message durability for RabbitMQ. Long-term storage for audit/compliance in operational databases and logs.
    
  - **Event Sourcing:**
    
    - **Necessary:** False
    - **Justification:** The current architecture and requirements indicate state-oriented persistence (REQ-DA-001 to REQ-DA-006). Event sourcing would be an expansion of scope beyond what is strictly essential for the described system. Audit logs and state change history in operational tables provide sufficient traceability for now.
    - **Scope:**
      
      
    
  - **Technology Options:**
    
    - **Technology:** RabbitMQ  
**Suitability:** high  
**Reasoning:** Explicitly specified for AI job queues and as an option for Notification Service. Supports persistent messaging and DLQs.  
    - **Technology:** PostgreSQL (for audit/state)  
**Suitability:** high  
**Reasoning:** Primary RDBMS, suitable for storing state derived from events or logs of processed events.  
    
  - **Replay Capabilities:**
    
    - **Required:** False
    - **Scenarios:**
      
      - Not essential for core functionality based on current requirements. Replay would typically be for recovery from major data corruption or re-deriving state, which is beyond the described immediate needs. Reprocessing from DLQ is a form of limited replay for failed messages.
      
    - **Implementation:** N/A for full event stream replay. DLQ reprocessing is the primary mechanism.
    
  - **Retention Policy:**
    
    - **Strategy:** Message broker: Short-term, until processed. Logs/Databases: Governed by system-wide data retention policies (Section 7.5, MON-007).
    - **Duration:** Varies by data type as per Section 7.5.
    - **Archiving Approach:** As per Section 7.5 and backup strategy (SREDRP-008).
    
  
- **Dead Letter Queue And Error Handling:**
  
  - **Dead Letter Strategy:**
    
    - **Approach:** RabbitMQ Dead Letter Exchange (DLX) and Dead Letter Queue (DLQ) for unprocessable messages.
    - **Queue Configuration:** Dedicated DLQs per primary queue or shared DLQ with routing key for origin.
    - **Processing Logic:** Manual or semi-automated review and reprocessing/discarding of messages from DLQ. Alerting on DLQ size.
    
  - **Retry Policies:**
    
    - **Error Type:** Transient n8n/AI Model communication failure  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Delay Configuration:** Initial 1s, multiplier 2, max 60s (handled within n8n or consumer).  
    - **Error Type:** Notification delivery failure (transient)  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Delay Configuration:** Initial 5s, multiplier 2, max 120s (handled by Notification Service).  
    - **Error Type:** Database optimistic locking conflict  
**Max Retries:** 2  
**Backoff Strategy:** fixed  
**Delay Configuration:** 100ms (handled by service layer)  
    
  - **Poison Message Handling:**
    
    - **Detection Mechanism:** Message moves to DLQ after exceeding max retry attempts by the consumer or RabbitMQ.
    - **Handling Strategy:** Isolate in DLQ, investigate root cause, potentially discard or manually remediate data and re-queue.
    - **Alerting Required:** True
    
  - **Error Notification:**
    
    - **Channels:**
      
      - Prometheus Alertmanager to PagerDuty/Slack/Email (as per MON-012, QA-003.1)
      
    - **Severity:** critical|warning
    - **Recipients:**
      
      - DevOps/SRE On-call
      - Relevant Development Team
      
    
  - **Recovery Procedures:**
    
    - **Scenario:** Message in DLQ due to transient downstream service outage  
**Procedure:** Wait for service recovery, then re-queue messages from DLQ using RabbitMQ management tools or custom scripts.  
**Automation Level:** semi-automated  
    - **Scenario:** Message in DLQ due to persistent data issue/bug  
**Procedure:** Analyze message payload, identify data issue or bug, deploy fix, manually remediate data if needed, then decide on re-queue or discard.  
**Automation Level:** manual  
    
  
- **Event Versioning Strategy:**
  
  - **Schema Evolution Approach:**
    
    - **Strategy:** Primarily additive changes to JSON payloads. For breaking changes, a new event type version will be introduced (e.g., `OrderCreated_v2`).
    - **Versioning Scheme:** Semantic versioning for event schemas is not strictly required for initial phase; simple integer suffix (e.g., _v2, _v3) or a 'version' field in event header/payload is sufficient.
    - **Migration Strategy:** Consumers to be updated to handle new versions. Old versions might be supported for a transition period if necessary.
    
  - **Compatibility Requirements:**
    
    - **Backward Compatible:** True
    - **Forward Compatible:** False
    - **Reasoning:** Consumers should be tolerant of new fields they don't understand (backward compatibility). Forward compatibility (old consumer understanding new event) is harder and often not a primary goal without a schema registry and more complex logic.
    
  - **Version Identification:**
    
    - **Mechanism:** Event 'type' string (e.g., `com.creativeflow.user.registered.v1`) or a dedicated 'version' field in event metadata.
    - **Location:** header|payload|both
    - **Format:** Integer or semantic-like string (e.g., '1', '1.0').
    
  - **Consumer Upgrade Strategy:**
    
    - **Approach:** Phased rollout of new consumer versions. Old consumers might continue processing older event versions or route them to DLQ if incompatible.
    - **Rollout Strategy:** Blue/green or canary deployments for consumer services.
    - **Rollback Procedure:** Revert consumer service to previous version that handles older event schemas.
    
  - **Schema Registry:**
    
    - **Required:** False
    - **Technology:** N/A for initial essential scope. Consider for future if event schema complexity and number of types grow significantly.
    - **Governance:** N/A
    
  
- **Event Monitoring And Observability:**
  
  - **Monitoring Capabilities:**
    
    - **Capability:** RabbitMQ Queue Metrics (depth, message rates, consumer count, ack rates)  
**Justification:** Essential for understanding message flow, identifying bottlenecks, and ensuring broker health (CPIO-007, MON-010).  
**Implementation:** Prometheus RabbitMQ exporter, Grafana dashboards.  
    - **Capability:** n8n Workflow Execution Metrics (success/failure rates, duration)  
**Justification:** Critical for AI generation pipeline monitoring (REQ-SSPE-019, MON-010).  
**Implementation:** n8n internal metrics endpoint scraped by Prometheus, or custom logging parsed by ELK/Loki.  
    - **Capability:** Event Consumer Service Performance (processing time, error rates)  
**Justification:** To ensure event handlers are performing within SLOs.  
**Implementation:** Application-level metrics exposed via Prometheus client libraries.  
    
  - **Tracing And Correlation:**
    
    - **Tracing Required:** True
    - **Correlation Strategy:** Unique Correlation ID generated at the start of a request/flow and propagated through all subsequent events and service calls (MON-005).
    - **Trace Id Propagation:** Via event headers (e.g., `X-Correlation-ID`) and OpenTelemetry context propagation.
    
  - **Performance Metrics:**
    
    - **Metric:** End-to-end event processing latency (from publish to final consumption)  
**Threshold:** Varies by event type (e.g., <1s for notifications, <N mins for AI gen steps)  
**Alerting:** True  
    - **Metric:** Message throughput per queue/topic  
**Threshold:** Monitor for significant deviations from baseline  
**Alerting:** True  
    - **Metric:** DLQ size  
**Threshold:** >0 (for critical queues) or >N (for others)  
**Alerting:** True  
    
  - **Event Flow Visualization:**
    
    - **Required:** True
    - **Tooling:** Distributed tracing tools (Jaeger/Zipkin via OpenTelemetry - MON-008). Log analysis tools (Kibana/Grafana Loki) using correlation IDs.
    - **Scope:** Critical business flows like AI generation, user registration, subscription changes.
    
  - **Alerting Requirements:**
    
    - **Condition:** RabbitMQ queue depth exceeds X for Y minutes  
**Severity:** warning|critical  
**Response Time:** Defined in QA-003.1 Escalation Matrix  
**Escalation Path:**
    
    - DevOps/SRE
    - Relevant Dev Team
    
    - **Condition:** Event processing error rate for a specific consumer > Z%  
**Severity:** critical  
**Response Time:** Defined in QA-003.1  
**Escalation Path:**
    
    - Relevant Dev Team
    - DevOps/SRE
    
    - **Condition:** DLQ message count > N  
**Severity:** warning|critical  
**Response Time:** Defined in QA-003.1  
**Escalation Path:**
    
    - DevOps/SRE
    - Relevant Dev Team
    
    - **Condition:** AI Generation failure rate > X% (MON-013)  
**Severity:** critical  
**Response Time:** Defined in QA-003.1  
**Escalation Path:**
    
    - AI/ML Team
    - DevOps/SRE
    
    
  
- **Implementation Priority:**
  
  - **Component:** RabbitMQ Setup (Exchanges, Core Queues, DLQs for AI Generation)  
**Priority:** high  
**Dependencies:**
    
    - infra.core
    
**Estimated Effort:** Medium  
  - **Component:** Core Event Definitions & Schemas (AI Gen, User Lifecycle, Subscription)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
  - **Component:** Producer/Consumer Logic in Key Services (Odoo, n8n, Auth, Notification, Billing)  
**Priority:** high  
**Dependencies:**
    
    - RabbitMQ Setup
    - Core Event Definitions
    
**Estimated Effort:** High  
  - **Component:** Basic Event Monitoring & Alerting (Queue Depths, Error Rates)  
**Priority:** medium  
**Dependencies:**
    
    - RabbitMQ Setup
    - Prometheus/Grafana
    
**Estimated Effort:** Medium  
  - **Component:** Event Versioning Strategy (initial implementation)  
**Priority:** medium  
**Dependencies:**
    
    - Core Event Definitions
    
**Estimated Effort:** Low  
  
- **Risk Assessment:**
  
  - **Risk:** Message loss due to improper RabbitMQ configuration or consumer error handling.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Use persistent messages, publisher confirms, consumer acknowledgements, robust DLQ strategy, idempotent consumers.  
  - **Risk:** Inconsistent event schemas leading to deserialization errors.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Standardized base event structure, versioning strategy, thorough testing of event contracts.  
  - **Risk:** Alert fatigue from poorly tuned monitoring or DLQ alerts.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Regular review and tuning of alert thresholds (MON-012), clear escalation paths, effective DLQ processing SOPs.  
  - **Risk:** Bottlenecks in event processing (e.g., slow consumers, RabbitMQ performance limits).  
**Impact:** high  
**Probability:** low  
**Mitigation:** Load testing, capacity planning for RabbitMQ and consumer services, monitoring consumer lag and processing times, horizontal scaling of consumers.  
  
- **Recommendations:**
  
  - **Category:** Messaging Infrastructure  
**Recommendation:** Prioritize robust RabbitMQ clustering (mirrored queues - CPIO-007) and persistence configuration for all business-critical event flows.  
**Justification:** Ensures high availability and durability of messages, which is crucial for core operations like AI generation and billing.  
**Priority:** high  
  - **Category:** Developer Practices  
**Recommendation:** Mandate idempotent design for all event consumers to safely handle at-least-once delivery and potential retries.  
**Justification:** Prevents data corruption or unintended side effects from processing duplicate messages, simplifying error recovery.  
**Priority:** high  
  - **Category:** Observability  
**Recommendation:** Implement distributed tracing with correlation IDs across all event-driven interactions from day one.  
**Justification:** Essential for debugging complex asynchronous flows and understanding system behavior in a microservices environment (MON-005, MON-008).  
**Priority:** high  
  - **Category:** Schema Management  
**Recommendation:** Adopt a simple event versioning approach initially (e.g., version field in header/payload or event type suffix) and document all event schemas thoroughly. Defer a full schema registry until complexity demands it.  
**Justification:** Balances the need for schema evolution with minimizing initial overhead, aligning with the 'essential only' principle.  
**Priority:** medium  
  


---

