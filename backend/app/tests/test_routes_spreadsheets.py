import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.models import Spreadsheet, Sheet, SpreadsheetProperties, SheetProperties, SheetData
from app.models.api_models import ErrorResponse

client = TestClient(app)

@pytest.fixture
def mock_sheet_service():
    with patch('app.api.routes.spreadsheets.sheet_service') as mock:
        yield mock

@pytest.fixture
def valid_token():
    return "anas_token"

@pytest.fixture
def mock_spreadsheet():
    return Spreadsheet(
        spreadsheet_id="test123",
        owner_id="anas1234",
        properties="test_properties",
        is_public=False
    )

@pytest.fixture
def mock_sheet():
    return Sheet(
        sheet_id=0,
        spreadsheet_id="test123",
        properties=SheetProperties(
            sheet_id=0,
            title="Sheet1",
            index=0,
            sheet_type="GRID"
        ),
        data=SheetData(
            startRow=0,
            startColumn=0,
            rowData={}
        ),
        DeveloperMetadata=None,
        updated_at="2024-01-01",
        updated_by="anas1234"
    )

class TestSpreadsheetRoutes:
    def test_verify_token_valid(self):
        result = client.get(
            "/api/v1/spreadsheets/test123/edit",
            headers={"Authorization": f"Bearer anas_token"}
        )
        assert result.status_code == 200

    def test_verify_token_invalid(self):
        result = client.get(
            "/api/v1/spreadsheets/test123/edit",
            headers={"Authorization": f"Bearer invalid_token"}
        )
        assert result.status_code == 401

    async def test_create_spreadsheet_success(self, mock_sheet_service, mock_spreadsheet):
        mock_sheet_service.createSpreadsheet = AsyncMock(return_value=mock_spreadsheet)
        
        response = client.post(
            "/api/v1/spreadsheets/create",
            json={"user_id": "anas1234"}
        )
        
        assert response.status_code == 200
        assert response.json()["spreadsheet_id"] == "test123"
        assert response.json()["owner_id"] == "anas1234"

    async def test_create_spreadsheet_error(self, mock_sheet_service):
        error = ErrorResponse(detail="Test error", status_code=400)
        mock_sheet_service.createSpreadsheet = AsyncMock(side_effect=error)
        
        response = client.post(
            "/api/v1/spreadsheets/create",
            json={"user_id": "anas1234"}
        )
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Test error"

    async def test_create_sheet_success(self, mock_sheet_service, mock_sheet):
        mock_sheet_service.createSheet = AsyncMock(return_value=mock_sheet)
        
        response = client.post(
            "/api/v1/spreadsheets/test123/createSheet",
            json={"user_id": "anas1234"}
        )
        
        assert response.status_code == 200
        assert response.json()["sheet_id"] == 0
        assert response.json()["spreadsheet_id"] == "test123"

    async def test_get_spreadsheet_success(self, mock_sheet_service, mock_spreadsheet, valid_token):
        mock_sheet_service.getSpreadsheet = AsyncMock(return_value=mock_spreadsheet)
        
        response = client.get(
            "/api/v1/spreadsheets/test123/view?gid=0",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["spreadsheet_id"] == "test123"

    async def test_get_spreadsheet_redirect_invalid_gid(self, mock_sheet_service, mock_spreadsheet, valid_token):
        mock_sheet_service.getSpreadsheet = AsyncMock(return_value=mock_spreadsheet)
        
        response = client.get(
            "/api/v1/spreadsheets/test123/view?gid=999",
            headers={"Authorization": f"Bearer {valid_token}"},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        assert response.headers["location"] == "/spreadsheets/test123/view?gid=0"

    async def test_get_spreadsheet_redirect_unauthorized_edit(self, mock_sheet_service, mock_spreadsheet, valid_token):
        mock_spreadsheet.owner_id = "different_user"
        mock_sheet_service.getSpreadsheet = AsyncMock(return_value=mock_spreadsheet)
        
        response = client.get(
            "/api/v1/spreadsheets/test123/edit?gid=0",
            headers={"Authorization": f"Bearer {valid_token}"},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        assert response.headers["location"] == "/spreadsheets/test123/view?gid=0"


