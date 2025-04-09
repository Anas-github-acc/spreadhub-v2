from fastapi import APIRouter

from app.api.routes import home, spreadsheets

router = APIRouter()

api_router = APIRouter()
api_router.include_router(home.router, tags=["home"])
api_router.include_router(spreadsheets.router, tags=["spreadsheets"])


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
