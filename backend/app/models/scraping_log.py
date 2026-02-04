from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class ScrapingLog(Base):
    """Scraping activity log model."""

    __tablename__ = "scraping_logs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Scraping information
    source = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False)  # started, completed, failed

    # Results
    jobs_found = Column(Integer, default=0)
    jobs_new = Column(Integer, default=0)
    jobs_updated = Column(Integer, default=0)

    # Error handling
    error_message = Column(Text)

    # Timing
    started_at = Column(DateTime, nullable=False, default=func.now())
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)

    # Additional data
    extra_data = Column(Text)  # JSON for additional info

    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, source='{self.source}', status='{self.status}')>"
