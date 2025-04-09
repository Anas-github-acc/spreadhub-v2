import asyncio
import inspect

from redis.asyncio import Redis

from app.core.db import redis_client


async def export_redis(redis: Redis) -> list[dict]:
    keys = await redis.keys("spreadsheet:*")
    data = []
    for key in keys:
        if inspect.isawaitable(rset := redis.hgetall(key)):
            item = await rset
        decoded = {k.decode("utf-8"): v.decode("utf-8") for k, v in item.items()}
        data.append(
            {
                "spreadsheet_id": decoded["spreadsheet_id"],
                "owner_id": decoded["owner_id"],  # UUID string
                "title": decoded["title"],
                "locale": decoded["locale"],
                "time_zone": decoded["time_zone"],
                "auto_recalc": decoded["auto_recalc"],
                "default_format": json.loads(
                    decoded["default_format"]
                ),  # Adjusted to use json.loads
                "created_at": decoded["created_at"],
                "updated_at": decoded["updated_at"],
                "is_public": decoded["is_public"] == "true",
            }
        )

    return data


if __name__ == "__main__":
    data = asyncio.run(
        export_redis(
            Redis(
                host=redis_client.connection_pool.connection_kwargs["host"],
                port=redis_client.connection_pool.connection_kwargs["port"],
                password=redis_client.connection_pool.connection_kwargs["password"],
                ssl=redis_client.connection_pool.connection_kwargs["ssl"],
                db=redis_client.connection_pool.connection_kwargs["db"],
            )
        )
    )
    import json

    with open("data.json", "w") as f:
        json.dump(data, f)
