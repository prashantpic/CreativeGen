# -*- coding: utf-8 -*-
"""
CreativeFlow.RabbitMQBroker
Script: declare_entities.py
Purpose: Idempotently declare RabbitMQ entities from a configuration file.

This script reads a YAML file defining vhosts, exchanges, queues, and bindings,
and ensures they exist in the RabbitMQ cluster. It checks for existence before
creating to avoid errors on re-runs.
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


def load_topology_config(config_path: str) -> dict:
    """Loads and parses the YAML topology configuration file."""
    log.info(f"Loading topology configuration from {config_path}...")
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


def apply_topology(client: RabbitMQApiClient, config: dict):
    """
    Applies the topology defined in the config to the RabbitMQ cluster.

    Args:
        client: An instance of RabbitMQApiClient.
        config: The parsed topology configuration dictionary.
    """
    # 1. Declare VHosts
    vhosts_config = config.get('vhosts', [])
    log.info(f"--- Processing {len(vhosts_config)} VHosts ---")
    for vhost in vhosts_config:
        name = vhost['name']
        if client.get_vhost(name):
            log.info(f"VHost '{name}' already exists. Skipping.")
        else:
            log.info(f"Creating VHost '{name}'...")
            client.create_vhost(name)
    
    # 2. Declare Exchanges
    exchanges_config = config.get('exchanges', [])
    log.info(f"\n--- Processing {len(exchanges_config)} Exchanges ---")
    for ex in exchanges_config:
        vhost, name = ex['vhost'], ex['name']
        existing_exchanges = {e['name'] for e in client.list_exchanges(vhost)}
        if name in existing_exchanges:
            log.info(f"Exchange '{name}' in vhost '{vhost}' already exists. Skipping.")
        else:
            log.info(f"Creating exchange '{name}' in vhost '{vhost}'...")
            client.create_exchange(
                vhost=vhost,
                name=name,
                type=ex.get('type', 'direct'),
                durable=ex.get('durable', True),
                auto_delete=ex.get('auto_delete', False),
                internal=ex.get('internal', False),
                arguments=ex.get('arguments')
            )

    # 3. Declare Queues
    queues_config = config.get('queues', [])
    log.info(f"\n--- Processing {len(queues_config)} Queues ---")
    for q in queues_config:
        vhost, name = q['vhost'], q['name']
        existing_queues = {qu['name'] for qu in client.list_queues(vhost)}
        if name in existing_queues:
            log.info(f"Queue '{name}' in vhost '{vhost}' already exists. Skipping.")
        else:
            log.info(f"Creating queue '{name}' in vhost '{vhost}'...")
            client.create_queue(
                vhost=vhost,
                name=name,
                durable=q.get('durable', True),
                auto_delete=q.get('auto_delete', False),
                arguments=q.get('arguments')
            )
            
    # 4. Declare Bindings
    bindings_config = config.get('bindings', [])
    log.info(f"\n--- Processing {len(bindings_config)} Bindings ---")
    for b in bindings_config:
        log.info(f"Creating binding: {b['source_exchange']} -> {b['destination_name']} "
                 f"in vhost '{b['vhost']}' with key '{b.get('routing_key', '')}'...")
        client.create_binding(
            vhost=b['vhost'],
            source_exchange=b['source_exchange'],
            destination_type=b.get('destination_type', 'queue'),
            destination_name=b['destination_name'],
            routing_key=b.get('routing_key', ''),
            arguments=b.get('arguments')
        )

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Declare RabbitMQ entities (vhosts, queues, etc.) from a YAML config file."
    )
    parser.add_argument(
        "--config-file", required=True, help="Path to the YAML topology configuration file."
    )
    args = parser.parse_args()

    if not all([API_URL, API_USER, API_PASSWORD]):
        log.error("Missing required environment variables: RABBITMQ_MANAGEMENT_API_URL, "
                  "RABBITMQ_MANAGEMENT_USER, RABBITMQ_MANAGEMENT_PASSWORD")
        sys.exit(1)

    try:
        topology_config = load_topology_config(args.config_file)
        client = RabbitMQApiClient(api_url=API_URL, username=API_USER, password=API_PASSWORD)
        apply_topology(client, topology_config)
        log.info("\nTopology declaration process completed successfully.")

    except HTTPError as e:
        log.error(f"An API error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()