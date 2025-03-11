from fastapi import APIRouter

from app.api.routes import spreadsheets, home

api_router = APIRouter()
api_router.include_router(home.router, tags=["home"])
api_router.include_router(spreadsheets.router, tags=["spreadsheets"])
