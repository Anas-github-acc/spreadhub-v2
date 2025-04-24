import React, { useState, useCallback } from 'react';
import { Spreadsheet, Sheet, Cell, CellStyle } from '../types';
import Grid from './Grid';
import Toolbar from './Toolbar';
import SheetTabs from './SheetTabs';
import { createCellId, parseCellId } from '../utils/cellUtils';

interface SpreadsheetEditorProps {
  initialSpreadsheet: Spreadsheet;
}

const DEFAULT_ROW_COUNT = 100;
const DEFAULT_COLUMN_COUNT = 26;

const SpreadsheetEditor: React.FC<SpreadsheetEditorProps> = ({ initialSpreadsheet }) => {
  const [spreadsheet, setSpreadsheet] = useState<Spreadsheet>(initialSpreadsheet);
  const [selectedCell, setSelectedCell] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  const activeSheet = spreadsheet.sheets[spreadsheet.activeSheetIndex];

  const handleCellChange = useCallback(
    (cellId: string, newValue: string) => {
      setSpreadsheet((prev) => {
        const updatedSheet = { ...prev.sheets[prev.activeSheetIndex] };
        const isFormula = newValue.startsWith('=');
        
        updatedSheet.cells = {
          ...updatedSheet.cells,
          [cellId]: {
            ...(updatedSheet.cells[cellId] || { id: cellId }),
            value: isFormula ? '' : newValue,
            formula: isFormula ? newValue : undefined,
            type: isFormula ? 'formula' : (isNaN(Number(newValue)) ? 'text' : 'number'),
          },
        };
        
        const updatedSheets = [...prev.sheets];
        updatedSheets[prev.activeSheetIndex] = updatedSheet;
        
        return {
          ...prev,
          sheets: updatedSheets,
        };
      });
      
      setIsEditing(false);
    },
    []
  );

  const handleCellFormatChange = useCallback(
    (style: Partial<CellStyle>) => {
      if (!selectedCell) return;
      
      setSpreadsheet((prev) => {
        const updatedSheet = { ...prev.sheets[prev.activeSheetIndex] };
        const cell = updatedSheet.cells[selectedCell] || {
          id: selectedCell,
          value: '',
          style: {},
        };
        
        updatedSheet.cells = {
          ...updatedSheet.cells,
          [selectedCell]: {
            ...cell,
            style: {
              ...(cell.style || {}),
              ...style,
            },
          },
        };
        
        const updatedSheets = [...prev.sheets];
        updatedSheets[prev.activeSheetIndex] = updatedSheet;
        
        return {
          ...prev,
          sheets: updatedSheets,
        };
      });
    },
    [selectedCell]
  );

  const handleSheetChange = useCallback(
    (index: number) => {
      setSpreadsheet((prev) => ({
        ...prev,
        activeSheetIndex: index,
      }));
      setSelectedCell(null);
    },
    []
  );

  const handleAddSheet = useCallback(() => {
    const newSheet: Sheet = {
      id: `sheet${spreadsheet.sheets.length + 1}`,
      name: `Sheet ${spreadsheet.sheets.length + 1}`,
      cells: {},
    };
    
    setSpreadsheet((prev) => ({
      ...prev,
      sheets: [...prev.sheets, newSheet],
      activeSheetIndex: prev.sheets.length,
    }));
  }, [spreadsheet.sheets.length]);

  const handleRenameSheet = useCallback(
    (sheetId: string, newName: string) => {
      setSpreadsheet((prev) => ({
        ...prev,
        sheets: prev.sheets.map((sheet) =>
          sheet.id === sheetId ? { ...sheet, name: newName } : sheet
        ),
      }));
    },
    []
  );

  const handleSpreadsheetNameChange = useCallback(
    (name: string) => {
      setSpreadsheet((prev) => ({
        ...prev,
        name,
      }));
    },
    []
  );

  const handleAddRow = useCallback(() => {
    alert('Add row functionality coming soon');
  }, []);

  const handleAddColumn = useCallback(() => {
    alert('Add column functionality coming soon');
  }, []);

  const handleDeleteRow = useCallback(() => {
    if (!selectedCell) {
      alert('Please select a cell first');
      return;
    }
    
    const { rowIndex } = parseCellId(selectedCell);
    alert(`Delete row ${rowIndex + 1} functionality coming soon`);
  }, [selectedCell]);

  const handleDeleteColumn = useCallback(() => {
    if (!selectedCell) {
      alert('Please select a cell first');
      return;
    }
    
    const { colIndex } = parseCellId(selectedCell);
    alert(`Delete column ${createCellId(0, colIndex).replace(/\d+$/, '')} functionality coming soon`);
  }, [selectedCell]);

  const handleSelectionChange = useCallback((cellId: string | null) => {
    setSelectedCell(cellId);
    setIsEditing(true);
  }, []);

  const selectedCellStyle = selectedCell ? activeSheet.cells[selectedCell]?.style : undefined;

  return (
    <div className="flex h-screen flex-col">
      <Toolbar
        onFormatChange={handleCellFormatChange}
        onAddRow={handleAddRow}
        onAddColumn={handleAddColumn}
        onDeleteRow={handleDeleteRow}
        onDeleteColumn={handleDeleteColumn}
        selectedCellStyle={selectedCellStyle}
        spreadsheetName={spreadsheet.name}
        onSpreadsheetNameChange={handleSpreadsheetNameChange}
        isEditing={isEditing && !!selectedCell}
      />
      <div className="flex-1 overflow-auto">
        <Grid
          rowCount={DEFAULT_ROW_COUNT}
          columnCount={DEFAULT_COLUMN_COUNT}
          cells={activeSheet.cells}
          onCellChange={handleCellChange}
          onSelectionChange={handleSelectionChange}
          columnWidths={activeSheet.columnWidths}
          rowHeights={activeSheet.rowHeights}
        />
      </div>
      <SheetTabs
        sheets={spreadsheet.sheets}
        activeSheetIndex={spreadsheet.activeSheetIndex}
        onSheetChange={handleSheetChange}
        onAddSheet={handleAddSheet}
        onRenameSheet={handleRenameSheet}
      />
    </div>
  );
};

export default SpreadsheetEditor;