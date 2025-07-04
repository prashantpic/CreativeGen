# Software Design Specification (SDS) for CreativeFlow.Infrastructure.Secrets.Vault

## 1. Introduction

### 1.1. Purpose
This document outlines the software design specification for the `CreativeFlow.Infrastructure.Secrets.Vault` repository. Its purpose is to define the configuration, policies, operational scripts, and Infrastructure as Code (IaC) setup for a highly available, secure HashiCorp Vault cluster. This Vault instance will serve as the central secrets management solution for the entire CreativeFlow AI platform, responsible for storing, managing access to, and auditing all sensitive data such as database credentials, third-party API keys, and internal service tokens.

### 1.2. Scope
The scope of this SDS covers:
-   Core Vault server configuration for a high-availability (HA) cluster.
-   Access control policies (ACLs) for administrators, CI/CD pipelines, and application services.
-   Authentication methods for both human operators and machine entities.
-   Configuration of secrets engines for storing secrets (KVv2) and providing Encryption-as-a-Service (Transit).
-   Operational scripts for essential day-one tasks like initialization and unsealing.
-   The complete Infrastructure as Code (IaC) setup using Terraform to manage all Vault resources declaratively.

## 2. System Architecture & Design Principles

The Vault service is designed as a critical piece of core infrastructure, built upon the following principles:

*   **High Availability (HA):** The Vault cluster will be deployed across multiple nodes using Vault's integrated storage (Raft) backend, which provides a robust, self-contained HA solution without external dependencies.
*   **Infrastructure as Code (IaC):** All Vault resources (auth methods, secrets engines, policies) will be managed declaratively using Terraform. This ensures consistency, repeatability, and an auditable history of changes.
*   **Policy as Code (PaC):** All access control policies will be written in HCL, version-controlled in Git, and applied via the IaC pipeline, ensuring that permissions are managed explicitly and are subject to code review.
*   **Principle of Least Privilege:** All entities (users, applications, CI/CD jobs) will be granted the minimum permissions necessary to perform their intended functions. This is enforced through granular ACL policies.
*   **Zero-Trust Security Model:** Every request to Vault requires authentication and authorization. AppRole and JWT/OIDC auth methods are used for secure machine-to-machine communication without relying on network trust.
*   **Encryption-as-a-Service:** The Transit secrets engine will be used to provide cryptographic functions to applications, ensuring that sensitive data can be encrypted/decrypted without applications ever handling the raw encryption keys.

## 3. Vault Server Configuration (`config/vault_server.hcl`)

This file defines the static, low-level configuration for each Vault server node. It will be managed and deployed by a configuration management tool (e.g., Ansible). Values should be templated to allow for environment-specific settings.

hcl
# /config/vault_server.hcl

# Disable memory locking for development/testing if needed, but enable in production.
# disable_mlock = true

# Storage Backend: Use integrated Raft storage for HA.
storage "raft" {
  path    = "{{ vault_raft_storage_path }}" # e.g., /opt/vault/data
  node_id = "{{ vault_node_id }}"          # e.g., vault-node-1 (must be unique per node)

  # For production, consider performance tuning options:
  # performance_multiplier = 1
}

# HA Listener for inter-node communication
# This is where other nodes in the cluster will connect.
listener "tcp" {
  address = "0.0.0.0:8201"
  cluster_address = "{{ vault_cluster_address }}:8201" # This node's address for cluster communication
  tls_disable = "true" # In production, set to false and configure TLS certs
  # tls_cert_file = "/etc/vault.d/certs/vault.crt"
  # tls_key_file  = "/etc/vault.d/certs/vault.key"
}

# API Listener for client communication
# This is the main address clients will use to interact with Vault.
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = "true" # In production, set to false and configure TLS certs
  # tls_cert_file = "/etc/vault.d/certs/vault.crt"
  # tls_key_file  = "/etc/vault.d/certs/vault.key"
}

# The address to advertise to other Vault servers in the cluster for client redirection.
api_addr = "http://{{ vault_api_address }}:8200" # Use https in production

# The address to advertise to other Vault servers in the cluster for cluster-related
# communication and redirection.
cluster_addr = "http://{{ vault_cluster_address }}:8201" # Use https in production

# Enable Prometheus telemetry for monitoring
telemetry {
  prometheus_retention_time = "24h"
  disable_hostname = true
}

# Enable the Vault Web UI
ui = true


## 4. Vault Policies (ACL)

Policies are defined in HCL and managed via Terraform. They enforce the principle of least privilege.

### 4.1. `policies/admin_policy.hcl`
Grants full administrative privileges. Assigned only to operator groups.

hcl
# /policies/admin_policy.hcl

# Allow full control over system-level settings and management
path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Allow full control over authentication methods
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Allow full control over all secrets engines
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Allow management of identity entities and groups
path "identity/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}


