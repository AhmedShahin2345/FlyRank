from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class JobStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class JobPriority(int, Enum):
    LOW = 0
    NORMAL = 50
    HIGH = 100


class EnrichJobInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    price_gbp: float = Field(ge=0, le=100000)


class EnrichJobOutput(BaseModel):
    category: str
    summary: str
    confidence: float = Field(ge=0, le=1)
    quality_flags: List[str] = Field(max_length=4)


class JobCreate(BaseModel):
    input: EnrichJobInput
    idempotency_key: Optional[str] = None
    priority: JobPriority = JobPriority.NORMAL
    callback_url: Optional[str] = None


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str


class JobDetail(BaseModel):
    job_id: str
    status: JobStatus
    input: EnrichJobInput
    output: Optional[EnrichJobOutput] = None
    error: Optional[str] = None
    retries: int = 0
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    idempotency_key: Optional[str] = None
    priority: JobPriority = JobPriority.NORMAL
    callback_url: Optional[str] = None


class JobListResponse(BaseModel):
    jobs: List[JobDetail]
    total: int
    limit: int
    offset: int


class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    queue_length: int
    processing_count: int
    dead_letter_count: int


class WorkerStats(BaseModel):
    jobs_processed: int
    jobs_failed: int
    jobs_retried: int
    current_job_id: Optional[str] = None
    uptime_seconds: float