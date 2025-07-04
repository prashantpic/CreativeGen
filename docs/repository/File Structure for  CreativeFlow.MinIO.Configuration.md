# Specification

# 1. Files

- **Path:** set_env.sh.template  
**Description:** Template script for setting environment variables required by other scripts, such as MinIO alias, endpoint URL, access key, and secret key. Users should copy this to set_env.sh and populate with actual values. THIS FILE SHOULD NOT CONTAIN ACTUAL SECRETS.  
**Template:** Shell Script Template  
**Dependency Level:** 0  
**Name:** set_env.sh.template  
**Type:** ConfigurationScript  
**Relative Path:** .  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Environment Configuration Setup
    
**Requirement Ids:**
    
    - DEP-001
    
**Purpose:** Provides a template for users to configure their MinIO client environment for executing the scripts in this repository.  
**Logic Description:** Contains placeholder environment variables for MC_HOST, MC_ACCESS_KEY, MC_SECRET_KEY. Users will source this file after filling in their specific MinIO cluster details. Includes comments guiding the user on how to obtain these values and the importance of not committing the populated set_env.sh file.  
**Documentation:**
    
    - **Summary:** A template file guiding users to set up their shell environment to interact with a target MinIO cluster using the 'mc' client.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** scripts/common_utils.sh  
**Description:** Contains common shell functions used by multiple scripts, such as error handling, logging, and environment variable checks.  
**Template:** Shell Script  
**Dependency Level:** 0  
**Name:** common_utils  
**Type:** UtilityScript  
**Relative Path:** scripts  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** log_info  
**Parameters:**
    
    - message
    
**Return Type:** void  
**Attributes:**   
    - **Name:** log_error  
**Parameters:**
    
    - message
    
**Return Type:** void  
**Attributes:**   
    - **Name:** check_env_vars  
**Parameters:**
    
    - var_names...
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Utility Functions
    - Standardized Logging
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable shell functions to ensure consistency and reduce redundancy in other scripts.  
**Logic Description:** Defines functions for logging messages with timestamps and severity. Includes a function to check if required environment variables (sourced from set_env.sh) are set before a script proceeds. Sources set_env.sh if it exists.  
**Documentation:**
    
    - **Summary:** A library of common utility functions for shell scripts within this repository, aiding in logging, error checking, and environment setup.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** scripts/initial_setup/create_buckets.sh  
**Description:** Script to create the initial set of buckets required by the CreativeFlow AI platform as per SRS Section 7.4.1.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** create_buckets  
**Type:** ConfigurationScript  
**Relative Path:** scripts/initial_setup  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Bucket Creation
    
**Requirement Ids:**
    
    - Section 7.4.1
    
**Purpose:** Automates the creation of predefined MinIO buckets for different data types used by the platform.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Defines an array of bucket names (e.g., user-uploads, generated-creatives, brand-kits, templates, system-assets, model-artifacts). Iterates through the array, using 'mc mb ALIAS/BUCKET_NAME' to create each bucket. Includes error handling and logging for each operation. Checks if bucket already exists before attempting creation.  
**Documentation:**
    
    - **Summary:** Creates the standard set of MinIO buckets (user-uploads, generated-creatives, etc.) required for the CreativeFlow AI platform operation, as defined in SRS 7.4.1.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/initial_setup/set_initial_bucket_policies.sh  
**Description:** Script to apply initial default access policies to the newly created buckets. Policies could be read-only for some, private by default for user data.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** set_initial_bucket_policies  
**Type:** ConfigurationScript  
**Relative Path:** scripts/initial_setup  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Bucket Policy Configuration
    
**Requirement Ids:**
    
    - Section 7.4.1
    - NFR-006
    
