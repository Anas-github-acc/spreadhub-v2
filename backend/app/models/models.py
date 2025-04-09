from pydantic import BaseModel
from typing import Dict, Literal, Optional, Any, List

from app.api.routes import spreadsheets

class ErrorValue(BaseModel):
    type: Literal["ERROR_TYPE_UNSPECIFIED", "ERROR", "NULL_VALUE", "DIVIDE_BY_ZERO", "VALUE", "REF", "NAME", "NUM", "N_A", "LOADING"]
    message: str

class ExtendedValue(BaseModel):
    numberValue: Optional[int] = None
    stringValue: Optional[str] = None
    boolValue: Optional[bool] = None
    formulaValue: Optional[str] = None
    errorValue: Optional[ErrorValue] = None

class CellFormat(BaseModel):
    numberFormat: Dict[str, Any]
    backgroundColor: Dict[str, float]
    backgroundColorStyle: Dict[str, Any]
    borders: Dict[str, Any]
    padding: Dict[str, Any]
    horizontalAlignment: Literal["LEFT", "CENTER", "RIGHT"]
    verticalAlignment: Literal["TOP", "MIDDLE", "BOTTOM"]
    wrapStrategy: Literal["OVERFLOW_CELL", "LEGACY_WRAP", "CLIP", "WRAP"]
    textDirection: Literal["LEFT_TO_RIGHT", "RIGHT_TO_LEFT"]
    textFormat: Dict[str, Any]
    hyperlinkDisplayType: Literal["LINKED", "PLAIN_TEXT"]
    textRotation: Dict[str, Any]

class CellData(BaseModel):
    userEnteredValue: Optional[ExtendedValue] = None
    effectiveValue: Optional[ExtendedValue] = None
    formattedValue: Optional[str] = None
    userEnteredFormat: Optional[CellFormat] = None
    effectiveFormat: Optional[CellFormat] = None
    hyperlink: Optional[str] = None
    note: Optional[str] = None
    textFormatRuns: Optional[List[Dict[str, Any]]] = None
    dataValidation: Optional[Dict[str, Any]] = None
    pivotTable: Optional[Dict[str, Any]] = None
    dataSourceTable: Optional[Dict[str, Any]] = None
    dataSourceFormula: Optional[Dict[str, Any]] = None

class Cell(BaseModel):
    cell_id: int
    sheet_id: str
    data: CellData
    locked: bool
    locked_by: Optional[str] = None
    locked_at: Optional[str] = None
    updated_at: str
    updated_by: str


class SheetData(BaseModel):
    startRow: int
    startColumn: int
    rowData: Dict[int, Cell]

class SheetMerges(BaseModel):
    sheet_id: int
    startRowIndex: int
    endRowIndex: int
    startColumnIndex: int
    endColumnIndex: int

class SheetProperties(BaseModel):
    sheet_id: int
    title: str
    index: int
    sheet_type: Literal["SHEET_TYPE_UNSPECIFIED", "GRID", "OBJECT", "DATA_SOURCE"] = "GRID"
    grid_properties: Dict[str, Any] = {
        "rowCount": 10000,
        "columnCount": 676,
        "frozenRowCount": 0,
        "frozenColumnCount": 0,
        "hideGridlines": False,
        "rowGroupControlAfter": False,
        "columnGroupControlAfter": False,
    }
    hidden: bool = False
    tab_color: Dict[str, Any] = {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0,
        "alpha": 1.0,
    }
    tab_color_style: Dict[str, Any] = {
        "themeColor": "ACCENT1",
        "rgbColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0,
        },
    }
    right_to_left: bool = False
    data_source_sheet_properties: Dict[str, Any] | None = None

    @property
    def theme_color(self) -> Literal["THEME_COLOR_TYPE_UNSPECIFIED", "TEXT", "BACKGROUND", "ACCENT1", "ACCENT2", "ACCENT3", "ACCENT4", "ACCENT5", "ACCENT6", "LINK"]:
        return self.tab_color_style["themeColor"]

class SheetDeveloperMetadata(BaseModel):
    metadata_id: str
    metadata: Dict[str, str] = {}

class Sheet(BaseModel):
    sheet_id: int
    spreadsheet_id: str
    properties: SheetProperties
    data: SheetData
    merges: SheetMerges | None = None
    DeveloperMetadata: SheetDeveloperMetadata | None
    updated_at: str
    updated_by: str

class SpreadsheetThemeColor(BaseModel):
    color_type: Literal["THEME_COLOR_TYPE_UNSPECIFIED", "TEXT", "BACKGROUND", "ACCENT1", "ACCENT2", "ACCENT3", "ACCENT4", "ACCENT5", "ACCENT6", "LINK"]
    rgb_color: Dict[str, float]

class SpreadsheetTheme(BaseModel):
    font_family: str
    theme_colors: Dict[str, SpreadsheetThemeColor]

class SpreadsheetProperties(BaseModel):
    title: str
    locale: str
    time_zone: str
    auto_recalc: Literal["RECALCULATION_INTERVAL_UNSPECIFIED", "ON_CHANGE", "MINUTE", "HOUR"]
    default_format: CellFormat
    spreadsheet_theme: SpreadsheetTheme # this define the theme of the spreadsheet

class Spreadsheet(BaseModel):
    spreadsheet_id: str = ''
    owner_id: str 
    sheets: Dict[int, Sheet] = {} # f"sheet:{sheet.spreadsheet_id}:{sheet.sheet_id}"
    properties: SpreadsheetProperties | str = ''
    created_at: str = ''
    updated_at: str = ''
    is_public: bool = False
    is_deleted: bool = False


class MergeNode(BaseModel):
    node_id: str 
    sheet_id: str
    cell_id: str
    parent_node_id: Optional[str] = None
    operation_type: Literal["insert", "update", "delete"]
    cell_data: Dict[str, Any]
    owner_id: str
    status: Literal["merged", "conflict", "pending"]
    created_at: str
    merged_at: Optional[str] = None
    conflict_resolved_at: Optional[str] = None

