# Architecture Design Specification

# 1. Components

- **Components:**
  
  ### .1. Web Application Frontend
  User-facing web interface built as a Progressive Web App (PWA) for creative generation and platform management. Renders UI, handles user interactions, communicates with backend APIs, manages client-state, and implements PWA features.

  #### .1.4. Type
  ClientApplication

  #### .1.5. Dependencies
  
  - api-gateway-003
  - notification-service-012
  - collaboration-service-011
  
  #### .1.6. Properties
  
  - **Version:** 1.0.0
  - **Framework:** React 19+
  
  #### .1.7. Interfaces
  
  - **Name:** UserInteraction  
**Type:** UI/UX  
**Operations:**
    
    - DisplayDashboard
    - OpenEditor
    - ManageProfile
    
**Visibility:** Public  
  
  #### .1.8. Technology
  React 19+, TypeScript, HTML5, CSS3, PWA (Service Workers, Manifest), Redux/Zustand, React Router, Axios/Fetch API

  #### .1.9. Resources
  
  - **Cpu:** N/A (Client-side)
  - **Memory:** N/A (Client-side)
  - **Storage:** Browser Cache
  
  #### .1.10. Configuration
  
  - **Api Base Path:** /api/v1
  - **Websocket Url:** wss://host/notifications
  
  #### .1.11. Health Check
  None

  #### .1.12. Responsible Features
  
  - REQ-WCI-001
  - REQ-WCI-002
  - REQ-WCI-003
  - REQ-WCI-004
  - REQ-WCI-005
  - REQ-WCI-006
  - REQ-WCI-007
  - REQ-WCI-008
  - REQ-WCI-009
  - REQ-WCI-010
  - REQ-WCI-011
  - REQ-WCI-012
  - UAPM-1-001
  - UAPM-1-003
  - UAPM-1-004
  - UAPM-1-005
  - UAPM-1-008
  - UAPM-1-009
  - REQ-4-001
  - REQ-4-002
  - REQ-4-003
  - REQ-4-004
  - REQ-4-005
  - REQ-4-007
  - REQ-4-008
  - REQ-4-009
  - REQ-5-001
  - REQ-6-005
  - REQ-6-007
  - REQ-7-005
  - REQ-9-005
  - REQ-9-006
  - REQ-9-008
  - SMPIO-009
  - SMPIO-010
  - SMPIO-012
  - SMPIO-013
  - REQ-14-001
  - REQ-14-002
  - REQ-14-003
  - REQ-14-004
  - REQ-14-005
  - REQ-14-008
  - REQ-14-009
  - REQ-14-010
  - REQ-14-012
  - PLI-001
  - PLI-002
  - PLI-005
  - PLI-006
  - PLI-007
  
  #### .1.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .2. Mobile Applications (iOS & Android)
  Native mobile applications for on-the-go creative work and platform access. Provides touch-optimized workflows, offline editing, device feature integration, and push notifications.

  #### .2.4. Type
  ClientApplication

  #### .2.5. Dependencies
  
  - api-gateway-003
  - notification-service-012
  - collaboration-service-011
  
  #### .2.6. Properties
  
  - **Version:** 1.0.0
  - **Framework:** Flutter 3.19+
  
  #### .2.7. Interfaces
  
  - **Name:** UserInteractionMobile  
**Type:** UI/UX  
**Operations:**
    
    - MobileEditCreative
    - SyncOfflineData
    - CaptureMedia
    
**Visibility:** Public  
  
  #### .2.8. Technology
  Flutter 3.19+, Dart, Native Platform Integration (Camera, Push Notifications via APNS/FCM), SQLite (Drift/Moor), Mobile Analytics SDK (Firebase, Mixpanel/Amplitude)

  #### .2.9. Resources
  
  - **Cpu:** N/A (Client-side)
  - **Memory:** N/A (Client-side)
  - **Storage:** Device Storage
  
  #### .2.10. Configuration
  
  - **Api Base Path:** /api/v1
  - **Websocket Url:** wss://host/notifications
  
  #### .2.11. Health Check
  None

  #### .2.12. Responsible Features
  
  - REQ-8-001
  - REQ-8-002
  - REQ-8-003
  - REQ-8-004
  - REQ-8-005
  - REQ-8-006
  - REQ-8-007
  - REQ-8-008
  - REQ-8-009
  - REQ-14-001
  - REQ-14-002
  - REQ-14-003
  - REQ-14-006
  - REQ-14-007
  - REQ-14-011
  - REQ-14-012
  - PLI-001
  - PLI-002
  - PLI-005
  - PLI-006
  - PLI-007
  
  #### .2.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .3. API Gateway
  Centralized entry point for all API requests from web, mobile, and third-party developers. Handles routing, authentication, authorization, rate limiting, and request/response transformation.

  #### .3.4. Type
  APIGateway

  #### .3.5. Dependencies
  
  - auth-service-004
  - user-profile-service-005
  - brand-kit-service-006
  - project-management-service-007
  - ai-generation-orchestration-service-008
  - subscription-billing-adapter-service-009
  - developer-platform-service-010
  - collaboration-service-011
  - social-publishing-service-013
  - customer-support-adapter-service-016
  - forum-service-017
  
  #### .3.6. Properties
  
  - **Version:** 1.0.0
  
  #### .3.7. Interfaces
  
  - **Name:** ClientFacingAPI  
**Type:** RESTful HTTP/S  
**Operations:**
    
    - All public API operations exposed to clients
    
**Visibility:** Public  
  
  #### .3.8. Technology
  Nginx (with OpenResty/Lua scripting), Kong, or KrakenD. Integrates with Authentication Service for token validation.

  #### .3.9. Resources
  
  - **Cpu:** 4 cores
  - **Memory:** 8GB
  - **Network:** 10Gbps
  
  #### .3.10. Configuration
  
  - **Max Connections:** 5000
  - **Timeout:** 10s
  - **Rate Limit Default:** 100req/min
  
  #### .3.11. Health Check
  
  - **Path:** /_gateway_health
  - **Interval:** 30
  - **Timeout:** 3
  
  #### .3.12. Responsible Features
  
  - REQ-2-004
  - REQ-2-005
  - REQ-2-006
  - UAPM-1-008
  - REQ-7-003
  - PMDT-001
  - CPIO-002
  
  #### .3.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .4. Authentication & Authorization Service
  Handles user authentication (email/password, social login), MFA, password management, session management (JWTs), OAuth token storage, and RBAC.

  #### .4.4. Type
  Service

  #### .4.5. Dependencies
  
  - postgresql-database-023
  - redis-cache-025
  - secrets-management-service-022
  - rabbitmq-broker-026
  
  #### .4.6. Properties
  
  - **Version:** 1.0.0
  
  #### .4.7. Interfaces
  
  - **Name:** AuthAPI  
**Type:** Internal REST API  
**Operations:**
    
    - RegisterUser
    - LoginUser
    - VerifyEmail
    - ManageMFA
    - ResetPassword
    - RefreshToken
    - ValidateToken
    - RevokeSession
    - GetDeviceSessions
    
**Visibility:** Internal  
  
  #### .4.8. Technology
  Python (FastAPI/Flask), OAuth 2.0/OpenID Connect libraries, JWT libraries, bcrypt/Argon2

  #### .4.9. Resources
  
  - **Cpu:** 2 cores
  - **Memory:** 4GB
  
  #### .4.10. Configuration
  
  - **Jwt Secret Key Path:** /secrets/jwt_secret
  - **Token Expiration Access:** 15m
  - **Token Expiration Refresh:** 7d
  - **Mfa Code Validity:** 5m
  - **Email Verification Link Validity:** 72h
  - **Max Concurrent Sessions:** 5
  
  #### .4.11. Health Check
  
  - **Path:** /health
  - **Interval:** 30
  - **Timeout:** 5
  
  #### .4.12. Responsible Features
  
  - UAPM-1-001
  - UAPM-1-002
  - UAPM-1-006
  - UAPM-1-008
  - REQ-2-001
  - REQ-2-002
  - REQ-2-003
  - REQ-2-004
  - REQ-2-006
  - REQ-2-007
  - REQ-2-008
  - REQ-2-009
  - REQ-2-010
  - REQ-2-011
  - REQ-2-012
  - REQ-3516
  - REQ-3517
  - REQ-3518
  - REQ-3519
  - REQ-3521
  - REQ-3522
  - REQ-3523
  - REQ-3524
  - REQ-3525
  - REQ-3526
  - REQ-3527
  - SMPIO-007
  
  #### .4.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .5. User Account & Profile Service
  Manages user profiles, preferences, data privacy rights (GDPR/CCPA), consent management, and team role display. Also displays aggregated account-related info.

  #### .5.4. Type
  Service

  #### .5.5. Dependencies
  
  - postgresql-database-023
  - subscription-billing-adapter-service-009
  
  #### .5.6. Properties
  
  - **Version:** 1.0.0
  
  #### .5.7. Interfaces
  
  - **Name:** UserProfileAPI  
**Type:** Internal REST API  
**Operations:**
    
    - GetUserProfile
    - UpdateUserProfile
    - RequestDataExport
    - DeleteAccountData
    - ManageConsent
    - GetUserAccountInfo
    
**Visibility:** Internal  
  
  #### .5.8. Technology
  Python (FastAPI/Flask)

  #### .5.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .5.10. Configuration
  
  - **Profile Picture Max Size Mb:** 5
  - **Default Language:** en-US
  
  #### .5.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .5.12. Responsible Features
  
  - UAPM-1-001
  - UAPM-1-003
  - UAPM-1-005
  - UAPM-1-007
  - UAPM-1-009
  - UAPM-1-010
  - REQ-DA-004
  - REQ-DA-017
  - SPR-001
  - SPR-002
  
  #### .5.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .6. Brand Kit Service
  Manages Brand Kits for Pro+ users, including colors, fonts, logos, and style preferences.

  #### .6.4. Type
  Service

  #### .6.5. Dependencies
  
  - postgresql-database-023
  - minio-object-storage-024
  - auth-service-004
  
  #### .6.6. Properties
  
  - **Version:** 1.0.0
  
  #### .6.7. Interfaces
  
  - **Name:** BrandKitAPI  
**Type:** Internal REST API  
**Operations:**
    
    - CreateBrandKit
    - GetBrandKit
    - UpdateBrandKit
    - DeleteBrandKit
    - ListBrandKits
    - SetDefaultBrandKit
    