**Purpose:** Applies baseline access policies to core MinIO buckets.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Defines policy types (e.g., private, public-read for specific system asset buckets if any). For each relevant bucket created by create_buckets.sh, applies a predefined policy using 'mc policy set POLICY_TYPE ALIAS/BUCKET_NAME'. Policy JSONs can be stored in config_templates/ and referenced, or simple policies like 'private' or 'download' can be used directly.  
**Documentation:**
    
    - **Summary:** Sets initial default access policies (e.g., private, public-read for specific system buckets) on the buckets created by create_buckets.sh.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/replication/setup_site_replication.sh  
**Description:** Script to configure MinIO active-active multi-site replication between local availability zones as per NFR-004, CPIO-005, REQ-DA-012. This assumes multiple MinIO clusters/sites are already deployed.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** setup_site_replication  
**Type:** ConfigurationScript  
**Relative Path:** scripts/replication  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Site Replication Setup
    
**Requirement Ids:**
    
    - NFR-004
    - CPIO-005
    - REQ-DA-012
    
**Purpose:** Configures site replication between different MinIO deployments for high availability within a primary region.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Takes parameters for source alias and target site alias(es)/endpoints/credentials. Uses 'mc admin replicate add/info/ls' commands to configure and verify site-to-site replication. Handles setup of credentials and service accounts required for replication between sites.  
**Documentation:**
    
    - **Summary:** Sets up and verifies MinIO active-active multi-site replication between configured MinIO clusters within local availability zones.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/replication/setup_bucket_replication_dr.sh  
**Description:** Script to configure asynchronous bucket replication to a Disaster Recovery (DR) site as per NFR-004, CPIO-005, REQ-DA-012.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** setup_bucket_replication_dr  
**Type:** ConfigurationScript  
**Relative Path:** scripts/replication  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Bucket Replication to DR
    
**Requirement Ids:**
    
    - NFR-004
    - CPIO-005
    - REQ-DA-012
    
**Purpose:** Configures asynchronous replication for specified buckets to a remote DR MinIO instance.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Takes parameters for source alias/bucket and target DR alias/bucket/credentials. Uses 'mc replicate add/info/ls' commands to configure bucket-level replication rules. Ensures target DR bucket exists or creates it. Handles necessary permissions for replication.  
**Documentation:**
    
    - **Summary:** Sets up and verifies asynchronous bucket replication from primary MinIO buckets to a designated Disaster Recovery (DR) site.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/policies/manage_users_groups.sh  
**Description:** Script to manage MinIO users and groups using 'mc admin user' and 'mc admin group' commands. Allows adding, removing, listing users/groups, and managing group memberships.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** manage_users_groups  
**Type:** ConfigurationScript  
**Relative Path:** scripts/policies  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO User Management
    - MinIO Group Management
    
**Requirement Ids:**
    
    - SEC-006
    
**Purpose:** Provides CLI-based operations for managing users and groups within the MinIO deployment.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Uses a case statement or subcommands (e.g., add-user, remove-user, add-group, add-user-to-group) to wrap 'mc admin user add/remove/list/info <ALIAS> <USER>' and 'mc admin group add/remove/list/info <ALIAS> <GROUP> <USER1> <USER2>...' commands. Parameterizes user names, access keys, secret keys (for creation), and group names.  
**Documentation:**
    
    - **Summary:** Manages MinIO users and groups, including creation, deletion, listing, and membership modifications.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Administration
    
- **Path:** scripts/policies/apply_iam_policy.sh  
**Description:** Script to apply IAM-like policies to MinIO users or groups. Takes a user/group name and a policy JSON file/name as input.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** apply_iam_policy  
**Type:** ConfigurationScript  
**Relative Path:** scripts/policies  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO IAM Policy Application
    
**Requirement Ids:**
    
    - SEC-006
    
**Purpose:** Applies predefined or custom IAM policies to MinIO users or groups.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Takes parameters for target type (user/group), target name, and policy name or path to policy JSON file (from config_templates/). Uses 'mc admin policy set ALIAS POLICY_NAME user=USER_NAME' or 'mc admin policy set ALIAS POLICY_NAME group=GROUP_NAME'. If policy JSON is provided, it might first use 'mc admin policy add ALIAS POLICY_NAME POLICY_FILE.json'.  
**Documentation:**
    
    - **Summary:** Applies JSON-defined IAM-like policies to specified MinIO users or groups for fine-grained access control.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/policies/set_bucket_lifecycle.sh  
