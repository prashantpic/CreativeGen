"""
Adapter for interacting with MinIO object storage.
"""
import logging
from datetime import timedelta
from io import BytesIO
from typing import BinaryIO

from fastapi.responses import StreamingResponse
from minio import Minio
from minio.error import S3Error

from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.utils.exceptions import ArtifactOperationFailedException

logger = logging.getLogger(__name__)


class MinioAdapter:
    """
    Adapter for MinIO object storage interactions.

    This class provides a clean interface to MinIO for storing and retrieving
    model artifacts, validation reports, and other large files. It handles
    client initialization, connection, and error handling.
    """

    def __init__(self):
        """
        Initializes the MinioAdapter and the MinIO client.
        """
        settings = get_settings()
        try:
            self.client = Minio(
                endpoint=settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY.get_secret_value(),
                secret_key=settings.MINIO_SECRET_KEY.get_secret_value(),
                secure=settings.MINIO_USE_SSL,
            )
            logger.info("MinIO client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}", exc_info=True)
            # In a real app, you might want to handle this more gracefully
            # or prevent the application from starting.
            self.client = None

    def _ensure_bucket_exists(self, bucket_name: str):
        """
        Ensures a bucket exists, creating it if necessary.

        Args:
            bucket_name: The name of the bucket to check/create.
        """
        if self.client:
            found = self.client.bucket_exists(bucket_name)
            if not found:
                self.client.make_bucket(bucket_name)
                logger.info(f"Created MinIO bucket: {bucket_name}")

    async def upload_file(
        self, bucket_name: str, object_name: str, file_stream: BinaryIO, length: int, content_type: str
    ) -> str:
        """
        Uploads a file-like object to a MinIO bucket.

        Args:
            bucket_name: The name of the target bucket.
            object_name: The name/path for the object in the bucket.
            file_stream: The binary stream of the file to upload.
            length: The total length of the file stream.
            content_type: The MIME type of the file.

        Returns:
            The object name (path) of the uploaded file.

        Raises:
            ArtifactOperationFailedException: If the upload fails.
        """
        if not self.client:
            raise ArtifactOperationFailedException("MinIO client is not available.")
        
        try:
            self._ensure_bucket_exists(bucket_name)
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_stream,
                length=length,
                content_type=content_type,
            )
            logger.info(f"Successfully uploaded '{object_name}' to bucket '{bucket_name}'.")
            return object_name
        except S3Error as exc:
            logger.error(f"Error uploading to MinIO: {exc}", exc_info=True)
            raise ArtifactOperationFailedException(f"Failed to upload artifact: {object_name}")

    async def download_file_stream(
        self, bucket_name: str, object_name: str
    ) -> StreamingResponse:
        """
        Downloads a file from MinIO as a streaming response.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name/path of the object to download.

        Returns:
            A FastAPI StreamingResponse containing the file data.

        Raises:
            ArtifactOperationFailedException: If the download fails.
        """
        if not self.client:
            raise ArtifactOperationFailedException("MinIO client is not available.")

        try:
            response = self.client.get_object(bucket_name, object_name)
            return StreamingResponse(response.stream(32 * 1024), media_type=response.headers.get("Content-Type"))
        except S3Error as exc:
            logger.error(f"Error downloading from MinIO: {exc}", exc_info=True)
            if "NoSuchKey" in str(exc):
                 raise ArtifactOperationFailedException(f"Artifact not found: {object_name}", status_code=404)
            raise ArtifactOperationFailedException(f"Failed to download artifact: {object_name}")

    async def delete_file(self, bucket_name: str, object_name: str):
        """
        Deletes a file from a MinIO bucket.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name/path of the object to delete.
        
        Raises:
            ArtifactOperationFailedException: If the deletion fails.
        """
        if not self.client:
            raise ArtifactOperationFailedException("MinIO client is not available.")

        try:
            self.client.remove_object(bucket_name, object_name)
            logger.info(f"Successfully deleted '{object_name}' from bucket '{bucket_name}'.")
        except S3Error as exc:
            logger.error(f"Error deleting from MinIO: {exc}", exc_info=True)
            raise ArtifactOperationFailedException(f"Failed to delete artifact: {object_name}")

    async def get_presigned_url(
        self, bucket_name: str, object_name: str, expires: timedelta = timedelta(hours=1)
    ) -> str:
        """
        Generates a presigned URL for temporary access to an object.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name/path of the object.
            expires: The duration for which the URL is valid.

        Returns:
            A presigned URL string.

        Raises:
            ArtifactOperationFailedException: If URL generation fails.
        """
        if not self.client:
            raise ArtifactOperationFailedException("MinIO client is not available.")
            
        try:
            url = self.client.presigned_get_object(
                bucket_name, object_name, expires=expires
            )
            return url
        except S3Error as exc:
            logger.error(f"Error generating presigned URL: {exc}", exc_info=True)
            raise ArtifactOperationFailedException(f"Failed to generate presigned URL for: {object_name}")