# Stage 4 — SQL by hand

Queries I ran directly against `tasks.db` (in DB Browser for SQLite / the `sqlite3` CLI), with what each returned.

```sql
SELECT * FROM tasks;
```
Returned all four rows at the time (the three seeds + one created via the API), one row per task with `id`, `title`, `done`.

```sql
SELECT * FROM tasks WHERE done = 1;
```
Returned no rows — no task was marked done yet, so the filter found nothing.

```sql
SELECT COUNT(*) FROM tasks;
```
Returned `4` — the number of tasks in the table at that moment.

```sql
UPDATE tasks SET done = 1;
```
Updated every row to `done = 1`; the API then showed all tasks as completed with no restart.

```sql
DELETE FROM tasks WHERE done = 1;
```
Deleted every task; `GET /tasks` immediately returned `[]` — the API and the CLI read the same file, so there is no syncing, just one source of truth.
