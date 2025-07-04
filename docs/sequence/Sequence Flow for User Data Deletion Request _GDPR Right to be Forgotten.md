# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . User Data Deletion Request (GDPR Right to be Forgotten)
  Outlines the process for handling a user's request to delete their personal data in compliance with GDPR Article 17.

  #### .4. Purpose
  To ensure compliance with data privacy regulations regarding user data deletion.

  #### .5. Type
  ComplianceFlow

  #### .6. Participant Repository Ids
  
  - repo-webapp-pwa
  - comp-apigateway-nginx
  - svc-odoo-backend
  - repo-db-postgresql
  - repo-storage-minio
  - comp-messagequeue-rabbitmq
  - svc-notification-service
  
  #### .7. Key Interactions
  
  - User initiates data deletion request via their profile settings in WebApp.
  - WebApp sends request to Odoo Backend via API Gateway.
  - Odoo Backend verifies user identity and logs the request for audit purposes.
  - Odoo Backend initiates data deletion process:
  -   - Marks user account for deletion/anonymization in PostgreSQL (soft delete initially, then hard delete/anonymize after grace period/confirmation as per Section 7.5).
  -   - Triggers deletion/anonymization of associated personal data in other tables (e.g., profiles, brand kits, non-essential usage logs).
  -   - Publishes events to RabbitMQ for other services to delete/anonymize user-specific data (e.g., UserDeletionRequested event).
  -   - For user-uploaded assets in MinIO, schedules them for deletion according to retention policies (Section 7.5).
  -   - For AI-generated creatives in MinIO, links to user, also scheduled for deletion.
  - Odoo Backend confirms deletion process initiation to the user via WebApp/Notification Service.
  - Automated jobs or manual processes complete the permanent deletion/anonymization after the defined period (e.g., 30 days), respecting legal holds (e.g., financial transaction records retained longer).
  
  #### .8. Related Feature Ids
  
  - SEC-004
  - Section 7.5
  - NFR-006
  
  #### .9. Domain
  DataPrivacy

  #### .10. Metadata
  
  - **Complexity:** High
  - **Priority:** Critical
  


---

# 2. Sequence Diagram Details

- **Success:** True
- **Cache_Created:** True
- **Status:** refreshed
- **Cache_Id:** sa82fb5u7x8prukjd65oqd30zx77obk6vylduvxy
- **Cache_Name:** cachedContents/sa82fb5u7x8prukjd65oqd30zx77obk6vylduvxy
- **Cache_Display_Name:** repositories
- **Cache_Status_Verified:** True
- **Model:** models/gemini-2.5-pro-preview-03-25
- **Workflow_Id:** I9v2neJ0O4zJsz8J
- **Execution_Id:** AIzaSyCGei_oYXMpZW-N3d-yH-RgHKXz8dsixhc
- **Project_Id:** 17
- **Record_Id:** 22
- **Cache_Type:** repositories


---

