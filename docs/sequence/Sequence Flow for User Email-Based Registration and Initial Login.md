# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . User Email-Based Registration and Initial Login
  Illustrates the sequence of interactions when a new user registers using their email, verifies their email, and logs in for the first time. Includes optional progressive profiling trigger.

  #### .4. Purpose
  To document the complete user onboarding flow for email-based registration, including verification and initial login, which is a critical path for user acquisition.

  #### .5. Type
  UserJourney

  #### .6. Participant Repository Ids
  
  - repo-webapp-pwa
  - comp-apigateway-nginx
  - svc-odoo-backend
  - comp-messagequeue-rabbitmq
  - svc-notification-service
  - repo-db-postgresql
  
  #### .7. Key Interactions
  
  - User submits registration form via WebApp.
  - API Gateway routes request to Odoo Backend.
  - Odoo Backend creates user record (unverified), stores verification token in PostgreSQL.
  - Odoo Backend publishes 'UserRegisteredNeedsVerification' event to RabbitMQ.
  - Notification Service consumes event, sends verification email.
  - User clicks verification link, request hits Odoo Backend via API Gateway.
  - Odoo Backend verifies token, updates user status to verified in PostgreSQL.
  - User logs in with credentials via WebApp.
  - Odoo Backend validates credentials, issues JWT.
  - WebApp may trigger progressive profiling questions.
  
  #### .8. Related Feature Ids
  
  - REQ-001
  - UAPM-1-001
  - SEC-001
  
  #### .9. Domain
  UserManagement

  #### .10. Metadata
  
  - **Complexity:** Medium
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

