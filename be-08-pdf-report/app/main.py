from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import ValidationError

from app.config import settings
from app.schemas import (
    ReportJobCreate, ReportJobResponse, ReportJobDetail, ReportJobListResponse,
    ReportStatus, HealthResponse
)
from app.queue import get_redis, ReportJobQueue, lifespan as queue_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    app.state.redis = await get_redis()
    app.state.queue = ReportJobQueue(app.state.redis)
    yield
    await app.state.redis.close()


app = FastAPI(
    title="PDF Report Generator API",
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


@app.post("/reports", response_model=ReportJobResponse, status_code=202)
async def create_report_job(job_data: ReportJobCreate):
    """Submit a report generation job for background processing."""
    job = await app.state.queue.create_job(job_data)
    
    return ReportJobResponse(
        job_id=job.job_id,
        status=job.status,
        message="Report job accepted for processing. Poll GET /reports/{job_id} for status."
    )


@app.get("/reports/{job_id}", response_model=ReportJobDetail)
async def get_report_job_status(job_id: str):
    """Get report job status and result."""
    job = await app.state.queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/reports", response_model=ReportJobListResponse)
async def list_report_jobs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: Optional[ReportStatus] = Query(None)
):
    """List report jobs with optional status filter."""
    return await app.state.queue.list_jobs(limit=limit, offset=offset, status=status)


@app.post("/reports/{job_id}/retry", response_model=ReportJobDetail)
async def retry_report_job(job_id: str):
    """Retry a failed or dead-letter report job."""
    job = await app.state.queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status not in (ReportStatus.FAILED, ReportStatus.DEAD_LETTER):
        raise HTTPException(status_code=400, detail="Job cannot be retried in current state")
    
    job.status = ReportStatus.QUEUED
    job.retries = 0
    job.error = None
    job.started_at = None
    job.completed_at = None
    
    await app.state.queue.update_job(job)
    await app.state.queue.redis.rpush(app.state.queue.queue_key, job_id)
    
    return job


@app.get("/reports/{job_id}/download")
async def download_report(job_id: str):
    """Download the generated report file."""
    job = await app.state.queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != ReportStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Report not ready")
    
    if not job.output:
        raise HTTPException(status_code=404, detail="Report file not found")
    
    # Extract filename from URL
    filename = job.output.filename
    filepath = f"./output/reports/{filename}"
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/pdf"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with queue and database metrics."""
    return await app.state.queue.get_health()


@app.get("/stats")
async def worker_stats():
    """Worker statistics."""
    return await app.state.queue.get_worker_stats()


@app.get("/dead-letter")
async def list_dead_letter(limit: int = Query(50, ge=1, le=200)):
    """List dead letter queue jobs."""
    return await app.state.queue.get_dead_letter_jobs(limit=limit)


@app.post("/dead-letter/{job_id}/retry", response_model=ReportJobDetail)
async def retry_dead_letter_job(job_id: str):
    """Retry a job from the dead letter queue."""
    job = await app.state.queue.retry_dead_letter_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found in dead letter queue")
    return job