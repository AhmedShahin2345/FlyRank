# 🚀 FlyRank Backend Engineering Internship

> **Comprehensive Backend Engineering Portfolio & Deliverables**  
> **Author**: [Ahmed Shahin](https://ahmedshahin2345.github.io/)  
> **Live Portfolio**: [ahmedshahin2345.github.io](https://ahmedshahin2345.github.io/)  
> **Main Repository**: [github.com/AhmedShahin2345/FlyRank](https://github.com/AhmedShahin2345/FlyRank)  
> **Backend Capstone Repository**: [github.com/AhmedShahin2345/flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)  
> **Resume**: [`CV_Ahmed_Shahin.pdf`](CV_Ahmed_Shahin.pdf)

---

> [!IMPORTANT]
> # 🌟 Backend Engineering Capstone — Standalone Repository
> **The FlyRank Widget Platform (Backend Capstone Project) is officially hosted in its own dedicated standalone repository:**  
> 🔗 **[https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)**  
> *(Click the link above to explore the complete standalone repository, CI/CD pipeline, and commit history. The complete codebase is also mirrored locally under [`backend-ai-engineering/be-10-capstone-widget-platform/`](backend-ai-engineering/be-10-capstone-widget-platform/))*

---

## 📌 Repository Overview

This repository contains all technical deliverables, production services, automation workflows, and milestone projects completed during the 8-week FlyRank Software Engineering Internship.

The codebase is organized into **two primary engineering tracks**:

```
FlyRank/
├── backend-ai-engineering/   # ⚙️ Track 1: Production microservices, auth, queues, scrapers, PDF, decision flow & Capstone
│   ├── be-01-simple-server/  # Native Python HTTP microservice
│   ├── be-03-auth/           # FastAPI + Supabase Auth with JWT bearer dependency (11 tests pass)
│   ├── be-03-sqlite/         # SQLite3 task CRUD API with schema migrations & parameterized SQL
│   ├── be-04-containerize/   # Multi-container Docker & Docker Compose setup with PostgreSQL
│   ├── be-05-scraper/        # Polite web scraper with disk cache & schema normalizer (7 tests pass)
│   ├── be-06-background-job/ # Async Redis queue worker pool with idempotency & DLQ (12 tests pass)
│   ├── be-07-llm/            # FastAPI LLM enrichment pipeline backed by Ollama gemma3:1b (6 tests pass)
│   ├── be-08-pdf-report/     # Async PostgreSQL + ReportLab PDF generation worker & download endpoint
│   ├── be-09-decision-flow/  # Next.js + React Flow + Inngest interactive visual AI decision editor
│   ├── be-10-capstone-widget-platform/ # 🌟 Complete Backend Capstone Platform codebase
│   └── README.md             # Backend AI Engineering track index & test instructions
│
├── ai-fluency/                # 🧠 Track 2: AI systems, prompt ladders, n8n agents, MCP & capstone docs
│   ├── identity/             # Design kit, monogram SVG, and typography tokens
│   ├── fl-04/                # n8n industry brief workflow + 5 verified run outputs
│   ├── mcp-setup/            # Model Context Protocol filesystem server configs
│   ├── fl-09-docs-demo/      # System documentation + YouTube video demo
│   ├── fl-10-capstone/       # Capstone package, retrospective, hours log & build-in-public post
│   ├── evidence/             # Screenshots, canvas captures, and 2-min unedited demo video
│   ├── fl-07-agent-workflow.json # Autonomous Brief Scout agent with cron scheduler & Slack dispatch
│   └── README.md             # AI Fluency track index & curriculum
│
├── CV_Ahmed_Shahin.pdf       # Updated CV with live portfolio link
├── DELIVERABLES.md           # Comprehensive 8-week portal submission card mapping
└── README.md                 # Root portfolio overview
```

---

## ⚙️ Track 1: Backend AI Engineering

The **[Backend AI Engineering Track](backend-ai-engineering/)** encompasses production backend patterns from HTTP fundamentals to asynchronous queues, PDF compilers, interactive decision flow engines, and the **Backend Capstone Widget Platform**:

| Module | Description | Technologies | Test Status |
|---|---|---|---|
| **[BE-01](backend-ai-engineering/be-01-simple-server/)** | Simple HTTP Server | Python `http.server` | Foundational routing |
| **[BE-03 Auth](backend-ai-engineering/be-03-auth/)** | Auth API & JWT Guard | FastAPI, Supabase Auth, Pytest | **11/11 Passed** |
| **[BE-03 SQLite](backend-ai-engineering/be-03-sqlite/)** | Task CRUD API | SQLite3, Parameterized SQL | Verified Persistence |
| **[BE-04](backend-ai-engineering/be-04-containerize/)** | Containerization | Docker, Docker Compose, PostgreSQL | Multi-Container |
| **[BE-05](backend-ai-engineering/be-05-scraper/)** | Polite Web Scraper | BeautifulSoup4, Requests, Pydantic | **7/7 Passed** (60 books) |
| **[BE-06](backend-ai-engineering/be-06-background-job/)** | Asynchronous Job Worker | FastAPI, Redis, Worker Pool | **12/12 Passed** |
| **[BE-07](backend-ai-engineering/be-07-llm/)** | LLM API Pipeline | FastAPI, Ollama (`gemma3:1b`), Pydantic | **6/6 Passed** |
| **[BE-08](backend-ai-engineering/be-08-pdf-report/)** | PDF Report Generator | FastAPI, PostgreSQL, ReportLab | Async Document Worker |
| **[BE-09](backend-ai-engineering/be-09-decision-flow/)** | AI Decision Flow Editor | Next.js, React Flow, Inngest | Interactive Graph Editor |
| **[BE-10 Capstone](backend-ai-engineering/be-10-capstone-widget-platform/)** | Backend Capstone Platform | FastAPI, PostgreSQL, Redis/RQ, Playwright | 🌟 **[Standalone Repo](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)** · Lead Capture Platform |

👉 *Explore backend modules and setup instructions in [`backend-ai-engineering/README.md`](backend-ai-engineering/README.md).*

---

## 🧠 Track 2: AI Fluency

The **[AI Fluency Track](ai-fluency/)** progresses from fundamental AI audits and prompt ladders to autonomous agent architectures, local LLM pipelines, and capstone documentation:

- **Autonomous Brief Scout Agent (FL-07 & W6)**:
  - Webhook endpoint (`POST /webhook/brief-agent`) and recurring cron trigger (`0 9 * * 2` Every Tuesday 09:00).
  - Fetches external RSS feeds, synthesizes executive summaries via local **Ollama (`gemma3:1b`)**, writes persistent Markdown briefs to disk, and dispatches outbound alerts.
- **Model Context Protocol (FL-05 MCP)**:
  - Local filesystem MCP server configuration and verified tool executions.
- **Brand Identity & Live Portfolio (W3–W5, W7)**:
  - Design kit, custom monogram SVG, DNS/hosting architecture walkthrough, and production deployment at [ahmedshahin2345.github.io](https://ahmedshahin2345.github.io/).
- **AI Fluency Capstone Package (FL-10)**:
  - Comprehensive systems retrospective, detailed hours log, and build-in-public announcement.

👉 *Explore full AI Fluency deliverables in [`ai-fluency/README.md`](ai-fluency/README.md).*

---

## 🧪 Quick Test Execution

Run automated unit and integration test suites across backend modules:

```bash
# 1. BE-03 Auth API (FastAPI + Supabase Auth)
cd backend-ai-engineering/be-03-auth && .venv/bin/pytest tests

# 2. BE-05 Scraper (Normalization & Cache)
cd ../be-05-scraper && .venv/bin/pytest tests

# 3. BE-07 LLM Pipeline (Retry Policies & Schema Repair)
cd ../be-07-llm && .venv/bin/python tests/test_pipeline.py
```

---

## 📋 Complete Deliverables & Submission Reference

For a complete card-by-card internship portal submission guide with exact links and attachment mapping across all 8 weeks, refer to **[`DELIVERABLES.md`](DELIVERABLES.md)**.