**Description:** Script to configure bucket lifecycle policies, e.g., for expiring old objects or transitioning data. Takes bucket name and lifecycle policy JSON file as input.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** set_bucket_lifecycle  
**Type:** ConfigurationScript  
**Relative Path:** scripts/policies  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Bucket Lifecycle Management
    
**Requirement Ids:**
    
    - Section 7.5
    
**Purpose:** Configures object lifecycle rules for MinIO buckets (e.g., expiration, transition).  
**Logic Description:** Sources common_utils.sh and set_env.sh. Takes parameters for bucket name and path to a lifecycle policy JSON file (from config_templates/). Uses 'mc ilm set ALIAS/BUCKET_NAME LIFECYCLE_POLICY.json'. Includes options to get or list existing lifecycle policies for a bucket.  
**Documentation:**
    
    - **Summary:** Applies or manages object lifecycle management (ILM) policies on specified MinIO buckets using a JSON configuration file.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/admin/check_cluster_health.sh  
**Description:** Script to check the health and status of the MinIO cluster using 'mc admin info' and other relevant admin commands.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** check_cluster_health  
**Type:** OperationalScript  
**Relative Path:** scripts/admin  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Cluster Health Check
    
**Requirement Ids:**
    
    - DEP-001
    
**Purpose:** Provides a quick way to assess the operational status and health of the MinIO cluster.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Executes 'mc admin info ALIAS' to display server status, disk usage, uptime, etc. May include other commands like 'mc admin top locks ALIAS' or 'mc admin heal ALIAS' (for checking heal status). Parses output for key health indicators or errors.  
**Documentation:**
    
    - **Summary:** Performs health checks on the MinIO cluster, reporting status, server information, and storage usage.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Monitoring
    
- **Path:** scripts/admin/manage_kms_kek.sh  
**Description:** Script for managing Key Encryption Keys (KEK) if MinIO's server-side encryption with an external KMS (like Vault) is used. This is advanced.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** manage_kms_kek  
**Type:** ConfigurationScript  
**Relative Path:** scripts/admin  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO KMS KEK Management
    
**Requirement Ids:**
    
    - SEC-003
    - REQ-DA-010
    
**Purpose:** Manages Key Encryption Keys (KEKs) for server-side encryption when MinIO is integrated with an external KMS.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Wraps 'mc admin kms key create/status/import/export ALIAS' commands. Requires MinIO server to be configured with KMS settings. Parameterizes KEK names and KMS interaction details where appropriate (though most KMS config is server-side).  
**Documentation:**
    
    - **Summary:** Manages Key Encryption Keys (KEKs) used by MinIO for server-side encryption with an external Key Management Service (KMS).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** scripts/admin/configure_prometheus_endpoint.sh  
**Description:** Script to configure or verify the Prometheus metrics scraping endpoint on MinIO using 'mc admin prometheus generate'.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** configure_prometheus_endpoint  
**Type:** ConfigurationScript  
**Relative Path:** scripts/admin  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - MinIO Prometheus Metrics Configuration
    
**Requirement Ids:**
    
    - DEP-005
    
**Purpose:** Configures MinIO's endpoint for Prometheus metrics scraping.  
**Logic Description:** Sources common_utils.sh and set_env.sh. Uses 'mc admin prometheus generate ALIAS BUCKET_NAME' to define a scrape target for Prometheus. Note: The actual scraping is done by Prometheus, this script configures MinIO's side. May also involve setting up service accounts with necessary permissions for Prometheus to scrape.  
**Documentation:**
    
    - **Summary:** Generates or verifies the configuration for MinIO to expose metrics for Prometheus scraping.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Monitoring
    
