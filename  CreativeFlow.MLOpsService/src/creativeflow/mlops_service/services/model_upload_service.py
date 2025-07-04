"""
Service for handling the upload of AI model artifacts.

This service manages the process of securely uploading model files to object
storage (MinIO), generating a unique storage path for each artifact.
"""
import logging
from typing import BinaryIO
from uuid import UUID

from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.infrastructure.storage.minio_adapter import MinioAdapter

logger = logging.getLogger(__name__)


class ModelUploadService:
    """Manages uploading model files to MinIO."""

    def __init__(self):
        """Initializes the service with a MinioAdapter."""
        settings = get_settings()
        self.storage_adapter = MinioAdapter(settings)
        self.bucket_name = settings.MINIO_MODEL_BUCKET_NAME

    async def upload_model_artifact(
        self, file_stream: BinaryIO, file_name: str, model_id: UUID, version_string: str, content_type: str, file_length: int
    ) -> str:
        """
        Uploads a model artifact to MinIO and returns its path.

        Generates a unique object name path in MinIO, for example:
        `models/{model_id}/{version_string}/{file_name}`

        Args:
            file_stream: The binary IO stream of the file to upload.
            file_name: The original name of the uploaded file.
            model_id: The UUID of the parent model.
            version_string: The version string for this artifact.
            content_type: The MIME type of the file.
            file_length: The length of the file in bytes.

        Returns:
            The full MinIO object path.
        """
        object_path = f"models/{model_id}/{version_string}/{file_name}"
        logger.info(f"Uploading artifact to MinIO path: {self.bucket_name}/{object_path}")
        
        await self.storage_adapter.upload_file(
            bucket_name=self.bucket_name,
            object_name=object_path,
            file_stream=file_stream,
            length=file_length,
            content_type=content_type,
        )
        
        logger.info(f"Successfully uploaded artifact to {object_path}")
        return object_path