from pydantic import BaseModel


class reqSpreadsheetCreate(BaseModel):
    pass

class reqSheetCreate(BaseModel):
    pass


class ErrorResponseModel(BaseModel):
    detail: str | None = None
    status_code: int = 400
    header: dict | None = None


class ErrorResponse(BaseException):
    def __init__(
        self,
        detail: str | None = None,
        status_code: int = 400,
        header: dict | None = None,
    ):
        self.detail = detail
        self.status_code = status_code
        self.header = header
        super().__init__(detail)
