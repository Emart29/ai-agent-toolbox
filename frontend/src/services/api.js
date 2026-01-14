import axios from 'axios';

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // Check if we're in production and have a production API URL
  if (import.meta.env.PROD && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // Development fallback
  return import.meta.env.VITE_API_URL || 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

console.log(`🔗 API Base URL: ${API_BASE_URL}`);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 
    'Content-Type': 'application/json' 
  },
  timeout: 120000, // 2 minutes timeout for long-running agent queries
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`📡 API Request: ${config.method.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging and error handling
api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`✅ API Response: ${response.config.method.toUpperCase()} ${response.config.url}`);
    }
    return response;
  },
  (error) => {
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    console.error('❌ API Error:', errorMessage);
    
    // Handle specific error cases
    if (error.response?.status === 500) {
      console.error('Server error - check backend logs');
    } else if (error.response?.status === 404) {
      console.error('Endpoint not found');
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - agent query took too long');
    } else if (error.code === 'ERR_NETWORK') {
      console.error('Network error - is the backend running?');
    }
    
    return Promise.reject(error);
  }
);

export const systemAPI = {
  getHealth: () => api.get('/system/health'),
  getInfo: () => api.get('/system/info'),
};

export const agentAPI = {
  query: (data) => api.post('/agent/query', data),
  getTools: () => api.get('/agent/tools'),
  getConversation: (id) => api.get(`/agent/conversation/${id}`),
};

export default api;