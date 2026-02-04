from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    """Job posting model."""

    __tablename__ = "jobs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Core job information
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255))
    job_type = Column(String(50))  # full-time, part-time, contract, etc.
    seniority_level = Column(String(50))  # entry, mid, senior, etc.

    # Job details
    description = Column(Text)
    salary_range = Column(String(100))

    # Source information
    source = Column(String(50), nullable=False, index=True)  # exa, linkedin, etc.
    source_url = Column(String(500), unique=True, nullable=False)
    source_job_id = Column(String(255))

    # Metadata
    posted_date = Column(DateTime, index=True)
    scraped_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True, index=True)

    # Tags
    tags = Column(Text)  # JSON array or comma-separated

    # Relationships
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"
