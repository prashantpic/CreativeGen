#!/usr/bin/env python3
#
# manage_app_users.py
#
# A command-line utility to programmatically manage RabbitMQ users and their
# permissions using the RabbitMQ Management HTTP API. This allows for more
# dynamic or complex configurations than a static definitions.json file.
#
# Dependencies: requests (install via `pip install -r ../requirements.txt`)
#
# Configuration:
# This script requires a `rabbitmq_api_client_config.py` file in the `../config`
# directory. A template `rabbitmq_api_client_config.py.template` is provided.
#
# Usage:
# ./manage_app_users.py --help
# ./manage_app_users.py create --username myapp --tags "management"
# ./manage_app_users.py set-perms --username myapp --vhost myvhost --write ".*"
# ./manage_app_users.py list
# ./manage_app_users.py delete --username myapp

import argparse
import getpass
import json
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing from 'config'
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Please run 'pip install -r ../requirements.txt'", file=sys.stderr)
    sys.exit(1)

try:
    from config.rabbitmq_api_client_config import RABBITMQ_API_CONFIG
except (ImportError, ModuleNotFoundError):
    print("Error: Configuration file 'src/config/rabbitmq_api_client_config.py' not found.", file=sys.stderr)
    print("Please copy 'src/config/rabbitmq_api_client_config.py.template' to it and fill in your details.", file=sys.stderr)
    sys.exit(1)

# --- API Client Functions ---

def _make_request(method, endpoint, payload=None):
    """Helper function to make requests to the RabbitMQ Management API."""
    url = f"{RABBITMQ_API_CONFIG['url']}/api/{endpoint}"
    auth = (RABBITMQ_API_CONFIG['username'], RABBITMQ_API_CONFIG['password'])
    headers = {'content-type': 'application/json'}
    
    try:
        response = requests.request(method, url, auth=auth, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with RabbitMQ API at {url}: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: API returned status {e.response.status_code}", file=sys.stderr)
        print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def create_user(username, password, tags=""):
    """Creates or updates a user."""
    print(f"Creating user '{username}'...")
    payload = {"password": password, "tags": tags}
    response = _make_request('PUT', f"users/{username}", payload=payload)
    if response.status_code == 201:
        print(f"SUCCESS: User '{username}' created.")
    elif response.status_code == 204:
        print(f"SUCCESS: User '{username}' updated.")

def delete_user(username):
    """Deletes a user."""
    print(f"Deleting user '{username}'...")
    _make_request('DELETE', f"users/{username}")
    print(f"SUCCESS: User '{username}' deleted.")

def set_permissions(username, vhost, configure, write, read):
    """Sets permissions for a user on a given vhost."""
    print(f"Setting permissions for user '{username}' on vhost '{vhost}'...")
    payload = {"configure": configure, "write": write, "read": read}
    _make_request('PUT', f"permissions/{vhost}/{username}", payload=payload)
    print("SUCCESS: Permissions set.")

def list_users():
    """Lists all users."""
    response = _make_request('GET', "users")
    users = response.json()
    print(json.dumps(users, indent=2))

def get_user_permissions(username, vhost):
    """Gets permissions for a specific user and vhost."""
    response = _make_request('GET', f"permissions/{vhost}/{username}")
    permissions = response.json()
    print(json.dumps(permissions, indent=2))

# --- Main CLI Logic ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage RabbitMQ users and permissions via the HTTP API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create user command
    p_create = subparsers.add_parser("create", help="Create or update a user.")
    p_create.add_argument("--username", required=True, help="The username to create.")
    p_create.add_argument("--password", help="The user's password. If not provided, will be prompted for.")
    p_create.add_argument("--tags", default="", help="Comma-separated list of tags (e.g., 'administrator,management').")

    # Delete user command
    p_delete = subparsers.add_parser("delete", help="Delete a user.")
    p_delete.add_argument("--username", required=True, help="The username to delete.")

    # Set permissions command
    p_set_perms = subparsers.add_parser("set-perms", help="Set permissions for a user.")
    p_set_perms.add_argument("--username", required=True, help="The user to grant permissions to.")
    p_set_perms.add_argument("--vhost", default=RABBITMQ_API_CONFIG.get('default_vhost', '/'), help="The virtual host.")
    p_set_perms.add_argument("--configure", default="", help="Regex for configure permissions.")
    p_set_perms.add_argument("--write", default="", help="Regex for write permissions.")
    p_set_perms.add_argument("--read", default="", help="Regex for read permissions.")

    # List users command
    p_list = subparsers.add_parser("list", help="List all users.")

    # Get user permissions command
    p_get_perms = subparsers.add_parser("get-perms", help="Get a user's permissions.")
    p_get_perms.add_argument("--username", required=True, help="The user to query.")
    p_get_perms.add_argument("--vhost", default=RABBITMQ_API_CONFIG.get('default_vhost', '/'), help="The virtual host.")
    
    args = parser.parse_args()

    try:
        if args.command == "create":
            password = args.password
            if not password:
                password = getpass.getpass(f"Enter password for user '{args.username}': ")
            create_user(args.username, password, args.tags)
        elif args.command == "delete":
            delete_user(args.username)
        elif args.command == "set-perms":
            set_permissions(args.username, args.vhost, args.configure, args.write, args.read)
        elif args.command == "list":
            list_users()
        elif args.command == "get-perms":
            get_user_permissions(args.username, args.vhost)
    except SystemExit as e:
        # Catch sys.exit calls from _make_request to prevent traceback
        sys.exit(e.code)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)