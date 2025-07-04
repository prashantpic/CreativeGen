# Software Design Specification: CreativeFlow.MinIOObjectStorage

## 1. Introduction

### 1.1 Purpose
This document specifies the design for the `CreativeFlow.MinIOObjectStorage` repository. This repository is responsible for providing the configuration files, IAM policies, and management scripts necessary to set up, configure, and manage the MinIO S3-compatible object storage cluster for the CreativeFlow AI platform. MinIO serves as the primary storage solution for unstructured data, including user assets, AI-generated creatives, brand elements, system assets, and AI model artifacts.

### 1.2 Scope
The scope of this specification includes:
*   Configuration details for MinIO server nodes (distributed mode).
*   Standard bucket definitions, versioning, and initial policies.
*   MinIO Client (mc) alias configurations.
*   Base IAM policy templates for bucket access control.
*   Python and Shell scripts for automating:
    *   Bucket creation and policy application.
    *   Configuration of site and bucket replication for High Availability (HA) and Disaster Recovery (DR).
    *   Monitoring of replication status.
*   Utility scripts for shared functionalities.

This document does *not* cover the OS-level installation of MinIO server binaries, network configuration, or the provisioning of underlying server infrastructure, which are assumed to be handled by broader infrastructure automation (e.g., Ansible scripts in the `Core Platform Infrastructure & Operations` repository).

### 1.3 Definitions, Acronyms, and Abbreviations
*   **MinIO**: High-performance, S3-compatible object storage.
*   **S3**: Amazon Simple Storage Service.
*   **mc**: MinIO Client command-line tool.
*   **IAM**: Identity and Access Management.
*   **JSON**: JavaScript Object Notation.
*   **Env**: Environment variable file.
*   **HA**: High Availability.
*   **DR**: Disaster Recovery.
*   **AZ**: Availability Zone.
*   **CDN**: Content Delivery Network.
*   **ETL**: Extract, Transform, Load.
*   **RPO**: Recovery Point Objective.
*   **RTO**: Recovery Time Objective.
*   **IaC**: Infrastructure as Code.
*   **SDK**: Software Development Kit.

## 2. System Overview
The MinIO object storage cluster is a critical data persistence component within the CreativeFlow AI platform. It provides scalable, durable, and highly available storage for all unstructured data. Key responsibilities include:
*   Storing user-uploaded assets (images, videos, source files).
*   Storing AI-generated creatives (both low-resolution samples and high-resolution final outputs).
*   Storing brand kit assets (logos, custom fonts).
*   Storing system-wide assets (e.g., public templates, stock icons).
*   Storing custom AI model artifacts for the MLOps pipeline.

The cluster will be deployed in a distributed mode across multiple self-hosted servers (as per DEP-001) to ensure scalability and fault tolerance. Data replication strategies will be implemented to provide HA within local AZs and DR capabilities to a geographically separate site (NFR-004). Access to data will be controlled via S3-compatible APIs and IAM policies.

## 3. Design Considerations

### 3.1 Scalability
*   **Distributed Mode**: MinIO will be deployed in distributed mode, allowing it to pool multiple drives/servers into a single object storage cluster. This inherently supports horizontal scaling by adding more server nodes and drives.
*   **Bucket Organization**: A well-defined bucket structure (Section 7.4.1) allows for logical partitioning of data, which can aid in managing scalability and access patterns.

### 3.2 Durability and High Availability
*   **Erasure Coding**: MinIO's distributed mode utilizes erasure coding to provide protection against drive and node failures. The specific erasure coding setup (e.g., N drives, M parity) will be configured during cluster setup based on DEP-001.
*   **Site Replication (Local AZs)**: As per NFR-004, active-active multi-site replication (or equivalent using bi-directional bucket replication if direct active-active site replication is not feasible for specific configurations) will be configured between MinIO deployments in different local availability zones. This ensures high availability for read/write operations within the primary data center.
*   **Bucket Replication (DR)**: Asynchronous bucket replication will be configured from the primary production cluster(s) to a MinIO cluster at the DR site. This ensures data is available for recovery in case of a primary site disaster.

