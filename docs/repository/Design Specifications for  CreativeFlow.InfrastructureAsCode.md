# Software Design Specification (SDS) for CreativeFlow.InfrastructureAsCode

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `CreativeFlow.InfrastructureAsCode` repository. Its primary purpose is to automate the provisioning, configuration, and ongoing management of all self-hosted Linux servers and their associated software stacks for the CreativeFlow AI platform. This automation will be achieved using Ansible, ensuring consistency, reliability, and efficiency across multiple environments (Development, Staging, Production, Disaster Recovery).

### 1.2 Scope
The scope of this repository includes:
*   Ansible playbooks, roles, inventory files, and variable definitions.
*   Automation for Operating System (Ubuntu 22.04 LTS) base configuration and hardening.
*   Deployment and configuration of core services: Nginx, PostgreSQL, Odoo, n8n, MinIO, Redis, RabbitMQ.
*   Deployment and configuration of the Kubernetes cluster (masters, workers, GPU support) for AI workloads.
*   Installation and configuration of monitoring agents.
*   Management of Cloudflare DNS records and basic WAF rules.
*   Automated patch management procedures.
*   Integration with a secrets management solution (HashiCorp Vault or Ansible Vault).
*   Design for integration with a CI/CD pipeline (GitLab CI/CD or GitHub Actions).

### 1.3 Definitions and Acronyms
*   **IaC:** Infrastructure as Code
*   **CI/CD:** Continuous Integration / Continuous Deployment
*   **K8s:** Kubernetes
*   **DR:** Disaster Recovery
*   **VM:** Virtual Machine
*   **INI:** Initialization file format (used for Ansible inventory)
*   **YAML:** YAML Ain't Markup Language (used for Ansible playbooks and variable files)
*   **Jinja2:** Templating engine used by Ansible
*   **PKA:** Public Key Authentication
*   **MFA:** Multi-Factor Authentication
*   **WAF:** Web Application Firewall
*   **CNI:** Container Network Interface
*   **CRI:** Container Runtime Interface
*   **GPU:** Graphics Processing Unit
*   **DCGM:** NVIDIA Data Center GPU Manager
*   **RDBMS:** Relational Database Management System
*   **ETL:** Extract, Transform, Load
*   **KPI:** Key Performance Indicator
*   **NFR:** Non-Functional Requirement
*   **SDS:** Software Design Specification
*   **RPO:** Recovery Point Objective
*   **RTO:** Recovery Time Objective
*   **UAT:** User Acceptance Testing
*   **SOP:** Standard Operating Procedure

## 2. General Design Principles

The Ansible code within this repository will adhere to the following principles:

*   **Idempotency:** All playbooks and roles will be designed to be idempotent, meaning they can be run multiple times on the same host(s) with the same outcome, without causing unintended changes after the initial successful application.
*   **Modularity:** Functionality will be encapsulated within roles for reusability, maintainability, and clarity. Roles will be focused on managing a specific service or component.
*   **Parameterization:** Extensive use of variables (defaults, group variables, host variables, extra variables) will allow for flexible configuration across different environments and hosts without modifying core playbook/role logic.
*   **Secrets Management:** Sensitive data (passwords, API keys, certificates) will NOT be stored in plaintext in Git. Ansible Vault will be used to encrypt sensitive variable files, and integration with HashiCorp Vault (via lookup plugins) will be the preferred method for dynamic secret retrieval.
*   **Version Control:** All Ansible code, including playbooks, roles, inventory, and variable files, will be version-controlled using Git. A clear branching strategy (e.g., GitFlow or a simpler feature-branch model) will be adopted.
*   **Readability & Maintainability:** Code will be well-structured, with clear naming conventions for files, variables, tasks, and roles. YAML files will be properly formatted. Comments will be used to explain complex logic or non-obvious configurations.
*   **Atomicity (where feasible):** Tasks within roles will be organized to be as atomic as possible, and handlers will be used to trigger service restarts/reloads only when necessary configuration changes occur.
*   **Error Handling:** Playbooks will include basic error handling, and tasks will be designed to fail explicitly if critical steps cannot be completed. Ansible's `failed_when` and `changed_when` conditions will be used appropriately.
*   **Testing:**
    *   **Linting:** `ansible-lint` will be used to check playbooks and roles for best practices and potential errors.
    *   **Syntax Check:** `ansible-playbook --syntax-check` will be used.
    *   **Dry Runs:** `ansible-playbook --check` (check mode) will be used extensively to predict changes before applying them, especially in CI/CD.
*   **Minimalism:** Roles and playbooks will only install necessary packages and configure essential services to reduce attack surface and complexity.
*   **Tagging:** Tasks within playbooks and roles will be appropriately tagged to allow for granular execution (e.g., `ansible-playbook site.yml --tags nginx_config`).

