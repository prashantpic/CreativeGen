# This HCL policy grants full administrative privileges for the Transit secrets engine.
# It is a highly privileged policy and should ONLY be assigned to trusted Vault
# administrators responsible for managing the platform's Key Management Service (KMS).

path "transit/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}