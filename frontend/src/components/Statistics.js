/**
 * Statistics Component
 * Displays summary statistics for uploaded equipment data
 */

import React from 'react';

const Statistics = ({ data, onDownloadPDF }) => {
  // Check if data is available
  if (!data) {
    return null;
  }

  return (
    <div className="card mb-4">
      <div className="card-header bg-success text-white">
        <h5 className="mb-0">Summary Statistics</h5>
      </div>
      <div className="card-body">
        <div className="row">
          <div className="col-md-3 mb-3">
            <div className="stat-box text-center p-3 border rounded">
              <h3 className="text-primary mb-0">{data.total_equipment_count}</h3>
              <p className="text-muted mb-0">Total Equipment</p>
            </div>
          </div>

          <div className="col-md-3 mb-3">
            <div className="stat-box text-center p-3 border rounded">
              <h3 className="text-info mb-0">{data.average_pressure.toFixed(2)}</h3>
              <p className="text-muted mb-0">Avg Pressure (bar)</p>
            </div>
          </div>

          <div className="col-md-3 mb-3">
            <div className="stat-box text-center p-3 border rounded">
              <h3 className="text-warning mb-0">{data.average_temperature.toFixed(2)}</h3>
              <p className="text-muted mb-0">Avg Temperature (°C)</p>
            </div>
          </div>

          <div className="col-md-3 mb-3">
            <div className="stat-box text-center p-3 border rounded">
              <button
                className="btn btn-danger btn-sm"
                onClick={() => onDownloadPDF(data.id)}
              >
                <i className="bi bi-file-pdf"></i> Download PDF
              </button>
              <p className="text-muted mb-0 mt-2">Generate Report</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
