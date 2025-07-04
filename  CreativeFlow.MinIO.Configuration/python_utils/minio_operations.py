#
# CreativeFlow.MinIO.Configuration - Python Utilities using MinIO SDK
#
# Requirement Mapping: NFR-004, Section 7.4.1
#
# This module provides Python functions for more complex MinIO operations
# not easily achievable with the 'mc' client.
#
import json
import logging
import os
import sys
from typing import Dict, Optional

from minio import Minio
from minio.error import S3Error

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def connect_client(endpoint: str, access_key: str, secret_key: str, secure: bool = True) -> Optional[Minio]:
    """
    Instantiates and returns a Minio client object.

    Args:
        endpoint: The MinIO server endpoint (e.g., 'localhost:9000').
        access_key: The user's access key.
        secret_key: The user's secret key.
        secure: Flag to use HTTPS (True) or HTTP (False).

    Returns:
        A Minio client object, or None if connection fails.
    """
    logging.info(f"Attempting to connect to MinIO at endpoint: {endpoint}")
    try:
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        # The client is lazy, so we need to perform an action to check the connection
        client.list_buckets()
        logging.info("Successfully connected to MinIO.")
        return client
    except S3Error as exc:
        logging.error(f"Failed to connect to MinIO: {exc}")
        return None
    except Exception as exc:
        logging.error(f"An unexpected error occurred during connection: {exc}")
        return None


def create_bucket_if_not_exists(client: Minio, bucket_name: str) -> bool:
    """
    Creates a bucket idempotently.

    Args:
        client: An initialized Minio client object.
        bucket_name: The name of the bucket to create.

    Returns:
        True if the bucket exists or was created successfully, False otherwise.
    """
    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            logging.info(f"Bucket '{bucket_name}' not found. Creating it...")
            client.make_bucket(bucket_name)
            logging.info(f"Bucket '{bucket_name}' created successfully.")
        else:
            logging.info(f"Bucket '{bucket_name}' already exists.")
        return True
    except S3Error as exc:
        logging.error(f"Error managing bucket '{bucket_name}': {exc}")
        return False


def set_complex_bucket_policy(client: Minio, bucket_name: str, policy_document_str: str) -> None:
    """
    Applies a complex JSON policy to a bucket.

    Args:
        client: An initialized Minio client object.
        bucket_name: The name of the target bucket.
        policy_document_str: A JSON string representing the bucket policy.
    """
    try:
        # Validate that the string is valid JSON
        json.loads(policy_document_str)
        logging.info(f"Applying policy to bucket '{bucket_name}'...")
        client.set_bucket_policy(bucket_name, policy_document_str)
        logging.info(f"Successfully applied policy to bucket '{bucket_name}'.")
    except json.JSONDecodeError:
        logging.error("The provided policy is not a valid JSON string.")
    except S3Error as exc:
        logging.error(f"Failed to set policy for bucket '{bucket_name}': {exc}")


def generate_replication_status_report(client: Minio, bucket_name: str) -> Dict:
    """
    Fetches and summarizes the replication configuration for a bucket.

    Args:
        client: An initialized Minio client object.
        bucket_name: The name of the bucket to inspect.

    Returns:
        A dictionary summarizing the replication rules.
    """
    report = {"bucket": bucket_name, "replication_configured": False, "rules": []}
    logging.info(f"Fetching replication configuration for bucket '{bucket_name}'...")
    try:
        config = client.get_bucket_replication(bucket_name)
        report["replication_configured"] = True
        for rule in config.rules:
            rule_summary = {
                "id": rule.rule_id,
                "status": rule.status,
                "priority": rule.priority,
                "target_bucket": rule.destination.bucket,
                "storage_class": rule.destination.storage_class,
                "filter": str(rule.rule_filter),
            }
            report["rules"].append(rule_summary)
        logging.info(f"Found {len(config.rules)} replication rule(s) for bucket '{bucket_name}'.")
    except S3Error as exc:
        # Specific error code for no replication config
        if "ReplicationConfigurationNotFoundError" in str(exc):
            logging.warning(f"No replication configuration found for bucket '{bucket_name}'.")
        else:
            logging.error(f"Could not retrieve replication config for '{bucket_name}': {exc}")
    return report


if __name__ == "__main__":
    logging.info("--- Running MinIO Python SDK Demonstration ---")

    # Get credentials from environment variables
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

    if not all([MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY]):
        logging.error(
            "Missing environment variables. Please set MINIO_ENDPOINT, MINIO_ACCESS_KEY, and MINIO_SECRET_KEY."
        )
        sys.exit(1)

    # For local testing, endpoint URL might not be secure
    is_secure = not ("localhost" in MINIO_ENDPOINT or "127.0.0.1" in MINIO_ENDPOINT)

    minio_client = connect_client(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=is_secure
    )

    if not minio_client:
        sys.exit(1)

    # --- Demonstrate Functions ---
    
    # 1. Create a test bucket
    test_bucket_name = "python-sdk-test-bucket"
    create_bucket_if_not_exists(minio_client, test_bucket_name)

    # 2. Set a complex policy (example: read-only policy)
    read_only_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{test_bucket_name}/*"],
            }
        ],
    }
    set_complex_bucket_policy(minio_client, test_bucket_name, json.dumps(read_only_policy))

    # 3. Generate a replication status report (will likely be empty unless configured)
    report = generate_replication_status_report(minio_client, test_bucket_name)
    logging.info(f"Replication report for '{test_bucket_name}': {json.dumps(report, indent=2)}")

    logging.info("--- Demonstration Finished ---")