#!/bin/bash

# Chemical Equipment Parameter Visualizer - Quick Setup Script
# FOSSEE Internship Technical Screening Project

echo "=========================================="
echo "Chemical Equipment Visualizer Setup"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check Node.js installation
if ! command -v node &> /dev/null
then
    echo "ERROR: Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

echo "✓ Node.js found"
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup Django backend
echo ""
echo "Setting up Django backend..."
cd backend

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Create superuser for Django admin (optional):"
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python manage.py createsuperuser
fi

cd ..

# Setup React frontend
echo ""
echo "Setting up React frontend..."
cd frontend

echo "Installing Node.js dependencies (this may take a few minutes)..."
npm install

cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source ../venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Desktop App (Terminal 3):"
echo "   source venv/bin/activate"
echo "   cd desktop"
echo "   python main.py"
echo ""
echo "Sample CSV file available: sample_equipment_data.csv"
echo ""
