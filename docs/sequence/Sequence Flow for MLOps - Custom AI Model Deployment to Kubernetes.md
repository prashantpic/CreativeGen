# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . MLOps - Custom AI Model Deployment to Kubernetes
  Details the process of an administrator deploying a new custom AI model version through the MLOps pipeline to the Kubernetes GPU cluster.

  #### .4. Purpose
  To illustrate the platform's capability to host and manage custom AI models, enabling advanced customization and experimentation.

  #### .5. Type
  OperationalFlow

  #### .6. Participant Repository Ids
  
  - repo-webapp-pwa
  - comp-apigateway-nginx
  - svc-odoo-backend
  - repo-storage-minio
  - repo-db-postgresql
  - svc-ci-cd-pipeline
  - comp-k8s-cluster
  
  #### .7. Key Interactions
  
  - Admin uploads model artifacts (e.g., ONNX file, Dockerfile for custom server) via an admin interface in WebApp or dedicated MLOps tool.
  - Request to Odoo Backend (or dedicated MLOps service) to register new model/version.
  - Model artifacts stored in MinIO (INT-007 Model Registry).
  - Metadata (version, parameters, lineage) stored in PostgreSQL (INT-007 Model Registry).
  - Automated validation & security scanning (e.g., Snyk for container, format checks) triggered (INT-007).
  - If validation passes, Admin approves deployment to staging via interface.
  - CI/CD Pipeline (DEP-003) picks up deployment request:
  -   - Builds model serving container image.
  -   - Pushes image to private container registry.
  -   - Applies Kubernetes manifests (Deployment, Service) to deploy the model to staging GPU cluster.
  - Admin performs tests on staging. If successful, promotes to production.
  - CI/CD Pipeline deploys to production Kubernetes cluster (canary or blue-green - INT-007).
  - Model endpoint is registered and available for n8n workflows.
  
  #### .8. Related Feature Ids
  
  - INT-007
  - AISIML-006
  - AISIML-007
  - AISIML-008
  - AISIML-009
  - AISIML-010
  - DEP-003
  
  #### .9. Domain
  MLOps

  #### .10. Metadata
  
  - **Complexity:** High
  - **Priority:** Medium
  


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

