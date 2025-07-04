# Main server configuration for HashiCorp Vault.
# This file defines the core operational parameters for the Vault server instance(s).
# It is loaded by Vault at startup to determine how it operates.

# Listener configuration: Defines where Vault listens for API requests.
# TLS is mandatory for production environments to secure all traffic.
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = false
  tls_cert_file = "/opt/vault/tls/vault.crt" # Path to the Vault server's public TLS certificate.
  tls_key_file  = "/opt/vault/tls/vault.key"  # Path to the Vault server's private TLS key.
}

# Storage backend configuration: Defines where Vault persists its data.
# Raft is used as the integrated storage backend for high availability without external dependencies.
storage "raft" {
  path = "/opt/vault/data"

  # The node_id must be unique for each node in a Raft cluster.
  # It is recommended to set this via an environment variable or a startup script
  # during node provisioning to ensure uniqueness.
  # e.g., node_id = "vault_node_1"
  
  # Example for clustering. Uncomment and configure for each node.
  # retry_join {
  #   leader_api_addr = "https://<vault_node_2_fqdn>:8200"
  #   leader_ca_cert_file = "/opt/vault/tls/ca.pem"
  # }
  # retry_join {
  #   leader_api_addr = "https://<vault_node_3_fqdn>:8200"
  #   leader_ca_cert_file = "/opt/vault/tls/ca.pem"
  # }
}

# The address that should be used for other cluster members to connect to this node.
# This is also the address that will be advertised to clients for redirection.
# Replace <this_node_fqdn_or_lb_ip> with the FQDN or IP of this node or the load balancer.
api_addr = "https://<this_node_fqdn_or_lb_ip>:8200"

# The address to advertise to other Vault servers in the cluster for request forwarding.
# Should be a routable address between the cluster nodes.
# Replace <this_node_internal_ip> with the internal IP of this node.
cluster_addr = "https://<this_node_internal_ip>:8201"

# Enable the web UI.
ui = true

# Telemetry configuration for metrics.
telemetry {
  # To avoid sending the server hostname in telemetry data.
  disable_hostname = true
  
  # If exposing a Prometheus metrics endpoint, define the retention time.
  prometheus_retention_time = "24h"
}

# Disables the server from executing mlock syscall.
# This is recommended for most environments (especially virtualized) to prevent issues
# where Vault's memory is swapped to disk. Ensure swap is disabled or minimized on the host.
disable_mlock = true