"""
Adapter for interacting with MinIO object storage.

This class provides a clean, asynchronous interface to the MinIO service
for storing and retrieving model artifacts, validation reports, and other
large files, abstracting away the specifics of the MinIO SDK.
"""
import asyncio
from datetime import timedelta
from io import BytesIO
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error
from starlette.responses import StreamingResponse

from creativeflow.mlops_service.core.config import Settings
from creativeflow.mlops_service.utils.exceptions import ArtifactUploadFailedException


class MinioAdapter:
    """Provides an interface to MinIO for file operations."""

    def __init__(self, settings: Settings):
        """
        Initializes the MinioAdapter.

        Args:
            settings: The application settings containing MinIO credentials.
        """
        self._client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY.get_secret_value(),
            secure=False  # Set to True if using HTTPS
        )

    async def _run_in_thread(self, func, *args, **kwargs):
        """Runs a synchronous function in a separate thread."""
        return await asyncio.to_thread(func, *args, **kwargs)

    async def upload_file(
        self, bucket_name: str, object_name: str, file_stream: BinaryIO, length: int, content_type: str
    ) -> str:
        """
        Uploads a file to a MinIO bucket.

        Args:
            bucket_name: The name of the target bucket.
            object_name: The name of the object to create.
            file_stream: The binary file stream to upload.
            length: The total length of the file stream.
            content_type: The MIME type of the file.

        Returns:
            The ETag of the uploaded object.

        Raises:
            ArtifactUploadFailedException: If the upload fails.
        """
        try:
            # Ensure bucket exists
            found = await self._run_in_thread(self._client.bucket_exists, bucket_name)
            if not found:
                await self._run_in_thread(self._client.make_bucket, bucket_name)

            result = await self._run_in_thread(
                self._client.put_object,
                bucket_name,
                object_name,
                file_stream,
                length,
                content_type
            )
            return result.etag
        except S3Error as exc:
            raise ArtifactUploadFailedException(f"Failed to upload to MinIO: {exc}")

    async def download_file_stream(
        self, bucket_name: str, object_name: str
    ) -> StreamingResponse:
        """
        Downloads a file from MinIO as a streaming response.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name of the object to download.

        Returns:
            A StreamingResponse containing the file data.
            
        Raises:
            ArtifactUploadFailedException: If the download fails.
        """
        try:
            response = await self._run_in_thread(
                self._client.get_object, bucket_name, object_name
            )
            return StreamingResponse(response.stream(32 * 1024), media_type=response.headers.get("Content-Type"))
        except S3Error as exc:
            raise ArtifactUploadFailedException(f"Failed to download from MinIO: {exc}")

    async def delete_file(self, bucket_name: str, object_name: str) -> None:
        """
        Deletes a file from a MinIO bucket.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name of the object to delete.
            
        Raises:
            ArtifactUploadFailedException: If deletion fails.
        """
        try:
            await self._run_in_thread(
                self._client.remove_object, bucket_name, object_name
            )
        except S3Error as exc:
            raise ArtifactUploadFailedException(f"Failed to delete from MinIO: {exc}")

    async def get_presigned_url(
        self, bucket_name: str, object_name: str, expires: timedelta = timedelta(hours=1)
    ) -> str:
        """
        Generates a presigned URL for temporary access to a MinIO object.

        Args:
            bucket_name: The name of the bucket.
            object_name: The name of the object.
            expires: The duration for which the URL is valid.

        Returns:
            The presigned URL string.
            
        Raises:
            ArtifactUploadFailedException: If URL generation fails.
        """
        try:
            url = await self._run_in_thread(
                self._client.presigned_get_object,
                bucket_name,
                object_name,
                expires=expires,
            )
            return url
        except S3Error as exc:
            raise ArtifactUploadFailedException(f"Failed to generate presigned URL: {exc}")