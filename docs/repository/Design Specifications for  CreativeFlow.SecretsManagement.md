# Software Design Specification: CreativeFlow.SecretsManagement

## 1. Introduction

### 1.1 Purpose
This document provides the detailed Software Design Specification (SDS) for the `CreativeFlow.SecretsManagement` repository. This system is responsible for the secure storage, management, and controlled access to all sensitive information (secrets) used by the CreativeFlow AI platform. This includes API keys, database credentials, certificates, and encryption keys. The primary technology employed will be HashiCorp Vault 1.16.2, complemented by Ansible Vault for secrets used within Ansible automation.

### 1.2 Scope
The scope of this SDS covers:
*   Configuration of the HashiCorp Vault server.
*   Setup of authentication methods (AppRole, Kubernetes).
*   Configuration of secrets engines (KVv2, Transit, Database).
*   Definition of access control policies.
*   Auditing configuration.
*   Vault Agent configuration and templates.
*   Ansible Vault setup and usage guidelines.
*   Scripts for applying configurations.
*   Operational procedures related to secrets management.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **SDS**: Software Design Specification
*   **KMS**: Key Management Service
*   **Vault**: HashiCorp Vault
*   **HCL**: HashiCorp Configuration Language
*   **KV**: Key-Value
*   **EaaS**: Encryption as a Service
*   **AppRole**: An authentication method in Vault for applications/machines.
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **IaC**: Infrastructure as Code
*   **CTMPL**: Consul Template Language
*   **PKI**: Public Key Infrastructure
*   **CA**: Certificate Authority
*   **mTLS**: Mutual Transport Layer Security

## 2. System Overview

The `CreativeFlow.SecretsManagement` system is a critical security component of the CreativeFlow AI platform. It leverages:

*   **HashiCorp Vault (version 1.16.2)**: A tool for securely accessing secrets. It provides a unified interface to any secret, while providing tight access control and recording a detailed audit log. It will be used for managing dynamic secrets, encryption keys, application credentials, and API keys for third-party services.
*   **Ansible Vault**: A feature of Ansible that allows encryption of sensitive data in Ansible playbooks, such as variables or files. It will be used to protect secrets consumed directly by Ansible automation scripts.

The system ensures that secrets are not hardcoded in applications, configuration files, or version control systems. It provides mechanisms for programmatic and human access to secrets based on authenticated identity and authorized policies.

## 3. Requirements Addressed

This system directly addresses the following platform requirements:

*   **SEC-003 (Cryptographic key management using KMS)**: Implemented via Vault's Transit secrets engine.
*   **DEP-003 (Secure handling of secrets in CI/CD)**: Implemented via Vault AppRole/Kubernetes authentication for CI/CD systems and appropriate policies.
*   **DEP-004.1 (Secrets management with Ansible Vault or HashiCorp Vault)**: Both tools are specified within this SDS for their respective use cases.
*   **INT-006 (Secure External AI Service API Key Management)**: External AI service API keys will be stored securely within Vault's KVv2 secrets engine.

## 4. Architectural Design

### 4.1 Core Principles
*   **Least Privilege**: Entities (users, applications, systems) are granted only the permissions necessary to perform their intended functions.
*   **Defense in Depth**: Multiple layers of security controls are implemented.
*   **Ephemeral Credentials**: Dynamic secrets with short TTLs are preferred over static, long-lived credentials where possible (e.g., database access).
*   **Auditability**: All access and operations within Vault are meticulously logged.
*   **Configuration as Code**: Vault and related configurations are defined in HCL and version-controlled.

### 4.2 HashiCorp Vault Architecture

#### 4.2.1 Storage Backend
Vault will be configured with an integrated storage backend, preferably **Raft**, for high availability (HA) without external dependencies for the storage layer. This allows for a clustered Vault setup.

#### 4.2.2 Authentication Methods
*   **AppRole**: For applications and services running outside Kubernetes, and potentially for CI/CD runners. Each application/service will have a distinct RoleID and will be responsible for securely obtaining its SecretID.
*   **Kubernetes**: For applications and services running within the Kubernetes cluster. Pods will authenticate using their Kubernetes Service Account Tokens.

#### 4.2.3 Secrets Engines
*   **KV Version 2 (KVv2)**: For storing arbitrary secrets like API keys for third-party services (OpenAI, StabilityAI, Stripe, PayPal), application configuration parameters, etc. Versioning of secrets is a key feature.
*   **Transit**: For Encryption as a Service (EaaS). Manages named encryption keys for encrypting/decrypting data within applications without exposing the keys themselves. Supports key rotation.
*   **Database**: For dynamically generating database credentials (username/password) for applications accessing PostgreSQL. Vault will manage a privileged account on the database to create and revoke these ephemeral credentials.
*   **PKI (Conditional)**: If `enable_pki_engine_root` and `enable_pki_engine_intermediate` feature toggles are true, PKI engines will be configured to manage internal Certificate Authorities (Root and Intermediate) for issuing TLS certificates to internal services, enabling mTLS and securing internal communications.

#### 4.2.4 Policies and Access Control
Granular access control policies, written in HCL, will define what authenticated entities can access which paths and perform which operations within Vault. Policies will be attached to entities via their authentication method roles.

#### 4.2.5 Auditing
Audit devices will be configured to log all requests and responses to Vault. A file-based audit device is the minimum requirement, with logs securely stored and regularly reviewed.

#### 4.2.6 Vault Agent
Vault Agent will be used by applications (as a sidecar or host agent) to:
*   Automate authentication to Vault.
*   Retrieve secrets and render them into configuration files using templates (CTMPL).
*   Cache secrets to reduce load on Vault server and improve resilience.
*   Keep secrets fresh by automatically re-fetching them upon lease expiry or changes.

### 4.3 Ansible Vault Architecture

#### 4.3.1 Encrypted Variable Storage
Ansible Vault will be used to encrypt sensitive data within Ansible variable files (e.g., `group_vars/all/secrets.yml`). This protects secrets used directly by Ansible playbooks during infrastructure provisioning and configuration management.

#### 4.3.2 Vault Password Management
The Ansible Vault password itself is highly sensitive and **MUST NOT** be stored in version control. Procedures will be established for securely managing and providing this password to developers and CI/CD systems (e.g., retrieving from HashiCorp Vault, CI/CD secret variables).

## 5. Detailed Configuration Specifications

This section details the configuration for each file defined in the repository structure.

### 5.1 HashiCorp Vault Configurations

#### 5.1.1 `hashicorp_vault/config/server.hcl`
*   **Purpose**: Main server configuration for HashiCorp Vault.
*   **Key Parameters**:
    *   `listener "tcp"`:
        *   `address`: e.g., `"0.0.0.0:8200"` or specific interface.
        *   `tls_disable`: `false` (TLS should be enabled for production).
        *   `tls_cert_file`: Path to TLS certificate.
        *   `tls_key_file`: Path to TLS private key.
        *   `tls_client_ca_file`: (Optional) For client certificate authentication.
    *   `storage "raft"`:
        *   `path`: e.g., `"/opt/vault/data"` (persistent storage path for Vault data).
        *   `node_id`: Unique ID for each node in a Raft cluster (if clustered).
        *   (Other Raft parameters like `retry_join`, `leader_addr` for clustering).
    *   `api_addr`: Publicly accessible address of this Vault node (e.g., `"https://vault.creativeflow.ai:8200"`).
    *   `cluster_addr`: Address for inter-node communication in a HA cluster (e.g., `"https://vault-internal-node1.creativeflow.local:8201"`).
    *   `ui`: `true` (to enable the web UI).
    *   `telemetry`:
        *   `statsite_address` / `statsd_address`: (Optional) Configure if metrics are pushed.
        *   `disable_hostname`: `true` (to avoid sending hostname).
        *   `prometheus_retention_time`: (If exposing Prometheus metrics endpoint).
    *   `disable_mlock`: `true` (generally recommended unless specific tuning requires it and implications are understood; prevents Vault from locking memory, which can be problematic in resource-constrained environments or VMs).
*   **Security Considerations**: TLS must be enforced. Storage path permissions must be restricted. `disable_mlock` should be carefully considered based on the deployment environment.
*   **Relationship to Requirements**: SEC-003, DEP-004.1.

#### 5.1.2 `hashicorp_vault/config/audit_file.hcl`
*   **Purpose**: Configure file-based auditing for Vault.
*   **Key Parameters**:
    *   `audit "file"`:
        *   `type`: `"file"`
        *   `options`:
            *   `file_path`: e.g., `"/var/log/vault/vault_audit.log"` (ensure path is secure and has sufficient space).
            *   `log_raw`: `false` (generally recommended, as Vault attempts to redact secrets from responses. Set to `true` only if absolutely necessary and with full understanding of risks).
            *   `hmac_accessor`: `true` (to HMAC accessor values in the audit log).
            *   `format`: `"json"` (for easier parsing by log management systems).
            *   `mode`: File permissions, e.g., `"0600"`.
*   **Security Considerations**: Audit log files must be protected from unauthorized access and modification. Log rotation and retention policies must be implemented externally (e.g., using logrotate).
*   **Relationship to Requirements**: SEC-003.

#### 5.1.3 `hashicorp_vault/auth_methods/approle.hcl`
*   **Purpose**: Enable and configure AppRole authentication.
*   **Key Parameters (example using `vault write` or Terraform resource `vault_auth_backend` and `vault_approle_auth_backend_role`):**
    *   Enable command: `vault auth enable -path=approle approle`
    *   Role definition (e.g., for `webapp`):
        hcl
        // This would be applied via 'vault write auth/approle/role/webapp-role' or Terraform
        // path "auth/approle/role/webapp-role" {
        //   role_name = "webapp-role" // Implicit
        //   secret_id_ttl = "10m"
        //   token_num_uses = 10
        //   token_ttl = "20m"
        //   token_max_ttl = "30m"
        //   token_policies = ["applications_base_policy", "webapp-specific-policy"] // Example policies
        //   bind_secret_id = true
        //   secret_id_num_uses = 1
        // }
        
        This HCL file (`approle.hcl`) would typically be used with a tool like Terraform to manage these configurations declaratively. If using `vault cli` directly in the `apply_vault_configurations.sh` script, it would translate to `vault write` commands. For example:
        `vault write auth/approle/role/webapp-role token_policies="applications_base_policy,webapp-specific-policy" secret_id_ttl="10m" token_ttl="20m" secret_id_num_uses=1`
