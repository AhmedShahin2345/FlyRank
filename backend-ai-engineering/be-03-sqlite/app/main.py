from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    database.migrate()
    yield


app = FastAPI(title="FlyRank W3 CRUD API", lifespan=lifespan)


class TaskIn(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = False


@app.get("/")
def root():
    return {"message": "FlyRank W3 CRUD API is running"}


def row_to_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


@app.get("/tasks")
def list_tasks(
    search: Optional[str] = None,
    done: Optional[bool] = None,
    sort: Optional[str] = None,
):
    query = "SELECT * FROM tasks"
    clauses = []
    params = []
    if search:
        clauses.append("title LIKE ?")
        params.append(f"%{search}%")
    if done is not None:
        clauses.append("done = ?")
        params.append(int(done))
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    if sort == "title":
        query += " ORDER BY title COLLATE NOCASE"
    conn = database.connect()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    conn = database.connect()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done, created_at, updated_at) "
        "VALUES (?, ?, datetime('now'), datetime('now'))",
        (task.title.strip(), int(task.done)),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    return row_to_task(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskIn):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    conn = database.connect()
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, done = ?, updated_at = datetime('now') WHERE id = ?",
        (task.title.strip(), int(task.done), task_id),
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    conn.close()
    return row_to_task(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = database.connect()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return None


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = database.connect()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return row_to_task(row)


@app.get("/stats")
def stats():
    conn = database.connect()
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    conn.close()
    return {
        "total": total,
        "done": done_count,
        "pending": total - done_count,
    }