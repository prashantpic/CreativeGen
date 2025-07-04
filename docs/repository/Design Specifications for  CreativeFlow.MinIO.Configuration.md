# Software Design Specification: CreativeFlow.MinIO.Configuration

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.MinIO.Configuration` repository. This repository contains configuration scripts and operational utilities essential for setting up, managing, and maintaining the MinIO S3-compatible object storage cluster used by the CreativeFlow AI platform. The specifications herein will guide the development of these scripts, ensuring they meet functional, operational, and security requirements.

### 1.2 Scope
The scope of this SDS covers the design and implementation of:
- Shell scripts (`.sh`) utilizing the MinIO Client (`mc`) for common MinIO administrative tasks.
- Python scripts (`.py`) leveraging the MinIO Python SDK for more complex operations or programmatic logic.
- Configuration templates (e.g., JSON for policies).
- Environment setup and utility scripts.

The scripts will address:
- Initial MinIO cluster setup (bucket creation, default policies).
- Replication configuration (site-to-site, bucket-level DR).
- Access control management (users, groups, IAM-like policies).
- Lifecycle policy management.
- Cluster administration and monitoring utilities (health checks, Prometheus endpoint).
- Key Management Service (KMS) integration for Key Encryption Keys (KEK).

### 1.3 Definitions, Acronyms, and Abbreviations
- **MinIO:** High-performance, S3-compatible object storage.
- **mc:** MinIO Client command-line tool.
- **SDK:** Software Development Kit.
- **IAM:** Identity and Access Management.
- **ILM:** Information Lifecycle Management.
- **KMS:** Key Management Service.
- **KEK:** Key Encryption Key.
- **DR:** Disaster Recovery.
- **PWA:** Progressive Web Application.
- **SDS:** Software Design Specification.
- **SRS:** Software Requirements Specification.
- **CI/CD:** Continuous Integration / Continuous Deployment.
- **NFR:** Non-Functional Requirement.
- **DEP:** Deployment Requirement (from Core Platform Infrastructure & Operations).
- **CPIO:** Core Platform Infrastructure & Operations Requirement.
- **REQ-DA:** Data Architecture & Storage Management Requirement.
- **SEC:** Security Requirement.

### 1.4 References
- CreativeFlow AI Software Requirements Specification (SRS)
    - Section 2.1 (MinIO object storage)
    - Section 5.1 (Object Storage in Arch)
    - Section 5.2.2 (Storage component)
    - Section 7.4.1 (Object Storage Organization)
    - Section 7.5 (Data Retention Policies - for lifecycle)
    - NFR-004 (MinIO Replication for fault tolerance)
    - NFR-006 (Data protection - for policies)
    - DEP-001 (Object Storage infrastructure reqs)
    - DEP-005 (Monitoring, Backup)
    - SEC-003 (KMS, Encryption)
    - SEC-006 (IAM policies, WAF)
    - CPIO-005 (MinIO cluster setup)
    - REQ-DA-010 (KMS integration)
    - REQ-DA-012 (MinIO Replication)
    - Appendix B (MinIO deployment architecture)
- MinIO Documentation (https://min.io/docs/minio/linux/index.html)
- MinIO Client (`mc`) Documentation (https://min.io/docs/minio/linux/reference/minio-mc.html)
- MinIO Python SDK Documentation (https://min.io/docs/minio/linux/developers/python/API.html)

### 1.5 Overview
This document is organized into sections detailing the overall design approach, common utilities, and specific design for each script and configuration file within the repository. Each file specification will include its purpose, dependencies, input parameters, core logic, and error handling considerations.

## 2. System Overview
The `CreativeFlow.MinIO.Configuration` repository provides a suite of tools to manage a self-hosted MinIO cluster. These tools are intended to be run by system administrators or automated via CI/CD pipelines (where appropriate, with secure secret management). They interact directly with MinIO servers using the `mc` client or the Python SDK.

The primary goals are:
- **Automation:** Automate repetitive MinIO configuration tasks.
- **Consistency:** Ensure consistent setup across different MinIO environments (dev, staging, prod, DR).
- **Best Practices:** Implement MinIO configurations adhering to security and operational best practices.
- **Maintainability:** Provide clear, well-documented scripts.

## 3. Design Considerations

### 3.1 Technology Stack
- **Shell:** Bash 5.2.15 (or compatible) for `mc` wrapper scripts.
- **MinIO Client (`mc`):** Latest stable version compatible with the MinIO server version (RELEASE.2024-06-15T06-06-15Z).
- **Python:** Python 3.11.9 for SDK-based utilities.
- **MinIO Python SDK:** `minio` library (e.g., `minio>=7.0.0`).
- **Operating System:** Scripts should be runnable on Linux environments (e.g., Ubuntu 22.04 LTS where Ansible/CI/CD runners might operate).

### 3.2 Security
- **Secrets Management:** All scripts requiring MinIO access credentials (access key, secret key) will rely on these being set as environment variables, typically sourced from a `set_env.sh` file. The `set_env.sh` file itself is a template (`set_env.sh.template`) and the populated version **MUST NOT** be committed to version control. For automated execution (e.g., CI/CD), secrets must be injected securely by the CI/CD system (e.g., HashiCorp Vault, GitLab CI variables).
- **Least Privilege:** IAM policies applied should follow the principle of least privilege.
- **Error Handling:** Scripts will implement robust error handling and provide informative messages.
- **Idempotency:** Where feasible, configuration scripts (e.g., bucket creation, policy application) will be designed to be idempotent, meaning they can be run multiple times with the same effect as running them once.

### 3.3 Modularity and Reusability
- A `common_utils.sh` script will house shared shell functions for logging, error handling, and environment variable checks.
- Python utilities will be organized within the `python_utils` directory with a `requirements.txt` for dependencies.

### 3.4 Configuration
- Policy documents (IAM, lifecycle) will be managed as JSON templates in `config_templates/` to allow for customization and version control.
- Environment-specific parameters (endpoints, credentials) will be managed outside the scripts, primarily through `set_env.sh`.

## 4. Detailed Design Specifications

### 4.1 `set_env.sh.template`
- **Purpose:** Template for users to configure MinIO client environment variables.
- **Requirement Mapping:** DEP-001
- **Type:** Configuration Script Template
- **Language:** Shell
- **Logic Description:**
    1.  Provide commented-out placeholder lines for the following environment variables:
        bash
        # export MC_HOST_ALIAS_URL="http://your-minio-endpoint:9000"
        # export MC_HOST_ALIAS_ACCESS_KEY="YOUR_ACCESS_KEY"
        # export MC_HOST_ALIAS_SECRET_KEY="YOUR_SECRET_KEY"
        # export MINIO_ALIAS_NAME="myminio" # Default alias name to be used by scripts
        
        *   Replace `ALIAS` in `MC_HOST_ALIAS_URL`, `MC_HOST_ALIAS_ACCESS_KEY`, `MC_HOST_ALIAS_SECRET_KEY` with the value of `MINIO_ALIAS_NAME`. For example, if `MINIO_ALIAS_NAME` is `myminio`, then the variables would be `MC_HOST_myminio_URL`, `MC_HOST_myminio_ACCESS_KEY`, `MC_HOST_myminio_SECRET_KEY`.
    2.  Include comments explaining what each variable is for and how to potentially obtain the values.
    3.  Include a strong warning that the populated `set_env.sh` (copied from this template) file should **NOT** be committed to version control.
    4.  Suggest adding the populated `set_env.sh` to `.gitignore`.
    5.  Provide an example of how to configure the alias using `mc alias set $MINIO_ALIAS_NAME $MC_HOST_ALIAS_URL $MC_HOST_ALIAS_ACCESS_KEY $MC_HOST_ALIAS_SECRET_KEY`. The scripts will assume this alias has been set OR that the `MC_HOST_...` variables are correctly configured for direct `mc` usage with the `$MINIO_ALIAS_NAME`.
- **Usage:** Users copy this file to `set_env.sh`, populate the variables, and then source it (`source set_env.sh`) in their shell before running other scripts.

### 4.2 `scripts/common_utils.sh`
- **Purpose:** Contains common shell functions for other scripts.
- **Type:** Utility Script
- **Language:** Shell (Bash)
- **Functions:**
    1.  `log_info()`:
        -   Parameters: `message` (string)
        -   Logic: Prints the message to STDOUT, prefixed with a timestamp (e.g., `YYYY-MM-DD HH:MM:SS INFO:`) and "INFO: ".
        -   Example: `log_info "Starting script..."`
    2.  `log_error()`:
        -   Parameters: `message` (string)
        -   Logic: Prints the message to STDERR, prefixed with a timestamp (e.g., `YYYY-MM-DD HH:MM:SS ERROR:`) and "ERROR: ".
        -   Example: `log_error "Failed to create bucket."`
    3.  `check_env_vars()`:
        -   Parameters: One or more environment variable names (strings).
        -   Logic:
            -   Iterates through the provided variable names.
            -   For each variable name, checks if it is set and non-empty.
            -   If a variable is not set or is empty, calls `log_error` with an appropriate message and exits the script with status 1.
        -   Example: `check_env_vars "MINIO_ALIAS_NAME" "MC_HOST_${MINIO_ALIAS_NAME}_URL"`
    4.  `check_mc_command()`:
        -   Parameters: None
        -   Logic: Checks if the `mc` command is available in the system's PATH. If not, logs an error and exits.
    5.  Initial Block:
        -   `set -e`: Exit immediately if a command exits with a non-zero status.
        -   `set -o pipefail`: The return value of a pipeline is the status of the last command to exit with a non-zero status, or zero if no command exited with a non-zero status.
        -   Check if `set_env.sh` exists in the parent directory. If yes, source it. If not, print a warning that environment variables might not be set.
        -   Call `check_mc_command`.
- **Usage:** Other shell scripts will source this file: `source ../common_utils.sh` (adjust path as needed).

### 4.3 `scripts/initial_setup/create_buckets.sh`
- **Purpose:** Creates initial MinIO buckets.
- **Requirement Mapping:** Section 7.4.1
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh` (sourced by `common_utils.sh`)
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Define an array of bucket names as per SRS 7.4.1:
        bash
        BUCKETS=(
            "user-uploads"
            "generated-creatives"
            "brand-kits"
            "templates"
            "system-assets"
            "model-artifacts"
            "database-backups" # Added for backups
            "logs-archive" # Added for log archives
        )
        
    4.  Loop through the `BUCKETS` array:
        a.  For each `bucket_name`:
            i.  `log_info "Checking if bucket '${MINIO_ALIAS_NAME}/${bucket_name}' exists..."`
            ii. If `mc stat "${MINIO_ALIAS_NAME}/${bucket_name}" >/dev/null 2>&1`; then
                `log_info "Bucket '${MINIO_ALIAS_NAME}/${bucket_name}' already exists."`
            iii. Else
                `log_info "Creating bucket '${MINIO_ALIAS_NAME}/${bucket_name}'..."`
                If `mc mb "${MINIO_ALIAS_NAME}/${bucket_name}"`; then
                    `log_info "Bucket '${MINIO_ALIAS_NAME}/${bucket_name}' created successfully."`
                Else
                    `log_error "Failed to create bucket '${MINIO_ALIAS_NAME}/${bucket_name}'. Exiting."`
                    `exit 1`
                fi
            fi
    5. `log_info "Bucket creation process completed."`