*   **Security Considerations**: RoleID should be treated as non-sensitive, but SecretID is highly sensitive and should have a short TTL and limited uses. Securely distribute SecretIDs to applications.
*   **Relationship to Requirements**: DEP-003, DEP-004.1.

#### 5.1.4 `hashicorp_vault/auth_methods/kubernetes.hcl`
*   **Purpose**: Enable and configure Kubernetes authentication.
*   **Key Parameters (example using `vault write` or Terraform):**
    *   Enable command: `vault auth enable -path=kubernetes kubernetes`
    *   Configuration:
        `vault write auth/kubernetes/config kubernetes_host="https_K8S_API_URL" kubernetes_ca_cert=@/path/to/ca.crt token_reviewer_jwt=@/path/to/reviewer_sa_token.jwt`
    *   Role definition (e.g., for `ai-processing-service`):
        `vault write auth/kubernetes/role/ai-processing-role bound_service_account_names=ai-processor-sa bound_service_account_namespaces=ai-processing token_policies="applications_base_policy,ai-processing-policy" ttl=24h`
*   **Security Considerations**: Secure the `token_reviewer_jwt`. Ensure Kubernetes RBAC restricts which service accounts can be used for Vault authentication.
*   **Relationship to Requirements**: DEP-003.

#### 5.1.5 `hashicorp_vault/secrets_engines/kv_v2_applications.hcl`
*   **Purpose**: Enable and configure KV Version 2 secrets engine for application secrets.
*   **Key Parameters (example using `vault write` or Terraform):**
    *   Enable command: `vault secrets enable -path=secret -version=2 kv`
    *   (Optional) Tune versions: `vault write secret/config max_versions=10 delete_version_after=2160h` (e.g. 90 days)
*   **Structure**: Secrets will be organized hierarchically, e.g.:
    *   `secret/data/webapp/prod/database` (username, password - if static)
    *   `secret/data/apigateway/common/ratelimit_config`
    *   `secret/data/ai_services/openai/api_key` (INT-006)
    *   `secret/data/ai_services/stabilityai/api_key` (INT-006)
    *   `secret/data/cicd/prod/deployment_token`
*   **Security Considerations**: Access to paths within this engine will be strictly controlled by policies. Regular review of secrets and rotation where applicable.
*   **Relationship to Requirements**: SEC-003, DEP-003, INT-006.

#### 5.1.6 `hashicorp_vault/secrets_engines/transit_application_keys.hcl`
*   **Purpose**: Enable and configure Transit secrets engine for EaaS.
*   **Key Parameters (example using `vault write` or Terraform):**
    *   Enable command: `vault secrets enable -path=transit transit`
    *   Create named encryption keys:
        `vault write -f transit/keys/app-data-encryption-key type=aes256-gcm96 exportable=false allow_plaintext_backup=false`
        `vault write -f transit/keys/user-pii-encryption-key type=aes256-gcm96`
    *   Configure key rotation:
        `vault write transit/keys/app-data-encryption-key/config rotation_period=2592000s` (30 days)
*   **Security Considerations**: Access to encrypt/decrypt operations and key management operations must be strictly controlled by policies. Keys should be non-exportable.
*   **Relationship to Requirements**: SEC-003.

#### 5.1.7 `hashicorp_vault/secrets_engines/database_dynamic_credentials.hcl`
*   **Purpose**: Enable dynamic generation of PostgreSQL credentials.
*   **Key Parameters (example using `vault write` or Terraform):**
    *   Enable command: `vault secrets enable database`
    *   Configure database connection (e.g., `postgresql-main`):
        
        vault write database/config/postgresql-main \
            plugin_name=postgresql-database-plugin \
            connection_url="postgresql://{{username}}:{{password}}@dbhost:5432/creativeflowdb?sslmode=disable" \
            allowed_roles="app-readonly,app-readwrite" \
            username="vault_db_admin" \
            password="VAULT_DB_ADMIN_PASSWORD_FROM_SECURE_SOURCE"
        
    *   Define roles (e.g., `app-readonly`):
        
        vault write database/roles/app-readonly \
            db_name=postgresql-main \
            creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
            default_ttl="1h" \
            max_ttl="24h"
        
*   **Security Considerations**: The `vault_db_admin` user needs sufficient privileges to create and manage other users/roles. `connection_url` needs to be secured.
*   **Relationship to Requirements**: SEC-003.

#### 5.1.8 `hashicorp_vault/policies/applications_base_policy.hcl`
*   **Purpose**: Base policy for applications.
*   **Content Example**:
    hcl
    # Allow reading secrets from a common application path
    path "secret/data/common/*" {
      capabilities = ["read"]
    }

    # Allow reading secrets specific to an application, identified by its AppRole name or metadata
    # Example: path "secret/data/app/{{identity.entity.aliases.auth_approle_XXXXXXXX.metadata.app_name}}/*"
    # This requires entity/alias setup. A simpler approach is multiple policies or wider paths if app_name is part of the path.
    # For simplicity, assuming app_name is part of the path:
    # path "secret/data/webapp/*" { capabilities = ["read"] }
    # path "secret/data/apigateway/*" { capabilities = ["read"] }

    # Allow use of transit engine for encryption/decryption with specific keys
    path "transit/encrypt/app-data-encryption-key" {
      capabilities = ["update"]
    }
    path "transit/decrypt/app-data-encryption-key" {
      capabilities = ["update"]
    }

    # Allow fetching dynamic DB credentials for a specific role
    path "database/creds/app-readonly" {
      capabilities = ["read"]
    }
    
*   **Notes**: Specific paths like `secret/data/webapp/*` would be granted to the `webapp-role` AppRole.
*   **Relationship to Requirements**: SEC-003, DEP-003, INT-006.

#### 5.1.9 `hashicorp_vault/policies/cicd_pipeline_policy.hcl`
*   **Purpose**: Policy for CI/CD systems.
*   **Content Example**:
    hcl
    # Allow reading CI/CD specific secrets
    path "secret/data/cicd/*" {
      capabilities = ["read", "list"]
    }

    # Allow CI/CD to potentially fetch a short-lived token for deployment tasks using a specific role
    path "auth/approle/role/deployment-agent/role-id" {
      capabilities = ["read"]
    }
    path "auth/approle/role/deployment-agent/secret-id" {
      capabilities = ["create", "update"] # To generate a SecretID
    }
    
    # Allow CI/CD to read secrets needed for deployment environments
    path "secret/data/app_name/staging/*" { # Parameterize app_name or have specific policies
        capabilities = ["read"]
    }
    path "secret/data/app_name/prod/*" {
        capabilities = ["read"]
    }
    
*   **Relationship to Requirements**: DEP-003, SEC-003.

#### 5.1.10 `hashicorp_vault/policies/kms_admin_policy.hcl`
*   **Purpose**: Administrative policy for Transit secrets engine (KMS).
*   **Content Example**:
    hcl
    # Manage keys in the transit engine
    path "transit/keys/*" {
      capabilities = ["create", "read", "update", "delete", "list"]
    }
    path "transit/keys/" { # Listing keys
        capabilities = ["list"]
    }

    # Manage key configuration (rotation, etc.)
    path "transit/keys/+/config" {
      capabilities = ["update"]
    }
    
    # Perform backup/restore of keys if enabled (not recommended for exportable=false keys)
    path "transit/backup/*" {
      capabilities = ["read"] # Assuming restore is a highly privileged separate op
    }

    # Allow all cryptographic operations for administrative/testing purposes on any key
    # In production, application-specific policies should grant more limited encrypt/decrypt access to specific keys.
    path "transit/encrypt/*" { capabilities = ["update"] }
    path "transit/decrypt/*" { capabilities = ["update"] }
    path "transit/rewrap/*" { capabilities = ["update"] }
    path "transit/sign/*" { capabilities = ["update"] }     # If signing keys are used
    path "transit/verify/*" { capabilities = ["update"] }   # If signing keys are used
    path "transit/hmac/*" { capabilities = ["update"] }     # If HMAC keys are used
    
*   **Relationship to Requirements**: SEC-003.

#### 5.1.11 `hashicorp_vault/config/vault_agent_config.hcl`
*   **Purpose**: Configuration for Vault Agent instances.
*   **Key Parameters**:
    *   `pid_file`: Path to PID file, e.g., `"/var/run/vault-agent.pid"`.
    *   `exit_after_auth = false` (for daemon mode).
    *   `vault { address = "VAULT_SERVER_URL" }` (e.g., `"https://vault.creativeflow.ai:8200"`).
    *   `auto_auth { ... }`: (See section 4.2.6, defines AppRole or Kubernetes auth).
        *   Example AppRole:
            hcl
            auto_auth {
              method "approle" {
                mount_path = "auth/approle"
                config = {
                  role_id_file_path = "/etc/vault-agent/role_id" // App provides this
                  secret_id_file_path = "/etc/vault-agent/secret_id" // App provides this, or agent fetches it
                  // remove_secret_id_file_after_read = true // If SecretID is ephemeral
                }
              }
            }
            
    *   `cache { use_auto_auth_token = true }`.
    *   `listener "tcp" { ... }` (optional, if agent acts as local proxy).
    *   Multiple `template { ... }` stanzas defining source templates and destination files.
    *   Multiple `secret { ... }` stanzas for direct rendering of secrets to files.
