from fastapi import APIRouter, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Literal, Union, Dict, Tuple, Optional

from app.models.models import Spreadsheet, Sheet
from app.core.services import sheet_service
from app.models.api_models import reqSpreadsheetCreate, ErrorResponse

router = APIRouter()




@router.post(
        "/spreadsheets/create",
        response_model=Spreadsheet | HTTPException,
        responses={
            200: {"model": Spreadsheet, "description": "Spreadsheet created successfully"},
            400: {"model": ErrorResponse, "description": "Invalid request"},
            500: {"model": ErrorResponse, "description": "Server error"},
        }
    )
async def create_spreadsheet(spreadsheet: reqSpreadsheetCreate) -> Spreadsheet:
    user_id = spreadsheet.user_id
    spreadsheet_data = await sheet_service.createSpreadsheet(user_id)
    return spreadsheet_data



    
@router.get(
        "/spreadsheets/{spreadsheet_id}/{status}",
        response_model=Spreadsheet,
        responses={
            200: {"model": Spreadsheet, "description": "Spreadsheet retrieved successfully"},
            302: {
                "description": "Redirect to valid gid or view mode",
                "headers": {
                    "Location": {"schema": {"type": "string"}, "description": "Redirect URL"}
                }
            },
            404: {"model": ErrorResponse, "description": "Spreadsheet not found"},
            500: {"model": ErrorResponse, "description": "Server error"}
        }
    )
async def get_spreadsheet(
    spreadsheet_id: str, 
    status: Literal["edit", "view"],
    gid: int = 0
) -> Union[Spreadsheet, RedirectResponse]:
    response: Union[Spreadsheet, ErrorResponse] = await sheet_service.getSpreadsheet(spreadsheet_id, gid)
    if isinstance(response, ErrorResponse):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.detail,
            headers=response.header
        )
    
    spreadsheet_data: Spreadsheet = response

    if gid not in spreadsheet_data.sheets:
        return RedirectResponse(
            url=f"/spreadsheets/{spreadsheet_id}/{status}?gid=0",
            status_code=302
        )
    
    if status == "edit" and not spreadsheet_data.is_public:
        return RedirectResponse(
            url=f"/spreadsheets/{spreadsheet_id}/view?gid={gid}",
            status_code=302
        )
        
    return spreadsheet_data
