# FlyRank API

A simple HTTP server with two JSON endpoints.

## Setup

1. Run the server:
   ```bash
   python3 server.py
   ```
2. The server will start on port 3000.

## Endpoints

- `GET /hello` - Returns a hello message
- `GET /time` - Returns the current UTC time

## Week 3 · Assignment A2 — Connecting CRUD to the database

The full CRUD task API backed by SQLite lives in [`be-03-sqlite/`](be-03-sqlite/).
Same five endpoints as Assignment 1, but data is stored in `tasks.db` and
survives restarts. See [its README](be-03-sqlite/README.md) for setup, the
why-SQLite explanation, example SQL, and the DB Browser screenshot.

## Week 4 · Assignment BE-03 — Auth: login & protect

The FastAPI + Supabase auth API lives in [`be-03-auth/`](be-03-auth/).
Signup, login, logout, and bearer-protected routes backed by Supabase Auth.
See [its README](be-03-auth/README.md) for the route table, curl examples,
and the AI-vs-me comparison.

## Week 5 · Assignment BE-05 — The polite scraper

The polite scraper for books.toscrape.com lives in [`be-05-scraper/`](be-05-scraper/).
It walks all three catalogue pages, caches every response, validates 60 book
records into `output/books.json`, and survives injected failures. See
[its README](be-05-scraper/README.md) for the checkpoints and AI-vs-me.

## Week 6 · Assignment BE-06 — Your first background job

The async enrichment API lives in [`be-06-background-job/`](be-06-background-job/).
It wraps the BE-07 pipeline in a job queue: `POST /enrich` returns `202` + `job_id`,
a Redis-backed worker pool processes jobs with retries and a dead-letter queue.
See [its README](be-06-background-job/README.md) for endpoints, docker-compose, and AI-vs-me.

## Week 7 · Assignment BE-07 — Put an LLM behind your API

The `POST /enrich` endpoint backed by Ollama `gemma3:1b` lives in [`be-07-llm/`](be-07-llm/).
Schema-validated output, retry policies, quarantine log, 6 pytest tests passing.
See [its README](be-07-llm/README.md) for the job card, eval results, and AI-vs-me.

## Week 8 · Assignment BE-08 — PDF Report Generator

The async report generator lives in [`be-08-pdf-report/`](be-08-pdf-report/).
It wraps the BE-06 job queue pattern with PostgreSQL (from BE-04) and ReportLab PDF generation.
`POST /reports` returns `202` + `job_id`, a worker pool generates PDFs, with idempotency, DLQ, and download endpoint.
See [its README](be-08-pdf-report/README.md) for endpoints, docker-compose, and AI-vs-me.

## Week 9 · Assignment BE-09 — AI Decision Flow with React Flow + Inngest

The visual AI workflow system lives in [`be-09-decision-flow/`](be-09-decision-flow/).
Next.js + React Flow frontend with Inngest workflow execution, OpenAI LLM returns YES/NO decisions.
Save/load workflows as JSON, execution logs panel, animated edges.
See [its README](be-09-decision-flow/README.md) for endpoints, docker-compose, and AI-vs-me.