from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, date, timedelta
from app.models.dealflow_application import DealflowApplication
from app.models.startup import Startup
from app.schemas.dealflow_application import (
    DealflowApplicationCreate,
    DealflowApplicationUpdate,
    DealflowStatus
)


class DealflowApplicationService:
    """Service for DealflowApplication operations."""

    async def create_application(
        self,
        db: AsyncSession,
        application_data: DealflowApplicationCreate
    ) -> DealflowApplication:
        """Create a new dealflow application."""
        db_application = DealflowApplication(**application_data.model_dump())
        db.add(db_application)
        await db.commit()
        await db.refresh(db_application)
        return db_application

    async def get_application(
        self,
        db: AsyncSession,
        application_id: int
    ) -> Optional[DealflowApplication]:
        """Get a dealflow application by ID."""
        result = await db.execute(
            select(DealflowApplication)
            .options(selectinload(DealflowApplication.startup))
            .where(DealflowApplication.id == application_id)
        )
        return result.scalar_one_or_none()

    async def get_applications(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[DealflowStatus] = None,
        startup_id: Optional[int] = None
    ) -> tuple[List[DealflowApplication], int]:
        """Get dealflow applications with filtering and pagination."""
        # Build query
        query = select(DealflowApplication).options(selectinload(DealflowApplication.startup))

        # Apply filters
        filters = []
        if status:
            filters.append(DealflowApplication.status == status.value)
        if startup_id:
            filters.append(DealflowApplication.startup_id == startup_id)

        if filters:
            query = query.where(*filters)

        # Get total count
        count_query = select(func.count()).select_from(DealflowApplication)
        if filters:
            count_query = count_query.where(*filters)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and ordering
        query = query.order_by(DealflowApplication.updated_at.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        applications = result.scalars().all()

        return list(applications), total

    async def update_application(
        self,
        db: AsyncSession,
        application_id: int,
        application_data: DealflowApplicationUpdate
    ) -> Optional[DealflowApplication]:
        """Update a dealflow application."""
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
        """Delete a dealflow application."""
        application = await self.get_application(db, application_id)
        if not application:
            return False

        await db.delete(application)
        await db.commit()
        return True

    async def log_contact(
        self,
        db: AsyncSession,
        application_id: int,
        contact_type: str
    ) -> Optional[DealflowApplication]:
        """Log a contact (email or meeting) for a dealflow application."""
        application = await self.get_application(db, application_id)
        if not application:
            return None

        if contact_type == "email":
            application.emails_sent += 1
        elif contact_type == "meeting":
            application.meetings_held += 1

        # Update last contact date
        application.last_contact_date = date.today()

        # Set first contact date if not set
        if not application.first_contact_date:
            application.first_contact_date = date.today()

        application.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(application)
        return application

    async def get_dealflow_stats(self, db: AsyncSession) -> dict:
        """Get dealflow pipeline statistics with gamification metrics."""
        # Total startups sourced
        total_result = await db.execute(
            select(func.count()).select_from(DealflowApplication)
        )
        total_startups = total_result.scalar()

        # Pipeline breakdown by status
        status_query = select(
            DealflowApplication.status,
            func.count(DealflowApplication.id)
        ).group_by(DealflowApplication.status)
        status_result = await db.execute(status_query)
        pipeline_breakdown = {status: count for status, count in status_result.all()}

        # Calculate conversion rates
        sourced_count = sum(pipeline_breakdown.values())  # All stages
        contacted_count = pipeline_breakdown.get("contacted", 0) + \
                         pipeline_breakdown.get("meeting", 0) + \
                         pipeline_breakdown.get("shared", 0) + \
                         pipeline_breakdown.get("progressing", 0) + \
                         pipeline_breakdown.get("closed", 0)
        meeting_count = pipeline_breakdown.get("meeting", 0) + \
                       pipeline_breakdown.get("shared", 0) + \
                       pipeline_breakdown.get("progressing", 0) + \
                       pipeline_breakdown.get("closed", 0)
        shared_count = pipeline_breakdown.get("shared", 0) + \
                      pipeline_breakdown.get("progressing", 0) + \
                      pipeline_breakdown.get("closed", 0)

        conversion_rates = {
            "sourced_to_contacted": round(contacted_count / sourced_count, 3) if sourced_count > 0 else 0,
            "contacted_to_meeting": round(meeting_count / contacted_count, 3) if contacted_count > 0 else 0,
            "meeting_to_shared": round(shared_count / meeting_count, 3) if meeting_count > 0 else 0
        }

        # Outcomes for closed deals
        closed_query = select(
            DealflowApplication.outcome,
            func.count(DealflowApplication.id)
        ).where(
            DealflowApplication.status == "closed"
        ).group_by(DealflowApplication.outcome)
        closed_result = await db.execute(closed_query)
        outcomes = {outcome: count for outcome, count in closed_result.all() if outcome}

        # Activity in last 7 days
        seven_days_ago = date.today() - timedelta(days=7)

        # New startups in last 7 days
        new_startups_query = select(func.count()).select_from(DealflowApplication).where(
            DealflowApplication.created_at >= datetime.combine(seven_days_ago, datetime.min.time())
        )
        new_startups_result = await db.execute(new_startups_query)
        new_startups_7d = new_startups_result.scalar()

        # Emails sent in last 7 days (sum of all emails_sent for apps updated in last 7 days)
        emails_query = select(func.sum(DealflowApplication.emails_sent)).where(
            DealflowApplication.last_contact_date >= seven_days_ago
        )
        emails_result = await db.execute(emails_query)
        emails_7d = emails_result.scalar() or 0

        # Meetings held in last 7 days
        meetings_query = select(func.sum(DealflowApplication.meetings_held)).where(
            DealflowApplication.last_contact_date >= seven_days_ago
        )
        meetings_result = await db.execute(meetings_query)
        meetings_7d = meetings_result.scalar() or 0

        # Network metrics (total founders contacted, intros made)
        total_contacts_query = select(
            func.sum(DealflowApplication.emails_sent),
            func.sum(DealflowApplication.meetings_held)
        )
        contacts_result = await db.execute(total_contacts_query)
        total_emails, total_meetings = contacts_result.one()

        intros_query = select(func.count()).select_from(DealflowApplication).where(
            DealflowApplication.intro_made_to.isnot(None)
        )
        intros_result = await db.execute(intros_query)
        intros_made = intros_result.scalar()

        return {
            "total_startups_sourced": total_startups,
            "pipeline_breakdown": pipeline_breakdown,
            "conversion_rates": conversion_rates,
            "outcomes": outcomes,
            "activity_last_7_days": {
                "new_startups": new_startups_7d,
                "emails_sent": emails_7d,
                "meetings_held": meetings_7d
            },
            "network_growth": {
                "total_emails_sent": total_emails or 0,
                "total_meetings_held": total_meetings or 0,
                "intros_made": intros_made
            }
        }

    async def get_application_by_startup(
        self,
        db: AsyncSession,
        startup_id: int
    ) -> Optional[DealflowApplication]:
        """Get dealflow application for a specific startup (if exists)."""
        result = await db.execute(
            select(DealflowApplication).where(DealflowApplication.startup_id == startup_id)
        )
        return result.scalar_one_or_none()