## 3. Directory Structure Overview

The repository will follow a standard Ansible project structure:


.
├── ansible.cfg                 # Ansible configuration file
├── requirements.yml            # Ansible Galaxy collections and roles
├── inventory/                  # Inventory files for different environments
│   ├── production/
│   │   └── hosts.ini
│   ├── staging/
│   │   └── hosts.ini
│   ├── development/
│   │   └── hosts.ini
│   └── dr/
│       └── hosts.ini
├── group_vars/                 # Variables for host groups
│   ├── all/
│   │   └── main.yml
│   │   └── secrets.vault.yml   # Encrypted global secrets
│   ├── production.yml
│   ├── production.vault.yml    # Encrypted production secrets
│   ├── staging.yml
│   ├── staging.vault.yml       # Encrypted staging secrets
│   ├── k8s_cluster/
│   │   └── k8s_config.yml
│   │   └── k8s_secrets.vault.yml
│   └── (other_group_specific_vars)/
├── host_vars/                  # Variables for specific hosts (if needed)
│   └── (hostname.yml)
├── playbooks/                  # Main playbooks
│   ├── site.yml
│   ├── patch_management.yml
│   ├── setup_kubernetes_cluster.yml
│   ├── configure_nginx_load_balancer.yml
│   └── (other_orchestration_playbooks).yml
├── roles/                      # Reusable roles
│   ├── common/
│   ├── nginx/
│   ├── kubernetes_master/
│   ├── kubernetes_worker/
│   ├── patching/
│   ├── cloudflare_config/
│   ├── postgresql/
│   ├── odoo/
│   ├── n8n/
│   ├── minio/
│   ├── redis/
│   ├── rabbitmq/
│   ├── docker/                 # Role for Docker installation if needed outside K8s context
│   ├── monitoring_agents/      # For Prometheus exporters, log shippers
│   ├── common_security/        # For more specific security hardening tasks
│   └── (other_service_roles)/
└── library/                    # Custom Ansible modules (if any)
└── filter_plugins/             # Custom Jinja2 filter plugins (if any)
└── lookup_plugins/             # Custom lookup plugins (e.g., for HashiCorp Vault)


## 4. Core Ansible Configuration

### 4.1 `ansible.cfg`
*   **Purpose:** To configure the behavior of Ansible for this project, ensuring consistent execution.
*   **Key Settings:**
    *   `inventory = ./inventory`: Points to the root of the inventory directory.
    *   `roles_path = ./roles`: Defines the location of Ansible roles.
    *   `remote_user = {{ ansible_ssh_user | default('creativeflow_admin') }}`: Default SSH user. Can be overridden.
    *   `private_key_file = ~/.ssh/id_ed25519_creativeflow` (Example, manage actual keys securely, preferably via SSH agent or environment-specific vault).
    *   `host_key_checking = False`: Recommended for managed environments where hosts are known. For higher security, use known hosts.
    *   `retry_files_enabled = False`: Prevents creation of `.retry` files on playbook failure.
    *   `forks = 10`: Number of parallel processes.
    *   `log_path = ./ansible.log`: Path to Ansible log file.
    *   `stdout_callback = yaml` (or `community.general.yaml` for better output).
    *   `callbacks_enabled = timer, profile_tasks, profile_roles`: For performance analysis.
    *   `jinja2_native = True`: Enable native Python types in Jinja2.
    *   Paths for `library`, `filter_plugins`, `lookup_plugins` if custom ones are developed.
    *   `vault_password_file = ./.vault_pass.txt` (Example: path to a file containing the vault password, ensure this file is gitignored and permissions are restrictive. Better for CI: use environment variables or credential injection).

### 4.2 `requirements.yml`
*   **Purpose:** To manage and version-control external Ansible dependencies.
*   **Content:**
    yaml
    collections:
      - name: community.general
        version: ">=7.0.0" # Example version
      - name: community.docker
        version: ">=3.0.0"
      - name: community.kubernetes # For K8s management using k8s module
        version: ">=2.0.0" # (formerly kubernetes.core)
      - name: community.postgresql
        version: ">=2.5.0"
      - name: ansible.posix
        version: ">=1.5.0"
      - name: community.crypto # For certificate management
      # For HashiCorp Vault integration if used directly via lookup plugin
      - name: community.hashi_vault
        version: ">=4.0.0"
      # Potentially other vendor/community collections for specific software (e.g., Redis, RabbitMQ)
      # Example:
      # - name: community.rabbitmq
      # - name: community.redis
    
    *   Specific versions should be pinned for stability and updated deliberately.

## 5. Inventory Management

