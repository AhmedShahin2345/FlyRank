# BE-06 — Your First Background Job

The `POST /enrich` endpoint from BE-07 is now asynchronous. The API accepts a request, returns `202 Accepted` with a `job_id`, and a background worker processes the LLM enrichment. A status endpoint lets callers poll for the result.

This is the professional pattern for everything slow: accept fast, work in the background, report status. It exercises the non-negotiables: jobs **will** run twice (idempotency), they **will** fail (retries with backoff), and someone must find out (dead-letter queue + alerting).

## What it does

A catalogue pipeline gets a record that a human would normally have to read and file by hand. Instead of blocking the request, the API:

1. **Accepts** the request instantly (`202` + `job_id`)
2. **Queues** the work with priority and idempotency key
3. **Processes** it in a separate worker (runs the BE-07 pipeline)
4. **Reports** status/result via `GET /jobs/{job_id}`
5. **Handles failures** with exponential backoff, then dead-letter queue

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│    Redis    │
│             │ 202 │   (API)     │     │  (Queue)    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐            │
                    │   Worker    │◀───────────┘
                    │  (BE-07     │
                    │  Pipeline)  │
                    └─────────────┘
```

## Quick Start

```bash
# 1. Copy env and configure
cp .env.example .env
# Edit .env with your Redis URL and LLM settings

# 2. Start Redis (or use docker-compose)
docker run -d -p 6379:6379 redis:7-alpine

# 3. Start the API
uvicorn app.main:app --port 8006

# 4. Start worker(s) in separate terminal(s)
python worker/main.py
# Or run multiple workers:
WORKER_ID=worker-2 python worker/main.py
```

## Docker Compose (Recommended)

```bash
docker-compose up --build
```

This starts Redis, the API on port 8006, and 2 workers.

## Endpoints

### `POST /enrich` — Submit enrichment job

Returns `202 Accepted` immediately with a `job_id`.

**Request:**
```json
{
  "input": {
    "title": "A Light in the Attic",
    "description": "Poetry from Shel Silverstein.",
    "price_gbp": 51.77
  },
  "idempotency_key": "optional-unique-key",
  "priority": 50,
  "callback_url": "https://your.app/webhook"
}
```

**Response (202):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Job accepted for processing. Poll GET /jobs/{job_id} for status."
}
```

**Idempotency:** Provide `Idempotency-Key` header or `idempotency_key` in body. Same key = same job returned.

**Priority:** `0` (low), `50` (normal), `100` (high). Higher priority jobs are processed first.

### `GET /jobs/{job_id}` — Get job status/result

**Response (200):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "input": {"title": "...", "description": "...", "price_gbp": 51.77},
  "output": {
    "category": "fiction",
    "summary": "Classic illustrated poetry from Shel Silverstein.",
    "confidence": 0.9,
    "quality_flags": []
  },
  "error": null,
  "retries": 0,
  "created_at": "2026-08-20T10:30:00Z",
  "started_at": "2026-08-20T10:30:01Z",
  "completed_at": "2026-08-20T10:30:03Z",
  "idempotency_key": "optional-unique-key",
  "priority": 50,
  "callback_url": null
}
```

**Status values:** `pending` → `queued` → `processing` → `completed` | `failed` | `dead_letter`

### `GET /jobs` — List jobs

Query params: `limit` (default 50), `offset` (default 0), `status` (filter)

### `POST /jobs/{job_id}/retry` — Retry failed/dead-letter job

Resets retries, clears error, re-queues with same priority.

### `GET /health` — Health check with queue metrics

```json
{
  "status": "healthy",
  "redis_connected": true,
  "queue_length": 12,
  "processing_count": 2,
  "dead_letter_count": 0
}
```

### `GET /stats` — Worker statistics

```json
{
  "jobs_processed": 156,
  "jobs_failed": 3,
  "jobs_retried": 7,
  "current_job_id": null,
  "uptime_seconds": 3600.5
}
```

### `GET /dead-letter` — List dead letter queue

### `POST /dead-letter/{job_id}/retry` — Retry from dead letter

## Reliability Features

| Feature | Implementation |
|---------|---------------|
| **Idempotency** | `Idempotency-Key` header/body maps to job ID; duplicate requests return same job |
| **Retries** | Exponential backoff (1s, 2s, 4s + jitter) up to `MAX_RETRIES` (default 3) |
| **Backoff** | Worker waits before re-claiming failed jobs |
| **Dead Letter** | After max retries, job moves to DLQ with full context |
| **Alerting** | Dead letters logged to `alerts:dead_letter` Redis list; webhook configurable |
| **Priority** | Sorted set queue processes HIGH (100) → NORMAL (50) → LOW (0) first |
| **Ownership** | Workers claim jobs atomically; only owner can complete/fail/release |
| **Stuck Jobs** | `MAX_JOB_AGE_SECONDS` detects abandoned processing jobs (monitoring) |

## Running Tests

```bash
# Requires Redis on localhost:6379/1
python -m pytest tests/ -v
```

Tests cover:
- Job creation, idempotency, priority ordering
- Claim/complete/fail/release lifecycle
- Retry logic and dead-letter transition
- DLQ retry
- Health check and stats
- API endpoint validation (400 on bad input)

## Configuration

All settings via `.env` (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `JOB_TTL_SECONDS` | `86400` | Job data TTL (24h) |
| `MAX_RETRIES` | `3` | Max retry attempts before DLQ |
| `RETRY_BACKOFF_BASE` | `1.0` | Base seconds for exponential backoff |
| `LLM_BASE_URL` | `http://localhost:11434/v1` | Ollama/OpenAI-compatible endpoint |
| `LLM_MODEL` | `gemma3:1b` | Model name |
| `LLM_ENABLED` | `true` | Set `false` for deterministic fallback |
| `LLM_STUB` | `0` | Set `1` for instant stub response (testing) |
| `ALERT_WEBHOOK_URL` | (empty) | Optional webhook for DLQ alerts |