### 4.2. `policies/ci_cd_policy.hcl`
Grants read-only access for CI/CD pipelines to application secrets. This policy will be associated with a JWT/OIDC role.

hcl
# /policies/ci_cd_policy.hcl

# Deny access to sensitive system paths by default
path "sys/*" {
  capabilities = ["deny"]
}
path "auth/*" {
  capabilities = ["deny"]
}

# Allow CI/CD pipelines to read secrets for applications based on environment.
# The path will be parameterized by claims from the CI/CD JWT token.
path "secret/data/apps/{{identity.entity.aliases.auth_jwt.name}}/*" {
  capabilities = ["read"]
}

**Note:** `{{identity.entity.aliases.auth_jwt.name}}` is a Vault templating feature that will resolve to a value from the JWT token, such as the repository path (`project_path:group/project`), providing dynamic, secure pathing.

### 4.3. `policies/app_services_policy.hcl`
A template for policies assigned to application microservices via AppRole. It grants access to service-specific secrets and cryptographic functions. This will be instantiated per service by Terraform.

hcl
# /policies/app_services_policy.hcl - Generic template

# Deny access to system and auth paths
path "sys/*"    { capabilities = ["deny"] }
path "auth/*"   { capabilities = ["deny"] }

# Allow the application to read its own secrets
# The {{app_name}} and {{environment}} will be replaced by Terraform for each service.
path "secret/data/apps/{{app_name}}/{{environment}}" {
  capabilities = ["read"]
}

# Allow the application to use the transit engine for encryption and decryption
# This grants access to encrypt/decrypt using a specific key, not manage the key itself.
path "transit/encrypt/{{app_name}}-key" {
  capabilities = ["update"]
}
path "transit/decrypt/{{app_name}}-key" {
  capabilities = ["update"]
}

# Allow the application to rewrap its token, extending its lifetime
path "auth/token/renew-self" {
  capabilities = ["update"]
}


## 5. Operational Scripts

### 5.1. `scripts/bootstrap_vault.sh`
This script performs the one-time initialization of the Vault cluster.

bash
#!/bin/bash
# /scripts/bootstrap_vault.sh

set -e

VAULT_ADDR=${VAULT_ADDR:-"http://127.0.0.1:8200"}
INIT_FILE="/root/vault_init_keys.txt"

echo "Checking if Vault is initialized..."

# Check the init status
if vault status -format=json | jq -e '.initialized == false'; then
  echo "Vault is not initialized. Initializing now..."
  
  # Initialize Vault with 5 keys and a threshold of 3
  vault operator init -key-shares=5 -key-threshold=3 > ${INIT_FILE}
  
  echo "############################################################"
  echo "## VAULT INITIALIZATION COMPLETE                          ##"
  echo "############################################################"
  echo ""
  echo "Unseal keys and Initial Root Token have been written to:"
  echo "${INIT_FILE}"
  echo ""
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!-CRITICAL-!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "SECURELY STORE these keys and token in a designated password manager."
  echo "This file should be deleted from the server after secure storage."
  echo "You will need 3 of the 5 unseal keys to unseal Vault."
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
else
  echo "Vault is already initialized. No action taken."
fi


### 5.2. `scripts/unseal_vault.sh`
This script automates the process of unsealing a Vault node.

bash
#!/bin/bash
# /scripts/unseal_vault.sh

set -e

VAULT_ADDR=${VAULT_ADDR:-"http://127.0.0.1:8200"}
KEY_COUNT=3 # Number of keys required to unseal

echo "Attempting to unseal Vault at ${VAULT_ADDR}"

# Check the seal status
if vault status -format=json | jq -e '.sealed == true'; then
  for (( i=1; i<=${KEY_COUNT}; i++ )); do
    # Read key securely from environment variable or prompt if not set
    key_var="VAULT_UNSEAL_KEY_${i}"
    if [ -n "${!key_var}" ]; then
      UNSEAL_KEY="${!key_var}"
      echo "Using unseal key from environment variable ${key_var}..."
    else
      read -s -p "Enter Unseal Key ${i}: " UNSEAL_KEY
      echo ""
    fi
    
    vault operator unseal "${UNSEAL_KEY}"
    
    # Check if unsealed after applying the key
    if vault status -format=json | jq -e '.sealed == false'; then
      echo "Vault has been successfully unsealed."
      exit 0
    fi
  done
  
  echo "Error: Applied ${KEY_COUNT} keys but Vault is still sealed. Please check the keys."
  exit 1
else
  echo "Vault is already unsealed. No action taken."
fi


## 6. Infrastructure as Code (Terraform)

