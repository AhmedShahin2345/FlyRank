# ⚙️ Backend AI Engineering Track · FlyRank Internship

Welcome to the **Backend AI Engineering** track of the FlyRank software engineering internship. This repository houses a production-grade suite of backend microservices, data extraction pipelines, authentication layers, background worker queues, PDF generation engines, containerized databases, and the **Backend Capstone Widget Platform**.

---

> [!IMPORTANT]
> # 🌟 Backend Engineering Capstone — Standalone Repository
> **The FlyRank Widget Platform (Backend Capstone Project) is officially hosted in its own dedicated standalone repository:**  
> 👉 **[https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)**  
> *(Click the link above to view the standalone repository, commit history, releases, and issue tracker. The complete codebase is also mirrored locally under [`be-10-capstone-widget-platform/`](be-10-capstone-widget-platform/))*

---

## 🏗️ Architecture & Progression Overview

```
[BE-01: HTTP Foundations] 
       │ (Standard library HTTP server & routing)
       ▼
[BE-03: Persistence & Auth]
  ├── be-03-sqlite ──▶ (SQLite CRUD, migrations & parameterized SQL)
  └── be-03-auth   ──▶ (FastAPI + Supabase Auth, JWT dependency guard, 11 tests)
       │
       ▼
[BE-04: Containerization]
       │ (Docker & Docker Compose multi-container Postgres + API)
       ▼
[BE-05: Data Engineering]
       │ (Polite web scraper, disk cache, schema normalizer, 7 tests)
       ▼
[BE-06: Asynchronous Jobs]
       │ (Async POST /enrich → 202 + job_id, Redis queue, worker pool, DLQ, 12 tests)
       ▼
[BE-07: LLM System Integration]
       │ (FastAPI POST /enrich, Ollama gemma3:1b, retry policy, quarantine log, 6 tests)
       ▼
[BE-08: Document Generation]
       │ (Async POST /reports → 202, ReportLab PDF generator, worker pool, download endpoint)
       ▼
[BE-09: Visual Decision Workflows]
       │ (Next.js + React Flow + Inngest visual workflow editor & OpenAI decision graph)
       ▼
[BE-10: Backend Capstone Platform]
       └─▶ (Multi-tenant lead-capture platform, FastAPI, Postgres, Redis/RQ, Playwright tests)
```

---

## 📦 Complete Module Directory

| Module | Directory | Core Technologies | Description & Highlights |
|---|---|---|---|
| **BE-01** | [`be-01-simple-server/`](be-01-simple-server/) | Python 3 `http.server` | Foundational HTTP server with `/hello` and `/time` endpoints. |
| **BE-03 Auth** | [`be-03-auth/`](be-03-auth/) | FastAPI, Supabase Auth, Pytest | Signup, login, logout, bearer token dependency, **11/11 tests pass**. |
| **BE-03 SQLite** | [`be-03-sqlite/`](be-03-sqlite/) | Python, SQLite3 | Persistent task CRUD API, SQL migrations, index design. |
| **BE-04** | [`be-04-containerize/`](be-04-containerize/) | Docker, Compose, PostgreSQL | Multi-container architecture, health checks, SQL init scripts. |
| **BE-05 Scraper** | [`be-05-scraper/`](be-05-scraper/) | Requests, BeautifulSoup4, Pydantic | Polite rate limiting (500ms), SHA-256 disk cache, 60 normalized books, **7/7 tests pass**. |
| **BE-06 Worker** | [`be-06-background-job/`](be-06-background-job/) | FastAPI, Redis, Worker Pool | Async `POST /enrich` → `202` + `job_id`, idempotency, exponential backoff, DLQ, **12 tests pass**. |
| **BE-07 LLM** | [`be-07-llm/`](be-07-llm/) | FastAPI, Ollama (`gemma3:1b`), Pydantic | `POST /enrich`, exponential backoff retries, schema repairs, quarantine log, **6/6 tests pass**. |
| **BE-08 PDF** | [`be-08-pdf-report/`](be-08-pdf-report/) | FastAPI, PostgreSQL, ReportLab | Async report jobs, PDF compilation worker, secure artifact download endpoint. |
| **BE-09 Flow** | [`be-09-decision-flow/`](be-09-decision-flow/) | Next.js, React Flow, Inngest | Interactive node graph visual editor, LLM decision evaluator, execution history. |
| **BE-10 Capstone** | [`be-10-capstone-widget-platform/`](be-10-capstone-widget-platform/) | FastAPI, PostgreSQL, Redis/RQ, Playwright | 🌟 **[Standalone Repo](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)** · Tenant-isolated widget lead capture platform. |

---

## 🧪 Running Automated Test Suites

```bash
# 1. BE-03 Auth API Test Suite (11 tests)
cd backend-ai-engineering/be-03-auth && .venv/bin/pytest tests

# 2. BE-05 Polite Scraper Test Suite (7 tests)
cd ../be-05-scraper && .venv/bin/pytest tests

# 3. BE-07 LLM Pipeline Test Suite (6 tests)
cd ../be-07-llm && .venv/bin/python tests/test_pipeline.py
```

---

## 💡 Key Engineering Principles

1. **Defensive Dependency Injection**:
   In `be-03-auth`, we utilized an active proxy wrapper (`_SupabaseProxy`) for the Supabase client to prevent uninitialized module-level import errors.

2. **Asynchronous Decoupling**:
   In `be-06-background-job`, `be-08-pdf-report`, and `be-10-capstone-widget-platform`, heavy compute and I/O tasks immediately return `202 Accepted` with a UUID `job_id`, delegating processing to resilient worker pools with Dead Letter Queues (DLQ).

3. **Strict Schema Validation & Quarantine**:
   In `be-07-llm`, raw model completions are strictly parsed into Pydantic models. Malformed JSON triggers an automated one-shot repair prompt; unrecoverable responses are quarantined to `logs/quarantine.jsonl`.
