# This file is a conceptual specification for AppRole authentication.
# It documents the roles and configurations that should be created by the
# `apply_vault_configurations.sh` script or an equivalent Terraform configuration.
# This file itself is not directly processed by Vault.

# --- Enable AppRole Auth Method ---
# Command to enable the approle auth method at the default path 'approle'.
# This should be executed once.
#
# vault auth enable -path=approle approle


# --- Role: webapp-prod-role ---
# This role is intended for the production web application.
# It grants access to webapp-specific secrets and common policies.
# The token generated will be valid for 60 minutes and can be used multiple times.
# The SecretID used to fetch the token is valid for 60 minutes and can be used up to 5 times.
#
# vault write auth/approle/role/webapp-prod-role \
#     token_policies="applications_base_policy,webapp-prod-secrets-policy" \
#     secret_id_ttl="60m" \
#     token_ttl="60m" \
#     token_max_ttl="4h" \
#     secret_id_num_uses=5 \
#     token_num_uses=0 \
#     bind_secret_id=true


# --- Role: cicd-deployer-role ---
# This role is for the CI/CD system when it needs to perform deployment tasks.
# It grants access to policies needed for deployment.
# The token is short-lived (30 min) and the SecretID is even shorter-lived (10 min)
# and can only be used once, making it suitable for a single CI/CD job.
#
# vault write auth/approle/role/cicd-deployer-role \
#     token_policies="cicd_pipeline_policy,app-deployer-policy" \
#     secret_id_ttl="10m" \
#     token_ttl="30m" \
#     secret_id_num_uses=1