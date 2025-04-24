import React, { useState, useEffect, useCallback } from 'react';
import { Cell as CellType } from '../types';
import { createCellId, createEmptyCell, calculateFormula } from '../utils/cellUtils';
import Cell from './Cell';

interface GridProps {
  rowCount: number;
  columnCount: number;
  cells: Record<string, CellType>;
  onCellChange: (cellId: string, newValue: string) => void;
  onSelectionChange?: (selection: string | null) => void;
  columnWidths?: Record<number, number>;
  rowHeights?: Record<number, number>;
}

const Grid: React.FC<GridProps> = ({
  rowCount,
  columnCount,
  cells,
  onCellChange,
  onSelectionChange,
  columnWidths = {},
  rowHeights = {},
}) => {
  const [activeCell, setActiveCell] = useState<string | null>(null);
  const [hoveredHeader, setHoveredHeader] = useState<{ type: 'row' | 'column'; index: number } | null>(null);

  const defaultColumnWidth = 120;
  const defaultRowHeight = 28;
  const headerSize = 28;

  useEffect(() => {
    if (onSelectionChange && activeCell) {
      onSelectionChange(activeCell);
    }
  }, [activeCell, onSelectionChange]);

  const getCell = useCallback(
    (rowIndex: number, colIndex: number): CellType => {
      const cellId = createCellId(rowIndex, colIndex);
      return cells[cellId] || createEmptyCell(rowIndex, colIndex);
    },
    [cells]
  );

  const getCellValue = useCallback(
    (cellId: string): string => {
      return cells[cellId]?.value || '';
    },
    [cells]
  );

  const handleCellClick = (cellId: string) => {
    setActiveCell(cellId);
  };

  const handleCellChange = (cellId: string, newValue: string) => {
    // Check if it's a formula
    const isFormula = newValue.startsWith('=');
    
    let value = newValue;
    if (isFormula) {
      // Store the formula but calculate the display value
      value = calculateFormula(newValue, getCellValue);
    }
    
    onCellChange(cellId, newValue);
  };

  const handleKeyDown = (e: React.KeyboardEvent, rowIndex: number, colIndex: number) => {
    if (!activeCell) return;
    
    const handleNavigation = (newRow: number, newCol: number) => {
      if (newRow >= 0 && newRow < rowCount && newCol >= 0 && newCol < columnCount) {
        const newCellId = createCellId(newRow, newCol);
        setActiveCell(newCellId);
      }
    };

    switch (e.key) {
      case 'ArrowUp':
        e.preventDefault();
        handleNavigation(rowIndex - 1, colIndex);
        break;
      case 'ArrowDown':
        e.preventDefault();
        handleNavigation(rowIndex + 1, colIndex);
        break;
      case 'ArrowLeft':
        if (!e.shiftKey) {
          e.preventDefault();
          handleNavigation(rowIndex, colIndex - 1);
        }
        break;
      case 'ArrowRight':
        if (!e.shiftKey) {
          e.preventDefault();
          handleNavigation(rowIndex, colIndex + 1);
        }
        break;
      case 'Tab':
        e.preventDefault();
        handleNavigation(rowIndex, e.shiftKey ? colIndex - 1 : colIndex + 1);
        break;
      case 'Enter':
        if (!e.isDefaultPrevented()) {
          e.preventDefault();
          handleNavigation(rowIndex + 1, colIndex);
        }
        break;
    }
  };

  const renderHeaderCell = (index: number, type: 'row' | 'column') => {
    const isHovered = hoveredHeader?.type === type && hoveredHeader.index === index;
    const label = type === 'column' ? createCellId(0, index).replace(/\d+$/, '') : (index + 1).toString();
    
    return (
      <div
        key={`${type}-${index}`}
        className={`flex items-center justify-center bg-gray-100 border-r border-b border-gray-300 font-medium text-xs text-gray-700 select-none
                  ${isHovered ? 'bg-gray-200' : ''}`}
        style={{
          width: type === 'column' ? (columnWidths[index] || defaultColumnWidth) : headerSize,
          height: type === 'row' ? (rowHeights[index] || defaultRowHeight) : headerSize,
          position: 'sticky',
          ...(type === 'column' ? { top: 0, zIndex: 10 } : { left: 0, zIndex: 11 }),
        }}
        onMouseEnter={() => setHoveredHeader({ type, index })}
        onMouseLeave={() => setHoveredHeader(null)}
      >
        {label}
      </div>
    );
  };

  const renderCornerCell = () => (
    <div
      className="bg-gray-200 border-r border-b border-gray-300 select-none"
      style={{
        width: headerSize,
        height: headerSize,
        position: 'sticky',
        top: 0,
        left: 0,
        zIndex: 12,
      }}
    />
  );

  return (
    <div className="flex flex-col">
      <div className="flex">
        {renderCornerCell()}
        <div className="flex">
          {Array.from({ length: columnCount }).map((_, index) => renderHeaderCell(index, 'column'))}
        </div>
      </div>
      <div className="flex">
        <div className="flex flex-col">
          {Array.from({ length: rowCount }).map((_, index) => renderHeaderCell(index, 'row'))}
        </div>
        <div className="flex flex-col">
          {Array.from({ length: rowCount }).map((_, rowIndex) => (
            <div key={`row-${rowIndex}`} className="flex" style={{ height: rowHeights[rowIndex] || defaultRowHeight }}>
              {Array.from({ length: columnCount }).map((_, colIndex) => {
                const cellId = createCellId(rowIndex, colIndex);
                const cell = getCell(rowIndex, colIndex);
                
                return (
                  <div
                    key={cellId}
                    style={{ width: columnWidths[colIndex] || defaultColumnWidth }}
                  >
                    <Cell
                      cell={cell}
                      isActive={activeCell === cellId}
                      onClick={() => handleCellClick(cellId)}
                      onChange={(value) => handleCellChange(cellId, value)}
                      onKeyDown={(e) => handleKeyDown(e, rowIndex, colIndex)}
                    />
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Grid;