### 5.1 Strategy
*   Static inventory files (`hosts.ini`) will be used for each environment (production, staging, development, DR).
*   Hosts will be grouped logically based on their function (e.g., `webservers`, `db_primary`, `k8s_masters`).
*   Consistency in group naming across environments is crucial for applying roles correctly.
*   Connection parameters (e.g., `ansible_host`, `ansible_user`, `ansible_ssh_private_key_file`) can be defined per host or group if they differ from `ansible.cfg` defaults. It's often better to rely on SSH agent, `~/.ssh/config`, or pass such parameters via CI/CD for production.

### 5.2 Example `inventory/production/hosts.ini`
ini
[all:vars]
env=production

[webservers]
web01.prod.creativeflow.ai ansible_host=10.0.1.10
web02.prod.creativeflow.ai ansible_host=10.0.1.11

[load_balancers]
lb01.prod.creativeflow.ai ansible_host=10.0.1.5
lb02.prod.creativeflow.ai ansible_host=10.0.1.6

[odoo_app_servers]
odoo01.prod.creativeflow.ai ansible_host=10.0.2.10
odoo02.prod.creativeflow.ai ansible_host=10.0.2.11

[n8n_app_servers]
n8n01.prod.creativeflow.ai ansible_host=10.0.2.20

[db_primary]
pg01.prod.creativeflow.ai ansible_host=10.0.3.10 postgresql_node_type=primary

[db_replicas]
pg02.prod.creativeflow.ai ansible_host=10.0.3.11 postgresql_node_type=replica postgresql_primary_host=pg01.prod.creativeflow.ai

[minio_cluster]
minio01.prod.creativeflow.ai ansible_host=10.0.4.10
minio02.prod.creativeflow.ai ansible_host=10.0.4.11
minio03.prod.creativeflow.ai ansible_host=10.0.4.12

[redis_cluster] # Or Sentinel setup
redis01.prod.creativeflow.ai ansible_host=10.0.5.10
redis02.prod.creativeflow.ai ansible_host=10.0.5.11
redis03.prod.creativeflow.ai ansible_host=10.0.5.12

[rabbitmq_cluster]
rmq01.prod.creativeflow.ai ansible_host=10.0.6.10
rmq02.prod.creativeflow.ai ansible_host=10.0.6.11
rmq03.prod.creativeflow.ai ansible_host=10.0.6.12

[k8s_masters]
k8smaster01.prod.creativeflow.ai ansible_host=10.0.7.10
k8smaster02.prod.creativeflow.ai ansible_host=10.0.7.11
k8smaster03.prod.creativeflow.ai ansible_host=10.0.7.12

[k8s_workers_gpu]
k8sworkergpu01.prod.creativeflow.ai ansible_host=10.0.8.10 is_gpu_node=true
k8sworkergpu02.prod.creativeflow.ai ansible_host=10.0.8.11 is_gpu_node=true

[k8s_workers_cpu]
k8sworkercpu01.prod.creativeflow.ai ansible_host=10.0.8.20

[monitoring_server]
monitor01.prod.creativeflow.ai ansible_host=10.0.9.10

*   Inventories for `staging`, `development`, and `dr` will follow a similar structure with environment-specific hostnames/IPs and an `env` variable (e.g., `env=staging`).

## 6. Variable Management

### 6.1 Hierarchy and Precedence
Ansible's variable precedence will be utilized:
1.  Extra vars (CLI `-e` or passed by CI/CD).
2.  Task vars.
3.  Block vars.
4.  Role vars (defined in `vars/` within a role).
5.  Host facts / discovered variables.
6.  Play vars.
7.  Host vars (`host_vars/hostname.yml`).
8.  Group vars (`group_vars/<group_name>.yml` or `group_vars/<group_name>/`).
9.  Inventory group vars (defined in inventory file).
10. Inventory host vars (defined in inventory file).
11. Role defaults (`defaults/main.yml` within a role).
12. `group_vars/all/main.yml`.

### 6.2 `group_vars/all/main.yml`
*   **Purpose:** Define global defaults and common settings.
*   **Example Content:**
    yaml
    # Common settings
    admin_user: "creativeflow_ops"
    default_ssh_port: 22
    ntp_servers:
      - "0.pool.ntp.org"
      - "1.pool.ntp.org"
    common_packages:
      - vim
      - curl
      - wget
      - htop
      - git
      - unattended-upgrades # For security patches
      - python3-pip
    
    # Paths
    log_base_dir: /var/log/creativeflow
    app_base_dir: /opt/creativeflow

    # Secrets Management - paths to where secrets are stored in Vault
    # These are NOT the secrets themselves, but pointers/paths for lookup plugins
    vault_secrets_base_path: "secret/data/creativeflow" # Example for HashiCorp Vault

    # Default versions (can be overridden per environment)
    default_postgres_version: "16"
    default_redis_version: "7.x"
    default_rabbitmq_version: "3.12.x"
    default_python_version: "3.11"
    default_node_version: "20.x"
    

