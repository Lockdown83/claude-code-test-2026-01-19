from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JobBase(BaseModel):
    """Base schema for Job with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    job_type: Optional[str] = Field(None, max_length=50)
    seniority_level: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = Field(None, max_length=100)
    source: str = Field(..., max_length=50)
    source_url: str = Field(..., max_length=500)
    source_job_id: Optional[str] = Field(None, max_length=255)
    posted_date: Optional[datetime] = None
    tags: Optional[str] = None
    is_vc_related: bool = False


class JobCreate(JobBase):
    """Schema for creating a new job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    job_type: Optional[str] = Field(None, max_length=50)
    seniority_level: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = Field(None, max_length=100)
    source: Optional[str] = Field(None, max_length=50)
    source_url: Optional[str] = Field(None, max_length=500)
    source_job_id: Optional[str] = Field(None, max_length=255)
    posted_date: Optional[datetime] = None
    tags: Optional[str] = None
    is_vc_related: Optional[bool] = None
    is_active: Optional[bool] = None


class JobInDB(JobBase):
    """Schema for Job as stored in database."""
    id: int
    normalized_title: Optional[str] = None
    normalized_company: Optional[str] = None
    content_hash: Optional[str] = None
    scraped_at: datetime
    last_seen_at: datetime
    is_active: bool = True
    master_job_id: Optional[int] = None

    class Config:
        from_attributes = True


class JobResponse(JobInDB):
    """Schema for Job in API responses."""
    pass


class JobListResponse(BaseModel):
    """Schema for paginated job list response."""
    total: int
    page: int
    page_size: int
    jobs: list[JobResponse]
