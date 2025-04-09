# Spreadhub-v2 Backend

FastAPI-based backend service for Sheethub project.

## Manually Setup & Run the Server

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
uv sync
```

## Development

Run the development server:

```bash
fastapi dev app/main.py
```

### or run this instead

Linux/MacOS:

```bash
chmod +x dev
dev
```

Windows:

```bash
./dev
```

## Testing

Run tests using pytest:

```bash
pytest
```

# Frontend Integration Guide

## Prerequisites

- Node.js 18.x or later
- npm (included with Node.js)
- Backend server running (follow steps above)

## Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd ./frontend
   ```
2. Install dependencies:

   ```bash
   npm install --save-dev openapi-typescript
   ```
3. Generate TypeScript types:

   ```bash
   npx openapi-typescript http://127.0.0.1:8000/api/v1/openapi.json -o src/types/api.ts
   ```

### Note

add the above command to `package.json` scripts for easier access.

```json
"export-type": npx openapi-typescript http://127.0.0.1:8000/api/v1/openapi.json -o src/types/api.ts
```

## Running Frontend

1. Start development server:

   ```bash
   npm run dev
   ```

   Access at `http://localhost:3000`

## Development Workflow

- **File Structure**:

  - `src/pages/`: Page components
  - `src/types/api.ts`: Generated API types
  - `src/components/`: Reusable components
- **API Integration Example**:

  ```typescript
  import { paths } from '../types/api';

  type SheetResponse = paths['/sheets']['post']['responses']['200']['content']['application/json'];

  async function createSheet() {
    const res = await fetch('http://127.0.0.1:8000/sheets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sheet_id: '1', user_id: 'user1', data: {} }),
    });
    const data: SheetResponse = await res.json();
    console.log(data);
  }
  ```

## Troubleshooting

- **Connection Refused**: Ensure backend is running
- **Missing Types**: Re-run type generation	
- **CORS Issues**: Check backend CORS settings in `.env`

## Working on the Backend (API)

- STEP 1: change the `.env.template` file to `.env` and set the following variables:
  
- STEP 2: run the server with the following command:

```bash
./dev
```

- STEP 3: then visit the following URL in your browser:

```bash
localhost:8000/docs
```

This will open the Swagger UI where you can test the API endpoints.

## Available API Endpoints

### Spreadsheet Operations

- `POST /api/v1/spreadsheets/create`

  - Creates a new spreadsheet
  - Requires: `user_id`
  - Returns: `Spreadsheet` object
- `POST /api/v1/spreadsheets/{spreadsheet_id}/createSheet`

  - Creates a new sheet in existing spreadsheet
  - Requires: `user_id`, `spreadsheet_id`
  - Returns: `Sheet` object

## Data Models

Key models for frontend integration:

- `Spreadsheet`: Main document container
- `Sheet`: Individual sheet within spreadsheet
- `CellData`: Cell content and formatting
- `SheetProperties`: Sheet configuration
- `ErrorResponse`: Standard error format

## Development Notes

- All endpoints are prefixed with `/api/v1/`
- CORS is enabled for frontend development
- Authentication is required for edit access to non-public spreadsheets
- Redirects handle invalid GIDs and unauthorized edit attempts

## Error Handling

Standard error responses include:

- 400: Invalid request
- 401: Unauthorized access
- 404: Resource not found
- 500: Server error
