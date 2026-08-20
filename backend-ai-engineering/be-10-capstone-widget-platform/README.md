> [!IMPORTANT]
> # 🌟 Backend Engineering Capstone — Standalone Repository
> **The FlyRank Widget Platform (Backend Capstone Project) is officially hosted in its own dedicated standalone repository:**  
> 👉 **[https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)**  
> *(Click the link above to view the standalone repository, commit history, releases, and issue tracker)*

# FlyRank Widget Platform (Backend Capstone)

A small, tenant-isolated lead-capture platform. An owner creates a widget, copies one script tag, and receives validated submissions from an approved external origin.

## Architecture

```text
Owner -> authenticated API -> PostgreSQL
Customer page -> widget.v1.js -> public config (short cache)
Visitor -> public submission API -> validation/rate limit -> PostgreSQL -> Redis/RQ worker
                                                              -> geo fallback -> notification
```

The bundle is versioned and immutable; widget config has a five-minute cache. Public endpoints verify the `Origin` against the widget's allowlist and respond to preflight requests.

The short [Phase 1 design](DESIGN.md) records the model, API boundary, layering, and explicit non-goal behind this implementation.

## Run locally

```sh
docker compose up --build --wait
docker compose --profile seed run --rm --no-deps demo-seed
```

The API is at `http://localhost:8000`; the separate-origin demo site is at `http://localhost:8081`. Compose loads safe defaults from `.env.example`; copy it to `.env` only when you need local overrides. The seed command runs inside the Compose network, so it can reach PostgreSQL using the same `DATABASE_URL` as the API. It prints usable demo credentials, an API token, and an embed snippet, then writes the local-only widget ID into `demo-site/demo-config.js` through the mounted directory.

## Useful commands

```sh
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
.venv/bin/python -m playwright install chromium
RUN_BROWSER_TESTS=1 .venv/bin/pytest -q tests/test_widget_rendering.py
.venv/bin/ruff format . && .venv/bin/ruff check .
.venv/bin/mypy app
.venv/bin/alembic upgrade head
```

## API outline

- `POST /api/v1/tenants` -> create owner
- `POST /api/v1/auth/tokens` -> issue bearer token
- `POST /api/v1/widgets` -> provision widget key, secrets, allowed origins
- `GET /api/v1/widgets/by-key/{public_key}` -> public cached config
- `POST /api/v1/submissions` -> public ingest, CORS check, enqueue job
- `GET /api/v1/widgets/{widget_id}/submissions` -> owner submission view