*   **Security Considerations**: Securely provide RoleID/SecretID to the agent or configure K8s auth correctly. Ensure templates do not expose secrets with overly broad permissions.
*   **Relationship to Requirements**: DEP-003, SEC-003.

#### 5.1.12 `hashicorp_vault/config/vault_agent_template_app_db.ctmpl` (and other templates)
*   **Purpose**: Define format for secrets rendered by Vault Agent.
*   **Content (example for database credentials)**:
    ctmpl
    {{- with secret "database/creds/my-app-db-role" -}}
    DB_HOST="pgsql.creativeflow.local"
    DB_PORT="5432"
    DB_NAME="creativeflowdb"
    DB_USER="{{ .Data.username }}"
    DB_PASSWORD="{{ .Data.password }}"
    {{- end -}}
    
*   **Content (example for an API key from KVv2)**:
    ctmpl
    {{- with secret "secret/data/my-app/external-service-api" -}}
    EXTERNAL_API_KEY="{{ .Data.data.key }}"
    EXTERNAL_API_SECRET="{{ .Data.data.secret }}"
    {{- end -}}
    
*   **Notes**: Templates should be specific to application needs. File permissions on rendered files should be restrictive.
*   **Relationship to Requirements**: SEC-003, DEP-003.

### 5.2 HashiCorp Vault Deployment Scripts

#### 5.2.1 `hashicorp_vault/scripts/apply_vault_configurations.sh`
*   **Purpose**: Automate application of HCL configurations to Vault.
*   **Logic**:
    1.  Source Vault address (`VAULT_ADDR`) and token (`VAULT_TOKEN` - an initial root/admin token for setup).
    2.  Enable audit devices: `vault audit enable -path=file_audit file file_path="/var/log/vault/vault_audit.log" log_raw=false format=json` (using parameters from `audit_file.hcl`).
    3.  Enable auth methods (AppRole, Kubernetes):
        *   `vault auth enable -path=approle approle` (if not already enabled).
        *   `vault auth enable -path=kubernetes kubernetes` (if not already enabled).
        *   Apply configurations from `approle.hcl` and `kubernetes.hcl` using `vault write auth/<path>/config ...` and `vault write auth/<path>/role/<role_name> ...`.
    4.  Enable secrets engines (KVv2, Transit, Database):
        *   `vault secrets enable -path=secret -version=2 kv` (if not already enabled).
        *   `vault secrets enable -path=transit transit` (if not already enabled).
        *   `vault secrets enable -path=database database` (if not already enabled).
        *   Apply configurations from respective HCL files using `vault write <path>/config ...`, `vault write <path>/keys/...`, `vault write <path>/roles/...`.
    5.  Write policies:
        *   `vault policy write applications_base_policy policies/applications_base_policy.hcl`
        *   `vault policy write cicd_pipeline_policy policies/cicd_pipeline_policy.hcl`
        *   `vault policy write kms_admin_policy policies/kms_admin_policy.hcl`
    6.  (If PKI enabled) Enable and configure PKI engines as per section 7.
*   **Security Considerations**: The initial `VAULT_TOKEN` must be highly privileged and handled securely, ideally revoked after setup. Script should be idempotent.
*   **Relationship to Requirements**: DEP-004.1, SEC-003.

### 5.3 Ansible Vault Configurations

#### 5.3.1 `ansible_vault/group_vars/all/secrets.yml`
*   **Purpose**: Securely store encrypted variables for Ansible.
*   **Content**: This file is encrypted. Its unencrypted representation would contain key-value pairs like:
    yaml
    # Example unencrypted content before 'ansible-vault encrypt'
    # database_admin_user: vault_superuser
    # database_admin_password: "REPLACE_WITH_STRONG_GENERATED_PASSWORD"
    # external_ai_service_api_key: "REPLACE_WITH_ACTUAL_KEY"
    # vault_raft_storage_path: "/opt/vault/data" # Non-sensitive example
    
*   **Management**: Encrypted using `ansible-vault encrypt secrets.yml`. Edited using `ansible-vault edit secrets.yml`. Viewed using `ansible-vault view secrets.yml`.
*   **Security Considerations**: The Ansible Vault password used to encrypt/decrypt this file is critical.
*   **Relationship to Requirements**: DEP-004.1.

#### 5.3.2 `ansible_vault/scripts/manage_ansible_vault_password.sh`
*   **Purpose**: Guide secure handling of the Ansible Vault password.
*   **Logic/Documentation Content**:
    *   **DO NOT COMMIT THE ANSIBLE VAULT PASSWORD FILE OR THE PASSWORD ITSELF TO GIT.**
    *   **Option 1: Password File (for developers/manual runs)**
        *   Create a file (e.g., `.ansible_vault_password`) containing only the password.
        *   Add this file path to `.gitignore`.
        *   Configure Ansible to use this file by setting `vault_password_file` in `ansible.cfg` or using `--vault-password-file` CLI option.
    *   **Option 2: Environment Variable (for CI/CD)**
        *   Store the password as a secure environment variable in the CI/CD system (e.g., `ANSIBLE_VAULT_PASSWORD`).
        *   Ansible automatically picks up this environment variable.
    *   **Option 3: HashiCorp Vault Integration (Recommended for CI/CD & secure developer access)**
        *   Store the Ansible Vault password itself within HashiCorp Vault.
        *   The CI/CD pipeline (or developer script) authenticates to HashiCorp Vault (e.g., using AppRole or K8s auth).
        *   Retrieves the Ansible Vault password from HashiCorp Vault.
        *   Provides it to `ansible-playbook` command, e.g., via a temporary password file or environment variable.
        *   Example snippet:
            bash
            # export VAULT_TOKEN=$(vault login -method=approle role_id=$ROLE_ID secret_id=$SECRET_ID -format=json | jq -r .auth.client_token)
            # ansible-playbook --vault-password-file <(vault kv get -format=json secret/cicd/ansible_vault_pass | jq -r .data.data.password) my_playbook.yml
            
*   **Relationship to Requirements**: DEP-004.1.

## 6. Secret Path Strategy
A consistent naming convention for secret paths in HashiCorp Vault is crucial for organization and policy enforcement.

*   **KVv2 Secrets (`secret/data/...`)**:
    *   Applications: `secret/data/<application_name>/<environment>/<config_group_or_secret_name>`
        *   Example: `secret/data/webapp/production/database_credentials`
        *   Example: `secret/data/apigateway/common/global_settings`
    *   Third-Party Services: `secret/data/external_services/<service_name>/<account_or_key_identifier>`
        *   Example: `secret/data/external_services/openai/main_api_key` (INT-006)
        *   Example: `secret/data/external_services/stripe/production_publishable_key`
    *   CI/CD: `secret/data/cicd/<pipeline_or_environment_specific>/<secret_name>`
        *   Example: `secret/data/cicd/production_deployment/ssh_private_key`

*   **Transit Secrets Engine Keys (`transit/keys/...`)**:
    *   `transit/keys/<data_classification_or_purpose>`
        *   Example: `transit/keys/application-general-data`
        *   Example: `transit/keys/user-sensitive-data`

*   **Database Secrets Engine Roles (`database/creds/...`)**:
    *   `database/creds/<db_connection_name>-<application_or_purpose>-<access_level>`
        *   Example: `database/creds/postgresql-main-webapp-readonly`
        *   Example: `database/creds/postgresql-main-data-etl-readwrite`

*   **AppRole Auth Method Roles (`auth/approle/role/...`)**:
    *   `auth/approle/role/<application_or_service_name>-role`
        *   Example: `auth/approle/role/creativeflow-webapp-prod-role`
        *   Example: `auth/approle/role/cicd-deployer-role`

*   **Kubernetes Auth Method Roles (`auth/kubernetes/role/...`)**:
    *   `auth/kubernetes/role/<k8s_service_account_name>-<namespace>-role`
        *   Example: `auth/kubernetes/role/my-app-sa-default-role`

*   **PKI Secrets Engine Roles (if enabled)**:
    *   PKI Root: `pki_root/`
    *   PKI Intermediate: `pki_int/`
    *   Roles: `pki_int/roles/<service_or_domain_name>`
        *   Example: `pki_int/roles/internal-services` (for issuing certs for `*.internal.creativeflow.ai`)

## 7. PKI Engine Configuration (If `enable_pki_engine_root` / `enable_pki_engine_intermediate` are true)

This section describes the configuration for Vault's PKI secrets engine to manage internal CAs and issue certificates.

### 7.1 Root CA Setup (`hashicorp_vault/secrets_engines/pki_root_ca.hcl`)
*   **Purpose**: Establish a self-signed Root Certificate Authority within Vault.
*   **Key Parameters**:
    *   Enable PKI engine at `pki_root`: `vault secrets enable -path=pki_root pki`
    *   Tune max lease TTL: `vault secrets tune -max-lease-ttl=87600h pki_root` (e.g., 10 years)
    *   Generate Root CA:
        `vault write -field=certificate pki_root/root/generate/internal common_name="creativeflow.ai Root CA" ttl=87600h key_bits=4096 > root_ca.crt`
    *   Configure CRL and CA issuer URLs:
        `vault write pki_root/config/urls issuing_certificates="API_ADDR/v1/pki_root/ca" crl_distribution_points="API_ADDR/v1/pki_root/crl"`

