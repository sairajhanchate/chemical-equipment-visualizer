/**
 * DataTable Component
 * Displays parsed equipment data in a responsive table format
 */

import React from 'react';

const DataTable = ({ data }) => {
  // Check if data is available
  if (!data || !data.equipment_records || data.equipment_records.length === 0) {
    return (
      <div className="card mb-4">
        <div className="card-header bg-secondary text-white">
          <h5 className="mb-0">Equipment Data</h5>
        </div>
        <div className="card-body">
          <p className="text-muted">No equipment data available. Upload a CSV file to see data.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card mb-4">
      <div className="card-header bg-secondary text-white">
        <h5 className="mb-0">Equipment Data ({data.equipment_records.length} records)</h5>
      </div>
      <div className="card-body">
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-dark">
              <tr>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure (bar)</th>
                <th>Temperature (°C)</th>
              </tr>
            </thead>
            <tbody>
              {data.equipment_records.map((record, index) => (
                <tr key={record.id || index}>
                  <td>{record.equipment_name}</td>
                  <td>
                    <span className="badge bg-info text-dark">
                      {record.equipment_type}
                    </span>
                  </td>
                  <td>{record.flowrate.toFixed(2)}</td>
                  <td>{record.pressure.toFixed(2)}</td>
                  <td>{record.temperature.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DataTable;
