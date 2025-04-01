import string
from app.adapters.redis import RedisAdapter
# from app.adapters.appwrite import AppwriteAdapter
from app.adapters.duckdb import DuckDBAdapter
from app.models.models import Spreadsheet, Sheet, SheetProperties, SheetData
from app.models.cell_lock import CellLock
from typing import Tuple

import secrets
import string
from datetime import datetime, timezone

class SheetServices:
  def __init__(self, db_adapter: RedisAdapter, lock_adapter: RedisAdapter, in_memory_adapter: DuckDBAdapter):
    self.db_adapter = db_adapter
    self.lock_adapter = lock_adapter
    self.in_memory_adapter = in_memory_adapter

  async def createSpreadsheet(self, user_id: str) -> Tuple[Spreadsheet, Sheet]:
    alp = string.ascii_letters + string.digits + "-_" # Generate a 44-character Google Sheets-like ID
    spreadsheet_id = "".join(secrets.choice(alp) for _ in range(44))

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

    # await self.in_memory_adapter.save_spreadsheet(spreadsheet)
    # await self.in_memory_adapter.save_sheet(first_sheet)
    await self.db_adapter.save_spreadsheet(spreadsheet)
    # await self.db_adapter.save_sheet(first_sheet)

    return (spreadsheet, first_sheet)
  

  async def getSpreadsheet(self, spreadsheet_id: str, gid: int) -> Tuple[Spreadsheet, Sheet] | None:
    return await self.db_adapter.get_spreadsheet(spreadsheet_id, gid)
  
  

  async def lockCell(self, lock: CellLock):
    await self.lock_adapter.lock_cell(lock)

  async def getCellLock(self, sheet_id: str, cell_id: str) -> CellLock | None:
    return await self.lock_adapter.get_cell_lock(sheet_id, cell_id)

  

  
