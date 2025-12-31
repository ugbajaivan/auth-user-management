import React from 'react';
import { Link } from 'react-router-dom';
import SignUpForm from '../components/SignUpForm';

function SignUpPage() {
  return (
    <div className="page-container">
      <div className="auth-container">
        <h1>Join Our Authentication System</h1>
        <p className="subtitle">
          Create your account to access protected routes, manage your profile, 
          and test JWT authentication with our FastAPI backend.
        </p>
        
        <div className="features">
          <h3>What you'll get:</h3>
          <ul>
            <li>✓ Secure JWT-based authentication</li>
            <li>✓ SQLite database storage</li>
            <li>✓ Protected routes and APIs</li>
            <li>✓ Profile management</li>
            <li>✓ Database statistics</li>
            <li>✓ Real-time API testing</li>
          </ul>
        </div>
        
        <SignUpForm />
        
        <div className="auth-links">
          <p>
            Already have an account? <Link to="/login">Sign in here</Link>
          </p>
          <p>
            <Link to="/">← Back to Home</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default SignUpPage;