### 4.4 `scripts/initial_setup/set_initial_bucket_policies.sh`
- **Purpose:** Applies initial default access policies to buckets.
- **Requirement Mapping:** Section 7.4.1, NFR-006
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Define policies for buckets. Example (actual policies depend on application needs):
        bash
        # Bucket: Policy Type (none, download, upload, public)
        declare -A BUCKET_POLICIES
        BUCKET_POLICIES["user-uploads"]="private" # Or 'upload' if service accounts write
        BUCKET_POLICIES["generated-creatives"]="private" # Or 'download' if direct links needed
        BUCKET_POLICIES["brand-kits"]="private"
        BUCKET_POLICIES["templates"]="download" # System templates might be publicly readable
        BUCKET_POLICIES["system-assets"]="download" # Or 'public' for general assets like PWA icons
        BUCKET_POLICIES["model-artifacts"]="private"
        BUCKET_POLICIES["database-backups"]="private"
        BUCKET_POLICIES["logs-archive"]="private"
        
    4.  Loop through the `BUCKET_POLICIES` associative array:
        a.  For each `bucket_name` and `policy_type`:
            i.  `log_info "Setting policy '${policy_type}' for bucket '${MINIO_ALIAS_NAME}/${bucket_name}'..."`
            ii. If `mc policy set "${policy_type}" "${MINIO_ALIAS_NAME}/${bucket_name}"`; then
                `log_info "Policy for '${MINIO_ALIAS_NAME}/${bucket_name}' set to '${policy_type}'."`
            iii. Else
                `log_error "Failed to set policy for '${MINIO_ALIAS_NAME}/${bucket_name}'. Check bucket existence and permissions."`
                # Optionally continue or exit based on severity
            fi
    5.  `log_info "Initial bucket policy application completed."`
    *   **Note:** For more complex policies than `mc policy set` simple types, this script would reference policy JSON files (from `config_templates/`) and use `mc policy set-json`.

