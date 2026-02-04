from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Dict
from datetime import datetime, timedelta
from app.database import get_db
from app.services.job_service import JobService
from app.models.job import Job
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse
)

router = APIRouter()
job_service = JobService()


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new job posting."""
    created_job = await job_service.create_job(db, job)
    return created_job


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    source: Optional[str] = None,
    company: Optional[str] = None,
    is_active: bool = True,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List jobs with optional filtering."""
    jobs, total = await job_service.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
        source=source,
        company=company,
        is_active=is_active,
        search=search
    )

    page = (skip // limit) + 1 if limit > 0 else 1

    return JobListResponse(
        total=total,
        page=page,
        page_size=limit,
        jobs=jobs
    )


@router.get("/stats", response_model=Dict)
async def get_job_stats(db: AsyncSession = Depends(get_db)):
    """Get job statistics."""
    # Total jobs
    total_result = await db.execute(select(func.count(Job.id)))
    total_jobs = total_result.scalar()

    # Active jobs
    active_result = await db.execute(
        select(func.count(Job.id)).where(Job.is_active == True)
    )
    active_jobs = active_result.scalar()

    # Jobs in last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_result = await db.execute(
        select(func.count(Job.id)).where(Job.scraped_at >= seven_days_ago)
    )
    jobs_last_7_days = recent_result.scalar()

    # Jobs by source
    source_result = await db.execute(
        select(Job.source, func.count(Job.id))
        .group_by(Job.source)
    )
    jobs_by_source = {source: count for source, count in source_result.all()}

    # Top companies (limit to top 10)
    company_result = await db.execute(
        select(Job.company, func.count(Job.id))
        .where(Job.is_active == True)
        .group_by(Job.company)
        .order_by(func.count(Job.id).desc())
        .limit(10)
    )
    jobs_by_company = {company: count for company, count in company_result.all()}

    return {
        "total_jobs_found": total_jobs,
        "active_jobs": active_jobs,
        "jobs_last_7_days": jobs_last_7_days,
        "jobs_by_source": jobs_by_source,
        "jobs_by_company": jobs_by_company
    }


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific job by ID."""
    job = await job_service.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a job posting."""
    updated_job = await job_service.update_job(db, job_id, job_update)
    if not updated_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated_job


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a job posting."""
    success = await job_service.delete_job(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return None
