import pytest
import asyncio
import os
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import redis.asyncio as redis
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Set test environment
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["LLM_STUB"] = "1"
os.environ["LLM_ENABLED"] = "false"

from app.config import settings
from app.schemas import (
    JobStatus, JobPriority, JobCreate, JobDetail, EnrichJobInput, EnrichJobOutput
)
from app.queue import JobQueue
from app.main import app


@pytest.fixture(scope="session")
def redis_client():
    """Create a test Redis client."""
    return redis.from_url("redis://localhost:6379/1", decode_responses=False)


@pytest.fixture(autouse=True)
async def _cleanup_redis(redis_client):
    """Cleanup Redis before and after each test."""
    await redis_client.flushdb()
    yield
    await redis_client.flushdb()
    await redis_client.close()


@pytest.fixture
def job_queue(redis_client):
    """Create a JobQueue instance for testing."""
    return JobQueue(redis_client)


@pytest.fixture
def async_client(redis_client):
    """Create async test client with lifespan."""
    from app.queue import JobQueue
    app.state.redis = redis_client
    app.state.queue = JobQueue(redis_client)
    
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def _create_client():
        from httpx import AsyncClient, ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            return client
    
    client = loop.run_until_complete(_create_client())
    yield client
    loop.run_until_complete(client.aclose())
    loop.close()


