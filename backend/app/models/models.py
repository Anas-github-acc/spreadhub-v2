from pydantic import BaseModel
from typing import Dict, Literal, Optional, Any

class Spreadsheet(BaseModel):
    Spreadsheet_id: str
    owner_id: str
    title: str
    locale: str
    time_zone: str
    auto_recalc: Literal["ON_CHANGE", "MINUTE", "HOUR"]
    default_format: Dict[str, Any]
    created_at: str
    updated_at: str
    is_public: bool

class Sheet(BaseModel):
    sheet_id: str
    spreadsheet_id: str
    title: str
    index: int
    sheet_type: Literal["GRID", "OBJECT"]
    grid_properties: Dict[str, Any]

class Cell(BaseModel):
    cell_id: str
    sheet_id: str
    row_num: int
    col_num: int
    data: Dict[str, Any]
    updated_at: str
    updated_by: str

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

class CellLock(BaseModel):
    cell_id: str
    sheet_id: str
    user_id: str
    loacked_at: str
    expires_at: str
 