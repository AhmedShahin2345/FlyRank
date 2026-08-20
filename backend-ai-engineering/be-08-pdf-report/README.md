# BE-08 — PDF Report Generator

A background job system that generates PDF reports from database data. Built on the BE-06 background job pattern with PostgreSQL (from BE-04) and ReportLab for PDF generation.

## What it does

The `POST /reports` endpoint accepts a report request, returns `202 Accepted` with a `job_id`, and a background worker generates the PDF report. A status endpoint lets callers poll for the result and download the finished PDF.

This exercises the professional pattern: accept fast, work in background, store artifact, return download link. It handles the non-negotiables: jobs **will** run twice (idempotency), they **will** fail (retries with backoff), and someone must find out (dead-letter queue + alerting).

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│    Redis    │
│             │ 202 │   (API)     │     │  (Queue)    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐            │
                    │   Worker    │◀───────────┘
                    │  (ReportLab)│
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ PostgreSQL  │
                    │  (Books)    │
                    └─────────────┘
```

## Quick Start

```bash
# 1. Copy env and configure
cp .env.example .env
# Edit .env with your Redis, PostgreSQL URLs

# 2. Start services (or use docker-compose)
docker-compose up --build

# 3. API runs on port 8008
```

## Docker Compose (Recommended)

```bash
docker-compose up --build
```

This starts PostgreSQL, Redis, the API on port 8008, and 1 report worker.

## Endpoints

### `POST /reports` — Submit report generation job

Returns `202 Accepted` immediately with a `job_id`.

**Request:**
```json
{
  "input": {
    "report_type": "book_catalog",
    "title": "Q3 2026 Book Catalog",
    "filters": {
      "category": "fiction",
      "min_price": 10,
      "max_price": 50,
      "in_stock_only": true
    }
  },
  "idempotency_key": "report-q3-2026",
  "callback_url": "https://your.app/webhook"
}
```

**Response (202):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Report job accepted for processing. Poll GET /reports/{job_id} for status."
}
```

### `GET /reports/{job_id}` — Get job status/result

**Response (200):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "input": {"report_type": "book_catalog", "title": "...", "filters": {...}},
  "output": {
    "report_url": "http://localhost:8008/reports/book_catalog_20260820_143022.pdf",
    "filename": "book_catalog_20260820_143022.pdf",
    "page_count": 4,
    "file_size_bytes": 245760,
    "generated_at": "2026-08-20T14:30:22Z"
  },
  "error": null,
  "retries": 0,
  "created_at": "2026-08-20T14:30:00Z",
  "started_at": "2026-08-20T14:30:01Z",
  "completed_at": "2026-08-20T14:30:20Z",
  "idempotency_key": "report-q3-2026",
  "callback_url": null
}
```

**Status values:** `pending` → `queued` → `processing` → `completed` | `failed` | `dead_letter`

### `GET /reports/{job_id}/download` — Download the generated PDF

Returns the PDF file directly with proper headers.

### `GET /reports` — List report jobs

Query params: `limit` (default 50), `offset` (default 0), `status` (filter)

### `POST /reports/{job_id}/retry` — Retry failed/dead-letter job

### `GET /health` — Health check with queue and database metrics

```json
{
  "status": "healthy",
  "redis_connected": true,
  "database_connected": true,
  "queue_length": 3,
  "processing_count": 1,
  "dead_letter_count": 0
}
```

### `GET /stats` — Worker statistics

### `GET /dead-letter` — List dead letter queue jobs

### `POST /dead-letter/{job_id}/retry` — Retry from dead letter

## Report Types

### Book Catalog (`book_catalog`)

Generates a professional PDF catalog of books from the database with:
- Cover page with title, date, filters applied, and summary stats
- Summary section with key statistics
- Formatted table with columns: Title, Category, Price, Rating, Availability
- Page numbers and professional footer
- Alternating row colors for readability

**Filters supported:**
- `category`: Filter by book category
- `min_price` / `max_price`: Price range
- `in_stock_only`: Only show available books

## Configuration

All settings via `.env` (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/flyrank` | PostgreSQL connection |
| `JOB_TTL_SECONDS` | `86400` | Job data TTL (24h) |
| `MAX_RETRIES` | `3` | Max retry attempts before DLQ |
| `REPORT_OUTPUT_DIR` | `./output/reports` | Where PDFs are stored |
| `REPORT_BASE_URL` | `http://localhost:8008/reports` | Base URL for download links |

## Local Development

```bash
# 1. PostgreSQL (if not using docker-compose)
# Create database and run init.sql

# 2. Redis
docker run -d -p 6379:6379 redis:7-alpine

# 3. API
uvicorn app.main:app --port 8008 --reload

# 4. Worker (separate terminal)
python worker/main.py
```

## Files

```
be-08-pdf-report/
├── app/
│   ├── main.py              # FastAPI endpoints
│   ├── config.py            # Pydantic settings
│   ├── schemas.py           # Pydantic models
│   ├── queue.py             # Redis job queue
│   ├── repository.py        # PostgreSQL book queries
│   └── pdf_generator.py     # ReportLab PDF generation
├── worker/
│   └── main.py              # Background worker
├── output/
│   └── reports/             # Generated PDFs (created at runtime)
├── init.sql                 # Database schema + sample data
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## AI vs Me (Bonus Stage)

I specified the report generator and asked an LLM to build it. The AI version:

1. **Used synchronous PDF generation** — blocked the worker event loop. My version uses a proper async worker with the BE-06 queue pattern.
2. **No idempotency** — duplicate requests created duplicate PDFs. My version has idempotency keys with Redis mapping.
3. **No dead-letter queue** — failures just logged and lost. My version has DLQ with full context and retry endpoint.
4. **Hardcoded database queries** — no repository pattern. My version uses a proper `BookRepository` class with parameterized queries.
5. **No download endpoint** — couldn't retrieve the PDF. My version has `/reports/{job_id}/download` with `FileResponse`.
6. **Silent deviations** — AI added a "webhook" field I never specified but didn't implement the callback. My version has the field and a stub for future implementation.

**What the AI did better:** It produced a working ReportLab template structure in one shot. I kept that structure and hardened the queue logic.

**What my spec forgot:** The exact PDF layout details (column widths, fonts, colors), the init.sql for sample data, and that workers need a unique ID for ownership. Small gaps, but each one let the AI choose for me.

---

**Built with Claude; I verified the queue logic, PDF generation, database queries, and docker-compose myself.**