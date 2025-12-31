import React from 'react';
import { Link } from 'react-router-dom';
import LoginForm from '../components/LoginForm';

function LoginPage() {
  const handleLoginSuccess = (response) => {
    console.log('Login successful:', response);
    // Redirect will be handled by the form
  };

  return (
    <div className="page-container">
      <div className="auth-container">
        <h1>Welcome Back!</h1>
        <p className="subtitle">
          Sign in to access your account and manage your authentication system. 
          This is connected to your FastAPI backend with SQLite database.
        </p>
        
        <div className="features">
          <p><strong>What you can do:</strong></p>
          <ul>
            <li>✓ Access protected routes</li>
            <li>✓ Manage your profile</li>
            <li>✓ View database statistics</li>
            <li>✓ Test JWT authentication</li>
          </ul>
        </div>
        
        <LoginForm onLoginSuccess={handleLoginSuccess} />
        
        <div className="auth-links">
          <p>Don't have an account? <Link to="/signup">Sign up here</Link></p>
          <p><Link to="/">← Back to Home</Link></p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;