### 7.2 Intermediate CA Setup (`hashicorp_vault/secrets_engines/pki_intermediate_ca.hcl`)
*   **Purpose**: Establish an Intermediate Certificate Authority signed by the Root CA.
*   **Key Parameters**:
    *   Enable PKI engine at `pki_int`: `vault secrets enable -path=pki_int pki`
    *   Tune max lease TTL: `vault secrets tune -max-lease-ttl=43800h pki_int` (e.g., 5 years)
    *   Generate Intermediate CSR:
        `vault write -format=json pki_int/intermediate/generate/internal common_name="creativeflow.ai Internal Services ICA" ttl=43800h key_bits=4096 | jq -r .data.csr > pki_intermediate.csr`
    *   Sign Intermediate CSR with Root CA:
        `vault write -format=json pki_root/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl=43800h | jq -r .data.certificate > signed_intermediate.pem`
    *   Set Signed Intermediate Certificate in `pki_int`:
        `vault write pki_int/intermediate/set-signed certificate=@signed_intermediate.pem`
    *   Configure CRL and CA issuer URLs for Intermediate CA:
        `vault write pki_int/config/urls issuing_certificates="API_ADDR/v1/pki_int/ca" crl_distribution_points="API_ADDR/v1/pki_int/crl"`

### 7.3 PKI Role Definitions (`hashicorp_vault/pki_roles/internal_services_role.hcl`)
*   **Purpose**: Define roles for issuing certificates from the Intermediate CA.
*   **Key Parameters (example for internal services)**:
    *   Role `internal-services`:
        `vault write pki_int/roles/internal-services allowed_domains="internal.creativeflow.ai,localhost" allow_subdomains=true allow_ip_sans=true max_ttl="720h" key_type="rsa" key_bits=2048`
*   **Policy Association**: Policies would grant specific AppRoles or K8s roles the ability to request certificates from these PKI roles (e.g., `path "pki_int/issue/internal-services" { capabilities = ["update"] }`).

## 8. Operational Procedures

### 8.1 Vault Initialization and Unsealing
*   **Initialization**: Performed once when Vault server starts for the first time against a new backend. Produces unseal keys and an initial root token.
    `vault operator init -key-shares=5 -key-threshold=3 > vault_init.txt`
*   **Unsealing**: Required every time Vault server starts or is restarted.
    `vault operator unseal <unseal_key_part_1>` (repeated for threshold number of keys)
*   **Security**: Unseal keys and root token MUST be distributed securely and stored safely by different trusted individuals. Consider Shamir's Secret Sharing for unseal keys. Root token should be used to set up initial auth methods and policies, then revoked or stored securely.
*   **Automation**: Auto-unseal can be configured using KMS (e.g., AWS KMS, Azure Key Vault, GCP KMS) or HSM for production, but this requires cloud provider integration, which is outside the self-hosted scope initially. If not using cloud KMS, manual unsealing or a secure custom unsealing script is needed.

### 8.2 Backup and Restore (Vault Data and Configuration)
*   **Configuration Backup**: All HCL configuration files and scripts (`hashicorp_vault/` and `ansible_vault/` directories) are version-controlled in Git, serving as the primary backup for configuration.
*   **Vault Data Backup (Raft Storage Backend)**:
    *   Vault's Raft storage backend is designed for HA. Data is replicated across cluster nodes.
    *   Regular snapshots of the Raft backend should be taken: `vault operator raft snapshot save backup.snap`
    *   These snapshots should be encrypted and stored securely offsite (e.g., in MinIO in a separate DR bucket or another secure backup location).
*   **Restore**:
    *   Configuration: Apply from Git using `apply_vault_configurations.sh`.
    *   Data (Raft): `vault operator raft snapshot restore backup.snap` (requires Vault to be stopped and unsealed after restore).
*   **Testing**: Backup and restore procedures must be tested regularly (at least quarterly) as part of DR drills.

### 8.3 Key Rotation
*   **Transit Keys**:
    *   Configure `rotation_period` on keys: `vault write transit/keys/<key_name>/config rotation_period=<duration>`
    *   Vault will automatically generate new key versions. Applications should be designed to use the latest key version for encryption. Decryption will work with older key versions.
    *   Manual rotation: `vault write -f transit/keys/<key_name>/rotate`
*   **API Keys (External Services stored in KVv2)**: This is a manual or semi-automated process. New keys obtained from providers must be updated in Vault. Applications need to fetch the latest version.
*   **Dynamic Database Credentials**: Automatically rotated/revoked based on their TTL.

### 8.4 Policy Management
*   Policies are defined in HCL files and version-controlled.
*   Changes are applied via `vault policy write <name> <file.hcl>` (automated by `apply_vault_configurations.sh`).
*   Regular review of policies to ensure they adhere to least privilege.

### 8.5 Audit Log Review
*   Regularly (e.g., weekly or daily for critical systems) review audit logs for suspicious activity, unauthorized access attempts, policy violations, or errors.
*   Integrate audit logs with a SIEM (Security Information and Event Management) system if available for automated analysis and alerting.
*   File-based audit logs need external log rotation and secure archival.

## 9. Deployment Strategy
*   **Vault Server Deployment**:
    *   Provision servers using Ansible (as per PMDT-011).
    *   Install Vault binary.
    *   Place `server.hcl` configuration file.
    *   Start Vault service.
    *   Initialize and unseal (see 8.1).
*   **Configuration Application**:
    *   Run `hashicorp_vault/scripts/apply_vault_configurations.sh` to:
        *   Enable audit devices.
        *   Enable and configure auth methods.
        *   Enable and configure secrets engines.
        *   Write policies.
        *   (If applicable) Setup PKI engines.
*   **CI/CD Integration**: The `apply_vault_configurations.sh` script (or Terraform equivalent) can be integrated into a CI/CD pipeline to manage Vault configuration updates in an automated and version-controlled manner.
*   **Ansible Vault**:
    *   `ansible_vault/group_vars/all/secrets.yml` is managed (encrypted/decrypted/edited) locally by developers or by CI/CD using the Ansible Vault password.
    *   The Ansible Vault password is made available to Ansible playbooks securely during execution (see 5.3.2).

## 10. Security Considerations
*   **Vault Master Key (Unseal Keys & Root Token)**: Extremely sensitive. Secure storage and distribution are paramount.
*   **Network Security**: Vault listeners should be protected by firewalls. Access to Vault UI and API should be restricted. Consider mTLS for API access.
*   **Storage Backend Security**: If using Raft, the data directory permissions must be strictly controlled.
*   **Audit Log Integrity**: Protect audit logs from tampering. Forward to a separate, secure log aggregation system.
*   **Policy Granularity**: Implement fine-grained policies based on the principle of least privilege. Avoid overly broad permissions.
*   **Regular Updates**: Keep Vault server, underlying OS, and any plugins/dependencies patched and up-to-date.
*   **Monitoring**: Monitor Vault operational metrics (e.g., via Prometheus) and audit logs for anomalies.
*   **Least Privileged Vault Token**: The token used by `apply_vault_configurations.sh` for initial setup or updates should be a short-lived admin token, ideally scoped down after initial setup if possible, or a root token that is carefully managed.
*   **Ansible Vault Password**: Treat this with the same level of care as the Vault root token/unseal keys.

This SDS provides a comprehensive design for the `CreativeFlow.SecretsManagement` repository, focusing on HashiCorp Vault and Ansible Vault to meet the platform's security and operational requirements for secrets.
markdown
# Software Design Specification: CreativeFlow.SecretsManagement

## 1. Introduction

### 1.1 Purpose
This document provides the detailed Software Design Specification (SDS) for the `CreativeFlow.SecretsManagement` repository. This system is responsible for the secure storage, management, and controlled access to all sensitive information (secrets) used by the CreativeFlow AI platform. This includes API keys, database credentials, certificates, and encryption keys. The primary technology employed will be HashiCorp Vault 1.16.2, complemented by Ansible Vault for secrets used within Ansible automation.

### 1.2 Scope
The scope of this SDS covers:
*   Configuration of the HashiCorp Vault server.
*   Setup of authentication methods (AppRole, Kubernetes).
*   Configuration of secrets engines (KVv2, Transit, Database, PKI).
*   Definition of access control policies.
*   Auditing configuration.
*   Vault Agent configuration and templates.
*   Ansible Vault setup and usage guidelines.
*   Scripts for applying configurations.
*   Operational procedures related to secrets management.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **SDS**: Software Design Specification
*   **KMS**: Key Management Service
*   **Vault**: HashiCorp Vault
*   **HCL**: HashiCorp Configuration Language
*   **KV**: Key-Value
*   **EaaS**: Encryption as a Service
*   **AppRole**: An authentication method in Vault for applications/machines.
*   **CI/CD**: Continuous Integration / Continuous Deployment
*   **IaC**: Infrastructure as Code
*   **CTMPL**: Consul Template Language
*   **PKI**: Public Key Infrastructure
*   **CA**: Certificate Authority
*   **mTLS**: Mutual Transport Layer Security
*   **SA**: Service Account (Kubernetes)
*   **TTL**: Time To Live

## 2. System Overview

The `CreativeFlow.SecretsManagement` system is a critical security component of the CreativeFlow AI platform. It leverages:

*   **HashiCorp Vault (version 1.16.2)**: A tool for securely accessing secrets. It provides a unified interface to any secret, while providing tight access control and recording a detailed audit log. It will be used for managing dynamic secrets, encryption keys, application credentials, and API keys for third-party services.
*   **Ansible Vault**: A feature of Ansible that allows encryption of sensitive data in Ansible playbooks, such as variables or files. It will be used to protect secrets consumed directly by Ansible automation scripts.

The system ensures that secrets are not hardcoded in applications, configuration files, or version control systems. It provides mechanisms for programmatic and human access to secrets based on authenticated identity and authorized policies.

## 3. Requirements Addressed

This system directly addresses the following platform requirements:

