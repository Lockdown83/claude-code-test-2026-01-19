from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class ApplicationStatus(str, Enum):
    """Enum for application status values."""
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    REJECTED = "rejected"
    OFFER = "offer"
    ACCEPTED = "accepted"


class ApplicationBase(BaseModel):
    """Base schema for Application with common fields."""
    job_id: int
    status: ApplicationStatus = ApplicationStatus.SAVED
    applied_date: Optional[date] = None
    notes: Optional[str] = None
    resume_version: Optional[str] = Field(None, max_length=255)
    cover_letter_path: Optional[str] = Field(None, max_length=500)
    last_contact_date: Optional[date] = None
    next_follow_up_date: Optional[date] = None
    interview_count: int = 0
    interview_notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""
    pass


class ApplicationUpdate(BaseModel):
    """Schema for updating an application (all fields optional)."""
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    notes: Optional[str] = None
    resume_version: Optional[str] = Field(None, max_length=255)
    cover_letter_path: Optional[str] = Field(None, max_length=500)
    last_contact_date: Optional[date] = None
    next_follow_up_date: Optional[date] = None
    interview_count: Optional[int] = None
    interview_notes: Optional[str] = None


class ApplicationInDB(ApplicationBase):
    """Schema for Application as stored in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationResponse(ApplicationInDB):
    """Schema for Application in API responses."""
    pass


class ApplicationWithJob(ApplicationResponse):
    """Schema for Application with associated Job details."""
    job_title: Optional[str] = None
    job_company: Optional[str] = None
    job_location: Optional[str] = None


class ApplicationListResponse(BaseModel):
    """Schema for paginated application list response."""
    total: int
    page: int
    page_size: int
    applications: list[ApplicationResponse]


class ApplicationStats(BaseModel):
    """Schema for application statistics."""
    total: int
    by_status: dict[str, int]
    recent_applications: int
    upcoming_follow_ups: int
