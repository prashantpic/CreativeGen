# This file is a conceptual specification for the Database secrets engine.
# It documents the setup for dynamically generating credentials for a PostgreSQL database.
# The commands here should be applied by a script or Terraform.

# --- Enable Database Secrets Engine ---
# Command to enable the database secrets engine at the default path 'database/'.
#
# vault secrets enable database


# --- Configure Database Connection: postgresql-creativeflow ---
# This configures Vault's connection to the PostgreSQL database.
# Vault will use the 'vault_db_manager' user to create and revoke dynamic credentials.
# The password for 'vault_db_manager' must be provided securely and NOT hardcoded here.
#
# vault write database/config/postgresql-creativeflow \
#     plugin_name="postgresql-database-plugin" \
#     connection_url="postgresql://{{username}}:{{password}}@postgres.internal.creativeflow.ai:5432/creativeflow_db?sslmode=verify-full" \
#     allowed_roles="webapp-readwrite,api-readonly" \
#     username="vault_db_manager" \
#     password="<REPLACE_WITH_VAULT_DB_MANAGER_PASSWORD_FROM_SECURE_SOURCE>" \
#     root_rotation_statements=["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]


# --- Define Dynamic Role: webapp-readwrite ---
# This defines a role that applications can request credentials for.
# When an application requests credentials for this role, Vault will execute the
# 'creation_statements' to create a new user with a unique username and password.
# The 'webapp_rw_privs' PostgreSQL role must exist beforehand and have the necessary permissions.
# The generated credentials will have a TTL of 1 hour.
#
# vault write database/roles/webapp-readwrite \
#     db_name="postgresql-creativeflow" \
#     creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT webapp_rw_privs TO \"{{name}}\";" \
#     default_ttl="1h" \
#     max_ttl="8h" \
#     revocation_statements="ALTER ROLE \"{{name}}\" NOLOGIN; SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = '{{name}}'; DROP ROLE IF EXISTS \"{{name}}\";"