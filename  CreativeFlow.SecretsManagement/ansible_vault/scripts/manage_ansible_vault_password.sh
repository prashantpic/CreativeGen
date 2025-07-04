#!/bin/bash
#
# This script provides guidance and helper functions for managing the
# Ansible Vault password securely.
#
# DO NOT store the actual password or password file in version control.
#

echo "Ansible Vault Password Management Guidance"
echo "========================================"
echo "This script demonstrates secure ways to provide the vault password to Ansible."
echo "Choose a method appropriate for your environment and security requirements."
echo ""

# --- Method 1: Password File (For Local Development) ---
#
# Create a file (e.g., ~/.ansible_vault_pass) containing ONLY the password string.
# Secure it: chmod 600 ~/.ansible_vault_pass
# Add it to your global gitignore file to prevent accidental commits.
#
# Then, configure Ansible to use it by adding this to your ansible.cfg:
#
# [defaults]
# vault_password_file = ~/.ansible_vault_pass
#
# Alternatively, use the command-line flag:
# ansible-playbook my_playbook.yml --vault-password-file ~/.ansible_vault_pass
#

# --- Method 2: Environment Variable (Good for CI/CD) ---
#
# Ansible automatically uses the ANSIBLE_VAULT_PASSWORD environment variable if it is set.
# Store the password as a protected/masked CI/CD variable in your pipeline settings.
#
# Example:
# export ANSIBLE_VAULT_PASSWORD="your-very-strong-password-from-ci-secrets"
# ansible-playbook my_playbook.yml
#

# --- Method 3: HashiCorp Vault Integration (Recommended for CI/CD) ---
#
# This is the most secure method. The Ansible Vault password itself is stored in
# HashiCorp Vault and retrieved just-in-time by the CI/CD pipeline or developer.
#
# This requires `vault` and `jq` CLI tools to be installed and configured
# with VAULT_ADDR and a valid VAULT_TOKEN (or other auth method).

# Example helper function to retrieve the password from HashiCorp Vault
get_ansible_vault_password_from_hc_vault() {
  local secret_path="secret/data/cicd/ansible_vault_password"
  local password

  echo "Attempting to retrieve Ansible Vault password from HashiCorp Vault at ${secret_path}..." >&2

  # The '|| true' prevents the script from exiting if vault fails, allowing for error handling
  password=$(vault kv get -format=json "${secret_path}" 2>/dev/null | jq -r '.data.data.password' || true)

  if [[ -z "$password" || "$password" == "null" ]]; then
    echo "Error: Could not retrieve Ansible Vault password from HashiCorp Vault." >&2
    echo "Please ensure you are logged into Vault and have permissions for '${secret_path}'." >&2
    return 1
  fi
  
  echo "$password"
}

# Example usage of the helper function:
#
# echo "Demonstrating retrieval from HashiCorp Vault..."
# ANSIBLE_VAULT_PASS=$(get_ansible_vault_password_from_hc_vault)
#
# if [ $? -eq 0 ]; then
#   echo "Password retrieved successfully."
#   # Using process substitution to provide the password without writing a temp file
#   # ansible-playbook my_playbook.yml --vault-password-file <(echo "$ANSIBLE_VAULT_PASS")
#   echo "You can now run 'ansible-playbook ... --vault-password-file <(echo \$ANSIBLE_VAULT_PASS)'"
# else
#   echo "Failed to get Ansible Vault password. Exiting."
#   exit 1
# fi

echo ""
echo "Script finished."