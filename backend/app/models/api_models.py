from .models import Spreadsheet, Sheet, SheetProperties, SheetData

class reqSpreadsheetCreate:
  user_id: str

# class resSpreadsheetCreate(Spreadsheet, Sheet):
#   def to_response(self):
#     return (Spreadsheet, Sheet)