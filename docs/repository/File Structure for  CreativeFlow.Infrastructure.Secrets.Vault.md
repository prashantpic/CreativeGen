# Specification

# 1. Files

- **Path:** config/vault_server.hcl  
**Description:** Core server configuration file for a HashiCorp Vault instance. This file defines the storage backend, HA listener, telemetry settings, and other fundamental server parameters. It is intended to be deployed and managed by a configuration management tool like Ansible.  
**Template:** HCL Configuration Template  
**Dependency Level:** 0  
**Name:** vault_server  
**Type:** Configuration  
**Relative Path:** config/vault_server  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Server HA Configuration
    - Vault Storage Backend Configuration
    - Vault Telemetry Configuration
    
**Requirement Ids:**
    
    - SEC-003
    
**Purpose:** To define the static, low-level configuration of the Vault server process itself, establishing how it stores data and communicates in a high-availability cluster.  
**Logic Description:** This HCL file will contain stanzas for 'storage' (e.g., 'raft' for Integrated Storage), 'listener' (defining the network address and TLS settings), 'ha_storage' (for HA coordination), 'telemetry' (for Prometheus metrics), and 'ui' (enabling the web UI). Values should be parameterized to be supplied by a configuration management tool for different environments.  
**Documentation:**
    
    - **Summary:** Defines the core operational parameters for a Vault server instance, including storage backend (Raft), high-availability settings, and network listeners. This file is the foundational configuration for starting the Vault service.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets  
**Metadata:**
    
    - **Category:** InfrastructureConfiguration
    
- **Path:** policies/admin_policy.hcl  
**Description:** Defines the super-administrator policy for Vault. Grants wide-ranging permissions to manage all aspects of the Vault cluster, including policies, auth methods, secret engines, and system settings. Access to this policy should be highly restricted.  
**Template:** HCL Policy Template  
**Dependency Level:** 1  
**Name:** admin_policy  
**Type:** Policy  
**Relative Path:** policies/admin_policy  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Role-Based Access Control
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Administrator Access Control
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-004.1
    
**Purpose:** To establish the root-level administrative access control policy required for operators to manage the Vault installation.  
**Logic Description:** This policy will grant 'sudo' capabilities on most paths. It will use HCL syntax to define path-based permissions. For example, 'path "sys/*" { capabilities = ["create", "read", "update", "delete", "list", "sudo"] }' and similar entries for 'auth/*' and secret paths will be included. This policy is applied via Terraform and assigned to an admin group or auth method role.  
**Documentation:**
    
    - **Summary:** HCL file containing the Vault ACL policy for administrative users. This policy grants permissions to configure all aspects of Vault, including auth methods, secret engines, and other policies.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Policies  
**Metadata:**
    
    - **Category:** AccessControl
    
- **Path:** policies/ci_cd_policy.hcl  
**Description:** Defines the access control policy for CI/CD pipelines (e.g., GitLab/GitHub Actions). Grants limited, specific permissions needed to read application secrets during deployment and potentially manage environment-specific secrets.  
**Template:** HCL Policy Template  
**Dependency Level:** 1  
**Name:** ci_cd_policy  
**Type:** Policy  
**Relative Path:** policies/ci_cd_policy  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Role-Based Access Control
    - Least Privilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - CI/CD Pipeline Access Control
    
**Requirement Ids:**
    
    - DEP-003
    - DEP-004.1
    
**Purpose:** To provide CI/CD pipelines with the minimum necessary permissions to retrieve secrets required for application deployment, without exposing sensitive data.  
**Logic Description:** This policy grants read-only access to specific paths within the KV secrets engine, structured by application and environment. For example, 'path "secret/data/apps/creativeflow-webapp/staging" { capabilities = ["read"] }'. It explicitly denies access to administrative paths. This policy is attached to a role in the JWT/OIDC auth method used by the CI/CD runners.  
**Documentation:**
    
    - **Summary:** Defines the Vault ACL policy for CI/CD runners. It grants read-only access to application secrets based on environment, enforcing the principle of least privilege for automated deployment processes.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Policies  
