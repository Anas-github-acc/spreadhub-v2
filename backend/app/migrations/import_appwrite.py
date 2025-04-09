import asyncio

from appwrite.services.databases import Databases

from app.core.db import DATABASE_ID, appwrite_client


async def import_appwrite(db: Databases, data: list[dict]):
    for item in data:
        db.create_document(DATABASE_ID, "spreadsheets", item["spreadsheet_id"], item)


if __name__ == "__main__":
    import json

    with open("data.json") as f:
        data = json.load(f)
    db = Databases(appwrite_client)
    asyncio.run(import_appwrite(db, data))
