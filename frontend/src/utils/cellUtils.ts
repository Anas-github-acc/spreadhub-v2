import { Cell } from '../types';

// Converts column index to column letter (0 => A, 1 => B, etc.)
export const indexToColumnLabel = (index: number): string => {
  let columnLabel = '';
  let tempIndex = index;
  
  while (tempIndex >= 0) {
    columnLabel = String.fromCharCode(65 + (tempIndex % 26)) + columnLabel;
    tempIndex = Math.floor(tempIndex / 26) - 1;
  }
  
  return columnLabel;
};

// Converts column letter to column index (A => 0, B => 1, etc.)
export const columnLabelToIndex = (label: string): number => {
  let index = 0;
  
  for (let i = 0; i < label.length; i++) {
    index = index * 26 + label.charCodeAt(i) - 64;
  }
  
  return index - 1;
};

// Creates a cell ID from row and column indices
export const createCellId = (rowIndex: number, colIndex: number): string => {
  const columnLabel = indexToColumnLabel(colIndex);
  return `${columnLabel}${rowIndex + 1}`;
};

// Parse cell ID to get row and column indices
export const parseCellId = (cellId: string): { rowIndex: number; colIndex: number } => {
  const matches = cellId.match(/([A-Z]+)(\d+)/);
  
  if (!matches) {
    throw new Error(`Invalid cell ID: ${cellId}`);
  }
  
  const [, columnLabel, rowLabel] = matches;
  const rowIndex = parseInt(rowLabel) - 1;
  const colIndex = columnLabelToIndex(columnLabel);
  
  return { rowIndex, colIndex };
};

// Calculate a simple formula
export const calculateFormula = (formula: string, getCellValue: (cellId: string) => string): string => {
  try {
    // Replace cell references with their values
    const valueFormula = formula.replace(/[A-Z]+\d+/g, (cellId) => {
      const value = getCellValue(cellId);
      return isNaN(Number(value)) ? '0' : value;
    });
    
    // Remove the leading = sign
    const expressionToEvaluate = valueFormula.substring(1);
    
    // Use Function constructor to safely evaluate the expression
    // This is a simple implementation - in production you'd want more robust formula handling
    const result = new Function(`return ${expressionToEvaluate}`)();
    
    return result.toString();
  } catch (error) {
    console.error('Error calculating formula:', error);
    return '#ERROR!';
  }
};

// Create a default empty cell
export const createEmptyCell = (rowIndex: number, colIndex: number): Cell => {
  const id = createCellId(rowIndex, colIndex);
  
  return {
    id,
    value: '',
    type: 'text',
    style: {
      align: 'left',
    },
  };
};