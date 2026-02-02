"""
Desktop Frontend for Chemical Equipment Parameter Visualizer
PyQt5 application that communicates with Django backend
Includes Matplotlib visualizations and data synchronization
FOSSEE Internship Technical Screening Project
"""

import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
    QMessageBox, QTabWidget, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Backend API configuration
API_BASE_URL = 'http://localhost:8000/api'


class UploadThread(QThread):
    """
    Background thread for CSV upload to prevent UI freezing
    Emits signals for success and failure
    """
    upload_success = pyqtSignal(dict)
    upload_error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """Execute file upload in background"""
        try:
            with open(self.file_path, 'rb') as f:
                files = {'csv_file': f}
                response = requests.post(f'{API_BASE_URL}/upload/', files=files)
                
                if response.status_code == 201:
                    self.upload_success.emit(response.json())
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    self.upload_error.emit(error_msg)
        except Exception as e:
            self.upload_error.emit(f'Error uploading file: {str(e)}')


class MatplotlibCanvas(FigureCanvas):
    """
    Canvas for embedding Matplotlib figures in PyQt5
    """
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)


class ChemicalEquipmentVisualizer(QMainWindow):
    """
    Main window for desktop application
    Provides interface for uploading CSVs, viewing data, and generating visualizations
    """
    
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header section
        header_layout = QHBoxLayout()
        title_label = QLabel('Chemical Equipment Parameter Visualizer')
        title_font = QFont('Arial', 16, QFont.Bold)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        badge_label = QLabel('FOSSEE Desktop Client')
        badge_label.setStyleSheet('background-color: #007bff; color: white; padding: 5px 10px; border-radius: 3px;')
        header_layout.addWidget(badge_label)
        main_layout.addLayout(header_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton('Upload CSV File')
        self.upload_btn.clicked.connect(self.upload_csv)
        self.upload_btn.setStyleSheet('background-color: #28a745; color: white; padding: 8px 16px; font-weight: bold;')
        button_layout.addWidget(self.upload_btn)
        
        self.sync_btn = QPushButton('Sync from Server')
        self.sync_btn.clicked.connect(self.sync_from_server)
        self.sync_btn.setStyleSheet('background-color: #17a2b8; color: white; padding: 8px 16px; font-weight: bold;')
        button_layout.addWidget(self.sync_btn)
        
        self.download_pdf_btn = QPushButton('Download PDF Report')
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        self.download_pdf_btn.setEnabled(False)
        self.download_pdf_btn.setStyleSheet('background-color: #dc3545; color: white; padding: 8px 16px; font-weight: bold;')
        button_layout.addWidget(self.download_pdf_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Statistics section
        stats_group = QGroupBox('Summary Statistics')
        stats_layout = QGridLayout()
        
        self.total_equipment_label = QLabel('Total Equipment: -')
        self.avg_pressure_label = QLabel('Avg Pressure: -')
        self.avg_temperature_label = QLabel('Avg Temperature: -')
        
        stats_layout.addWidget(self.total_equipment_label, 0, 0)
        stats_layout.addWidget(self.avg_pressure_label, 0, 1)
        stats_layout.addWidget(self.avg_temperature_label, 0, 2)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        # Tab widget for data and charts
        self.tab_widget = QTabWidget()
        
        # Data table tab
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure (bar)', 'Temperature (°C)'
        ])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.tab_widget.addTab(self.data_table, 'Equipment Data')
        
        # Charts tab
        charts_widget = QWidget()
        charts_layout = QHBoxLayout(charts_widget)
        
        # Bar chart for equipment types
        self.bar_chart_canvas = MatplotlibCanvas(self, width=5, height=4)
        charts_layout.addWidget(self.bar_chart_canvas)
        
        # Scatter plot for pressure vs temperature
        self.scatter_chart_canvas = MatplotlibCanvas(self, width=5, height=4)
        charts_layout.addWidget(self.scatter_chart_canvas)
        
        self.tab_widget.addTab(charts_widget, 'Visualizations')
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage('Ready')
        
    def upload_csv(self):
        """Handle CSV file selection and upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv)'
        )
        
        if file_path:
            self.statusBar().showMessage('Uploading file...')
            self.upload_btn.setEnabled(False)
            
            # Create and start upload thread
            self.upload_thread = UploadThread(file_path)
            self.upload_thread.upload_success.connect(self.on_upload_success)
            self.upload_thread.upload_error.connect(self.on_upload_error)
            self.upload_thread.start()
    
    def on_upload_success(self, response):
        """Handle successful upload"""
        self.statusBar().showMessage('File uploaded successfully!')
        self.upload_btn.setEnabled(True)
        
        # Extract data from response
        self.current_data = response.get('data', {})
        self.update_display()
        
        QMessageBox.information(self, 'Success', 'CSV file processed successfully!')
    
    def on_upload_error(self, error_msg):
        """Handle upload error"""
        self.statusBar().showMessage('Upload failed')
        self.upload_btn.setEnabled(True)
        QMessageBox.critical(self, 'Upload Error', error_msg)
    
    def sync_from_server(self):
        """Fetch latest upload history from server"""
        self.statusBar().showMessage('Syncing from server...')
        
        try:
            response = requests.get(f'{API_BASE_URL}/history/')
            
            if response.status_code == 200:
                data = response.json()
                history = data.get('history', [])
                
                if history:
                    # Load the most recent upload
                    self.current_data = history[0]
                    self.update_display()
                    self.statusBar().showMessage(f'Synced successfully! Loaded {len(history)} recent uploads.')
                    QMessageBox.information(self, 'Sync Complete', f'Loaded latest upload (ID: {self.current_data["id"]})')
                else:
                    self.statusBar().showMessage('No data available on server')
                    QMessageBox.information(self, 'Sync Complete', 'No uploads found on server')
            else:
                raise Exception('Failed to fetch data from server')
                
        except Exception as e:
            self.statusBar().showMessage('Sync failed')
            QMessageBox.critical(self, 'Sync Error', f'Failed to sync from server: {str(e)}')
    
    def update_display(self):
        """Update all display elements with current data"""
        if not self.current_data:
            return
        
        # Update statistics
        self.total_equipment_label.setText(f'Total Equipment: {self.current_data.get("total_equipment_count", 0)}')
        self.avg_pressure_label.setText(f'Avg Pressure: {self.current_data.get("average_pressure", 0):.2f} bar')
        self.avg_temperature_label.setText(f'Avg Temperature: {self.current_data.get("average_temperature", 0):.2f} °C')
        
        # Enable PDF download button
        self.download_pdf_btn.setEnabled(True)
        
        # Update data table
        self.populate_table()
        
        # Update charts
        self.update_charts()
    
    def populate_table(self):
        """Populate data table with equipment records"""
        equipment_records = self.current_data.get('equipment_records', [])
        
        self.data_table.setRowCount(len(equipment_records))
        
        for row, record in enumerate(equipment_records):
            self.data_table.setItem(row, 0, QTableWidgetItem(record.get('equipment_name', '')))
            self.data_table.setItem(row, 1, QTableWidgetItem(record.get('equipment_type', '')))
            self.data_table.setItem(row, 2, QTableWidgetItem(f"{record.get('flowrate', 0):.2f}"))
            self.data_table.setItem(row, 3, QTableWidgetItem(f"{record.get('pressure', 0):.2f}"))
            self.data_table.setItem(row, 4, QTableWidgetItem(f"{record.get('temperature', 0):.2f}"))
    
    def update_charts(self):
        """Update Matplotlib charts with current data"""
        # Update bar chart - Equipment type distribution
        self.bar_chart_canvas.axes.clear()
        type_dist = self.current_data.get('equipment_type_distribution_json', {})
        
        if type_dist:
            types = list(type_dist.keys())
            counts = list(type_dist.values())
            
            colors = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6', '#1abc9c']
            self.bar_chart_canvas.axes.bar(types, counts, color=colors[:len(types)])
            self.bar_chart_canvas.axes.set_xlabel('Equipment Type')
            self.bar_chart_canvas.axes.set_ylabel('Count')
            self.bar_chart_canvas.axes.set_title('Equipment Type Distribution')
            self.bar_chart_canvas.axes.tick_params(axis='x', rotation=45)
        
        self.bar_chart_canvas.figure.tight_layout()
        self.bar_chart_canvas.draw()
        
        # Update scatter plot - Pressure vs Temperature
        self.scatter_chart_canvas.axes.clear()
        equipment_records = self.current_data.get('equipment_records', [])
        
        if equipment_records:
            pressures = [r.get('pressure', 0) for r in equipment_records]
            temperatures = [r.get('temperature', 0) for r in equipment_records]
            
            self.scatter_chart_canvas.axes.scatter(pressures, temperatures, alpha=0.6, c='#2ecc71', s=50)
            self.scatter_chart_canvas.axes.set_xlabel('Pressure (bar)')
            self.scatter_chart_canvas.axes.set_ylabel('Temperature (°C)')
            self.scatter_chart_canvas.axes.set_title('Pressure vs Temperature Analysis')
            self.scatter_chart_canvas.axes.grid(True, alpha=0.3)
        
        self.scatter_chart_canvas.figure.tight_layout()
        self.scatter_chart_canvas.draw()
    
    def download_pdf(self):
        """Download PDF report for current upload"""
        if not self.current_data:
            QMessageBox.warning(self, 'No Data', 'No data available to generate report')
            return
        
        upload_id = self.current_data.get('id')
        
        try:
            self.statusBar().showMessage('Downloading PDF report...')
            
            response = requests.get(f'{API_BASE_URL}/report/{upload_id}/')
            
            if response.status_code == 200:
                # Save PDF file
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    'Save PDF Report',
                    f'equipment_report_{upload_id}.pdf',
                    'PDF Files (*.pdf)'
                )
                
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    
                    self.statusBar().showMessage('PDF downloaded successfully!')
                    QMessageBox.information(self, 'Success', f'PDF report saved to: {save_path}')
            else:
                raise Exception('Failed to generate PDF report')
                
        except Exception as e:
            self.statusBar().showMessage('PDF download failed')
            QMessageBox.critical(self, 'Download Error', f'Failed to download PDF: {str(e)}')


def main():
    """Main entry point for desktop application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ChemicalEquipmentVisualizer()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
