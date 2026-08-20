from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(title="FlyRank W3 CRUD API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "FlyRank W3 CRUD API is running"}
