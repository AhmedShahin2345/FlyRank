from fastapi import FastAPI

from . import config
from .routes import auth, logout, protected, public
from .supabase_client import init_client

app = FastAPI(title="FlyRank Auth API", description="Auth · Login & protect", version="1.0.0")

init_client()
print(f"Server running and connected to Supabase on port {config.PORT}")

app.include_router(auth.router)
app.include_router(logout.router)
app.include_router(public.router)
app.include_router(protected.router)