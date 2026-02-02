/**
 * Main Application Component
 * Chemical Equipment Parameter Visualizer - Web Frontend
 * FOSSEE Internship Technical Screening Project
 */

import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import Statistics from './components/Statistics';
import { downloadPDFReport, getUploadHistory } from './services/api';
import './App.css';

function App() {
  const [currentData, setCurrentData] = useState(null);
  const [uploadHistory, setUploadHistory] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(false);

  /**
   * Fetch upload history on component mount
   */
  useEffect(() => {
    fetchUploadHistory();
  }, []);

  /**
   * Fetch the last 5 uploads from backend
   */
  const fetchUploadHistory = async () => {
    setLoading(true);
    try {
      const response = await getUploadHistory();
      setUploadHistory(response.history || []);
    } catch (err) {
      console.error('Failed to fetch upload history:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle successful CSV upload
   */
  const handleUploadSuccess = (response) => {
    setCurrentData(response.data);
    setSuccess('CSV file processed successfully!');
    setError(null);
    
    // Refresh upload history
    fetchUploadHistory();
    
    // Clear success message after 5 seconds
    setTimeout(() => setSuccess(null), 5000);
  };

  /**
   * Handle upload errors
   */
  const handleUploadError = (err) => {
    setError(err.error || 'An error occurred during upload');
    setSuccess(null);
    
    // Clear error message after 8 seconds
    setTimeout(() => setError(null), 8000);
  };

  /**
   * Handle PDF download
   */
  const handleDownloadPDF = async (uploadId) => {
    try {
      setSuccess('Generating PDF report...');
      await downloadPDFReport(uploadId);
      setSuccess('PDF report downloaded successfully!');
      setTimeout(() => setSuccess(null), 5000);
    } catch (err) {
      setError('Failed to download PDF report');
      setTimeout(() => setError(null), 8000);
    }
  };

  /**
   * Load data from upload history
   */
  const loadHistoricalData = (historyItem) => {
    setCurrentData(historyItem);
    setSuccess('Historical data loaded successfully');
    setTimeout(() => setSuccess(null), 3000);
  };

  return (
    <div className="App">
      {/* Header */}
      <nav className="navbar navbar-dark bg-dark">
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1">
            Chemical Equipment Parameter Visualizer
          </span>
          <span className="badge bg-light text-dark">FOSSEE Internship Project</span>
        </div>
      </nav>

      <div className="container mt-4">
        {/* Alert Messages */}
        {success && (
          <div className="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Success!</strong> {success}
            <button
              type="button"
              className="btn-close"
              onClick={() => setSuccess(null)}
              aria-label="Close"
            ></button>
          </div>
        )}

        {error && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error!</strong> {error}
            <button
              type="button"
              className="btn-close"
              onClick={() => setError(null)}
              aria-label="Close"
            ></button>
          </div>
        )}

        {/* File Upload Section */}
        <FileUpload
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
        />

        {/* Statistics Section */}
        {currentData && (
          <Statistics data={currentData} onDownloadPDF={handleDownloadPDF} />
        )}

        {/* Charts Section */}
        <Charts data={currentData} />

        {/* Data Table Section */}
        <DataTable data={currentData} />

        {/* Upload History Section */}
        {uploadHistory.length > 0 && (
          <div className="card mb-4">
            <div className="card-header bg-info text-white">
              <h5 className="mb-0">Recent Uploads</h5>
            </div>
            <div className="card-body">
              <div className="table-responsive">
                <table className="table table-sm">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Upload Date</th>
                      <th>Equipment Count</th>
                      <th>Avg Pressure</th>
                      <th>Avg Temperature</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {uploadHistory.map((item) => (
                      <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                        <td>{item.total_equipment_count}</td>
                        <td>{item.average_pressure.toFixed(2)} bar</td>
                        <td>{item.average_temperature.toFixed(2)} °C</td>
                        <td>
                          <button
                            className="btn btn-sm btn-outline-primary me-2"
                            onClick={() => loadHistoricalData(item)}
                          >
                            View
                          </button>
                          <button
                            className="btn btn-sm btn-outline-danger"
                            onClick={() => handleDownloadPDF(item.id)}
                          >
                            PDF
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-muted py-4">
          <small>
            Chemical Equipment Parameter Visualizer | FOSSEE Internship Technical Screening
          </small>
        </footer>
      </div>
    </div>
  );
}

export default App;
