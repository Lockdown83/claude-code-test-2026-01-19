from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict
from app.database import get_db
from app.services.dealflow_application_service import DealflowApplicationService
from app.schemas.dealflow_application import (
    DealflowApplicationCreate,
    DealflowApplicationUpdate,
    DealflowApplicationResponse,
    DealflowApplicationListResponse,
    DealflowStatus
)
from pydantic import BaseModel

router = APIRouter()
dealflow_service = DealflowApplicationService()


class ContactLogRequest(BaseModel):
    """Request model for logging contact."""
    contact_type: str  # "email" or "meeting"


@router.post("/", response_model=DealflowApplicationResponse, status_code=201)
async def create_dealflow_application(
    application: DealflowApplicationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new dealflow application."""
    # Check if application already exists for this startup
    existing = await dealflow_service.get_application_by_startup(db, application.startup_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Dealflow application already exists for this startup (ID: {existing.id})"
        )

    created_application = await dealflow_service.create_application(db, application)
    return created_application


@router.get("/", response_model=DealflowApplicationListResponse)
async def list_dealflow_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[DealflowStatus] = None,
    startup_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List dealflow applications with optional filtering."""
    applications, total = await dealflow_service.get_applications(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        startup_id=startup_id
    )

    page = (skip // limit) + 1 if limit > 0 else 1

    return DealflowApplicationListResponse(
        total=total,
        page=page,
        page_size=limit,
        dealflow_applications=applications
    )


@router.get("/stats", response_model=Dict)
async def get_dealflow_stats(
    db: AsyncSession = Depends(get_db)
):
    """Get dealflow pipeline statistics."""
    stats = await dealflow_service.get_dealflow_stats(db)
    return stats


@router.get("/{application_id}", response_model=DealflowApplicationResponse)
async def get_dealflow_application(
    application_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific dealflow application by ID."""
    application = await dealflow_service.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Dealflow application not found")
    return application


@router.put("/{application_id}", response_model=DealflowApplicationResponse)
async def update_dealflow_application(
    application_id: int,
    application_update: DealflowApplicationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a dealflow application."""
    updated_application = await dealflow_service.update_application(
        db, application_id, application_update
    )
    if not updated_application:
        raise HTTPException(status_code=404, detail="Dealflow application not found")
    return updated_application


@router.post("/{application_id}/contact", response_model=DealflowApplicationResponse)
async def log_contact(
    application_id: int,
    contact_log: ContactLogRequest,
    db: AsyncSession = Depends(get_db)
):
    """Log a contact (email or meeting) for a dealflow application."""
    if contact_log.contact_type not in ["email", "meeting"]:
        raise HTTPException(
            status_code=400,
            detail="Contact type must be 'email' or 'meeting'"
        )

    updated_application = await dealflow_service.log_contact(
        db, application_id, contact_log.contact_type
    )
    if not updated_application:
        raise HTTPException(status_code=404, detail="Dealflow application not found")
    return updated_application


@router.delete("/{application_id}", status_code=204)
async def delete_dealflow_application(
    application_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a dealflow application."""
    success = await dealflow_service.delete_application(db, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dealflow application not found")
    return None
