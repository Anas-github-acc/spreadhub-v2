from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/spreadsheets", response_model=str)
def spreadsheets() -> str:
    return "grid and all...!"