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

from app.config import settings
from app.queue import ReportJobQueue, get_redis
from app.schemas import ReportStatus, ReportJobOutput
from app.repository import BookRepository
from app.pdf_generator import generate_book_catalog_pdf


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("report_worker")


class ReportWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.redis: Optional[redis.Redis] = None
        self.queue: Optional[ReportJobQueue] = None
        self.running = False
        self.current_job_id: Optional[str] = None
        self.start_time = time.time()
        self.book_repo = BookRepository(settings.DATABASE_URL)
        
        self.jobs_processed = 0
        self.jobs_failed = 0
        self.jobs_retried = 0

    async def start(self):
        """Start the worker."""
        self.redis = await get_redis()
        self.queue = ReportJobQueue(self.redis)
        self.running = True
        
        await self.redis.hset("report_worker:stats", mapping={
            "jobs_processed": "0",
            "jobs_failed": "0",
            "jobs_retried": "0",
            "started_at": str(self.start_time)
        })
        
        logger.info(f"Report worker {self.worker_id} started")
        
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._shutdown)
        
        await self._run_loop()

    def _shutdown(self):
        """Signal handler for graceful shutdown."""
        logger.info(f"Report worker {self.worker_id} received shutdown signal")
        self.running = False

    async def _run_loop(self):
        """Main worker loop."""
        while self.running:
            try:
                job = await self.queue.claim_next_job(self.worker_id)
                if job:
                    await self._process_job(job)
                else:
                    await asyncio.sleep(2)  # Longer sleep for reports
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Report worker {self.worker_id} error in main loop: {e}")
                await asyncio.sleep(5)

    async def _process_job(self, job):
        """Process a single report job."""
        self.current_job_id = job.job_id
        logger.info(f"Report worker {self.worker_id} processing job {job.job_id} (type: {job.input.report_type})")
        
        try:
            if job.input.report_type.value == "book_catalog":
                await self._generate_book_catalog_report(job)
            else:
                raise ValueError(f"Unknown report type: {job.input.report_type}")
                
        except Exception as e:
            logger.error(f"Report worker {self.worker_id} failed job {job.job_id}: {e}")
            await self.queue.fail_job(job.job_id, self.worker_id, str(e))
            self.jobs_failed += 1
        finally:
            self.current_job_id = None

    async def _generate_book_catalog_report(self, job):
        """Generate a book catalog PDF report."""
        # Get books from database
        books = self.book_repo.get_all_books(job.input.filters)
        
        if not books:
            raise ValueError("No books found matching the criteria")
        
        # Get stats for the report
        stats = self.book_repo.get_price_stats()
        
        # Generate PDF
        result = generate_book_catalog_pdf(
            books=books,
            output_dir=settings.REPORT_OUTPUT_DIR,
            base_url=settings.REPORT_BASE_URL,
            title=job.input.title,
            filters=job.input.filters,
            stats=stats
        )
        
        # Create output object
        output = ReportJobOutput(
            report_url=result["url"],
            filename=result["filename"],
            page_count=result["page_count"],
            file_size_bytes=result["file_size_bytes"],
            generated_at=result["generated_at"]
        )
        
        # Mark job as completed
        success = await self.queue.complete_job(job.job_id, self.worker_id, output)
        if success:
            self.jobs_processed += 1
            logger.info(f"Report worker {self.worker_id} completed job {job.job_id}: {result['filename']}")
        else:
            logger.warning(f"Report worker {self.worker_id} failed to complete job {job.job_id} (ownership lost)")

    async def stop(self):
        """Stop the worker gracefully."""
        self.running = False
        if self.redis:
            await self.redis.close()
        logger.info(f"Report worker {self.worker_id} stopped")


async def main():
    """Entry point for the worker."""
    worker_id = os.environ.get("WORKER_ID", f"report-worker-{os.getpid()}")
    worker = ReportWorker(worker_id)
    
    try:
        await worker.start()
    except KeyboardInterrupt:
        pass
    finally:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())