**Visibility:** Internal  
  
  #### .6.8. Technology
  Python (FastAPI/Flask)

  #### .6.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .6.10. Configuration
  
  - **Max Logos Per Kit:** 10
  - **Max Custom Fonts Per Kit:** 5
  
  #### .6.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .6.12. Responsible Features
  
  - UAPM-1-004
  - REQ-DA-004
  
  #### .6.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  - **Allowed Roles:**
    
    - Pro
    - Team
    - Enterprise
    
  
  ### .7. Creative Management Service
  Manages Workbenches, Projects, creative assets (uploaded & AI-generated metadata), asset versioning, project templates, and input asset libraries.

  #### .7.4. Type
  Service

  #### .7.5. Dependencies
  
  - postgresql-database-023
  - minio-object-storage-024
  - brand-kit-service-006
  - auth-service-004
  
  #### .7.6. Properties
  
  - **Version:** 1.0.0
  
  #### .7.7. Interfaces
  
  - **Name:** CreativeMgmtAPI  
**Type:** Internal REST API  
**Operations:**
    
    - ManageWorkbench
    - ManageProject
    - UploadAsset
    - GetAssetHistory
    - ManageTemplates
    - ManageExportSettings
    
**Visibility:** Internal  
  
  #### .7.8. Technology
  Python (FastAPI/Flask)

  #### .7.9. Resources
  
  - **Cpu:** 2 cores
  - **Memory:** 4GB
  
  #### .7.10. Configuration
  
  - **Max Projects Per Workbench:** 100
  - **Max Assets Per Project:** 1000
  
  #### .7.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .7.12. Responsible Features
  
  - REQ-4-001
  - REQ-4-002
  - REQ-4-003
  - REQ-4-004
  - REQ-4-005
  - REQ-4-006
  - REQ-4-007
  - REQ-4-008
  - REQ-4-009
  - REQ-4-010
  - REQ-4-011
  - REQ-DA-002
  - REQ-DA-005
  - REQ-DA-007
  - REQ-DA-008
  
  #### .7.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .8. AI Generation Orchestration Service
  Handles requests for AI creative generation, interfaces with n8n for workflow execution, manages AI model selection, tracks generation status, and processes results. Coordinates credit deduction.

  #### .8.4. Type
  Service

  #### .8.5. Dependencies
  
  - rabbitmq-broker-026
  - n8n-workflow-engine-018
  - postgresql-database-023
  - subscription-billing-adapter-service-009
  - notification-service-012
  - ai-model-integration-service-019
  
  #### .8.6. Properties
  
  - **Version:** 1.0.0
  
  #### .8.7. Interfaces
  
  - **Name:** AIGenerationAPI  
**Type:** Internal REST API  
**Operations:**
    
    - InitiateGeneration
    - GetGenerationStatus
    - SelectSampleForHighRes
    
**Visibility:** Internal  
  
  #### .8.8. Technology
  Python (FastAPI/Flask)

  #### .8.9. Resources
  
  - **Cpu:** 2 cores
  - **Memory:** 4GB
  
  #### .8.10. Configuration
  
  - **Default Low Res Preview Size:** 512x512
  - **Max High Res Size:** 4096x4096
  
  #### .8.11. Health Check
  
  - **Path:** /health
  - **Interval:** 30
  - **Timeout:** 5
  
  #### .8.12. Responsible Features
  
  - REQ-3-003
  - REQ-3-006
  - REQ-3-007
  - REQ-3-010
  - REQ-3-011
  - REQ-3-012
  - REQ-3-013
  - REQ-3-015
  - AISIML-002
  - AISIML-004
  - AISIML-005
  - UAPM-1-005
  
  #### .8.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .9. Subscription & Billing Service (Odoo Adapter)
  Manages user subscriptions, credit system, billing processes, and invoicing by interfacing with Odoo and payment gateways (Stripe, PayPal).

  #### .9.4. Type
  Service

  #### .9.5. Dependencies
  
  - odoo-erp-platform-020
  - postgresql-database-023
  - secrets-management-service-022
  
  #### .9.6. Properties
  
  - **Version:** 1.0.0
  
  #### .9.7. Interfaces
  
  - **Name:** BillingAPI  
**Type:** Internal REST API  
**Operations:**
    
    - ManageSubscription
    - GetCreditBalance
    - DeductCredits
    - GetInvoices
    - UpdatePaymentMethod
    
**Visibility:** Internal  
  
  #### .9.8. Technology
  Python (FastAPI/Flask), Stripe SDK, PayPal SDK

  #### .9.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .9.10. Configuration
  
  - **Odoo Api Endpoint:** http://odoo:8069
  - **Stripe Api Key Path:** /secrets/stripe_key
  
  #### .9.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 10
  
  #### .9.12. Responsible Features
  
  - REQ-6-001
  - REQ-6-002
  - REQ-6-003
  - REQ-6-004
  - REQ-6-005
  - REQ-6-006
  - REQ-6-007
  - REQ-6-008
  - REQ-6-009
  - REQ-6-010
  - REQ-6-011
  - REQ-6-012
  - REQ-6-013
  - REQ-6-014
  - REQ-6-015
  - REQ-6-016
  - REQ-6-017
  - REQ-6-018
  - REQ-6-019
  - REQ-6-020
  - UAPM-1-005
  - REQ-3-007
  - REQ-DA-006
  - REQ-DA-017
  
  #### .9.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .10. API Developer Platform Service
  Manages API access for third-party developers, including API key management, usage tracking for monetization, and webhook notifications.

  #### .10.4. Type
  Service

  #### .10.5. Dependencies
  
  - postgresql-database-023
  - rabbitmq-broker-026
  - ai-generation-orchestration-service-008
  - project-management-service-007
  - auth-service-004
  - secrets-management-service-022
  
  #### .10.6. Properties
  
  - **Version:** 1.0.0
  
  #### .10.7. Interfaces
  
  - **Name:** DeveloperPortalAPI  
**Type:** Internal REST API  
**Operations:**
    
    - ManageAPIKeys
    - ConfigureWebhooks
    - GetAPIUsage
    
**Visibility:** Internal  
  
  #### .10.8. Technology
  Python (FastAPI/Flask)

  #### .10.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .10.10. Configuration
  
  - **Api Key Prefix:** cfai_
  - **Webhook Max Retries:** 5
  
  #### .10.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .10.12. Responsible Features
  
  - REQ-2-005
  - REQ-3520
  - REQ-7-001
  - REQ-7-002
  - REQ-7-003
  - REQ-7-004
  - REQ-7-005
  - REQ-7-006
  - REQ-3576
  - REQ-3577
  - REQ-3578
  - REQ-3579
  - REQ-3580
  - REQ-3581
  - REQ-6-013
  
  #### .10.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .11. Real-time Collaboration Service
  Enables multiple users to concurrently view and edit creative design documents in real-time using CRDTs (e.g., Yjs).

  #### .11.4. Type
  Service

  #### .11.5. Dependencies
  
  - redis-cache-025
  - auth-service-004
  
  #### .11.6. Properties
  
  - **Version:** 1.0.0
  
  #### .11.7. Interfaces
  
  - **Name:** CollaborationSocketAPI  
**Type:** WebSocket  
**Operations:**
    
    - JoinSession
    - BroadcastChanges
    - ReceiveChanges
    - SyncPresence
    
**Visibility:** Internal  
  
  #### .11.8. Technology
  Node.js (with Socket.IO) or Python (FastAPI with WebSockets), Yjs library

  #### .11.9. Resources
  
  - **Cpu:** 2 cores
  - **Memory:** 4GB
  
  #### .11.10. Configuration
  
  - **Max Collaborators Per Document:** 10
  - **Sync Interval Ms:** 100
  
  #### .11.11. Health Check
  
  - **Path:** /health
  - **Interval:** 30
  - **Timeout:** 5
  
  #### .11.12. Responsible Features
  
  - REQ-5-001
  - REQ-5-002
  - REQ-3554
  - REQ-3555
  - REQ-8-004
  - REQ-14-010
  
  #### .11.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .12. Notification Service
  Manages and delivers real-time updates and notifications to users via WebSockets (for web) and push notifications (APNS/FCM for mobile).

  #### .12.4. Type
  Service

  #### .12.5. Dependencies
  
  - rabbitmq-broker-026
  - redis-cache-025
  - secrets-management-service-022
  
  #### .12.6. Properties
  
  - **Version:** 1.0.0
  
  #### .12.7. Interfaces
  
  - **Name:** ClientWebSocketAPI  
**Type:** WebSocket  
**Operations:**
    
    - SubscribeToUpdates
    - ReceiveNotification
    
**Visibility:** Internal  
  
  #### .12.8. Technology
  Python (FastAPI with WebSockets) or Node.js (Express with Socket.IO), APNS/FCM SDKs

  #### .12.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .12.10. Configuration
  
  - **Apns Cert Path:** /secrets/apns_cert
  - **Fcm Server Key Path:** /secrets/fcm_key
  
  #### .12.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .12.12. Responsible Features
  
  - REQ-3-011
  - REQ-3-012
  - REQ-3538
  - REQ-3539
  - REQ-8-006
  - REQ-3587
  - CPIO-009
  
  #### .12.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .13. Social Media Publishing Service
  Integrates with various social media platform APIs (Instagram, Facebook, LinkedIn, Twitter/X, Pinterest, TikTok) to enable users to directly publish or schedule content. Securely manages OAuth tokens.

  #### .13.4. Type
  Service

  #### .13.5. Dependencies
  
  - postgresql-database-023
  - secrets-management-service-022
  - auth-service-004
  
  #### .13.6. Properties
  
  - **Version:** 1.0.0
  
  #### .13.7. Interfaces
  
  - **Name:** SocialPublishingAPI  
**Type:** Internal REST API  
**Operations:**
    
    - ConnectSocialAccount
    - PublishPost
    - SchedulePost
    - GetConnectedAccounts
    - RevokeSocialConnection
    
