# Configuration: Secrets Management Integration with HashiCorp Vault

This document describes the strategy for securely managing all sensitive data, particularly API keys, using HashiCorp Vault. This approach is critical for fulfilling security requirement **INT-006**. The primary mechanism for this integration is the custom n8n node, `SecureVaultApiCallerNode`.

## Core Strategy

1.  **Centralized Storage**: All secrets, including API keys for third-party AI services (OpenAI, Stability AI), internal service credentials, and other sensitive tokens, **MUST** be stored in HashiCorp Vault. They should **NEVER** be stored in Git, n8n's internal credential store (unless as a last resort for dev), or environment variables (except for Vault's own authentication credentials).

2.  **Just-in-Time Retrieval**: Secrets are fetched by n8n workflows at runtime, immediately before they are needed. They are held in memory only for the duration of the API call and are not persisted in n8n's execution logs.

3.  **Principle of Least Privilege**: The Vault authentication role used by the n8n instance must have policies that grant it read-only access to the specific secret paths it requires, and nothing more.

## Vault Configuration for n8n

The n8n instance needs to be able to authenticate with Vault. This is configured via environment variables.

*   **`VAULT_ADDR`**
    *   **Description**: The full URL of the HashiCorp Vault server.
    *   **Example**: `https://vault.creativeflow.tech`

*   **Authentication Method: AppRole (Recommended for Services)**
    *   **Description**: AppRole is a secure authentication mechanism for applications. The n8n instance will be configured with a `RoleID` and a `SecretID` to obtain a Vault token.
    *   **`VAULT_APPROLE_ID`**: The RoleID for the n8n AppRole.
    *   **`VAULT_APPROLE_SECRET_ID`**: The SecretID for the n8n AppRole. This should be treated as a highly sensitive secret.

*   **Authentication Method: Kubernetes Auth (Alternative if n8n runs in K8s)**
    *   **Description**: If n8n is deployed within the Kubernetes cluster, it can use its Kubernetes Service Account Token to authenticate with Vault. This is a highly secure method that avoids managing long-lived secrets like AppRole SecretIDs.
    *   **Configuration**: This requires setting up the Vault Kubernetes Auth Method and binding the n8n service account to a Vault policy. The custom nodes would then use the service account token found at `/var/run/secrets/kubernetes.io/serviceaccount/token`.

## Example Secret Paths in Vault

Secrets should be organized logically within Vault. Assuming the use of the KV Version 2 secrets engine mounted at `secret/`:

*   **OpenAI API Key**:
    *   **Path**: `secret/data/creativeflow/ai_providers/openai`
    *   **Key**: `api_key`
    *   **Value**: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

*   **Stability AI API Key**:
    *   **Path**: `secret/data/creativeflow/ai_providers/stabilityai`
    *   **Key**: `api_key`
    *   **Value**: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

*   **Content Moderation Service API Key**:
    *   **Path**: `secret/data/creativeflow/services/content_moderation`
    *   **Key**: `api_key`
    *   **Value**: `cm-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Usage in Custom Nodes

*   The `SecureVaultApiCallerNode` is designed to handle this entire flow.
*   It internally reads the `VAULT_ADDR`, `VAULT_APPROLE_ID`, and `VAULT_APPROLE_SECRET_ID` environment variables to initialize its Vault client.
*   It uses the `vaultSecretPath` and `vaultSecretKey` parameters provided in the workflow to fetch the correct secret.
*   The fetched secret is immediately used to make the API call and is not returned as a direct output of the node, preventing accidental exposure.