from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List
from app.models.startup import Startup
from app.schemas.startup import StartupCreate, StartupUpdate


class StartupService:
    """Service for Startup CRUD operations."""

    async def create_startup(self, db: AsyncSession, startup_data: StartupCreate) -> Startup:
        """Create a new startup."""
        db_startup = Startup(**startup_data.model_dump())
        db.add(db_startup)
        await db.commit()
        await db.refresh(db_startup)
        return db_startup

    async def get_startup(self, db: AsyncSession, startup_id: int) -> Optional[Startup]:
        """Get a startup by ID."""
        result = await db.execute(
            select(Startup).where(Startup.id == startup_id)
        )
        return result.scalar_one_or_none()

    async def get_startups(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        funding_stage: Optional[str] = None,
        industry: Optional[str] = None,
        source: Optional[str] = None,
        is_active: bool = True,
        search: Optional[str] = None
    ) -> tuple[List[Startup], int]:
        """Get startups with filtering and pagination."""
        # Build query
        query = select(Startup)

        # Apply filters
        filters = []
        if is_active is not None:
            filters.append(Startup.is_active == is_active)
        if funding_stage:
            filters.append(Startup.funding_stage == funding_stage)
        if industry:
            filters.append(Startup.industry.ilike(f"%{industry}%"))
        if source:
            filters.append(Startup.source == source)
        if search:
            search_filter = or_(
                Startup.name.ilike(f"%{search}%"),
                Startup.description.ilike(f"%{search}%")
            )
            filters.append(search_filter)

        if filters:
            query = query.where(*filters)

        # Get total count
        count_query = select(func.count()).select_from(Startup)
        if filters:
            count_query = count_query.where(*filters)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and ordering
        query = query.order_by(Startup.discovered_date.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        startups = result.scalars().all()

        return list(startups), total

    async def update_startup(
        self,
        db: AsyncSession,
        startup_id: int,
        startup_data: StartupUpdate
    ) -> Optional[Startup]:
        """Update a startup."""
        startup = await self.get_startup(db, startup_id)
        if not startup:
            return None

        update_data = startup_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(startup, field, value)

        await db.commit()
        await db.refresh(startup)
        return startup

    async def delete_startup(self, db: AsyncSession, startup_id: int) -> bool:
        """Delete a startup."""
        startup = await self.get_startup(db, startup_id)
        if not startup:
            return False

        await db.delete(startup)
        await db.commit()
        return True

    async def search_startups(
        self,
        db: AsyncSession,
        search_term: str,
        limit: int = 50
    ) -> List[Startup]:
        """Full-text search on startup name and description."""
        query = select(Startup).where(
            or_(
                Startup.name.ilike(f"%{search_term}%"),
                Startup.description.ilike(f"%{search_term}%")
            ),
            Startup.is_active == True
        ).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())
