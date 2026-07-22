# Task Tracker Backend

A lightweight FastAPI backend for a simple Task Tracker learning project. It currently exposes a health check endpoint and is structured to grow into a full CRUD API backed by JSON file storage.

## Setup

### 1. Create and activate a virtual environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example env file and adjust values if needed:

**Linux / macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

## Running the server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Testing the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "timestamp": "2026-07-04T12:00:00.000000+00:00"}
```