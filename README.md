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
