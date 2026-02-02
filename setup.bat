@echo off
REM Chemical Equipment Parameter Visualizer - Quick Setup Script
REM FOSSEE Internship Technical Screening Project

echo ==========================================
echo Chemical Equipment Visualizer Setup
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check Node.js installation
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js 14 or higher.
    pause
    exit /b 1
)

echo [OK] Node.js found
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Setup Django backend
echo.
echo Setting up Django backend...
cd backend

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
set /p CREATEUSER="Do you want to create a superuser for Django admin? (y/n): "
if /i "%CREATEUSER%"=="y" (
    python manage.py createsuperuser
)

cd ..

REM Setup React frontend
echo.
echo Setting up React frontend...
cd frontend

echo Installing Node.js dependencies (this may take a few minutes)...
call npm install

cd ..

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To run the application:
echo.
echo 1. Backend (Terminal 1):
echo    cd backend
echo    ..\venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo 3. Desktop App (Terminal 3):
echo    venv\Scripts\activate
echo    cd desktop
echo    python main.py
echo.
echo Sample CSV file available: sample_equipment_data.csv
echo.
pause
