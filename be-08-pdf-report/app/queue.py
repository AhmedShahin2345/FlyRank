import json
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

import redis.asyncio as redis
from redis.asyncio import Redis

from app.config import settings
from app.schemas import (
    ReportStatus, ReportJobCreate, ReportJobDetail, ReportJobListResponse,
    ReportJobInput, ReportJobOutput, HealthResponse, WorkerStats
)


class ReportJobQueue:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.queue_key = "reports:queue"
        self.processing_key = "reports:processing"
        self.job_prefix = "report_job:"
        self.idempotency_prefix = "report_idempotency:"
        self.dlq_key = "reports:dead_letter"
        self.stats_key = "report_worker:stats"
        self.lock_prefix = "lock:report_job:"

    async def _get_job_key(self, job_id: str) -> str:
        return f"{self.job_prefix}{job_id}"

    async def create_job(self, job_data: ReportJobCreate) -> ReportJobDetail:
        """Create a new report job with optional idempotency key."""
        if job_data.idempotency_key:
            existing_job_id = await self.redis.get(
                f"{self.idempotency_prefix}{job_data.idempotency_key}"
            )
            if existing_job_id:
                existing_job = await self.get_job(existing_job_id.decode())
                if existing_job:
                    return existing_job

        job_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        job = ReportJobDetail(
            job_id=job_id,
            status=ReportStatus.PENDING,
            input=job_data.input,
            callback_url=job_data.callback_url,
            idempotency_key=job_data.idempotency_key,
            created_at=now,
        )

        job_key = await self._get_job_key(job_id)
        await self.redis.setex(
            job_key,
            settings.JOB_TTL_SECONDS,
            job.model_dump_json()
        )

        # Add to queue (FIFO for reports)
        await self.redis.lpush(self.queue_key, job_id)
        
        # Use LPUSH for queue, LRANGE for reading (FIFO)
        # Actually, let's use a list with LPUSH/RPOP for FIFO
        # But we added with LPUSH, so we need RPOP for FIFO
        # Let's use RPUSH/LPOP for proper FIFO
        
        # Re-do with RPUSH
        await self.redis.lrem(self.queue_key, 0, job_id)  # Remove if added
        await self.redis.rpush(self.queue_key, job_id)

        if job_data.idempotency_key:
            await self.redis.setex(
                f"{self.idempotency_prefix}{job_data.idempotency_key}",
                settings.JOB_TTL_SECONDS,
                job_id
            )

        return job

    async def get_job(self, job_id: str) -> Optional[ReportJobDetail]:
        """Get job by ID."""
        job_key = await self._get_job_key(job_id)
        data = await self.redis.get(job_key)
        if data:
            return ReportJobDetail.model_validate_json(data)
        return None

    async def update_job(self, job: ReportJobDetail) -> None:
        """Update job in storage."""
        job_key = await self._get_job_key(job.job_id)
        await self.redis.setex(
            job_key,
            settings.JOB_TTL_SECONDS,
            job.model_dump_json()
        )

    async def claim_next_job(self, worker_id: str) -> Optional[ReportJobDetail]:
        """Atomically claim the next job (FIFO)."""
        # Use Lua script for atomic claim
        lua_script = """
        local queue_key = KEYS[1]
        local processing_key = KEYS[2]
        local job_prefix = KEYS[3]
        local worker_id = ARGV[1]
        local ttl = tonumber(ARGV[2])
        
        local job_id = redis.call('LPOP', queue_key)
        if not job_id then
            return nil
        end
        
        local job_key = job_prefix .. job_id
        local job_data = redis.call('GET', job_key)
        if not job_data then
            return nil
        end
        
        redis.call('HSET', processing_key, job_id, worker_id)
        redis.call('EXPIRE', processing_key, ttl)
        
        return job_data
        """
        
        script = self.redis.register_script(lua_script)
        result = await script(
            keys=[self.queue_key, self.processing_key, self.job_prefix],
            args=[worker_id, settings.JOB_TTL_SECONDS]
        )
        
        if result:
            job_data = json.loads(result)
            job = ReportJobDetail.model_validate(job_data)
            job.status = ReportStatus.PROCESSING
            job.started_at = datetime.now(timezone.utc)
            await self.update_job(job)
            return job
        return None

    async def release_job(self, job_id: str, worker_id: str) -> bool:
        """Release a job back to queue (for retry)."""
        owner = await self.redis.hget(self.processing_key, job_id)
        if owner and owner.decode() != worker_id:
            return False

        job = await self.get_job(job_id)
        if not job:
            return False

        job.retries += 1
        job.status = ReportStatus.QUEUED
        job.started_at = None
        
        await self.redis.rpush(self.queue_key, job_id)
        await self.redis.hdel(self.processing_key, job_id)
        await self.update_job(job)
        return True

    async def complete_job(self, job_id: str, worker_id: str, output: ReportJobOutput) -> bool:
        """Mark job as completed with output."""
        owner = await self.redis.hget(self.processing_key, job_id)
        if owner and owner.decode() != worker_id:
            return False

        job = await self.get_job(job_id)
        if not job:
            return False

        job.status = ReportStatus.COMPLETED
        job.output = output
        job.completed_at = datetime.now(timezone.utc)
        
        await self.redis.hdel(self.processing_key, job_id)
        await self.update_job(job)
        
        await self._increment_stat("jobs_processed")
        return True

    async def fail_job(self, job_id: str, worker_id: str, error: str) -> bool:
        """Mark job as failed, move to DLQ if max retries exceeded."""
        owner = await self.redis.hget(self.processing_key, job_id)
        if owner and owner.decode() != worker_id:
            return False

        job = await self.get_job(job_id)
        if not job:
            return False

        job.error = error
        job.retries += 1

        if job.retries > settings.MAX_RETRIES:
            job.status = ReportStatus.DEAD_LETTER
            job.completed_at = datetime.now(timezone.utc)
            
            await self.redis.lpush(self.dlq_key, job.model_dump_json())
            await self.redis.ltrim(self.dlq_key, 0, settings.DLQ_MAX_SIZE - 1)
            
            await self._increment_stat("jobs_failed")
        else:
            job.status = ReportStatus.QUEUED
            job.started_at = None
            await self.redis.rpush(self.queue_key, job_id)
            await self._increment_stat("jobs_retried")

        await self.redis.hdel(self.processing_key, job_id)
        await self.update_job(job)
        return True

    async def _increment_stat(self, key: str) -> None:
        await self.redis.hincrby(self.stats_key, key, 1)

    async def list_jobs(self, limit: int = 50, offset: int = 0, status: Optional[ReportStatus] = None) -> ReportJobListResponse:
        """List jobs with optional status filter."""
        # Use SCAN for production, simplified here
        pattern = f"{self.job_prefix}*"
        jobs = []
        cursor = 0
        count = 0
        
        while count < limit + offset:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)
            for key in keys:
                data = await self.redis.get(key)
                if data:
                    job = ReportJobDetail.model_validate_json(data)
                    if status is None or job.status == status:
                        if count >= offset:
                            jobs.append(job)
                        count += 1
                        if len(jobs) >= limit:
                            break
            if cursor == 0:
                break
        
        return ReportJobListResponse(jobs=jobs, total=count, limit=limit, offset=offset)

    async def get_health(self) -> HealthResponse:
        """Get queue health metrics."""
        queue_length = await self.redis.llen(self.queue_key)
        processing_count = await self.redis.hlen(self.processing_key)
        dead_letter_count = await self.redis.llen(self.dlq_key)
        
        try:
            await self.redis.ping()
            redis_connected = True
        except Exception:
            redis_connected = False
        
        # Check database connection
        try:
            import psycopg2
            conn = psycopg2.connect(settings.DATABASE_URL, connect_timeout=2)
            conn.close()
            db_connected = True
        except Exception:
            db_connected = False

        return HealthResponse(
            status="healthy" if (redis_connected and db_connected) else "degraded",
            redis_connected=redis_connected,
            database_connected=db_connected,
            queue_length=queue_length,
            processing_count=processing_count,
            dead_letter_count=dead_letter_count
        )

    async def get_worker_stats(self) -> WorkerStats:
        """Get worker statistics."""
        stats_data = await self.redis.hgetall(self.stats_key)
        stats = {k.decode(): int(v) for k, v in stats_data.items()}
        
        return WorkerStats(
            jobs_processed=stats.get("jobs_processed", 0),
            jobs_failed=stats.get("jobs_failed", 0),
            jobs_retried=stats.get("jobs_retried", 0),
            uptime_seconds=time.time() - stats.get("started_at", time.time())
        )

    async def get_dead_letter_jobs(self, limit: int = 50) -> List[ReportJobDetail]:
        """Get jobs from dead letter queue."""
        jobs = []
        for i in range(min(limit, await self.redis.llen(self.dlq_key))):
            data = await self.redis.lindex(self.dlq_key, i)
            if data:
                jobs.append(ReportJobDetail.model_validate_json(data))
        return jobs

    async def retry_dead_letter_job(self, job_id: str) -> Optional[ReportJobDetail]:
        """Retry a job from dead letter queue."""
        jobs = await self.get_dead_letter_jobs(1000)
        for job in jobs:
            if job.job_id == job_id:
                await self.redis.lrem(self.dlq_key, 1, job.model_dump_json())
                job.status = ReportStatus.QUEUED
                job.retries = 0
                job.error = None
                job.started_at = None
                job.completed_at = None
                await self.redis.rpush(self.queue_key, job_id)
                await self.update_job(job)
                return job
        return None


async def get_redis() -> Redis:
    """Get Redis connection."""
    return redis.from_url(settings.REDIS_URL, decode_responses=False)


@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager."""
    app.state.redis = await get_redis()
    app.state.queue = ReportJobQueue(app.state.redis)
    yield
    await app.state.redis.close()