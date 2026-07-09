# BE-04: Containerize your stack

## Goal Achieved
This project implements a fully containerized stack running a Python FastAPI application, Postgres, and Redis. It successfully swaps the A2 in-memory repository for a real Postgres repository without modifying the service layer or routing logic.

## Requirements Checklist
- [x] **Postgres runs in Docker with a volume**: Defined in `docker-compose.yml` using the `pgdata` volume. Start the stack with `docker compose up --build`.
- [x] **Connection string from `.env`**: `.env` is properly ignored in `.gitignore`, and a `.env.example` is committed.
- [x] **Architecture Proven**: The `UserRepository` interface is now implemented by `PostgresUserRepository`. The `main.py` simply comments out `InMemoryUserRepository` and swaps it for Postgres. **The service and routes remain 100% unchanged.**
- [x] **Persistence Proven**: 
  - *How I checked*: 
    1. Ran `docker compose up -d`
    2. Hit `POST http://localhost:8000/users` with a new user payload.
    3. Hit `GET http://localhost:8000/users` to see the new row.
    4. Ran `docker compose down` (which stops and removes the containers).
    5. Ran `docker compose up -d` again.
    6. Hit `GET http://localhost:8000/users` again—the row was perfectly preserved thanks to the mounted Docker volume.

## Stretch Goals (Included)
- **Redis Integration**: Redis is added to `docker-compose.yml`. I've added a `/ping-redis` route to `main.py` that successfully connects to Redis and pings it.
- **EXPLAIN ANALYZE**: Added an index `idx_users_email` in `init.sql`. 
  - *Before Index:* `Seq Scan on users (cost=0.00..15.50 rows=1 width=520) (actual time=0.015..0.016 rows=1 loops=1) Filter: ((email)::text = 'ahmed@example.com'::text)`
  - *After Index:* `Index Scan using idx_users_email on users (cost=0.15..8.17 rows=1 width=520) (actual time=0.008..0.009 rows=1 loops=1) Index Cond: ((email)::text = 'ahmed@example.com'::text)`
  - The index scan cut the execution time down by nearly 50% on exact lookups.
