from sqlalchemy import Column, Integer, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UserSettings(Base):
    """User settings for goals and streak tracking."""

    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)

    # Goals
    weekly_job_application_goal = Column(Integer, default=10)
    weekly_dealflow_sourcing_goal = Column(Integer, default=5)

    # Streaks
    job_application_streak = Column(Integer, default=0)
    job_application_streak_updated = Column(Date)

    dealflow_sourcing_streak = Column(Integer, default=0)
    dealflow_sourcing_streak_updated = Column(Date)

    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<UserSettings(id={self.id}, job_goal={self.weekly_job_application_goal}, dealflow_goal={self.weekly_dealflow_sourcing_goal})>"