**Metadata:**
    
    - **Category:** AccessControl
    
- **Path:** policies/app_services_policy.hcl  
**Description:** A generic template for an application service policy. This would be parameterized or duplicated for each microservice, granting access to its specific secrets (e.g., database credentials) and any shared secrets it requires.  
**Template:** HCL Policy Template  
**Dependency Level:** 1  
**Name:** app_services_policy  
**Type:** Policy  
**Relative Path:** policies/app_services_policy  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Role-Based Access Control
    - Least Privilege
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Application Service Access Control
    
**Requirement Ids:**
    
    - INT-006
    - SEC-003
    
**Purpose:** To define a template for access control policies for backend applications, allowing them to securely fetch their required secrets at runtime.  
**Logic Description:** This policy grants read access to a service-specific path in the KV store, like 'path "secret/data/apps/user-management-service/production" { capabilities = ["read"] }'. It may also grant permissions to use the transit secrets engine for data encryption/decryption, e.g., 'path "transit/encrypt/app-data" { capabilities = ["update"] }'. This policy is attached to an AppRole specific to each service.  
**Documentation:**
    
    - **Summary:** Defines a template Vault ACL policy for application microservices. It provides read-only access to service-specific secrets (e.g., database credentials, third-party API keys) and potentially access to cryptographic functions.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Policies  
**Metadata:**
    
    - **Category:** AccessControl
    
- **Path:** scripts/bootstrap_vault.sh  
**Description:** A shell script to perform the initial setup of a new Vault cluster. This includes initializing Vault, capturing the unseal keys and root token, and storing them securely (e.g., in a password manager or separate secure location for operators).  
**Template:** Shell Script  
**Dependency Level:** 0  
**Name:** bootstrap_vault  
**Type:** Script  
**Relative Path:** scripts/bootstrap_vault  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Initialization
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-004.1
    
**Purpose:** To automate the sensitive and critical first-time initialization process of a Vault server, ensuring initial keys are properly handled.  
**Logic Description:** The script will check if Vault is already initialized. If not, it will run 'vault operator init' and parse the output to capture the unseal keys and initial root token. It will then prompt the operator to store these credentials in a pre-determined secure location. This script is for one-time use per cluster and requires high privileges.  
**Documentation:**
    
    - **Summary:** Automates the 'vault operator init' process for a new Vault cluster. It captures the unseal keys and root token, providing instructions for their secure storage. This script is a critical part of the initial deployment.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Operations
    
- **Path:** scripts/unseal_vault.sh  
**Description:** A shell script to unseal a Vault server instance. It reads the required number of unseal keys from a secure input (e.g., environment variables, file) and applies them to the Vault operator unseal endpoint.  
**Template:** Shell Script  
**Dependency Level:** 0  
**Name:** unseal_vault  
**Type:** Script  
**Relative Path:** scripts/unseal_vault  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Vault Unsealing Automation
    
**Requirement Ids:**
    
    - SEC-003
    
**Purpose:** To automate the process of unsealing Vault after a restart or planned sealing, which is a common operational task.  
**Logic Description:** This script will loop a required number of times (e.g., 3 out of 5), prompting an operator for each unseal key or reading them from pre-configured secure environment variables. For each key, it will execute 'vault operator unseal <key>'. The script will check the seal status after each attempt and exit upon successful unsealing.  
**Documentation:**
    
    - **Summary:** Provides a simple, automated way to unseal a Vault server by applying the necessary unseal keys. This is used after server restarts to make Vault operational.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Operations
    
- **Path:** terraform/main.tf  
**Description:** Main Terraform configuration file. It configures the Vault provider, specifying the Vault server address and authentication method for Terraform to use. It also orchestrates the invocation of various modules for managing resources within Vault.  
**Template:** Terraform Configuration  
**Dependency Level:** 1  
**Name:** main  
**Type:** Terraform  
**Relative Path:** terraform/main  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Terraform Vault Provider Configuration
    
**Requirement Ids:**
    
    - DEP-004.1
    
