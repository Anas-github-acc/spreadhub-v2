import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import SpreadsheetEditor from './components/SpreadsheetEditor';
import { Spreadsheet } from './types';

function App() {
  const [activeSpreadsheet, setActiveSpreadsheet] = useState<Spreadsheet | null>(null);

  const handleCreateSpreadsheet = (name: string) => {
    const newSpreadsheet: Spreadsheet = {
      id: `spreadsheet-${Date.now()}`,
      name,
      sheets: [
        {
          id: 'sheet1',
          name: 'Sheet 1',
          cells: {},
        },
      ],
      activeSheetIndex: 0,
    };
    setActiveSpreadsheet(newSpreadsheet);
  };

  return (
    <div className="h-screen w-full bg-white">
      {activeSpreadsheet ? (
        <SpreadsheetEditor initialSpreadsheet={activeSpreadsheet} />
      ) : (
        <LandingPage onCreateSpreadsheet={handleCreateSpreadsheet} />
      )}
    </div>
  );
}

export default App;