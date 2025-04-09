import duckdb


class DuckDBAdapter:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = duckdb.connect(db_path)
        with open("app/db_schema/duckdb_schema.sql") as f:
            self.conn.execute(f.read())

    # async def save_spreadsheet(self, spreadsheet: Spreadsheet):
    #     self.conn.execute(
    #         """
    #         INSERT INTO spreadsheets (
    #             spreadsheet_id, owner_id, title, locale, time_zone, auto_recalc,
    #             created_at, updated_at, is_public
    #         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    #         ON CONFLICT (spreadsheet_id) DO UPDATE SET
    #             owner_id = EXCLUDED.owner_id,
    #             title = EXCLUDED.title,
    #             locale = EXCLUDED.locale,
    #             time_zone = EXCLUDED.time_zone,
    #             auto_recalc = EXCLUDED.auto_recalc,
    #             created_at = EXCLUDED.created_at,
    #             updated_at = EXCLUDED.updated_at,
    #             is_public = EXCLUDED.is_public
    #         """,
    #         (
    #             spreadsheet.spreadsheet_id, str(spreadsheet.owner_id), spreadsheet.properties.title,
    #             spreadsheet.properties.locale, spreadsheet.properties.time_zone, spreadsheet.properties.auto_recalc,
    #             spreadsheet.created_at, spreadsheet.updated_at, spreadsheet.is_public
    #         )
    #     )

    # async def save_sheet(self, sheet: Sheet):
    #     self.conn.execute(
    #         """
    #         INSERT INTO sheets (
    #             sheet_id, spreadsheet_id, title, index, sheet_type, grid_properties, gid
    #         ) VALUES (?, ?, ?, ?, ?, ?, ?)
    #         ON CONFLICT (sheet_id) DO UPDATE SET
    #             spreadsheet_id = EXCLUDED.spreadsheet_id,
    #             title = EXCLUDED.title,
    #             index = EXCLUDED.index,
    #             sheet_type = EXCLUDED.sheet_type,
    #         """,
    #         (
    #             sheet.sheet_id, sheet.spreadsheet_id, sheet.properties.title, sheet.properties.index,
    #             sheet.properties.sheet_type
    #         )
    #     )

    # async def get_spreadsheet(self, spreadsheet_id: str) -> Spreadsheet:
    #     result = self.conn.execute(
    #         "SELECT * FROM spreadsheets WHERE spreadsheet_id = ?",
    #         (spreadsheet_id,)
    #     ).fetchone()
    #     if not result:
    #         raise ValueError("Spreadsheet not found")
    #     return Spreadsheet(
    #         spreadsheet_id=result[0],
    #         owner_id=UUID(result[1]),
    #         title=result[2],
    #         locale=result[3],
    #         time_zone=result[4],
    #         auto_recalc=result[5],
    #         default_format=eval(result[6]),
    #         created_at=result[7],
    #         updated_at=result[8],
    #         is_public=result[9]
    #     )