### 6.3 Environment-Specific Variables (e.g., `group_vars/production.yml`)
*   **Purpose:** Override global defaults and define environment-specific configurations.
*   **Example Content (`group_vars/production.yml`):**
    yaml
    env_type: "production"
    api_domain: "api.creativeflow.ai"
    webapp_domain: "app.creativeflow.ai"
    # Database connection details (actual passwords in .vault.yml or HashiCorp Vault)
    postgres_db_host: "pg01.prod.creativeflow.ai"
    postgres_app_user: "cf_app_prod"
    # Odoo Specific
    odoo_db_user: "odoo_prod"
    odoo_workers: 8 
    # Monitoring
    prometheus_scrape_interval: "30s"
    log_level_default: "INFO" # For applications
    

### 6.4 Group-Specific Variables (e.g., `group_vars/k8s_cluster/k8s_config.yml`)
*   **Purpose:** Define configurations specific to a group of hosts (e.g., all Kubernetes nodes).
*   **Example Content (`group_vars/k8s_cluster/k8s_config.yml`):**
    yaml
    kubernetes_version: "1.28.x" # Target K8s version
    k8s_api_server_vip: "10.0.7.5" # Virtual IP for K8s API HA
    pod_network_cidr: "10.244.0.0/16"
    service_network_cidr: "10.96.0.0/12"
    cni_plugin: "calico" # or flannel, weave, etc.
    install_gpu_operator: true
    gpu_operator_version: "v23.9.1" # Example
    docker_version: "25.0.x"
    

### 6.5 Encrypted Variables (`*.vault.yml`)
*   **Purpose:** Store sensitive data like passwords, API keys, private certificate keys.
*   **Method:** These files will be encrypted using `ansible-vault encrypt <filename>`.
*   **Example (`group_vars/production.vault.yml`):**
    yaml
    # This file is encrypted with Ansible Vault
    # Example content BEFORE encryption:
    # postgres_app_password: "prod_db_password_very_secret"
    # odoo_db_password: "odoo_prod_password_secret"
    # cloudflare_api_token: "cloudflare_api_token_secret"
    # stripe_api_key_live: "sk_live_xxxxxxxxxxxx"
    
    Content will be encrypted ciphertext. The vault password will be managed securely, potentially injected by the CI/CD system from its own secrets store or HashiCorp Vault.

## 7. Playbook Design

### 7.1 `playbooks/site.yml`
*   **Purpose:** Main entry point for configuring the entire infrastructure.
*   **Logic:**
    *   Gathers facts from all hosts.
    *   Applies common configurations to all hosts using the `common` role.
    *   Applies specific roles to relevant host groups in a logical order.
    *   Example structure:
        yaml
        - name: Apply common configuration to all hosts
          hosts: all
          become: yes
          roles:
            - common
            - common_security # Further security hardening
            - monitoring_agents # Base monitoring agents like node_exporter
            - docker # If Docker is a common prerequisite

        - name: Configure Nginx Load Balancers
          hosts: load_balancers
          become: yes
          roles:
            - role: nginx
              nginx_mode: loadbalancer
              # Pass specific LB vars if needed

        - name: Configure Web Servers (if separate from LBs or app servers)
          hosts: webservers
          become: yes
          roles:
            - role: nginx
              nginx_mode: webserver

        - name: Setup PostgreSQL Database Servers
          hosts: db_primary, db_replicas
          become: yes
          roles:
            - postgresql

        - name: Setup MinIO Object Storage Cluster
          hosts: minio_cluster
          become: yes
          roles:
            - minio

        - name: Setup Redis Cluster/Sentinel
          hosts: redis_cluster
          become: yes
          roles:
            - redis

        - name: Setup RabbitMQ Cluster
          hosts: rabbitmq_cluster
          become: yes
          roles:
            - rabbitmq

        - name: Deploy Odoo Application Servers
          hosts: odoo_app_servers
          become: yes
          roles:
            - odoo
            - role: nginx # As reverse proxy for Odoo
              nginx_odoo_upstream_host: "{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}" # Example
              nginx_odoo_upstream_port: 8069

        - name: Deploy n8n Application Servers
          hosts: n8n_app_servers
          become: yes
          roles:
            - n8n
            - role: nginx # As reverse proxy for n8n
              nginx_n8n_upstream_host: "{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}" # Example
              nginx_n8n_upstream_port: 5678

        - name: Setup Kubernetes Cluster
          import_playbook: setup_kubernetes_cluster.yml

        - name: Configure Cloudflare (DNS, basic WAF)
          hosts: localhost # Typically run against localhost to use API
          connection: local
          gather_facts: no
          roles:
            - cloudflare_config
        

