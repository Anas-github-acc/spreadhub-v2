export interface Cell {
  id: string;
  value: string;
  formula?: string;
  type?: 'text' | 'number' | 'formula' | 'date';
  style?: CellStyle;
}

export interface CellStyle {
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  align?: 'left' | 'center' | 'right';
  backgroundColor?: string;
  textColor?: string;
}

export interface Sheet {
  id: string;
  name: string;
  cells: Record<string, Cell>;
  columnWidths?: Record<number, number>;
  rowHeights?: Record<number, number>;
}

export interface Spreadsheet {
  id: string;
  name: string;
  sheets: Sheet[];
  activeSheetIndex: number;
  status?: 'active' | 'archived' | 'deleted';
  created?: string;
  updated?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}