### 3.3 Security
*   **IAM Policies**: Bucket and object access will be controlled via S3 IAM policies. Base restrictive policies will be defined, and specific permissions will be granted to service accounts and users on a least-privilege basis.
*   **Encryption**: MinIO supports server-side encryption (SSE-S3, SSE-C). While data encryption at rest is mentioned in REQ-DA-009 as a system-wide requirement, this repository focuses on bucket-level policies and assumes MinIO's internal encryption mechanisms are leveraged. Configuration for specific encryption keys or KMS integration is outside the scope of these config files but should be considered at the MinIO server setup level.
*   **Network Security**: Network access to MinIO servers (ports 9000, 9001 by default) will be restricted by firewalls. Communication should ideally be over TLS.
*   **Credentials Management**: Root credentials (`MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`) for MinIO servers will be managed securely using HashiCorp Vault or Ansible Vault, not stored in plaintext configuration files. The `.env` file will use placeholders like `_FILE` to indicate sourcing from secret files.

### 3.4 Manageability
*   **Configuration as Code**: All bucket definitions, policies, and alias configurations are defined in JSON files, promoting IaC principles.
*   **Automation Scripts**: Python scripts utilizing the MinIO SDK and shell scripts (for MinIO Client `mc`) will automate common management tasks.
*   **Monitoring**: Scripts for monitoring replication status are included. Integration with a broader monitoring system (e.g., Prometheus via MinIO's Prometheus endpoint) is expected at the infrastructure level.

## 4. Configuration Specifications

### 4.1 `config/minio_cluster_vars.env`
*   **Purpose**: Template for essential MinIO server environment variables for distributed cluster operation.
*   **Format**: Key-value pairs.
*   **Key Variables**:
    *   `MINIO_ROOT_USER_FILE`: Path to file containing the root user name.
        *   *Example*: `/run/secrets/minio_root_user`
    *   `MINIO_ROOT_PASSWORD_FILE`: Path to file containing the root user password.
        *   *Example*: `/run/secrets/minio_root_password`
    *   `MINIO_VOLUMES`: Specifies the storage locations (disks/paths) on each server for MinIO to use.
        *   *Example*: `"http://minio1.creativeflow.local/mnt/disk{1...4}/minio_data http://minio2.creativeflow.local/mnt/disk{1...4}/minio_data ..."` (up to the number of servers as per DEP-001)
    *   `MINIO_SERVER_URLS` (Optional, for older MinIO versions or specific proxy setups; modern MinIO infers this from `MINIO_VOLUMES` or command line args for distributed mode start): List of MinIO server URLs in the cluster.
    *   `MINIO_REGION`: The default region for the MinIO cluster.
        *   *Example*: `us-east-1`
    *   `MINIO_STORAGE_CLASS_STANDARD`: Standard storage class name (usually `STANDARD`).
    *   `MINIO_STORAGE_CLASS_RRS`: Reduced Redundancy Storage class name (if used, e.g., `REDUCED_REDUNDANCY`).
    *   `MINIO_PROMETHEUS_AUTH_TYPE`: Set to `public` or `jwt` for Prometheus metrics endpoint.
    *   `MINIO_PROMETHEUS_URL`: URL for Prometheus endpoint (e.g., `console`).
    *   `MINIO_OPTS`: Additional MinIO server options if needed.
*   **Notes**: Actual secrets (root user/password) will be mounted from a secure vault (e.g., HashiCorp Vault) at runtime by the server provisioning system (e.g., Ansible).

### 4.2 `config/buckets_definition.json`
*   **Purpose**: Declaratively define MinIO buckets for the platform.
*   **Format**: JSON array of objects.
*   **Object Structure**:
    json
    [
      {
        "name": "bucket-name", // e.g., "users", "generations-samples", "generations-final", "brand-kits", "system-assets-public", "ai-models-custom", "platform-backups-db"
        "versioning": true, // or false
        "objectLocking": false, // or true, if WORM compliance is needed for specific buckets (e.g., audit logs if stored here, not typically primary use)
        "defaultPolicyFile": "policies/policy-file-name.json" // Optional: path relative to the repository root
      }
      // ... more bucket definitions
    ]
    
*   **Required Buckets (Based on SRS Section 7.4.1)**:
    *   `users/user_id/profile_pictures/`: For profile pictures.
    *   `users/user_id/uploaded_assets/`: For general user-uploaded source assets.
    *   `workbenches/workbench_id/projects/project_id/input_assets/`: Project-specific input assets.
    *   `generations/user_id/generation_id/samples/`: Low-resolution AI-generated samples.
    *   `generations/user_id/generation_id/final/`: High-resolution final AI-generated assets.
    *   `generations/user_id/generation_id/versions/`: Versions of generated assets.
    *   `brand_kits/user_id_or_team_id/brand_kit_id/logos/`: Brand kit logos.
    *   `brand_kits/user_id_or_team_id/brand_kit_id/fonts/`: Brand kit custom fonts.
    *   `templates/system/category/template_id/`: System-provided templates.
    *   `templates/user_id/private/template_id/`: User-saved private templates.
    *   `system_assets/public/icons/`: Publicly accessible system icons.
    *   `system_assets/public/stock_images/`: Publicly accessible stock images.
    *   `ai_models/custom/model_id/version_id/`: Custom AI model artifacts.
    *   `platform_backups/database/`: For storing database backups.
    *   `platform_backups/minio_metadata/`: For MinIO metadata backups (if applicable).
    *   `logs/application/`: For application log archives (optional, if ELK/Loki doesn't cover long-term archival).

    The `buckets_definition.json` will define the top-level buckets (e.g., `users`, `generations`, `brand-kits`, etc.). The script creating these buckets will ensure these names are used. The folder structure within buckets is typically managed by application logic when objects are put.

### 4.3 `config/mc_aliases.json`
*   **Purpose**: Standardize MinIO Client (mc) alias configurations.
*   **Format**: JSON object where keys are alias names.
*   **Alias Object Structure**:
    json
    {
      "primary_cluster": {
        "url": "https://minio.creativeflow.local", // Primary cluster endpoint
        "accessKey": "MINIO_ACCESS_KEY_PLACEHOLDER", // Placeholder, actual key managed by vault
        "secretKey": "MINIO_SECRET_KEY_PLACEHOLDER", // Placeholder
        "api": "S3v4",
        "path": "auto"
      },
      "dr_cluster": {
        "url": "https://minio-dr.creativeflow.local", // DR cluster endpoint
        "accessKey": "DR_MINIO_ACCESS_KEY_PLACEHOLDER",
        "secretKey": "DR_MINIO_SECRET_KEY_PLACEHOLDER",
        "api": "S3v4",
        "path": "auto"
      }
      // ... other aliases as needed (e.g., for local AZ sites if they have distinct endpoints before LB)
    }
    
*   **Notes**: Access keys and secret keys are placeholders. Scripts or users will need to configure `mc` with actual credentials retrieved from a vault.

### 4.4 `policies/base_private_bucket_policy.json`
*   **Purpose**: Default restrictive policy for private buckets.
*   **Format**: AWS S3-style bucket policy JSON.
*   **Logic**:
    *   Deny all public access (`"Effect": "Deny", "Principal": "*"` for most actions).
    *   Allow specific actions (e.g., `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket`) for predefined MinIO users/groups or service account ARNs representing application services.
    *   Uses placeholders for `{{BUCKET_NAME}}` and `{{SERVICE_ACCOUNT_ARN_LIST}}` or `{{USER_GROUP_LIST}}` which scripts will replace.
    json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Deny",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": [
            "arn:aws:s3:::{{BUCKET_NAME}}",
            "arn:aws:s3:::{{BUCKET_NAME}}/*"
          ],
          "Condition": {
            "StringNotEqualsIfExists": {
              "aws:PrincipalArn": [
                "{{ADMIN_USER_ARN_PLACEHOLDER}}" // Example: an admin user/role
                // "{{SERVICE_ACCOUNT_ARN_PLACEHOLDER_1}}",
                // "{{SERVICE_ACCOUNT_ARN_PLACEHOLDER_2}}"
              ]
            },
            "BoolIfExists": {
                "aws:SecureTransport": "false" // Optional: enforce HTTPS
            }
          }
        }
        // Add Allow statements for specific service accounts or user groups
        // e.g., allow specific service account for creative-management-service to PutObject
        // {
        //   "Effect": "Allow",
        //   "Principal": { "AWS": ["{{SERVICE_ACCOUNT_ARN_CREATIVE_SVC}}"] },
        //   "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
        //   "Resource": "arn:aws:s3:::{{BUCKET_NAME}}/*"
        // },
        // {
        //   "Effect": "Allow",
        //   "Principal": { "AWS": ["{{SERVICE_ACCOUNT_ARN_CREATIVE_SVC}}"] },
        //   "Action": "s3:ListBucket",
        //   "Resource": "arn:aws:s3:::{{BUCKET_NAME}}"
        // }
      ]
    }
    

