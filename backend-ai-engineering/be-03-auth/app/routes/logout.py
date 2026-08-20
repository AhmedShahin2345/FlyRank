from fastapi import APIRouter, Depends, status

from ..deps import get_current_user
from ..supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user: dict = Depends(get_current_user)):
    supabase.auth.sign_out()
    return None