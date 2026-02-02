/**
 * FileUpload Component
 * Handles CSV file selection and upload to backend
 */

import React, { useState } from 'react';

const FileUpload = ({ onUploadSuccess, onUploadError }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  /**
   * Handle file selection from input
   */
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    
    if (file) {
      // Validate file type
      if (!file.name.endsWith('.csv')) {
        onUploadError({ error: 'Please select a CSV file (.csv extension required)' });
        setSelectedFile(null);
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        onUploadError({ error: 'File size must be less than 5MB' });
        setSelectedFile(null);
        return;
      }
      
      setSelectedFile(file);
    }
  };

  /**
   * Handle file upload to backend
   */
  const handleUpload = async () => {
    if (!selectedFile) {
      onUploadError({ error: 'Please select a file first' });
      return;
    }

    setUploading(true);

    try {
      // Import API service dynamically to avoid circular dependencies
      const { uploadCSV } = await import('../services/api');
      const response = await uploadCSV(selectedFile);
      
      // Notify parent component of successful upload
      onUploadSuccess(response);
      
      // Reset file input
      setSelectedFile(null);
      document.getElementById('csvFileInput').value = '';
      
    } catch (error) {
      onUploadError(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h5 className="mb-0">Upload Equipment Data</h5>
      </div>
      <div className="card-body">
        <div className="mb-3">
          <label htmlFor="csvFileInput" className="form-label">
            Select CSV File
          </label>
          <input
            type="file"
            className="form-control"
            id="csvFileInput"
            accept=".csv"
            onChange={handleFileSelect}
            disabled={uploading}
          />
          <small className="form-text text-muted">
            CSV should contain columns: Equipment Name, Type, Flowrate, Pressure, Temperature
          </small>
        </div>

        {selectedFile && (
          <div className="alert alert-info mb-3">
            <strong>Selected file:</strong> {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
          </div>
        )}

        <button
          className="btn btn-success"
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
        >
          {uploading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Uploading...
            </>
          ) : (
            'Upload and Process'
          )}
        </button>
      </div>
    </div>
  );
};

export default FileUpload;
