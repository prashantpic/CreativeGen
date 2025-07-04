# This is a generic configuration file for the HashiCorp Vault Agent.
# It can be adapted for different use cases, such as running as a sidecar
# in Kubernetes or as a daemon on a virtual machine.

# Path to the agent's process ID file.
pid_file = "/var/run/vault-agent/vault-agent.pid"

# Main Vault server connection details.
vault {
  # The address of the Vault server or cluster.
  address = "https://vault.creativeflow.ai:8200"

  # For production, if Vault's TLS certificate is signed by a private CA,
  # specify the path to that CA certificate file.
  # tls_ca_cert = "/etc/vault-agent/ca.pem"

  # Do not use in production. Only for development with self-signed certs.
  # tls_skip_verify = true
}

# Auto-Auth configuration enables the agent to authenticate automatically.
# Only one 'method' block should be active at a time.
auto_auth {
  # --- AppRole Method ---
  # Use this method for applications running on VMs or in environments
  # where AppRole credentials can be securely provided.
  method "approle" {
    mount_path = "auth/approle"
    config = {
      # Path to the file containing the RoleID. This file should be deployed
      # with the application and have restricted read permissions.
      role_id_file_path = "/etc/vault-agent/role_id"

      # Path to the file containing the SecretID. This file should be
      # securely delivered to the application at startup (e.g., by a CI/CD pipeline).
      secret_id_file_path = "/etc/vault-agent/secret_id"

      # For enhanced security, remove the SecretID file after the agent reads it once.
      # This is highly recommended if the SecretID is single-use.
      remove_secret_id_file_after_read = true
    }
  }

  # --- Kubernetes Method (Example) ---
  # Use this method for applications running as pods in Kubernetes.
  # method "kubernetes" {
  #   mount_path = "auth/kubernetes"
  #   config = {
  #     # The name of the Vault role to authenticate against.
  #     role = "my-app-role-for-k8s-auth"
  #     
  #     # The path to the Kubernetes Service Account token is usually auto-detected
  #     # by the agent when running inside a pod.
  #   }
  # }
}

# Cache configuration allows the agent to cache tokens and secrets.
cache {
  # Use the token generated by the auto-auth method for caching.
  use_auto_auth_token = true
}

# A listener block can be configured to create a local proxy for applications
# that are Vault-aware, reducing the need for every app to know the Vault address.
# listener "tcp" {
#   address = "127.0.0.1:8100"
#   tls_disable = true
# }

# --- Template Stanza ---
# Defines how the agent retrieves a secret and renders it into a file.
# Multiple template blocks can be defined.
template {
  # Path to the source template file (e.g., vault_agent_template_app_db.ctmpl).
  source      = "/etc/vault-agent/templates/db_config.ctmpl"
  
  # Path to the destination file where the rendered secret will be written.
  destination = "/srv/my_app/config/database.ini"

  # Permissions for the destination file. Should be as restrictive as possible.
  perms       = "0640"

  # Optional command to run after the template is successfully rendered.
  # Useful for signaling an application to reload its configuration.
  command     = "systemctl reload my-app.service"
}

# --- Secret Stanza ---
# Directly renders a secret's value to a file without a template.
# This is useful for simple secrets like an API key.
#
# secret {
#   destination = "/etc/my-app/api_key.txt"
#   perms = "0600"
#   template = <<EOTPL
#   {{- with secret "secret/data/apps/webapp/production/api_keys" -}}
#   {{ .Data.data.openai_key }}
#   {{- end -}}
#   EOTPL
# }