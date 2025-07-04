# Configuration: n8n Instance Settings

This document outlines the essential configuration parameters for running the `CreativeFlow.N8NWorkflowEngine` instance. These settings are primarily managed through environment variables, which should be set in the deployment environment (e.g., Docker environment file, Kubernetes ConfigMap/Secret).

## Critical Security Variables

*   **`N8N_ENCRYPTION_KEY`**
    *   **Description**: A mandatory, high-entropy secret key used by n8n to encrypt sensitive data, such as credentials, stored in its database.
    *   **Action**: Generate a strong, random string (at least 32 characters) and store it securely (e.g., in HashiCorp Vault, Kubernetes Secret). **Losing this key will result in irreversible loss of access to all encrypted credentials.**
    *   **Example**: `N8N_ENCRYPTION_KEY=YourSuperLongAndRandomSecretKeyForN8nEncryption`

## Database Configuration (PostgreSQL)

The n8n instance is configured to use a PostgreSQL database for storing its operational data (workflows, executions, credentials).

*   **`DB_TYPE`**: Must be set to `postgres`.
*   **`DB_POSTGRESDB_HOST`**: Hostname or IP address of the PostgreSQL server.
*   **`DB_POSTGRESDB_PORT`**: Port number for the PostgreSQL server (default: `5432`).
*   **`DB_POSTGRESDB_USER`**: Username for the database connection.
*   **`DB_POSTGRESDB_PASSWORD`**: Password for the database connection.
*   **`DB_POSTGRESDB_DATABASE`**: The name of the database n8n should use.

## Custom Node Configuration

*   **`N8N_CUSTOM_EXTENSIONS_PATH`**
    *   **Description**: The filesystem path within the n8n container where custom node packages are located. This allows n8n to discover and load the `CreativeFlowModelSelectorNode`, `SecureVaultApiCallerNode`, and `K8sJobOrchestratorNode`.
    *   **Example**: `/home/node/.n8n/custom` (a common default) or `/n8n/nodes`. The build process (e.g., Dockerfile) must place the compiled nodes from the `nodes/dist` directory into this path.

## Core n8n Behavior

*   **Execution Mode**: For scalability, n8n should be run in a scaled configuration. This typically involves:
    *   One `main` process instance (`N8N_EXECUTION_PROCESS=main`).
    *   Multiple `queue` process instances (`N8N_EXECUTION_PROCESS=queue`) to handle workflow executions, consuming jobs from RabbitMQ.
*   **`EXECUTIONS_DATA_PRUNE`**: Set to `true` to enable automatic pruning of old execution data.
*   **`EXECUTIONS_DATA_MAX_AGE_HOURS`**: The maximum age (in hours) of execution data to retain. This is crucial for managing database size.
    *   **Example**: `EXECUTIONS_DATA_MAX_AGE_HOURS=720` (30 days)
*   **`N8N_LOG_LEVEL`**: Logging verbosity. Recommended values for production are `info` or `warn`. Use `debug` for troubleshooting.
*   **`N8N_LOG_OUTPUT`**: Where to send logs. `console` is standard for containerized environments.

## Feature Toggles

These environment variables control the behavior of specific features within the workflows.

*   **`USE_VAULT_FOR_ALL_AI_KEYS`**: (Default: `true`) If `false`, allows workflows to use n8n's built-in credential store as a fallback (less secure, for dev/test only).
*   **`ENABLE_AB_TESTING_MODEL_SELECTOR`**: (Default: `false`) Set to `true` to activate the A/B testing logic in the `CreativeFlowModelSelectorNode`.
*   **`ENABLE_CONTENT_MODERATION_WORKFLOW`**: (Default: `true`) If `false`, the content moderation sub-workflow will be skipped.
*   **`ENABLE_DETAILED_USAGE_LOGGING_VIA_API`**: (Default: `true`) If `false`, the step to call the internal usage logging API will be skipped.

## Resource Allocation

For a production environment, the n8n instance(s) should be allocated sufficient resources:
*   **CPU**: At least 1-2 vCPUs recommended per instance.
*   **Memory**: At least 2-4 GB RAM per instance.
*   **Note**: Resource needs will vary based on workflow complexity and execution volume. Monitoring is key to finding the right allocation.