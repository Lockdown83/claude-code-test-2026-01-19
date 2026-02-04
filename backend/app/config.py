from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    # Database
    database_url: str = "sqlite+aiosqlite:///./vc_jobs.db"

    # Exa API
    exa_api_key: str = ""

    # CORS
    allowed_origins: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]

    # Celery/Redis
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # Scraping Settings
    scraping_rate_limit: float = 2.0
    scraping_user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

    # Deduplication
    duplicate_threshold: int = 85
    company_match_threshold: int = 90

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
