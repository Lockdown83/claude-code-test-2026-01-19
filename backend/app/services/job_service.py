from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class JobService:
    """Service for Job CRUD operations."""

    async def create_job(self, db: AsyncSession, job_data: JobCreate) -> Job:
        """Create a new job."""
        db_job = Job(**job_data.model_dump())
        db.add(db_job)
        await db.commit()
        await db.refresh(db_job)
        return db_job

    async def get_job(self, db: AsyncSession, job_id: int) -> Optional[Job]:
        """Get a job by ID."""
        result = await db.execute(
            select(Job).where(Job.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_jobs(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        source: Optional[str] = None,
        company: Optional[str] = None,
        is_active: bool = True,
        search: Optional[str] = None
    ) -> tuple[List[Job], int]:
        """Get jobs with filtering and pagination."""
        # Build query
        query = select(Job)

        # Apply filters
        filters = []
        if is_active is not None:
            filters.append(Job.is_active == is_active)
        if source:
            filters.append(Job.source == source)
        if company:
            filters.append(Job.company.ilike(f"%{company}%"))
        if search:
            search_filter = or_(
                Job.title.ilike(f"%{search}%"),
                Job.company.ilike(f"%{search}%"),
                Job.description.ilike(f"%{search}%")
            )
            filters.append(search_filter)

        if filters:
            query = query.where(*filters)

        # Get total count
        count_query = select(func.count()).select_from(Job)
        if filters:
            count_query = count_query.where(*filters)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and ordering
        query = query.order_by(Job.posted_date.desc(), Job.scraped_at.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        jobs = result.scalars().all()

        return list(jobs), total

    async def update_job(
        self,
        db: AsyncSession,
        job_id: int,
        job_data: JobUpdate
    ) -> Optional[Job]:
        """Update a job."""
        job = await self.get_job(db, job_id)
        if not job:
            return None

        update_data = job_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)

        await db.commit()
        await db.refresh(job)
        return job

    async def delete_job(self, db: AsyncSession, job_id: int) -> bool:
        """Delete a job."""
        job = await self.get_job(db, job_id)
        if not job:
            return False

        await db.delete(job)
        await db.commit()
        return True
