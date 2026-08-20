from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str = ""
    password: str = ""


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(body: AuthRequest):
    if not body.email or not body.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )
    try:
        res = supabase.auth.sign_up(
            {"email": body.email, "password": body.password}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create account",
        )
    if res.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create account",
        )
    return {"user": res.user}


@router.post("/login")
def login(body: AuthRequest):
    if not body.email or not body.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )
    session = res.session
    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "token_type": "bearer",
    }