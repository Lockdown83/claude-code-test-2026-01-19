from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.services.startup_service import StartupService
from app.schemas.startup import (
    StartupCreate,
    StartupUpdate,
    StartupResponse,
    StartupListResponse
)

router = APIRouter()
startup_service = StartupService()


@router.post("/", response_model=StartupResponse, status_code=201)
async def create_startup(
    startup: StartupCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new startup."""
    created_startup = await startup_service.create_startup(db, startup)
    return created_startup


@router.get("/", response_model=StartupListResponse)
async def list_startups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    funding_stage: Optional[str] = None,
    industry: Optional[str] = None,
    source: Optional[str] = None,
    is_active: bool = True,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List startups with optional filtering."""
    startups, total = await startup_service.get_startups(
        db=db,
        skip=skip,
        limit=limit,
        funding_stage=funding_stage,
        industry=industry,
        source=source,
        is_active=is_active,
        search=search
    )

    page = (skip // limit) + 1 if limit > 0 else 1

    return StartupListResponse(
        total=total,
        page=page,
        page_size=limit,
        startups=startups
    )


@router.get("/{startup_id}", response_model=StartupResponse)
async def get_startup(
    startup_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific startup by ID."""
    startup = await startup_service.get_startup(db, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup


@router.put("/{startup_id}", response_model=StartupResponse)
async def update_startup(
    startup_id: int,
    startup_update: StartupUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a startup."""
    updated_startup = await startup_service.update_startup(db, startup_id, startup_update)
    if not updated_startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return updated_startup


@router.delete("/{startup_id}", status_code=204)
async def delete_startup(
    startup_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a startup."""
    success = await startup_service.delete_startup(db, startup_id)
    if not success:
        raise HTTPException(status_code=404, detail="Startup not found")
    return None
