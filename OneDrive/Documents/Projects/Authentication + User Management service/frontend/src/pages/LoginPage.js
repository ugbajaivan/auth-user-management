import React from 'react';
import LoginForm from '../components/LoginForm';
import './LoginPage.css';

function LoginPage() {
  return (
    <div className="login-page">
      <div className="login-left">
        <div className="welcome-content">
          <h1>Welcome Back!</h1>
          <p>
            Sign in to access your account and manage your authentication system.
            This is connected to your FastAPI backend with SQLite database.
          </p>
          <div className="features-list">
            <h3>What you can do:</h3>
            <ul>
              <li>✅ Access protected routes</li>
              <li>✅ Manage your profile</li>
              <li>✅ View database statistics</li>
              <li>✅ Test JWT authentication</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className="login-right">
        <LoginForm />
        <div className="signup-prompt">
          <p>Don't have an account? <a href="#register">Sign up here</a></p>
          <p className="backend-info">
            <small>
              Backend: FastAPI + SQLite | 
              API running on: <code>http://localhost:8000</code>
            </small>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;