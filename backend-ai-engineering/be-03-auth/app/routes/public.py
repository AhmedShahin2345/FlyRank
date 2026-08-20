from fastapi import APIRouter

router = APIRouter(tags=["public"])


@router.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}