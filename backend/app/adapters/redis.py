from csv import Error
import json
import inspect
from typing import Union, Dict, Any, Optional, Tuple
from redis import Redis
from app.api.routes import spreadsheets
from app.models.cell_lock import CellLock
from app.models.models import CellData, Spreadsheet, Sheet
from app.models.api_models import ErrorResponse


class RedisAdapter:
    def __init__(self, redis: Redis):
        self.redis: Redis = redis


    
    async def save_spreadsheet(self, spreadsheet: Spreadsheet) -> None:
        key: str = f"spreadsheet:{spreadsheet.spreadsheet_id}"
        # data = json.dumps(spreadsheet.model_dump())
        data: Dict[str, Any] = spreadsheet.model_dump()
        self.redis.json().set(key, '$', data)
        # self.redis.json().set(key, '$.sheets', [])


    async def save_sheet(self, sheet: Sheet):
        sheet_key: str = f"sheet:{sheet.spreadsheet_id}:{sheet.sheet_id}"
        spreadsheet_key: str = f"spreadsheet:{sheet.spreadsheet_id}"
        
        last_index_raw: Optional[list] = self.redis.json().get(spreadsheet_key, '$.sheets[-1].properties.index')
        last_index: int = last_index_raw[0] if last_index_raw and isinstance(last_index_raw, list) else 0

        sheet.properties.title = f'Sheet{last_index + 1}'
        sheet.properties.index = last_index + 1
        
        data: Dict[str, Any] = sheet.model_dump()
        # self.redis.json().set(sheet_key, '$', data)

        if(sheet.sheet_id != 0):
            return ErrorResponse(
                detail="sheet_id must not be zero",
                status_code=400,
            )

        self.redis.json().set(spreadsheet_key, f"$.sheets.{sheet.sheet_id}", data)
        return None



    async def get_spreadsheet(self, spreadsheet_id: str, gid: int) -> Union[Spreadsheet, ErrorResponse]:
        key = f"spreadsheet:{spreadsheet_id}"
        # possible error (don't forget to changes this every where)
        
        data_raw: Optional[list] = self.redis.json().mget( [
            'spreadsheet_id',
            'owner_id',
            'properties',
            'created_at',
            'updated_at',
            'is_public',
            'is_deleted'
        ], key)

        if not data_raw or not isinstance(data_raw, list) or not data_raw[0]:
            return ErrorResponse(
                detail="no spreadsheet for given id"
            )
        
        data: Dict[str, Any] = data_raw[0]
        
        sheet: Optional[list] = self.redis.json().get(f'{key}.sheets.{gid}')
        if sheet and isinstance(sheet, list) and sheet[0]:
            if "sheets" not in data:    
                data["sheets"] = {}
            data["sheets"][gid] = sheet[0]

        try:
            return Spreadsheet.model_validate(data)
        except ValueError as e:
            return ErrorResponse(
                detail="invalide Spreadsheet data",
                status_code=500,
            )
        
    
    
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
