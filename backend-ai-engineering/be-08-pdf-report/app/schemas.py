from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ReportStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class ReportType(str, Enum):
    BOOK_CATALOG = "book_catalog"
    USER_SUMMARY = "user_summary"
    CUSTOM = "custom"


class ReportJobInput(BaseModel):
    report_type: ReportType = ReportType.BOOK_CATALOG
    title: str = Field(default="Book Catalog Report", max_length=200)
    filters: Dict[str, Any] = Field(default_factory=dict)
    template_options: Dict[str, Any] = Field(default_factory=dict)


class ReportJobOutput(BaseModel):
    report_url: str
    filename: str
    page_count: int
    file_size_bytes: int
    generated_at: datetime


class ReportJobCreate(BaseModel):
    input: ReportJobInput
    idempotency_key: Optional[str] = None
    callback_url: Optional[str] = None


class ReportJobResponse(BaseModel):
    job_id: str
    status: ReportStatus
    message: str


class ReportJobDetail(BaseModel):
    job_id: str
    status: ReportStatus
    input: ReportJobInput
    output: Optional[ReportJobOutput] = None
    error: Optional[str] = None
    retries: int = 0
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    idempotency_key: Optional[str] = None
    callback_url: Optional[str] = None


class ReportJobListResponse(BaseModel):
    jobs: List[ReportJobDetail]
    total: int
    limit: int
    offset: int


class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    database_connected: bool
    queue_length: int
    processing_count: int
    dead_letter_count: int


class WorkerStats(BaseModel):
    jobs_processed: int
    jobs_failed: int
    jobs_retried: int
    current_job_id: Optional[str] = None
    uptime_seconds: float