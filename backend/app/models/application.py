from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Application(Base):
    """Application tracking model."""

    __tablename__ = "applications"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to Job
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)

    # Application status
    status = Column(
        String(50),
        nullable=False,
        index=True,
        default="saved"
    )  # saved, applied, interviewing, rejected, offer, accepted
    applied_date = Column(Date, index=True)

    # Application details
    notes = Column(Text)
    resume_version = Column(String(255))
    cover_letter_path = Column(String(500))

    # Follow-up tracking
    last_contact_date = Column(Date)
    next_follow_up_date = Column(Date)

    # Interview tracking
    interview_count = Column(Integer, default=0)
    interview_notes = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="applications")

    def __repr__(self):
        return f"<Application(id={self.id}, job_id={self.job_id}, status='{self.status}')>"