**Visibility:** Internal  
  
  #### .13.8. Technology
  Python (FastAPI/Flask), Official Social Media SDKs

  #### .13.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .13.10. Configuration
  
  - **Max Scheduled Posts Per User:** 100
  - **Token Refresh Grace Period Days:** 7
  
  #### .13.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .13.12. Responsible Features
  
  - SMPIO-001
  - SMPIO-002
  - SMPIO-003
  - SMPIO-004
  - SMPIO-005
  - SMPIO-006
  - SMPIO-007
  - SMPIO-008
  - SMPIO-011
  - REQ-3600
  - REQ-3601
  - REQ-3602
  - REQ-3603
  - REQ-3604
  - REQ-3605
  - REQ-3606
  - REQ-3607
  - REQ-3610
  - REQ-2-009
  
  #### .13.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .14. Analytics Data Forwarding Service
  Collects key user interaction and revenue-related events from various platform sources and forwards them to third-party analytics platforms (GA4, Mixpanel/Amplitude, Firebase).

  #### .14.4. Type
  Service

  #### .14.5. Dependencies
  
  - rabbitmq-broker-026
  
  #### .14.6. Properties
  
  - **Version:** 1.0.0
  
  #### .14.7. Interfaces
  
  - **Name:** EventIngestionAPI  
**Type:** Internal REST API / RabbitMQ Consumer  
**Operations:**
    
    - TrackEvent
    
**Visibility:** Internal  
  
  #### .14.8. Technology
  Python (FastAPI/Flask) or Node.js, GA4/Mixpanel/Amplitude/Firebase SDKs

  #### .14.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 1GB
  
  #### .14.10. Configuration
  
  - **Ga4 Stream Id:** G-XXXX
  - **Mixpanel Token:** XXXX
  
  #### .14.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .14.12. Responsible Features
  
  - REQ-11-001
  - REQ-11-002
  - REQ-11-003
  - REQ-11-004
  - REQ-11-005
  - REQ-3613
  - REQ-3614
  - REQ-3615
  - REQ-3616
  - REQ-3617
  - REQ-8-009
  - REQ-3590
  
  #### .14.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .15. MLOps Platform Service
  Manages the lifecycle of custom AI models, including upload, validation, deployment to Kubernetes, versioning, monitoring, and feedback collection.

  #### .15.4. Type
  Service

  #### .15.5. Dependencies
  
  - minio-object-storage-024
  - postgresql-database-023
  - ai-model-serving-platform-021
  - secrets-management-service-022
  
  #### .15.6. Properties
  
  - **Version:** 1.0.0
  
  #### .15.7. Interfaces
  
  - **Name:** MLOpsAPI  
**Type:** Internal REST API  
**Operations:**
    
    - UploadModel
    - ListModels
    - GetModelDetails
    - DeployModelVersion
    - MonitorModelPerformance
    - CollectFeedback
    
**Visibility:** Internal  
  
  #### .15.8. Technology
  Python (FastAPI/Flask), Kubernetes API Client, Snyk/Clair integration

  #### .15.9. Resources
  
  - **Cpu:** 2 cores
  - **Memory:** 4GB
  
  #### .15.10. Configuration
  
  - **Model Registry Name:** CreativeFlowModelRegistry
  - **Allowed Model Formats:**
    
    - ONNX
    - SavedModel
    - TorchScript
    
  
  #### .15.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 10
  
  #### .15.12. Responsible Features
  
  - AISIML-006
  - AISIML-007
  - AISIML-008
  - AISIML-009
  - AISIML-010
  - AISIML-011
  - AISIML-012
  - REQ-3623
  - REQ-3624
  - REQ-3625
  - REQ-3626
  - REQ-3627
  - REQ-3628
  - REQ-3629
  - REQ-SSPE-014
  - REQ-20-013
  
  #### .15.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  - **Allowed Roles:**
    
    - Admin
    - EnterpriseUser
    
  
  ### .16. Customer Support Service (Odoo Adapter)
  Interfaces with Odoo Helpdesk and Knowledge modules to provide integrated customer support functionalities like ticket management, knowledge base access, and potentially live chat.

  #### .16.4. Type
  Service

  #### .16.5. Dependencies
  
  - odoo-erp-platform-020
  - auth-service-004
  
  #### .16.6. Properties
  
  - **Version:** 1.0.0
  
  #### .16.7. Interfaces
  
  - **Name:** SupportAPI  
**Type:** Internal REST API  
**Operations:**
    
    - SubmitTicket
    - GetTicketStatus
    - SearchKnowledgeBase
    - InitiateLiveChat
    
**Visibility:** Internal  
  
  #### .16.8. Technology
  Python (FastAPI/Flask)

  #### .16.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 1GB
  
  #### .16.10. Configuration
  
  - **Odoo Helpdesk Endpoint:** http://odoo:8069/helpdesk
  - **Default Kbresults Per Page:** 10
  
  #### .16.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .16.12. Responsible Features
  
  - REQ-9-001
  - REQ-9-002
  - REQ-9-003
  - REQ-9-004
  - REQ-9-006
  - REQ-3592
  - REQ-3593
  - REQ-3594
  - REQ-3595
  - REQ-3597
  
  #### .16.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .17. Community Forum Service
  Provides an integrated community forum for user discussions, topic creation, replies, and moderation.

  #### .17.4. Type
  Service

  #### .17.5. Dependencies
  
  - postgresql-database-023
  - user-profile-service-005
  - auth-service-004
  
  #### .17.6. Properties
  
  - **Version:** 1.0.0
  
  #### .17.7. Interfaces
  
  - **Name:** ForumAPI  
**Type:** Internal REST API  
**Operations:**
    
    - CreateTopic
    - PostReply
    - SearchForum
    - ModeratePost
    
**Visibility:** Internal  
  
  #### .17.8. Technology
  Python (Django/Flask with forum extensions) or Node.js (Express with forum libraries)

  #### .17.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .17.10. Configuration
  
  - **Topics Per Page:** 20
  - **Max Reply Length:** 5000
  
  #### .17.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .17.12. Responsible Features
  
  - REQ-9-007
  - REQ-3598
  
  #### .17.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .18. n8n Workflow Engine
  Orchestrates AI creative generation workflows, data pre-processing, AI model selection/interaction, error handling, and content safety checks. Consumes jobs from RabbitMQ.

  #### .18.4. Type
  WorkflowEngine

  #### .18.5. Dependencies
  
  - rabbitmq-broker-026
  - ai-model-integration-service-019
  - ai-model-serving-platform-021
  - minio-object-storage-024
  - notification-service-012
  - secrets-management-service-022
  
  #### .18.6. Properties
  
  - **Version:** n8n latest stable
  
  #### .18.7. Interfaces
  
  - **Name:** JobConsumer  
**Type:** RabbitMQ Consumer  
**Operations:**
    
    - ConsumeGenerationJob
    
**Visibility:** Internal  
  
  #### .18.8. Technology
  n8n (Node.js based)

  #### .18.9. Resources
  
  - **Cpu:** 4 cores
  - **Memory:** 8GB
  
  #### .18.10. Configuration
  
  - **Max Concurrent Workflows:** 50
  - **Workflow Timeout Seconds:** 300
  
  #### .18.11. Health Check
  
  - **Path:** /healthz
  - **Interval:** 30
  - **Timeout:** 5
  
  #### .18.12. Responsible Features
  
  - REQ-3-001
  - REQ-3-002
  - REQ-3-003
  - REQ-3-004
  - REQ-3-005
  - REQ-3-006
  - REQ-3-008
  - REQ-3-009
  - REQ-3-010
  - REQ-3-011
  - REQ-3-012
  - REQ-3-013
  - REQ-3-015
  - REQ-3-014
  - REQ-3528
  - REQ-3529
  - REQ-3530
  - REQ-3531
  - REQ-3532
  - REQ-3533
  - REQ-3534
  - REQ-3535
  - REQ-3536
  - REQ-3537
  - REQ-3538
  - REQ-3539
  - REQ-3540
  - REQ-3541
  - REQ-3542
  
  #### .18.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .19. AI Model Integration Service
  Provides a standardized internal interface/adapter layer for interacting with diverse third-party AI model providers (OpenAI, Stability AI) and custom models. Used by n8n.

  #### .19.4. Type
  Service

  #### .19.5. Dependencies
  
  - secrets-management-service-022
  - ai-model-serving-platform-021
  
  #### .19.6. Properties
  
  - **Version:** 1.0.0
  
  #### .19.7. Interfaces
  
  - **Name:** AIProviderAPI  
**Type:** Internal REST/gRPC API  
**Operations:**
    
    - GenerateImage
    - ProcessText
    - CallCustomModel
    
**Visibility:** Internal  
  
  #### .19.8. Technology
  Python (FastAPI/Flask), OpenAI SDK, Stability AI SDK

  #### .19.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .19.10. Configuration
  
  - **Openai Api Key Path:** /secrets/openai_key
  - **Stability Api Key Path:** /secrets/stability_key
  - **Default Retry Attempts:** 3
  
  #### .19.11. Health Check
  
  - **Path:** /health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .19.12. Responsible Features
  
  - AISIML-001
  - AISIML-003
  - AISIML-004
  - AISIML-005
  - REQ-3618
  - REQ-3620
  - REQ-3621
  - REQ-3622
  
  #### .19.13. Security
  
  - **Requires Authentication:** False
  - **Requires Authorization:** False
  
  ### .20. Odoo ERP Platform
  External ERP system handling core business logic for subscriptions, billing, credit system management, invoicing, customer support helpdesk, and knowledge base. Interacted with via adapter services.

  #### .20.4. Type
  ExternalPlatform

  #### .20.5. Dependencies
  
  - postgresql-database-023
  
  #### .20.6. Properties
  
  - **Version:** Odoo 18+
  
  #### .20.7. Interfaces
  
  - **Name:** OdooExternalAPI  
**Type:** XML-RPC/JSON-RPC  
**Operations:**
    
    - Various Odoo operations
    
**Visibility:** Internal  
  
  #### .20.8. Technology
  Odoo (Python, XML, JavaScript)

  #### .20.9. Resources
  
  - **Cpu:** Defined by Odoo hosting
  - **Memory:** Defined by Odoo hosting
  
  #### .20.10. Configuration
  
  
  #### .20.11. Health Check
  None

  #### .20.12. Responsible Features
  
  - REQ-6-019
  - REQ-3574
  - REQ-9-001
  - REQ-3592
  
  #### .20.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .21. AI Model Serving Platform
  GPU-accelerated Kubernetes cluster for hosting and serving custom AI models. Manages GPU resources and auto-scaling.

  #### .21.4. Type
  RuntimePlatform

  #### .21.5. Dependencies
  
  - secrets-management-service-022
  - minio-object-storage-024
  
  #### .21.6. Properties
  
  - **Version:** Kubernetes latest stable
  
  #### .21.7. Interfaces
  
  - **Name:** ModelInferenceAPI  
