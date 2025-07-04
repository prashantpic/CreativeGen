#!/bin/bash
#
# This script applies the defined HCL configurations and policies to a running Vault instance.
# It is designed to be idempotent where possible, meaning it can be run multiple times
# without causing errors or unintended changes.
#
# Prerequisites:
# 1. The 'vault' and 'jq' CLI tools must be installed and in the PATH.
# 2. The VAULT_ADDR and VAULT_TOKEN environment variables must be set.
#    The VAULT_TOKEN must have sufficient permissions to perform these actions
#    (e.g., the initial root token or a highly privileged admin token).
#

set -e

# --- Environment Check ---
: "${VAULT_ADDR?Error: VAULT_ADDR environment variable is not set.}"
: "${VAULT_TOKEN?Error: VAULT_TOKEN environment variable is not set.}"
: "${ENABLE_PKI_ENGINE_ROOT:=false}"
: "${ENABLE_PKI_ENGINE_INTERMEDIATE:=false}"

echo "Applying Vault Configurations to instance at ${VAULT_ADDR}..."
echo "--------------------------------------------------------"

# --- 1. Audit Devices ---
echo "[1/6] Configuring audit devices..."
vault audit list | grep -q "file_audit_log/" || \
  vault audit enable -path=file_audit_log file file_path="/var/log/vault/vault_audit.log" log_raw="false" format="json" mode="0600"
echo "File audit device 'file_audit_log' ensured."

# --- 2. Auth Methods ---
echo "[2/6] Configuring authentication methods..."
# Enable AppRole
vault auth list | grep -q "approle/" || vault auth enable -path=approle approle
echo "AppRole auth method ensured."
# Create AppRole Roles (Example)
vault write auth/approle/role/webapp-prod-role token_policies="applications_base_policy,webapp-prod-secrets-policy" secret_id_ttl="60m" token_ttl="60m" secret_id_num_uses=5 bind_secret_id=true > /dev/null
echo "Role 'webapp-prod-role' configured."

# Enable Kubernetes
vault auth list | grep -q "kubernetes/" || vault auth enable -path=kubernetes kubernetes
echo "Kubernetes auth method ensured."
# NOTE: Kubernetes config and roles require specific cluster info and are best applied
# from within the cluster or via a CI/CD pipeline with access to cluster details.
# Example placeholders:
# vault write auth/kubernetes/config kubernetes_host="https://<K8S_API_URL>" ...
# vault write auth/kubernetes/role/my-app bound_service_account_names=...

# --- 3. Secrets Engines ---
echo "[3/6] Configuring secrets engines..."
# Enable KV-V2
vault secrets list | grep -q "secret/" || vault secrets enable -path=secret kv-v2
echo "KV-V2 secrets engine at 'secret/' ensured."

# Enable Transit
vault secrets list | grep -q "transit/" || vault secrets enable -path=transit transit
echo "Transit secrets engine at 'transit/' ensured."
# Create transit keys (Example)
vault write -f transit/keys/app-general-encryption-key type=aes256-gcm96 exportable=false allow_plaintext_backup=false > /dev/null
vault write transit/keys/app-general-encryption-key/config rotation_period=2592000s > /dev/null
echo "Transit key 'app-general-encryption-key' configured with 30-day rotation."

# Enable Database
vault secrets list | grep -q "database/" || vault secrets enable -path=database database
echo "Database secrets engine at 'database/' ensured."
# NOTE: Configuring the database engine requires a live database and a secure password.
# This should be done in a secure, automated way, potentially retrieving the password
# from another Vault secret.
# Example placeholder:
# vault write database/config/postgresql-creativeflow plugin_name=... password="<SECURE_PASSWORD>"

# --- 4. Policies ---
echo "[4/6] Writing policies..."
POLICY_DIR="$(dirname "$0")/../policies"
vault policy write applications_base_policy "${POLICY_DIR}/applications_base_policy.hcl"
vault policy write cicd_pipeline_policy "${POLICY_DIR}/cicd_pipeline_policy.hcl"
vault policy write kms_admin_policy "${POLICY_DIR}/kms_admin_policy.hcl"
# Add other policies here, e.g., vault policy write webapp-prod-secrets-policy ...
echo "Core policies written."

# --- 5. PKI Engine Setup (Conditional) ---
echo "[5/6] Checking for PKI engine setup..."
if [ "$ENABLE_PKI_ENGINE_ROOT" = "true" ]; then
  echo "  -> Setting up PKI Root CA..."
  vault secrets list | grep -q "^pki_root/" || vault secrets enable -path=pki_root pki
  vault secrets tune -max-lease-ttl=87600h pki_root # 10 years
  
  # Check if root CA already exists to avoid overwriting
  if ! vault read pki_root/ca/pem > /dev/null 2>&1; then
    echo "  -> Generating new Root CA..."
    vault write -field=certificate pki_root/root/generate/internal \
      common_name="CreativeFlow AI Root CA" \
      ttl=87600h key_type=rsa key_bits=4096 exclude_cn_from_sans=true > root_ca.crt
    echo "  -> Root CA certificate saved to root_ca.crt"
  else
    echo "  -> Root CA already exists."
  fi
  
  vault write pki_root/config/urls \
    issuing_certificates="${VAULT_ADDR}/v1/pki_root/ca" \
    crl_distribution_points="${VAULT_ADDR}/v1/pki_root/crl"
  echo "  -> PKI Root CA configuration updated."
else
  echo "  -> PKI Root CA setup skipped (ENABLE_PKI_ENGINE_ROOT is not 'true')."
fi

if [ "$ENABLE_PKI_ENGINE_INTERMEDIATE" = "true" ] && [ "$ENABLE_PKI_ENGINE_ROOT" = "true" ]; then
  echo "  -> Setting up PKI Intermediate CA..."
  vault secrets list | grep -q "^pki_int/" || vault secrets enable -path=pki_int pki
  vault secrets tune -max-lease-ttl=43800h pki_int # 5 years
  
  # Check if intermediate is already set up
  if ! vault read pki_int/ca/pem > /dev/null 2>&1; then
      echo "  -> Generating new Intermediate CA CSR..."
      CSR_DATA=$(vault write -format=json pki_int/intermediate/generate/internal \
        common_name="CreativeFlow AI Internal Services ICA" \
        ttl=43800h key_type=rsa key_bits=4096 exclude_cn_from_sans=true)
      
      echo "  -> Signing Intermediate CSR with Root CA..."
      SIGN_DATA=$(echo "$CSR_DATA" | jq -r .data.csr | vault write -format=json pki_root/root/sign-intermediate - \
        format=pem_bundle ttl=43800h)
        
      echo "  -> Setting signed certificate for Intermediate CA..."
      echo "$SIGN_DATA" | jq -r .data.certificate | vault write pki_int/intermediate/set-signed -
  else
    echo "  -> Intermediate CA already exists."
  fi

  vault write pki_int/config/urls \
    issuing_certificates="${VAULT_ADDR}/v1/pki_int/ca" \
    crl_distribution_points="${VAULT_ADDR}/v1/pki_int/crl"
  echo "  -> PKI Intermediate CA configuration updated."
else
  echo "  -> PKI Intermediate CA setup skipped."
fi

# --- 6. Completion ---
echo "[6/6] Vault configuration script finished."
echo "--------------------------------------------------------"