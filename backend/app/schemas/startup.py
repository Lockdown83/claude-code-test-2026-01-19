from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StartupBase(BaseModel):
    """Base schema for Startup."""
    name: str = Field(..., max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    funding_stage: Optional[str] = Field(None, max_length=50)
    last_funding_date: Optional[datetime] = None
    funding_amount: Optional[str] = Field(None, max_length=100)
    valuation: Optional[str] = Field(None, max_length=100)
    traction_metrics: Optional[str] = None  # JSON string
    founders: Optional[str] = None  # JSON string
    industry: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None
    source: str = Field(..., max_length=50)
    source_url: Optional[str] = Field(None, max_length=500)
    source_id: Optional[str] = Field(None, max_length=255)


class StartupCreate(StartupBase):
    """Schema for creating a startup."""
    pass


class StartupUpdate(BaseModel):
    """Schema for updating a startup."""
    name: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    funding_stage: Optional[str] = Field(None, max_length=50)
    last_funding_date: Optional[datetime] = None
    funding_amount: Optional[str] = Field(None, max_length=100)
    valuation: Optional[str] = Field(None, max_length=100)
    traction_metrics: Optional[str] = None
    founders: Optional[str] = None
    industry: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None
    is_active: Optional[bool] = None


class StartupInDB(StartupBase):
    """Schema for startup in database."""
    id: int
    discovered_date: datetime
    last_updated: datetime
    is_active: bool

    class Config:
        from_attributes = True


class StartupResponse(StartupInDB):
    """Schema for startup API response."""
    pass


class StartupListResponse(BaseModel):
    """Schema for paginated startup list response."""
    total: int
    page: int
    page_size: int
    startups: list[StartupResponse]