**Type:** Internal gRPC/REST API  
**Operations:**
    
    - Predict/Generate
    
**Visibility:** Internal  
  - **Name:** K8sDeploymentAPI  
**Type:** Kubernetes API  
**Operations:**
    
    - DeployModelService
    - ScaleDeployment
    
**Visibility:** Internal  
  
  #### .21.8. Technology
  Kubernetes (K3s/RKE2), Docker, NVIDIA GPU Operator, TensorFlow Serving/TorchServe/Triton

  #### .21.9. Resources
  
  - **Cpu:** Cluster-dependent
  - **Memory:** Cluster-dependent
  - **Gpu:** Multiple NVIDIA GPUs
  
  #### .21.10. Configuration
  
  - **Namespace:** ai-models
  - **Default Replicas:** 1
  
  #### .21.11. Health Check
  None

  #### .21.12. Responsible Features
  
  - CPIO-008
  - REQ-3673
  - AISIML-007
  - REQ-3624
  - REQ-SSPE-011
  - REQ-SSPE-012
  
  #### .21.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .22. Secrets Management Service
  Securely stores and manages all secrets like API keys, database credentials, certificates, and encryption keys.

  #### .22.4. Type
  InfrastructureService

  #### .22.5. Dependencies
  
  
  #### .22.6. Properties
  
  - **Version:** HashiCorp Vault latest stable
  
  #### .22.7. Interfaces
  
  - **Name:** SecretsAPI  
**Type:** REST API  
**Operations:**
    
    - ReadSecret
    - WriteSecret
    - ListSecrets
    
**Visibility:** Internal  
  
  #### .22.8. Technology
  HashiCorp Vault or Ansible Vault with secure backend

  #### .22.9. Resources
  
  - **Cpu:** 1 core
  - **Memory:** 2GB
  
  #### .22.10. Configuration
  
  - **Backend Type:** raft/consul
  - **Audit Log Path:** /var/log/vault_audit.log
  
  #### .22.11. Health Check
  
  - **Path:** /v1/sys/health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .22.12. Responsible Features
  
  - AISIML-003
  - REQ-DA-010
  - REQ-20-008
  - PMDT-007
  - REQ-3620
  - REQ-3765
  - REQ-3727
  - REQ-3790
  - REQ-3796
  
  #### .22.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  - **Allowed Roles:**
    
    - SystemAdmin
    - ServiceAccount
    
  
  ### .23. PostgreSQL Relational Database
  Primary RDBMS for storing structured application data. Configured with read replicas, streaming replication for HA/DR, encryption at rest, and automated backups.

  #### .23.4. Type
  Database

  #### .23.5. Dependencies
  
  
  #### .23.6. Properties
  
  - **Version:** PostgreSQL 16+
  
  #### .23.7. Interfaces
  
  - **Name:** SQLInterface  
**Type:** SQL/JDBC/ODBC  
**Operations:**
    
    - Standard CRUD, Transactions
    
**Visibility:** Internal  
  
  #### .23.8. Technology
  PostgreSQL

  #### .23.9. Resources
  
  - **Cpu:** 8+ cores
  - **Memory:** 32GB+
  - **Storage:** Scalable SSD (e.g., 2TB+)
  
  #### .23.10. Configuration
  
  - **Max_Connections:** 500
  - **Shared_Buffers:** 8GB
  - **Wal_Level:** replica
  
  #### .23.11. Health Check
  None

  #### .23.12. Responsible Features
  
  - REQ-DA-001
  - REQ-DA-004
  - REQ-DA-005
  - REQ-DA-006
  - REQ-DA-009
  - REQ-DA-011
  - REQ-DA-013
  - REQ-DA-014
  - REQ-DA-015
  - REQ-DA-018
  - REQ-3756
  - REQ-3759
  - REQ-3760
  - REQ-3761
  - REQ-3764
  - REQ-3766
  - REQ-3768
  - REQ-3769
  - REQ-3770
  - REQ-3773
  - CPIO-004
  - REQ-3669
  
  #### .23.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .24. MinIO Object Storage
  S3-compatible object storage for unstructured data. Configured for multi-site replication, encryption at rest, and backups.

  #### .24.4. Type
  ObjectStore

  #### .24.5. Dependencies
  
  
  #### .24.6. Properties
  
  - **Version:** MinIO latest stable
  
  #### .24.7. Interfaces
  
  - **Name:** S3CompatibleAPI  
**Type:** HTTP/S (S3 SDKs)  
**Operations:**
    
    - PutObject
    - GetObject
    - DeleteObject
    - ListObjects
    
**Visibility:** Internal  
  
  #### .24.8. Technology
  MinIO

  #### .24.9. Resources
  
  - **Cpu:** 4+ cores per node
  - **Memory:** 16GB+ per node
  - **Storage:** Scalable HDD/SSD (e.g., 10TB+)
  
  #### .24.10. Configuration
  
  - **Region:** us-east-1
  - **Auto Encryption:** true
  - **Replication Targets:**
    
    - dr-site-minio
    
  
  #### .24.11. Health Check
  None

  #### .24.12. Responsible Features
  
  - REQ-DA-002
  - REQ-DA-007
  - REQ-DA-009
  - REQ-DA-012
  - REQ-DA-015
  - REQ-3757
  - REQ-3762
  - REQ-3764
  - REQ-3767
  - REQ-3770
  - CPIO-005
  - REQ-3670
  
  #### .24.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .25. Redis In-Memory Data Store
  Used for session management, content caching, rate limiting, and Pub/Sub. Configured for persistence and HA (Sentinel/Cluster).

  #### .25.4. Type
  CacheStore

  #### .25.5. Dependencies
  
  
  #### .25.6. Properties
  
  - **Version:** Redis latest stable
  
  #### .25.7. Interfaces
  
  - **Name:** RedisAPI  
**Type:** Redis Protocol  
**Operations:**
    
    - GET
    - SET
    - DEL
    - INCR
    - PUBLISH
    - SUBSCRIBE
    
**Visibility:** Internal  
  
  #### .25.8. Technology
  Redis

  #### .25.9. Resources
  
  - **Cpu:** 2+ cores
  - **Memory:** 8GB+
  - **Network:** High
  
  #### .25.10. Configuration
  
  - **Persistence:** AOF
  - **Ha_Mode:** sentinel
  - **Maxmemory_Policy:** allkeys-lru
  
  #### .25.11. Health Check
  None

  #### .25.12. Responsible Features
  
  - REQ-DA-003
  - REQ-3758
  - CPIO-006
  - REQ-3671
  
  #### .25.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .26. RabbitMQ Message Broker
  Manages asynchronous job queues. Deployed as a mirrored cluster for HA.

  #### .26.4. Type
  MessageBroker

  #### .26.5. Dependencies
  
  
  #### .26.6. Properties
  
  - **Version:** RabbitMQ latest stable
  
  #### .26.7. Interfaces
  
  - **Name:** AMQPProtocolAPI  
**Type:** AMQP  
**Operations:**
    
    - PublishMessage
    - ConsumeMessage
    - DeclareQueue
    
**Visibility:** Internal  
  
  #### .26.8. Technology
  RabbitMQ

  #### .26.9. Resources
  
  - **Cpu:** 2+ cores per node
  - **Memory:** 8GB+ per node
  
  #### .26.10. Configuration
  
  - **Cluster_Node_Count:** 3
  - **Default_Vhost:** /
  - **Queue_Mirroring_Policy:** all
  
  #### .26.11. Health Check
  None

  #### .26.12. Responsible Features
  
  - REQ-SSPE-009
  - REQ-3695
  - CPIO-007
  - REQ-3672
  
  #### .26.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  
  ### .27. Shared Logging Library
  Provides standardized logging capabilities (structured JSON, correlation IDs, configurable levels) for use across backend services.

  #### .27.4. Type
  Library

  #### .27.5. Dependencies
  
  
  #### .27.6. Properties
  
  - **Language:** Python, Node.js
  
  #### .27.7. Interfaces
  
  - **Name:** LoggerAPI  
**Type:** Code Library  
**Operations:**
    
    - log_info
    - log_error
    - set_correlation_id
    
**Visibility:** Internal  
  
  #### .27.8. Technology
  Standard logging libraries (e.g., Python `logging`, `python-json-logger`)

  #### .27.9. Resources
  None

  #### .27.10. Configuration
  None

  #### .27.11. Health Check
  None

  #### .27.12. Responsible Features
  
  - MON-005
  - MON-006
  - REQ-3737
  - REQ-3738
  
  #### .27.13. Security
  None

  ### .28. Shared Security Library
  Provides common security utility functions (e.g., input validation helpers, output encoders, CSRF protection helpers) for backend services.

  #### .28.4. Type
  Library

  #### .28.5. Dependencies
  
  
  #### .28.6. Properties
  
  - **Language:** Python, Node.js
  
  #### .28.7. Interfaces
  
  - **Name:** SecurityUtilAPI  
**Type:** Code Library  
**Operations:**
    
    - validate_input
    - encode_output
    - check_permission
    
**Visibility:** Internal  
  
  #### .28.8. Technology
  OWASP ESAPI, Pydantic (for Python validation)

  #### .28.9. Resources
  None

  #### .28.10. Configuration
  None

  #### .28.11. Health Check
  None

  #### .28.12. Responsible Features
  
  - SPR-001
  - SPR-002
  - REQ-7-006
  - REQ-3663
  - REQ-3664
  - REQ-3581
  
  #### .28.13. Security
  None

  ### .29. Shared Internationalization (I18n) Library
  Provides utilities for handling internationalization and localization aspects in backend services, such as date/time/number formatting based on locale.

  #### .29.4. Type
  Library

  #### .29.5. Dependencies
  
  
  #### .29.6. Properties
  
  - **Language:** Python
  
  #### .29.7. Interfaces
  
  - **Name:** I18nUtilAPI  
**Type:** Code Library  
**Operations:**
    
    - format_datetime_locale
    - format_number_locale
    
