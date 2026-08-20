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
