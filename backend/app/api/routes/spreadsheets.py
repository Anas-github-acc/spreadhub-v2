from fastapi import APIRouter, HTTPException, Response, Cookie
from typing import Awaitable, Literal, Tuple

from app.models.models import Spreadsheet, Sheet
from app.core.services import sheet_service
from app.models.api_models import reqSpreadsheetCreate


router = APIRouter()

@router.post("/spreadsheets/create")
async def create_spreadsheet(spreadsheet: reqSpreadsheetCreate):
    user_id = spreadsheet.user_id
    spreadsheet_data, first_sheet = await sheet_service.createSpreadsheet(user_id)
    return {"spreadsheet": spreadsheet_data, "sheet": first_sheet}
    
@router.get("/spreadsheets/{spreadsheet_id}/{status}", response_model=Tuple[Spreadsheet, Sheet])
async def get_spreadsheet(
    spreadsheet_id: str, 
    status: Literal["edit", "view"],
    gid: int = 0
):
    result = await sheet_service.getSpreadsheet(spreadsheet_id, gid)
    if not result:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")

    spreadsheet, sheet = result
    
    if gid not in spreadsheet.sheets:
        return Response(
            status_code=302, 
            headers={"Location": f"/spreadsheets/{spreadsheet_id}/{status}?gid=0"}
        )
    
    if status == "edit" and not spreadsheet.is_public:
        return Response(
            status_code=302, 
            headers={"Location": f"/spreadsheets/{spreadsheet_id}/view?gid={gid}"}
        )
        
    return spreadsheet, sheet
