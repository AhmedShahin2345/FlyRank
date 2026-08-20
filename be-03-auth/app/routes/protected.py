from fastapi import APIRouter, Depends

from ..deps import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }


@router.get("/dashboard")
def dashboard(user: dict = Depends(get_current_user)):
    return {
        "message": f"Welcome {user.email}! This is your dashboard.",
    }