### 4.5 `policies/public_read_bucket_policy.json`
*   **Purpose**: Policy for buckets or paths needing public read-only access.
*   **Format**: AWS S3-style bucket policy JSON.
*   **Logic**:
    *   Allow `s3:GetObject` for `Principal: "*"` on specific resource paths (e.g., `arn:aws:s3:::{{BUCKET_NAME}}/public/*`).
    *   All other actions (e.g., `s3:PutObject`, `s3:DeleteObject`) should be restricted to admin principals or specific service accounts.
    json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::{{BUCKET_NAME}}/public/*" // Example for a 'public' prefix
        }
        // Potentially other statements to restrict write access to admins
      ]
    }
    

## 5. Script Specifications

### 5.1 `scripts/common_utils.py`
*   **Purpose**: Reusable utility functions for Python-based MinIO management scripts.
*   **Language**: Python 3.11.9
*   **Dependencies**: `minio` (MinIO Python SDK), `json`, `logging`, `os`, `argparse`.
*   **Functions**:
    *   `setup_logging(log_level=logging.INFO) -> logging.Logger`:
        *   **Logic**: Configures a standardized logger (console output, basic formatting including timestamp, level, message).
        *   **Returns**: Configured logger instance.
    *   `load_json_config(file_path: str) -> dict`:
        *   **Logic**: Reads and parses a JSON file. Handles file not found and JSON parsing errors.
        *   **Returns**: Dictionary representation of the JSON content.
        *   **Error Handling**: Raises `FileNotFoundError` or `json.JSONDecodeError`.
    *   `get_minio_credentials_from_env(alias_name_prefix: str) -> tuple[str, str, str]`:
        *   **Logic**: Reads MinIO endpoint URL, access key, and secret key from environment variables prefixed with `alias_name_prefix` (e.g., `PRIMARY_MINIO_URL`, `PRIMARY_MINIO_ACCESS_KEY`, `PRIMARY_MINIO_SECRET_KEY`).
        *   **Returns**: Tuple (endpoint_url, access_key, secret_key).
        *   **Error Handling**: Raises `ValueError` if required environment variables are not set.
    *   `initialize_minio_client(endpoint_url: str, access_key: str, secret_key: str, secure: bool = True) -> Minio`:
        *   **Logic**: Initializes and returns a MinIO SDK client instance using provided credentials and endpoint.
        *   **Returns**: `Minio` client object.
        *   **Error Handling**: May raise exceptions from the MinIO SDK if connection fails.
    *   `execute_mc_command(command: list[str], timeout_seconds: int = 300) -> tuple[int, str, str]`:
        *   **Logic**: Executes an `mc` command-line instruction using `subprocess.run`. Captures stdout and stderr.
        *   **Parameters**: `command` is a list of command arguments (e.g., `['mc', 'admin', 'replicate', 'status', 'myalias/mybucket']`).
        *   **Returns**: Tuple (return_code, stdout_str, stderr_str).
        *   **Error Handling**: Raises `subprocess.TimeoutExpired` if command exceeds timeout. Logs errors.

### 5.2 `scripts/cluster_management/initialize_minio_distributed.sh`
*   **Purpose**: Helper script to construct and display the command for starting MinIO servers in distributed mode.
*   **Language**: Shell (Bash 5.2.15)
*   **Dependencies**: `config/minio_cluster_vars.env` must exist and be sourced.
*   **Logic**:
    1.  Source `config/minio_cluster_vars.env`.
    2.  Validate that `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`, and `MINIO_VOLUMES` are set. Exit with error if not.
    3.  Construct the `minio server` command.
        *   Example command structure: `minio server --console-address ":9001" $MINIO_VOLUMES`
        *   The `MINIO_VOLUMES` variable should contain the space-separated list of all server endpoints and their respective drive paths for the distributed set, e.g., `"http://server1/mnt/disk{1...X} http://server2/mnt/disk{1...X} ..."`
    4.  Echo the constructed command to stdout.
    5.  Add a note that this command needs to be run on each MinIO server node, typically managed by a service manager like systemd, configured via Ansible.
*   **Error Handling**: Basic checks for required environment variables.

### 5.3 `scripts/bucket_management/create_buckets.py`
*   **Purpose**: Automate creation and initial configuration of MinIO buckets.
*   **Language**: Python 3.11.9
*   **Dependencies**: `minio` SDK, `scripts/common_utils.py`, `config/buckets_definition.json`, `config/mc_aliases.json` (or environment variables for credentials).
*   **Core Logic**:
    1.  Setup logging using `common_utils.setup_logging()`.
    2.  Parse command-line arguments (e.g., `--alias` to specify MinIO cluster alias, `--config` for `buckets_definition.json` path).
    3.  Load credentials for the specified alias using `common_utils.get_minio_credentials_from_env()` or by parsing `mc_aliases.json` (less secure for script automation).
    4.  Initialize MinIO client using `common_utils.initialize_minio_client()`.
    5.  Load bucket definitions from `config/buckets_definition.json` using `common_utils.load_json_config()`.
    6.  For each bucket definition in the JSON:
        *   Call `create_bucket_if_not_exists(minio_client, bucket_name, versioning_enabled, object_locking_enabled)`.
*   **Function**: `create_bucket_if_not_exists(client, bucket_name, versioning, object_locking)`:
    *   Check if bucket exists using `client.bucket_exists(bucket_name)`.
    *   If not, create bucket using `client.make_bucket(bucket_name, object_locking=object_locking)`. Log success/failure.
    *   If bucket created successfully or already exists, check and set versioning status:
        *   Get current versioning status: `client.get_bucket_versioning(bucket_name)`.
        *   If `versioning` is true and status is not `Enabled`, set versioning: `client.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))`.
        *   If `versioning` is false and status is not `Suspended` (or Off), set versioning: `client.set_bucket_versioning(bucket_name, VersioningConfig(SUSPENDED))`.
    *   Log actions.
*   **Error Handling**:
    *   Catch exceptions from MinIO SDK calls (e.g., connection errors, permission issues).
    *   Log errors and continue to the next bucket if possible, or exit with an error code.

### 5.4 `scripts/bucket_management/apply_bucket_policies.py`
*   **Purpose**: Automate application of IAM policies to MinIO buckets.
*   **Language**: Python 3.11.9
*   **Dependencies**: `minio` SDK, `scripts/common_utils.py`, `config/buckets_definition.json`, policy JSON files in `policies/`, `config/mc_aliases.json` (or environment variables).
*   **Core Logic**:
    1.  Setup logging.
    2.  Parse command-line arguments (e.g., `--alias`, `--buckets-config`).
    3.  Load credentials and initialize MinIO client.
    4.  Load bucket definitions from `config/buckets_definition.json`.
    5.  For each bucket with a `defaultPolicyFile` defined:
        *   Construct the full path to the policy file.
        *   Load the policy JSON content using `common_utils.load_json_config()`.
        *   Perform placeholder replacement in the policy string (e.g., `{{BUCKET_NAME}}` with actual bucket name).
        *   Call `apply_policy(minio_client, bucket_name, policy_content_str)`.
*   **Function**: `apply_policy(client, bucket_name, policy_str)`:
    *   Set bucket policy using `client.set_bucket_policy(bucket_name, policy_str)`.
    *   Log success/failure.
*   **Error Handling**:
    *   Handle file not found for policy files.
    *   Catch exceptions from MinIO SDK calls.
    *   Log errors.

### 5.5 `scripts/replication_management/setup_site_replication.py`
*   **Purpose**: Configure MinIO site-to-site or bucket replication.
*   **Language**: Python 3.11.9
*   **Dependencies**: `minio` SDK (preferred), `subprocess` (for `mc` as fallback if SDK lacks admin features), `scripts/common_utils.py`, `config/mc_aliases.json` (for target cluster details), a new replication configuration JSON file.
*   **Replication Configuration File (`config/replication_rules.json`) Example**:
    json
    {
      "siteReplications": [ // For active-passive Site Replication (if MinIO supports it directly as "active-active" like)
        {
          "sourceAlias": "primary_cluster_az1", // mc alias of the source site
          "targetAlias": "primary_cluster_az2", // mc alias of the target site for local HA
          "targetName": "local_ha_az2", // Arbitrary name for the target in source's replication config
          "notes": "Bi-directional setup for local AZ HA would require this and its inverse."
        }
      ],
      "bucketReplications": [
        {
          "sourceAlias": "primary_cluster", // mc alias of the source MinIO
          "sourceBucket": "generations-final",
          "targetAlias": "dr_cluster", // mc alias of the DR MinIO
          "targetBucket": "generations-final-dr", // Can be same or different name
          "isAsync": true, // True for DR
          "priority": 1, // Replication rule priority
          "tags": [{"key": "replicate", "value": "true"}], // Optional: replicate objects with specific tags
          "storageClass": "STANDARD" // Optional: target storage class
        },
        // Example for simulating active-active between local AZs via bucket replication
        {
          "sourceAlias": "primary_cluster_az1",
          "sourceBucket": "user-uploads",
          "targetAlias": "primary_cluster_az2",
          "targetBucket": "user-uploads",
          "isAsync": false, // Aim for near-synchronous for local AZs
          "priority": 1
        },
        {
          "sourceAlias": "primary_cluster_az2",
          "sourceBucket": "user-uploads",
          "targetAlias": "primary_cluster_az1",
          "targetBucket": "user-uploads",
          "isAsync": false,
          "priority": 1
        }
      ]
    }
    
*   **Core Logic**:
    1.  Setup logging.
    2.  Parse command-line arguments (e.g., `--replication-config` for `replication_rules.json`).
    3.  Load `replication_rules.json`.
    4.  **For Site Replication (if applicable and directly supported by MinIO for active-active like behavior across AZs)**:
        *   Iterate through `siteReplications`.
        *   For each rule, retrieve credentials for source and target aliases.
        *   Use `mc admin replicate add <SOURCE_ALIAS> <TARGET_ALIAS_WITH_CREDENTIALS_AND_ENDPOINT>` or SDK equivalent.
        *   This part is complex with MinIO site replication usually being active-passive. "Active-active" often refers to application-level or load-balancer strategies with multiple independent MinIO clusters that then use bucket replication. The script should focus on setting up *bucket replication* for both local AZ HA (bi-directional) and DR (uni-directional).
    5.  **For Bucket Replication (Primary Method)**:
        *   Iterate through `bucketReplications`.
        *   For each rule:
            *   Initialize MinIO client for the `sourceAlias`.
            *   Define replication rule configuration (XML or Python dict for SDK). This includes target bucket ARN (which means the target bucket must exist), status (Enabled), priority, filter (tags/prefix), delete marker replication, etc.
            *   The target bucket ARN would be `arn:aws:s3:::<targetBucketName>`. The "site" or endpoint for this target is implied by the `targetAlias`.
            *   Ensure credentials for `targetAlias` are available to the *source* MinIO server for it to replicate. This is often done by setting up service accounts on the target and configuring them on the source MinIO replication settings, or by using `mc admin replicate add <SOURCE_ALIAS>/<SOURCE_BUCKET> <REMOTE_TARGET_ARN_WITH_CREDENTIALS>`. The script might need to use `mc` commands if SDK support for setting up inter-cluster replication credentials is limited.
            *   `client_source.set_bucket_replication(source_bucket, replication_config)`.
        *   Handle logic for `isAsync`: MinIO bucket replication is inherently asynchronous. "Synchronous" or near-synchronous for local AZs would mean ensuring replication lag is minimal and potentially failing writes if replication confirmation isn't received quickly (application-level check, not typically a MinIO config). The `isAsync` flag here would primarily guide monitoring expectations rather than MinIO configuration itself.
*   **Error Handling**: Log detailed errors from SDK/`mc` calls.

### 5.6 `scripts/replication_management/monitor_replication.py`
*   **Purpose**: Monitor status and lag of MinIO replication.
*   **Language**: Python 3.11.9
*   **Dependencies**: `minio` SDK (preferred), `subprocess` (for `mc`), `scripts/common_utils.py`, `config/mc_aliases.json`, `config/replication_rules.json` (to know what to monitor).
*   **Core Logic**:
    1.  Setup logging.
    2.  Parse command-line arguments (e.g., `--replication-config`).
    3.  Load `replication_rules.json` to get source/target bucket pairs.
    4.  For each bucket replication rule:
        *   Initialize MinIO client for the `sourceAlias`.
        *   Attempt to get replication status. The MinIO SDK `get_bucket_replication` returns the configuration, not live status. `mc admin replicate status <ALIAS>/<BUCKET>` provides live status.
        *   Use `common_utils.execute_mc_command(['mc', 'admin', 'replicate', 'status', f'{source_alias}/{source_bucket}'])`.
        *   Parse the output of `mc admin replicate status`. This output typically includes:
            *   `Replication Status`: (e.g., ` آنلاین `)
            *   `Remote Bucket`:
            *   `Bandwidth`:
            *   `Objects`: (pending)
            *   `Size`: (pending)
            *   `Failed Objects`:
        *   Log the parsed status.
        *   Implement logic to check if "Pending Size" or "Failed Objects" exceed predefined thresholds and log warnings/errors or exit with a non-zero code for monitoring system integration.
*   **Error Handling**: Handle errors from `mc` command execution. Handle parsing errors.

### 5.7 `.minio-config.md5sums`
*   **Purpose**: Aid in verifying configuration file integrity.
*   **Format**: Text file. Each line: `<MD5_CHECKSUM>  <RELATIVE_FILE_PATH>`
*   **Usage**:
    *   Generated by a script (potentially a simple shell script using `md5sum`) that calculates checksums for files in `config/` and `policies/`.
    *   Can be used by deployment scripts or manual checks to verify that the deployed configuration files match the intended versions from the repository.
    *   Example content:
        
        d41d8cd98f00b204e9800998ecf8427e  config/minio_cluster_vars.env
        e58f92c5d29a25a69f20d5e5c890944b  config/buckets_definition.json
        ...
        
    *   This file itself should be version-controlled.

## 6. Data Management

### 6.1 Bucket Organization
The MinIO cluster will be organized using a hierarchical structure of buckets and prefixes as detailed in SRS Section 7.4.1. This structure ensures:
*   **Isolation**: Data for different users, projects, and purposes is logically separated.
*   **Security**: Granular access policies can be applied at the bucket or prefix level.
*   **Manageability**: Simplifies data lifecycle management, backups, and replication configurations.
The `scripts/bucket_management/create_buckets.py` script will create the top-level buckets defined in `config/buckets_definition.json`. Application services are responsible for creating objects within these buckets using the specified prefix paths.

### 6.2 Replication Strategy (NFR-004)
*   **Local Availability Zones (HA)**:
    *   Two or more MinIO clusters will be deployed in separate local AZs (e.g., different racks with independent power/network).
    *   Bi-directional bucket replication will be configured between these local AZ MinIO clusters for all critical buckets. This aims to provide an active-active like setup at the application level, though MinIO's bucket replication is asynchronous. The goal is near real-time data consistency between local AZs.
    *   The `setup_site_replication.py` script will manage the configuration of these bi-directional bucket replication rules.
*   **Disaster Recovery (DR)**:
    *   A separate MinIO cluster will be deployed at a geographically distant DR site.
    *   Uni-directional asynchronous bucket replication will be configured from the primary production MinIO cluster(s) to the DR cluster for all critical buckets.
    *   This ensures data is available for recovery in case of a major outage affecting the primary data center, meeting RPO targets.
    *   The `setup_site_replication.py` script will also manage this DR replication setup.
*   **Monitoring**: The `monitor_replication.py` script will be used to track the health and lag of these replication setups.

## 7. Integration Points
*   **Application Services**: Various backend services (e.g., Creative Management Service, User Account & Profile Service, MLOps Platform Service) will interact with MinIO using its S3-compatible API (via MinIO SDKs in their respective languages, primarily Python) for storing and retrieving objects.
*   **Ansible (Infrastructure Management)**: Ansible scripts (from a different repository) will be responsible for:
    *   Provisioning and configuring the MinIO server nodes.
    *   Deploying MinIO server binaries.
    *   Managing MinIO service startup and lifecycle (e.g., using systemd).
    *   Securely injecting root credentials into the MinIO server environments.
    *   Executing the scripts within this `CreativeFlow.MinIOObjectStorage` repository to configure buckets, policies, and replication post-server setup.
*   **Monitoring System (Prometheus/Grafana)**: MinIO exposes a Prometheus metrics endpoint. The central monitoring system will scrape these metrics for dashboards and alerting. This repository does not configure Prometheus itself but ensures MinIO is set up to be scraped.

## 8. Deployment and Management
*   **Initial Cluster Setup**: Handled by Ansible, which will use `scripts/cluster_management/initialize_minio_distributed.sh` (or its logic) to start MinIO servers in distributed mode with environment variables from `config/minio_cluster_vars.env`.
*   **Bucket & Policy Configuration**: After cluster setup, Ansible will execute `scripts/bucket_management/create_buckets.py` and `scripts/bucket_management/apply_bucket_policies.py` to set up the necessary storage structure and access controls.
*   **Replication Setup**: Ansible will execute `scripts/replication_management/setup_site_replication.py` to configure HA and DR replication.
*   **Ongoing Management**:
    *   Monitoring: `scripts/replication_management/monitor_replication.py` can be scheduled (e.g., via cron, integrated into monitoring checks).
    *   Updates: Changes to bucket definitions or policies will be managed by updating the respective JSON files in this repository, version-controlled, and re-applied using the scripts (potentially via CI/CD pipelines that trigger Ansible runs).

## 9. Security Considerations
*   **Credentials**: Root MinIO credentials must be stored and managed securely (e.g., HashiCorp Vault) and injected at runtime. Service accounts with least-privilege access should be used by applications.
*   **Network Access**: MinIO server ports (9000 for API, 9001 for console by default) should be firewalled and only accessible from trusted networks/services. Use TLS for all S3 API communication.
*   **Bucket Policies**: Implement restrictive bucket policies by default. Grant access only to necessary principals (users, groups, service accounts). Regularly review policies.
*   **Public Access**: Limit public access strictly to buckets/objects that genuinely require it (e.g., `system_assets/public/*`). Ensure policies for such buckets only allow `s3:GetObject`.
*   **Versioning and Object Locking**: Enable versioning on critical buckets to protect against accidental deletions or overwrites. Consider object locking for buckets requiring WORM (Write Once Read Many) characteristics if regulatory compliance demands it (e.g., audit logs, though this is not a primary use case for most CreativeFlow buckets).
*   **Audit Logging**: MinIO server access and API calls should be logged. While MinIO provides some logging, integrating these with a central security logging system (SIEM) is recommended at the infrastructure level.

This Software Design Specification provides a detailed plan for the configuration and management scripts within the `CreativeFlow.MinIOObjectStorage` repository, ensuring alignment with the overall system architecture and requirements.