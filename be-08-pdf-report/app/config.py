import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # PostgreSQL (from BE-04)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/flyrank"
    
    # Job settings
    JOB_TTL_SECONDS: int = 86400
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_BASE: float = 1.0
    DLQ_MAX_SIZE: int = 1000
    
    # Report settings
    REPORT_OUTPUT_DIR: str = "./output/reports"
    REPORT_BASE_URL: str = "http://localhost:8008/reports"
    
    # Alerting
    ALERT_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()