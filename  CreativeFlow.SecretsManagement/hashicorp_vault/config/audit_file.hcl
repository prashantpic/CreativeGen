# Configures a file-based audit device for HashiCorp Vault.
# This ensures all requests to Vault and responses from Vault are logged
# for security, compliance, and auditing purposes.

audit "file_audit_log" {
  type = "file"
  
  options = {
    # The path where the audit log file will be written.
    # The directory must exist, and Vault must have write permissions to it.
    file_path = "/var/log/vault/vault_audit.log"
    
    # Specifies whether to log the raw request and response.
    # Should be "false" in production as it may log sensitive data in responses.
    # Set to "true" only for debugging specific issues under controlled conditions.
    log_raw = "false"
    
    # If set, the accessor of any token, entity, or alias will be HMAC'd before
    # being logged. This prevents an attacker from using accessor values in the
    # audit log to locate all of a particular user's activity.
    hmac_accessor = "true"
    
    # The format for the audit logs. "json" is recommended for easy parsing by
    # log management systems (e.g., SIEM, ELK, Loki).
    format = "json"
    
    # File permissions for the audit log file. "0600" ensures that only the
    # Vault user can read and write the file.
    mode = "0600"
  }
}

# NOTE: Log rotation is not handled by Vault itself for file audit devices.
# An external tool like 'logrotate' must be configured on the host to manage
# the size and retention of the audit log file.