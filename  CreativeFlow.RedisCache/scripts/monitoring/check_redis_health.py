#!/usr/bin/env python3
#
# CreativeFlow.RedisCache - check_redis_health.py
#
# Performs comprehensive health checks on Redis instances (master/replica) and
# Sentinel setups, outputting key metrics.
# Suitable for integration with monitoring systems like Nagios or for producing
# structured JSON for other consumers (e.g., Prometheus textfile collector).
#

import argparse
import json
import sys
import time

try:
    import redis
except ImportError:
    print("Error: The 'redis-py' library is not installed. Please install it using 'pip install redis'.", file=sys.stderr)
    sys.exit(3)


class RedisHealthChecker:
    """Performs health checks directly on a Redis instance."""

    def __init__(self, host, port, password=None):
        """Initializes the checker with connection details."""
        self.host = host
        self.port = int(port)
        self.password = password
        self.client = None

    def _get_redis_connection(self):
        """Establishes and returns a Redis connection, reusing if available."""
        if self.client:
            try:
                if self.client.ping():
                    return self.client
            except redis.exceptions.ConnectionError:
                self.client = None # Stale connection
        
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                socket_connect_timeout=2,
                socket_timeout=2,
                decode_responses=True
            )
            self.client.ping()
            return self.client
        except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError, redis.exceptions.TimeoutError) as e:
            self.error_message = f"Cannot connect to Redis at {self.host}:{self.port}: {e}"
            return None

    def check_instance_liveness(self):
        """Checks if the Redis instance is alive via PING command."""
        client = self._get_redis_connection()
        if not client:
            return {"status": "CRITICAL", "message": self.error_message}
        
        start_time = time.monotonic()
        try:
            if client.ping():
                latency = (time.monotonic() - start_time) * 1000
                return {"status": "OK", "message": f"Instance is alive (PONG), latency: {latency:.2f}ms"}
        except Exception as e:
            return {"status": "CRITICAL", "message": f"PING failed: {e}"}
        
        return {"status": "CRITICAL", "message": "Instance is not responding to PING"}

    def get_instance_info(self, sections=None):
        """Retrieves INFO command output for specified sections."""
        client = self._get_redis_connection()
        if not client:
            return {"status": "CRITICAL", "message": self.error_message, "data": {}}
        
        try:
            if sections:
                if isinstance(sections, str):
                    sections = [sections]
                info_data = {section: client.info(section) for section in sections}
            else:
                info_data = {'default': client.info()}
            return {"status": "OK", "data": info_data}
        except Exception as e:
            return {"status": "CRITICAL", "message": f"Failed to get INFO: {e}", "data": {}}

    def check_replication_status(self):
        """Checks replication status (master/slave, lag)."""
        info_result = self.get_instance_info('replication')
        if info_result['status'] != 'OK':
            return info_result
        
        info = info_result['data']['replication']
        role = info.get('role')
        replication_details = {"role": role}
        status = "OK"

        if role == 'master':
            replication_details['connected_slaves'] = info.get('connected_slaves', 0)
            slaves_info = []
            for i in range(int(replication_details['connected_slaves'])):
                slave_key = f'slave{i}'
                if slave_key in info:
                    slaves_info.append(dict(item.split("=") for item in info[slave_key].split(",")))
            replication_details['slaves'] = slaves_info
        elif role == 'slave':
            replication_details.update({
                'master_host': info.get('master_host'),
                'master_port': info.get('master_port'),
                'master_link_status': info.get('master_link_status'),
                'master_last_io_seconds_ago': int(info.get('master_last_io_seconds_ago', -1)),
                'master_sync_in_progress': info.get('master_sync_in_progress') == '1',
            })
            if replication_details['master_link_status'] != 'up':
                status = "CRITICAL"
        
        return {"status": status, "data": replication_details}


