from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    print("Starting up...")
    await init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="VC Job Scraper API",
    description="API for scraping and tracking VC job opportunities",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "VC Job Scraper API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {
        "message": "VC Job Scraper API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routes
from app.api.routes import jobs, applications, scraping, startups, dealflow, dealflow_scraping, dashboard

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(scraping.router, prefix="/api/scraping", tags=["scraping"])
app.include_router(startups.router, prefix="/api/startups", tags=["startups"])
app.include_router(dealflow.router, prefix="/api/dealflow", tags=["dealflow"])
app.include_router(dealflow_scraping.router, prefix="/api/dealflow-scraping", tags=["dealflow-scraping"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
