/**
 * API Service for Chemical Equipment Parameter Visualizer
 * Handles all HTTP requests to the Django backend
 */

import axios from 'axios';

// Base URL for backend API - adjust if backend runs on different port
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Create axios instance with default configuration
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload CSV file to backend for processing
 * @param {File} file - CSV file to upload
 * @returns {Promise} Response with processed data and statistics
 */
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('csv_file', file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Network error occurred' };
  }
};

/**
 * Fetch upload history (last 5 uploads)
 * @returns {Promise} Array of recent uploads with metadata
 */
export const getUploadHistory = async () => {
  try {
    const response = await apiClient.get('/history/');
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch upload history' };
  }
};

/**
 * Fetch details for a specific upload
 * @param {number} uploadId - ID of the upload to retrieve
 * @returns {Promise} Upload details with equipment records
 */
export const getUploadDetail = async (uploadId) => {
  try {
    const response = await apiClient.get(`/upload/${uploadId}/`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch upload details' };
  }
};

/**
 * Download PDF report for a specific upload
 * @param {number} uploadId - ID of the upload to generate report for
 * @returns {Promise} Blob containing PDF file
 */
export const downloadPDFReport = async (uploadId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/report/${uploadId}/`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `equipment_report_${uploadId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to download PDF report' };
  }
};

/**
 * Health check to verify backend connectivity
 * @returns {Promise} Health status response
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health/');
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Backend is not reachable' };
  }
};

export default {
  uploadCSV,
  getUploadHistory,
  getUploadDetail,
  downloadPDFReport,
  healthCheck,
};
