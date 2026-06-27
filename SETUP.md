# ContentFlow Setup Guide

This guide will help you set up and run the ContentFlow application on your local machine.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm (comes with Node.js)

## Initial Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (already created)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Verify .env file exists (already created with defaults)
# You can customize settings in backend/.env
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies (already installed)
npm install

# Verify vite.config.js has proxy configuration (already configured)
```

## Running the Application

### Option 1: Run Both Separately (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The backend will run on `http://localhost:8000` and the frontend on `http://localhost:5173`.

### Option 2: Quick Start Script

You can create a simple script to start both:

**start.sh (macOS/Linux):**
```bash
#!/bin/bash

# Start backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both"

# Wait for both processes
wait
```

Make it executable:
```bash
chmod +x start.sh
./start.sh
```

## Verification

Once both services are running:

1. Open your browser and go to `http://localhost:5173`
2. You should see the ContentFlow Dashboard
3. The dashboard will show the system status (API, Database, Storage)
4. Click "Refresh Status" to verify the health check endpoint is working

Alternatively, test the backend directly:
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "storage": "ready"
}
```

## Troubleshooting

### Backend Issues

**Virtual environment not activating:**
- Ensure you're in the `backend/` directory
- Check that `.venv/` directory exists

**Dependencies not installing:**
- Try upgrading pip: `pip install --upgrade pip`
- Ensure Python 3.9+ is installed: `python3 --version`

**Database errors:**
- Check that `contentflow.db` file is being created in the backend directory
- Verify `.env` file has correct `DATABASE_URL`

**Port already in use:**
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or kill the process using port 8000: `lsof -ti:8000 | xargs kill -9`

### Frontend Issues

**Dependencies not installing:**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules/` and `package-lock.json`, then run `npm install` again

**Port already in use:**
- Vite will automatically try the next available port (5174, 5175, etc.)

**Proxy errors:**
- Verify `vite.config.js` has the proxy configuration
- Ensure backend is running on port 8000

### Common Issues

**CORS errors:**
- Ensure backend CORS middleware is configured in `app/main.py`
- Check that frontend origin (`http://localhost:5173`) is allowed

**Storage directory errors:**
- Check that `storage/` directory exists at project root
- Verify `.env` has correct `STORAGE_BASE_PATH`

## Development Tips

- Backend runs with auto-reload when using `--reload` flag
- Frontend has hot module replacement (HMR) enabled by default
- Check backend logs in the terminal where uvicorn is running
- Use browser DevTools for frontend debugging
- API documentation available at `http://localhost:8000/docs` when backend is running

## Next Steps

After successful setup, refer to the [Development Plan](Docs/DEVELOPMENT_PLAN.md) to continue with Phase 1 (Project Module).