**Visibility:** Internal  
  
  #### .29.8. Technology
  Python Babel

  #### .29.9. Resources
  None

  #### .29.10. Configuration
  None

  #### .29.11. Health Check
  None

  #### .29.12. Responsible Features
  
  - PLI-001
  - PLI-005
  - REQ-3654
  - REQ-3658
  
  #### .29.13. Security
  None

  


---

# 2. Component_Relations

- **Architecture:**
  
  - **Components:**
    
    - **Id:** webapp-main  
**Name:** Web Application Main Shell  
**Description:** Main PWA container, routing, core PWA functionalities, and shared frontend services.  
**Type:** FrontendApplication  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    - webapp-auth-module
    - webapp-dashboard
    - webapp-creative-editor
    - webapp-template-gallery
    - webapp-user-profile-manager-ui
    - webapp-brandkit-manager-ui
    - webapp-project-workspace-ui
    - webapp-collaboration-client
    - webapp-subscription-billing-ui
    - webapp-developer-portal-ui
    - webapp-pwa-engine
    - webapp-accessibility-module
    - webapp-i18n-module
    - webapp-notification-handler
    - apigw-main
    - svc-notification-main
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Framework:** React 19+
    
**Technology:** React, TypeScript, PWA  
**Resources:**
    
    - **Cpu:** N/A (Client-Side)
    - **Memory:** N/A (Client-Side)
    
**Configuration:**
    
    - **Api Endpoint:** /gw
    - **Feature Flags:**
      
      
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-001
    
**Security:** None  
    - **Id:** webapp-api-service  
**Name:** Webapp API Service (Frontend)  
**Description:** Abstraction layer for making API calls from the web frontend to the backend.  
**Type:** FrontendModule  
**Dependencies:**
    
    - apigw-main
    
**Properties:**
    
    
**Technology:** TypeScript, Axios/Fetch  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    
**Security:** None  
    - **Id:** webapp-state-management  
**Name:** Webapp State Management  
**Description:** Manages global client-side state for the web application.  
**Type:** FrontendModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Redux/Zustand  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    
**Security:** None  
    - **Id:** webapp-dashboard  
**Name:** WebApp Dashboard UI  
**Description:** Handles the main dashboard UI, quick access, and summaries.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-004
    - REQ-WCI-005
    - REQ-4-009
    - REQ-WCI-003
    - REQ-14-008
    
**Security:** None  
    - **Id:** webapp-creative-editor  
**Name:** WebApp Creative Editor UI  
**Description:** WYSIWYG editor for creating and modifying creatives.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    - webapp-collaboration-client
    
**Properties:**
    
    
**Technology:** React, TypeScript, Canvas/SVG libraries  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-006
    - REQ-WCI-007
    - REQ-14-004
    - SMPIO-009
    - SMPIO-010
    - SMPIO-013
    - REQ-3-008
    - REQ-3-003
    - REQ-14-005
    
**Security:** None  
    - **Id:** webapp-template-gallery  
**Name:** WebApp Template Gallery UI  
**Description:** UI for browsing, searching, and filtering templates.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-009
    - REQ-WCI-010
    - REQ-9-008
    - REQ-14-008
    
**Security:** None  
    - **Id:** webapp-user-profile-manager-ui  
**Name:** WebApp User Profile & Account UI  
**Description:** UI for managing user profiles, preferences, security settings, and data privacy.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - UAPM-1-003
    - UAPM-1-005
    - UAPM-1-007
    - UAPM-1-008
    - UAPM-1-009
    - UAPM-1-010
    - REQ-2-007
    
**Security:** None  
    - **Id:** webapp-brandkit-manager-ui  
**Name:** WebApp Brand Kit Management UI  
**Description:** UI for Pro+ users to manage their brand kits.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - UAPM-1-004
    
**Security:** None  
    - **Id:** webapp-project-workspace-ui  
**Name:** WebApp Workbench & Project UI  
**Description:** UI for managing workbenches, projects, and assets within them.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-4-001
    - REQ-4-002
    - REQ-4-003
    - REQ-4-004
    - REQ-4-005
    - REQ-4-006
    - REQ-4-007
    - REQ-4-008
    
**Security:** None  
    - **Id:** webapp-collaboration-client  
**Name:** WebApp Collaboration Client  
**Description:** Handles real-time collaboration features, CRDT integration, and presence indicators.  
**Type:** FrontendModule  
**Dependencies:**
    
    - webapp-state-management
    - svc-collaboration-main
    
**Properties:**
    
    
**Technology:** TypeScript, Yjs, WebSocket client  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-5-001
    - REQ-WCI-008
    - REQ-14-010
    - REQ-14-005 (indirectly)
    
**Security:** None  
    - **Id:** webapp-subscription-billing-ui  
**Name:** WebApp Subscription & Billing UI  
**Description:** UI for users to manage their subscriptions and view billing details.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-6-005
    
**Security:** None  
    - **Id:** webapp-developer-portal-ui  
**Name:** WebApp Developer Portal UI  
**Description:** UI for API users to manage API keys and webhooks.  
**Type:** FrontendComponent  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-7-005
    - REQ-7-002
    - REQ-7-004
    
**Security:** None  
    - **Id:** webapp-auth-module  
**Name:** WebApp Authentication Module  
**Description:** Handles UI flows for user login, registration, password reset, and MFA setup.  
**Type:** FrontendModule  
**Dependencies:**
    
    - webapp-api-service
    - webapp-state-management
    
**Properties:**
    
    
**Technology:** React, TypeScript  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - UAPM-1-001
    - UAPM-1-002
    - UAPM-1-006
    
**Security:** None  
    - **Id:** webapp-pwa-engine  
**Name:** WebApp PWA Engine  
**Description:** Implements PWA functionalities like service workers and manifest.  
**Type:** FrontendModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Service Workers API, Web App Manifest  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-001
    - REQ-WCI-003 (mobile-first aspects)
    
**Security:** None  
    - **Id:** webapp-accessibility-module  
**Name:** WebApp Accessibility Module  
**Description:** Ensures WCAG compliance across web UI components through standards, tools, and practices.  
**Type:** FrontendModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** HTML, ARIA, CSS, Accessibility testing tools  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-011
    - REQ-14-001
    - REQ-14-003
    
**Security:** None  
    - **Id:** webapp-i18n-module  
**Name:** WebApp Internationalization Module  
**Description:** Handles language selection, translation loading, and localized formatting.  
**Type:** FrontendModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** i18next/react-i18next or similar  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-012
    - PLI-001
    - PLI-002
    - PLI-005
    - PLI-006
    - PLI-007
    - REQ-14-012
    - REQ-14-005 (contextual help aspects)
    
**Security:** None  
    - **Id:** webapp-notification-handler  
**Name:** WebApp Notification Handler  
**Description:** Receives and displays real-time notifications via WebSockets.  
**Type:** FrontendModule  
**Dependencies:**
    
    - svc-notification-main
    
**Properties:**
    
    
**Technology:** TypeScript, WebSocket client, UI notification libraries  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-WCI-008 (system messages)
    
**Security:** None  
    - **Id:** mobileapp-main  
**Name:** Mobile Application Main Shell  
**Description:** Core Flutter application structure, navigation, and shared mobile services.  
**Type:** MobileApplication  
**Dependencies:**
    
    - mobileapp-api-service
    - mobileapp-state-management
    - mobileapp-creative-editor
    - mobileapp-offline-sync-engine
    - mobileapp-device-integration
    - mobileapp-push-notification-handler
    - mobileapp-analytics-tracker
    - mobileapp-accessibility-module
    - mobileapp-local-db
    - apigw-main
    - svc-notification-main
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Framework:** Flutter 3.19+
    
**Technology:** Flutter, Dart  
**Resources:**
    
    - **Cpu:** N/A (Client-Side)
    - **Memory:** N/A (Client-Side)
    
**Configuration:**
    
    - **Api Endpoint:** /gw
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-001
    - REQ-8-007
    - REQ-SSPE-004
    
**Security:** None  
    - **Id:** mobileapp-api-service  
**Name:** MobileApp API Service  
**Description:** Abstraction layer for making API calls from the mobile app to the backend.  
**Type:** MobileModule  
**Dependencies:**
    
    - apigw-main
    
**Properties:**
    
    
**Technology:** Dart, http/dio  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    
**Security:** None  
    - **Id:** mobileapp-state-management  
**Name:** MobileApp State Management  
**Description:** Manages global client-side state for the mobile application.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Provider/Riverpod/Bloc  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    
**Security:** None  
    - **Id:** mobileapp-creative-editor  
**Name:** MobileApp Creative Editor UI  
**Description:** Mobile-optimized creative editor with touch interactions.  
**Type:** MobileComponent  
**Dependencies:**
    
    - mobileapp-api-service
    - mobileapp-state-management
    - mobileapp-offline-sync-engine
    
**Properties:**
    
    
**Technology:** Flutter, Dart  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-002
    - REQ-14-002
    - REQ-14-004
    - REQ-14-005
    
**Security:** None  
    - **Id:** mobileapp-offline-sync-engine  
**Name:** MobileApp Offline Sync Engine  
**Description:** Handles offline data storage (SQLite) and synchronization logic with the backend.  
**Type:** MobileModule  
**Dependencies:**
    
    - mobileapp-api-service
    - mobileapp-local-db
    - svc-collaboration-main
    
**Properties:**
    
    
**Technology:** Dart, SQLite (Drift/Moor)  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-003
    - REQ-8-004
    - REQ-14-006
    
**Security:** None  
    - **Id:** mobileapp-device-integration  
**Name:** MobileApp Device Integration Module  
**Description:** Integrates with native device features like camera, voice-to-text, and deep linking.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Flutter Platform Channels, Dart  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-005
    - REQ-14-002 (camera)
    - REQ-14-011
    
**Security:** None  
    - **Id:** mobileapp-push-notification-handler  
**Name:** MobileApp Push Notification Handler  
**Description:** Receives and displays push notifications via APNS/FCM.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Flutter, Firebase Cloud Messaging SDK, APNS SDK integration  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-006
    
**Security:** None  
    - **Id:** mobileapp-analytics-tracker  
**Name:** MobileApp Analytics Tracker  
**Description:** Integrates with mobile analytics SDKs for tracking user behavior and app performance.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Flutter, Firebase Analytics SDK, Mixpanel/Amplitude SDK  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-009
    - REQ-11-005
    - REQ-SSPE-021
    