### 7.2 `playbooks/patch_management.yml`
*   **Purpose:** Automate OS and software patching.
*   **Logic:**
    *   Can be parameterized to target specific groups or all hosts (`-e "target_hosts=webservers"`).
    *   Uses the `patching` role.
    *   May include serial execution for rolling updates.
    *   Example:
        yaml
        - name: Apply system patches
          hosts: "{{ target_hosts | default('all') }}"
          become: yes
          serial: 1 # Example: one host at a time for critical services
          roles:
            - patching
        

### 7.3 `playbooks/setup_kubernetes_cluster.yml`
*   **Purpose:** Orchestrate Kubernetes cluster deployment.
*   **Logic:**
    *   Separates master and worker node setup.
    *   Ensures masters are set up before workers attempt to join.
    *   Example:
        yaml
        - name: Setup Kubernetes Master Nodes
          hosts: k8s_masters
          become: yes
          roles:
            - kubernetes_master

        - name: Setup Kubernetes Worker Nodes
          hosts: k8s_workers_gpu, k8s_workers_cpu
          become: yes
          roles:
            - kubernetes_worker
        

### 7.4 `playbooks/configure_nginx_load_balancer.yml`
*   **Purpose:** Specific playbook for setting up Nginx load balancers.
*   **Logic:**
    *   Targets `load_balancers` group.
    *   Applies the `nginx` role with `nginx_mode: loadbalancer`.
    *   Uses templates to define upstream server blocks based on other groups (e.g., `webservers`, `odoo_app_servers`).
    *   Manages SSL termination.

## 8. Role Design

For each role, the general structure will be:
`roles/<role_name>/{tasks,handlers,templates,files,vars,defaults,meta}`

### 8.1 Role: `common`
*   **Purpose:** Base configuration for all servers.
*   **`vars/main.yml` / `defaults/main.yml`:** `admin_user`, `common_packages`, `ntp_servers`, `timezone`.
*   **`tasks/main.yml`:**
    *   Set hostname.
    *   Configure timezone.
    *   Install common packages.
    *   Create admin user(s) with sudo privileges and authorized SSH keys.
    *   Basic SSH hardening (e.g., disable password authentication, permit root login no).
    *   Configure unattended upgrades for security patches.
    *   Setup basic firewall (e.g., UFW allowing SSH and essential ports).
*   **`handlers/main.yml`:** `restart sshd`, `reload ufw`.

### 8.2 Role: `common_security`
*   **Purpose:** Apply more advanced security hardening measures.
*   **`tasks/main.yml`:**
    *   Configure `auditd` for system auditing.
    *   Install and configure tools like `fail2ban`.
    *   Kernel parameter hardening (`/etc/sysctl.conf`).
    *   Ensure filesystem permissions are secure.
    *   Remove unnecessary packages/services.
    *   Implement CIS benchmark recommendations where applicable.

### 8.3 Role: `docker`
*   **Purpose:** Install and configure Docker engine.
*   **`vars/main.yml` / `defaults/main.yml`:** `docker_version`, `docker_users` (to add to docker group).
*   **`tasks/main.yml`:**
    *   Add Docker official GPG key and repository.
    *   Install Docker Engine, CLI, containerd.
    *   Configure Docker daemon options (e.g., log driver, storage driver).
    *   Add users to the `docker` group.
    *   Start and enable Docker service.
*   **`handlers/main.yml`:** `restart docker`.

