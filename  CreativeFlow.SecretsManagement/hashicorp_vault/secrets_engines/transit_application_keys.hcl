# This file is a conceptual specification for the Transit secrets engine (EaaS).
# It documents the setup and key creation for providing centralized cryptographic
# operations to applications. The commands here should be applied by a script or Terraform.

# --- Enable Transit Secrets Engine ---
# Command to enable the transit secrets engine at the path 'transit/'.
#
# vault secrets enable -path=transit transit


# --- Create Standard Encryption Key: app-general-encryption-key ---
# This key is for general-purpose application data encryption.
# It is non-exportable and does not allow plaintext backup, which is the most secure configuration.
#
# vault write -f transit/keys/app-general-encryption-key \
#     type=aes256-gcm96 \
#     exportable=false \
#     allow_plaintext_backup=false

# Configure automatic key rotation for the general purpose key (e.g., every 30 days).
# Applications will automatically use the new key version for encryption.
# Decryption of data encrypted with older versions will still work seamlessly.
#
# vault write transit/keys/app-general-encryption-key/config rotation_period=2592000s


# --- Create Derived Encryption Key: user-auth-token-encryption-key ---
# This key uses 'derived' mode, enabling convergent encryption. It means that the same
# input plaintext with the same context will produce the same ciphertext. This can be
# useful for encrypting data that needs to be looked up in its encrypted form,
# such as certain types of tokens where the encrypted value itself is an index.
#
# vault write -f transit/keys/user-auth-token-encryption-key \
#     type=aes256-gcm96 \
#     derived=true