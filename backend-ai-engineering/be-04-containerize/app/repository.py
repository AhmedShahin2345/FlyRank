from abc import ABC, abstractmethod
import psycopg2
from psycopg2.extras import RealDictCursor
import os

class UserRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add(self, name: str, email: str):
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = [
            {"id": 1, "name": "Memory User", "email": "mem@example.com"}
        ]
        self._next_id = 2

    def get_all(self):
        return self.users

    def add(self, name: str, email: str):
        user = {"id": self._next_id, "name": name, "email": email}
        self.users.append(user)
        self._next_id += 1
        return user


class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.conn_string = os.getenv("DATABASE_URL")
    
    def _get_connection(self):
        return psycopg2.connect(self.conn_string)

    def get_all(self):
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, name, email FROM users ORDER BY id ASC")
                return cur.fetchall()

    def add(self, name: str, email: str):
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email",
                    (name, email)
                )
                conn.commit()
                return cur.fetchone()
