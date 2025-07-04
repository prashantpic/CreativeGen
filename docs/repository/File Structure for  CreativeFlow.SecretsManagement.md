# Specification

# 1. Files

- **Path:** hashicorp_vault/config/server.hcl  
**Description:** Main server configuration file for HashiCorp Vault. Defines listener parameters, storage backend, telemetry, UI settings, and HA configuration if applicable. This file is critical for initializing and running the Vault server.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 0  
**Name:** server  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/config/server.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Server Core Setup
    - Listener Configuration
    - Storage Backend Definition
    - Telemetry Configuration
    - UI Enablement
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-004.1
    
**Purpose:** To define the core operational parameters for the HashiCorp Vault server.  
**Logic Description:** Specifies TCP listener addresses and TLS settings. Configures the storage backend (e.g., Raft, Consul, Filesystem - Raft preferred for HA). Sets options for telemetry data collection. Enables or disables the Vault UI. Defines HA parameters if applicable (e.g., api_addr, cluster_addr).  
**Documentation:**
    
    - **Summary:** This HCL file contains the primary configuration settings for the HashiCorp Vault server instance(s). It is loaded by Vault at startup to determine how it operates.
    
**Namespace:** hashicorp.vault.config  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/config/audit_file.hcl  
**Description:** Configures an audit device for HashiCorp Vault, typically a file-based audit log. This ensures all requests to Vault and responses from Vault are logged for security and compliance.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** audit_file  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/config/audit_file.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Auditing
    - File-based Audit Log Setup
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-004.1
    
**Purpose:** To enable and configure auditing for all operations within HashiCorp Vault.  
**Logic Description:** Enables an audit device of type 'file'. Specifies the file_path for the audit log. Configures log rotation, permissions, and formatting options (e.g., json). Ensures sensitive information is not inadvertently logged or appropriately handled if it must be.  
**Documentation:**
    
    - **Summary:** This HCL file configures a file audit device for Vault, ensuring all interactions are logged for security and compliance monitoring.
    
**Namespace:** hashicorp.vault.audit  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/policies/applications_base_policy.hcl  
**Description:** Defines a base access control policy for applications accessing secrets stored in HashiCorp Vault. Grants read access to common application secrets paths.  
**Template:** HCL Vault Policy  
**Dependency Level:** 2  
**Name:** applications_base_policy  
**Type:** Policy  
**Relative Path:** hashicorp_vault/policies/applications_base_policy.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - PolicyAsCode
    - LeastPrivilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Secret Access Control
    - Read-only access to KV secrets
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-003
    - INT-006
    
**Purpose:** To provide applications with necessary read-only permissions to their specific secrets.  
**Logic Description:** Defines path-based permissions. For example, path "secret/data/app_name/*" { capabilities = ["read"] }. This policy will be associated with AppRoles or other auth methods used by applications.  
**Documentation:**
    
    - **Summary:** This HCL policy file grants applications read-only access to their designated secrets paths in the KVv2 secrets engine.
    
**Namespace:** hashicorp.vault.policy  
**Metadata:**
    
    - **Category:** SecurityPolicy
    
- **Path:** hashicorp_vault/policies/cicd_pipeline_policy.hcl  
**Description:** Defines access control policy for CI/CD pipelines interacting with HashiCorp Vault. Grants permissions to read CI/CD specific secrets and potentially manage AppRole RoleIDs/SecretIDs or other auth entities for deploying applications.  
**Template:** HCL Vault Policy  
**Dependency Level:** 2  
**Name:** cicd_pipeline_policy  
**Type:** Policy  
**Relative Path:** hashicorp_vault/policies/cicd_pipeline_policy.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - PolicyAsCode
    - LeastPrivilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - CI/CD Secret Access Control
    - CI/CD Operational Permissions
    
**Requirement Ids:**
    
    - DEP-003
    - SEC-003
    
**Purpose:** To grant CI/CD pipelines necessary permissions for secure secret handling and deployment tasks.  
**Logic Description:** Defines path-based permissions. For example, path "secret/data/cicd/*" { capabilities = ["read"] }. May also include permissions to manage specific auth method roles if CI/CD is responsible for provisioning application credentials, e.g., path "auth/approle/role/app_name/role-id" { capabilities = ["read"] } and path "auth/approle/role/app_name/secret-id" { capabilities = ["create", "update"] }.  
**Documentation:**
    
    - **Summary:** This HCL policy file grants CI/CD pipelines permissions to access necessary secrets and potentially manage auth credentials for applications.
    
**Namespace:** hashicorp.vault.policy  
**Metadata:**
    
    - **Category:** SecurityPolicy
    