class TestJobQueue:
    """Tests for the JobQueue class."""

    @pytest.mark.asyncio
    async def test_create_job_basic(self, job_queue):
        """Test creating a basic job."""
        job_data = JobCreate(
            input=EnrichJobInput(
                title="Test Book",
                description="A test book",
                price_gbp=10.0
            )
        )
        job = await job_queue.create_job(job_data)
        
        assert job.job_id is not None
        assert job.status == JobStatus.PENDING
        assert job.input.title == "Test Book"
        assert job.priority == JobPriority.NORMAL
        assert job.idempotency_key is None

    @pytest.mark.asyncio
    async def test_create_job_with_idempotency(self, job_queue):
        """Test idempotency key prevents duplicate jobs."""
        job_data = JobCreate(
            input=EnrichJobInput(
                title="Test Book",
                description="A test book",
                price_gbp=10.0
            ),
            idempotency_key="test-key-123"
        )
        
        job1 = await job_queue.create_job(job_data)
        job2 = await job_queue.create_job(job_data)
        
        assert job1.job_id == job2.job_id
        assert job1.idempotency_key == "test-key-123"

    @pytest.mark.asyncio
    async def test_create_job_with_priority(self, job_queue):
        """Test job creation with different priorities."""
        low_job = JobCreate(
            input=EnrichJobInput(title="Low", price_gbp=1.0),
            priority=JobPriority.LOW
        )
        high_job = JobCreate(
            input=EnrichJobInput(title="High", price_gbp=1.0),
            priority=JobPriority.HIGH
        )
        
        low = await job_queue.create_job(low_job)
        high = await job_queue.create_job(high_job)
        
        assert low.priority == JobPriority.LOW
        assert high.priority == JobPriority.HIGH

    @pytest.mark.asyncio
    async def test_get_job(self, job_queue):
        """Test retrieving a job by ID."""
        job_data = JobCreate(
            input=EnrichJobInput(title="Test", price_gbp=1.0)
        )
        created = await job_queue.create_job(job_data)
        
        retrieved = await job_queue.get_job(created.job_id)
        
        assert retrieved is not None
        assert retrieved.job_id == created.job_id
        assert retrieved.status == JobStatus.PENDING

    @pytest.mark.asyncio
    async def test_get_nonexistent_job(self, job_queue):
        """Test retrieving a non-existent job returns None."""
        job = await job_queue.get_job("non-existent-id")
        assert job is None

    @pytest.mark.asyncio
    async def test_claim_next_job_priority_order(self, job_queue):
        """Test that higher priority jobs are claimed first."""
        low = JobCreate(input=EnrichJobInput(title="Low", price_gbp=1.0), priority=JobPriority.LOW)
        normal = JobCreate(input=EnrichJobInput(title="Normal", price_gbp=1.0), priority=JobPriority.NORMAL)
        high = JobCreate(input=EnrichJobInput(title="High", price_gbp=1.0), priority=JobPriority.HIGH)
        
        await job_queue.create_job(low)
        await job_queue.create_job(normal)
        await job_queue.create_job(high)
        
        job1 = await job_queue.claim_next_job("worker-1")
        job2 = await job_queue.claim_next_job("worker-1")
        job3 = await job_queue.claim_next_job("worker-1")
        
        assert job1.priority == JobPriority.HIGH
        assert job2.priority == JobPriority.NORMAL
        assert job3.priority == JobPriority.LOW

    @pytest.mark.asyncio
    async def test_claim_next_job_updates_status(self, job_queue):
        """Test that claiming a job updates its status to PROCESSING."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        
        claimed = await job_queue.claim_next_job("worker-1")
        
        assert claimed.status == JobStatus.PROCESSING
        assert claimed.started_at is not None
        assert claimed.job_id == created.job_id

    @pytest.mark.asyncio
    async def test_complete_job(self, job_queue):
        """Test completing a job with output."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        claimed = await job_queue.claim_next_job("worker-1")
        
        output = EnrichJobOutput(
            category="fiction",
            summary="Test summary",
            confidence=0.9,
            quality_flags=[]
        )
        
        success = await job_queue.complete_job(claimed.job_id, "worker-1", output)
        
        assert success is True
        
        job = await job_queue.get_job(claimed.job_id)
        assert job.status == JobStatus.COMPLETED
        assert job.output is not None
        assert job.output.category == "fiction"
        assert job.completed_at is not None

    @pytest.mark.asyncio
    async def test_complete_job_wrong_worker(self, job_queue):
        """Test that completing a job with wrong worker ID fails."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        claimed = await job_queue.claim_next_job("worker-1")
        
        output = EnrichJobOutput(category="fiction", summary="Test", confidence=0.9, quality_flags=[])
        success = await job_queue.complete_job(claimed.job_id, "worker-2", output)
        
        assert success is False

    @pytest.mark.asyncio
    async def test_fail_job_retry(self, job_queue):
        """Test failing a job schedules retry when under max retries."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        claimed = await job_queue.claim_next_job("worker-1")
        
        success = await job_queue.fail_job(claimed.job_id, "worker-1", "Test error")
        
        assert success is True
        
        job = await job_queue.get_job(claimed.job_id)
        assert job.status == JobStatus.QUEUED
        assert job.retries == 1
        assert job.error == "Test error"
        assert job.started_at is None

    @pytest.mark.asyncio
    async def test_fail_job_dead_letter(self, job_queue):
        """Test failing a job at max retries moves to dead letter queue."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
    
        for i in range(settings.MAX_RETRIES - 1):
            claimed = await job_queue.claim_next_job("worker-1")
            await job_queue.fail_job(claimed.job_id, "worker-1", f"Error {i}")
    
        claimed = await job_queue.claim_next_job("worker-1")
        success = await job_queue.fail_job(claimed.job_id, "worker-1", "Final error")
    
        assert success is True
    
        job = await job_queue.get_job(claimed.job_id)
        assert job.status == JobStatus.DEAD_LETTER
        assert job.retries == settings.MAX_RETRIES
        
        dlq_jobs = await job_queue.get_dead_letter_jobs()
        assert len(dlq_jobs) == 1
        assert dlq_jobs[0].job_id == claimed.job_id

    @pytest.mark.asyncio
    async def test_fail_job_wrong_worker(self, job_queue):
        """Test that failing a job with wrong worker ID fails."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        claimed = await job_queue.claim_next_job("worker-1")
        
        success = await job_queue.fail_job(claimed.job_id, "worker-2", "Test error")
        
        assert success is False

    @pytest.mark.asyncio
    async def test_release_job(self, job_queue):
        """Test releasing a job back to queue."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
        claimed = await job_queue.claim_next_job("worker-1")
        
        success = await job_queue.release_job(claimed.job_id, "worker-1")
        
        assert success is True
        
        job = await job_queue.get_job(claimed.job_id)
        assert job.status == JobStatus.QUEUED
        assert job.retries == 1
        assert job.started_at is None

    @pytest.mark.asyncio
    async def test_retry_dead_letter_job(self, job_queue):
        """Test retrying a job from dead letter queue."""
        job_data = JobCreate(input=EnrichJobInput(title="Test", price_gbp=1.0))
        created = await job_queue.create_job(job_data)
    
        for i in range(settings.MAX_RETRIES - 1):
            claimed = await job_queue.claim_next_job("worker-1")
            await job_queue.fail_job(claimed.job_id, "worker-1", f"Error {i}")
        
        claimed = await job_queue.claim_next_job("worker-1")
        await job_queue.fail_job(claimed.job_id, "worker-1", "Final error")
    
        retried = await job_queue.retry_dead_letter_job(claimed.job_id)
    
        assert retried is not None
        assert retried.status == JobStatus.QUEUED
        assert retried.retries == 0
        assert retried.error is None
        
        dlq_jobs = await job_queue.get_dead_letter_jobs()
        assert len(dlq_jobs) == 0

    @pytest.mark.asyncio
    async def test_list_jobs(self, job_queue):
        """Test listing jobs with filters."""
        for i in range(5):
            job_data = JobCreate(
                input=EnrichJobInput(title=f"Book {i}", price_gbp=1.0),
                priority=JobPriority.HIGH if i < 2 else JobPriority.NORMAL
            )
            await job_queue.create_job(job_data)
        
        claimed = await job_queue.claim_next_job("worker-1")
        
        all_jobs = await job_queue.list_jobs(limit=10)
        assert all_jobs.total == 5
        
        pending = await job_queue.list_jobs(limit=10, status=JobStatus.PENDING)
        assert all(j.status == JobStatus.PENDING for j in pending.jobs)
        
        processing = await job_queue.list_jobs(limit=10, status=JobStatus.PROCESSING)
        assert len(processing.jobs) == 1
        assert processing.jobs[0].job_id == claimed.job_id

    @pytest.mark.asyncio
    async def test_health_check(self, job_queue):
        """Test health check endpoint."""
        health = await job_queue.get_health()
        
        assert health.status in ("healthy", "degraded")
        assert isinstance(health.redis_connected, bool)
        assert health.queue_length >= 0
        assert health.processing_count >= 0
        assert health.dead_letter_count >= 0

    @pytest.mark.asyncio
    async def test_worker_stats(self, job_queue):
        """Test worker statistics."""
        stats = await job_queue.get_worker_stats()
        
        assert stats.jobs_processed >= 0
        assert stats.jobs_failed >= 0
        assert stats.jobs_retried >= 0
        assert stats.uptime_seconds >= 0


class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    @pytest.mark.asyncio
    async def test_create_enrich_job(self, async_client):
        """Test POST /enrich endpoint."""
        response = await async_client.post(
            "/enrich",
            json={
                "input": {
                    "title": "Test Book",
                    "description": "A test book",
                    "price_gbp": 10.0
                }
            }
        )
        
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "pending"
        assert "accepted" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_create_enrich_job_with_idempotency_header(self, async_client):
        """Test POST /enrich with Idempotency-Key header."""
        response1 = await async_client.post(
            "/enrich",
            json={"input": {"title": "Test", "price_gbp": 1.0}},
            headers={"Idempotency-Key": "test-header-key"}
        )
        response2 = await async_client.post(
            "/enrich",
            json={"input": {"title": "Test", "price_gbp": 1.0}},
            headers={"Idempotency-Key": "test-header-key"}
        )
        
        assert response1.status_code == 202
        assert response2.status_code == 202
        assert response1.json()["job_id"] == response2.json()["job_id"]

    @pytest.mark.asyncio
    async def test_get_job_status(self, async_client):
        """Test GET /jobs/{job_id} endpoint."""
        create_resp = await async_client.post(
            "/enrich",
            json={"input": {"title": "Test", "price_gbp": 1.0}}
        )
        job_id = create_resp.json()["job_id"]
        
        response = await async_client.get(f"/jobs/{job_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_get_nonexistent_job(self, async_client):
        """Test GET /jobs/{job_id} for non-existent job."""
        response = await async_client.get("/jobs/non-existent-id")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_jobs(self, async_client):
        """Test GET /jobs endpoint."""
        for i in range(3):
            await async_client.post("/enrich", json={"input": {"title": f"Book {i}", "price_gbp": 1.0}})
        
        response = await async_client.get("/jobs?limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3
        assert len(data["jobs"]) >= 3

    @pytest.mark.asyncio
    async def test_health_check(self, async_client):
        """Test GET /health endpoint."""
        response = await async_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "redis_connected" in data
        assert "queue_length" in data

    @pytest.mark.asyncio
    async def test_validation_error(self, async_client):
        """Test validation error returns 400 with field details."""
        response = await async_client.post(
            "/enrich",
            json={"input": {"description": "Missing title", "price_gbp": 1.0}}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "invalid request body"
        assert "fields" in data
        assert any("title" in f for f in data["fields"])