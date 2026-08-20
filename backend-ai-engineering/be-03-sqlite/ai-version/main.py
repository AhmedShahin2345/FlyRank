from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI(title="AI-generated tasks API")

DB = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER)"
    )
    conn.execute("INSERT INTO tasks (title, done) VALUES ('Buy milk', 0)")
    conn.execute("INSERT INTO tasks (title, done) VALUES ('Walk the dog', 0)")
    conn.execute("INSERT INTO tasks (title, done) VALUES ('Finish the assignment', 0)")
    conn.commit()
    conn.close()


init_db()


def row_to_task(row):
    return {"id": row[0], "title": row[1], "done": bool(row[2])}


@app.get("/tasks")
def list_tasks():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [row_to_task(r) for r in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = sqlite3.connect(DB)
    row = conn.execute(f"SELECT * FROM tasks WHERE id = {task_id}").fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return row_to_task(row)


@app.post("/tasks", status_code=201)
def create_task(title: str, done: bool = False):
    conn = sqlite3.connect(DB)
    cur = conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, int(done)))
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return row_to_task(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, done: bool = False):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, int(done), task_id))
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return row_to_task(row)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"deleted": True}