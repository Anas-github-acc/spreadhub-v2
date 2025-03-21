CREATE TABLE spreadsheets (
    spreadsheet_id VARCHAR PRIMARY KEY,
    owner_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    locale VARCHAR,
    time_zone VARCHAR,
    auto_recalc VARCHAR CHECK (auto_recalc IN ('ON_CHANGE', 'MINUTE', 'HOUR')),
    default_format JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_public BOOLEAN
);

CREATE TABLE sheets (
    sheet_id VARCHAR PRIMARY KEY,
    spreadsheet_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    index INTEGER,
    sheet_type VARCHAR CHECK (sheet_type IN ('GRID', 'OBJECT')),
    grid_properties JSON,
    gid INTEGER NOT NULL,  -- Added for Google Sheets compatibility
    FOREIGN KEY (spreadsheet_id) REFERENCES spreadsheets(spreadsheet_id)
);

CREATE TABLE cells (
    cell_id VARCHAR PRIMARY KEY,
    sheet_id VARCHAR NOT NULL,
    row_num INTEGER NOT NULL,
    col_num INTEGER NOT NULL,
    data JSON,
    updated_at TIMESTAMP,
    updated_by VARCHAR,
    FOREIGN KEY (sheet_id) REFERENCES sheets(sheet_id)
);

CREATE TABLE merge_tree (
    node_id VARCHAR PRIMARY KEY,
    sheet_id VARCHAR NOT NULL,
    cell_id VARCHAR NOT NULL,
    parent_node_id VARCHAR,
    operation_type VARCHAR CHECK (operation_type IN ('insert', 'update', 'delete')),
    cell_data JSON,
    owner_id VARCHAR,
    status VARCHAR CHECK (status IN ('merged', 'conflict', 'pending')),
    created_at TIMESTAMP,
    merged_at TIMESTAMP,
    conflict_resolved_at TIMESTAMP,
    FOREIGN KEY (sheet_id) REFERENCES sheets(sheet_id),
    FOREIGN KEY (cell_id) REFERENCES cells(cell_id)
);