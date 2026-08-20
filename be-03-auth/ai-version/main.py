from fastapi import FastAPI, HTTPException, Header
from fastapi.security import HTTPBearer
from supabase import create_client
import os

app = FastAPI(title="AI-generated Auth API")
bearer_scheme = HTTPBearer()

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


@app.post("/auth/signup", status_code=201)
def signup(body: dict):
    res = supabase.auth.sign_up(
        {"email": body["email"], "password": body["password"]}
    )
    return {"user": res.user}


@app.post("/auth/login")
def login(body: dict):
    res = supabase.auth.sign_in_with_password(
        {"email": body["email"], "password": body["password"]}
    )
    return {
        "access_token": res.session.access_token,
        "refresh_token": res.session.refresh_token,
    }


@app.post("/auth/logout", status_code=204)
def logout(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    supabase.auth.sign_out()
    return None


@app.get("/protected/profile")
def profile(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    user = supabase.auth.get_user(token).user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": user.id, "email": user.email}


@app.get("/protected/dashboard")
def dashboard():
    return {"message": "Welcome to your dashboard!"}


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}