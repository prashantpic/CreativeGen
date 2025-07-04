# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . AI Creative Generation - Sample and Final (Web App)
  Details the end-to-end process of a user generating AI creative samples, selecting one, and generating a high-resolution final asset through the web application. Covers interactions from frontend through Odoo, RabbitMQ, n8n, AI cluster, and back.

  #### .4. Purpose
  To illustrate the core product functionality of AI-powered creative generation, including the multi-step asynchronous workflow.

  #### .5. Type
  UserJourney

  #### .6. Participant Repository Ids
  
  - repo-webapp-pwa
  - comp-apigateway-nginx
  - svc-odoo-backend
  - comp-messagequeue-rabbitmq
  - svc-n8n-workflow-engine
  - comp-k8s-cluster
  - ext-ai-openai
  - repo-storage-minio
  - svc-notification-service
  - repo-db-postgresql
  
  #### .7. Key Interactions
  
  - User submits creative request (prompt, params) via WebApp.
  - API Gateway routes to Odoo Backend.
  - Odoo validates, checks credits (REQ-016), records request in PostgreSQL.
  - Odoo publishes 'AIGenerationJobRequested' to RabbitMQ.
  - n8n consumes job, orchestrates AI model call (e.g., to OpenAI via ext-ai-openai, or custom model on comp-k8s-cluster).
  - AI model generates samples, n8n stores them in MinIO.
  - n8n publishes 'AIGenerationSamplesReady' to RabbitMQ (includes sample URLs, updates PostgreSQL via Odoo/direct).
  - Notification Service consumes event, notifies WebApp via WebSocket.
  - WebApp displays samples to user.
  - User selects a sample; WebApp sends selection to Odoo Backend.
  - Odoo triggers n8n for high-res generation (via RabbitMQ).
  - n8n orchestrates high-res generation, stores final asset in MinIO.
  - n8n publishes 'AIGenerationFinalAssetReady', Odoo updates PostgreSQL, Notification Service informs WebApp.
  
  #### .8. Related Feature Ids
  
  - REQ-005
  - REQ-006
  - REQ-008
  - REQ-009
  - REQ-016
  - NFR-001
  - Section 5.3.1
  
  #### .9. Domain
  CreativeGeneration

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

