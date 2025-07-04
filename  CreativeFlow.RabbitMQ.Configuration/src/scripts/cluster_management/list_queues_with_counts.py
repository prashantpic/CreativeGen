#!/usr/bin/env python3
#
# list_queues_with_counts.py
#
# A command-line utility to list queues in a RabbitMQ cluster along with their
# message counts, consumer counts, and other key metrics.
#
# It uses the RabbitMQ Management HTTP API.
#
# Dependencies: requests, tabulate (optional)
#
# Configuration:
# This script requires a `rabbitmq_api_client_config.py` file in the `../config`
# directory. A template is provided.

import argparse
import json
import re
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
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    
try:
    from config.rabbitmq_api_client_config import RABBITMQ_API_CONFIG
except (ImportError, ModuleNotFoundError):
    print("Error: Configuration file 'src/config/rabbitmq_api_client_config.py' not found.", file=sys.stderr)
    print("Please copy 'src/config/rabbitmq_api_client_config.py.template' to it and fill in your details.", file=sys.stderr)
    sys.exit(1)


def get_queues(vhost=None):
    """Fetches queue details from the RabbitMQ Management API."""
    api_url = RABBITMQ_API_CONFIG['url']
    auth = (RABBITMQ_API_CONFIG['username'], RABBITMQ_API_CONFIG['password'])
    
    if vhost:
        # VHost must be URL-encoded for the API call
        vhost_encoded = requests.utils.quote(vhost, safe='')
        endpoint = f"/api/queues/{vhost_encoded}"
    else:
        endpoint = "/api/queues"
        
    url = f"{api_url}{endpoint}"
    
    try:
        response = requests.get(url, auth=auth, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with RabbitMQ API at {url}: {e}", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: API returned status {e.response.status_code}", file=sys.stderr)
        print(f"Response: {e.response.text}", file=sys.stderr)
        return None

def display_queues(queues):
    """Formats and prints the list of queues."""
    if not queues:
        print("No queues found matching the criteria.")
        return

    headers = ["VHost", "Queue Name", "State", "Ready", "Unacked", "Total", "Consumers"]
    table_data = []

    for q in queues:
        table_data.append([
            q.get('vhost', 'N/A'),
            q.get('name', 'N/A'),
            q.get('state', 'N/A'),
            q.get('messages_ready', 0),
            q.get('messages_unacknowledged', 0),
            q.get('messages', 0),
            q.get('consumers', 0)
        ])

    if TABULATE_AVAILABLE:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # Fallback to simple aligned text if tabulate is not installed
        print("NOTE: 'tabulate' library not found. Using basic output format.")
        print("Install it with 'pip install tabulate' for a better view.")
        
        col_widths = [len(h) for h in headers]
        for row in table_data:
            for i, cell in enumerate(row):
                if len(str(cell)) > col_widths[i]:
                    col_widths[i] = len(str(cell))

        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * len(header_line))

        for row in table_data:
            row_line = " | ".join(str(c).ljust(w) for c, w in zip(row, col_widths))
            print(row_line)

def main():
    """Main function to parse arguments and orchestrate the script."""
    parser = argparse.ArgumentParser(description="List RabbitMQ queues and their message counts via the HTTP API.")
    parser.add_argument("--vhost", help="Filter by a specific virtual host. If not provided, lists queues across all vhosts.")
    parser.add_argument("--pattern", help="Filter queue names by a regex pattern.")
    
    args = parser.parse_args()

    all_queues = get_queues(args.vhost)

    if all_queues is None:
        sys.exit(1)

    filtered_queues = all_queues
    if args.pattern:
        try:
            regex = re.compile(args.pattern)
            filtered_queues = [q for q in all_queues if regex.search(q.get('name', ''))]
        except re.error as e:
            print(f"Error: Invalid regex pattern '{args.pattern}': {e}", file=sys.stderr)
            sys.exit(1)

    display_queues(filtered_queues)

if __name__ == "__main__":
    main()