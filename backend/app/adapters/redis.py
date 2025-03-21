import inspect
from redis.asyncio import Redis
from app.api.routes import spreadsheets
from app.models.cell_lock import CellLock
from app.models.models import CellData, Spreadsheet, Sheet
from typing import Tuple
import json

class RedisAdapter:
    def __init__(self, redis: Redis):
        self.redis = redis

    # spreadsheets methods
    async def save_spreadsheet(self, spreadsheet: Spreadsheet):
        key = f"spreadsheet:{spreadsheet.spreadsheet_id}"
        data = spreadsheet.model_dump()
        self.redis.hset(key, mapping=data)


    async def get_spreadsheet(self, spreadsheet_id: str, gid: int) -> Tuple[Spreadsheet, Sheet] | None:
        key = f"spreadsheet:{spreadsheet_id}"
        # possible error (don't forget to changes this every where)
        if inspect.isawaitable(rset := self.redis.hgetall(key)):
            data = await rset
        if not data:
            return None
        sheet_key = f"sheet:{spreadsheet_id}:{gid}"
        if inspect.isawaitable(rset := self.redis.hgetall(sheet_key)):
            sheet_data = await rset
        if not sheet_data:
            return None
        
        return (Spreadsheet(**data), Sheet(**sheet_data))
    
    # sheet methods
    async def save_sheet(self, sheet: Sheet):
        sheet_key = f"sheet:{sheet.spreadsheet_id}:{sheet.sheet_id}"
        data = sheet.model_dump()
        self.redis.hset(sheet_key, mapping=data)

        spreadsheet_key = f"spreadsheet:{sheet.spreadsheet_id}"
        if inspect.isawaitable(rset := self.redis.hget(spreadsheet_key, "sheets")):
            sheets_data = await rset
        sheets = json.loads(sheets_data.decode() if isinstance(sheets_data, bytes) else sheets_data) if sheets_data else {}
        sheets[sheet.sheet_id] = sheet_key
    
    
    # lock cell methods
    async def lock_cell(self, lock: CellLock):
        key = f"lock:{lock.sheet_id}:{lock.cell_id}"
        mapping = {
            "cell_id": lock.cell_id,
            "sheet_id": lock.sheet_id,
            "user_id": str(lock.user_id),
            "locked_at": lock.locked_at,
            "expires_at": lock.expires_at,
        }
        self.redis.hset(key, mapping=mapping)

    async def unlock_cell(self, sheet_id: str, cell_id: str):
        key = f"lock:{sheet_id}:{cell_id}"
        self.redis.delete(key)

    async def get_cell_lock(self, sheet_id: str, cell_id: str) -> CellLock | None:
        key = f"lock:{sheet_id}:{cell_id}"
        if inspect.isawaitable(rset := self.redis.hgetall(key)):
            data = await rset
            
        if not data:
            return None

        return CellLock(**data)