**Security:** None  
    - **Id:** mobileapp-accessibility-module  
**Name:** MobileApp Accessibility Module  
**Description:** Ensures WCAG compliance for the mobile application.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Flutter Accessibility Widgets, Dart  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-008
    - REQ-14-001
    - REQ-14-003
    
**Security:** None  
    - **Id:** mobileapp-local-db  
**Name:** MobileApp Local Database Wrapper  
**Description:** Provides an interface to the local SQLite database.  
**Type:** MobileModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** SQLite via Drift/Moor  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-8-003 (storage aspect)
    
**Security:** None  
    - **Id:** apigw-main  
**Name:** API Gateway  
**Description:** Central entry point for all API requests. Handles routing, authentication, rate limiting.  
**Type:** APIGateway  
**Dependencies:**
    
    - svc-auth-main
    - infra-redis
    - infra-core-loadbalancer
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Nginx with OpenResty/Lua, Kong, or custom Go/Python  
**Resources:**
    
    - **Cpu:** 2 cores
    - **Memory:** 4GB
    
**Configuration:**
    
    - **Timeout:** 30s
    - **Retry Attempts:** 3
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-2-004 (validation)
    - REQ-2-005 (validation)
    - REQ-7-002 (validation)
    - REQ-7-003 (enforcement)
    - UAPM-1-008 (session limits, if enforced at GW)
    - REQ-2-006 (session limits, if enforced at GW)
    - CPIO-002 (as LB or behind it)
    - PMDT-001 (tool selection implies its use)
    
**Security:**
    
    - **Requires Authentication:** False
    
    - **Id:** apigw-router  
**Name:** API Gateway Router  
**Description:** Routes incoming API requests to the appropriate backend microservices.  
**Type:** APIGatewayModule  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Nginx/Kong configuration, Lua scripting  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    
**Security:** None  
    - **Id:** apigw-auth-filter  
**Name:** API Gateway Authentication Filter  
**Description:** Validates JWT access tokens and API keys.  
**Type:** APIGatewayModule  
**Dependencies:**
    
    - svc-auth-main
    
**Properties:**
    
    
**Technology:** Nginx/Kong plugins, Lua scripting  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-2-004
    - REQ-2-005
    - REQ-7-002
    
**Security:** None  
    - **Id:** apigw-rate-limiter  
**Name:** API Gateway Rate Limiter  
**Description:** Enforces rate limits based on user tier, API key, or IP address.  
**Type:** APIGatewayModule  
**Dependencies:**
    
    - infra-redis
    
**Properties:**
    
    
**Technology:** Nginx/Kong plugins, Lua scripting  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-7-003
    - UAPM-1-008
    - REQ-2-006
    
**Security:** None  
    - **Id:** svc-auth-main  
**Name:** Authentication & Authorization Service  
**Description:** Handles user authentication, MFA, password management, sessions, social login, JWTs, and RBAC.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-db-postgres
    - infra-redis
    - svc-notification-main
    - infra-secrets-manager
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask), OAuthlib, PyJWT, bcrypt  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 2GB
    
**Configuration:**
    
    - **Jwt Secret Key Ref:** auth/jwt-secret
    - **Token Expiry:** 15m
    - **Refresh Token Expiry:** 7d
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - UAPM-1-001
    - REQ-2-001
    - UAPM-1-002
    - REQ-2-002
    - UAPM-1-006
    - REQ-2-004
    - REQ-2-006
    - UAPM-1-008
    - REQ-2-007
    - REQ-2-003
    - REQ-2-008
    - REQ-2-009
    - SMPIO-007
    - REQ-2-010
    - REQ-DA-004 (auth fields)
    
**Security:**
    
    - **Requires Authentication:** False
    
    - **Id:** svc-auth-registration  
**Name:** AuthService Registration Handler  
**Description:** Handles new user registration (email/password, social).  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-passwordhasher
    - svc-auth-userdb-adapter
    - svc-auth-tokenissuer
    - svc-notification-main
    
**Responsible Features:**
    
    - UAPM-1-001
    - REQ-2-001
    
**Technology:** Python  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-login  
**Name:** AuthService Login Handler  
**Description:** Handles user login and initiates MFA if configured.  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-passwordhasher
    - svc-auth-userdb-adapter
    - svc-auth-tokenissuer
    - svc-auth-mfamanager
    
**Responsible Features:**
    
    - UAPM-1-001 (login part)
    - REQ-2-004
    
**Technology:** Python  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-mfamanager  
**Name:** AuthService MFA Manager  
**Description:** Manages all aspects of Multi-Factor Authentication.  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-userdb-adapter
    - sharedlib-sms-client
    - sharedlib-email-client
    - svc-auth-totpgenerator
    
**Responsible Features:**
    
    - UAPM-1-002
    - REQ-2-002
    
**Technology:** Python, pyotp  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-passwordmanager  
**Name:** AuthService Password Manager  
**Description:** Handles password changes and recovery.  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-passwordhasher
    - svc-auth-userdb-adapter
    - svc-notification-main
    
**Responsible Features:**
    
    - UAPM-1-006
    
**Technology:** Python  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-sessionmanager  
**Name:** AuthService Session Manager  
**Description:** Manages JWT issuance, validation, refresh tokens, and active session tracking in Redis.  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-tokenissuer
    - svc-auth-tokenvalidator
    - infra-redis
    
**Responsible Features:**
    
    - REQ-2-004
    - REQ-2-006
    - UAPM-1-008
    - REQ-2-007
    
**Technology:** Python, PyJWT  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-sociallogin  
**Name:** AuthService Social Login Integrator  
**Description:** Handles OAuth 2.0/OpenID Connect flows with social providers.  
**Type:** ServiceModule  
**Dependencies:**
    
    - infra-secrets-manager
    
**Responsible Features:**
    
    - UAPM-1-001 (social)
    - REQ-2-001 (social)
    - REQ-2-009
    - SMPIO-007
    
**Technology:** Python, OAuthlib  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-rbacengine  
**Name:** AuthService RBAC Engine  
**Description:** Performs role-based and subscription tier-based access control checks.  
**Type:** ServiceModule  
**Dependencies:**
    
    - svc-auth-userdb-adapter
    
**Responsible Features:**
    
    - REQ-2-003
    - REQ-2-008
    
**Technology:** Python  
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-tokenissuer  
**Name:** AuthService Token Issuer  
**Description:** Generates JWTs.  
**Type:** ServiceUtility  
**Dependencies:**
    
    - infra-secrets-manager
    
**Technology:** Python, PyJWT  
**Responsible Features:**
    
    
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-tokenvalidator  
**Name:** AuthService Token Validator  
**Description:** Validates JWTs.  
**Type:** ServiceUtility  
**Dependencies:**
    
    - infra-secrets-manager
    
**Technology:** Python, PyJWT  
**Responsible Features:**
    
    
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-passwordhasher  
**Name:** AuthService Password Hasher  
**Description:** Hashes and verifies passwords using bcrypt/Argon2.  
**Type:** ServiceUtility  
**Dependencies:**
    
    
**Technology:** Python, bcrypt/argon2cffi  
**Responsible Features:**
    
    - UAPM-1-006
    
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-auth-userdb-adapter  
**Name:** AuthService User DB Adapter  
**Description:** Data access layer for authentication-related user data in PostgreSQL.  
**Type:** DataAccessAdapter  
**Dependencies:**
    
    - infra-db-postgres
    
**Technology:** Python, SQLAlchemy/psycopg2  
**Responsible Features:**
    
    
**Resources:**
    
    
**Configuration:**
    
    
**Properties:**
    
    
**Health Check:** None  
**Security:** None  
    - **Id:** svc-userprofile-main  
**Name:** User Account & Profile Service  
**Description:** Manages user profiles, preferences, data privacy rights, consent, and team role display.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-db-postgres
    - svc-subscriptionbilling-adapter
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask)  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 1GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - UAPM-1-003
    - UAPM-1-001 (progressive profiling)
    - UAPM-1-007
    - REQ-DA-017
    - UAPM-1-009
    - UAPM-1-010
    - UAPM-1-005
    - REQ-DA-004 (profile fields)
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      - ADMIN
      
    
    - **Id:** svc-creativemgmt-main  
**Name:** Creative Management Service  
**Description:** Manages Brand Kits, Workbenches, Projects, assets, versions, and templates.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-db-postgres
    - infra-storage-minio
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask)  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 2GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - UAPM-1-004
    - REQ-4-001
    - REQ-4-002
    - REQ-4-003
    - REQ-4-004
    - REQ-DA-002
    - REQ-4-005
    - REQ-4-006
    - REQ-4-007
    - REQ-4-011
    - REQ-DA-008
    - REQ-DA-005
    - REQ-DA-007
    - REQ-4-010
    - REQ-DA-004 (brand kit schema)
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      - ADMIN
      
    
    - **Id:** svc-aigen-main  
**Name:** AI Generation Orchestration Service  
**Description:** Handles AI creative generation requests, interacts with n8n, manages model selection, status tracking.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-mq-rabbitmq
    - workflow-n8n-main
    - infra-db-postgres
    - svc-subscriptionbilling-adapter
    - svc-notification-main
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask)  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 1GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-3-010
    - AISIML-002
    - REQ-3-011
    - REQ-3-012
    - REQ-3-006
    - AISIML-005
    - REQ-3-015
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    - REQ-3-004
    - REQ-3-005
    - REQ-3-007
    - REQ-3-008
    - REQ-3-009
    - REQ-DA-005 (generation schema)
    - REQ-SSPE-001
    - REQ-SSPE-002
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      - API_USER
      - ADMIN
      
    
    - **Id:** svc-subscriptionbilling-adapter  
**Name:** Subscription & Billing Service (Odoo Adapter)  
**Description:** Adapter for Odoo to manage subscriptions, credits, billing, and invoicing.  
**Type:** MicroserviceAdapter  
**Dependencies:**
    
    - erp-odoo-main
    - infra-db-postgres
    - infra-payment-stripe
    - infra-payment-paypal
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask)  
**Resources:**
    
    - **Cpu:** 0.5 cores
    - **Memory:** 1GB
    
