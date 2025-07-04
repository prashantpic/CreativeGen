# -*- coding: utf-8 -*-
"""
CreativeFlow.RabbitMQBroker
Script: manage_users.py
Purpose: Command-line interface to manage RabbitMQ users and permissions.

This script uses the RabbitMQ Management HTTP API to perform actions like
adding, deleting, listing users, and setting granular permissions.
It reads API connection details from environment variables.
"""

import argparse
import logging
import os
import sys

from requests.exceptions import HTTPError
from ..utils.rabbitmq_api_client import RabbitMQApiClient

# --- Configuration ---
LOG_LEVEL = os.getenv("PYTHON_SCRIPT_LOG_LEVEL", "INFO").upper()
API_URL = os.getenv("RABBITMQ_MANAGEMENT_API_URL")
API_USER = os.getenv("RABBITMQ_MANAGEMENT_USER")
API_PASSWORD = os.getenv("RABBITMQ_MANAGEMENT_PASSWORD")

# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def setup_arg_parser():
    """Sets up the argument parser for the script."""
    parser = argparse.ArgumentParser(
        description="Manage RabbitMQ users and permissions via the HTTP API."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Add User ---
    parser_add = subparsers.add_parser("add_user", help="Add a new user.")
    parser_add.add_argument("--username", required=True, help="The username to add.")
    parser_add.add_argument("--password", required=True, help="The password for the new user.")
    parser_add.add_argument("--tags", default="", help="Comma-separated list of tags (e.g., administrator,monitoring).")

    # --- Delete User ---
    parser_delete = subparsers.add_parser("delete_user", help="Delete a user.")
    parser_delete.add_argument("--username", required=True, help="The username to delete.")

    # --- List Users ---
    subparsers.add_parser("list_users", help="List all users.")

    # --- Set Permissions ---
    parser_set_perms = subparsers.add_parser("set_permissions", help="Set permissions for a user in a vhost.")
    parser_set_perms.add_argument("--username", required=True, help="The user to grant permissions to.")
    parser_set_perms.add_argument("--vhost", required=True, help="The virtual host for the permissions.")
    parser_set_perms.add_argument("--configure", default="", help="Regex for configure permissions.")
    parser_set_perms.add_argument("--write", default="", help="Regex for write permissions.")
    parser_set_perms.add_argument("--read", default="", help="Regex for read permissions.")

    return parser


def main():
    """Main execution function."""
    # Check for required environment variables
    if not all([API_URL, API_USER, API_PASSWORD]):
        log.error("Missing required environment variables: RABBITMQ_MANAGEMENT_API_URL, "
                  "RABBITMQ_MANAGEMENT_USER, RABBITMQ_MANAGEMENT_PASSWORD")
        sys.exit(1)

    parser = setup_arg_parser()
    args = parser.parse_args()

    try:
        client = RabbitMQApiClient(api_url=API_URL, username=API_USER, password=API_PASSWORD)

        if args.command == "add_user":
            log.info(f"Adding user '{args.username}' with tags '{args.tags}'...")
            client.create_user(username=args.username, password=args.password, tags=args.tags)
            log.info(f"User '{args.username}' added successfully.")

        elif args.command == "delete_user":
            log.info(f"Deleting user '{args.username}'...")
            client.delete_user(username=args.username)
            log.info(f"User '{args.username}' deleted successfully.")

        elif args.command == "list_users":
            log.info("Fetching list of users...")
            users = client.list_users()
            if not users:
                log.info("No users found.")
                return

            print(f"{'Username':<25} {'Tags':<30}")
            print("-" * 55)
            for user in users:
                print(f"{user.get('name', 'N/A'):<25} {user.get('tags', 'N/A'):<30}")

        elif args.command == "set_permissions":
            log.info(f"Setting permissions for user '{args.username}' on vhost '{args.vhost}'...")
            client.set_permissions(
                username=args.username,
                vhost=args.vhost,
                configure_regex=args.configure,
                write_regex=args.write,
                read_regex=args.read
            )
            log.info("Permissions set successfully.")

    except HTTPError as e:
        log.error(f"An API error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()