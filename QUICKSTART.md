# Quick Start Guide

## 30-Second Setup (Experienced Developers)

### Prerequisites Installed?
- Python 3.8+
- Node.js 14+
- pip

### Automated Setup (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

### Automated Setup (Windows)
```cmd
setup.bat
```

### Manual Setup
```bash
# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py runserver  # Terminal 1

# Frontend (new terminal)
cd frontend
npm install
npm start  # Terminal 2

# Desktop (new terminal)
source venv/bin/activate  # Windows: venv\Scripts\activate
cd desktop
python main.py  # Terminal 3
```

## First Test (2 Minutes)

1. Open web browser: http://localhost:3000
2. Click "Select CSV File"
3. Choose `sample_equipment_data.csv`
4. Click "Upload and Process"
5. View charts and download PDF
6. Open desktop app
7. Click "Sync from Server"

## Common Issues

**Port 8000 in use:**
```bash
python manage.py runserver 8001
# Update API_BASE_URL in frontend/src/services/api.js
```

**Database errors:**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
```

**npm errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Endpoints Test

```bash
# Health check
curl http://localhost:8000/api/health/

# Upload CSV (with curl)
curl -X POST -F "csv_file=@sample_equipment_data.csv" http://localhost:8000/api/upload/

# View history
curl http://localhost:8000/api/history/
```

## Project Components

```
Backend:  http://localhost:8000/api/
Frontend: http://localhost:3000/
Admin:    http://localhost:8000/admin/
Desktop:  Run python desktop/main.py
```

## Full Documentation

See README.md for complete documentation.
