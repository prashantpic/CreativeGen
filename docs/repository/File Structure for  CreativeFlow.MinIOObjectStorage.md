# Specification

# 1. Files

- **Path:** config/minio_cluster_vars.env  
**Description:** Environment variables template for configuring MinIO server nodes in a distributed cluster. Defines placeholders for root credentials, volume paths, server URLs, region, and other essential startup parameters. Actual secrets must be sourced from a secure vault.  
**Template:** Environment File Template  
**Dependency Level:** 0  
**Name:** minio_cluster_vars  
**Type:** Configuration  
**Relative Path:** config/minio_cluster_vars.env  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Cluster Configuration Baseline
    
**Requirement Ids:**
    
    - DEP-001 (Object Storage infrastructure reqs)
    
**Purpose:** To provide a template for essential MinIO server environment variables required for cluster operation.  
**Logic Description:** Contains key-value pairs for MinIO server settings. Variables include MINIO_ROOT_USER_FILE, MINIO_ROOT_PASSWORD_FILE, MINIO_VOLUMES, MINIO_SERVER_URLS (for distributed mode), MINIO_REGION, MINIO_STORAGE_CLASS_STANDARD, MINIO_STORAGE_CLASS_RRS. Comments explain each variable's purpose and how to integrate with secrets management.  
**Documentation:**
    
    - **Summary:** Defines environment variables for MinIO server startup configuration, crucial for setting up a distributed MinIO cluster according to specified server specs.
    
**Namespace:** CreativeFlow.Data.MinIO.Config  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** config/buckets_definition.json  
**Description:** JSON file defining the standard buckets to be created in the MinIO cluster, their initial versioning status, and intended purpose. Used by automation scripts to ensure consistent bucket setup.  
**Template:** JSON Configuration Template  
**Dependency Level:** 0  
**Name:** buckets_definition  
**Type:** Configuration  
**Relative Path:** config/buckets_definition.json  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Bucket Schema Definition
    
**Requirement Ids:**
    
    - Section 7.4.1 (Object Storage Organization)
    
**Purpose:** To declaratively define the set of MinIO buckets required by the CreativeFlow AI platform.  
**Logic Description:** A JSON array of objects. Each object represents a bucket with properties like 'name' (e.g., 'users', 'generations', 'brand-kits', 'system-assets', 'ai-models', 'backups'), 'versioning' (true/false), 'objectLocking' (true/false), 'defaultPolicyFile' (path to a policy JSON in policies/ directory). This structure facilitates programmatic bucket creation and configuration.  
**Documentation:**
    
    - **Summary:** Defines the standard bucket names and their initial configuration settings for the MinIO cluster, ensuring alignment with the platform's object storage organization strategy.
    
**Namespace:** CreativeFlow.Data.MinIO.Config  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** config/mc_aliases.json  
**Description:** Configuration template for MinIO Client (mc) aliases. Defines aliases for connecting to the primary MinIO cluster, DR cluster, and potentially other relevant MinIO endpoints.  
**Template:** JSON Configuration Template  
**Dependency Level:** 0  
**Name:** mc_aliases  
**Type:** Configuration  
**Relative Path:** config/mc_aliases.json  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Client Configuration
    
**Requirement Ids:**
    
    - DEP-001 (Object Storage infrastructure reqs)
    
**Purpose:** To standardize MinIO client alias configurations for easy access to MinIO clusters.  
**Logic Description:** JSON structure defining mc aliases. Each alias includes 'url' (MinIO server endpoint), 'accessKey' (placeholder), 'secretKey' (placeholder), and 'api' (S3v4). This allows scripts and administrators to consistently refer to MinIO instances.  
**Documentation:**
    
    - **Summary:** Provides a template for configuring MinIO Client (mc) aliases, facilitating scripted and manual interactions with various MinIO cluster endpoints.
    
**Namespace:** CreativeFlow.Data.MinIO.Config  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** policies/base_private_bucket_policy.json  
**Description:** A base IAM policy template for private MinIO buckets, denying public access and allowing specific service accounts or user groups access. To be customized per bucket.  
**Template:** JSON Policy Template  
**Dependency Level:** 0  
**Name:** base_private_bucket_policy  
**Type:** Configuration  
**Relative Path:** policies/base_private_bucket_policy.json  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - AccessControl
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Private Bucket Access Policy
    
**Requirement Ids:**
    
    - Section 7.4.1 (Object Storage Organization)
    
**Purpose:** To provide a default restrictive policy for MinIO buckets ensuring data privacy.  
**Logic Description:** Standard AWS S3-style bucket policy JSON. Denies all access by default, then selectively grants permissions (e.g., s3:GetObject, s3:PutObject, s3:ListBucket) to specific MinIO users, groups, or service account ARNs. Placeholders for principals and resource paths included.  
**Documentation:**
    
    - **Summary:** Defines a foundational restrictive access policy for private MinIO buckets, intended to be customized and applied to ensure data security.
    