*   **SEC-003 (Cryptographic key management using KMS)**: Implemented via Vault's Transit secrets engine and potentially PKI engine for certificate management.
*   **DEP-003 (Secure handling of secrets in CI/CD)**: Implemented via Vault AppRole/Kubernetes authentication for CI/CD systems and appropriate policies.
*   **DEP-004.1 (Secrets management with Ansible Vault or HashiCorp Vault)**: Both tools are specified within this SDS for their respective use cases.
*   **INT-006 (Secure External AI Service API Key Management)**: External AI service API keys will be stored securely within Vault's KVv2 secrets engine.

## 4. Architectural Design

### 4.1 Core Principles
*   **Least Privilege**: Entities (users, applications, systems) are granted only the permissions necessary to perform their intended functions.
*   **Defense in Depth**: Multiple layers of security controls are implemented.
*   **Ephemeral Credentials**: Dynamic secrets with short TTLs are preferred over static, long-lived credentials where possible (e.g., database access).
*   **Auditability**: All access and operations within Vault are meticulously logged.
*   **Configuration as Code**: Vault and related configurations are defined in HCL and version-controlled.

### 4.2 HashiCorp Vault Architecture

#### 4.2.1 Storage Backend
Vault will be configured with an integrated storage backend, **Raft**, for high availability (HA) without external dependencies for the storage layer. This allows for a clustered Vault setup.

#### 4.2.2 Authentication Methods
*   **AppRole**: For applications and services running outside Kubernetes, and potentially for CI/CD runners. Each application/service will have a distinct RoleID and will be responsible for securely obtaining its SecretID.
*   **Kubernetes**: For applications and services running within the Kubernetes cluster. Pods will authenticate using their Kubernetes Service Account Tokens.

#### 4.2.3 Secrets Engines
*   **KV Version 2 (KVv2)**: For storing arbitrary secrets like API keys for third-party services (OpenAI, StabilityAI, Stripe, PayPal), application configuration parameters, etc. Versioning of secrets is a key feature.
*   **Transit**: For Encryption as a Service (EaaS). Manages named encryption keys for encrypting/decrypting data within applications without exposing the keys themselves. Supports key rotation.
*   **Database**: For dynamically generating database credentials (username/password) for applications accessing PostgreSQL. Vault will manage a privileged account on the database to create and revoke these ephemeral credentials.
*   **PKI (Conditional)**: If `enable_pki_engine_root` and `enable_pki_engine_intermediate` feature toggles are true, PKI engines will be configured to manage internal Certificate Authorities (Root and Intermediate) for issuing TLS certificates to internal services, enabling mTLS and securing internal communications.

#### 4.2.4 Policies and Access Control
Granular access control policies, written in HCL, will define what authenticated entities can access which paths and perform which operations within Vault. Policies will be attached to entities via their authentication method roles.

#### 4.2.5 Auditing
Audit devices will be configured to log all requests and responses to Vault. A file-based audit device is the minimum requirement, with logs securely stored and regularly reviewed.

#### 4.2.6 Vault Agent
Vault Agent will be used by applications (as a sidecar or host agent) to:
*   Automate authentication to Vault.
*   Retrieve secrets and render them into configuration files using templates (CTMPL).
*   Cache secrets to reduce load on Vault server and improve resilience.
*   Keep secrets fresh by automatically re-fetching them upon lease expiry or changes.

### 4.3 Ansible Vault Architecture

#### 4.3.1 Encrypted Variable Storage
Ansible Vault will be used to encrypt sensitive data within Ansible variable files (e.g., `group_vars/all/secrets.yml`). This protects secrets used directly by Ansible playbooks during infrastructure provisioning and configuration management.

#### 4.3.2 Vault Password Management
The Ansible Vault password itself is highly sensitive and **MUST NOT** be stored in version control. Procedures will be established for securely managing and providing this password to developers and CI/CD systems (e.g., retrieving from HashiCorp Vault, CI/CD secret variables).

## 5. Detailed Configuration Specifications

This section details the configuration for each file defined in the repository structure. All paths are relative to the repository root.

### 5.1 HashiCorp Vault Configurations

#### 5.1.1 `hashicorp_vault/config/server.hcl`
*   **Purpose**: Main server configuration for HashiCorp Vault.
*   **Key Parameters**:
    *   `listener "tcp"`:
        *   `address`: `"0.0.0.0:8200"` (Listen on all interfaces, port 8200. Adjust if needed for specific network configurations).
        *   `tls_disable`: `false` (TLS must be enabled for production).
        *   `tls_cert_file`: Path to the Vault server's TLS certificate file (e.g., `"/opt/vault/tls/vault.crt"`).
        *   `tls_key_file`: Path to the Vault server's TLS private key file (e.g., `"/opt/vault/tls/vault.key"`).
    *   `storage "raft"`:
        *   `path`: `"/opt/vault/data"` (Directory for Raft storage. Ensure this path is on persistent storage).
        *   `node_id`: (Required for each node in a Raft cluster, e.g., `"vault_node_1"`. Typically set via environment variable or script during node provisioning).
        *   If clustering, include `retry_join` blocks with other node addresses, e.g.:
            hcl
            retry_join {
              leader_api_addr = "https://<node2_api_addr>:8200"
              // ... other nodes
            }
            
    *   `api_addr`: `"https://<this_node_fqdn_or_lb_ip>:8200"` (Address clients use to reach this node or the load balancer in front of the cluster).
    *   `cluster_addr`: `"https://<this_node_internal_ip>:8201"` (Address for inter-node Raft communication).
    *   `ui`: `true` (Enables the Vault web UI).
    *   `telemetry`:
        *   `disable_hostname`: `true` (Recommended to avoid sending server hostnames in telemetry).
        *   (Optional Prometheus metrics endpoint) `prometheus_retention_time = "24h"`
    *   `disable_mlock`: `true` (Recommended to avoid issues with memory swapping, especially in virtualized environments. Ensure swap is disabled or minimized on the host).
*   **Security Considerations**: Enforce TLS with strong ciphers. Restrict file permissions on `tls_key_file` and `storage.path`.
*   **Relationship to Requirements**: SEC-003, DEP-004.1.

#### 5.1.2 `hashicorp_vault/config/audit_file.hcl`
*   **Purpose**: Configure file-based auditing for Vault.
*   **Key Parameters**:
    hcl
    audit "file_audit_log" { // Name of the audit device
      type = "file"
      options = {
        file_path = "/var/log/vault/vault_audit.log" // Ensure this directory exists and has correct permissions
        log_raw   = "false" // Set to true only for debugging specific issues, as it may log sensitive data in responses.
        hmac_accessor = "true" // HMACs accessor values for privacy.
        format    = "json"
        mode      = "0600" // Restrictive file permissions
      }
    }
    
*   **Security Considerations**: Audit logs must be protected (immutable if possible), regularly backed up, and forwarded to a central SIEM. Implement log rotation externally (e.g., `logrotate`).
*   **Relationship to Requirements**: SEC-003.

#### 5.1.3 `hashicorp_vault/auth_methods/approle.hcl`
*   **Purpose**: Declarative configuration for enabling and defining AppRole authentication method and roles (intended for use with Terraform or `apply_vault_configurations.sh` script adapting this to CLI commands).
*   **HCL Example (conceptual, to be applied via script/Terraform)**:
    hcl
    // Command to enable: vault auth enable -path=approle approle
    // config { type = "approle" } // This would be part of the enable command implicitly or an auth backend resource in TF

    // Role: webapp-prod-role
    // Command: vault write auth/approle/role/webapp-prod-role \
    //          token_policies="applications_base_policy,webapp-prod-secrets-policy" \
    //          secret_id_ttl="60m" \
    //          token_ttl="60m" \
    //          token_max_ttl="4h" \
    //          secret_id_num_uses=5 \
    //          token_num_uses=0 \ // 0 means unlimited uses for the token itself within its TTL
    //          bind_secret_id=true

    // Role: cicd-deployer-role
    // Command: vault write auth/approle/role/cicd-deployer-role \
    //          token_policies="cicd_pipeline_policy,app-deployer-policy" \
    //          secret_id_ttl="10m" \
    //          token_ttl="30m" \
    //          secret_id_num_uses=1
    
*   **Notes**: The HCL file itself might not directly map to a single `vault write config` for AppRole, but rather serves as a specification for roles that are created. The `apply_vault_configurations.sh` script will translate these intentions into `vault write auth/approle/role/...` commands.
*   **Security Considerations**: Securely distribute `RoleID` (less sensitive) and `SecretID` (highly sensitive, short-lived). Use `bind_secret_id` and IP/CIDR binding (`token_bound_cidrs`) where possible.
*   **Relationship to Requirements**: DEP-003, DEP-004.1.

#### 5.1.4 `hashicorp_vault/auth_methods/kubernetes.hcl`
*   **Purpose**: Declarative configuration for Kubernetes authentication method.
*   **HCL Example (conceptual, to be applied via script/Terraform)**:
    hcl
    // Command to enable: vault auth enable -path=kubernetes kubernetes
    //
    // Command: vault write auth/kubernetes/config \
    //          kubernetes_host="https://<K8S_API_SERVER_URL>:6443" \
    //          kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \ // Path within Vault pod
    //          token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token // Vault's SA token
    //          # Alternatively, use service_account_jwt for Vault running outside K8s if it has SA permissions.

    // Role: creativeflow-api-service-role
    // Command: vault write auth/kubernetes/role/creativeflow-api-service \
    //          bound_service_account_names="api-service-sa" \
    //          bound_service_account_namespaces="creativeflow-prod" \
    //          token_policies="applications_base_policy,api-service-secrets-policy" \
    //          ttl="1h"
    
*   **Notes**: The Kubernetes host and CA cert are critical. `token_reviewer_jwt` is the token of a service account that Vault uses to validate incoming Kubernetes service account tokens.
*   **Security Considerations**: Ensure Vault's service account for `token_reviewer_jwt` has minimal necessary permissions (typically `system:auth-delegator`). Bind roles to specific service accounts and namespaces.
*   **Relationship to Requirements**: DEP-003.