## Local Development with Ollama

```bash
# Terminal 1: Ollama (if not running)
ollama serve

# Terminal 2: Pull model (one-time)
ollama pull gemma3:1b

# Terminal 3: Redis
docker run -d -p 6379:6379 redis:7-alpine

# Terminal 4: API
uvicorn app.main:app --port 8006 --reload

# Terminal 5: Worker
python worker/main.py
```

## Example Usage

```bash
# Submit job
curl -X POST http://localhost:8006/enrich \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: book-123' \
  -d '{"input":{"title":"The Power of Habit","description":"Why we do what we do","price_gbp":12.99}}'

# Response: {"job_id":"...","status":"pending",...}

# Poll for result
curl http://localhost:8006/jobs/<job_id>

# When completed:
# {"job_id":"...","status":"completed","output":{"category":"nonfiction","summary":"...","confidence":0.85,"quality_flags":[]},...}
```

## Files

```
be-06-background-job/
├── app/
│   ├── main.py          # FastAPI endpoints
│   ├── config.py        # Pydantic settings
│   ├── schemas.py       # Pydantic models
│   └── queue.py         # Redis job queue implementation
├── worker/
│   └── main.py          # Background worker process
├── tests/
│   └── test_queue.py    # Comprehensive test suite
├── logs/                # Quarantine, cost, alerts (created at runtime)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## AI vs Me (Bonus Stage)

I wrote a specification from memory and asked an LLM to build the same background job system. The AI version:

1. **Used in-memory queue** — no Redis, no persistence, no multi-worker support. My version uses Redis with atomic Lua scripts for claiming.
2. **No idempotency** — duplicate requests created duplicate jobs. My version has header/body idempotency keys with Redis mapping.
3. **No dead-letter queue** — failures just logged and lost. My version has DLQ with full context and retry endpoint.
4. **No priority queue** — FIFO only. My version uses sorted set with priority scores.
5. **No ownership model** — any worker could complete any job. My version uses atomic claim with worker ID verification.
6. **Silent deviations** — AI added a "webhook" field I never specified but didn't implement the callback. My version has the field and a stub for future implementation.

**What the AI did better:** It produced a clean FastAPI structure and correct Pydantic models in one shot. I kept that structure and hardened the queue logic.

**What my spec forgot:** The exact Lua script for atomic claim/release, the DLQ data format, and that workers need a unique ID for ownership. Small gaps, but each one let the AI choose for me.

Full spec would be in `ai-version/SPEC.md` (not included — this is the human-built version).

---

**Built with Claude; I verified the queue logic, Lua scripts, retry/DLQ flow, and all tests myself.**