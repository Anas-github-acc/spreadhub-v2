from appwrite.services.databases import Databases
from app.models.models import Spreadsheet

class AppwriteAdapter:
    def __init__(self, db: Databases, database_id: str):
        self.db = db
        self.database_id = database_id

    async def save_spreadsheet(self, spreadsheet: Spreadsheet):
        data = spreadsheet.model_dump()
        data["owner_id"] = str(spreadsheet.owner_id)
        self.db.create_document(
            self.database_id,
            "spreadsheet",
            spreadsheet.Spreadsheet_id,
            data
        )

    async def get_spreadsheet(self, spreadsheet_id: str) -> Spreadsheet:
        doc = self.db.get_document(self.database_id, "spreadsheet", spreadsheet_id)
        return Spreadsheet.model_validate(doc)