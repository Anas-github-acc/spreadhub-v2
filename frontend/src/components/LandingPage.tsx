import React, { useState } from 'react';
import { FileSpreadsheet, Plus } from 'lucide-react';

interface LandingPageProps {
  onCreateSpreadsheet: (name: string) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onCreateSpreadsheet }) => {
  const [isCreating, setIsCreating] = useState(false);
  const [newSpreadsheetName, setNewSpreadsheetName] = useState('');

  const handleCreate = () => {
    if (newSpreadsheetName.trim()) {
      onCreateSpreadsheet(newSpreadsheetName.trim());
    } else {
      onCreateSpreadsheet('Untitled Spreadsheet');
    }
  };

  return (
    <div className="flex h-full flex-col">
      <header className="border-b border-gray-200 bg-white px-6 py-4">
        <h1 className="text-2xl font-semibold text-gray-800">Spreadsheets</h1>
      </header>
      
      <main className="flex-1 overflow-auto p-6">
        <div className="mb-8">
          <button
            className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
            onClick={() => setIsCreating(true)}
          >
            <Plus size={16} />
            New Spreadsheet
          </button>
        </div>

        {isCreating && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="w-96 rounded-lg bg-white p-6 shadow-xl">
              <h2 className="mb-4 text-lg font-semibold">Create New Spreadsheet</h2>
              <input
                type="text"
                className="mb-4 w-full rounded border border-gray-300 px-3 py-2"
                placeholder="Untitled Spreadsheet"
                value={newSpreadsheetName}
                onChange={(e) => setNewSpreadsheetName(e.target.value)}
                autoFocus
              />
              <div className="flex justify-end gap-2">
                <button
                  className="rounded px-4 py-2 text-gray-600 hover:bg-gray-100"
                  onClick={() => setIsCreating(false)}
                >
                  Cancel
                </button>
                <button
                  className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
                  onClick={handleCreate}
                >
                  Create
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          <button
            className="group flex h-52 flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-4 hover:border-blue-500 hover:bg-blue-50"
            onClick={() => setIsCreating(true)}
          >
            <FileSpreadsheet className="mb-2 h-8 w-8 text-gray-400 group-hover:text-blue-500" />
            <span className="text-sm font-medium text-gray-600 group-hover:text-blue-600">
              Create New Spreadsheet
            </span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;