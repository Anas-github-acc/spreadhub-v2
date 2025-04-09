from .models import Spreadsheet, Sheet, SheetProperties, SheetData
from pydantic import BaseModel

class reqSpreadsheetCreate(BaseModel):
  user_id: str

# class resSpreadsheetCreate(Spreadsheet, Sheet):
#   def to_response(self):
#     return (Spreadsheet, Sheet)

class ErrorResponse(BaseModel):
  status_code: int = 200
  detail: str | None = None
  header: dict | None = None