- **Path:** python_utils/minio_operations.py  
**Description:** Python utility module using the MinIO SDK for more complex operations not easily achievable with 'mc' or requiring programmatic logic (e.g., batch operations, complex policy generation, detailed reporting).  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** minio_operations  
**Type:** UtilityScript  
**Relative Path:** python_utils  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** connect_client  
**Parameters:**
    
    - endpoint
    - access_key
    - secret_key
    - secure=True
    
**Return Type:** Minio  
**Attributes:**   
    - **Name:** create_bucket_if_not_exists  
**Parameters:**
    
    - client
    - bucket_name
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** set_complex_bucket_policy  
**Parameters:**
    
    - client
    - bucket_name
    - policy_document_str
    
**Return Type:** void  
**Attributes:**   
    - **Name:** generate_replication_status_report  
**Parameters:**
    
    - client
    - bucket_name
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - Advanced MinIO SDK Operations
    
**Requirement Ids:**
    
    - NFR-004
    - Section 7.4.1
    
**Purpose:** Provides Python functions leveraging the MinIO SDK for advanced configuration and management tasks.  
**Logic Description:** Imports the 'minio' Python library. Defines functions for connecting to MinIO, creating buckets with specific configurations, applying complex JSON policies, and potentially querying detailed replication status or performing batch object operations. Uses environment variables or configuration files for connection details.  
**Documentation:**
    
    - **Summary:** A Python module offering extended MinIO management capabilities using the official MinIO SDK, for tasks requiring more complex logic than simple 'mc' commands.
    
**Namespace:** CreativeFlow.Storage.MinIO.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/requirements.txt  
**Description:** Lists Python dependencies for scripts in the python_utils directory, primarily the 'minio' SDK.  
**Template:** Text File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyFile  
**Relative Path:** python_utils  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Python Dependency Management
    
**Requirement Ids:**
    
    
**Purpose:** Specifies Python package dependencies for the utility scripts.  
**Logic Description:** Contains lines like 'minio>=7.0.0'. Used by 'pip install -r requirements.txt' to set up the Python environment for these scripts.  
**Documentation:**
    
    - **Summary:** Defines the Python package dependencies (e.g., minio SDK version) required for the Python utility scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** config_templates/iam_policy_example.json  
**Description:** Example JSON template for a MinIO IAM policy document. Can be customized and used with apply_iam_policy.sh.  
**Template:** JSON Template  
**Dependency Level:** 0  
**Name:** iam_policy_example  
**Type:** ConfigurationTemplate  
**Relative Path:** config_templates  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - IAM Policy Template
    
**Requirement Ids:**
    
    - SEC-006
    
**Purpose:** Provides a starting point or example for creating IAM policy documents for MinIO.  
**Logic Description:** A valid MinIO IAM policy JSON structure with placeholders or example statements for actions (e.g., s3:GetObject, s3:PutObject) and resources (e.g., arn:aws:s3:::bucketname/*).  
**Documentation:**
    
    - **Summary:** An example JSON template illustrating the structure of an IAM policy document for MinIO, which can be adapted for specific needs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Template
    
- **Path:** config_templates/lifecycle_policy_example.json  
**Description:** Example JSON template for a MinIO bucket lifecycle policy. Can be customized and used with set_bucket_lifecycle.sh.  
**Template:** JSON Template  
**Dependency Level:** 0  
**Name:** lifecycle_policy_example  
**Type:** ConfigurationTemplate  
**Relative Path:** config_templates  
**Repository Id:** REPO-MINIO-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Lifecycle Policy Template
    
**Requirement Ids:**
    
    - Section 7.5
    
**Purpose:** Provides an example structure for MinIO bucket lifecycle configuration rules.  
**Logic Description:** A valid MinIO lifecycle configuration JSON structure (XML is also used by MinIO, but mc ilm set typically takes JSON). Includes example rules for expiration (e.g., delete objects older than X days) or transition (if MinIO tiering is used).  
**Documentation:**
    
    - **Summary:** An example JSON template demonstrating the structure for defining MinIO bucket lifecycle rules, such as object expiration or transitions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Template
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