**Configuration:**
    
    - **Odoo Api Url:** http://odoo:8069
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-6-006
    - REQ-6-007
    - UAPM-1-005 (credits display)
    - REQ-6-008
    - REQ-6-010
    - REQ-6-011
    - REQ-6-012
    - REQ-3-007 (credit refund trigger)
    - REQ-6-014
    - REQ-6-015
    - REQ-6-016
    - REQ-6-017
    - REQ-6-018
    - REQ-6-001
    - REQ-6-002
    - REQ-6-003
    - REQ-6-004
    - REQ-DA-006
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - SYSTEM
      - ADMIN
      
    
    - **Id:** svc-apideveloper-main  
**Name:** API Developer Platform Service  
**Description:** Manages API access for third-party developers, including keys, usage, and webhooks.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-db-postgres
    - apigw-main
    - infra-mq-rabbitmq
    - svc-aigen-main
    - infra-secrets-manager
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask)  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 1GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-2-005
    - REQ-7-003
    - REQ-6-013
    - REQ-7-004
    - REQ-7-006
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - API_USER
      - ADMIN
      
    
    - **Id:** svc-collaboration-main  
**Name:** Real-time Collaboration Service  
**Description:** Enables concurrent editing using CRDTs via WebSockets.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-redis
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Node.js (Socket.IO) or Python (FastAPI WebSockets), Yjs  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 2GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-5-001
    - REQ-5-002
    - REQ-8-004 (collaborative aspects)
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      
    
    - **Id:** svc-notification-main  
**Name:** Notification Service  
**Description:** Delivers real-time updates (WebSockets) and push notifications (APNS/FCM).  
**Type:** Microservice  
**Dependencies:**
    
    - infra-mq-rabbitmq
    - infra-redis
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI WebSockets) or Node.js (Socket.IO)  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 1GB
    
**Configuration:**
    
    - **Apns Key Ref:** secrets/apns-key
    - **Fcm Key Ref:** secrets/fcm-key
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - CPIO-009
    - REQ-3-011 (trigger)
    - REQ-3-012 (trigger)
    - REQ-8-006
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      - SYSTEM
      
    
    - **Id:** svc-socialpublish-main  
**Name:** Social Media Publishing Service  
**Description:** Integrates with social media APIs for content publishing and scheduling.  
**Type:** Microservice  
**Dependencies:**
    
    - infra-secrets-manager
    - infra-db-postgres
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask), Social Media SDKs  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 1GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - SMPIO-001
    - SMPIO-002
    - SMPIO-003
    - SMPIO-004
    - SMPIO-005
    - SMPIO-006
    - SMPIO-007
    - REQ-2-009 (storage part)
    - SMPIO-008
    - SMPIO-011
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - USER
      - ADMIN
      
    
    - **Id:** svc-analyticsforwarder-main  
**Name:** Analytics Data Forwarding Service  
**Description:** Collects and forwards events to third-party analytics platforms.  
**Type:** Microservice  
**Dependencies:**
    
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask) or Node.js, Analytics SDKs  
**Resources:**
    
    - **Cpu:** 0.5 cores
    - **Memory:** 512MB
    
**Configuration:**
    
    - **Ga4 Stream Id:** G-XXXX
    - **Mixpanel Token:** YOUR_TOKEN
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 60
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-11-001
    - REQ-11-002
    - REQ-11-003
    - REQ-11-004
    - REQ-11-005
    - REQ-8-009 (backend forwarding)
    - REQ-SSPE-021 (backend data source)
    
**Security:**
    
    - **Requires Authentication:** False
    
    - **Id:** svc-mlops-main  
**Name:** MLOps Platform Service  
**Description:** Manages the lifecycle of custom AI models (upload, validation, deployment, monitoring).  
**Type:** Microservice  
**Dependencies:**
    
    - infra-storage-minio
    - infra-db-postgres
    - infra-aimodelserving-k8s
    - infra-monitoring-prometheus
    - infra-security-scanner
    
**Properties:**
    
    - **Version:** 1.0.0
    
**Technology:** Python (FastAPI/Flask), Kubernetes Client  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 2GB
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /health
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - AISIML-006
    - AISIML-007
    - AISIML-008
    - AISIML-009
    - AISIML-010
    - AISIML-011
    - AISIML-012
    - REQ-SSPE-014
    - REQ-20-013 (service part)
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - ADMIN
      - ENTERPRISE_USER
      
    
    - **Id:** workflow-n8n-main  
**Name:** n8n Workflow Engine  
**Description:** Orchestrates AI creative generation workflows.  
**Type:** WorkflowEngine  
**Dependencies:**
    
    - infra-mq-rabbitmq
    - infra-aimodelserving-k8s
    - infra-storage-minio
    - svc-notification-main
    - infra-ai-openai
    - infra-ai-stabilityai
    
**Properties:**
    
    - **Version:** Latest Stable n8n
    
**Technology:** n8n (Node.js)  
**Resources:**
    
    - **Cpu:** 2 cores
    - **Memory:** 4GB
    
**Configuration:**
    
    - **Rabbit Mq Url:** amqp://rabbitmq
    - **Minio Endpoint:** http://minio:9000
    
**Health Check:**
    
    - **Path:** /healthz
    - **Interval:** 30
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    - REQ-3-004
    - REQ-3-005
    - REQ-3-006
    - REQ-3-008
    - REQ-3-009
    - REQ-3-010
    - REQ-3-011
    - REQ-3-012
    - REQ-3-013
    - AISIML-001
    - AISIML-005
    - REQ-3-015
    - REQ-SSPE-013
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - SYSTEM
      
    
    - **Id:** erp-odoo-main  
**Name:** Odoo ERP Platform  
**Description:** Handles core business logic for subscriptions, billing, credits, invoicing, and customer support.  
**Type:** ERPPlatform  
**Dependencies:**
    
    - infra-db-postgres
    - infra-payment-stripe
    - infra-payment-paypal
    
**Properties:**
    
    - **Version:** Odoo 18+
    
**Technology:** Odoo (Python, XML, JavaScript)  
**Resources:**
    
    - **Cpu:** 4 cores
    - **Memory:** 16GB
    
**Configuration:**
    
    - **Db_Host:** postgres-odoo
    - **Db_User:** odoo
    
**Health Check:**
    
    - **Path:** /web/database/selector
    - **Interval:** 60
    - **Timeout:** 15
    
**Responsible Features:**
    
    - REQ-6-019
    - REQ-6-010 (rules engine)
    - REQ-6-014 (integration point)
    - REQ-6-015 (generation)
    - REQ-6-017 (calculation)
    - REQ-9-001
    - REQ-9-002
    - REQ-9-003
    - REQ-9-004 (if chat via Odoo LiveChat)
    - REQ-DA-016 (data import tools)
    - REQ-6-001
    - REQ-6-002
    - REQ-6-003
    - REQ-6-004
    - REQ-6-005 (data source)
    - REQ-6-006 (logic engine)
    - REQ-6-008 (limit enforcement source)
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - ADMIN
      - SUPPORT_AGENT
      - SALES_USER
      
    
    - **Id:** infra-aimodelserving-k8s  
**Name:** AI Model Serving Platform (Kubernetes)  
**Description:** GPU-accelerated Kubernetes cluster for hosting and serving AI models.  
**Type:** InfrastructurePlatform  
**Dependencies:**
    
    - infra-core-servers
    - infra-core-gpu
    - infra-container-registry
    
**Properties:**
    
    
**Technology:** Kubernetes, Docker, NVIDIA GPU Operator, TF Serving/TorchServe/Triton  
**Resources:**
    
    - **Cpu:** Scalable
    - **Memory:** Scalable
    - **Gpu:** Scalable (NVIDIA)
    
**Configuration:**
    
    - **K8S Api Endpoint:** https://kubernetes.default.svc
    
**Health Check:** None  
**Responsible Features:**
    
    - CPIO-008
    - AISIML-007 (hosting)
    - REQ-SSPE-011
    - REQ-SSPE-012
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - SYSTEM_ADMIN
      - MLOPS_SERVICE
      
    
    - **Id:** infra-db-postgres  
**Name:** PostgreSQL Relational Database Cluster  
**Description:** Primary RDBMS for structured application data.  
**Type:** Database  
**Dependencies:**
    
    - infra-core-servers
    - infra-core-storage
    
**Properties:**
    
    - **Version:** PostgreSQL 16+
    
**Technology:** PostgreSQL  
**Resources:**
    
    - **Cpu:** 4+ cores
    - **Memory:** 16GB+
    - **Storage:** 1TB+
    
**Configuration:**
    
    - **Max_Connections:** 200
    - **Shared_Buffers:** 4GB
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-DA-001
    - CPIO-004
    - REQ-DA-009
    - REQ-DA-011
    - REQ-DA-013
    - REQ-DA-014
    - REQ-DA-015
    - SREDRP-007
    - SREDRP-008
    - REQ-DA-004
    - REQ-DA-005
    - REQ-DA-006
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-storage-minio  
**Name:** MinIO Object Storage Cluster  
**Description:** S3-compatible storage for unstructured data.  
**Type:** ObjectStorage  
**Dependencies:**
    
    - infra-core-servers
    - infra-core-storage
    
**Properties:**
    
    
**Technology:** MinIO  
**Resources:**
    
    - **Cpu:** Scalable
    - **Memory:** Scalable
    - **Storage:** 10TB+
    
**Configuration:**
    
    - **Region:** us-east-1
    - **Replication Enabled:** True
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-DA-002
    - CPIO-005
    - REQ-DA-007
    - REQ-DA-009 (encryption)
    - REQ-DA-012
    - SREDRP-007
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-redis  
**Name:** Redis In-Memory Data Store Cluster  
**Description:** Used for caching, session management, rate limiting, and Pub/Sub.  
**Type:** Cache  
**Dependencies:**
    
    - infra-core-servers
    
**Properties:**
    
    - **Ha:** Sentinel/Cluster
    
**Technology:** Redis  
**Resources:**
    
    - **Cpu:** 2+ cores
    - **Memory:** 8GB+
    
**Configuration:**
    
    - **Persistence:** AOF
    - **Maxmemory_Policy:** allkeys-lru
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-DA-003
    - CPIO-006
    - REQ-2-006 (session store)
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-mq-rabbitmq  
**Name:** RabbitMQ Message Broker Cluster  
**Description:** Manages asynchronous job queues.  
**Type:** MessageQueue  
**Dependencies:**
    
    - infra-core-servers
    
