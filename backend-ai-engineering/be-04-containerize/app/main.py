from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis

# Important: Swapping storage is just one line of change here!
# from app.repository import InMemoryUserRepository
from app.repository import PostgresUserRepository
from app.service import UserService

app = FastAPI()

# repository = InMemoryUserRepository()
repository = PostgresUserRepository()
service = UserService(repository)

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/users")
def get_users():
    return service.list_users()

@app.post("/users")
def create_user(user: UserCreate):
    return service.create_user(user.name, user.email)

@app.get("/ping-redis")
def ping_redis():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return {"status": "Redis URL not configured"}
    
    try:
        r = redis.Redis.from_url(redis_url)
        r.ping()
        return {"status": "Redis is alive and responding to ping!"}
    except Exception as e:
        return {"status": f"Redis ping failed: {str(e)}"}
