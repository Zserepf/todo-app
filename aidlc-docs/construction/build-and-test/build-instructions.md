# Build Instructions — Unit 1: Notification Backend

## Prerequisites
- **Python**: 3.12+
- **Package Manager**: pip
- **Dependencies**: See `backend/requirements.txt`
- **Test Framework**: pytest

## Build Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
pip install pytest
```

### 2. Verify Application Starts
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Verify Endpoints Registered
With the server running, visit `http://localhost:8000/docs` and confirm:
- `/api/notifications` (GET) is listed
- `/api/notifications/{notification_id}/read` (PATCH) is listed
- `/api/notifications/read-all` (POST) is listed
- `/api/notifications` (DELETE) is listed

### 4. Verify Data File Exists
```bash
cat backend/data/notifications.json
```
**Expected**: `[]`

## Build Artifacts
- No compiled artifacts (Python interpreted)
- `backend/data/notifications.json` — empty JSON array (storage file)

## Troubleshooting

### Import Error: email-validator
- **Cause**: `pydantic[email]` extras not installed
- **Solution**: `pip install pydantic[email]`

### ModuleNotFoundError: passlib or python-jose
- **Cause**: Auth dependencies not installed
- **Solution**: `pip install -r requirements.txt`
