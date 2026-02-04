from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.services.application_service import ApplicationService
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListResponse,
    ApplicationStats,
    ApplicationStatus
)

router = APIRouter()
application_service = ApplicationService()


@router.post("/", response_model=ApplicationResponse, status_code=201)
async def create_application(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new job application."""
    # Check if application already exists for this job
    existing = await application_service.get_application_by_job(db, application.job_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Application already exists for this job (ID: {existing.id})"
        )

    created_application = await application_service.create_application(db, application)
    return created_application


@router.get("/", response_model=ApplicationListResponse)
async def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[ApplicationStatus] = None,
    job_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List applications with optional filtering."""
    applications, total = await application_service.get_applications(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        job_id=job_id
    )

    page = (skip // limit) + 1 if limit > 0 else 1

    return ApplicationListResponse(
        total=total,
        page=page,
        page_size=limit,
        applications=applications
    )


@router.get("/stats", response_model=ApplicationStats)
async def get_application_stats(
    db: AsyncSession = Depends(get_db)
):
    """Get application statistics."""
    stats = await application_service.get_application_stats(db)
    return stats


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific application by ID."""
    application = await application_service.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an application."""
    updated_application = await application_service.update_application(
        db, application_id, application_update
    )
    if not updated_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_application


@router.delete("/{application_id}", status_code=204)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an application."""
    success = await application_service.delete_application(db, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return None