**Purpose:** To serve as the entry point for managing Vault resources via Terraform, defining the connection to the Vault server and the overall resource management plan.  
**Logic Description:** This file contains the 'terraform' block to specify required provider versions (e.g., hashicorp/vault). It includes the 'provider "vault"' block, configuring the address and authentication credentials. It will then contain 'module' blocks to call reusable modules for auth methods, secret engines, and policies, passing environment-specific variables.  
**Documentation:**
    
    - **Summary:** The root Terraform file that configures the connection to the HashiCorp Vault server and orchestrates the creation and management of all Vault resources (auth methods, secrets engines, policies) by calling various modules.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/variables.tf  
**Description:** Defines the input variables for the root Terraform configuration. This allows for parameterization of the Vault setup, such as Vault address, environment name, and other high-level configurations, making the code reusable across environments.  
**Template:** Terraform Configuration  
**Dependency Level:** 0  
**Name:** variables  
**Type:** Terraform  
**Relative Path:** terraform/variables  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Terraform Variable Definitions
    
**Requirement Ids:**
    
    - DEP-004.1
    
**Purpose:** To declare all input variables used by the Terraform configuration, providing a clear contract for what needs to be configured for each environment.  
**Logic Description:** This file contains multiple 'variable' blocks. Examples include 'variable "vault_addr" { type = string, description = "The address of the Vault server." }' and 'variable "environment" { type = string, description = "The target environment (e.g., staging, production)." }'. Default values can be provided for non-sensitive variables.  
**Documentation:**
    
    - **Summary:** Declares input variables for the Terraform configuration, such as the Vault server address and environment name. This allows the same configuration to be applied to different environments with different parameters.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/environments/production/production.tfvars  
**Description:** Terraform variable definitions file for the production environment. It provides the specific values for the variables declared in variables.tf, tailored for the production Vault cluster. This file contains sensitive information and must be managed securely.  
**Template:** Terraform Vars  
**Dependency Level:** 1  
**Name:** production  
**Type:** Terraform  
**Relative Path:** terraform/environments/production/production  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Production Environment Configuration
    
**Requirement Ids:**
    
    - DEP-004.1
    
**Purpose:** To define the specific configuration values for deploying and managing the production Vault environment using Terraform.  
**Logic Description:** This is a simple key-value file. It will contain lines like 'vault_addr = "https://vault.prod.creativeflow.ai"' and 'environment = "production"'. It assigns concrete values to the variables defined in the root variables.tf file. This file should NOT be checked into version control if it contains secrets; a template should be checked in instead.  
**Documentation:**
    
    - **Summary:** Contains the variable values specific to the production environment, such as the production Vault server URL. This file is used by Terraform to apply the correct configuration for production.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform.Environments  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/modules/secret_engines/kv2/main.tf  
**Description:** A reusable Terraform module to create and configure a KV Version 2 secrets engine instance in Vault. It allows specifying the path and configuration options for the secrets engine.  
**Template:** Terraform Module  
**Dependency Level:** 2  
**Name:** main  
**Type:** Terraform  
**Relative Path:** terraform/modules/secret_engines/kv2/main  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    - Modularity
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KVv2 Secrets Engine Management
    
**Requirement Ids:**
    
    - INT-006
    - SEC-003
    
**Purpose:** To provide a standardized, reusable way to provision Key/Value (Version 2) secrets engines for storing application secrets.  
**Logic Description:** This file will define a 'resource "vault_mount" "kv2"' block with 'type = "kv"' and 'options = { version = "2" }'. The 'path' will be taken from an input variable. It will also define input variables in a 'variables.tf' file within the same module directory, such as 'variable "mount_path" { type = string }'.  
**Documentation:**
    
    - **Summary:** Reusable Terraform module for creating a KV Version 2 secrets engine at a specified path. This is used for storing arbitrary secrets like API keys and database credentials.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform.Modules.SecretEngines  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/modules/secret_engines/transit/main.tf  
