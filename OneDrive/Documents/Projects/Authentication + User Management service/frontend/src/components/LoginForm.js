import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // ADD THIS
import { authAPI } from '../services/api';
import './LoginForm.css';

function LoginForm({ onLoginSuccess }) {
  const navigate = useNavigate();  // ADD THIS
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking...');

  // NEW: Check if backend is running
  React.useEffect(() => {
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/');
      if (response.ok) {
        setBackendStatus('✅ Connected');
      } else {
        setBackendStatus('❌ Not responding');
      }
    } catch (err) {
      setBackendStatus('❌ Cannot connect');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Validation
    if (!username.trim() || !password.trim()) {
      setError('Please fill in all fields');
      return;
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      // REAL API CALL
      console.log('Sending login request to FastAPI...');
      const response = await authAPI.login(username, password);
      
      console.log('Login successful!', response);
      
      // Show success
      alert(`Login successful! Welcome ${username}`);
      
      // Clear form
      setUsername('');
      setPassword('');
      
      // Call parent callback if provided
      if (onLoginSuccess) {
        onLoginSuccess(response);
      }
      
      // REDIRECT TO DASHBOARD - ADD THIS
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
      
    } catch (err) {
      // Handle API errors
      console.error('Login failed:', err);
      
      let errorMessage = 'Login failed';
      
      if (err.response) {
        // Server responded with error
        errorMessage = err.response.data?.detail || `Error: ${err.response.status}`;
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to server. Is FastAPI running?';
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: Test backend connection button
  const testBackendConnection = async () => {
    setIsLoading(true);
    try {
      const data = await authAPI.getDatabaseInfo();
      alert(`Backend is working! Database info:\n${JSON.stringify(data, null, 2)}`);
      setBackendStatus('✅ Connected and working');
    } catch (err) {
      alert(`Backend error: ${err.message}`);
      setBackendStatus('❌ Connection failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <h2>Login to Your Account</h2>
      
      {/* Backend Status Display */}
      <div className="backend-status">
        <p>Backend Status: <span className={`status ${backendStatus.includes('✅') ? 'connected' : 'disconnected'}`}>
          {backendStatus}
        </span></p>
        <button 
          type="button" 
          onClick={testBackendConnection}
          className="test-btn"
          disabled={isLoading}
        >
          Test Backend Connection
        </button>
      </div>
      
      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            disabled={isLoading}
          />
          <small className="password-hint">
            Must be at least 6 characters with uppercase, lowercase, number, and special character
          </small>
        </div>
        
        <button 
          type="submit" 
          className="submit-btn"
          disabled={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
        
        {/* Test Credentials */}
        <div className="demo-hint">
          <p><strong>Test with existing users:</strong></p>
          <div className="user-list">
            <div className="user-item">
              <span className="username">ivan</span>
              <span className="password-hint">(check users.csv for password)</span>
            </div>
            <div className="user-item">
              <span className="username">billy</span>
              <span className="password-hint">(use password you set)</span>
            </div>
          </div>
          <p className="api-info">
            API: <code>POST http://localhost:8000/login</code>
          </p>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;