**Properties:**
    
    - **Ha:** Mirrored Cluster
    
**Technology:** RabbitMQ  
**Resources:**
    
    - **Cpu:** 2+ cores
    - **Memory:** 8GB+
    
**Configuration:**
    
    - **Vhost:** /
    - **Default_User:** guest
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-SSPE-009
    - CPIO-007
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-secrets-manager  
**Name:** Secrets Management Service  
**Description:** Securely stores and manages API keys, database credentials, certificates, etc.  
**Type:** InfrastructureService  
**Dependencies:**
    
    - infra-core-servers
    
**Properties:**
    
    
**Technology:** HashiCorp Vault or Ansible Vault with secure backend  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 2GB
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - AISIML-003
    - REQ-DA-010
    - REQ-20-008
    - PMDT-007
    - PMDT-013
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - SYSTEM_ADMIN
      - SERVICE_ACCOUNT
      
    
    - **Id:** infra-monitoring-prometheus  
**Name:** Prometheus Monitoring System  
**Description:** Collects metrics from all system components.  
**Type:** MonitoringSystem  
**Dependencies:**
    
    - infra-core-servers
    - infra-monitoring-grafana
    - infra-monitoring-alertmanager
    
**Properties:**
    
    
**Technology:** Prometheus  
**Resources:**
    
    - **Cpu:** 2 cores
    - **Memory:** 8GB
    - **Storage:** 500GB (for metrics)
    
**Configuration:**
    
    - **Scrape_Interval:** 15s
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-001
    - MON-002
    - CPIO-014
    - PMDT-016
    - REQ-SSPE-018
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-monitoring-grafana  
**Name:** Grafana Visualization Platform  
**Description:** Provides dashboards for viewing metrics.  
**Type:** MonitoringSystem  
**Dependencies:**
    
    - infra-monitoring-prometheus
    
**Properties:**
    
    
**Technology:** Grafana  
**Resources:**
    
    - **Cpu:** 1 core
    - **Memory:** 4GB
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-003
    - CPIO-014
    - PMDT-016
    - REQ-SSPE-018
    
**Security:**
    
    - **Requires Authentication:** True
    - **Allowed Roles:**
      
      - OPS_TEAM
      - DEV_TEAM
      
    
    - **Id:** infra-monitoring-alertmanager  
**Name:** Prometheus Alertmanager  
**Description:** Handles alerts based on Prometheus metrics.  
**Type:** MonitoringSystem  
**Dependencies:**
    
    - infra-monitoring-prometheus
    
**Properties:**
    
    
**Technology:** Prometheus Alertmanager  
**Resources:**
    
    - **Cpu:** 0.5 cores
    - **Memory:** 1GB
    
**Configuration:**
    
    - **Config_File:** /etc/alertmanager/config.yml
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-011
    - MON-012
    - MON-013
    - CPIO-015
    - REQ-QAS-009
    - REQ-SSPE-020
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-logging-elk-loki  
**Name:** Centralized Logging Platform (ELK/Loki)  
**Description:** Aggregates, stores, and analyzes logs from all components.  
**Type:** LoggingSystem  
**Dependencies:**
    
    - infra-core-servers
    
**Properties:**
    
    
**Technology:** Elasticsearch/Logstash/Kibana or Grafana Loki/Fluentd  
**Resources:**
    
    - **Cpu:** 4+ cores
    - **Memory:** 16GB+
    - **Storage:** 2TB+ (for logs)
    
**Configuration:**
    
    - **Log_Retention_Days:** 30
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-004
    - MON-005
    - MON-006
    - MON-007
    - CPIO-014
    - PMDT-017
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-cicd-pipeline  
**Name:** CI/CD Pipeline  
**Description:** Automates build, test, security scanning, and deployment processes.  
**Type:** DevOpsTool  
**Dependencies:**
    
    - infra-scm-git
    - infra-container-registry
    - infra-configmgmt-ansible
    - infra-secrets-manager
    - infra-security-scanner
    
**Properties:**
    
    
**Technology:** GitLab CI/CD or GitHub Actions  
**Resources:**
    
    - **Cpu:** Shared (CI runners)
    - **Memory:** Shared
    
**Configuration:**
    
    - **.Gitlab-Ci.Yml / .Github/Workflows:** version-controlled
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-20-001
    - REQ-20-002
    - REQ-20-003
    - REQ-20-004
    - REQ-20-005
    - REQ-20-006
    - REQ-20-007
    - REQ-20-013
    - PMDT-001
    - PMDT-002
    - PMDT-003
    - PMDT-004
    - PMDT-005
    - PMDT-006
    - CPIO-013
    - REQ-QAS-007 (pipeline is part of quality gate)
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-configmgmt-ansible  
**Name:** Configuration Management (Ansible)  
**Description:** Automates provisioning, configuration, and management of servers.  
**Type:** DevOpsTool  
**Dependencies:**
    
    - infra-scm-git
    - infra-secrets-manager
    
**Properties:**
    
    
**Technology:** Ansible  
**Resources:**
    
    - **Cpu:** Control Node: 1 core
    - **Memory:** Control Node: 2GB
    
**Configuration:**
    
    - **Inventory_File:** hosts.ini
    - **Playbooks_Dir:** /etc/ansible/playbooks
    
**Health Check:** None  
**Responsible Features:**
    
    - CPIO-011
    - REQ-20-009
    - REQ-20-010
    - REQ-20-011
    - PMDT-011
    - PMDT-012
    - PMDT-018
    - REQ-SDS-009
    
**Security:**
    
    - **Requires Authentication:** True
    
    - **Id:** infra-cdn-cloudflare  
**Name:** CDN & Security (Cloudflare)  
**Description:** Global content delivery, caching, DDoS protection, WAF.  
**Type:** InfrastructureService  
**Dependencies:**
    
    
**Properties:**
    
    
**Technology:** Cloudflare  
**Resources:**
    
    
**Configuration:**
    
    - **Dns_Records_Managed:** True
    - **Waf_Rules_Enabled:** True
    
**Health Check:** None  
**Responsible Features:**
    
    - CPIO-001
    - REQ-SSPE-010
    - CPIO-010 (WAF/DDoS)
    
**Security:** None  
    - **Id:** infra-payment-stripe  
**Name:** Payment Gateway Integration (Stripe)  
**Description:** Integration point for Stripe payment processing.  
**Type:** ExternalServiceIntegration  
**Dependencies:**
    
    - erp-odoo-main
    
**Properties:**
    
    
**Technology:** Stripe SDK  
**Resources:**
    
    
**Configuration:**
    
    - **Api Key Ref:** secrets/stripe-api-key
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-6-014
    
**Security:** None  
    - **Id:** infra-payment-paypal  
**Name:** Payment Gateway Integration (PayPal)  
**Description:** Integration point for PayPal payment processing.  
**Type:** ExternalServiceIntegration  
**Dependencies:**
    
    - erp-odoo-main
    
**Properties:**
    
    
**Technology:** PayPal SDK  
**Resources:**
    
    
**Configuration:**
    
    - **Client Id Ref:** secrets/paypal-client-id
    
**Health Check:** None  
**Responsible Features:**
    
    - REQ-6-014
    
**Security:** None  
    - **Id:** infra-ai-openai  
**Name:** OpenAI Service Integration  
**Description:** Integration point for OpenAI models (GPT-4, DALL-E 3).  
**Type:** ExternalServiceIntegration  
**Dependencies:**
    
    - workflow-n8n-main
    - infra-secrets-manager
    
**Properties:**
    
    
**Technology:** OpenAI SDK/REST API  
**Resources:**
    
    
**Configuration:**
    
    - **Api Key Ref:** secrets/openai-api-key
    
**Health Check:** None  
**Responsible Features:**
    
    - AISIML-001
    
**Security:** None  
    - **Id:** infra-ai-stabilityai  
**Name:** Stability AI Service Integration  
**Description:** Integration point for Stability AI models (Stable Diffusion).  
**Type:** ExternalServiceIntegration  
**Dependencies:**
    
    - workflow-n8n-main
    - infra-secrets-manager
    
**Properties:**
    
    
**Technology:** Stability AI SDK/REST API  
**Resources:**
    
    
**Configuration:**
    
    - **Api Key Ref:** secrets/stabilityai-api-key
    
**Health Check:** None  
**Responsible Features:**
    
    - AISIML-001
    
**Security:** None  
    - **Id:** sharedlib-security  
**Name:** Shared Security Library  
**Description:** Provides common security utilities for input validation, output encoding, CSRF protection, etc.  
**Type:** Library  
**Dependencies:**
    
    
**Properties:**
    
    - **Language:** Python/TypeScript/Dart
    
**Technology:** Language-specific security libraries (e.g., OWASP ESAPI, bleach)  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - SPR-001
    - SPR-002
    
**Security:** None  
    - **Id:** sharedlib-i18n  
**Name:** Shared Internationalization Library  
**Description:** Provides utilities for string translation and localization.  
**Type:** Library  
**Dependencies:**
    
    
**Properties:**
    
    - **Language:** Python/TypeScript/Dart
    
**Technology:** gettext, i18next, intl package (Dart)  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - PLI-001
    - PLI-002
    - PLI-004
    - PLI-005
    - PLI-009
    
**Security:** None  
    - **Id:** sharedlib-logging  
**Name:** Shared Logging Library  
**Description:** Standardizes logging formats and practices across services.  
**Type:** Library  
**Dependencies:**
    
    
**Properties:**
    
    - **Language:** Python/TypeScript/Dart
    
**Technology:** Standard logging modules, structlog (Python)  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-005
    
**Security:** None  
    - **Id:** sharedlib-errorhandling  
**Name:** Shared Error Handling Library  
**Description:** Centralizes error handling logic and reporting.  
**Type:** Library  
**Dependencies:**
    
    - sharedlib-logging
    
**Properties:**
    
    - **Language:** Python/TypeScript/Dart
    
**Technology:** Custom error classes, middleware/decorators  
**Resources:**
    
    
**Configuration:**
    
    
**Health Check:** None  
**Responsible Features:**
    
    - MON-008
    - REQ-14-009
    
**Security:** None  
    
  - **Configuration:**
    
    - **Environment:** production
    - **Logging Level:** INFO
    - **Trace Propagation Enabled:** True
    - **Default Language:** en-US
    - **Default Timezone:** UTC
    
  


---

