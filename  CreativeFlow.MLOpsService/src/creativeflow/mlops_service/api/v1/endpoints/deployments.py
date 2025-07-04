"""
FastAPI router for AI Model Deployment and A/B testing endpoints.

This module defines the API for creating, managing, and monitoring deployments
of AI model versions to the Kubernetes cluster.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1 import schemas
from creativeflow.mlops_service.core.security import verify_api_key
from creativeflow.mlops_service.database import get_db
from creativeflow.mlops_service.services.model_deployment_service import ModelDeploymentService
from creativeflow.mlops_service.utils.exceptions import DeploymentFailedException

router = APIRouter()
model_deployment_service = ModelDeploymentService()

@router.post(
    "/",
    response_model=schemas.DeploymentResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new deployment for an AI Model Version",
    dependencies=[Depends(verify_api_key)],
)
async def create_deployment(
    deployment_in: schemas.DeploymentCreateSchema,
    db: Session = Depends(get_db),
):
    """
    Initiate the deployment of a validated model version to the Kubernetes cluster.
    This is an asynchronous operation; the endpoint returns immediately while
    deployment proceeds in the background.
    """
    # In a real async scenario, this might publish to a queue. Here we call it directly.
    # Assuming user_id would be extracted from a JWT.
    user_id: Optional[UUID] = None
    return await model_deployment_service.deploy_model_version(
        db, deployment_config=deployment_in, user_id=user_id
    )


@router.get(
    "/{deployment_id}",
    response_model=schemas.DeploymentResponseSchema,
    summary="Get status and details of a deployment",
    dependencies=[Depends(verify_api_key)],
)
async def get_deployment_status(
    deployment_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve the current status and configuration of a specific deployment."""
    deployment = await model_deployment_service.get_deployment_by_id(db, deployment_id=deployment_id)
    if not deployment:
        raise DeploymentFailedException(f"Deployment {deployment_id} not found.")
    return deployment


@router.get(
    "/",
    response_model=List[schemas.DeploymentResponseSchema],
    summary="List all deployments",
    dependencies=[Depends(verify_api_key)],
)
async def list_deployments(
    model_version_id: Optional[UUID] = None,
    environment: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of all deployments, optionally filtering by model version or environment.
    """
    # This simplified version just gets all. A real service would implement filtering.
    return await model_deployment_service.list_deployments(db, skip=skip, limit=limit)


@router.put(
    "/{deployment_id}",
    response_model=schemas.DeploymentResponseSchema,
    summary="Update an existing deployment",
    dependencies=[Depends(verify_api_key)],
)
async def update_deployment(
    deployment_id: UUID,
    deployment_update: schemas.DeploymentUpdateSchema,
    db: Session = Depends(get_db),
):
    """
    Update an existing deployment, for example, to change the number of replicas
    or adjust A/B test traffic splits.
    """
    # Assuming user_id would be extracted from a JWT.
    user_id: Optional[UUID] = None
    return await model_deployment_service.update_deployment(
        db, deployment_id=deployment_id, deployment_update=deployment_update, user_id=user_id
    )


@router.delete(
    "/{deployment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete/undeploy a model",
    dependencies=[Depends(verify_api_key)],
)
async def delete_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a deployment, which removes the running model from the Kubernetes cluster
    and archives its record in the database.
    """
    # Assuming user_id would be extracted from a JWT.
    user_id: Optional[UUID] = None
    await model_deployment_service.delete_deployment(db, deployment_id=deployment_id, user_id=user_id)
    return