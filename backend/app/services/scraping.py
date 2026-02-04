from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Optional
from datetime import datetime
import logging
from app.services.exa_service import ExaService
from app.services.job_service import JobService
from app.models.scraping_log import ScrapingLog
from app.models.job import Job
from app.schemas.job import JobCreate

logger = logging.getLogger(__name__)


class ScrapingService:
    """Service for orchestrating job scraping via Exa API."""

    def __init__(self):
        """Initialize scraping service with dependencies."""
        self.exa_service = None  # Lazy init to avoid API key issues
        self.job_service = JobService()

    def _get_exa_service(self) -> ExaService:
        """Lazy initialize Exa service."""
        if not self.exa_service:
            self.exa_service = ExaService()
        return self.exa_service

    async def run_scraping_job(
        self,
        db: AsyncSession,
        query: str = "venture capital jobs hiring",
        num_results: int = 50,
        **search_params
    ) -> Dict:
        """
        Run a complete scraping job:
        1. Search via Exa API
        2. Save to database (skip if source_url already exists)
        3. Log results

        Args:
            db: Database session
            query: Search query
            num_results: Number of results to fetch
            **search_params: Additional Exa search parameters

        Returns:
            Dictionary with scraping results
        """
        started_at = datetime.utcnow()
        scraping_log = ScrapingLog(
            source="exa",
            status="started",
            started_at=started_at
        )

        try:
            logger.info(f"Starting scraping job: '{query}'")

            # Step 1: Search via Exa
            exa = self._get_exa_service()
            raw_jobs = await exa.search_vc_jobs(
                query=query,
                num_results=num_results,
                **search_params
            )

            scraping_log.jobs_found = len(raw_jobs)
            logger.info(f"Found {len(raw_jobs)} jobs from Exa")

            # Step 2: Save to database
            jobs_new = 0
            jobs_skipped = 0

            for job_data in raw_jobs:
                try:
                    # Check if job with same source_url already exists
                    result = await db.execute(
                        select(Job).where(Job.source_url == job_data.get('source_url'))
                    )
                    existing = result.scalar_one_or_none()

                    if existing:
                        jobs_skipped += 1
                        logger.debug(f"Skipped duplicate: {job_data.get('source_url')}")
                    else:
                        # Create new job
                        job_create = JobCreate(**job_data)
                        await self.job_service.create_job(db, job_create)
                        jobs_new += 1
                        logger.debug(f"Created new job: {job_data['title']}")

                except Exception as e:
                    logger.error(f"Error saving job: {str(e)}")
                    jobs_skipped += 1
                    continue

            # Commit all changes
            await db.commit()

            # Step 3: Update scraping log
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()

            scraping_log.status = "completed"
            scraping_log.jobs_new = jobs_new
            scraping_log.jobs_updated = 0
            scraping_log.completed_at = completed_at
            scraping_log.duration_seconds = duration

            db.add(scraping_log)
            await db.commit()

            logger.info(
                f"Scraping completed: {jobs_new} new, {jobs_skipped} skipped"
            )

            return {
                "status": "completed",
                "jobs_found": len(raw_jobs),
                "jobs_new": jobs_new,
                "jobs_updated": 0,
                "duplicates_removed": jobs_skipped,
                "duration_seconds": duration
            }

        except Exception as e:
            logger.error(f"Scraping job failed: {str(e)}")

            # Update scraping log with error
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()

            scraping_log.status = "failed"
            scraping_log.error_message = str(e)
            scraping_log.completed_at = completed_at
            scraping_log.duration_seconds = duration

            db.add(scraping_log)
            await db.commit()

            raise

    async def search_vc_firms(
        self,
        db: AsyncSession,
        firms: List[str],
        num_per_firm: int = 10
    ) -> Dict:
        """Search for jobs at specific VC firms."""
        query = " OR ".join([f"jobs at {firm}" for firm in firms])
        return await self.run_scraping_job(
            db,
            query=query,
            num_results=num_per_firm * len(firms)
        )

    async def search_by_role(
        self,
        db: AsyncSession,
        role: str,
        num_results: int = 50
    ) -> Dict:
        """Search for specific role in VC."""
        query = f"{role} venture capital jobs hiring"
        return await self.run_scraping_job(
            db,
            query=query,
            num_results=num_results
        )

    async def get_scraping_logs(
        self,
        db: AsyncSession,
        limit: int = 20
    ) -> List[ScrapingLog]:
        """Get recent scraping logs."""
        from sqlalchemy import select
        result = await db.execute(
            select(ScrapingLog)
            .order_by(ScrapingLog.started_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
