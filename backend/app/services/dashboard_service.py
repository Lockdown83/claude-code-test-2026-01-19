from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from app.services.application_service import ApplicationService
from app.services.dealflow_application_service import DealflowApplicationService
from app.models.user_settings import UserSettings
from sqlalchemy import select


class DashboardService:
    """Service for unified dashboard statistics."""

    def __init__(self):
        self.application_service = ApplicationService()
        self.dealflow_service = DealflowApplicationService()

    async def get_dashboard_stats(self, db: AsyncSession) -> dict:
        """Get combined dashboard statistics for jobs and dealflow."""
        # Get job application stats
        job_stats = await self.application_service.get_application_stats(db)

        # Get dealflow stats
        dealflow_stats = await self.dealflow_service.get_dealflow_stats(db)

        # Get user settings (goals and streaks)
        user_settings = await self._get_or_create_user_settings(db)

        # Calculate job streak
        job_streak = await self._calculate_job_streak(db, user_settings)

        # Calculate dealflow streak
        dealflow_streak = await self._calculate_dealflow_streak(db, user_settings)

        # Calculate weekly goals progress
        job_weekly_progress = job_stats.get("recent_applications", 0) / user_settings.weekly_job_application_goal \
            if user_settings.weekly_job_application_goal > 0 else 0

        dealflow_weekly_progress = dealflow_stats.get("activity_last_7_days", {}).get("new_startups", 0) / \
            user_settings.weekly_dealflow_sourcing_goal if user_settings.weekly_dealflow_sourcing_goal > 0 else 0

        # Build combined response
        return {
            "jobs": {
                "total_active": job_stats.get("total", 0),
                "applications": {
                    "total": job_stats.get("total", 0),
                    "by_status": job_stats.get("by_status", {}),
                    "response_rate": job_stats.get("response_rate", 0),
                    "interview_rate": job_stats.get("interview_rate", 0),
                    "offer_rate": job_stats.get("offer_rate", 0)
                },
                "activity_last_7_days": job_stats.get("recent_applications", 0),
                "weekly_goal": {
                    "target": user_settings.weekly_job_application_goal,
                    "current": job_stats.get("recent_applications", 0),
                    "progress": round(min(job_weekly_progress, 1.0), 3)
                },
                "current_streak": job_streak
            },
            "dealflow": {
                "total_startups": dealflow_stats.get("total_startups_sourced", 0),
                "pipeline": dealflow_stats.get("pipeline_breakdown", {}),
                "conversion_rates": dealflow_stats.get("conversion_rates", {}),
                "network_growth": dealflow_stats.get("network_growth", {}),
                "activity_last_7_days": dealflow_stats.get("activity_last_7_days", {}),
                "weekly_goal": {
                    "target": user_settings.weekly_dealflow_sourcing_goal,
                    "current": dealflow_stats.get("activity_last_7_days", {}).get("new_startups", 0),
                    "progress": round(min(dealflow_weekly_progress, 1.0), 3)
                },
                "current_streak": dealflow_streak
            },
            "combined": {
                "total_activity_last_7_days": job_stats.get("recent_applications", 0) + \
                    dealflow_stats.get("activity_last_7_days", {}).get("new_startups", 0),
                "overall_streak": max(job_streak, dealflow_streak)
            }
        }

    async def _get_or_create_user_settings(self, db: AsyncSession) -> UserSettings:
        """Get or create user settings."""
        result = await db.execute(select(UserSettings))
        settings = result.scalar_one_or_none()

        if not settings:
            settings = UserSettings()
            db.add(settings)
            await db.commit()
            await db.refresh(settings)

        return settings

    async def _calculate_job_streak(self, db: AsyncSession, user_settings: UserSettings) -> int:
        """Calculate current job application streak."""
        # For MVP, just return the stored streak
        # In production, you'd check if last_updated is today and calculate
        return user_settings.job_application_streak

    async def _calculate_dealflow_streak(self, db: AsyncSession, user_settings: UserSettings) -> int:
        """Calculate current dealflow sourcing streak."""
        # For MVP, just return the stored streak
        return user_settings.dealflow_sourcing_streak

    async def update_streak(
        self,
        db: AsyncSession,
        activity_type: str
    ) -> UserSettings:
        """
        Update streak counter when activity occurs.

        Args:
            db: Database session
            activity_type: "job" or "dealflow"
        """
        user_settings = await self._get_or_create_user_settings(db)
        today = date.today()

        if activity_type == "job":
            last_updated = user_settings.job_application_streak_updated

            if last_updated is None:
                # First time
                user_settings.job_application_streak = 1
                user_settings.job_application_streak_updated = today
            elif last_updated == today:
                # Already counted today
                pass
            elif last_updated == today - timedelta(days=1):
                # Consecutive day
                user_settings.job_application_streak += 1
                user_settings.job_application_streak_updated = today
            else:
                # Streak broken
                user_settings.job_application_streak = 1
                user_settings.job_application_streak_updated = today

        elif activity_type == "dealflow":
            last_updated = user_settings.dealflow_sourcing_streak_updated

            if last_updated is None:
                user_settings.dealflow_sourcing_streak = 1
                user_settings.dealflow_sourcing_streak_updated = today
            elif last_updated == today:
                pass
            elif last_updated == today - timedelta(days=1):
                user_settings.dealflow_sourcing_streak += 1
                user_settings.dealflow_sourcing_streak_updated = today
            else:
                user_settings.dealflow_sourcing_streak = 1
                user_settings.dealflow_sourcing_streak_updated = today

        await db.commit()
        await db.refresh(user_settings)
        return user_settings
