import React, { useState, useEffect, useRef } from 'react';
import { Cell as CellType } from '../types';

interface CellProps {
  cell: CellType;
  isActive: boolean;
  onClick: () => void;
  onChange: (value: string) => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
  style?: React.CSSProperties;
}

const Cell: React.FC<CellProps> = ({
  cell,
  isActive,
  onClick,
  onChange,
  onKeyDown,
  style = {},
}) => {
  const [editMode, setEditMode] = useState(false);
  const [inputValue, setInputValue] = useState(cell.formula || cell.value);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isActive && editMode && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isActive, editMode]);

  useEffect(() => {
    setInputValue(cell.formula || cell.value);
  }, [cell.formula, cell.value]);

  const handleDoubleClick = () => {
    setEditMode(true);
  };

  const handleBlur = () => {
    setEditMode(false);
    onChange(inputValue);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      setEditMode(false);
      onChange(inputValue);
    } else if (e.key === 'Escape') {
      setEditMode(false);
      setInputValue(cell.formula || cell.value);
    } else {
      onKeyDown(e);
    }
  };

  const getCellStyle = (): React.CSSProperties => {
    const cellStyle: React.CSSProperties = {
      fontWeight: cell.style?.bold ? 'bold' : 'normal',
      fontStyle: cell.style?.italic ? 'italic' : 'normal',
      textDecoration: cell.style?.underline ? 'underline' : 'none',
      textAlign: cell.style?.align || 'left',
      backgroundColor: cell.style?.backgroundColor || 'transparent',
      color: cell.style?.textColor || 'inherit',
      ...style,
    };

    if (isActive) {
      cellStyle.outline = '2px solid #4285F4';
      cellStyle.outlineOffset = '-2px';
      cellStyle.zIndex = 2;
    }

    return cellStyle;
  };

  const renderDisplayValue = () => {
    const displayValue = cell.value;
    
    // Display the calculated result of a formula
    if (cell.type === 'formula' && !editMode) {
      return displayValue;
    }
    
    return displayValue;
  };

  return (
    <div
      className="relative h-full w-full overflow-hidden border-b border-r border-gray-200 outline-none transition-all duration-100"
      style={getCellStyle()}
      onClick={onClick}
      onDoubleClick={handleDoubleClick}
    >
      {editMode ? (
        <input
          ref={inputRef}
          className="absolute inset-0 h-full w-full px-2 py-1 outline-none"
          value={inputValue}
          onChange={handleInputChange}
          onBlur={handleBlur}
          onKeyDown={handleInputKeyDown}
        />
      ) : (
        <div className="h-full w-full overflow-hidden text-ellipsis whitespace-nowrap px-2 py-1">
          {renderDisplayValue()}
        </div>
      )}
    </div>
  );
};

export default Cell;