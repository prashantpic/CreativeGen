# -*- coding: utf-8 -*-
"""
CreativeFlow.RabbitMQBroker
Script: export_metrics.py
Purpose: Export RabbitMQ metrics for Prometheus consumption.

This script can run in two modes:
1. HTTP Server Mode: Exposes a /metrics endpoint for Prometheus to scrape.
2. File Mode: Writes metrics to a file for consumption by node_exporter's
   textfile collector.
"""

import argparse
import logging
import os
import sys
import tempfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from ..utils.rabbitmq_api_client import RabbitMQApiClient

# --- Configuration ---
LOG_LEVEL = os.getenv("PYTHON_SCRIPT_LOG_LEVEL", "INFO").upper()
API_URL = os.getenv("RABBITMQ_MANAGEMENT_API_URL")
API_USER = os.getenv("RABBITMQ_MANAGEMENT_USER")
API_PASSWORD = os.getenv("RABBITMQ_MANAGEMENT_PASSWORD")

# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def generate_metrics_text(client: RabbitMQApiClient) -> str:
    """
    Fetches data from RabbitMQ Management API and formats it as Prometheus metrics.
    """
    metrics = []

    try:
        # --- Overview Metrics ---
        overview = client.get_overview()
        if overview:
            metrics.append(f'rabbitmq_overview_messages_ready {overview.get("queue_totals", {}).get("messages_ready", 0)}')
            metrics.append(f'rabbitmq_overview_messages_unacked {overview.get("queue_totals", {}).get("messages_unacknowledged", 0)}')
            metrics.append(f'rabbitmq_connections_total {overview.get("object_totals", {}).get("connections", 0)}')
            metrics.append(f'rabbitmq_channels_total {overview.get("object_totals", {}).get("channels", 0)}')
            metrics.append(f'rabbitmq_queues_total {overview.get("object_totals", {}).get("queues", 0)}')

        # --- Node Metrics ---
        nodes = client.get_nodes()
        if nodes:
            for node in nodes:
                node_name = node.get("name", "unknown")
                labels = f'{{node="{node_name}"}}'
                metrics.append(f'rabbitmq_node_disk_free_bytes{labels} {node.get("disk_free", 0)}')
                metrics.append(f'rabbitmq_node_mem_used_bytes{labels} {node.get("mem_used", 0)}')
                metrics.append(f'rabbitmq_node_fd_used{labels} {node.get("fd_used", 0)}')
                metrics.append(f'rabbitmq_node_sockets_used{labels} {node.get("sockets_used", 0)}')
                metrics.append(f'rabbitmq_node_running{labels} {1 if node.get("running") else 0}')

        # --- Per-Queue Metrics ---
        vhosts = client.list_vhosts()
        if vhosts:
            for vhost_info in vhosts:
                vhost_name = vhost_info['name']
                queues = client.list_queues(vhost_name)
                for queue in queues:
                    q_name = queue.get("name")
                    labels = f'{{vhost="{vhost_name}",queue="{q_name}"}}'
                    metrics.append(f'rabbitmq_queue_messages_ready{labels} {queue.get("messages_ready", 0)}')
                    metrics.append(f'rabbitmq_queue_messages_unacked{labels} {queue.get("messages_unacknowledged", 0)}')
                    metrics.append(f'rabbitmq_queue_consumers{labels} {queue.get("consumers", 0)}')
                    metrics.append(f'rabbitmq_queue_messages_total{labels} {queue.get("messages", 0)}')

    except Exception as e:
        log.error(f"Failed to fetch metrics from RabbitMQ API: {e}")
        # Add a metric to indicate the exporter is failing
        metrics.append('rabbitmq_exporter_scrape_success 0')
    else:
        metrics.append('rabbitmq_exporter_scrape_success 1')

    return "\n".join(metrics) + "\n"


class MetricsRequestHandler(BaseHTTPRequestHandler):
    """A handler for serving Prometheus metrics."""
    def do_GET(self):
        if self.path == '/metrics':
            try:
                client = self.server.api_client
                metrics_text = generate_metrics_text(client)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; version=0.0.4')
                self.end_headers()
                self.wfile.write(metrics_text.encode('utf-8'))
            except Exception as e:
                log.error(f"Error handling /metrics request: {e}")
                self.send_error(500, "Internal Server Error")
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        # Suppress the default verbose logging of http.server
        return


def run_http_server(client: RabbitMQApiClient, port: int):
    """Runs the metrics exporter as an HTTP server."""
    log.info(f"Starting Prometheus metrics exporter on port {port}")
    server_address = ('', port)
    
    class CustomHTTPServer(HTTPServer):
        def __init__(self, *args, **kwargs):
            self.api_client = client
            super().__init__(*args, **kwargs)
            
    httpd = CustomHTTPServer(server_address, MetricsRequestHandler)
    httpd.serve_forever()


def run_file_exporter(client: RabbitMQApiClient, output_file: str, interval: int):
    """Runs the metrics exporter in file mode."""
    log.info(f"Starting Prometheus metrics file exporter to {output_file} every {interval}s")
    while True:
        try:
            metrics_text = generate_metrics_text(client)
            # Write to a temporary file and then atomically rename it
            # This prevents Prometheus from reading a partially written file
            fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(output_file))
            with os.fdopen(fd, 'w') as f:
                f.write(metrics_text)
            os.rename(temp_path, output_file)
            log.debug(f"Metrics written to {output_file}")
        except Exception as e:
            log.error(f"Failed to write metrics to file: {e}")
        time.sleep(interval)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Export RabbitMQ metrics for Prometheus.")
    parser.add_argument("--mode", choices=['http', 'file'], default='http',
                        help="Exporter mode: 'http' (default) or 'file'.")
    parser.add_argument("--port", type=int, default=9419,
                        help="Port to listen on for HTTP mode.")
    parser.add_argument("--output-file", help="Path to write metrics to in file mode.")
    parser.add_argument("--interval", type=int, default=15,
                        help="Scrape interval in seconds for file mode.")

    args = parser.parse_args()

    if args.mode == 'file' and not args.output_file:
        parser.error("--output-file is required for file mode.")
        
    if not all([API_URL, API_USER, API_PASSWORD]):
        log.error("Missing required environment variables: RABBITMQ_MANAGEMENT_API_URL, "
                  "RABBITMQ_MANAGEMENT_USER, RABBITMQ_MANAGEMENT_PASSWORD")
        sys.exit(1)

    try:
        api_client = RabbitMQApiClient(api_url=API_URL, username=API_USER, password=API_PASSWORD)
        
        if args.mode == 'http':
            run_http_server(api_client, args.port)
        elif args.mode == 'file':
            run_file_exporter(api_client, args.output_file, args.interval)

    except KeyboardInterrupt:
        log.info("Exporter shutting down.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()