import asyncio
import inspect
from typing import List, Dict
from app.core.db import redis_client
from redis.asyncio import Redis

async def export_redis(redis: Redis) -> List[Dict]:
  keys = await redis.keys('spreadsheet:*')
  data = []
  for key in keys:
    if inspect.isawaitable(rset := redis.hgetall(key)):
            item = await rset
    decoded = {k.decode("utf-8"): v.decode('utf-8') for k, v in item.items()}
    data.append({
        "spreadsheet_id": decoded["spreadsheet_id"],
        "owner_id": decoded["owner_id"],  # UUID string
        "title": decoded["title"],
        "locale": decoded["locale"],
        "time_zone": decoded["time_zone"],
        "auto_recalc": decoded["auto_recalc"],
        "default_format": eval(decoded["default_format"]),  # Adjust if JSON
        "created_at": decoded["created_at"],
        "updated_at": decoded["updated_at"],
        "is_public": decoded["is_public"] == "true",
    })

  return data


if __name__=="__main__":
    data = asyncio.run(export_redis(redis_client))
    import json
    with open('data.json', "w") as f:
        json.dump(data, f)
