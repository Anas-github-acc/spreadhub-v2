import { Spreadsheet, Sheet, ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const createSpreadsheet = async (name: string): Promise<ApiResponse<Spreadsheet>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/spreadsheets/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name }),
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating spreadsheet:', error);
    return {
      success: false,
      error: 'Failed to create spreadsheet',
    };
  }
};

export const createSheet = async (
  spreadsheetId: string,
  sheetName: string
): Promise<ApiResponse<Sheet>> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/spreadsheets/${spreadsheetId}/createSheet`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: sheetName }),
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating sheet:', error);
    return {
      success: false,
      error: 'Failed to create sheet',
    };
  }
};

export const updateSpreadsheetStatus = async (
  spreadsheetId: string,
  status: 'active' | 'archived' | 'deleted'
): Promise<ApiResponse<Spreadsheet>> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/spreadsheets/${spreadsheetId}/${status}`,
      {
        method: 'PATCH',
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating spreadsheet status:', error);
    return {
      success: false,
      error: 'Failed to update spreadsheet status',
    };
  }
};

export const getSpreadsheet = async (
  spreadsheetId: string
): Promise<ApiResponse<Spreadsheet>> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/spreadsheets/${spreadsheetId}`,
      {
        method: 'GET',
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching spreadsheet:', error);
    return {
      success: false,
      error: 'Failed to fetch spreadsheet',
    };
  }
};

export const updateSpreadsheet = async (
  spreadsheetId: string,
  spreadsheet: Partial<Spreadsheet>
): Promise<ApiResponse<Spreadsheet>> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/spreadsheets/${spreadsheetId}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(spreadsheet),
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating spreadsheet:', error);
    return {
      success: false,
      error: 'Failed to update spreadsheet',
    };
  }
};