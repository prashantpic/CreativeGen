sequenceDiagram
    actor "Developer Workstation" as ext-developer-workstation
    participant "Git Repository" as svc-git-repository
    participant "CI/CD Pipeline Orchestrator" as svc-ci-cd-pipeline
    participant "Container Registry" as svc-container-registry
    participant "Secrets Vault" as svc-secrets-vault
    participant "Staging Kubernetes Cluster" as comp-k8s-cluster

    activate ext-developer-workstation
    ext-developer-workstation-svc-git-repository: 1. Push Code Changes (AI Generation Service)
    activate svc-git-repository
    svc-git-repository--ext-developer-workstation: Push Acknowledged
    deactivate ext-developer-workstation

    svc-git-repository-svc-ci-cd-pipeline: 2. Trigger Pipeline (Webhook/Git Hook)
    deactivate svc-git-repository
    activate svc-ci-cd-pipeline

    svc-ci-cd-pipeline-svc-git-repository: 3. Checkout Code (latest commit)
    activate svc-git-repository
    svc-git-repository--svc-ci-cd-pipeline: Return Code Files
    deactivate svc-git-repository

    svc-ci-cd-pipeline-svc-ci-cd-pipeline: 4. Execute Build Stage
    note over svc-ci-cd-pipeline: Build Stage includes: Compiling code, Running linters, Performing static analysis. (QA-001)

    alt Build Success
        svc-ci-cd-pipeline-svc-ci-cd-pipeline: 5. [IF Build Success] Execute Test Stage
        note over svc-ci-cd-pipeline: Test Stage includes: Running unit tests, Running integration tests. (QA-001)

        alt Test Success
            svc-ci-cd-pipeline-svc-ci-cd-pipeline: 6. [IF Test Success] Execute Security Scan Stage
            note over svc-ci-cd-pipeline: Security Scan Stage includes: SAST, DAST (code/config based), Dependency Vulnerability Scans. (QA-001)

            alt Security Scan Success
                svc-ci-cd-pipeline-svc-ci-cd-pipeline: 7. [IF Security Scan Success] Build Docker Container Image

                alt Image Build Success
                    svc-ci-cd-pipeline-svc-container-registry: 8. [IF Image Build Success] Push Docker Image (e.g., ai-gen-service:v1.1.0-staging)
                    activate svc-container-registry
                    svc-container-registry--svc-ci-cd-pipeline: Image Push Confirmation/Status (Success/Failure)
                    deactivate svc-container-registry

                    alt Image Push Success
                        svc-ci-cd-pipeline-svc-ci-cd-pipeline: 9. [IF Image Push Success] Initiate Deployment to Staging

                        svc-ci-cd-pipeline-svc-git-repository: 9.1. Fetch Deployment Configs (K8s manifests, Ansible playbooks)
                        activate svc-git-repository
                        svc-git-repository--svc-ci-cd-pipeline: Return Deployment Configs
                        deactivate svc-git-repository

                        svc-ci-cd-pipeline-svc-secrets-vault: 9.2. Retrieve Secrets (DB creds for migrations, Staging specific secrets)
                        activate svc-secrets-vault
                        svc-secrets-vault--svc-ci-cd-pipeline: Return Secrets
                        deactivate svc-secrets-vault

                        svc-ci-cd-pipeline-svc-ci-cd-pipeline: 9.3. Execute Infrastructure Configuration (Ansible, if applicable)
                        note over svc-ci-cd-pipeline: Pipeline uses fetched Ansible playbooks to configure Staging environment infrastructure if needed (DEP-004.1). This step might target Kubernetes nodes or other related infrastructure components.

                        alt Infra Config Success OR N/A
                            svc-ci-cd-pipeline-comp-k8s-cluster: 9.4. [IF Infra Config Success OR N/A] Apply K8s Manifests (Update AI Gen Service - Rolling Update)
                            activate comp-k8s-cluster
                            comp-k8s-cluster--svc-ci-cd-pipeline: Manifest Apply Initiated

                            svc-ci-cd-pipeline-comp-k8s-cluster: 9.5. Monitor Deployment Rollout Status
                            comp-k8s-cluster--svc-ci-cd-pipeline: Deployment Rollout Status (Success/Failure)

                            alt Rollout Success
                                svc-ci-cd-pipeline-comp-k8s-cluster: 9.6. [IF Rollout Success] Execute DB Migration Job (Flyway/Liquibase)
                                comp-k8s-cluster--svc-ci-cd-pipeline: DB Migration Job Status (Success/Failure)

                                alt DB Migration Success
                                    svc-ci-cd-pipeline-comp-k8s-cluster: 9.7. [IF DB Migration Success] Perform Automated Smoke Tests/Health Checks (on deployed service endpoint)
                                    comp-k8s-cluster--svc-ci-cd-pipeline: Smoke Test/Health Check Results (Success/Failure)
                                end
                            end
                            deactivate comp-k8s-cluster
                        end
                    end
                end
            end
        end
    end

    svc-ci-cd-pipeline-svc-ci-cd-pipeline: 10. Finalize Deployment & Report Overall Staging Deployment Status

    svc-ci-cd-pipeline-svc-git-repository: 10.1. Update Commit Status (Staging Deployment: Success/Failure)
    activate svc-git-repository
    svc-git-repository--svc-ci-cd-pipeline: Status Update Acknowledged
    deactivate svc-git-repository

    deactivate svc-ci-cd-pipeline

    note over ext-developer-workstation, comp-k8s-cluster: If any critical stage (Build, Test, Security Scan, Image Build/Push, Deployment steps) fails, the pipeline stops, reports failure, and does not proceed to subsequent stages.