# Software Design Specification (SDS): CreativeFlow.Infrastructure.IaC.Ansible

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.Infrastructure.IaC.Ansible` repository. The purpose of this repository is to implement the principles of Infrastructure as Code (IaC) to automate the provisioning, configuration, and management of the entire self-hosted infrastructure for the CreativeFlow AI platform.

This specification will guide the development of Ansible playbooks, roles, and supporting files to ensure a consistent, repeatable, secure, and maintainable infrastructure across all environments (Development, Staging, Production, and Disaster Recovery).

### 1.2. Scope
The scope of this repository includes the complete Ansible codebase required to manage the following components:
- **Operating Systems:** Ubuntu 22.04 LTS server hardening and base configuration.
- **Web & Proxy Servers:** Nginx as a load balancer and reverse proxy.
- **Application Servers:** Odoo, n8n, and custom backend services.
- **Database Systems:** PostgreSQL primary and replica servers.
- **Caching Systems:** Redis server and cluster/sentinel setup.
- **Message Queues:** RabbitMQ server and cluster setup.
- **Object Storage:** MinIO cluster setup.
- **Container Orchestration:** Kubernetes (K8s) cluster (master and worker nodes), including GPU support.
- **Monitoring & Logging:** Deployment of agents and exporters (Prometheus, Filebeat, etc.).

This SDS details the structure, logic, and variables for all Ansible artifacts required to fulfill requirements `DEP-003`, `DEP-004`, `DEP-004.1`, `DEP-005`, and relevant parts of `NFR-010`.

## 2. General Principles & Standards

The entire Ansible codebase must adhere to the following principles:

- **Idempotency:** All playbooks and roles must be idempotent. Running them multiple times on the same host must result in the same desired state without causing errors or unintended changes after the initial successful run.
- **Modularity:** Functionality must be encapsulated into discrete, reusable roles. Each role should be responsible for configuring a single software component (e.g., `nginx`, `postgresql_server`).
- **Version Control:** All code, including playbooks, roles, inventories, and variable files, must be stored and managed in a Git repository.
- **Environment Parity:** The codebase must support deploying to multiple environments (dev, staging, prod, dr) using the same roles and playbooks, with environment-specific differences managed exclusively through inventory and variable files.
- **Security by Design:**
    - **Least Privilege:** Services and users should be configured with the minimum required permissions.
    - **Secrets Management:** No secrets (passwords, API keys, tokens) shall be stored in plaintext in the Git repository. Ansible Vault will be used for encryption.

## 3. Project Structure Overview

The repository will follow a standard and scalable Ansible project structure as defined in the `file_structure_json`.


/
├── ansible.cfg
├── environments/
│   ├── development/
│   │   └── inventory.ini
│   ├── dr/
│   │   └── inventory.ini
│   ├── production/
│   │   └── inventory.ini
│   └── staging/
│       └── inventory.ini
├── group_vars/
│   ├── all/
│   │   ├── common_vars.yml
│   │   └── secrets.yml
│   ├── production/
│   │   ├── main.yml
│   │   └── secrets.yml
│   └── staging/
│       └── main.yml
├── host_vars/
│   └── (Optional, for host-specific variables)
├── library/
│   └── (For custom Python modules)
├── playbooks/
│   ├── provision_kubernetes_cluster.yml
│   └── patch_management.yml
├── roles/
│   ├── common/
│   ├── gpu_support/
│   ├── kubernetes_common/
│   ├── kubernetes_master/
│   ├── kubernetes_worker/
│   ├── minio_server/
│   ├── nginx_lb/
│   ├── n8n_server/
│   ├── odoo_server/
│   ├── postgresql_server/
│   ├── prometheus_exporters/
│   ├── rabbitmq_server/
│   └── redis_server/
├── requirements.yml
└── site.yml


## 4. Core Configuration Files

### 4.1. `ansible.cfg`
This file configures the default behavior of Ansible for the project.

- **`[defaults]` section:**
    - `inventory`: Set to `environments/production/inventory.ini` as a safe default. CI/CD will override this with `-i`.
    - `roles_path`: Set to `./roles`.
    - `remote_user`: Define a default remote user (e.g., `ansible_admin`).
    - `private_key_file`: Define the path to the default SSH private key.
    - `host_key_checking`: Set to `False` in dev, but should be `True` in staging/prod with known hosts managed.
    - `retry_files_enabled`: Set to `False` to avoid creating `.retry` files.
- **`[privilege_escalation]` section:**
    - Configure `become=True`, `become_method=sudo`, `become_user=root`, `become_ask_pass=False`.
- **`[ssh_connection]` section:**
    - `pipelining`: Set to `True` for performance improvement.
    - `ssh_args`: Configure default SSH arguments, like `-o ControlMaster=auto -o ControlPersist=60s`.

### 4.2. `requirements.yml`
This file will manage external Ansible role and collection dependencies from Ansible Galaxy or other Git repositories.

- **Collections:**
    - `community.general`: For a wide range of utility modules.
    - `community.docker`: For Docker and Docker Compose management.
    - `community.kubernetes`: For interaction with Kubernetes APIs.
    - `community.postgresql`: For advanced PostgreSQL management tasks.
- **Roles:**
    - Any vetted community roles for specific software if they provide a significant advantage over custom-built roles (e.g., a complex monitoring agent setup).

## 5. Environment and Secrets Management

### 5.1. Inventory (`environments/`)
- Each environment (`production`, `staging`, `development`, `dr`) will have its own `inventory.ini` file.
- The inventory will use the INI format and define host groups based on function, for example:
    - `[all_servers]`
    - `[web_servers]`
    - `[odoo_servers]`
    - `[db_primary]`
    - `[db_replicas]`
    - `[k8s_masters]`
    - `[k8s_workers]`
    - `[k8s_workers_gpu]`

### 5.2. Variables (`group_vars/`)
- **`group_vars/all/common_vars.yml`:** Defines variables that apply everywhere. Examples: `admin_user: 'ansible_admin'`, `ntp_servers: ['pool.ntp.org']`, `base_domain_name: 'creativeflow.ai'`.
- **Environment-Specific Vars (`group_vars/<env>/main.yml`):** Overrides `all` variables. Examples for `staging`: `environment: 'staging'`, `api_server_url: 'https://staging-api.creativeflow.ai'`. For `production`: `environment: 'production'`, `api_server_url: 'https://api.creativeflow.ai'`.
- **Variable Precedence:** Ansible's standard variable precedence will be relied upon to ensure environment-specific settings correctly override global defaults.

### 5.3. Secrets Management
- All sensitive data (passwords, tokens, private keys) will be stored in `secrets.yml` files within the `group_vars` directory structure.
- These files **must** be encrypted using `ansible-vault encrypt <file_path>`.
- The CI/CD pipeline will be configured to use a vault password stored securely in the CI/CD platform's secret management system (e.g., GitLab CI Variables, GitHub Secrets). The password will be passed to `ansible-playbook` via the `--vault-password-file` argument.
- For enhanced security, integration with HashiCorp Vault is a future consideration. Ansible would fetch secrets from Vault at runtime, centralizing secret management.

## 6. Playbooks Specification

### 6.1. `site.yml` (Master Playbook)
This is the main entry point for configuring the entire infrastructure. It orchestrates the execution of roles against host groups.

yaml
---
- name: Apply common configuration to all servers
  hosts: all_servers
  roles:
    - common

- name: Configure Nginx Load Balancers
  hosts: web_servers
  roles:
    - role: nginx_lb

- name: Configure PostgreSQL Servers
  hosts: db_primary, db_replicas
  roles:
    - role: postgresql_server

# ... other plays for odoo, n8n, redis, etc. ...

- name: Configure Kubernetes Cluster
  import_playbook: playbooks/provision_kubernetes_cluster.yml

- name: Deploy Monitoring Agents
  hosts: all_servers
  roles:
    - role: prometheus_exporters


### 6.2. `playbooks/patch_management.yml`
This playbook handles system updates and patching as per `DEP-005`.

- **Hosts:** Targets a specific group passed via command-line (`--limit`) or defaults to a safe group.
- **Tasks:**
    - `apt/yum`: Use the appropriate package manager module.
    - Task to check for required reboots after patching.
    - Handlers to perform a managed reboot if necessary.
- **Strategy:** Can be configured with a `serial` keyword to update servers one at a time or in small batches to maintain service availability.

### 6.3. `playbooks/provision_kubernetes_cluster.yml`
This playbook orchestrates the setup of the entire Kubernetes cluster.

- **Plays:**
    1.  **Target `k8s_masters`, `k8s_workers`**: Apply the `kubernetes_common` role.
    2.  **Target `k8s_workers_gpu`**: Apply the `gpu_support` role.
    3.  **Target `k8s_masters`**: Apply the `kubernetes_master` role.
    4.  **Target `k8s_workers`, `k8s_workers_gpu`**: Apply the `kubernetes_worker` role.

## 7. Roles Specification

For each role, the structure will be standard (`tasks`, `handlers`, `templates`, `vars`, `defaults`, `meta`).

### 7.1. `roles/common`
- **Purpose:** Establish a secure and consistent baseline on all servers.
- **Key Tasks:**
    - Set hostname.
    - Update package cache (`apt update`).
    - Install common packages (`htop`, `curl`, `vim`, `ufw`).
    - Configure firewall (UFW) with default deny, allowing SSH.
    - Create `ansible_admin` user with sudo privileges.
    - Harden SSH configuration (`/etc/ssh/sshd_config`): disable root login, password authentication.
    - Configure NTP for time synchronization.

### 7.2. `roles/nginx_lb`
- **Purpose:** Configure Nginx as a high-availability reverse proxy and load balancer.
- **Key Tasks:**
    - Install Nginx.
    - Deploy main `nginx.conf` from a template.
    - Use `template` module to loop through a variable `nginx_sites` and create virtual host configurations in `sites-available`.
    - Each site config will define `upstream` blocks, `server` blocks, `listen` ports, `ssl_certificate` paths, and `location` proxy rules.
    - Enable sites by creating symlinks to `sites-enabled`.
    - Ensure Nginx service is started and enabled.
- **Key Variables:** `nginx_sites` (list of dictionaries, each defining a site), `ssl_cert_path`, `ssl_key_path`.

### 7.3. `roles/postgresql_server`
- **Purpose:** Install and configure PostgreSQL servers.
- **Key Tasks:**
    - Install PostgreSQL server and client packages.
    - Manage `postgresql.conf` and `pg_hba.conf` via templates to configure memory settings, logging, and client authentication.
    - Create application-specific databases and users with specific privileges.
    - Configure streaming replication (primary to replicas) based on host group membership (`db_primary` vs `db_replicas`).
    - Install and configure connection pooler (e.g., PgBouncer).

### 7.4. `roles/kubernetes_*`
- **`kubernetes_common`:** Installs `containerd`, `kubelet`, `kubeadm`, `kubectl`. Configures kernel modules (`br_netfilter`) and sysctl settings.
- **`kubernetes_master`:** Initializes the control plane on the primary master using `kubeadm init`. Stores the join command for other nodes. Applies the CNI manifest (e.g., Calico).
- **`kubernetes_worker`:** Joins the node to the cluster using the stored join command from the master.

### 7.5. `roles/gpu_support`
- **Purpose:** Prepare Kubernetes worker nodes for GPU workloads.
- **Key Tasks:**
    - Install NVIDIA drivers for the specific GPU hardware.
    - Install the NVIDIA Container Toolkit.
    - Deploy the NVIDIA GPU Operator to the Kubernetes cluster, which manages GPU resources and device plugins. This will likely be done by applying a Helm chart or YAML manifest using the `community.kubernetes.k8s` module.

### 7.6. Other Service Roles (`odoo_server`, `n8n_server`, etc.)
- Each role will follow a similar pattern:
    1.  Install necessary dependencies (e.g., Python for Odoo, Node.js for n8n).
    2.  Deploy the application (from a package, git repository, or pre-built artifact).
    3.  Manage configuration files using Jinja2 templates and environment-specific variables.
    4.  Set up a `systemd` service to manage the application process.
    5.  Configure firewall rules as needed.

### 7.7. `roles/prometheus_exporters`
- **Purpose:** Deploy monitoring agents.
- **Key Tasks:**
    - Conditionally deploy specific exporters based on the host's group.
    - Example: `when: "'db_primary' in group_names or 'db_replicas' in group_names"` for `postgres_exporter`.
    - Download exporter binaries, create a system user for them, and configure systemd service files.

## 8. CI/CD Integration

- **Trigger:** The CI/CD pipeline (GitLab CI/CD or GitHub Actions) will trigger on commits and merge requests to main branches.
- **Pipeline Stages:**
    1.  **Lint & Validate:** Run `ansible-lint` and `yamllint` on all YAML files. Run `ansible-playbook --syntax-check` on all playbooks.
    2.  **Test (Dry Run):** Execute `ansible-playbook -i <env_inventory> --check site.yml` against the `staging` environment. This stage verifies that the playbook would run without errors and reports potential changes without making them.
    3.  **Deploy to Staging:** (Requires manual approval) Executes `ansible-playbook -i <staging_inventory> site.yml`.
    4.  **Deploy to Production:** (Requires manual approval & protected branch) Executes `ansible-playbook -i <production_inventory> site.yml` during a scheduled maintenance window.
- **Secrets:** The `ANSIBLE_VAULT_PASSWORD` will be provided to the pipeline as a protected environment variable.

## 9. Disaster Recovery (DR)

- Ansible will be instrumental in the DR strategy.
- The `environments/dr/inventory.ini` file will define the hosts at the DR site.
- The same `site.yml` playbook will be used to configure the DR servers, ensuring consistency with production.
- In a DR event, a specific DR failover playbook will be run. This playbook will:
    - Promote the DR PostgreSQL replica to a primary server.
    - Reconfigure application services to point to the new primary database at the DR site.
    - Update DNS records (potentially via an Ansible module for the DNS provider) to point traffic to the DR site's load balancers.