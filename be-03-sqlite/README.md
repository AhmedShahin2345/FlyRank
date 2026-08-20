# FlyRank Week 3 · Assignment A2 — Connecting CRUD to the Database

This project takes the in-memory task CRUD API and moves its storage to a real
**SQLite** database. Same five endpoints, same request/response shapes — but
data now survives a server restart.

## Why SQLite?

- **Single file** — the whole database is one file, `tasks.db`. No server to
  install, no configuration, no credentials.
- **Zero setup** — SQLite is built into Python (`sqlite3` is in the standard
  library), so a clean clone runs with just a `pip install -r requirements.txt`.
- **Survives restarts** — in Assignment 1 tasks lived in a Python list and
  vanished on restart. Now they live on disk, so they're still there tomorrow.

## Where the database lives

`tasks.db` sits next to this folder and is **created automatically** the first
time the server starts. The `tasks` table is created automatically too, and
three example tasks are seeded **only when the table is empty** — restarting
never duplicates them. The file is git-ignored (`.gitignore`) so each fresh
clone starts clean and the database builds itself.

## Run it

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 3000
```

Then:

```bash
curl http://localhost:3000/tasks
```

A stranger cloning this repo and running those two commands gets a working API
with its table and three seeded tasks in under 5 minutes.

## Endpoints (identical to Assignment 1)

| Method | Path           | Success | Errors                       |
|--------|----------------|---------|------------------------------|
| GET    | /tasks         | 200     | —                            |
| GET    | /tasks/{id}    | 200     | 404 `{"error":"Task not found"}` |
| POST   | /tasks         | 201     | 400 missing/empty title      |
| PUT    | /tasks/{id}    | 200     | 400 invalid body · 404 unknown id |
| DELETE | /tasks/{id}    | 204     | 404 unknown id               |

All queries use **parameterized placeholders** (`?`) — user input is passed
separately, never glued into SQL strings.

## Example SQL query (Stage 4)

Ran by hand against `tasks.db` — the API reflected the change immediately,
with no restart:

```sql
SELECT COUNT(*) FROM tasks;
```

Returned the number of rows in the table; editing the database by hand and
seeing it through `GET /tasks` proves the API and the file share one source of
truth. More queries in [sql-queries.md](sql-queries.md).

## Database screenshot

The database open in DB Browser for SQLite, showing the seeded tasks:

![tasks.db in DB Browser](docs/tasks-db-screenshot.png)

## Extras

- Search: `GET /tasks?search=milk` — `WHERE title LIKE ?`
- Status filter: `GET /tasks?done=true` — `WHERE done = ?`
- Sorting: `GET /tasks?sort=title` — `ORDER BY title`
- Stats: `GET /stats` — `SELECT COUNT(*)`
- Timestamps: `created_at` / `updated_at` added via `ALTER TABLE`
- Index on `title` to speed up the search extra
- Seeding wrapped in a transaction (all-or-nothing)
