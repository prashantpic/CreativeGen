# -*- coding: utf-8 -*-
"""
CreativeFlow.RabbitMQBroker
Script: apply_ha_policies.py
Purpose: Apply RabbitMQ policies from a configuration file.

This script reads a YAML file defining policies (e.g., for High Availability)
and applies them to the RabbitMQ cluster. Applying a policy is an idempotent
operation (PUT).
"""

import argparse
import logging
import os
import sys
import yaml

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


def load_policies_config(config_path: str) -> dict:
    """Loads and parses the YAML policies configuration file."""
    log.info(f"Loading policies configuration from {config_path}...")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        log.info("Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        log.error(f"Configuration file not found at {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        log.error(f"Error parsing YAML file: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Apply RabbitMQ policies from a YAML config file."
    )
    parser.add_argument(
        "--config-file", required=True, help="Path to the YAML policies configuration file."
    )
    args = parser.parse_args()

    if not all([API_URL, API_USER, API_PASSWORD]):
        log.error("Missing required environment variables: RABBITMQ_MANAGEMENT_API_URL, "
                  "RABBITMQ_MANAGEMENT_USER, RABBITMQ_MANAGEMENT_PASSWORD")
        sys.exit(1)
        
    try:
        policies_config = load_policies_config(args.config_file)
        client = RabbitMQApiClient(api_url=API_URL, username=API_USER, password=API_PASSWORD)

        policies = policies_config.get('policies', [])
        if not policies:
            log.warning("No policies found in the configuration file.")
            sys.exit(0)
            
        log.info(f"--- Applying {len(policies)} Policies ---")
        for policy in policies:
            vhost = policy['vhost']
            name = policy['name']
            log.info(f"Applying policy '{name}' to vhost '{vhost}'...")
            client.set_policy(
                vhost=vhost,
                name=name,
                pattern=policy['pattern'],
                definition=policy['definition'],
                priority=policy.get('priority', 0),
                apply_to=policy.get('apply-to', 'all')
            )
            log.info(f"Policy '{name}' applied successfully.")
        
        log.info("\nPolicy application process completed successfully.")

    except HTTPError as e:
        log.error(f"An API error occurred: {e}")
        sys.exit(1)
    except KeyError as e:
        log.error(f"A required key is missing in the policy configuration: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()