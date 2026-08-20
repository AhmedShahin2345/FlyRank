import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Job settings
    JOB_TTL_SECONDS: int = 86400  # 24 hours
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_BASE: float = 1.0
    MAX_JOB_AGE_SECONDS: int = 3600  # 1 hour before considering stuck
    
    # LLM settings (inherited from BE-07)
    LLM_BASE_URL: str = "http://localhost:11434/v1"
    LLM_API_KEY: str = "ollama"
    LLM_MODEL: str = "gemma3:1b"
    LLM_TIMEOUT: float = 30.0
    LLM_CACHE: str = "1"
    LLM_ENABLED: str = "true"
    
    # Dead letter queue
    DLQ_MAX_SIZE: int = 1000
    
    # Alerting (log-based for now)
    ALERT_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()