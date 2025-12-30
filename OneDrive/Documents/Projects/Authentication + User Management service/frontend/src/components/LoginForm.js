// Step 1: Import React and useState hook
import React, { useState } from 'react';
import './LoginForm.css'; // We'll create this next

// Step 2: Create the LoginForm component
function LoginForm() {
  // Step 3: Create state variables for form inputs
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Step 4: Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent page refresh
    
    // Basic validation
    if (!username || !password) {
      setError('Please fill in all fields');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    // Step 5: Simulate API call (we'll connect to real API later)
    console.log('Attempting login with:', { username, password });
    
    // Simulate API delay
    setTimeout(() => {
      if (username === 'demo' && password === 'demo123') {
        alert(`Login successful! Welcome ${username}`);
        // Clear form
        setUsername('');
        setPassword('');
      } else {
        setError('Invalid credentials. Try: demo / demo123');
      }
      setIsLoading(false);
    }, 1000);
  };

  // Step 6: Return the JSX (HTML-like structure)
  return (
    <div className="login-form-container">
      <h2>Login to Your Account</h2>
      
      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="login-form">
        {/* Username Field */}
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
        
        {/* Password Field */}
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
        </div>
        
        {/* Submit Button */}
        <button 
          type="submit" 
          className="submit-btn"
          disabled={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
        
        {/* Demo Credentials Hint */}
        <div className="demo-hint">
          <p><strong>Demo credentials:</strong></p>
          <p>Username: <code>demo</code></p>
          <p>Password: <code>demo123</code></p>
        </div>
      </form>
    </div>
  );
}

// Step 7: Export the component
export default LoginForm;