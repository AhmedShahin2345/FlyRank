import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "tasks.db"

SEED_TASKS = [
    ("Buy milk", 0),
    ("Walk the dog", 0),
    ("Finish the W3 assignment", 0),
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
        )
        """
    )
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        with conn:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                SEED_TASKS,
            )
    conn.close()


def migrate():
    conn = connect()
    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(tasks)").fetchall()
    ]
    if "created_at" not in columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT")
        conn.execute("ALTER TABLE tasks ADD COLUMN updated_at TEXT")
        conn.execute(
            "UPDATE tasks SET created_at = datetime('now'), updated_at = datetime('now')"
        )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title)")
    conn.commit()
    conn.close()
