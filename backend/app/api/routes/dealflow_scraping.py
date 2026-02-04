from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from app.database import get_db
from app.services.dealflow_scraping import DealflowScrapingService
from app.models.scraping_log import ScrapingLog

router = APIRouter()
dealflow_scraping_service = DealflowScrapingService()


class DealflowScrapeRequest(BaseModel):
    """Request model for dealflow scraping."""
    query: str = Field(..., max_length=500)
    num_results: int = Field(default=50, ge=1, le=100)
    start_published_date: Optional[str] = None


class AcceleratorBatchRequest(BaseModel):
    """Request model for accelerator batch scraping."""
    accelerator: str = Field(..., max_length=100)
    batch_name: str = Field(..., max_length=50)
    num_results: int = Field(default=30, ge=1, le=100)


class SectorSearchRequest(BaseModel):
    """Request model for sector search."""
    sectors: List[str] = Field(..., max_items=10)
    num_per_sector: int = Field(default=30, ge=1, le=100)


class DealflowScrapeResponse(BaseModel):
    """Response model for dealflow scraping results."""
    status: str
    startups_found: int
    startups_new: int
    startups_updated: int
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


@router.post("/start", response_model=DealflowScrapeResponse)
async def start_dealflow_scraping(
    request: DealflowScrapeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a dealflow scraping job using Exa API.

    This will:
    1. Search for startups via Exa API
    2. Save new startups to database
    3. Return statistics

    Requires EXA_API_KEY to be set in environment.
    """
    try:
        result = await dealflow_scraping_service.run_dealflow_scrape(
            db=db,
            query=request.query,
            num_results=request.num_results,
            start_published_date=request.start_published_date
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.post("/accelerator", response_model=DealflowScrapeResponse)
async def search_accelerator_batch(
    request: AcceleratorBatchRequest,
    db: AsyncSession = Depends(get_db)
):
    """Search for startups from a specific accelerator batch."""
    try:
        result = await dealflow_scraping_service.search_accelerators(
            db=db,
            accelerators=[{
                "name": request.accelerator,
                "batch": request.batch_name
            }],
            num_per_batch=request.num_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.post("/sectors", response_model=DealflowScrapeResponse)
async def search_sectors(
    request: SectorSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """Search for startups in specific sectors/industries."""
    try:
        result = await dealflow_scraping_service.search_sectors(
            db=db,
            sectors=request.sectors,
            num_per_sector=request.num_per_sector
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.get("/logs", response_model=List[ScrapingLogResponse])
async def get_scraping_logs(
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get recent dealflow scraping logs."""
    logs = await dealflow_scraping_service.get_scraping_logs(db, limit=limit)
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
    """Get dealflow scraping service status."""
    try:
        from app.services.exa_dealflow_service import ExaDealflowService
        from app.config import settings

        if not settings.exa_api_key:
            return {
                "status": "not_configured",
                "message": "Exa API key is not set. Add EXA_API_KEY to your .env file"
            }

        return {
            "status": "ready",
            "message": "Dealflow scraping service is ready to use"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
