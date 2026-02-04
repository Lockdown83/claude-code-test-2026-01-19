from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class DealflowStatus(str, Enum):
    """Dealflow pipeline status enum."""
    SOURCED = "sourced"
    RESEARCHING = "researching"
    CONTACTED = "contacted"
    MEETING = "meeting"
    SHARED = "shared"
    PROGRESSING = "progressing"
    CLOSED = "closed"


class DealflowOutcome(str, Enum):
    """Dealflow outcome enum."""
    PASSED = "passed"
    INVESTED = "invested"
    LOST_TO_COMPETITOR = "lost-to-competitor"
    NO_RESPONSE = "no-response"
    NOT_A_FIT = "not-a-fit"


class DealflowApplicationBase(BaseModel):
    """Base schema for DealflowApplication."""
    startup_id: int
    status: DealflowStatus = DealflowStatus.SOURCED
    first_contact_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    emails_sent: int = 0
    meetings_held: int = 0
    notes: Optional[str] = None
    research_summary: Optional[str] = None
    outcome: Optional[str] = Field(None, max_length=50)
    outcome_reason: Optional[str] = None
    intro_made_to: Optional[str] = Field(None, max_length=255)
    intro_date: Optional[date] = None


class DealflowApplicationCreate(BaseModel):
    """Schema for creating a dealflow application."""
    startup_id: int
    status: DealflowStatus = DealflowStatus.SOURCED
    notes: Optional[str] = None


class DealflowApplicationUpdate(BaseModel):
    """Schema for updating a dealflow application."""
    status: Optional[DealflowStatus] = None
    first_contact_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    emails_sent: Optional[int] = None
    meetings_held: Optional[int] = None
    notes: Optional[str] = None
    research_summary: Optional[str] = None
    outcome: Optional[str] = None
    outcome_reason: Optional[str] = None
    intro_made_to: Optional[str] = None
    intro_date: Optional[date] = None


class DealflowApplicationInDB(DealflowApplicationBase):
    """Schema for dealflow application in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DealflowApplicationResponse(DealflowApplicationInDB):
    """Schema for dealflow application API response."""
    pass


class DealflowApplicationWithStartup(DealflowApplicationResponse):
    """Schema for dealflow application with startup details."""
    startup_name: str
    startup_industry: Optional[str]
    startup_funding_stage: Optional[str]


class DealflowApplicationListResponse(BaseModel):
    """Schema for paginated dealflow application list response."""
    total: int
    page: int
    page_size: int
    dealflow_applications: list[DealflowApplicationResponse]