- **Path:** hashicorp_vault/policies/kms_admin_policy.hcl  
**Description:** Defines administrative access control policy for managing Key Management Service (KMS) functionalities within Vault, such as the Transit secrets engine.  
**Template:** HCL Vault Policy  
**Dependency Level:** 2  
**Name:** kms_admin_policy  
**Type:** Policy  
**Relative Path:** hashicorp_vault/policies/kms_admin_policy.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - PolicyAsCode
    - LeastPrivilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KMS Administration Access Control
    
**Requirement Ids:**
    
    - SEC-003
    
**Purpose:** To grant authorized administrators permissions to manage encryption keys and KMS operations.  
**Logic Description:** Defines path-based permissions for managing the transit secrets engine. For example, path "transit/keys/*" { capabilities = ["create", "read", "update", "delete", "list"] }, path "transit/encrypt/app_key" { capabilities = ["update"] }, path "transit/decrypt/app_key" { capabilities = ["update"] }.  
**Documentation:**
    
    - **Summary:** This HCL policy file grants administrative privileges for managing keys and operations within the Transit secrets engine, effectively controlling KMS functions.
    
**Namespace:** hashicorp.vault.policy  
**Metadata:**
    
    - **Category:** SecurityPolicy
    
- **Path:** hashicorp_vault/auth_methods/approle.hcl  
**Description:** Configures the AppRole authentication method in HashiCorp Vault. This method allows machines or applications to authenticate with Vault using a RoleID and SecretID.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** approle_auth  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/auth_methods/approle.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AppRole Authentication Setup
    - Role Definitions for Applications
    - Role Definitions for CI/CD
    
**Requirement Ids:**
    
    - DEP-003
    - DEP-004.1
    
**Purpose:** To enable and configure AppRole authentication for programmatic access to Vault by applications and CI/CD pipelines.  
**Logic Description:** Enables the AppRole auth method at a specific path (e.g., `auth/approle`). Defines various roles, such as 'application-role' or 'cicd-role', specifying token policies, secret ID TTLs, token TTLs, and other constraints for each role.  
**Documentation:**
    
    - **Summary:** This HCL file configures the AppRole authentication method, including defining roles that applications and CI/CD systems will use to authenticate with Vault.
    
**Namespace:** hashicorp.vault.auth.approle  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/auth_methods/kubernetes.hcl  
**Description:** Configures the Kubernetes authentication method in HashiCorp Vault. This allows applications running within a Kubernetes cluster to authenticate with Vault using their Kubernetes Service Account Token.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** kubernetes_auth  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/auth_methods/kubernetes.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Kubernetes Authentication Setup
    - Role Definitions for Kubernetes Service Accounts
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To enable and configure Kubernetes authentication for services running within Kubernetes to securely access Vault secrets.  
**Logic Description:** Enables the Kubernetes auth method. Configures it with Kubernetes host, CA certificate, and service account JWT. Defines roles mapping Kubernetes service accounts in specific namespaces to Vault policies and TTLs.  
**Documentation:**
    
    - **Summary:** This HCL file configures the Kubernetes authentication method, allowing pods to authenticate to Vault using their service account tokens.
    
**Namespace:** hashicorp.vault.auth.kubernetes  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/secrets_engines/kv_v2_applications.hcl  
**Description:** Configures a Key/Value Version 2 (KV-V2) secrets engine in HashiCorp Vault for storing application-specific secrets, such as API keys, database credentials, and configuration parameters.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** kv_v2_applications  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/secrets_engines/kv_v2_applications.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Secrets Storage
    - KV Version 2 Engine Setup
    - External AI Service API Key Storage
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-003
    - INT-006
    
**Purpose:** To enable and configure a secure, versioned key-value store for application secrets.  
**Logic Description:** Enables the KV secrets engine at a specific path (e.g., `secret/`). Configures options like `max_versions` to keep a history of secret versions. This engine will store secrets for various applications, including external AI service API keys required by INT-006.  
**Documentation:**
    
    - **Summary:** This HCL file sets up a KV version 2 secrets engine, typically mounted at 'secret/', for storing versioned application secrets.
    
**Namespace:** hashicorp.vault.secrets.kv  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/secrets_engines/transit_application_keys.hcl  
**Description:** Configures the Transit secrets engine in HashiCorp Vault to provide encryption as a service (EaaS) for applications. Manages named encryption keys for encrypting/decrypting application data without exposing the keys themselves.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** transit_application_keys  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/secrets_engines/transit_application_keys.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - Cryptography
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Encryption as a Service
    - Named Encryption Key Management
    - Key Rotation Policy Definition
    
