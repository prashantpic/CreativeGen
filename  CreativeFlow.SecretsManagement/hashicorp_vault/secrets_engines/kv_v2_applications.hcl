# This file is a conceptual specification for the KV Version 2 secrets engine.
# It documents the setup for a secure, versioned key-value store for application secrets.
# The commands documented here should be applied via the `apply_vault_configurations.sh` script
# or an equivalent Terraform configuration.

# --- Enable KV-V2 Secrets Engine ---
# This command enables the KV-V2 secrets engine at the path 'secret/'.
# Using 'kv-v2' as the type is the modern syntax.
#
# vault secrets enable -path=secret kv-v2


# --- Configure KV-V2 Engine (Optional Tuning) ---
# This command configures the engine to keep up to 10 versions of each secret
# and to retain deleted versions for 90 days (2160 hours) before they are
# permanently removed. This allows for recovery from accidental deletion.
#
# vault write secret/config max_versions=10 delete_version_after=2160h


# --- Usage Note ---
# This configuration enables the engine. Actual secrets are not defined here.
# They would be written to paths under this engine programmatically or via UI/CLI.
# Example path for storing an OpenAI API key (as per requirement INT-006):
#
# vault kv put secret/ai_services/openai/api_key key="sk-..."
#
# The data is retrieved from 'secret/data/ai_services/openai/api_key'.