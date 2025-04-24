import React, { useState } from 'react';
import { Sheet } from '../types';
import { PlusCircle } from 'lucide-react';

interface SheetTabsProps {
  sheets: Sheet[];
  activeSheetIndex: number;
  onSheetChange: (index: number) => void;
  onAddSheet: () => void;
  onRenameSheet: (sheetId: string, newName: string) => void;
}

const SheetTabs: React.FC<SheetTabsProps> = ({
  sheets,
  activeSheetIndex,
  onSheetChange,
  onAddSheet,
  onRenameSheet,
}) => {
  const [editingSheetId, setEditingSheetId] = useState<string | null>(null);
  const [newSheetName, setNewSheetName] = useState('');

  const handleTabClick = (index: number) => {
    if (editingSheetId === null) {
      onSheetChange(index);
    }
  };

  const handleDoubleClick = (sheetId: string, name: string) => {
    setEditingSheetId(sheetId);
    setNewSheetName(name);
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewSheetName(e.target.value);
  };

  const handleNameBlur = () => {
    if (editingSheetId && newSheetName.trim()) {
      onRenameSheet(editingSheetId, newSheetName.trim());
    }
    setEditingSheetId(null);
  };

  const handleNameKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      if (editingSheetId && newSheetName.trim()) {
        onRenameSheet(editingSheetId, newSheetName.trim());
      }
      setEditingSheetId(null);
    } else if (e.key === 'Escape') {
      setEditingSheetId(null);
    }
  };

  return (
    <div className="flex h-10 items-center border-t border-gray-300 bg-gray-100 px-4">
      <div className="flex h-full space-x-1 overflow-x-auto">
        {sheets.map((sheet, index) => (
          <div
            key={sheet.id}
            className={`group flex h-8 min-w-24 cursor-pointer items-center rounded-t-md border-b-2 px-4 
                      ${index === activeSheetIndex 
                        ? 'border-blue-500 bg-white' 
                        : 'border-transparent bg-gray-100 hover:bg-gray-200'}`}
            onClick={() => handleTabClick(index)}
            onDoubleClick={() => handleDoubleClick(sheet.id, sheet.name)}
          >
            {editingSheetId === sheet.id ? (
              <input
                type="text"
                className="w-full bg-transparent text-sm outline-none"
                value={newSheetName}
                onChange={handleNameChange}
                onBlur={handleNameBlur}
                onKeyDown={handleNameKeyDown}
                autoFocus
              />
            ) : (
              <span className="truncate text-sm">{sheet.name}</span>
            )}
          </div>
        ))}
      </div>
      <button
        className="ml-2 flex h-8 w-8 items-center justify-center rounded-full text-gray-600 hover:bg-gray-200 hover:text-gray-900"
        onClick={onAddSheet}
        title="Add sheet"
      >
        <PlusCircle size={18} />
      </button>
    </div>
  );
};

export default SheetTabs;