class SentinelHealthChecker:
    """Performs health checks on a Redis Sentinel setup."""

    def __init__(self, sentinel_host, sentinel_port, master_name, sentinel_password=None):
        """Initializes the checker with Sentinel connection details."""
        self.sentinel_host = sentinel_host
        self.sentinel_port = int(sentinel_port)
        self.master_name = master_name
        self.sentinel_password = sentinel_password
        self.sentinel_client = None

    def _get_sentinel_connection(self):
        """Establishes and returns a Redis Sentinel connection."""
        if self.sentinel_client:
            try:
                if self.sentinel_client.ping():
                    return self.sentinel_client
            except redis.exceptions.ConnectionError:
                self.sentinel_client = None

        try:
            self.sentinel_client = redis.Redis(
                host=self.sentinel_host,
                port=self.sentinel_port,
                password=self.sentinel_password,
                socket_connect_timeout=2,
                socket_timeout=2,
                decode_responses=True
            )
            self.sentinel_client.ping()
            return self.sentinel_client
        except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError, redis.exceptions.TimeoutError) as e:
            self.error_message = f"Cannot connect to Sentinel at {self.sentinel_host}:{self.sentinel_port}: {e}"
            return None

    def check_sentinel_master_status(self):
        """Checks the status of the master monitored by Sentinel."""
        s = self._get_sentinel_connection()
        if not s:
            return {"status": "CRITICAL", "message": self.error_message, "data": {}}
        
        try:
            master_info = s.sentinel_master(self.master_name)
            status = "OK"
            if 's_down' in master_info.get('flags', '') or 'o_down' in master_info.get('flags', ''):
                status = "CRITICAL"
            return {"status": status, "data": master_info}
        except redis.exceptions.ResponseError:
            return {"status": "CRITICAL", "message": f"Sentinel master '{self.master_name}' not found.", "data": {}}
        except Exception as e:
            return {"status": "CRITICAL", "message": f"Failed to get Sentinel master info for '{self.master_name}': {e}", "data": {}}

    def check_sentinel_slaves_status(self):
        """Checks the status of slaves for the monitored master."""
        s = self._get_sentinel_connection()
        if not s:
            return {"status": "WARNING", "message": self.error_message, "data": []}
        
        try:
            slaves_info = s.sentinel_slaves(self.master_name)
            return {"status": "OK", "data": slaves_info}
        except Exception as e:
            return {"status": "WARNING", "message": f"Failed to get Sentinel slaves info for '{self.master_name}': {e}", "data": []}


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Redis and Sentinel Health Checker.", formatter_class=argparse.RawTextHelpFormatter)
    
    # Redis Instance arguments
    parser.add_argument("--host", default="localhost", help="Redis server host (default: localhost)")
    parser.add_argument("--port", default=6379, type=int, help="Redis server port (default: 6379)")
    parser.add_argument("--password", help="Redis server password (reads from REDIS_PASSWORD env var if not set)")
    
    # Sentinel arguments
    parser.add_argument("--sentinel-host", help="Sentinel host")
    parser.add_argument("--sentinel-port", default=26379, type=int, help="Sentinel port (default: 26379)")
    parser.add_argument("--sentinel-master-name", help="Name of the master monitored by Sentinel")
    parser.add_argument("--sentinel-password", help="Sentinel server password (for Sentinel auth)")

    # Control arguments
    parser.add_argument("--output-format", choices=['json', 'nagios'], default='json', help="Output format (default: json)")
    parser.add_argument("--check-type", 
                        choices=['instance', 'replication', 'sentinel-master', 'sentinel-slaves', 'all-instance', 'all-sentinel'],
                        required=True, help="Type of check to perform:\n"
                        "  instance: Basic liveness check of a Redis instance.\n"
                        "  replication: Replication status of a Redis instance.\n"
                        "  sentinel-master: Status of a master via Sentinel.\n"
                        "  sentinel-slaves: Status of slaves via Sentinel.\n"
                        "  all-instance: All checks for a single Redis instance.\n"
                        "  all-sentinel: All checks via Sentinel.")

    args = parser.parse_args()
    results = {}

    # Instance Checks
    if args.check_type in ['instance', 'replication', 'all-instance']:
        redis_checker = RedisHealthChecker(args.host, args.port, args.password)
        if args.check_type in ['instance', 'all-instance']:
            results['liveness'] = redis_checker.check_instance_liveness()
        if args.check_type in ['replication', 'all-instance']:
            results['replication'] = redis_checker.check_replication_status()
        if args.check_type == 'all-instance':
            results['info_summary'] = redis_checker.get_instance_info(['server', 'clients', 'memory', 'persistence', 'stats', 'cpu'])

    # Sentinel Checks
    if args.check_type in ['sentinel-master', 'sentinel-slaves', 'all-sentinel']:
        if not args.sentinel_host or not args.sentinel_master_name:
            print("CRITICAL: --sentinel-host and --sentinel-master-name are required for Sentinel checks.", file=sys.stderr)
            sys.exit(2)
        sentinel_checker = SentinelHealthChecker(args.sentinel_host, args.sentinel_port, args.sentinel_master_name, args.sentinel_password)
        if args.check_type in ['sentinel-master', 'all-sentinel']:
            results['sentinel_master_status'] = sentinel_checker.check_sentinel_master_status()
        if args.check_type in ['sentinel-slaves', 'all-sentinel']:
            results['sentinel_slaves_status'] = sentinel_checker.check_sentinel_slaves_status()

    # Output generation
    if args.output_format == 'json':
        print(json.dumps(results, indent=2))
    elif args.output_format == 'nagios':
        overall_status_code = 0 # OK
        messages = []
        
        if not results:
            print("UNKNOWN: No checks were performed.")
            sys.exit(3)

        for key, res_dict in results.items():
            if isinstance(res_dict, dict) and 'status' in res_dict:
                status = res_dict['status']
                msg = res_dict.get('message', f"{key} status is {status}")
                messages.append(msg)
                if status == 'CRITICAL':
                    overall_status_code = 2
                elif status == 'WARNING' and overall_status_code < 2:
                    overall_status_code = 1
        
        status_text_map = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}
        overall_status_text = status_text_map[overall_status_code]
        
        summary_message = f"{overall_status_text}: {'; '.join(messages)}"
        print(summary_message)
        sys.exit(overall_status_code)

if __name__ == "__main__":
    main()