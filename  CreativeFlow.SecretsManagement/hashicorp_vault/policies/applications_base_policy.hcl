# This HCL policy file grants foundational permissions for applications.
# It is intended to be combined with more specific policies that grant access
# to application-specific secret paths.
# This approach follows the principle of least privilege by composing policies.

# Allow reading secrets from a common path available to all applications.
path "secret/data/common/*" {
  capabilities = ["read"]
}

# Allow use of the 'app-general-encryption-key' from the transit secrets engine
# for cryptographic operations. "update" capability is required for encrypt/decrypt.
path "transit/encrypt/app-general-encryption-key" {
  capabilities = ["update"]
}

path "transit/decrypt/app-general-encryption-key" {
  capabilities = ["update"]
}