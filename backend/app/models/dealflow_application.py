from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DealflowApplication(Base):
    """Dealflow pipeline tracking model."""

    __tablename__ = "dealflow_applications"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    startup_id = Column(Integer, ForeignKey("startups.id", ondelete="CASCADE"),
                       nullable=False, index=True)

    # Pipeline status (7 stages)
    status = Column(String(50), nullable=False, index=True, default="sourced")
    # Enum: sourced, researching, contacted, meeting, shared, progressing, closed

    # Contact tracking
    first_contact_date = Column(Date)
    last_contact_date = Column(Date)
    emails_sent = Column(Integer, default=0)
    meetings_held = Column(Integer, default=0)

    # Notes and research
    notes = Column(Text)
    research_summary = Column(Text)

    # Outcome tracking (for "closed" status)
    outcome = Column(String(50))  # passed, invested, lost-to-competitor, etc.
    outcome_reason = Column(Text)

    # Relationship building
    intro_made_to = Column(String(255))  # Which firm/person introduced to
    intro_date = Column(Date)

    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    startup = relationship("Startup", back_populates="dealflow_apps")

    def __repr__(self):
        return f"<DealflowApplication(id={self.id}, startup_id={self.startup_id}, status='{self.status}')>"
