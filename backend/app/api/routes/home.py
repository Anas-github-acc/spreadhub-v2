from fastapi import APIRouter

from app.core.db import redis_client

router = APIRouter()


@router.get("/home")
async def home():
    redis_client.set("health", "fine")
    res = redis_client.get("health")
    return {"health": res}