**Description:** A reusable Terraform module to create and configure a Transit secrets engine in Vault. This engine provides 'encryption as a service', allowing applications to encrypt/decrypt data without handling the encryption keys directly.  
**Template:** Terraform Module  
**Dependency Level:** 2  
**Name:** main  
**Type:** Terraform  
**Relative Path:** terraform/modules/secret_engines/transit/main  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    - Modularity
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Transit Secrets Engine Management
    - Encryption as a Service Configuration
    
**Requirement Ids:**
    
    - SEC-003
    - REQ-DA-010
    
**Purpose:** To provision the Transit secrets engine, which is central to the platform's cryptographic key management and data encryption strategy.  
**Logic Description:** This file defines a 'resource "vault_mount" "transit"' block with 'type = "transit"'. It then defines one or more 'resource "vault_transit_secret_backend_key" "app_key"' blocks to create named encryption keys within the engine. The names of the mount and keys will be parameterized using input variables.  
**Documentation:**
    
    - **Summary:** Reusable Terraform module for creating and configuring the Transit secrets engine. This enables centralized management of encryption keys and provides cryptographic functions as a service to other applications.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform.Modules.SecretEngines  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/modules/auth_methods/approle/main.tf  
**Description:** A reusable Terraform module to configure the AppRole authentication method. AppRole is designed for machine-to-machine authentication, allowing applications to securely retrieve a Vault token.  
**Template:** Terraform Module  
**Dependency Level:** 2  
**Name:** main  
**Type:** Terraform  
**Relative Path:** terraform/modules/auth_methods/approle/main  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    - Modularity
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AppRole Auth Method Configuration
    
**Requirement Ids:**
    
    - SEC-003
    - DEP-004.1
    
**Purpose:** To provide a standardized way for applications and microservices to authenticate with Vault and receive a token with appropriate permissions.  
**Logic Description:** This module will define a 'resource "vault_auth_backend" "approle"' with 'type = "approle"'. It will then define a 'resource "vault_approle_auth_backend_role"' to create roles. The role name and associated policies will be passed as input variables. This allows creating distinct roles for each microservice with least-privilege policies.  
**Documentation:**
    
    - **Summary:** Reusable Terraform module for configuring the AppRole authentication method. It allows creating roles that applications can use to authenticate with Vault and obtain a token.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform.Modules.AuthMethods  
**Metadata:**
    
    - **Category:** IaC
    
- **Path:** terraform/modules/auth_methods/jwt_oidc/main.tf  
**Description:** A reusable Terraform module to configure the JWT/OIDC authentication method. This is used to allow external identity providers, such as a CI/CD system (GitLab/GitHub Actions), to authenticate with Vault using a JWT.  
**Template:** Terraform Module  
**Dependency Level:** 2  
**Name:** main  
**Type:** Terraform  
**Relative Path:** terraform/modules/auth_methods/jwt_oidc/main  
**Repository Id:** REPO-SECRETS-MANAGEMENT-VAULT-001  
**Pattern Ids:**
    
    - Infrastructure as Code
    - Modularity
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - JWT/OIDC Auth Method Configuration
    
**Requirement Ids:**
    
    - DEP-003
    
**Purpose:** To enable secure, automated authentication for CI/CD pipelines, allowing them to fetch deployment secrets without long-lived credentials.  
**Logic Description:** This module will define a 'resource "vault_auth_backend" "jwt"' with 'type = "jwt"'. It will also include a 'resource "vault_jwt_auth_backend_role" "cicd_role"'. The role will be configured with a 'bound_audiences' or 'bound_claims' to validate tokens from a specific issuer (e.g., GitLab). The 'user_claim' will identify the unique pipeline/job, and the role will be associated with the CI/CD policy.  
**Documentation:**
    
    - **Summary:** Reusable Terraform module for configuring the JWT/OIDC authentication method. This is primarily used to allow CI/CD systems to securely authenticate using their own tokens and retrieve deployment secrets.
    
**Namespace:** CreativeFlow.Infrastructure.Secrets.Terraform.Modules.AuthMethods  
**Metadata:**
    
    - **Category:** IaC
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableTransitEngine
  - enableDatabaseEngine
  - enableAppRoleAuth
  - enableJwtOidcAuth
  
- **Database Configs:**
  
  


---

