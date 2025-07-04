# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . Real-Time Collaborative Editing on a Project
  Shows how multiple users can concurrently edit a creative project, with changes synchronized in real-time using CRDTs.

  #### .4. Purpose
  To illustrate the collaborative editing feature, a key differentiator of the platform.

  #### .5. Type
  FeatureFlow

  #### .6. Participant Repository Ids
  
  - repo-webapp-pwa
  - svc-crdt-collaboration
  - svc-notification-service
  - repo-db-postgresql
  - repo-storage-minio
  
  #### .7. Key Interactions
  
  - User A makes an edit (e.g., moves an element) in a shared project on WebApp.
  - WebApp sends change (CRDT update) to Collaboration Service (e.g., via WebSocket managed by Notification Service, or dedicated CRDT sync server).
  - Collaboration Service processes CRDT update, resolves conflicts if any.
  - Collaboration Service broadcasts merged CRDT update to all connected clients (User A, User B, User C) in the same project session.
  - WebApp of User B and User C receive update and apply changes to their local views.
  - Periodically, or on significant changes, consolidated state is persisted by Collaboration Service to PostgreSQL (project data) and MinIO (asset updates if applicable).
  - Change history/versions are logged (REQ-013).
  
  #### .8. Related Feature Ids
  
  - REQ-013
  - REQ-019.1
  - Section 5.3.2
  
  #### .9. Domain
  Collaboration

  #### .10. Metadata
  
  - **Complexity:** High
  - **Priority:** High
  


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