### 8.4 Role: `nginx`
*   **Purpose:** Install and configure Nginx (web server, reverse proxy, load balancer).
*   **`vars/main.yml` / `defaults/main.yml`:** `nginx_mode` (webserver, reverse_proxy, loadbalancer), `nginx_worker_processes`, `nginx_log_dir`, `ssl_cert_path`, `ssl_key_path`, `upstream_servers` (list of dicts for LB/RP).
*   **`tasks/main.yml`:**
    *   Install Nginx.
    *   Deploy `nginx.conf` from template (`templates/nginx.conf.j2`).
    *   Deploy virtual host configurations from templates (e.g., `templates/vhost.conf.j2`) using `with_items` for defined sites/services.
    *   Manage SSL certificates (copying from a secure location or integrating with Let's Encrypt role).
    *   Enable/start Nginx service.
*   **`templates/nginx.conf.j2`:** Main Nginx configuration.
*   **`templates/vhost.conf.j2`:** Template for individual site configurations (server blocks).
*   **`handlers/main.yml`:** `reload nginx`, `restart nginx`.

### 8.5 Role: `postgresql`
*   **Purpose:** Install and configure PostgreSQL server, including replication.
*   **`vars/main.yml` / `defaults/main.yml`:** `postgresql_version`, `postgresql_port`, `postgresql_data_dir`, `postgresql_databases` (list of DBs to create), `postgresql_users` (list of users with passwords from vault), `postgresql_node_type` (primary/replica), `postgresql_primary_host` (for replicas), `postgresql_replication_user`, `postgresql_replication_password` (from vault).
*   **`tasks/main.yml`:**
    *   Install PostgreSQL server and client packages, `python3-psycopg2`.
    *   Initialize database cluster (if new).
    *   Configure `postgresql.conf` (listen_addresses, max_connections, shared_buffers, WAL settings for replication) using template.
    *   Configure `pg_hba.conf` (authentication methods) using template.
    *   Create databases and users.
    *   Grant privileges.
    *   If `postgresql_node_type == 'primary'`, configure for replication (e.g., create replication slot).
    *   If `postgresql_node_type == 'replica'`, configure to connect to primary (`recovery.conf` or equivalent for PG12+).
    *   Start/enable PostgreSQL service.
*   **`templates/postgresql.conf.j2`, `templates/pg_hba.conf.j2`**.
*   **`handlers/main.yml`:** `restart postgresql`, `reload postgresql`.

### 8.6 Role: `odoo`
*   **Purpose:** Deploy and configure Odoo ERP.
*   **`vars/main.yml` / `defaults/main.yml`:** `odoo_version`, `odoo_user`, `odoo_home`, `odoo_config_file_path`, `odoo_addons_path`, `odoo_workers`, `odoo_db_host`, `odoo_db_port`, `odoo_db_user`, `odoo_db_password` (from vault).
*   **`tasks/main.yml`:**
    *   Install Odoo system dependencies (Python, wkhtmltopdf, Less, etc.).
    *   Create Odoo system user.
    *   Clone Odoo source code (specific version/branch) or install from deb packages.
    *   Install Python dependencies from `requirements.txt`.
    *   Create Odoo configuration file (`odoo.conf`) from template.
    *   Set up log directory and permissions.
    *   Create systemd service unit file for Odoo.
    *   Start/enable Odoo service.
*   **`templates/odoo.conf.j2`, `templates/odoo.service.j2`**.
*   **`handlers/main.yml`:** `restart odoo`.

### 8.7 Role: `n8n`
*   **Purpose:** Deploy and configure n8n workflow automation tool.
*   **`vars/main.yml` / `defaults/main.yml`:** `n8n_version`, `n8n_user`, `n8n_install_dir`, `n8n_port`, `n8n_env_vars` (dict of environment variables for n8n, including DB connection, encryption key from vault).
*   **`tasks/main.yml`:**
    *   Install Node.js and npm/yarn.
    *   Create n8n system user.
    *   Install n8n globally or locally using npm/yarn.
    *   Create environment file for n8n from template or by setting environment variables for the service.
    *   Configure n8n to use PostgreSQL as its database.
    *   Set up systemd service for n8n (or PM2).
    *   Start/enable n8n service.
*   **`templates/n8n.service.j2` (or PM2 config template), `templates/n8n_env.j2` (if using env file)**.
*   **`handlers/main.yml`:** `restart n8n`.

### 8.8 Role: `minio`
*   **Purpose:** Deploy and configure MinIO S3-compatible object storage.
*   **`vars/main.yml` / `defaults/main.yml`:** `minio_version`, `minio_user`, `minio_install_dir`, `minio_data_dirs` (list of disk paths), `minio_access_key` (from vault), `minio_secret_key` (from vault), `minio_cluster_nodes` (list of peer IPs/hostnames for distributed mode), `minio_region`.
*   **`tasks/main.yml`:**
    *   Create MinIO system user.
    *   Download MinIO binary.
    *   Create data directories with correct permissions.
    *   Create MinIO environment/configuration file.
    *   Set up systemd service unit file for MinIO server.
    *   Start/enable MinIO service.
    *   Configure MinIO Client (`mc`) for administrative tasks (e.g., creating initial buckets, setting replication, as separate tasks or playbooks).
*   **`templates/minio.service.j2`, `templates/minio_env.j2`**.
*   **`handlers/main.yml`:** `restart minio`.

### 8.9 Role: `redis`
*   **Purpose:** Deploy and configure Redis in-memory data store.
*   **`vars/main.yml` / `defaults/main.yml`:** `redis_version`, `redis_port`, `redis_bind_ip`, `redis_password` (from vault), `redis_persistence_type` (aof/rdb), `redis_maxmemory`, `redis_mode` (standalone, sentinel, cluster).
*   **`tasks/main.yml`:**
    *   Install Redis server.
    *   Configure `redis.conf` from template.
    *   If Sentinel mode, configure `sentinel.conf`.
    *   If Cluster mode, perform cluster creation steps.
    *   Start/enable Redis service (and Sentinel service if applicable).
*   **`templates/redis.conf.j2`, `templates/sentinel.conf.j2`**.
*   **`handlers/main.yml`:** `restart redis`, `restart redis-sentinel`.

### 8.10 Role: `rabbitmq`
*   **Purpose:** Deploy and configure RabbitMQ message broker.
*   **`vars/main.yml` / `defaults/main.yml`:** `rabbitmq_version`, `rabbitmq_nodename`, `rabbitmq_erlang_cookie` (from vault), `rabbitmq_users` (list of users with passwords from vault), `rabbitmq_vhosts`, `rabbitmq_cluster_nodes` (for clustering).
*   **`tasks/main.yml`:**
    *   Add RabbitMQ and Erlang repositories/GPG keys.
    *   Install RabbitMQ server and Erlang.
    *   Set Erlang cookie.
    *   Configure `rabbitmq.conf` and `rabbitmq-env.conf` if needed.
    *   Enable RabbitMQ management plugin.
    *   Start/enable RabbitMQ service.
    *   Create users, vhosts, and set permissions.
    *   Join nodes to form a cluster (if `rabbitmq_cluster_nodes` is defined).
    *   Set up mirrored queues policy if applicable.
*   **`handlers/main.yml`:** `restart rabbitmq-server`.

### 8.11 Role: `kubernetes_master` & `kubernetes_worker`
*   **`vars/main.yml` / `defaults/main.yml` (for k8s group or specific roles):** `kubernetes_version`, `cni_plugin_url` (e.g., Calico manifest URL), `k8s_api_advertise_address`, `pod_network_cidr`, `kubeadm_token` (generated on first master, shared). For workers: `is_gpu_node` (boolean), `nvidia_driver_version`.
*   **`tasks/main.yml` (master):**
    *   Install Docker/CRI, kubeadm, kubelet, kubectl.
    *   Disable swap.
    *   Initialize cluster (`kubeadm init`).
    *   Configure kubectl for admin.
    *   Apply CNI plugin.
    *   Generate and store/output join command for workers.
*   **`tasks/main.yml` (worker):**
    *   Install Docker/CRI, kubeadm, kubelet.
    *   Disable swap.
    *   If `is_gpu_node`: install NVIDIA drivers, NVIDIA container toolkit, NVIDIA GPU Operator.
    *   Join cluster using `kubeadm join`.
*   **`handlers/main.yml`:** `restart kubelet`.

### 8.12 Role: `patching`
*   **Purpose:** Apply OS updates and security patches.
*   **`vars/main.yml` / `defaults/main.yml`:** `patching_reboot_allowed` (boolean), `patching_package_list` (specific packages to update, or 'all').
*   **`tasks/main.yml`:**
    *   Update package manager cache (`apt update`, `yum check-update`).
    *   Perform upgrade (`apt dist-upgrade -y`, `yum update -y`).
    *   Check if reboot is required (e.g., `/var/run/reboot-required`).
    *   Reboot host if `patching_reboot_allowed` and reboot is required, with appropriate pre/post checks.
*   **`handlers/main.yml`:** None typically, reboots handled in tasks.

### 8.13 Role: `cloudflare_config`
*   **Purpose:** Manage Cloudflare DNS and basic WAF settings via API.
*   **`vars/main.yml` / `defaults/main.yml`:** `cloudflare_api_token` (from vault), `cloudflare_email`, `cloudflare_zone_id`, `dns_records` (list of records to manage), `waf_rules` (list of basic rules).
*   **`tasks/main.yml`:**
    *   Use `community.general.cloudflare_dns` module to create/update DNS records.
    *   Use `uri` module or a dedicated Cloudflare collection to manage WAF rules or other settings.
*   **Note:** Complex Cloudflare management is often done via Terraform or directly in Cloudflare UI. This role is for basic, automatable IaC-managed settings.

### 8.14 Role: `monitoring_agents`
*   **Purpose:** Install and configure various monitoring agents.
*   **`vars/main.yml` / `defaults/main.yml`:** `install_node_exporter` (boolean), `install_filebeat` (boolean), `filebeat_elasticsearch_hosts`, `node_exporter_version`.
*   **`tasks/main.yml`:**
    *   Install `node_exporter` for Prometheus system metrics.
    *   Install `filebeat` (or fluentd/fluent-bit) for log shipping to ELK/Loki.
    *   Configure agents to point to respective collection endpoints.
    *   Start/enable agent services.
*   **`handlers/main.yml`:** `restart node_exporter`, `restart filebeat`.

## 9. Secrets Management Strategy

*   **Primary Method:** HashiCorp Vault.
    *   Ansible will use the `community.hashi_vault.hashi_vault` lookup plugin or custom lookup plugins to retrieve secrets at runtime.
    *   CI/CD runners and Ansible controller nodes will need appropriate Vault authentication methods configured (e.g., AppRole, Kubernetes Auth).
*   **Secondary Method (for local dev or less sensitive data, if Vault is not immediately available for all contexts):** Ansible Vault.
    *   Sensitive variable files (e.g., `group_vars/all/secrets.vault.yml`, `group_vars/production.vault.yml`) will be encrypted.
    *   The vault password will be provided to `ansible-playbook` via `--vault-password-file` or `--vault-id @prompt`. In CI/CD, the vault password itself must be a secret injected into the pipeline.
*   **NO SECRETS IN PLAINTEXT IN GIT.**

## 10. CI/CD Integration Strategy (DEP-003)

*   Ansible playbooks will be executed by the CI/CD system (GitLab CI/CD or GitHub Actions).
*   **Pipeline Stages for IaC:**
    1.  **Lint & Syntax Check:** Run `ansible-lint` and `ansible-playbook --syntax-check` on changed playbooks/roles.
    2.  **Dry Run (Check Mode):** Execute playbooks with `--check` flag against a staging or temporary validation environment to preview changes.
    3.  **Integration/Validation Tests (Optional, Advanced):** If using tools like Molecule, run role tests.
    4.  **Apply to Staging:** Deploy changes to the staging environment.
    5.  **Manual Approval (Optional):** For production deployments.
    6.  **Apply to Production:** Deploy changes to the production environment.
    7.  **Apply to DR:** Propagate changes to the DR environment.
*   The CI/CD pipeline will manage environment-specific variables and Vault credentials securely.
*   Branching strategy (e.g., changes to `main` branch deploy to production after staging, feature branches deploy to dev/test environments) will dictate pipeline triggers.

## 11. Maintenance and Updates (DEP-005)

*   **OS & Software Patching:** Automated via `playbooks/patch_management.yml` and the `patching` role. Scheduled regularly (e.g., weekly or monthly) during defined maintenance windows.
*   **Ansible Core & Collections Updates:** `requirements.yml` will be periodically reviewed and updated to newer stable versions. Playbooks and roles will be tested against new Ansible/collection versions in a development environment before rolling out.
*   **Application Updates (Odoo, n8n, etc.):** Version variables in `group_vars` or role defaults will be updated. The respective Ansible roles (`odoo`, `n8n`, etc.) will handle the upgrade process (e.g., fetching new version, running migration scripts if applicable, restarting services). This requires careful design of the upgrade tasks within each role.

## 12. Error Handling and Logging

*   **Ansible Error Handling:**
    *   Playbooks will use `block`/`rescue`/`always` for complex error handling where needed.
    *   `failed_when` conditions to define custom failure criteria for tasks.
    *   `ignore_errors: yes` will be used sparingly and only when a failure is acceptable or handled explicitly.
*   **Logging:**
    *   Ansible's default logging will be captured to `ansible.log` (as per `ansible.cfg`).
    *   Increased verbosity (`-v`, `-vvv`) can be used for debugging.
    *   CI/CD pipeline will capture and store logs for each execution.
    *   Important changes and task outputs can be registered and logged using the `debug` module.

## 13. Future Considerations / Scalability

*   **Dynamic Inventory:** While starting with static INI files, the system can be adapted to use dynamic inventory scripts if the number of hosts grows significantly or if using cloud providers.
*   **More Complex Cloudflare/WAF Management:** If advanced Cloudflare automation is needed, consider dedicated Terraform scripts or more specialized Ansible collections, as the `cloudflare_config` role is intended for basics.
*   **Testing with Molecule:** For more rigorous testing of Ansible roles in isolation, Molecule can be integrated.
*   **Advanced Kubernetes Deployments:** While basic K8s setup is covered, application deployments onto K8s would typically be handled by Kubernetes manifests (e.g., Helm charts, Kustomize) managed by a separate IaC layer or integrated with application CI/CD, rather than directly by these server-focused Ansible roles. This repository focuses on K8s *cluster* setup.
*   **AI Tools Configuration:** Specific "AI tools" mentioned in the description are broad. If these are custom applications, they'll need their own Ansible roles for deployment similar to Odoo/n8n. If they are managed services within K8s, their deployment would be via K8s manifests. This SDS assumes Ansible would configure prerequisites or nodes where these tools run if self-hosted outside K8s.