#### 5.1.5 `hashicorp_vault/secrets_engines/kv_v2_applications.hcl`
*   **Purpose**: Declarative configuration for enabling KV Version 2 secrets engine.
*   **HCL Example (conceptual, applied via script/Terraform)**:
    hcl
    // Command to enable: vault secrets enable -path=secret kv-v2
    // (Note: -version=2 is deprecated in CLI, use kv-v2 as type or use -path=secret kv options.version=2)
    // Or more commonly: vault secrets enable -path=secret kv
    // vault write secret/config max_versions=10 delete_version_after=2160h // Example: 90 days retention for deleted

    // This file primarily signifies the *intent* to use KVv2 at a standard path like 'secret/'.
    // Actual secrets are written programmatically or via UI/CLI under this path.
    // Example paths for secrets (not defined in this HCL, but stored under the engine):
    // secret/data/webapp/production/db_config
    // secret/data/ai_services/openai/api_key (for INT-006)
    
*   **Security Considerations**: Strict policies must control access to paths within this engine.
*   **Relationship to Requirements**: SEC-003, DEP-003, INT-006.

#### 5.1.6 `hashicorp_vault/secrets_engines/transit_application_keys.hcl`
*   **Purpose**: Declarative configuration for Transit secrets engine and key definitions.
*   **HCL Example (conceptual, applied via script/Terraform)**:
    hcl
    // Command to enable: vault secrets enable -path=transit transit

    // Key: app-general-encryption-key
    // Command: vault write -f transit/keys/app-general-encryption-key type=aes256-gcm96 exportable=false allow_plaintext_backup=false
    // Command: vault write transit/keys/app-general-encryption-key/config rotation_period=2592000s // 30 days

    // Key: user-auth-token-encryption-key
    // Command: vault write -f transit/keys/user-auth-token-encryption-key type=aes256-gcm96 derived=true context="<base64_encoded_context>"
    
*   **Notes**: `derived=true` allows for key derivation per context (e.g., per user ID) if convergent encryption is needed for specific tokens.
*   **Security Considerations**: Control access to `encrypt`, `decrypt`, `rewrap`, and key management operations via policies. Keys should generally be non-exportable.
*   **Relationship to Requirements**: SEC-003.

#### 5.1.7 `hashicorp_vault/secrets_engines/database_dynamic_credentials.hcl`
*   **Purpose**: Declarative configuration for Database secrets engine and roles for PostgreSQL.
*   **HCL Example (conceptual, applied via script/Terraform)**:
    hcl
    // Command to enable: vault secrets enable database

    // Connection: postgresql-creativeflow
    // Command: vault write database/config/postgresql-creativeflow \
    //          plugin_name="postgresql-database-plugin" \
    //          connection_url="postgresql://{{username}}:{{password}}@postgres.internal.creativeflow.ai:5432/creativeflow_db?sslmode=verify-full" \
    //          allowed_roles="webapp-readwrite,api-readonly" \
    //          username="vault_db_manager" \ // This user needs CREATE ROLE, GRANT, REVOKE, DROP ROLE
    //          password="<password_for_vault_db_manager_from_secure_source>" \
    //          root_rotation_statements=["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"] // For rotating vault_db_manager password

    // Role: webapp-readwrite
    // Command: vault write database/roles/webapp-readwrite \
    //          db_name="postgresql-creativeflow" \
    //          creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT webapp_rw_privs TO \"{{name}}\";" \
    //          default_ttl="1h" \
    //          max_ttl="8h" \
    //          revocation_statements="ALTER ROLE \"{{name}}\" NOLOGIN; SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = '{{name}}'; DROP ROLE IF EXISTS \"{{name}}\";"
    
*   **Notes**: `webapp_rw_privs` would be a pre-defined role in PostgreSQL with the necessary permissions.
*   **Security Considerations**: The `vault_db_manager` account password must be strong and managed securely. Creation/revocation statements must be carefully crafted to grant minimal necessary privileges and ensure cleanup.
*   **Relationship to Requirements**: SEC-003.

#### 5.1.8 `hashicorp_vault/policies/applications_base_policy.hcl`
*   **Purpose**: A foundational policy likely included by more specific application policies.
*   **Content Example**:
    hcl
    # Allow reading common configuration secrets
    path "secret/data/common/*" {
      capabilities = ["read"]
    }

    # Allow use of specific transit keys for encryption/decryption
    path "transit/encrypt/app-general-encryption-key" {
      capabilities = ["update"] // "update" is used for encrypt/decrypt operations
    }
    path "transit/decrypt/app-general-encryption-key" {
      capabilities = ["update"]
    }
    
*   **Usage**: This base policy would be combined with application-specific policies, e.g., `webapp-prod-secrets-policy` granting access to `secret/data/webapp/production/*` and `database/creds/webapp-readwrite`.
*   **Relationship to Requirements**: SEC-003, DEP-003, INT-006.

#### 5.1.9 `hashicorp_vault/policies/cicd_pipeline_policy.hcl`
*   **Purpose**: Define permissions for CI/CD systems.
*   **Content Example**:
    hcl
    # Read CI/CD specific secrets (e.g., registry credentials, deployment tokens)
    path "secret/data/cicd/*" {
      capabilities = ["read", "list"]
    }

    # If CI/CD needs to provision AppRole SecretIDs for applications during deployment
    path "auth/approle/role/webapp-prod-role/secret-id" {
      capabilities = ["create", "update"] // "update" is effectively "create a new one"
    }
    # Allow reading the RoleID
    path "auth/approle/role/webapp-prod-role/role-id" {
      capabilities = ["read"]
    }

    # Read secrets needed for application deployment configuration (environment specific)
    path "secret/data/webapp/staging/*" { capabilities = ["read"] }
    path "secret/data/webapp/production/*" { capabilities = ["read"] }
    
*   **Relationship to Requirements**: DEP-003, SEC-003.

#### 5.1.10 `hashicorp_vault/policies/kms_admin_policy.hcl`
*   **Purpose**: Administrative policy for managing the Transit secrets engine (KMS features).
*   **Content Example**:
    hcl
    # Full control over transit keys and engine configuration
    path "transit/*" {
      capabilities = ["create", "read", "update", "delete", "list", "sudo"]
    }
    
*   **Notes**: This is a highly privileged policy and should be assigned only to Vault administrators responsible for KMS.
*   **Relationship to Requirements**: SEC-003.

#### 5.1.11 `hashicorp_vault/config/vault_agent_config.hcl`
*   **Purpose**: General configuration structure for Vault Agent. Specific instances might have variations.
*   **Key Parameters**:
    hcl
    pid_file = "./pidfile" // Example, should be a proper path

    vault {
      address = "https://vault.creativeflow.ai:8200" // Should be templated or env var
      // tls_skip_verify = true // NOT FOR PRODUCTION, for dev only if self-signed certs
      // ca_cert = "/path/to/vault_ca.pem" // If using custom CA
    }

    auto_auth {
      method "approle" {
        mount_path = "auth/approle"
        config = {
          role_id_file_path     = "/etc/vault-agent/role_id"
          secret_id_file_path   = "/etc/vault-agent/secret_id"
          remove_secret_id_file_after_read = true
        }
      }
      // Example for Kubernetes auth (one method per auto_auth block)
      // method "kubernetes" {
      //   mount_path = "auth/kubernetes"
      //   config = {
      //     role = "my-app-role-for-k8s-auth"
      //     // service_account_token_file is usually auto-detected if running in K8s
      //   }
      // }
    }

    cache {
      use_auto_auth_token = true
    }

    // Example template stanza
    template {
      source      = "/etc/vault-agent/templates/db_config.ctmpl" // Path to vault_agent_template_app_db.ctmpl
      destination = "/srv/my_app/config/database.ini"
      perms       = "0640"
      command     = "systemctl reload my-app" // Optional command on change
    }
    
*   **Notes**: Multiple `template` and `secret` stanzas can be defined for different secrets. The paths for `role_id_file_path` and `secret_id_file_path` need to be populated by the application's deployment process or a bootstrap mechanism.
*   **Relationship to Requirements**: DEP-003, SEC-003.

#### 5.1.12 `hashicorp_vault/config/vault_agent_template_app_db.ctmpl`
*   **Purpose**: Template for Vault Agent to render database credentials.
*   **Content Example**:
    ctmpl
    # Database Configuration
    # Generated by Vault Agent at {{ timestamp }}
    {{ with secret "database/creds/webapp-readwrite" }}
    DB_USERNAME="{{ .Data.username }}"
    DB_PASSWORD="{{ .Data.password }}"
    DB_LEASE_DURATION="{{ .LeaseDuration }}"
    {{ end }}
    
*   **Notes**: This is just one example template. Other templates would exist for different applications or types of secrets (e.g., API keys from KVv2).
    *   For KVv2 secrets: `{{ with secret "secret/data/app/config" }}{{ .Data.data.api_key }}{{ end }}`
*   **Relationship to Requirements**: SEC-003, DEP-003.

### 5.2 HashiCorp Vault Deployment Scripts

