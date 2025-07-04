# This file is a conceptual specification for Kubernetes authentication.
# It documents the configuration needed to allow pods within a Kubernetes cluster
# to authenticate with Vault using their Service Account (SA) JWT.
# The commands documented here should be applied via the `apply_vault_configurations.sh` script
# or an equivalent Terraform configuration.

# --- Enable Kubernetes Auth Method ---
# Command to enable the kubernetes auth method at the default path 'kubernetes'.
# This should be executed once.
#
# vault auth enable -path=kubernetes kubernetes


# --- Configure Kubernetes Auth Method ---
# This command configures the connection from Vault to the Kubernetes API server.
# This is necessary for Vault to validate the service account tokens presented by pods.
# This command should typically be run from within a pod that has access to the k8s API,
# such as the Vault server pod itself if it's running in the cluster.
#
# vault write auth/kubernetes/config \
#     kubernetes_host="https://<K8S_API_SERVER_URL>:6443" \
#     kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
#     token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token


# --- Role: creativeflow-api-service ---
# This is an example role that maps a specific Kubernetes Service Account to a set of Vault policies.
# Any pod running with the 'api-service-sa' service account in the 'creativeflow-prod' namespace
# can authenticate against this role to receive a Vault token with the specified policies.
#
# vault write auth/kubernetes/role/creativeflow-api-service \
#     bound_service_account_names="api-service-sa" \
#     bound_service_account_namespaces="creativeflow-prod" \
#     token_policies="applications_base_policy,api-service-secrets-policy" \
#     ttl="1h"