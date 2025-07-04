# This HCL policy file grants necessary permissions for CI/CD systems
# (e.g., GitLab CI, GitHub Actions) to perform deployment tasks securely.

# Allow reading and listing secrets stored in the dedicated CI/CD path.
# This could include Docker registry credentials, deployment tokens, etc.
path "secret/data/cicd/*" {
  capabilities = ["read", "list"]
}

# Allow the CI/CD pipeline to provision a short-lived, single-use SecretID
# for an application's AppRole during its deployment process. This is a secure
# way to bootstrap applications.
path "auth/approle/role/webapp-prod-role/secret-id" {
  capabilities = ["create", "update"]
}

# Allow the CI/CD pipeline to read the RoleID of the application it is deploying.
# The RoleID is generally considered non-sensitive.
path "auth/approle/role/webapp-prod-role/role-id" {
  capabilities = ["read"]
}

# Allow the CI/CD pipeline to read application secrets for specific environments.
# This is necessary to inject configuration into deployment manifests or environments.
path "secret/data/webapp/staging/*" {
  capabilities = ["read"]
}

path "secret/data/webapp/production/*" {
  capabilities = ["read"]
}