from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Startup(Base):
    """Startup/company model for dealflow tracking."""

    __tablename__ = "startups"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Company basics
    name = Column(String(255), nullable=False, index=True)
    website = Column(String(500))
    description = Column(Text)

    # Funding information
    funding_stage = Column(String(50), index=True)  # seed, series-a, series-b, etc.
    last_funding_date = Column(DateTime)
    funding_amount = Column(String(100))  # e.g., "$5M", "Undisclosed"
    valuation = Column(String(100))

    # Traction metrics (optional - from user notes or research)
    traction_metrics = Column(Text)  # JSON: {revenue, users, growth_rate}

    # Founder information
    founders = Column(Text)  # JSON array: [{name, linkedin, background}]

    # Market/sector
    industry = Column(String(100), index=True)  # fintech, AI, biotech, etc.
    tags = Column(Text)  # comma-separated or JSON

    # Source information
    source = Column(String(50), nullable=False, index=True)  # exa, manual, etc.
    source_url = Column(String(500))
    source_id = Column(String(255))

    # Metadata
    discovered_date = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    dealflow_apps = relationship("DealflowApplication", back_populates="startup", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Startup(id={self.id}, name='{self.name}', stage='{self.funding_stage}')>"
