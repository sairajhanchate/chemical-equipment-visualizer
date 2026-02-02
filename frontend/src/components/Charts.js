/**
 * Charts Component
 * Displays data visualizations using Chart.js
 * - Bar chart for equipment type distribution
 * - Scatter plot for Pressure vs Temperature
 */

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Scatter } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Charts = ({ data }) => {
  // Check if data is available
  if (!data || !data.equipment_records || data.equipment_records.length === 0) {
    return (
      <div className="alert alert-warning">
        No data available for visualization. Upload a CSV file to see charts.
      </div>
    );
  }

  /**
   * Prepare data for equipment type distribution bar chart
   */
  const prepareBarChartData = () => {
    const typeDistribution = data.equipment_type_distribution_json || {};
    
    return {
      labels: Object.keys(typeDistribution),
      datasets: [
        {
          label: 'Equipment Count',
          data: Object.values(typeDistribution),
          backgroundColor: [
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 99, 132, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
          ],
          borderColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  /**
   * Prepare data for pressure vs temperature scatter plot
   */
  const prepareScatterData = () => {
    const scatterPoints = data.equipment_records.map((record) => ({
      x: record.pressure,
      y: record.temperature,
    }));

    return {
      datasets: [
        {
          label: 'Pressure vs Temperature',
          data: scatterPoints,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          pointRadius: 5,
          pointHoverRadius: 7,
        },
      ],
    };
  };

  // Chart options
  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        font: {
          size: 16,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Count',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Equipment Type',
        },
      },
    },
  };

  const scatterChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Pressure vs Temperature Analysis',
        font: {
          size: 16,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Pressure (bar)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Temperature (°C)',
        },
      },
    },
  };

  return (
    <div className="row">
      {/* Bar Chart - Equipment Type Distribution */}
      <div className="col-md-6 mb-4">
        <div className="card">
          <div className="card-body">
            <Bar data={prepareBarChartData()} options={barChartOptions} />
          </div>
        </div>
      </div>

      {/* Scatter Plot - Pressure vs Temperature */}
      <div className="col-md-6 mb-4">
        <div className="card">
          <div className="card-body">
            <Scatter data={prepareScatterData()} options={scatterChartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Charts;