#### 5.2.1 `hashicorp_vault/scripts/apply_vault_configurations.sh`
*   **Purpose**: Automate application of HCL-like configurations to a running Vault instance.
*   **Logic**:
    bash
    #!/bin/bash
    set -e

    # Ensure VAULT_ADDR and VAULT_TOKEN are set in the environment
    : "${VAULT_ADDR?VAULT_ADDR not set}"
    : "${VAULT_TOKEN?VAULT_TOKEN not set}"

    echo "Applying Vault Configurations..."

    # --- Audit Devices ---
    echo "Configuring file audit device..."
    # Ideally, check if already enabled. For script simplicity, this might re-apply.
    # Use parameters from hashicorp_vault/config/audit_file.hcl
    vault audit enable -path=file_audit_log file file_path="/var/log/vault/vault_audit.log" log_raw="false" format="json" mode="0600" || echo "File audit device 'file_audit_log' already enabled or failed."

    # --- Auth Methods ---
    echo "Enabling and configuring AppRole auth method..."
    vault auth list | grep -q "approle/" || vault auth enable -path=approle approle
    # Apply AppRole roles (example for webapp-prod-role, adapt from approle.hcl)
    vault write auth/approle/role/webapp-prod-role \
        token_policies="applications_base_policy,webapp-prod-secrets-policy" \
        secret_id_ttl="60m" token_ttl="60m" secret_id_num_uses=5 bind_secret_id=true || echo "Failed to write webapp-prod-role"

    echo "Enabling and configuring Kubernetes auth method..."
    vault auth list | grep -q "kubernetes/" || vault auth enable -path=kubernetes kubernetes
    # Apply Kubernetes config and roles (adapt from kubernetes.hcl)
    # vault write auth/kubernetes/config ...
    # vault write auth/kubernetes/role/creativeflow-api-service ...

    # --- Secrets Engines ---
    echo "Enabling and configuring KVv2 secrets engine at 'secret/'..."
    vault secrets list | grep -q "secret/" || vault secrets enable -path=secret kv-v2
    # vault write secret/config max_versions=10 delete_version_after=2160h # Example

    echo "Enabling and configuring Transit secrets engine at 'transit/'..."
    vault secrets list | grep -q "transit/" || vault secrets enable -path=transit transit
    # Create transit keys (adapt from transit_application_keys.hcl)
    # vault write -f transit/keys/app-general-encryption-key ...
    # vault write transit/keys/app-general-encryption-key/config rotation_period=2592000s

    echo "Enabling and configuring Database secrets engine at 'database/'..."
    vault secrets list | grep -q "database/" || vault secrets enable database
    # Configure DB connections and roles (adapt from database_dynamic_credentials.hcl)
    # vault write database/config/postgresql-creativeflow ...
    # vault write database/roles/webapp-readwrite ...

    # --- Policies ---
    echo "Writing policies..."
    vault policy write applications_base_policy hashicorp_vault/policies/applications_base_policy.hcl
    vault policy write cicd_pipeline_policy hashicorp_vault/policies/cicd_pipeline_policy.hcl
    vault policy write kms_admin_policy hashicorp_vault/policies/kms_admin_policy.hcl
    # Add other specific policies like webapp-prod-secrets-policy etc.

    # --- PKI Engines (Conditional) ---
    # if [ "$ENABLE_PKI_ENGINE_ROOT" = "true" ]; then
    #   echo "Setting up PKI Root CA..."
    #   vault secrets list | grep -q "pki_root/" || vault secrets enable -path=pki_root pki
    #   vault secrets tune -max-lease-ttl=87600h pki_root
    #   # Check if root CA already exists before generating to avoid overwriting
    #   # vault write -field=certificate pki_root/root/generate/internal common_name="creativeflow.ai Root CA" ttl=87600h > root_ca.crt
    #   # vault write pki_root/config/urls issuing_certificates="${VAULT_ADDR}/v1/pki_root/ca" crl_distribution_points="${VAULT_ADDR}/v1/pki_root/crl"
    # fi
    # if [ "$ENABLE_PKI_ENGINE_INTERMEDIATE" = "true" ]; then
    #   echo "Setting up PKI Intermediate CA..."
    #   # ... similar logic for intermediate CA, signing with root ...
    # fi

    echo "Vault configurations applied."
    
*   **Notes**: This script is illustrative. For production, using Terraform with the Vault provider is highly recommended for managing Vault configuration declaratively and idempotently. The script needs robust error checking and conditions to prevent re-applying configurations unnecessarily if they haven't changed.
*   **Relationship to Requirements**: DEP-004.1, SEC-003.

### 5.3 Ansible Vault Configurations

#### 5.3.1 `ansible_vault/group_vars/all/secrets.yml`
*   **Purpose**: Securely store encrypted global variables for Ansible playbooks.
*   **Content**: This file is encrypted by `ansible-vault`. The unencrypted content would be YAML key-value pairs. Example *unencrypted* structure:
    yaml
    # These are examples of variable names, actual values are encrypted in the file.
    # HashiCorp Vault related (if Ansible needs to interact with it, e.g., to get Ansible Vault password)
    # hc_vault_ansible_accessor_role_id: "..."
    # hc_vault_ansible_accessor_secret_id_pull_token: "..." # Token to fetch the actual SecretID

    # Database credentials for Ansible to configure applications (if not using dynamic Vault secrets for apps)
    # postgres_app_user_password: "supersecretapppassword"

    # Third-party API keys needed by Ansible for setup tasks
    # third_party_service_deploy_key: "..."

    # Internal service tokens or passwords set up by Ansible
    # odoo_initial_admin_password: "complexinitialadminpass"
    
*   **Encryption Command**: `ansible-vault encrypt ansible_vault/group_vars/all/secrets.yml`
*   **Editing Command**: `ansible-vault edit ansible_vault/group_vars/all/secrets.yml`
*   **Viewing Command**: `ansible-vault view ansible_vault/group_vars/all/secrets.yml`
*   **Security Considerations**: The security of this file relies entirely on the strength and secrecy of the Ansible Vault password.
*   **Relationship to Requirements**: DEP-004.1.

#### 5.3.2 `ansible_vault/scripts/manage_ansible_vault_password.sh`
*   **Purpose**: Provide standardized guidance and potential helper functions for managing the Ansible Vault password securely. This script itself might not store the password but rather fetch it or instruct on its use.
*   **Content (Guidance/Example Script Logic)**:
    bash
    #!/bin/bash

    # THIS SCRIPT PROVIDES GUIDANCE. THE ACTUAL VAULT PASSWORD/FILE IS NOT STORED HERE.

    echo "Ansible Vault Password Management Guidance"
    echo "-----------------------------------------"
    echo "The Ansible Vault password is required to decrypt 'secrets.yml'."
    echo "NEVER commit the password or the password file to version control."
    echo ""

    # Option 1: Using a password file (for local development)
    # Create a file, e.g., ~/.ansible_vault_pass, with the password.
    # Ensure it has restrictive permissions (chmod 600).
    # Add to .gitignore: echo ".ansible_vault_pass" >> .gitignore
    # Configure ansible.cfg:
    # [defaults]
    # vault_password_file = ~/.ansible_vault_pass
    # Or use: ansible-playbook my_playbook.yml --vault-password-file ~/.ansible_vault_pass

    # Option 2: Using an environment variable (good for CI/CD)
    # export ANSIBLE_VAULT_PASSWORD="your_strong_password"
    # Ansible will automatically use this variable. Store it securely in CI/CD secrets.

    # Option 3: Retrieving from HashiCorp Vault (Recommended for CI/CD and advanced users)
    # Requires VAULT_ADDR and VAULT_TOKEN (or other auth method) to be configured.
    # Example:
    # get_ansible_vault_password_from_hc_vault() {
    #   local secret_path="secret/data/cicd/ansible_vault_password"
    #   local password
    #   password=$(vault kv get -format=json "${secret_path}" | jq -r '.data.data.password')
    #   if [[ -z "$password" || "$password" == "null" ]]; then
    #     echo "Error: Could not retrieve Ansible Vault password from HashiCorp Vault at ${secret_path}" >&2
    #     return 1
    #   fi
    #   echo "$password"
    # }
    #
    # Usage:
    # ANSIBLE_VAULT_PASS=$(get_ansible_vault_password_from_hc_vault)
    # if [ $? -eq 0 ]; then
    #   ansible-playbook my_playbook.yml --vault-password-file <(echo "$ANSIBLE_VAULT_PASS")
    #   # Or, for Ansible versions that support it directly:
    #   # ANSIBLE_VAULT_PASSWORD_FILE=<(echo "$ANSIBLE_VAULT_PASS") ansible-playbook my_playbook.yml
    # else
    #   echo "Failed to get Ansible Vault password."
    # fi
    echo "Choose a method appropriate for your environment and security requirements."
    
*   **Security Considerations**: This script emphasizes secure practices. The choice of method depends on the context (developer machine vs. CI/CD).
*   **Relationship to Requirements**: DEP-004.1.

## 6. Secret Path Strategy in HashiCorp Vault

A clear and consistent hierarchy for secret paths is essential for organization, policy management, and auditability.