**Namespace:** CreativeFlow.Data.MinIO.Policies  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** policies/public_read_bucket_policy.json  
**Description:** IAM policy template for MinIO buckets that require public read-only access for certain objects (e.g., system assets, public templates).  
**Template:** JSON Policy Template  
**Dependency Level:** 0  
**Name:** public_read_bucket_policy  
**Type:** Configuration  
**Relative Path:** policies/public_read_bucket_policy.json  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - AccessControl
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Public Read-Only Bucket Access Policy
    
**Requirement Ids:**
    
    - Section 7.4.1 (Object Storage Organization)
    
**Purpose:** To provide a policy for buckets or specific paths within buckets that need to be publicly readable.  
**Logic Description:** S3-style bucket policy JSON. Allows s3:GetObject for Principal '*' on specified resource paths (e.g., bucketname/public/*). All other actions are denied or restricted to specific admin principals. Careful consideration for which paths are made public.  
**Documentation:**
    
    - **Summary:** Defines an access policy allowing public read-only access to specific objects or prefixes within a MinIO bucket, suitable for public-facing assets.
    
**Namespace:** CreativeFlow.Data.MinIO.Policies  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/common_utils.py  
**Description:** Python utility module with common functions used by other MinIO management scripts, such as MinIO client initialization, error handling, logging setup, and configuration loading.  
**Template:** Python Utility Module Template  
**Dependency Level:** 0  
**Name:** common_utils  
**Type:** Utility  
**Relative Path:** scripts/common_utils.py  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - HelperUtilities
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initialize_minio_client  
**Parameters:**
    
    - alias_name: str
    
**Return Type:** Minio  
**Attributes:** public static  
    - **Name:** load_json_config  
**Parameters:**
    
    - file_path: str
    
**Return Type:** dict  
**Attributes:** public static  
    - **Name:** setup_logging  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Shared Scripting Logic
    - MinIO SDK Client Setup
    
**Requirement Ids:**
    
    
**Purpose:** To provide reusable utility functions for MinIO management scripts, promoting code reuse and consistency.  
**Logic Description:** Contains functions for: initializing the MinIO Python SDK client using pre-configured aliases (from mc_aliases.json or environment); robustly loading and parsing JSON configuration files; setting up standardized logging for scripts; common error handling wrappers for MinIO SDK calls.  
**Documentation:**
    
    - **Summary:** A Python module offering shared functionalities like MinIO client initialization, configuration parsing, and logging, used across various management scripts.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Utils  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** scripts/cluster_management/initialize_minio_distributed.sh  
**Description:** Shell script to initialize or verify a MinIO distributed setup based on environment variables defined in 'config/minio_cluster_vars.env'. Assumes MinIO server binaries are installed and servers are provisioned.  
**Template:** Shell Script Template  
**Dependency Level:** 1  
**Name:** initialize_minio_distributed  
**Type:** Script  
**Relative Path:** scripts/cluster_management/initialize_minio_distributed.sh  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagementScript
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Distributed Mode Setup/Verification
    
**Requirement Ids:**
    
    - DEP-001 (Object Storage infrastructure reqs)
    
**Purpose:** To guide/automate the command for starting MinIO in distributed mode on multiple servers as per DEP-001.  
**Logic Description:** Sources 'config/minio_cluster_vars.env'. Constructs the 'minio server' command with appropriate server URLs and volume paths for a distributed setup. Includes checks for required environment variables. This script is more of a template or helper for running the actual MinIO server command, as the server process itself is long-running and managed by systemd/Ansible in production.  
**Documentation:**
    
    - **Summary:** Provides a command template or helper script for initiating MinIO servers in distributed mode, referencing shared environment variables for server addresses and storage volumes.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Cluster  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** scripts/bucket_management/create_buckets.py  
**Description:** Python script to create and configure MinIO buckets based on the 'config/buckets_definition.json' file. Uses MinIO SDK.  
**Template:** Python Script Template  
**Dependency Level:** 1  
**Name:** create_buckets  
**Type:** Script  
**Relative Path:** scripts/bucket_management/create_buckets.py  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagementScript
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** create_bucket_if_not_exists  
**Parameters:**
    
    - minio_client: Minio
    - bucket_name: str
    - versioning_enabled: bool
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Automated Bucket Creation
    - Bucket Versioning Setup
    
**Requirement Ids:**
    
    - Section 7.4.1 (Object Storage Organization)
    
**Purpose:** To automate the creation and initial configuration of all required MinIO buckets.  
**Logic Description:** Imports 'common_utils'. Loads 'config/buckets_definition.json'. Iterates through the bucket definitions. For each bucket, uses the MinIO client (initialized via common_utils) to check if the bucket exists. If not, creates it. Configures versioning if specified. Logs actions and errors.  
**Documentation:**
    
    - **Summary:** Automates the creation of MinIO buckets as defined in 'buckets_definition.json', including setting initial versioning status.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Buckets  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** scripts/bucket_management/apply_bucket_policies.py  
**Description:** Python script to apply IAM policies defined in the 'policies/' directory to their corresponding MinIO buckets. Uses MinIO SDK.  
**Template:** Python Script Template  
**Dependency Level:** 2  
**Name:** apply_bucket_policies  
**Type:** Script  
**Relative Path:** scripts/bucket_management/apply_bucket_policies.py  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagementScript
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** apply_policy  
**Parameters:**
    
    - minio_client: Minio
    - bucket_name: str
    - policy_file_path: str
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Automated Bucket Policy Application
    
**Requirement Ids:**
    
    - Section 7.4.1 (Object Storage Organization)
    
**Purpose:** To automate the application of access control policies to MinIO buckets.  
**Logic Description:** Imports 'common_utils'. Loads 'config/buckets_definition.json' to identify buckets and their associated policy files. For each bucket with a 'defaultPolicyFile' specified, reads the policy JSON from the 'policies/' directory. Uses the MinIO client to set the bucket policy. Logs actions and errors.  
**Documentation:**
    
    - **Summary:** Applies predefined IAM policies from the 'policies/' directory to the corresponding MinIO buckets, ensuring correct access controls.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Buckets  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** scripts/replication_management/setup_site_replication.py  
**Description:** Python script to configure MinIO site replication (active-active multi-site for local AZs, asynchronous bucket replication for DR). Uses MinIO SDK or mc commands.  
**Template:** Python Script Template  
**Dependency Level:** 1  
**Name:** setup_site_replication  
**Type:** Script  
**Relative Path:** scripts/replication_management/setup_site_replication.py  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - ConfigurationManagementScript
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** configure_site_replication_target  
**Parameters:**
    
    - mc_alias_source: str
    - mc_alias_target: str
    - target_name: str
    - endpoint: str
    - access_key: str
    - secret_key: str
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** enable_bucket_replication  
**Parameters:**
    
    - mc_alias_source: str
    - bucket_name: str
    - target_site_name: str
    - is_async: bool
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - MinIO Data Replication Setup
    
**Requirement Ids:**
    
    - NFR-004 (MinIO Replication for fault tolerance)
    
**Purpose:** To automate the configuration of data replication across different MinIO sites/clusters for HA and DR.  
**Logic Description:** Imports 'common_utils'. Reads replication configuration (source/target aliases, bucket lists, replication type) potentially from a dedicated JSON config or environment variables. Uses 'mc admin replicate add' or equivalent SDK calls to set up replication targets and rules for specified buckets. Differentiates between synchronous (within local AZs, if supported directly by MinIO site replication for active-active, or managed via bucket replication rules for active-passive type sync) and asynchronous (to DR) replication. Handles errors and logs configuration steps.  
**Documentation:**
    
    - **Summary:** Configures MinIO site-to-site or bucket replication for high availability and disaster recovery purposes, ensuring data durability.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Replication  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** scripts/replication_management/monitor_replication.py  
**Description:** Python script to monitor the status and lag of MinIO replication configurations. Uses MinIO SDK or mc commands for status.  
**Template:** Python Script Template  
**Dependency Level:** 1  
**Name:** monitor_replication  
**Type:** Script  
**Relative Path:** scripts/replication_management/monitor_replication.py  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - MonitoringScript
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** get_replication_status  
**Parameters:**
    
    - mc_alias: str
    - bucket_name: str
    
**Return Type:** dict  
**Attributes:** private  
    
**Implemented Features:**
    
    - MinIO Replication Monitoring
    
**Requirement Ids:**
    
    - NFR-004 (MinIO Replication for fault tolerance)
    
**Purpose:** To provide visibility into the health and performance of MinIO data replication processes.  
**Logic Description:** Imports 'common_utils'. Connects to the MinIO cluster(s) using configured aliases. Uses 'mc admin replicate status' or SDK equivalents to fetch replication metrics for configured buckets/sites. Parses the output to extract key information like pending replication size, replication speed, and error counts. Can be integrated with monitoring systems to raise alerts on significant lag or failures.  
**Documentation:**
    
    - **Summary:** Checks and reports the status of configured MinIO replication rules, helping to identify potential issues with data synchronization.
    
**Namespace:** CreativeFlow.Data.MinIO.Scripts.Replication  
**Metadata:**
    
    - **Category:** Scripting
    
- **Path:** .minio-config.md5sums  
**Description:** File containing MD5 checksums for critical configuration files to track changes and ensure integrity. This is a convention, not a standard MinIO file.  
**Template:** Checksum File Template  
**Dependency Level:** 2  
**Name:** .minio-config.md5sums  
**Type:** Utility  
**Relative Path:** .minio-config.md5sums  
**Repository Id:** REPO-MINIO-STORAGE-001  
**Pattern Ids:**
    
    - IntegrityCheck
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration Integrity Verification Aid
    
**Requirement Ids:**
    
    
**Purpose:** To help verify the integrity of configuration files deployed or managed by this repository.  
**Logic Description:** A text file where each line contains an MD5 checksum followed by the relative path to a configuration file (e.g., from 'config/' or 'policies/' directories). Scripts can generate or verify these checksums to detect unintended modifications.  
**Documentation:**
    
    - **Summary:** Stores MD5 checksums of critical configuration files to aid in verifying their integrity and detecting unauthorized changes.
    
**Namespace:** CreativeFlow.Data.MinIO  
**Metadata:**
    
    - **Category:** Utility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