**Requirement Ids:**
    
    - SEC-003
    
**Purpose:** To enable cryptographic operations (encryption, decryption, key versioning, rotation) for applications using centrally managed keys.  
**Logic Description:** Enables the transit secrets engine at a specific path (e.g., `transit/`). Creates named encryption keys (e.g., 'app-data-key', 'pii-key') with configurable types (e.g., aes256-gcm96), convergent encryption settings, and key rotation policies (e.g., `rotation_period`).  
**Documentation:**
    
    - **Summary:** This HCL file configures the Transit secrets engine for managing cryptographic keys and performing encryption/decryption operations for applications.
    
**Namespace:** hashicorp.vault.secrets.transit  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/secrets_engines/database_dynamic_credentials.hcl  
**Description:** Configures the Database secrets engine in HashiCorp Vault to dynamically generate database credentials for applications. This enhances security by providing short-lived, on-demand credentials.  
**Template:** HCL Vault Configuration  
**Dependency Level:** 1  
**Name:** database_dynamic_credentials  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/secrets_engines/database_dynamic_credentials.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - DynamicSecrets
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dynamic Database Credential Generation
    - Database Secrets Engine Setup for PostgreSQL
    
**Requirement Ids:**
    
    - SEC-003
    
**Purpose:** To enable secure, dynamic generation of database credentials for applications, reducing the risk associated with static credentials.  
**Logic Description:** Enables the database secrets engine. Configures connection details to a PostgreSQL database (connection_url, username, password for Vault's management user). Defines roles that map to specific database users/permissions and specify SQL statements for creating/revoking credentials and setting TTLs for generated credentials.  
**Documentation:**
    
    - **Summary:** This HCL file configures the Database secrets engine to manage and dynamically generate credentials for PostgreSQL databases.
    
**Namespace:** hashicorp.vault.secrets.database  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/scripts/apply_vault_configurations.sh  
**Description:** Shell script to apply HashiCorp Vault configurations (policies, auth methods, secrets engines) to a running Vault instance using the Vault CLI. This script automates the setup or update of Vault's configuration from the HCL files.  
**Template:** Shell Script  
**Dependency Level:** 3  
**Name:** apply_vault_configurations  
**Type:** Script  
**Relative Path:** hashicorp_vault/scripts/apply_vault_configurations.sh  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - InfrastructureAsCodeOrchestration
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Configuration Automation
    - Policy Application
    - Auth Method Enablement
    - Secrets Engine Enablement
    
**Requirement Ids:**
    
    - DEP-004.1
    - SEC-003
    
**Purpose:** To automate the application of HCL-defined configurations to HashiCorp Vault.  
**Logic Description:** Sets VAULT_ADDR and VAULT_TOKEN environment variables. Uses 'vault policy write' for each policy file. Uses 'vault auth enable' and 'vault write auth/.../config' for auth methods. Uses 'vault secrets enable' and 'vault write .../config' for secrets engines. Includes error handling and idempotency checks where possible. This could also be a Terraform main.tf file if Terraform is chosen for provisioning Vault resources.  
**Documentation:**
    
    - **Summary:** This script orchestrates the application of various HCL configuration files to initialize or update a HashiCorp Vault server.
    
**Namespace:** scripts.vault  
**Metadata:**
    
    - **Category:** DeploymentScript
    
- **Path:** ansible_vault/group_vars/all/secrets.yml  
**Description:** Ansible Vault encrypted YAML file containing secrets applicable to all hosts in the Ansible inventory. Used to store sensitive variables like API keys, passwords, or certificates that Ansible playbooks will use.  
**Template:** YAML Ansible Vault  
**Dependency Level:** 0  
**Name:** secrets  
**Type:** Configuration  
**Relative Path:** ansible_vault/group_vars/all/secrets.yml  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - EncryptedSecrets
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Ansible Encrypted Variable Storage
    - Centralized Secret Management for Ansible
    
**Requirement Ids:**
    
    - DEP-004.1
    
**Purpose:** To securely store variables used by Ansible playbooks, encrypted using Ansible Vault.  
**Logic Description:** This file would contain key-value pairs. For example: 'db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          36633934336261323230383033613631623130363235656439633932323334653734633134623232
          3932656533656431316335363832303930643561323930620a323265396531353861363030306233
          30613130343661393632393631623032633265336366303663623334363539396533303135303939
          34333732373439326539300a65303462323639323862333462633163356633306638616466336536
          3230396138'. The actual content is encrypted.  
**Documentation:**
    
    - **Summary:** Stores sensitive variables encrypted with Ansible Vault, accessible by Ansible during playbook execution.
    
**Namespace:** ansible.vars.vault  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** ansible_vault/scripts/manage_ansible_vault_password.sh  
**Description:** A helper script or documentation outlining the procedure for managing the Ansible Vault password file. The password file itself should NOT be committed to version control. This script might retrieve it from a secure location like HashiCorp Vault or a password manager.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** manage_ansible_vault_password  
**Type:** Script  
**Relative Path:** ansible_vault/scripts/manage_ansible_vault_password.sh  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - SecurePasswordManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Ansible Vault Password File Handling Guidance
    
**Requirement Ids:**
    
    - DEP-004.1
    
**Purpose:** To provide a secure and standardized way for developers and CI/CD systems to access the Ansible Vault password.  
**Logic Description:** The script could: 1. Prompt for the password. 2. Retrieve the password from HashiCorp Vault using 'vault kv get'. 3. Retrieve from an environment variable set securely by CI/CD. 4. Explain how to create/use a password file specified in ansible.cfg. Emphasizes NOT storing the raw password file in Git.  
**Documentation:**
    
    - **Summary:** This script (or accompanying documentation) details the secure process for obtaining and using the Ansible Vault password, potentially integrating with HashiCorp Vault for password storage.
    
**Namespace:** scripts.ansible  
**Metadata:**
    
    - **Category:** UtilityScript
    
- **Path:** hashicorp_vault/config/vault_agent_template_app_db.ctmpl  
**Description:** Vault Agent template file for rendering database credentials for an application. Vault Agent uses this template to fetch secrets from Vault and write them to a file in a format the application can consume.  
**Template:** Consul Template Language (CTMPL)  
**Dependency Level:** 2  
**Name:** vault_agent_template_app_db  
**Type:** ConfigurationTemplate  
**Relative Path:** hashicorp_vault/config/vault_agent_template_app_db.ctmpl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - SidecarPattern
    - DynamicSecrets
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dynamic Database Credential Rendering
    - Vault Agent Secret Templating
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-003
    
**Purpose:** To define how dynamic database credentials fetched by Vault Agent should be formatted for application consumption.  
**Logic Description:** Uses Consul Template markup. Example: '{{ with secret "database/creds/app-role" }}DB_USERNAME="{{ .Data.username }}"
DB_PASSWORD="{{ .Data.password }}"{{ end }}'. This template would be used by Vault Agent running as a sidecar or on the same host as the application.  
**Documentation:**
    
    - **Summary:** A CTMPL template used by Vault Agent to retrieve dynamic database credentials from Vault and render them into a configuration file for an application.
    
**Namespace:** hashicorp.vault.agent.template  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** hashicorp_vault/config/vault_agent_config.hcl  
**Description:** Configuration file for HashiCorp Vault Agent. Defines Vault server address, authentication method (e.g., AppRole, K8s), and secret/template stanzas for retrieving and rendering secrets.  
**Template:** HCL Vault Agent Configuration  
**Dependency Level:** 1  
**Name:** vault_agent_config  
**Type:** Configuration  
**Relative Path:** hashicorp_vault/config/vault_agent_config.hcl  
**Repository Id:** REPO-SECRETS-MANAGEMENT-001  
**Pattern Ids:**
    
    - SidecarPattern
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Agent Setup
    - Secret Caching Configuration
    - Auto-Auth Configuration
    
**Requirement Ids:**
    
    - DEP-003
    - SEC-003
    
**Purpose:** To configure Vault Agent instances that applications or CI/CD jobs might use to interact with Vault.  
**Logic Description:** Specifies 'pid_file', 'vault { address = "..." }'. Defines 'auto_auth' method (e.g., 'approle' with role_id_file_path and secret_id_file_path, or 'kubernetes' role). Includes 'cache' settings. Defines 'template' stanzas linking CTMPL files (like vault_agent_template_app_db.ctmpl) to destination files and commands to run on render. Defines 'secret' stanzas for direct secret writing to files.  
**Documentation:**
    
    - **Summary:** This HCL file configures Vault Agent, enabling applications to easily and securely retrieve secrets from HashiCorp Vault without direct API interaction.
    
**Namespace:** hashicorp.vault.agent.config  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_pki_engine_root
  - enable_pki_engine_intermediate
  - enable_dynamic_db_credentials_postgres
  - enable_approle_auth
  - enable_kubernetes_auth
  - enable_ansible_vault_integration_examples
  
- **Database Configs:**
  
  


---

