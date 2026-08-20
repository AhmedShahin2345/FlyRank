from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import settings
from app.schemas import (
    JobCreate, JobResponse, JobDetail, JobListResponse,
    JobStatus, HealthResponse, EnrichJobInput
)
from app.queue import get_redis, JobQueue, lifespan as queue_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    app.state.redis = await get_redis()
    app.state.queue = JobQueue(app.state.redis)
    yield
    await app.state.redis.close()


app = FastAPI(
    title="Book Enrichment Background Job API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    fields = [f"{e.get('loc', ['?'])[-1]}: {e.get('msg', 'invalid')}" for e in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"detail": "invalid request body", "fields": fields},
    )


@app.post("/enrich", response_model=JobResponse, status_code=202)
async def create_enrich_job(
    job_data: JobCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    """
    Submit a book enrichment job for background processing.
    
    Returns 202 Accepted with a job_id for polling.
    Supports idempotency via Idempotency-Key header or request body.
    """
    # Use header if provided, otherwise use body
    if idempotency_key and not job_data.idempotency_key:
        job_data.idempotency_key = idempotency_key
    
    job = await app.state.queue.create_job(job_data)
    
    return JobResponse(
        job_id=job.job_id,
        status=job.status,
        message="Job accepted for processing. Poll GET /jobs/{job_id} for status."
    )


@app.get("/jobs/{job_id}", response_model=JobDetail)
async def get_job_status(job_id: str):
    """Get job status and result."""
    job = await app.state.queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: Optional[JobStatus] = Query(None)
):
    """List jobs with optional status filter."""
    return await app.state.queue.list_jobs(limit=limit, offset=offset, status=status)


@app.post("/jobs/{job_id}/retry", response_model=JobDetail)
async def retry_job(job_id: str):
    """Retry a failed or dead-letter job."""
    job = await app.state.queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status not in (JobStatus.FAILED, JobStatus.DEAD_LETTER):
        raise HTTPException(status_code=400, detail="Job cannot be retried in current state")
    
    # Reset and re-queue
    job.status = JobStatus.QUEUED
    job.retries = 0
    job.error = None
    job.started_at = None
    job.completed_at = None
    
    await app.state.queue.update_job(job)
    await app.state.queue.redis.zadd(
        app.state.queue.queue_key,
        {job_id: -job.priority.value}
    )
    
    return job


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with queue metrics."""
    return await app.state.queue.get_health()


@app.get("/stats")
async def worker_stats():
    """Worker statistics."""
    return await app.state.queue.get_worker_stats()


@app.get("/dead-letter")
async def list_dead_letter(limit: int = Query(50, ge=1, le=200)):
    """List dead letter queue jobs."""
    return await app.state.queue.get_dead_letter_jobs(limit=limit)


@app.post("/dead-letter/{job_id}/retry", response_model=JobDetail)
async def retry_dead_letter_job(job_id: str):
    """Retry a job from the dead letter queue."""
    job = await app.state.queue.retry_dead_letter_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found in dead letter queue")
    return job