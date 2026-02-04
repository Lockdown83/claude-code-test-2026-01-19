from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Optional
from datetime import datetime
import logging
from app.services.exa_dealflow_service import ExaDealflowService
from app.services.startup_service import StartupService
from app.models.scraping_log import ScrapingLog
from app.models.startup import Startup
from app.schemas.startup import StartupCreate

logger = logging.getLogger(__name__)


class DealflowScrapingService:
    """Service for orchestrating dealflow scraping via Exa API."""

    def __init__(self):
        """Initialize dealflow scraping service with dependencies."""
        self.exa_service = None  # Lazy init to avoid API key issues
        self.startup_service = StartupService()

    def _get_exa_service(self) -> ExaDealflowService:
        """Lazy initialize Exa dealflow service."""
        if not self.exa_service:
            self.exa_service = ExaDealflowService()
        return self.exa_service

    async def run_dealflow_scrape(
        self,
        db: AsyncSession,
        query: str,
        num_results: int = 50,
        **search_params
    ) -> Dict:
        """
        Run a complete dealflow scraping job:
        1. Search via Exa API
        2. Save to database (skip if duplicate by website)
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
            source="exa-dealflow",
            status="started",
            started_at=started_at
        )

        try:
            logger.info(f"Starting dealflow scraping: '{query}'")

            # Step 1: Search via Exa
            exa = self._get_exa_service()
            raw_startups = await exa.search_startups(
                query=query,
                num_results=num_results,
                **search_params
            )

            scraping_log.jobs_found = len(raw_startups)
            logger.info(f"Found {len(raw_startups)} startups from Exa")

            # Step 2: Save to database
            startups_new = 0
            startups_skipped = 0

            for startup_data in raw_startups:
                try:
                    # Check if startup with same website already exists
                    website = startup_data.get('website')
                    if website:
                        result = await db.execute(
                            select(Startup).where(Startup.website == website)
                        )
                        existing = result.scalar_one_or_none()

                        if existing:
                            startups_skipped += 1
                            logger.debug(f"Skipped duplicate: {website}")
                            continue

                    # Create new startup
                    startup_create = StartupCreate(**startup_data)
                    await self.startup_service.create_startup(db, startup_create)
                    startups_new += 1
                    logger.debug(f"Created new startup: {startup_data['name']}")

                except Exception as e:
                    logger.error(f"Error saving startup: {str(e)}")
                    startups_skipped += 1
                    continue

            # Commit all changes
            await db.commit()

            # Step 3: Update scraping log
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()

            scraping_log.status = "completed"
            scraping_log.jobs_new = startups_new
            scraping_log.jobs_updated = 0
            scraping_log.completed_at = completed_at
            scraping_log.duration_seconds = duration

            db.add(scraping_log)
            await db.commit()

            logger.info(
                f"Dealflow scraping completed: {startups_new} new, {startups_skipped} skipped"
            )

            return {
                "status": "completed",
                "startups_found": len(raw_startups),
                "startups_new": startups_new,
                "startups_updated": 0,
                "duplicates_removed": startups_skipped,
                "duration_seconds": duration
            }

        except Exception as e:
            logger.error(f"Dealflow scraping failed: {str(e)}")

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

    async def search_accelerators(
        self,
        db: AsyncSession,
        accelerators: List[Dict[str, str]],
        num_per_batch: int = 30
    ) -> Dict:
        """
        Search for startups from specific accelerator batches.

        Args:
            db: Database session
            accelerators: List of dicts with 'name' and 'batch' keys
            num_per_batch: Number of results per accelerator batch

        Returns:
            Dictionary with scraping results
        """
        all_startups = []
        total_new = 0
        total_skipped = 0

        for acc in accelerators:
            exa = self._get_exa_service()
            startups = await exa.search_accelerator_batch(
                accelerator=acc.get("name", ""),
                batch_name=acc.get("batch", ""),
                num_results=num_per_batch
            )
            all_startups.extend(startups)

        # Process all startups
        started_at = datetime.utcnow()

        for startup_data in all_startups:
            try:
                website = startup_data.get('website')
                if website:
                    result = await db.execute(
                        select(Startup).where(Startup.website == website)
                    )
                    existing = result.scalar_one_or_none()

                    if existing:
                        total_skipped += 1
                        continue

                startup_create = StartupCreate(**startup_data)
                await self.startup_service.create_startup(db, startup_create)
                total_new += 1

            except Exception as e:
                logger.error(f"Error saving startup: {str(e)}")
                total_skipped += 1
                continue

        await db.commit()

        completed_at = datetime.utcnow()
        duration = (completed_at - started_at).total_seconds()

        return {
            "status": "completed",
            "startups_found": len(all_startups),
            "startups_new": total_new,
            "startups_updated": 0,
            "duplicates_removed": total_skipped,
            "duration_seconds": duration
        }

    async def search_sectors(
        self,
        db: AsyncSession,
        sectors: List[str],
        num_per_sector: int = 30
    ) -> Dict:
        """
        Search for startups in specific sectors.

        Args:
            db: Database session
            sectors: List of sector names (e.g., ["fintech", "AI", "biotech"])
            num_per_sector: Number of results per sector

        Returns:
            Dictionary with scraping results
        """
        all_startups = []

        for sector in sectors:
            exa = self._get_exa_service()
            startups = await exa.search_by_sector(
                sector=sector,
                num_results=num_per_sector
            )
            all_startups.extend(startups)

        # Process all startups
        started_at = datetime.utcnow()
        total_new = 0
        total_skipped = 0

        for startup_data in all_startups:
            try:
                website = startup_data.get('website')
                if website:
                    result = await db.execute(
                        select(Startup).where(Startup.website == website)
                    )
                    existing = result.scalar_one_or_none()

                    if existing:
                        total_skipped += 1
                        continue

                startup_create = StartupCreate(**startup_data)
                await self.startup_service.create_startup(db, startup_create)
                total_new += 1

            except Exception as e:
                logger.error(f"Error saving startup: {str(e)}")
                total_skipped += 1
                continue

        await db.commit()

        completed_at = datetime.utcnow()
        duration = (completed_at - started_at).total_seconds()

        return {
            "status": "completed",
            "startups_found": len(all_startups),
            "startups_new": total_new,
            "startups_updated": 0,
            "duplicates_removed": total_skipped,
            "duration_seconds": duration
        }

    async def get_scraping_logs(
        self,
        db: AsyncSession,
        limit: int = 20
    ) -> List[ScrapingLog]:
        """Get recent dealflow scraping logs."""
        result = await db.execute(
            select(ScrapingLog)
            .where(ScrapingLog.source == "exa-dealflow")
            .order_by(ScrapingLog.started_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
