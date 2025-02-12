from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/home", response_model=str)
async def home() -> str:
    return "Hello, world!"