*   **KVv2 Secrets Engine (mounted at `secret/`)**:
    *   General Structure: `secret/data/<context>/<application_or_service>/<environment>/<specific_secret_group>`
    *   `<context>`: e.g., `apps`, `external_services`, `cicd`, `databases_static_creds`
    *   Examples:
        *   `secret/data/apps/webapp/production/session_key`
        *   `secret/data/apps/apigateway/common/cors_config`
        *   `secret/data/external_services/openai/api_key_main` (INT-006)
        *   `secret/data/external_services/stripe/prod_secret_key`
        *   `secret/data/cicd/global/docker_registry_password`
        *   `secret/data/databases_static_creds/odoo_db/prod_user_password` (for Odoo's own DB user, if not dynamic)

*   **Transit Secrets Engine (mounted at `transit/`)**:
    *   Keys: `transit/keys/<purpose_or_data_type_key>`
        *   Example: `transit/keys/app-sensitive-data`
        *   Example: `transit/keys/oauth-tokens`
    *   Operations: `transit/(encrypt|decrypt|rewrap)/<key_name>`

*   **Database Secrets Engine (mounted at `database/`)**:
    *   Connections: `database/config/<db_instance_name>`
        *   Example: `database/config/postgresql-primary`
    *   Roles (for dynamic credentials): `database/roles/<db_instance_name>-<app_role_purpose>`
        *   Example: `database/roles/postgresql-primary-webapp-readwrite`
    *   Credentials path: `database/creds/<role_name>` (e.g., `database/creds/postgresql-primary-webapp-readwrite`)

*   **AppRole Auth Method (mounted at `auth/approle/`)**:
    *   Roles: `auth/approle/role/<service_or_app_identifier>-<environment_or_purpose>`
        *   Example: `auth/approle/role/creativeflow-api-prod`
        *   Example: `auth/approle/role/cicd-runner-main`

*   **Kubernetes Auth Method (mounted at `auth/kubernetes/`)**:
    *   Roles: `auth/kubernetes/role/<k8s_sa_name>-<k8s_namespace_app_identifier>`
        *   Example: `auth/kubernetes/role/ai-processor-sa-ai-workloads`

*   **PKI Secrets Engine (if enabled)**:
    *   Root CA Mount: `pki_root/`
    *   Intermediate CA Mount: `pki_int/`
    *   Roles: `pki_int/roles/<purpose_or_domain_pattern>`
        *   Example: `pki_int/roles/internal-web-services` (for `*.svc.cluster.local` or `*.internal.creativeflow.ai`)

## 7. PKI Engine Configuration (Conditional)

If `enable_pki_engine_root = "true"` and `enable_pki_engine_intermediate = "true"` are set (e.g., as environment variables or configuration for the `apply_vault_configurations.sh` script), the following configurations will be applied.

### 7.1 Root CA Setup (`hashicorp_vault/secrets_engines/pki_root_ca.hcl` - conceptual for script)
*   **Purpose**: Establish a self-signed Root CA. This CA should be long-lived and its private key material is highly sensitive.
*   **Script Actions (`apply_vault_configurations.sh` adaptation)**:
    1.  `vault secrets list | grep -q "^pki_root/" || vault secrets enable -path=pki_root pki`
    2.  `vault secrets tune -max-lease-ttl=87600h pki_root` (10 years)
    3.  Check if Root CA exists: `vault read pki_root/ca/pem > /dev/null 2>&1`
    4.  If not exists, generate Root CA:
        `vault write -field=certificate pki_root/root/generate/internal common_name="CreativeFlow AI Root CA" ttl=87600h key_type=rsa key_bits=4096 exclude_cn_from_sans=true > /opt/vault/pki/root_ca.crt`
        (Store `root_ca.crt` securely for distribution to clients needing to trust certs issued by this PKI)
    5.  `vault write pki_root/config/urls issuing_certificates="${VAULT_ADDR}/v1/pki_root/ca" crl_distribution_points="${VAULT_ADDR}/v1/pki_root/crl"`

### 7.2 Intermediate CA Setup (`hashicorp_vault/secrets_engines/pki_intermediate_ca.hcl` - conceptual for script)
*   **Purpose**: Establish an Intermediate CA, signed by the internal Root CA, for issuing end-entity certificates.
*   **Script Actions (`apply_vault_configurations.sh` adaptation)**:
    1.  `vault secrets list | grep -q "^pki_int/" || vault secrets enable -path=pki_int pki`
    2.  `vault secrets tune -max-lease-ttl=43800h pki_int` (5 years)
    3.  Generate Intermediate CSR (if not already set up):
        `CSR_RESPONSE=$(vault write -format=json pki_int/intermediate/generate/internal common_name="CreativeFlow AI Internal Services ICA" ttl=43800h key_type=rsa key_bits=4096 exclude_cn_from_sans=true)`
        `INTERMEDIATE_CSR=$(echo "$CSR_RESPONSE" | jq -r .data.csr)`
        `echo "$INTERMEDIATE_CSR" > /opt/vault/pki/intermediate_ca.csr`
    4.  Sign Intermediate CSR with Root CA:
        `SIGNED_CERT_RESPONSE=$(vault write -format=json pki_root/root/sign-intermediate csr=@/opt/vault/pki/intermediate_ca.csr format=pem_bundle ttl=43800h)`
        `SIGNED_INTERMEDIATE_CERT=$(echo "$SIGNED_CERT_RESPONSE" | jq -r .data.certificate)`
        `echo "$SIGNED_INTERMEDIATE_CERT" > /opt/vault/pki/signed_intermediate_ca.pem`
    5.  Set Signed Intermediate Certificate:
        `vault write pki_int/intermediate/set-signed certificate=@/opt/vault/pki/signed_intermediate_ca.pem`
    6.  `vault write pki_int/config/urls issuing_certificates="${VAULT_ADDR}/v1/pki_int/ca" crl_distribution_points="${VAULT_ADDR}/v1/pki_int/crl"`

### 7.3 PKI Role Definitions (`hashicorp_vault/pki_roles/example_service_role.hcl` - conceptual for script)
*   **Purpose**: Define roles for issuing certificates for specific services or use cases.
*   **Script Actions (Example for `internal-services` role)**:
    `vault write pki_int/roles/internal-services allowed_domains="internal.creativeflow.ai,svc.cluster.local" allow_subdomains=true allow_ip_sans=true max_ttl="2160h" key_type="rsa" key_bits=2048 generate_lease=true` (720h for cert TTL, 2160h for lease of cert itself)
*   **Policies**: Corresponding policies will grant access to `pki_int/issue/<role_name>` for authorized entities.

## 8. Operational Procedures

### 8.1 Vault Initialization and Unsealing
*   **Initialization**:
    *   Executed once via `vault operator init -key-shares=5 -key-threshold=3`.
    *   The 5 unseal keys and 1 initial root token must be securely distributed among at least 3 different key custodians.
    *   The initial root token is used for the very first setup (running `apply_vault_configurations.sh` or Terraform) and then should be revoked or stored in a highly secure manner (e.g., physical safe), with day-to-day administration done via less privileged tokens/auth methods.
*   **Unsealing**:
    *   Required after every Vault server restart.
    *   `vault operator unseal <unseal_key_fragment>` - repeated 3 times with different key fragments.
    *   Consider auto-unseal mechanisms for production using a dedicated KMS (e.g., another Vault instance acting as KMS, or cloud KMS if hybrid model is adopted later) if manual unsealing is operationally burdensome, but this adds complexity. For a self-hosted only setup, manual or carefully scripted unsealing with key fragments stored securely is typical.

### 8.2 Backup and Restore
*   **Configuration**: All `.hcl` and script files are version-controlled in Git. This is the primary backup for *configuration*.
*   **Vault Data (Raft storage)**:
    *   `vault operator raft snapshot save <snapshot_file_path>` - Perform daily.
    *   Encrypt the snapshot: `gpg -c <snapshot_file_path>`
    *   Store encrypted snapshot securely offsite (e.g., different server, DR MinIO bucket).
*   **Restore**:
    1.  Restore Vault server configuration from Git using Ansible if needed.
    2.  Stop Vault service.
    3.  Decrypt snapshot: `gpg -d <encrypted_snapshot_file_path.gpg> > <snapshot_file_path>`
    4.  Restore data: `vault operator raft snapshot restore -force <snapshot_file_path>` (Requires Vault to be unsealed *after* this command if it was sealed).
    5.  Start Vault service and unseal.
*   **Testing**: Perform restore drills quarterly to a non-production environment.

### 8.3 Key Rotation
*   **Transit Keys**: Leverage Vault's built-in rotation (`rotation_period` in key config or manual `vault write -f transit/keys/<key_name>/rotate`). Applications should always request encryption with the latest key version. Vault handles decryption with older versions.
*   **KV Secrets (e.g., External API Keys)**: Manual process. Obtain new key from provider, update secret in Vault (creating a new version). Applications using Vault Agent with templates will pick up the new version upon next lease renewal or agent restart.
*   **Database Dynamic Credentials**: Handled automatically by Vault based on TTLs.
*   **AppRole SecretIDs**: Short-lived and single-use (or few uses) by design. Applications/CI must re-fetch new SecretIDs.
*   **Vault's Own TLS Certificates**: Rotate manually or via an automated certificate management solution before expiry.
*   **PKI Certificates**: End-entity certificates issued by Vault PKI will have their own TTLs. The Intermediate CA cert needs rotation before expiry (generate new CSR, sign by Root, update in Vault). Root CA is long-lived.

### 8.4 Policy Management
*   Policies are defined in HCL files within `hashicorp_vault/policies/`.
*   All policy changes must be version-controlled in Git.
*   Apply changes using `vault policy write <policy_name> <policy_file.hcl>` (can be part of `apply_vault_configurations.sh` or a separate CI/CD job for policy updates).
*   Regularly audit policies for adherence to least privilege.

### 8.5 Audit Log Review
*   Configure external log shipping for `vault_audit.log` to a SIEM or centralized logging system (e.g., ELK/Loki).
*   Implement automated alerts in the SIEM for suspicious audit log events (e.g., numerous authentication failures, policy denials, root token usage).
*   Perform manual periodic reviews of audit logs.

## 9. Security Considerations
*   **Unseal Keys & Root Token Security**: Critical. Use split-knowledge/M-of-N schemes. Store offline in secure locations.
*   **Network Isolation**: Restrict network access to Vault API and UI to trusted networks/hosts using firewalls.
*   **TLS Everywhere**: Ensure all Vault communication (client-server, server-server in cluster) uses TLS.
*   **Least Privilege Principle**: Applied rigorously for all policies and auth method roles.
*   **Regular Updates**: Keep Vault and its underlying OS patched.
*   **Break-Glass Procedures**: Document procedures for emergency access if primary admin methods fail (leveraging root token/unseal keys).
*   **Physical Security**: For self-hosted servers, ensure adequate physical security of the data center.
*   **Ansible Vault Password Security**: Manage with utmost care, ideally fetched from HashiCorp Vault by CI/CD or secured locally by developers.
*   **Vault Agent Security**: Secure the agent's token acquisition method (e.g., RoleID/SecretID files, K8s SA token). Ensure rendered secret files have restrictive permissions.
