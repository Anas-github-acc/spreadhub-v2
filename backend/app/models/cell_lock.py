from pydantic import BaseModel


class CellLock(BaseModel):
    cell_id: str
    sheet_id: str
    user_id: str
    locked_at: str
    expires_at: str
