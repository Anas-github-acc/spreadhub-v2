import React from 'react';
import { 
  Bold, Italic, Underline, AlignLeft, AlignCenter, AlignRight,
  Download, Share, Settings, Plus, Trash, Copy, Columns
} from 'lucide-react';
import { CellStyle } from '../types';

interface ToolbarProps {
  onFormatChange: (style: Partial<CellStyle>) => void;
  onAddRow: () => void;
  onAddColumn: () => void;
  onDeleteRow: () => void;
  onDeleteColumn: () => void;
  selectedCellStyle?: CellStyle;
  spreadsheetName: string;
  onSpreadsheetNameChange: (name: string) => void;
  isEditing: boolean;
}

const Toolbar: React.FC<ToolbarProps> = ({
  onFormatChange,
  onAddRow,
  onAddColumn,
  onDeleteRow,
  onDeleteColumn,
  selectedCellStyle = {},
  spreadsheetName,
  onSpreadsheetNameChange,
  isEditing,
}) => {
  const [isEditingName, setIsEditingName] = React.useState(false);
  const [nameValue, setNameValue] = React.useState(spreadsheetName);
  
  React.useEffect(() => {
    setNameValue(spreadsheetName);
  }, [spreadsheetName]);

  const handleNameClick = () => {
    setIsEditingName(true);
  };

  const handleNameBlur = () => {
    setIsEditingName(false);
    if (nameValue.trim()) {
      onSpreadsheetNameChange(nameValue.trim());
    } else {
      setNameValue(spreadsheetName);
    }
  };

  const handleNameKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      if (nameValue.trim()) {
        onSpreadsheetNameChange(nameValue.trim());
      } else {
        setNameValue(spreadsheetName);
      }
      setIsEditingName(false);
    } else if (e.key === 'Escape') {
      setNameValue(spreadsheetName);
      setIsEditingName(false);
    }
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameValue(e.target.value);
  };

  const ToolbarButton: React.FC<{
    icon: React.ReactNode;
    active?: boolean;
    onClick: () => void;
    title: string;
    disabled?: boolean;
  }> = ({ icon, active, onClick, title, disabled = false }) => (
    <button
      className={`h-8 w-8 rounded p-1 text-sm ${
        active ? 'bg-gray-200 text-gray-900' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
      } ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
      onClick={onClick}
      title={title}
      disabled={disabled}
    >
      {icon}
    </button>
  );

  return (
    <div className="flex flex-col border-b border-gray-200">
      <div className="flex items-center justify-between p-2">
        <div className="flex items-center space-x-2">
          {isEditingName ? (
            <input
              type="text"
              className="w-64 rounded border border-gray-300 px-2 py-1 text-lg font-medium outline-none focus:border-blue-500"
              value={nameValue}
              onChange={handleNameChange}
              onBlur={handleNameBlur}
              onKeyDown={handleNameKeyDown}
              autoFocus
            />
          ) : (
            <h1
              className="text-lg font-medium text-gray-800 hover:bg-gray-100 px-2 py-1 rounded cursor-pointer"
              onClick={handleNameClick}
            >
              {spreadsheetName || 'Untitled Spreadsheet'}
            </h1>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <ToolbarButton
            icon={<Download size={16} />}
            onClick={() => alert('Download feature coming soon')}
            title="Download"
          />
          <ToolbarButton
            icon={<Share size={16} />}
            onClick={() => alert('Share feature coming soon')}
            title="Share"
          />
          <ToolbarButton
            icon={<Settings size={16} />}
            onClick={() => alert('Settings feature coming soon')}
            title="Settings"
          />
        </div>
      </div>
      <div className="flex items-center space-x-1 border-t border-gray-200 p-1">
        <div className="flex space-x-1 border-r border-gray-200 pr-2">
          <ToolbarButton
            icon={<Bold size={16} />}
            active={selectedCellStyle.bold}
            onClick={() => onFormatChange({ bold: !selectedCellStyle.bold })}
            title="Bold"
            disabled={!isEditing}
          />
          <ToolbarButton
            icon={<Italic size={16} />}
            active={selectedCellStyle.italic}
            onClick={() => onFormatChange({ italic: !selectedCellStyle.italic })}
            title="Italic"
            disabled={!isEditing}
          />
          <ToolbarButton
            icon={<Underline size={16} />}
            active={selectedCellStyle.underline}
            onClick={() => onFormatChange({ underline: !selectedCellStyle.underline })}
            title="Underline"
            disabled={!isEditing}
          />
        </div>
        <div className="flex space-x-1 border-r border-gray-200 pr-2">
          <ToolbarButton
            icon={<AlignLeft size={16} />}
            active={selectedCellStyle.align === 'left'}
            onClick={() => onFormatChange({ align: 'left' })}
            title="Align Left"
            disabled={!isEditing}
          />
          <ToolbarButton
            icon={<AlignCenter size={16} />}
            active={selectedCellStyle.align === 'center'}
            onClick={() => onFormatChange({ align: 'center' })}
            title="Align Center"
            disabled={!isEditing}
          />
          <ToolbarButton
            icon={<AlignRight size={16} />}
            active={selectedCellStyle.align === 'right'}
            onClick={() => onFormatChange({ align: 'right' })}
            title="Align Right"
            disabled={!isEditing}
          />
        </div>
        <div className="flex space-x-1 border-r border-gray-200 pr-2">
          <ToolbarButton
            icon={<Plus size={16} />}
            onClick={onAddRow}
            title="Add Row"
          />
          <ToolbarButton
            icon={<Columns size={16} />}
            onClick={onAddColumn}
            title="Add Column"
          />
        </div>
        <div className="flex space-x-1">
          <ToolbarButton
            icon={<Trash size={16} />}
            onClick={onDeleteRow}
            title="Delete Row"
          />
          <ToolbarButton
            icon={<Copy size={16} />}
            onClick={onDeleteColumn}
            title="Delete Column"
          />
        </div>
      </div>
    </div>
  );
};

export default Toolbar;