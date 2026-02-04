from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from app.database import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()


@router.get("/stats", response_model=Dict)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Get unified dashboard statistics combining jobs and dealflow.

    Returns comprehensive metrics including:
    - Job application stats (total, by status, conversion rates)
    - Dealflow pipeline stats (stages, conversion rates, network growth)
    - Gamification metrics (weekly goals, streaks, activity)
    - Combined activity metrics
    """
    stats = await dashboard_service.get_dashboard_stats(db)
    return stats