### 4.5 `scripts/replication/setup_site_replication.sh`
- **Purpose:** Configures MinIO active-active multi-site replication.
- **Requirement Mapping:** NFR-004, CPIO-005, REQ-DA-012
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Input Parameters (via environment variables or command-line arguments):**
    -   `PRIMARY_MINIO_ALIAS`: Alias for the primary MinIO site (already configured in `set_env.sh`).
    -   `REPLICA_SITE_NAME`: A unique name for the replica site.
    -   `REPLICA_ENDPOINT_URL`: Endpoint URL of the replica MinIO site.
    -   `REPLICA_ACCESS_KEY`: Access key for the replica MinIO site.
    -   `REPLICA_SECRET_KEY`: Secret key for the replica MinIO site.
    -   `REPLICATION_BUCKETS`: Comma-separated list of buckets to replicate (optional, if not all buckets).
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Check required input parameters/environment variables.
    3.  `log_info "Setting up site replication from '${PRIMARY_MINIO_ALIAS}' to '${REPLICA_SITE_NAME}'..."`
    4.  Configure the remote site target on the primary alias:
        `mc admin replicate add "${PRIMARY_MINIO_ALIAS}" "${REPLICA_SITE_NAME}" --endpoint "${REPLICA_ENDPOINT_URL}" --access-key "${REPLICA_ACCESS_KEY}" --secret-key "${REPLICA_SECRET_KEY}" --priority 1`
        (Add necessary flags like `--replicate existing-objects` if needed, `--health-check-secs`, etc.)
    5.  Verify replication setup:
        `mc admin replicate info "${PRIMARY_MINIO_ALIAS}" "${REPLICA_SITE_NAME}"`
    6.  If `REPLICATION_BUCKETS` is provided, loop through them and potentially apply bucket-specific replication configurations or verify, though site replication often covers all buckets by default or specific global settings.
        (MinIO's site replication typically replicates all data. Bucket-level replication is a different concept for specific remote targets, usually DR.)
        *   **Clarification:** Site replication (`mc admin replicate add <ALIAS> <REMOTE_ALIAS>`) aims for active-active or active-passive between full sites. Bucket replication (`mc replicate add <ALIAS/BUCKET> ...`) is for replicating specific buckets. This script seems geared towards site replication.
    7.  `log_info "Site replication setup to '${REPLICA_SITE_NAME}' completed. Manual setup on the replica site pointing back to primary may be needed for full active-active."`
    *   **Note:** Full active-active requires reciprocal setup on the replica site. This script handles one direction.

### 4.6 `scripts/replication/setup_bucket_replication_dr.sh`
- **Purpose:** Configures asynchronous bucket replication to a DR site.
- **Requirement Mapping:** NFR-004, CPIO-005, REQ-DA-012
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Input Parameters:**
    -   `SOURCE_BUCKET_PATH`: Full path to source bucket (e.g., `myminio/user-uploads`).
    -   `DR_TARGET_ALIAS`: Alias for the DR MinIO instance (must be pre-configured in `mc`).
    -   `DR_TARGET_BUCKET_NAME`: Name of the bucket on the DR instance.
    -   `REPLICATION_RULE_NAME`: A unique name for the replication rule.
    -   Optional flags: `--replicate delete,delete-marker,existing-objects`, `--priority`, `--tags`, `--storage-class`.
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Check required input parameters.
    3.  `log_info "Setting up bucket replication for '${SOURCE_BUCKET_PATH}' to '${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}'..."`
    4.  Ensure DR target bucket exists on DR_TARGET_ALIAS or create it (requires DR_TARGET_ALIAS to have appropriate credentials):
        `mc stat "${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}" || mc mb "${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}"`
    5.  Add replication rule:
        `mc replicate add "${SOURCE_BUCKET_PATH}" --remote-bucket "arn:aws:s3:::${DR_TARGET_BUCKET_NAME}" --arn "${DR_TARGET_ALIAS}" --rule-name "${REPLICATION_RULE_NAME}" [OPTIONAL_FLAGS]`
        (The `--arn` here refers to the remote target ARN defined via `mc admin replicate add <LOCAL_ALIAS> <REMOTE_ALIAS> --arn ...` if using remote targets, or directly to the DR alias if set up for SQS notifications.)
        *   Alternative: `mc replicate add ${SOURCE_BUCKET_PATH} --remote-bucket "s3://${DR_TARGET_BUCKET_NAME}" --endpoint ${DR_ENDPOINT_URL} --access-key ${DR_ACCESS_KEY} --secret-key ${DR_SECRET_KEY} --region ${DR_REGION_IF_ANY}` if directly configuring.
        *   The preferred method for bucket replication involves setting up a remote target using `mc admin cluster bucket remote add` or `mc mirror --watch` for simpler setups. The `mc replicate add` is more IAM role/ARN focused traditionally. For self-hosted, often using a service account on the target.
        *   Let's assume direct configuration with endpoint if simpler:
          bash
          # Example direct configuration (requires service account on DR target with write perms)
          # Ensure DR_ENDPOINT_URL, DR_ACCESS_KEY, DR_SECRET_KEY are set
          mc replicate add "${SOURCE_BUCKET_PATH}" \
             --remote-bucket "arn:aws:s3:::${DR_TARGET_BUCKET_NAME}" \
             --endpoint "${DR_ENDPOINT_URL_FOR_REPLICATION}" \
             --access-key "${DR_SERVICE_ACCOUNT_ACCESS_KEY}" \
             --secret-key "${DR_SERVICE_ACCOUNT_SECRET_KEY}" \
             --rule-name "${REPLICATION_RULE_NAME}" \
             --replicate "existing-objects,delete" # Example flags
          
    6.  Verify replication status:
        `mc replicate ls "${SOURCE_BUCKET_PATH}"`
        `mc replicate status "${SOURCE_BUCKET_PATH}" --rule-name "${REPLICATION_RULE_NAME}"`
    7.  `log_info "Bucket replication for '${SOURCE_BUCKET_PATH}' to DR site configured."`

### 4.7 `scripts/policies/manage_users_groups.sh`
- **Purpose:** Manages MinIO users and groups.
- **Requirement Mapping:** SEC-006
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Usage:** `./manage_users_groups.sh <ACTION> [ARGUMENTS...]`
    -   Actions:
        -   `add-user <USERNAME> <PASSWORD>`
        -   `remove-user <USERNAME>`
        -   `list-users`
        -   `info-user <USERNAME>`
        -   `add-group <GROUPNAME>`
        -   `remove-group <GROUPNAME>`
        -   `list-groups`
        -   `info-group <GROUPNAME>`
        -   `add-user-to-group <GROUPNAME> <USERNAME>`
        -   `remove-user-from-group <GROUPNAME> <USERNAME>`
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Implement a `case` statement for the first argument (`ACTION`).
    4.  **`add-user`**: `mc admin user add "${MINIO_ALIAS_NAME}" "$2" "$3"`
    5.  **`remove-user`**: `mc admin user rm "${MINIO_ALIAS_NAME}" "$2"`
    6.  **`list-users`**: `mc admin user ls "${MINIO_ALIAS_NAME}"`
    7.  **`info-user`**: `mc admin user info "${MINIO_ALIAS_NAME}" "$2"`
    8.  **`add-group`**: `mc admin group add "${MINIO_ALIAS_NAME}" "$2"`
    9.  **`remove-group`**: `mc admin group rm "${MINIO_ALIAS_NAME}" "$2"`
    10. **`list-groups`**: `mc admin group ls "${MINIO_ALIAS_NAME}"`
    11. **`info-group`**: `mc admin group info "${MINIO_ALIAS_NAME}" "$2"`
    12. **`add-user-to-group`**: `mc admin group add "${MINIO_ALIAS_NAME}" "$2" "$3"`
    13. **`remove-user-from-group`**: `mc admin group rm "${MINIO_ALIAS_NAME}" "$2" "$3"`
    14. Include error handling and logging for each `mc` command.
    15. Provide help/usage instructions if no action or invalid action is given.

### 4.8 `scripts/policies/apply_iam_policy.sh`
- **Purpose:** Applies IAM-like policies to MinIO users or groups.
- **Requirement Mapping:** SEC-006
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`, policy JSON files in `config_templates/`
- **Usage:** `./apply_iam_policy.sh <user|group> <TARGET_NAME> <POLICY_NAME_OR_FILE_PATH>`
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Validate input arguments (type, target name, policy).
    4.  If `POLICY_NAME_OR_FILE_PATH` is a file path:
        a.  Extract policy name from file path (e.g., basename without extension).
        b.  `log_info "Adding policy '${policy_name}' from file '${POLICY_NAME_OR_FILE_PATH}'..."`
        c.  If `mc admin policy add "${MINIO_ALIAS_NAME}" "${policy_name}" "${POLICY_NAME_OR_FILE_PATH}"`; then
            `log_info "Policy '${policy_name}' added."`
        d.  Else
            `log_error "Failed to add policy '${policy_name}'. It might already exist or the file is invalid."`
            # Potentially continue if policy already exists, exit otherwise.
        fi
        Set `policy_to_apply="${policy_name}"`.
    5.  Else (assume it's a predefined policy name):
        Set `policy_to_apply="${POLICY_NAME_OR_FILE_PATH}"`.
    6.  If type is `user`:
        `log_info "Setting policy '${policy_to_apply}' for user '${TARGET_NAME}'..."`
        If `mc admin policy set "${MINIO_ALIAS_NAME}" "${policy_to_apply}" user="${TARGET_NAME}"`; then
            `log_info "Policy set for user '${TARGET_NAME}'."`
        Else
            `log_error "Failed to set policy for user '${TARGET_NAME}'."`
        fi
    7.  Else if type is `group`:
        `log_info "Setting policy '${policy_to_apply}' for group '${TARGET_NAME}'..."`
        If `mc admin policy set "${MINIO_ALIAS_NAME}" "${policy_to_apply}" group="${TARGET_NAME}"`; then
            `log_info "Policy set for group '${TARGET_NAME}'."`
        Else
            `log_error "Failed to set policy for group '${TARGET_NAME}'."`
        fi
    8.  Else: `log_error "Invalid target type. Must be 'user' or 'group'."`, exit 1.

### 4.9 `scripts/policies/set_bucket_lifecycle.sh`
- **Purpose:** Configures bucket lifecycle policies.
- **Requirement Mapping:** Section 7.5
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`, lifecycle policy JSON files in `config_templates/`
- **Usage:** `./set_bucket_lifecycle.sh <BUCKET_NAME> <LIFECYCLE_POLICY_FILE_PATH>`
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Validate input arguments (bucket name, policy file path). Check if policy file exists.
    4.  `log_info "Setting lifecycle policy from '${LIFECYCLE_POLICY_FILE_PATH}' for bucket '${MINIO_ALIAS_NAME}/${BUCKET_NAME}'..."`
    5.  If `mc ilm set "${MINIO_ALIAS_NAME}/${BUCKET_NAME}" "${LIFECYCLE_POLICY_FILE_PATH}"`; then
        `log_info "Lifecycle policy applied successfully to '${MINIO_ALIAS_NAME}/${BUCKET_NAME}'."`
        `mc ilm ls "${MINIO_ALIAS_NAME}/${BUCKET_NAME}"` # Display current policy
    6.  Else
        `log_error "Failed to apply lifecycle policy to '${MINIO_ALIAS_NAME}/${BUCKET_NAME}'."`
        `exit 1`
    fi

### 4.10 `scripts/admin/check_cluster_health.sh`
- **Purpose:** Checks MinIO cluster health.
- **Requirement Mapping:** DEP-001
- **Type:** Operational Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  `log_info "Fetching MinIO cluster information for alias '${MINIO_ALIAS_NAME}'..."`
    4.  Execute `mc admin info "${MINIO_ALIAS_NAME}"`. Log output.
    5.  `log_info "Checking for any healing activity..."`
    6.  Execute `mc admin heal "${MINIO_ALIAS_NAME}"`. Log output.
    7.  (Optional) Execute `mc admin top locks "${MINIO_ALIAS_NAME}"` if lock contention is a common concern.
    8.  `log_info "Cluster health check completed."`
    *   No complex parsing, script primarily displays `mc admin` output for manual review or basic CI pass/fail based on command exit codes.

### 4.11 `scripts/admin/manage_kms_kek.sh`
- **Purpose:** Manages KEKs for server-side encryption with external KMS.
- **Requirement Mapping:** SEC-003, REQ-DA-010
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Usage:** `./manage_kms_kek.sh <ACTION> [ARGUMENTS...]`
    -   Actions:
        -   `create <KEK_NAME>`
        -   `status <KEK_NAME>`
        -   `list`
        -   (Import/Export are more advanced and might require specific KMS provider interactions not coverable by generic `mc` script here, usually `mc admin kms key import/export` is for transferring master KEKs which is very sensitive.)
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Implement a `case` statement for the first argument (`ACTION`).
    4.  **`create`**:
        `log_info "Creating KEK '${2}' on '${MINIO_ALIAS_NAME}'..."`
        If `mc admin kms key create "${MINIO_ALIAS_NAME}" --key-id "$2"`; then
            `log_info "KEK '$2' created successfully."`
        Else
            `log_error "Failed to create KEK '$2'."`
        fi
    5.  **`status`**:
        `log_info "Getting status for KEK '${2}' on '${MINIO_ALIAS_NAME}'..."`
        `mc admin kms key status "${MINIO_ALIAS_NAME}" --key-id "$2"`
    6.  **`list`**:
        `log_info "Listing KEKs on '${MINIO_ALIAS_NAME}'..."`
        `mc admin kms key ls "${MINIO_ALIAS_NAME}"`
    7.  Provide help/usage instructions if no action or invalid action is given.
    8.  Emphasize that MinIO server must be pre-configured to use an external KMS (e.g., HashiCorp Vault) for these commands to be effective.

### 4.12 `scripts/admin/configure_prometheus_endpoint.sh`
- **Purpose:** Configures MinIO's Prometheus metrics endpoint.
- **Requirement Mapping:** DEP-005
- **Type:** Configuration Script
- **Language:** Shell (Bash)
- **Dependencies:** `scripts/common_utils.sh`, `set_env.sh`
- **Usage:** `./configure_prometheus_endpoint.sh [JOB_NAME]` (Job name is optional, defaults to 'minio-job')
- **Logic Description:**
    1.  Source `common_utils.sh`.
    2.  Call `check_env_vars "MINIO_ALIAS_NAME"`.
    3.  Set `JOB_NAME` to `$1` or default to `minio-job`.
    4.  `log_info "Generating Prometheus scrape configuration for job '${JOB_NAME}' on alias '${MINIO_ALIAS_NAME}'..."`
    5.  Execute `mc admin prometheus generate "${MINIO_ALIAS_NAME}" "${JOB_NAME}"`. This command outputs the Prometheus scrape config.
    6.  `log_info "Prometheus configuration generated. Add this to your prometheus.yml:"`
    7.  Print the output of the command directly.
    8.  `log_info "Ensure Prometheus has network access to MinIO's metrics endpoint and appropriate credentials if MinIO requires authentication for metrics."`
    *   **Note:** This script doesn't *set* anything on MinIO directly for Prometheus scraping itself, but rather generates the config *for* Prometheus. MinIO exposes metrics by default if Prometheus support is enabled in its config. The `mc admin prometheus generate` command is primarily for creating the scrape job definition for Prometheus.
    *   This might also involve setting a specific service account or policy in MinIO to allow Prometheus to scrape if MinIO is secured. This part could be added if needed using `manage_users_groups.sh` and `apply_iam_policy.sh` concepts.

### 4.13 `python_utils/minio_operations.py`
- **Purpose:** Python utilities using MinIO SDK for advanced operations.
- **Requirement Mapping:** NFR-004, Section 7.4.1
- **Type:** Utility Script
- **Language:** Python 3.11.9
- **Dependencies:** `minio` SDK (see `requirements.txt`)
- **Core Logic:**
    -   Import `Minio` from `minio` and other necessary modules (`os`, `json`, `sys`).
    -   Implement functions as defined in the file structure:
        1.  **`connect_client(endpoint, access_key, secret_key, secure=True)`**:
            -   Takes endpoint, access_key, secret_key, and secure flag.
            -   Instantiates and returns a `Minio` client object.
            -   Includes error handling for connection issues.
        2.  **`create_bucket_if_not_exists(client: Minio, bucket_name: str)`**:
            -   Uses `client.bucket_exists(bucket_name)`.
            -   If not exists, uses `client.make_bucket(bucket_name)`.
            -   Logs actions and returns True if created/existed, False on error.
        3.  **`set_complex_bucket_policy(client: Minio, bucket_name: str, policy_document_str: str)`**:
            -   Takes a Minio client, bucket name, and a policy document as a JSON string.
            -   Uses `client.set_bucket_policy(bucket_name, policy_document_str)`.
            -   Logs success or errors.
        4.  **`generate_replication_status_report(client: Minio, bucket_name: str)`**:
            -   This is a more complex operation. MinIO SDK might not directly provide a high-level "replication status report" in a simple call. This function might need to:
                -   List replication rules using `client.get_bucket_replication(bucket_name)`.
                -   For each rule, interpret its status. True replication status often requires checking both source and target, and potentially metrics if available.
                -   This function will be a best-effort interpretation or rely on specific MinIO extensions if they exist in the SDK for detailed status.
                -   The primary goal is to demonstrate SDK usage for configuration and information retrieval.
            -   Returns a dictionary summarizing the findings.
    -   Consider a main block `if __name__ == "__main__":` for example usage or CLI interface using `argparse` if this script is to be directly executable for certain tasks.
    -   Environment variables (e.g., `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`) should be the primary way to get credentials, with arguments as fallbacks.

### 4.14 `python_utils/requirements.txt`
- **Purpose:** Lists Python dependencies.
- **Type:** Dependency File
- **Content:**
    
    minio>=7.1.0  # Or latest stable version
    # Add other dependencies if any, e.g., python-dotenv for .env file support
    

### 4.15 `config_templates/iam_policy_example.json`
- **Purpose:** Example IAM policy JSON template.
- **Requirement Mapping:** SEC-006
- **Type:** Configuration Template
- **Language:** JSON
- **Content Example:**
    json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::examplebucket/*",
                    "arn:aws:s3:::examplebucket"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject"
                ],
                "Resource": [
                    "arn:aws:s3:::examplebucket/uploads/*"
                ]
            }
        ]
    }
    
    -   Include comments in the SDS (not in the JSON itself) that users should replace `examplebucket` and customize actions/resources.

### 4.16 `config_templates/lifecycle_policy_example.json`
- **Purpose:** Example bucket lifecycle policy JSON template.
- **Requirement Mapping:** Section 7.5
- **Type:** Configuration Template
- **Language:** JSON
- **Content Example (for `mc ilm set` which expects the rule set, not the full XML):**
    json
    {
        "Rules": [
            {
                "ID": "ExpireOldSamplesRule",
                "Status": "Enabled",
                "Filter": {
                    "Prefix": "samples/"
                },
                "Expiration": {
                    "Days": 30
                }
            },
            {
                "ID": "DeleteIncompleteUploadsAfter7Days",
                "Status": "Enabled",
                "AbortIncompleteMultipartUpload": {
                    "DaysAfterInitiation": 7
                }
            }
        ]
    }
    
    -   MinIO `mc ilm set` typically uses an XML format if directly setting the `lifecycle.xml`. However, if scripting `mc ilm import/export`, it might handle JSON. The `mc ilm rule add` commands are more granular.
    -   If `mc ilm set BUCKET LIFECYCLE.json` is the target, the JSON format might need to be compatible with what MinIO server expects internally for its `set-bucket-lifecycle` API, which is XML.
    -   **Revisiting `mc ilm set`:** The `mc ilm set` command actually expects an XML file. So, this should be `lifecycle_policy_example.xml`.
    -   Alternative: Use `mc ilm rule add ...` for each rule, which might be more script-friendly than managing a full XML. If using `mc ilm rule add`, then a JSON template isn't directly used by `mc`, but could serve as a specification for a script that *generates* the `mc ilm rule add` commands.
    -   **Decision:** For simplicity with `mc ilm set`, this should be an XML template or the script `set_bucket_lifecycle.sh` should be more complex to construct XML or use individual rule commands. Let's assume an XML template for `mc ilm set`.

### 4.16 (Revised) `config_templates/lifecycle_policy_example.xml`
- **Purpose:** Example bucket lifecycle policy XML template.
- **Requirement Mapping:** Section 7.5
- **Type:** Configuration Template
- **Language:** XML
- **Content Example:**
    xml
    <LifecycleConfiguration>
        <Rule>
            <ID>ExpireOldSamplesRule</ID>
            <Status>Enabled</Status>
            <Filter>
                <Prefix>samples/</Prefix>
            </Filter>
            <Expiration>
                <Days>30</Days>
            </Expiration>
        </Rule>
        <Rule>
            <ID>DeleteIncompleteUploadsAfter7Days</ID>
            <Status>Enabled</Status>
            <AbortIncompleteMultipartUpload>
                <DaysAfterInitiation>7</DaysAfterInitiation>
            </AbortIncompleteMultipartUpload>
        </Rule>
    </LifecycleConfiguration>
    
    -   **Note for `set_bucket_lifecycle.sh`:** It should now expect an XML file path.

## 5. General Scripting Conventions
- All shell scripts should start with `#!/bin/bash`.
- Use `set -e` and `set -o pipefail` for robust error handling in shell scripts.
- Variables in shell scripts should be `${VAR_NAME}`.
- All scripts should provide a way to display help/usage instructions (e.g., if `-h` or `--help` is passed, or if incorrect arguments are provided).
- Python scripts should follow PEP 8.
- Logging should be consistent using `log_info` and `log_error` from `common_utils.sh`.

## 6. Future Considerations (Not for immediate implementation but good to note)
- **Idempotency enhancements:** While aimed for, rigorously testing idempotency for all scenarios, especially involving `mc admin` commands that modify state, is crucial.
- **Transactional Semantics:** MinIO configuration changes are generally atomic per command, but a sequence of commands in a script is not inherently transactional. Scripts should be designed to be re-runnable, or provide clear guidance on manual steps if a partial failure occurs.
- **Integration with Ansible:** While these are standalone scripts, they could be wrapped or called by Ansible playbooks for higher-level orchestration. The `set_env.sh` mechanism would be replaced by Ansible's variable and secret management in such a scenario.

This detailed design specification provides a solid foundation for generating the scripts and configurations for the `CreativeFlow.MinIO.Configuration` repository.