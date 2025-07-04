"""
Service for orchestrating AI model validation and security scanning.

This service manages the validation pipeline for models, including triggering
security scans, functional tests, and performance benchmarks. It uses background
tasks to handle these potentially long-running processes asynchronously.
"""
import logging
from typing import List
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas import validation_schemas
from creativeflow.mlops_service.domain.enums import ModelVersionStatusEnum, ValidationStatusEnum
from creativeflow.mlops_service.infrastructure.database.orm_models import (
    AIModelValidationResultORM, AIModelVersionORM
)
from creativeflow.mlops_service.infrastructure.database.repositories import (
    validation_repository, version_repository
)
from creativeflow.mlops_service.infrastructure.security_scanners.scanner_adapter import ScannerAdapter
from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.utils.exceptions import ModelVersionNotFoundException


logger = logging.getLogger(__name__)

class ModelValidationService:
    """Orchestrates the model validation pipeline."""

    def __init__(self):
        """Initializes the service with its dependencies."""
        self.validation_repo = validation_repository
        self.version_repo = version_repository
        self.scanner_adapter = ScannerAdapter(get_settings())

    async def _run_validation_tasks(self, db: Session, version_id: UUID, result_id: UUID, scan_types: List[str]):
        """The actual validation logic that runs in the background."""
        logger.info(f"Starting background validation for version {version_id}, result {result_id}")
        validation_result = await self.validation_repo.get(db, id=result_id)
        if not validation_result:
            logger.error(f"ValidationResult {result_id} not found for background task.")
            return

        validation_result.status = ValidationStatusEnum.RUNNING
        await self.validation_repo.update(db, db_obj=validation_result, obj_in={"status": ValidationStatusEnum.RUNNING})
        
        passed = True
        summary_parts = []

        try:
            # Placeholder for actual scan logic
            if "security" in scan_types:
                # Assuming CUSTOM_PYTHON_CONTAINER implies a container to scan
                model_version = await self.version_repo.get(db, id=version_id)
                image_name = f"model-repo/{model_version.model.name}:{model_version.version_string}" # Example image name
                scan_result = await self.scanner_adapter.scan_container_image(image_name)
                if scan_result.get("status") != "PASSED":
                    passed = False
                summary_parts.append(f"Security Scan: {scan_result.get('summary')}")

            if "functional" in scan_types:
                summary_parts.append("Functional Scan: Passed (Placeholder)")
            
            if "performance" in scan_types:
                summary_parts.append("Performance Scan: Passed (Placeholder)")

            final_status = ValidationStatusEnum.PASSED if passed else ValidationStatusEnum.FAILED
            model_version_status = ModelVersionStatusEnum.VALIDATED if passed else ModelVersionStatusEnum.VALIDATION_FAILED
            
            # Update validation result
            update_data = {"status": final_status, "summary": "\n".join(summary_parts)}
            await self.validation_repo.update(db, db_obj=validation_result, obj_in=update_data)

            # Update model version status
            version_update_data = {"status": model_version_status}
            await self.version_repo.update(db, db_obj=model_version, obj_in=version_update_data)
            
            logger.info(f"Validation for version {version_id} completed with status: {final_status}")
            
        except Exception as e:
            logger.error(f"Error during background validation for version {version_id}: {e}", exc_info=True)
            await self.validation_repo.update(db, db_obj=validation_result, obj_in={"status": ValidationStatusEnum.FAILED, "summary": f"An unexpected error occurred: {e}"})
            model_version = await self.version_repo.get(db, id=version_id)
            await self.version_repo.update(db, db_obj=model_version, obj_in={"status": ModelVersionStatusEnum.VALIDATION_FAILED})


    async def initiate_validation(
        self,
        db: Session,
        background_tasks: BackgroundTasks,
        version_id: UUID,
        validation_config: validation_schemas.ValidationRequestSchema,
        user_id: Optional[UUID],
    ) -> AIModelValidationResultORM:
        """
        Initiates an asynchronous validation process for a model version.

        Args:
            db: The database session.
            background_tasks: FastAPI's background task runner.
            version_id: The UUID of the model version to validate.
            validation_config: The configuration specifying which scans to run.
            user_id: The ID of the user initiating the validation.

        Returns:
            The created AIModelValidationResultORM object with a PENDING status.
        """
        model_version = await self.version_repo.get(db, id=version_id)
        if not model_version:
            raise ModelVersionNotFoundException(str(version_id))
        
        # Update model version status to PENDING_VALIDATION
        await self.version_repo.update(db, db_obj=model_version, obj_in={"status": ModelVersionStatusEnum.PENDING_VALIDATION})
        
        # Create a pending validation result record
        validation_result = AIModelValidationResultORM(
            model_version_id=version_id,
            scan_type=", ".join(validation_config.scan_types),
            status=ValidationStatusEnum.PENDING,
            summary="Validation process has been queued.",
            validated_by_user_id=user_id
        )
        db.add(validation_result)
        db.commit()
        db.refresh(validation_result)
        
        # Add the long-running validation process to the background
        background_tasks.add_task(
            self._run_validation_tasks,
            db,
            version_id,
            validation_result.id,
            validation_config.scan_types
        )
        
        return validation_result

    async def get_validation_result_by_id(
        self, db: Session, result_id: UUID
    ) -> Optional[AIModelValidationResultORM]:
        """
        Retrieves a specific validation result by its ID.

        Args:
            db: The database session.
            result_id: The UUID of the validation result.

        Returns:
            The AIModelValidationResultORM object or None if not found.
        """
        return await self.validation_repo.get(db, id=result_id)

    async def get_results_for_version(
        self, db: Session, version_id: UUID
    ) -> List[AIModelValidationResultORM]:
        """
        Retrieves all validation results for a specific model version.

        Args:
            db: The database session.
            version_id: The UUID of the model version.

        Returns:
            A list of AIModelValidationResultORM objects.
        """
        return await self.validation_repo.list_by_model_version_id(db, model_version_id=version_id)