from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, date, timedelta
from app.models.application import Application
from app.models.job import Job
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationStatus


class ApplicationService:
    """Service for Application CRUD operations."""

    async def create_application(
        self,
        db: AsyncSession,
        application_data: ApplicationCreate
    ) -> Application:
        """Create a new application."""
        db_application = Application(**application_data.model_dump())
        db.add(db_application)
        await db.commit()
        await db.refresh(db_application)
        return db_application

    async def get_application(
        self,
        db: AsyncSession,
        application_id: int
    ) -> Optional[Application]:
        """Get an application by ID."""
        result = await db.execute(
            select(Application)
            .options(selectinload(Application.job))
            .where(Application.id == application_id)
        )
        return result.scalar_one_or_none()

    async def get_applications(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ApplicationStatus] = None,
        job_id: Optional[int] = None
    ) -> tuple[List[Application], int]:
        """Get applications with filtering and pagination."""
        # Build query
        query = select(Application).options(selectinload(Application.job))

        # Apply filters
        filters = []
        if status:
            filters.append(Application.status == status.value)
        if job_id:
            filters.append(Application.job_id == job_id)

        if filters:
            query = query.where(*filters)

        # Get total count
        count_query = select(func.count()).select_from(Application)
        if filters:
            count_query = count_query.where(*filters)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and ordering
        query = query.order_by(Application.updated_at.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        applications = result.scalars().all()

        return list(applications), total

    async def update_application(
        self,
        db: AsyncSession,
        application_id: int,
        application_data: ApplicationUpdate
    ) -> Optional[Application]:
        """Update an application."""
        application = await self.get_application(db, application_id)
        if not application:
            return None

        # Update fields
        update_data = application_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(application, field, value)

        # Update timestamp
        application.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(application)
        return application

    async def delete_application(
        self,
        db: AsyncSession,
        application_id: int
    ) -> bool:
        """Delete an application."""
        application = await self.get_application(db, application_id)
        if not application:
            return False

        await db.delete(application)
        await db.commit()
        return True

    async def get_application_stats(self, db: AsyncSession) -> dict:
        """Get application statistics with gamification metrics."""
        # Total count
        total_result = await db.execute(select(func.count()).select_from(Application))
        total = total_result.scalar()

        # Count by status
        status_query = select(
            Application.status,
            func.count(Application.id)
        ).group_by(Application.status)
        status_result = await db.execute(status_query)
        by_status = {status: count for status, count in status_result.all()}

        # Recent applications (last 7 days)
        seven_days_ago = date.today() - timedelta(days=7)
        recent_query = select(func.count()).select_from(Application).where(
            Application.applied_date >= seven_days_ago
        )
        recent_result = await db.execute(recent_query)
        recent_applications = recent_result.scalar()

        # Upcoming follow-ups (next 7 days)
        seven_days_future = date.today() + timedelta(days=7)
        follow_up_query = select(func.count()).select_from(Application).where(
            Application.next_follow_up_date.between(date.today(), seven_days_future)
        )
        follow_up_result = await db.execute(follow_up_query)
        upcoming_follow_ups = follow_up_result.scalar()

        # Calculate conversion rates
        # Response rate: % that moved beyond "applied" status
        applied_count = by_status.get("applied", 0) + \
                       by_status.get("interviewing", 0) + \
                       by_status.get("rejected", 0) + \
                       by_status.get("offer", 0) + \
                       by_status.get("accepted", 0)

        responded_count = by_status.get("interviewing", 0) + \
                         by_status.get("rejected", 0) + \
                         by_status.get("offer", 0) + \
                         by_status.get("accepted", 0)

        response_rate = (responded_count / applied_count) if applied_count > 0 else 0

        # Interview rate: % that reached interviewing stage
        interview_count = by_status.get("interviewing", 0) + \
                         by_status.get("offer", 0) + \
                         by_status.get("accepted", 0)
        interview_rate = (interview_count / applied_count) if applied_count > 0 else 0

        # Offer rate: % that got offers
        offer_count = by_status.get("offer", 0) + by_status.get("accepted", 0)
        offer_rate = (offer_count / applied_count) if applied_count > 0 else 0

        return {
            "total": total,
            "by_status": by_status,
            "recent_applications": recent_applications,
            "upcoming_follow_ups": upcoming_follow_ups,
            "response_rate": round(response_rate, 3),
            "interview_rate": round(interview_rate, 3),
            "offer_rate": round(offer_rate, 3)
        }

    async def get_application_by_job(
        self,
        db: AsyncSession,
        job_id: int
    ) -> Optional[Application]:
        """Get application for a specific job (if exists)."""
        result = await db.execute(
            select(Application).where(Application.job_id == job_id)
        )
        return result.scalar_one_or_none()
