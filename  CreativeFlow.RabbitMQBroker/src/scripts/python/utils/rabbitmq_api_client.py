# -*- coding: utf-8 -*-
"""
CreativeFlow.RabbitMQBroker
Module: rabbitmq_api_client
Purpose: A reusable client for interacting with the RabbitMQ Management HTTP API.

This module provides a Python class, `RabbitMQApiClient`, that encapsulates
the logic for making authenticated requests to the RabbitMQ Management API.
It is designed to be used by other management and monitoring scripts within this repository.
"""

import logging
from typing import Optional, Dict, Any, List
from urllib.parse import quote

import requests

log = logging.getLogger(__name__)


class RabbitMQApiClient:
    """
    A client for the RabbitMQ Management HTTP API.
    Handles authentication, request signing, and response parsing.
    """

    def __init__(self, api_url: str, username: str, password: str):
        """
        Initializes the RabbitMQ API client.

        Args:
            api_url (str): The base URL of the RabbitMQ Management API (e.g., http://localhost:15672).
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        if not api_url.endswith('/'):
            api_url += '/'
        self._api_url = api_url
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._session.headers.update({"User-Agent": "CreativeFlow-RabbitMQBroker-Client/1.0"})
        log.info(f"RabbitMQApiClient initialized for API URL: {self._api_url}")

    def _request(self, method: str, path: str, json_payload: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        Private helper for making HTTP requests to the API.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'PUT', 'POST', 'DELETE').
            path (str): The API endpoint path (e.g., 'api/overview').
            json_payload (Optional[Dict[str, Any]]): A dictionary to be sent as the JSON body.
            params (Optional[Dict[str, Any]]): A dictionary of URL parameters.

        Returns:
            Optional[Any]: The parsed JSON response, or None if the response has no content.

        Raises:
            requests.exceptions.RequestException: For connection errors or HTTP status code errors.
        """
        full_url = self._api_url + path
        try:
            log.debug(f"Request: {method} {full_url} | Payload: {json_payload}")
            response = self._session.request(method, full_url, json=json_payload, params=params)
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses

            if response.status_code == 204:  # No Content
                return None
            return response.json()
        except requests.exceptions.HTTPError as e:
            log.error(f"HTTP Error for {method} {full_url}: {e.response.status_code} {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            log.error(f"Request failed for {method} {full_url}: {e}")
            raise

    # --- VHOSTS ---
    def list_vhosts(self) -> List[Dict[str, Any]]:
        return self._request('GET', 'api/vhosts')

    def get_vhost(self, vhost_name: str) -> Optional[Dict[str, Any]]:
        encoded_vhost = quote(vhost_name, safe='')
        try:
            return self._request('GET', f'api/vhosts/{encoded_vhost}')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def create_vhost(self, vhost_name: str) -> None:
        encoded_vhost = quote(vhost_name, safe='')
        self._request('PUT', f'api/vhosts/{encoded_vhost}')

    def delete_vhost(self, vhost_name: str) -> None:
        encoded_vhost = quote(vhost_name, safe='')
        self._request('DELETE', f'api/vhosts/{encoded_vhost}')

    # --- USERS & PERMISSIONS ---
    def list_users(self) -> List[Dict[str, Any]]:
        return self._request('GET', 'api/users')
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        encoded_user = quote(username, safe='')
        try:
            return self._request('GET', f'api/users/{encoded_user}')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def create_user(self, username: str, password: str, tags: str = "") -> None:
        encoded_user = quote(username, safe='')
        payload = {"password": password, "tags": tags}
        self._request('PUT', f'api/users/{encoded_user}', json_payload=payload)

    def delete_user(self, username: str) -> None:
        encoded_user = quote(username, safe='')
        self._request('DELETE', f'api/users/{encoded_user}')
        
    def set_permissions(self, username: str, vhost: str, configure_regex: str, write_regex: str, read_regex: str) -> None:
        encoded_user = quote(username, safe='')
        encoded_vhost = quote(vhost, safe='')
        payload = {"configure": configure_regex, "write": write_regex, "read": read_regex}
        self._request('PUT', f'api/permissions/{encoded_vhost}/{encoded_user}', json_payload=payload)

    # --- EXCHANGES, QUEUES, BINDINGS ---
    def list_exchanges(self, vhost: str) -> List[Dict[str, Any]]:
        encoded_vhost = quote(vhost, safe='')
        return self._request('GET', f'api/exchanges/{encoded_vhost}')

    def create_exchange(self, vhost: str, name: str, type: str, durable: bool, auto_delete: bool, internal: bool = False, arguments: Optional[Dict] = None) -> None:
        encoded_vhost = quote(vhost, safe='')
        encoded_name = quote(name, safe='')
        payload = {"type": type, "durable": durable, "auto_delete": auto_delete, "internal": internal, "arguments": arguments or {}}
        self._request('PUT', f'api/exchanges/{encoded_vhost}/{encoded_name}', json_payload=payload)

    def list_queues(self, vhost: str) -> List[Dict[str, Any]]:
        encoded_vhost = quote(vhost, safe='')
        return self._request('GET', f'api/queues/{encoded_vhost}')

    def create_queue(self, vhost: str, name: str, durable: bool, auto_delete: bool, arguments: Optional[Dict] = None) -> None:
        encoded_vhost = quote(vhost, safe='')
        encoded_name = quote(name, safe='')
        payload = {"durable": durable, "auto_delete": auto_delete, "arguments": arguments or {}}
        self._request('PUT', f'api/queues/{encoded_vhost}/{encoded_name}', json_payload=payload)

    def create_binding(self, vhost: str, source_exchange: str, destination_type: str, destination_name: str, routing_key: str, arguments: Optional[Dict] = None) -> None:
        encoded_vhost = quote(vhost, safe='')
        encoded_source = quote(source_exchange, safe='')
        encoded_dest = quote(destination_name, safe='')
        dest_type_char = 'q' if destination_type == 'queue' else 'e'
        payload = {"routing_key": routing_key, "arguments": arguments or {}}
        self._request('POST', f'api/bindings/{encoded_vhost}/e/{encoded_source}/{dest_type_char}/{encoded_dest}', json_payload=payload)

    # --- POLICIES ---
    def list_policies(self, vhost: str) -> List[Dict[str, Any]]:
        encoded_vhost = quote(vhost, safe='')
        return self._request('GET', f'api/policies/{encoded_vhost}')

    def set_policy(self, vhost: str, name: str, pattern: str, definition: Dict, priority: int = 0, apply_to: str = "all") -> None:
        encoded_vhost = quote(vhost, safe='')
        encoded_name = quote(name, safe='')
        payload = {"pattern": pattern, "definition": definition, "priority": priority, "apply-to": apply_to}
        self._request('PUT', f'api/policies/{encoded_vhost}/{encoded_name}', json_payload=payload)

    # --- MONITORING ---
    def get_overview(self) -> Dict[str, Any]:
        return self._request('GET', 'api/overview')

    def get_nodes(self) -> List[Dict[str, Any]]:
        return self._request('GET', 'api/nodes')

    def get_queue_metrics(self, vhost: str, queue_name: str) -> Optional[Dict[str, Any]]:
        encoded_vhost = quote(vhost, safe='')
        encoded_queue = quote(queue_name, safe='')
        try:
            return self._request('GET', f'api/queues/{encoded_vhost}/{encoded_queue}')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise