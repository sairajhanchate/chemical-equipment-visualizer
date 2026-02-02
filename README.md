# Chemical Equipment Parameter Visualizer

A hybrid full-stack application for visualizing and analyzing chemical equipment parameters. This project demonstrates integration between Django REST Framework backend, React.js web frontend, and PyQt5 desktop application.

**Developed for:** FOSSEE Internship Technical Screening Project

## Project Overview

This system allows users to:
- Upload CSV files containing chemical equipment data
- Automatically calculate statistics (average pressure, temperature, equipment distribution)
- Visualize data through interactive charts
- Generate PDF reports
- Access data through both web and desktop interfaces

## System Architecture

```
├── Backend (Django + DRF)
│   ├── REST API endpoints
│   ├── CSV processing with Pandas
│   ├── Data storage (SQLite)
│   └── PDF generation (ReportLab)
│
├── Web Frontend (React.js)
│   ├── File upload interface
│   ├── Data tables
│   ├── Chart.js visualizations
│   └── PDF download functionality
│
└── Desktop Frontend (PyQt5)
    ├── Standalone Python application
    ├── Matplotlib embedded charts
    ├── Server synchronization
    └── PDF report download
```

## Technology Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data processing and analysis
- **ReportLab** - PDF report generation
- **SQLite** - Database (default Django DB)

### Web Frontend
- **React.js 18.2.0** - UI framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Bootstrap 5** - Styling

### Desktop Frontend
- **PyQt5** - GUI framework
- **Matplotlib** - Chart generation
- **Requests** - API communication

## Prerequisites

Before setting up the project, ensure you have:

- **Python 3.8+** installed
- **Node.js 14+** and npm installed
- **pip** (Python package installer)
- **Virtual environment** support (venv or virtualenv)

## Installation and Setup

### Step 1: Clone or Extract the Project

```bash
cd chemical-equipment-visualizer
```

### Step 2: Set Up Backend (Django)

#### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Initialize Database

```bash
cd backend

# Create database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional - for admin access)
python manage.py createsuperuser
# Follow prompts to create admin credentials
```

#### Run Backend Server

```bash
python manage.py runserver
```

The backend API will be available at: `http://localhost:8000/api/`

**Important:** Keep this terminal window open and running.

### Step 3: Set Up Web Frontend (React)

Open a **new terminal window**.

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

The web application will open automatically at: `http://localhost:3000/`

**Important:** Keep this terminal window open and running.

### Step 4: Run Desktop Application (PyQt5)

Open a **new terminal window**.

```bash
# Activate the same virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run desktop application
cd desktop
python main.py
```

The PyQt5 desktop window will open.

## Project Structure

```
chemical-equipment-visualizer/
│
├── backend/                          # Django backend
│   ├── backend/                      # Project settings
│   │   ├── settings.py              # Django configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── wsgi.py                  # WSGI config
│   │   └── __init__.py
│   │
│   ├── equipment_api/               # Main API app
│   │   ├── models.py                # Database models
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # API views
│   │   ├── urls.py                  # API URL routing
│   │   ├── admin.py                 # Admin configuration
│   │   ├── utils.py                 # Utility functions (PDF generation)
│   │   └── __init__.py
│   │
│   ├── media/                       # Uploaded files and reports
│   │   ├── csvs/                    # Uploaded CSV files
│   │   └── reports/                 # Generated PDF reports
│   │
│   ├── manage.py                    # Django management script
│   └── db.sqlite3                   # SQLite database (created after migration)
│
├── frontend/                         # React web frontend
│   ├── public/
│   │   └── index.html               # HTML template
│   │
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── FileUpload.js       # CSV upload component
│   │   │   ├── DataTable.js        # Equipment data table
│   │   │   ├── Charts.js           # Chart.js visualizations
│   │   │   └── Statistics.js       # Statistics display
│   │   │
│   │   ├── services/
│   │   │   └── api.js              # API service for backend calls
│   │   │
│   │   ├── App.js                   # Main application component
│   │   ├── App.css                  # Application styles
│   │   └── index.js                 # React entry point
│   │
│   └── package.json                 # Node.js dependencies
│
├── desktop/                          # PyQt5 desktop application
│   └── main.py                      # Desktop application main file
│
├── requirements.txt                  # Python dependencies
├── sample_equipment_data.csv        # Sample CSV for testing
└── README.md                        # This file
```

## Usage Guide

### CSV File Format

Your CSV file should contain the following columns:

- **Equipment Name** - Unique identifier for equipment
- **Type** - Category/type of equipment (e.g., Pump, Reactor, Heat Exchanger)
- **Flowrate** - Flow rate in specified units
- **Pressure** - Operating pressure in bar
- **Temperature** - Operating temperature in °C

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
PUMP-001,Centrifugal Pump,150.5,5.2,45.8
REACTOR-001,CSTR,200.0,8.5,120.5
HEAT-EX-001,Shell and Tube,180.3,6.8,85.2
```

A sample CSV file is provided: `sample_equipment_data.csv`

### Using the Web Application

1. **Upload CSV File**
   - Click "Select CSV File" button
   - Choose your equipment data CSV
   - Click "Upload and Process"

2. **View Statistics**
   - Summary statistics display automatically after upload
   - Shows total equipment count, average pressure, and average temperature

3. **Analyze Data**
   - View equipment data in the table
   - Examine bar chart showing equipment type distribution
   - Analyze scatter plot of pressure vs temperature

4. **Download PDF Report**
   - Click "Download PDF" button in statistics section
   - PDF report will be downloaded to your computer

5. **View Upload History**
   - Scroll down to see recent uploads
   - Click "View" to load historical data
   - Click "PDF" to download report for past uploads

### Using the Desktop Application

1. **Upload CSV File**
   - Click "Upload CSV File" button
   - Select your CSV file
   - Data will be processed and displayed

2. **Sync from Server**
   - Click "Sync from Server" button
   - Fetches the latest upload from backend
   - Automatically displays the most recent data

3. **View Data**
   - Switch to "Equipment Data" tab to see table
   - Switch to "Visualizations" tab to see charts

4. **Download PDF Report**
   - Click "Download PDF Report" button
   - Choose save location
   - PDF will be saved to selected location

## API Endpoints

The backend provides the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check |
| POST | `/api/upload/` | Upload and process CSV file |
| GET | `/api/history/` | Get last 5 uploads |
| GET | `/api/upload/<id>/` | Get specific upload details |
| GET | `/api/report/<id>/` | Download PDF report |

## Features

### Backend Features
- ✅ CSV file validation (format, size)
- ✅ Pandas-based data processing
- ✅ Automatic statistical calculations
- ✅ Equipment type distribution analysis
- ✅ Professional PDF report generation
- ✅ Upload history tracking
- ✅ Error handling and validation

### Web Frontend Features
- ✅ Responsive Bootstrap design
- ✅ File upload with validation
- ✅ Interactive data tables
- ✅ Chart.js visualizations (Bar and Scatter)
- ✅ PDF download functionality
- ✅ Upload history view
- ✅ Real-time error/success notifications

### Desktop Frontend Features
- ✅ Native desktop interface
- ✅ Matplotlib chart embedding
- ✅ Server synchronization
- ✅ Background file upload
- ✅ PDF report download
- ✅ Tabbed interface for data and charts

## Error Handling

The application handles various error scenarios:

- **Invalid file format** - Non-CSV files are rejected
- **Missing columns** - CSV validation checks for required columns
- **Empty data** - Handles empty or invalid CSV files
- **Network errors** - Graceful handling of backend connectivity issues
- **File size limits** - Enforces 5MB maximum file size

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Run on different port
python manage.py runserver 8001
# Update API_BASE_URL in frontend accordingly
```

**Database errors:**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# React will automatically suggest alternative port (3001)
# Or set PORT environment variable:
PORT=3001 npm start
```

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Desktop Application Issues

**PyQt5 import errors:**
```bash
# Reinstall PyQt5
pip uninstall PyQt5
pip install PyQt5==5.15.10
```

**Backend connection refused:**
- Ensure Django backend is running on port 8000
- Check firewall settings
- Verify API_BASE_URL in `desktop/main.py`

## Development Notes

### Code Style
- Python code follows PEP 8 style guidelines
- JavaScript follows standard ES6+ conventions
- Comments are included for clarity
- Modular design for maintainability

### Database
- Uses SQLite by default for simplicity
- Can be easily switched to PostgreSQL or MySQL
- Migrations are version controlled

### Security Considerations
- CORS configured for development (localhost)
- File size limits enforced
- File type validation
- Input sanitization
- Change SECRET_KEY in production

## Future Enhancements

Potential improvements for production deployment:

- [ ] User authentication and authorization
- [ ] PostgreSQL database for production
- [ ] Docker containerization
- [ ] Advanced data filtering and search
- [ ] Export to Excel functionality
- [ ] Real-time data updates using WebSockets
- [ ] Mobile responsive improvements
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

## Testing the Application

### Quick Test with Sample Data

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm start`
3. Upload `sample_equipment_data.csv` through web interface
4. Verify data appears in tables and charts
5. Download PDF report
6. Open desktop app and click "Sync from Server"

### Creating Custom Test Data

Generate your own CSV with the required columns:
```python
import pandas as pd

data = {
    'Equipment Name': ['TEST-001', 'TEST-002'],
    'Type': ['Pump', 'Reactor'],
    'Flowrate': [100.0, 150.0],
    'Pressure': [5.0, 8.0],
    'Temperature': [40.0, 120.0]
}

df = pd.DataFrame(data)
df.to_csv('test_data.csv', index=False)
```

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- React Documentation: https://react.dev/
- Chart.js Documentation: https://www.chartjs.org/docs/
- PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages carefully
3. Verify all dependencies are installed correctly
4. Ensure all three components (backend, frontend, desktop) are running

## License

This project is developed as part of FOSSEE Internship Technical Screening.

---

**Project Status:** Complete and ready for evaluation

**Last Updated:** February 2026
