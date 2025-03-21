from fastapi import APIRouter
from app.core.db import redis_client, appwrite_db, DATABASE_ID
from app.adapters.redis import RedisAdapter
# from app.adapters.appwrite import AppwriteAdapter
from app.adapters.duckdb import DuckDBAdapter
from app.services.sheets import SheetServices
from app.api.routes import spreadsheets, home

# db_adapter = AppwriteAdapter(appwrite_db, DATABASE_ID)
db_adapter = RedisAdapter(redis_client)
lock_adapter = RedisAdapter(redis_client)
in_memory_adapter = DuckDBAdapter()
sheet_service = SheetServices(db_adapter, lock_adapter, in_memory_adapter)

api_router = APIRouter()
api_router.include_router(home.router)
api_router.include_router(spreadsheets.router, tags=["spreadsheets"])