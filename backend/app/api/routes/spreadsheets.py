from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader

from app.core.services import sheet_service
from app.models.api_models import (
    ErrorResponse,
    ErrorResponseModel,
)
from app.models.models import Sheet, Spreadsheet
from app.auth import clerkClient

router = APIRouter()


router = APIRouter()

oauth2_scheme = APIKeyHeader(name="Authorization")


def verify_token(token: str):
    # In a real application, you'd verify the token against your auth system
    # This is just a simple example
    print(f"Verifying token: {token}")
    if token != "anas_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user_id": "anas123"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return user


@router.post(
    "/spreadsheets/create",
    response_model=Spreadsheet,
    responses={
        200: {"model": Spreadsheet, "description": "Spreadsheet created successfully"},
        400: {"model": ErrorResponseModel, "description": "Invalid request"},
        500: {"model": ErrorResponseModel, "description": "Server error"},
    },
)
async def create_spreadsheet(user: dict[str, Any] = Depends(get_current_user)) -> Spreadsheet:
    try:
        user_id = user["user_id"]
        spreadsheet_data: Spreadsheet = await sheet_service.createSpreadsheet(user_id)
        return spreadsheet_data
    except ErrorResponse as e:
        raise HTTPException(
            status_code=e.status_code, detail=e.detail, headers=e.header
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/spreadsheets/{spreadsheet_id}/createSheet",
    response_model=Sheet,
    responses={
        200: {"model": Sheet, "description": "Sheet have been created successfully!"},
        400: {"model": ErrorResponseModel, "description": "Invalid request"},
        500: {"model": ErrorResponseModel, "description": "Server error"},
    },
)
async def create_sheet(spreadsheet_id: str, user: dict[str, Any] = Depends(get_current_user)) -> Sheet:
    try:
        user_id = user["user_id"]
        sheet_data: Sheet = await sheet_service.createSheet(spreadsheet_id, user_id)
        return sheet_data
    except ErrorResponse as e:
        raise HTTPException(
            status_code=e.status_code, detail=e.detail, headers=e.header
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/spreadsheets/{spreadsheet_id}/{status}",
    response_model=Spreadsheet,
    responses={
        200: {
            "model": Spreadsheet,
            "description": "Spreadsheet retrieved successfully",
        },
        302: {
            "description": "Redirect to valid gid or view mode",
            "headers": {
                "Location": {
                    "schema": {"type": "string"},
                    "description": "Redirect URL",
                }
            },
        },
        404: {"model": ErrorResponseModel, "description": "Spreadsheet not found"},
        500: {"model": ErrorResponseModel, "description": "Server error"},
    },
)
async def get_spreadsheet(
    spreadsheet_id: str,
    status: Literal["edit", "view"],
    gid: int = 0,
    user: dict[str, Any] = Depends(get_current_user),
) -> Spreadsheet | RedirectResponse:
    response: Spreadsheet | ErrorResponse = await sheet_service.getSpreadsheet(
        spreadsheet_id, gid
    )
    if isinstance(response, ErrorResponse):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.detail,
            headers=response.header,
        )

    spreadsheet_data: Spreadsheet = response

    if gid not in spreadsheet_data.sheets:
        return RedirectResponse(
            url=f"/api/v1/spreadsheets/{spreadsheet_id}/{status}?gid=0", status_code=302
        )

    if (
        status == "edit"
        and not spreadsheet_data.is_public
        and spreadsheet_data.owner_id != user["user_id"]
    ):
        return RedirectResponse(
            url=f"/api/v1/spreadsheets/{spreadsheet_id}/view?gid={gid}", status_code=302
        )

    return spreadsheet_data
