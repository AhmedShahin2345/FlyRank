import os
import sys
import time
import signal
import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import redis.asyncio as redis

# Add parent directory to path to import BE-07 pipeline
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "be-07-llm"))

from app.config import settings
from app.queue import JobQueue, get_redis
from app.schemas import JobStatus, EnrichJobOutput

# Import BE-07 pipeline components
from src.llm.pipeline import run_pipeline
from src.llm.schema import EnrichInput, EnrichOutput
from src.llm.stub import fallback_answer, stub_answer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("worker")


class BackgroundWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.redis: Optional[redis.Redis] = None
        self.queue: Optional[JobQueue] = None
        self.running = False
        self.current_job_id: Optional[str] = None
        self.start_time = time.time()
        
        # Initialize stats
        self.jobs_processed = 0
        self.jobs_failed = 0
        self.jobs_retried = 0

    async def start(self):
        """Start the worker."""
        self.redis = await get_redis()
        self.queue = JobQueue(self.redis)
        self.running = True
        
        # Initialize stats in Redis
        await self.redis.hset("worker:stats", mapping={
            "jobs_processed": "0",
            "jobs_failed": "0",
            "jobs_retried": "0",
            "started_at": str(self.start_time)
        })
        
        logger.info(f"Worker {self.worker_id} started")
        
        # Register signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._shutdown)
        
        await self._run_loop()

    def _shutdown(self):
        """Signal handler for graceful shutdown."""
        logger.info(f"Worker {self.worker_id} received shutdown signal")
        self.running = False

    async def _run_loop(self):
        """Main worker loop."""
        while self.running:
            try:
                job = await self.queue.claim_next_job(self.worker_id)
                if job:
                    await self._process_job(job)
                else:
                    # No jobs available, wait before polling again
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {self.worker_id} error in main loop: {e}")
                await asyncio.sleep(5)  # Back off on error

    async def _process_job(self, job):
        """Process a single job."""
        self.current_job_id = job.job_id
        logger.info(f"Worker {self.worker_id} processing job {job.job_id} (attempt {job.retries + 1})")
        
        try:
            # Convert job input to EnrichInput
            enrich_input = EnrichInput(
                title=job.input.title,
                description=job.input.description,
                price_gbp=job.input.price_gbp
            )
            
            # Check for stub/fallback modes
            if os.environ.get("LLM_STUB") == "1":
                result = stub_answer(enrich_input)
            elif os.environ.get("LLM_ENABLED", "true").lower() in ("false", "0", "no"):
                result = fallback_answer()
            else:
                # Run the actual pipeline
                result = run_pipeline(enrich_input, "v1")
            
            # Convert to EnrichJobOutput
            output = EnrichJobOutput(
                category=result.category.value,
                summary=result.summary,
                confidence=result.confidence,
                quality_flags=[flag.value for flag in result.quality_flags]
            )
            
            # Mark job as completed
            success = await self.queue.complete_job(job.job_id, self.worker_id, output)
            if success:
                self.jobs_processed += 1
                logger.info(f"Worker {self.worker_id} completed job {job.job_id}")
            else:
                logger.warning(f"Worker {self.worker_id} failed to complete job {job.job_id} (ownership lost)")
                
        except Exception as e:
            logger.error(f"Worker {self.worker_id} failed job {job.job_id}: {e}")
            # Mark job as failed (will handle retry/DLQ internally)
            await self.queue.fail_job(job.job_id, self.worker_id, str(e))
            self.jobs_failed += 1
        finally:
            self.current_job_id = None

    async def stop(self):
        """Stop the worker gracefully."""
        self.running = False
        if self.redis:
            await self.redis.close()
        logger.info(f"Worker {self.worker_id} stopped")


async def main():
    """Entry point for the worker."""
    worker_id = os.environ.get("WORKER_ID", f"worker-{os.getpid()}")
    worker = BackgroundWorker(worker_id)
    
    try:
        await worker.start()
    except KeyboardInterrupt:
        pass
    finally:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())