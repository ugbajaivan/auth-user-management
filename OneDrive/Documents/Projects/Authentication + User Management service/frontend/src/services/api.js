import axios from 'axios';

// Create axios instance for your FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000', // Your FastAPI URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API functions
export const authAPI = {
  // Register new user
  register: async (username, password) => {
    const response = await api.post('/signup', { username, password });
    return response.data;
  },

  // Login user
  login: async (username, password) => {
    const response = await api.post('/login', { username, password });
    
    // Save token and username to localStorage
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('username', username);
    }
    
    return response.data;
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  },

  // Get protected data (tests if token is valid)
  getProtectedData: async () => {
    const response = await api.get('/protected');
    return response.data;
  },

  // Get database info
  getDatabaseInfo: async () => {
    const response = await api.get('/database-info');
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  // Get current token
  getToken: () => {
    return localStorage.getItem('token');
  },

  // Get current username
  getUsername: () => {
    return localStorage.getItem('username');
  }
};

// Test/debug endpoints
export const debugAPI = {
  testToken: async (token) => {
    const response = await api.post('/test-token-debug', null, {
      params: { token }
    });
    return response.data;
  },

  testJWT: async () => {
    const response = await api.get('/test-jwt-direct');
    return response.data;
  }
};

export default api;