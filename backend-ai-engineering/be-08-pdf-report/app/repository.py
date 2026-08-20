import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import os


class DatabasePool:
    _pool: Optional[SimpleConnectionPool] = None
    
    @classmethod
    def initialize(cls, database_url: str, min_conn: int = 1, max_conn: int = 10):
        if cls._pool is None:
            cls._pool = SimpleConnectionPool(min_conn, max_conn, database_url)
    
    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            raise RuntimeError("Database pool not initialized. Call initialize() first.")
        return cls._pool.getconn()
    
    @classmethod
    def return_connection(cls, conn):
        if cls._pool:
            cls._pool.putconn(conn)
    
    @classmethod
    def close_all(cls):
        if cls._pool:
            cls._pool.closeall()
            cls._pool = None


@contextmanager
def get_db_connection(database_url: str):
    """Context manager for database connections."""
    DatabasePool.initialize(database_url)
    conn = DatabasePool.get_connection()
    try:
        yield conn
    finally:
        DatabasePool.return_connection(conn)


class BookRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url
        DatabasePool.initialize(database_url)
    
    def get_all_books(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get all books with optional filters."""
        with get_db_connection(self.database_url) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                where_clauses = []
                params = []
                
                if filters:
                    if filters.get("category"):
                        where_clauses.append("category = %s")
                        params.append(filters["category"])
                    if filters.get("min_price"):
                        where_clauses.append("price_gbp >= %s")
                        params.append(filters["min_price"])
                    if filters.get("max_price"):
                        where_clauses.append("price_gbp <= %s")
                        params.append(filters["max_price"])
                    if filters.get("in_stock_only"):
                        where_clauses.append("availability ILIKE '%%in stock%%'")
                
                where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                cur.execute(f"""
                    SELECT id, title, category, price_gbp, availability, rating, description, 
                           product_url, source_page, fetched_at
                    FROM books
                    {where_sql}
                    ORDER BY title
                """, params)
                
                return cur.fetchall()
    
    def get_book_count(self, filters: Dict[str, Any] = None) -> int:
        """Get total count of books with optional filters."""
        with get_db_connection(self.database_url) as conn:
            with conn.cursor() as cur:
                where_clauses = []
                params = []
                
                if filters:
                    if filters.get("category"):
                        where_clauses.append("category = %s")
                        params.append(filters["category"])
                    if filters.get("min_price"):
                        where_clauses.append("price_gbp >= %s")
                        params.append(filters["min_price"])
                    if filters.get("max_price"):
                        where_clauses.append("price_gbp <= %s")
                        params.append(filters["max_price"])
                    if filters.get("in_stock_only"):
                        where_clauses.append("availability ILIKE '%%in stock%%'")
                
                where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                cur.execute(f"SELECT COUNT(*) FROM books {where_sql}", params)
                return cur.fetchone()[0]
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        with get_db_connection(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT category FROM books ORDER BY category")
                return [row[0] for row in cur.fetchall()]
    
    def get_price_stats(self) -> Dict[str, float]:
        """Get price statistics."""
        with get_db_connection(self.database_url) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        MIN(price_gbp) as min_price,
                        MAX(price_gbp) as max_price,
                        AVG(price_gbp) as avg_price,
                        COUNT(*) as total_books
                    FROM books
                """)
                return cur.fetchone()