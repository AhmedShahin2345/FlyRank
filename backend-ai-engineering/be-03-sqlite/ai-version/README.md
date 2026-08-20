# AI rematch — the prompt I wrote

I asked an AI assistant to migrate my in-memory CRUD task API to SQLite, without
copying from the assignment sheet. This is the exact prompt I used:

---

> I have a simple FastAPI CRUD API for tasks that currently keeps tasks in a
> Python list. Move it to SQLite.
>
> - Use Python + FastAPI + the built-in `sqlite3` module.
> - Create a SQLite database file called `tasks.db` next to the code.
> - Create a table called `tasks` if it doesn't already exist, with columns:
>   `id` (integer primary key), `title` (text), `done` (integer 0/1).
> - Seed three example tasks when the app starts.
> - Endpoints must behave identically to before:
>   - `GET /tasks` — list all tasks
>   - `GET /tasks/{id}` — one task, 404 if unknown
>   - `POST /tasks` — create a task, 201, missing or empty title returns 400
>   - `PUT /tasks/{id}` — update title and done, 404 if unknown, 400 if invalid
>   - `DELETE /tasks/{id}` — delete a task, 204 on success, 404 if unknown
> - Use parameterized queries (`?` placeholders) for safety.
> - Keep everything in one file so it's easy to review.
> - Return tasks as JSON with `id`, `title`, and `done` (boolean).

---

The AI's answer is in [`ai-version/`](ai-version/), generated in quarantine. My
hand-built version (Stages 0–5) is untouched in the parent folder.

## Running the AI version

```bash
cd ai-version
pip install fastapi uvicorn
uvicorn main:app --port 8001
```

## What I tested

- Does it start on the first try and create its `tasks.db`? **Yes** — it boots
  and the file appears automatically.
- Does its seed run only once, or do examples multiply on restart?
  **They multiply.** Every startup inserts the three examples again.
- Does data survive a restart? **Partially** — rows you add do survive, but the
  seed duplicates make the list grow on every boot.
- Status codes: DELETE returns `200` instead of `204`, and an empty title gives
  FastAPI's default `422` instead of the required `400`.

## Diff vs my hand-built version

`git diff --no-index ai-version/main.py ../app/main.py` — the concrete
differences are listed in the README's **"AI vs me"** section.

## Rematch

After the review I improved my prompt (added: "seed only when the table is
empty", "return 204 with an empty body on delete", "return 400 JSON for missing
or empty title", "every query must use ? placeholders") and regenerated. The
second version fixed the seed duplication and the 204, but still returned 422
for an empty title unless I specified the exact validation behaviour.