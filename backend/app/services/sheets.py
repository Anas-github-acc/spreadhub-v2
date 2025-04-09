from app.adapters.redis import RedisAdapter
# from app.adapters.appwrite import AppwriteAdapter
from app.adapters.duckdb import DuckDBAdapter
from app.models.models import Spreadsheet, Sheet, SheetProperties, SheetData
from app.models.api_models import ErrorResponse
from app.models.cell_lock import CellLock
from typing import Tuple, Union

from datetime import datetime, timezone
import random
import base64
import os

class SheetServices:
  def __init__(self, db_adapter: RedisAdapter, lock_adapter: RedisAdapter, in_memory_adapter: DuckDBAdapter):
    self.db_adapter = db_adapter
    self.lock_adapter = lock_adapter
    self.in_memory_adapter = in_memory_adapter

  async def createSpreadsheet(self, user_id: str) -> Spreadsheet:
    # alp = string.ascii_letters + string.digits + "-_"
    # spreadsheet_id = "".join(secrets.choice(alp) for _ in range(44))
    random_bytes = os.urandom(32)
    spreadsheet_id = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')

    spreadsheet = Spreadsheet(owner_id=user_id)
    spreadsheet.spreadsheet_id = spreadsheet_id
    spreadsheet.created_at = datetime.now(timezone.utc).isoformat()
    spreadsheet.updated_at = datetime.now(timezone.utc).isoformat()
    spreadsheet.is_public = False

    first_sheet = Sheet(
      sheet_id=0,
      spreadsheet_id=spreadsheet_id,
      properties=SheetProperties(
        sheet_id=0,
        title="Sheet1",
        index=0,
        sheet_type="GRID",
      ),
      data=SheetData(
        startRow=0,
        startColumn=0,
        rowData={},
      ),
      DeveloperMetadata=None,
      updated_at=spreadsheet.updated_at,
      updated_by=spreadsheet.owner_id
    )

    spreadsheet.sheets = {0: first_sheet}

    # await self.in_memory_adapter.save_spreadsheet(spreadsheet)
    # await self.in_memory_adapter.save_sheet(first_sheet)
    await self.db_adapter.save_spreadsheet(spreadsheet)
    # await self.db_adapter.save_sheet(first_sheet)

    return spreadsheet
  
  async def createSheet(self, spreadsheet_id: str, user_id: str) -> Sheet | None :
    gid = random.randint(1, 2_147_483_647)

    sheet = Sheet(
      sheet_id=gid,
      spreadsheet_id=spreadsheet_id,
      properties=SheetProperties(
        sheet_id=gid,
        title=f"Sheet{gid}",
        index=gid,
        sheet_type="GRID",
      ),
      data=SheetData(
        startRow=0,
        startColumn=0,
        rowData={},
      ),
      DeveloperMetadata=None,
      updated_at=datetime.now(timezone.utc).isoformat(),
      updated_by=user_id
    )
    
    await self.db_adapter.save_sheet(sheet)

    return sheet
  
  

  async def getSpreadsheet(self, spreadsheet_id: str, gid: int) -> Union[Spreadsheet, ErrorResponse]:
    return await self.db_adapter.get_spreadsheet(spreadsheet_id, gid)
  
  

  async def lockCell(self, lock: CellLock):
    await self.lock_adapter.lock_cell(lock)



  async def getCellLock(self, sheet_id: str, cell_id: str) -> CellLock | None:
    return await self.lock_adapter.get_cell_lock(sheet_id, cell_id)

  

  
