from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List
from app.database import get_db
from app.services.scraping import ScrapingService
from app.models.scraping_log import ScrapingLog

router = APIRouter()
scraping_service = ScrapingService()


class ScrapeRequest(BaseModel):
    """Request model for scraping."""
    query: str = Field(default="venture capital jobs hiring", max_length=500)
    num_results: int = Field(default=50, ge=1, le=100)
    start_published_date: Optional[str] = None
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None


class ScrapeResponse(BaseModel):
    """Response model for scraping results."""
    status: str
    jobs_found: int
    jobs_new: int
    jobs_updated: int
    duplicates_removed: int
    duration_seconds: float


class ScrapingLogResponse(BaseModel):
    """Response model for scraping log."""
    id: int
    source: str
    status: str
    jobs_found: int
    jobs_new: int
    jobs_updated: int
    error_message: Optional[str]
    started_at: str
    completed_at: Optional[str]
    duration_seconds: Optional[float]

    class Config:
        from_attributes = True


@router.post("/start", response_model=ScrapeResponse)
async def start_scraping(
    request: ScrapeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a scraping job using Exa API.

    This will:
    1. Search for jobs via Exa API
    2. Deduplicate results
    3. Save new jobs to database
    4. Return statistics

    Requires EXA_API_KEY to be set in environment.
    """
    try:
        result = await scraping_service.run_scraping_job(
            db=db,
            query=request.query,
            num_results=request.num_results,
            start_published_date=request.start_published_date,
            include_domains=request.include_domains,
            exclude_domains=request.exclude_domains
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.post("/search-firms", response_model=ScrapeResponse)
async def search_vc_firms(
    firms: List[str] = ["Sequoia Capital", "Andreessen Horowitz", "Accel"],
    num_per_firm: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Search for jobs at specific VC firms."""
    try:
        result = await scraping_service.search_vc_firms(
            db=db,
            firms=firms,
            num_per_firm=num_per_firm
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.post("/search-role", response_model=ScrapeResponse)
async def search_by_role(
    role: str = "analyst",
    num_results: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Search for specific role in venture capital."""
    try:
        result = await scraping_service.search_by_role(
            db=db,
            role=role,
            num_results=num_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.get("/logs", response_model=List[ScrapingLogResponse])
async def get_scraping_logs(
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get recent scraping logs."""
    logs = await scraping_service.get_scraping_logs(db, limit=limit)
    return [
        ScrapingLogResponse(
            id=log.id,
            source=log.source,
            status=log.status,
            jobs_found=log.jobs_found,
            jobs_new=log.jobs_new,
            jobs_updated=log.jobs_updated,
            error_message=log.error_message,
            started_at=log.started_at.isoformat(),
            completed_at=log.completed_at.isoformat() if log.completed_at else None,
            duration_seconds=log.duration_seconds
        )
        for log in logs
    ]


@router.get("/status")
async def get_scraping_status():
    """Get scraping service status."""
    try:
        # Try to initialize Exa service to check if API key is set
        from app.services.exa_service import ExaService
        from app.config import settings

        if not settings.exa_api_key:
            return {
                "status": "not_configured",
                "message": "Exa API key is not set. Add EXA_API_KEY to your .env file"
            }

        return {
            "status": "ready",
            "message": "Scraping service is ready to use"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