### 6.1. Root Configuration (`terraform/`)
*   **`main.tf`**: Entry point. Configures the Vault provider and calls modules.
    terraform
    terraform {
      required_providers {
        vault = {
          source  = "hashicorp/vault"
          version = "~> 3.25"
        }
      }
    }

    provider "vault" {
      address = var.vault_addr
      # Authentication for Terraform will be handled via environment variables
      # (VAULT_TOKEN) in the CI/CD pipeline.
    }

    # Example module invocations
    module "secret_engines" {
      source      = "./modules/secret_engines"
      environment = var.environment
      applications = var.applications # Pass application definitions
    }

    module "auth_methods" {
      source            = "./modules/auth_methods"
      environment       = var.environment
      jwt_oidc_provider_url = var.jwt_oidc_provider_url
      applications      = var.applications
    }

    module "policies" {
      source       = "./modules/policies"
      applications = var.applications
    }
    
*   **`variables.tf`**: Defines inputs for the configuration.
    terraform
    variable "vault_addr" {
      type        = string
      description = "The address of the Vault server."
    }

    variable "environment" {
      type        = string
      description = "The target environment (e.g., staging, production)."
    }
    
    variable "jwt_oidc_provider_url" {
      type = string
      description = "The OIDC discovery URL for the JWT auth provider (e.g., GitLab)."
    }

    variable "applications" {
      type = map(object({
        policy_name = string
        # other app-specific vars
      }))
      description = "A map of application definitions to configure secrets and auth."
    }
    
*   **`terraform/environments/production/production.tfvars`**: Environment-specific values. This file should be managed securely and **NOT** committed to version control.
    hcl
    # Example content for production.tfvars
    vault_addr = "https://vault.prod.creativeflow.ai"
    environment = "production"
    jwt_oidc_provider_url = "https://gitlab.com"
    
    applications = {
      "user-management-service" = {
        policy_name = "app-user-management-policy"
      },
      "ai-generation-service" = {
        policy_name = "app-ai-generation-policy"
      }
    }
    

### 6.2. Modules (`terraform/modules/`)

#### 6.2.1. `secret_engines` Module
*   **`main.tf`**: Manages all secret engines.
    terraform
    # /modules/secret_engines/main.tf
    
    # KV Version 2 engine for application secrets
    resource "vault_mount" "kv2_apps" {
      path        = "secret"
      type        = "kv"
      description = "KVv2 engine for all application secrets"
      options = {
        version = "2"
      }
    }

    # Transit engine for Encryption-as-a-Service
    resource "vault_mount" "transit" {
      path        = "transit"
      type        = "transit"
      description = "Encryption as a Service"
    }
    
    # Create an encryption key for each application
    resource "vault_transit_secret_backend_key" "app_keys" {
      for_each = var.applications
      
      backend = vault_mount.transit.path
      name    = "${each.key}-key"
      type    = "aes256-gcm96" # Strong default
    }
    
*   **`variables.tf`**: Defines inputs like `applications`.

#### 6.2.2. `auth_methods` Module
*   **`main.tf`**: Manages auth methods like AppRole and JWT/OIDC.
    terraform
    # /modules/auth_methods/main.tf
    
    # AppRole for applications
    resource "vault_auth_backend" "approle" {
      type = "approle"
    }
    
    resource "vault_approle_auth_backend_role" "app_roles" {
      for_each = var.applications

      backend        = vault_auth_backend.approle.path
      role_name      = each.key
      token_policies = [each.value.policy_name]
      # Add other constraints like secret_id_ttl, token_ttl, etc.
    }
    
    # JWT/OIDC for CI/CD
    resource "vault_auth_backend" "jwt" {
      type = "jwt"
      path = "jwt-cicd"
    }

    resource "vault_jwt_auth_backend_config" "cicd_config" {
      backend               = vault_auth_backend.jwt.path
      oidc_discovery_url    = var.jwt_oidc_provider_url
      bound_issuer          = var.jwt_oidc_provider_url
    }
    
    resource "vault_jwt_auth_backend_role" "cicd_role" {
      backend        = vault_auth_backend.jwt.path
      role_name      = "ci-cd-role"
      token_policies = ["ci_cd_policy"]
      user_claim     = "project_path" # e.g., for GitLab
      bound_claims = {
        # Restrict to a specific GitLab group or project
        "project_path" = "creative-flow-ai/*" 
      }
    }
    
*   **`variables.tf`**: Defines inputs like `jwt_oidc_provider_url` and `applications`.

#### 6.2.3. `policies` Module
*   **`main.tf`**: Manages all ACL policies from HCL files.
    terraform
    # /modules/policies/main.tf
    
    resource "vault_policy" "admin" {
      name   = "admin"
      policy = file("${path.module}/../../policies/admin_policy.hcl")
    }

    resource "vault_policy" "ci_cd" {
      name   = "ci_cd_policy"
      policy = file("${path.module}/../../policies/ci_cd_policy.hcl")
    }
    
    resource "vault_policy" "app_policies" {
      for_each = var.applications
      
      name = each.value.policy_name
      policy = templatefile("${path.module}/../../policies/app_services_policy.hcl", {
        app_name = each.key
        environment = var.environment
      })
    }
    
*   **`variables.tf`**: Defines inputs like `applications` and `environment`.