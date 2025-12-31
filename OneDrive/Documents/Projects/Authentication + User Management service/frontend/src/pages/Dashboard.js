import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [dbInfo, setDbInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const username = authAPI.getUsername();

  useEffect(() => {
    // Check if user is authenticated
    if (!authAPI.isAuthenticated()) {
      navigate('/login');
      return;
    }
    
    // Fetch dashboard data
    fetchDashboardData();
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch protected data (tests if token is valid)
      const protectedData = await authAPI.getProtectedData();
      setUserData(protectedData);
      
      // Fetch database info
      const dbData = await authAPI.getDatabaseInfo();
      setDbInfo(dbData);
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      authAPI.logout();
      navigate('/login');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Welcome, {username}!</h1>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>
      
      <main className="dashboard-content">
        <div className="dashboard-grid">
          {/* User Info Card */}
          <div className="card">
            <h2>👤 Your Profile</h2>
            <div className="card-content">
              <p><strong>Username:</strong> {username}</p>
              <p><strong>Status:</strong> <span className="status-active">Active</span></p>
              <p><strong>Token Valid:</strong> {userData ? '✅ Yes' : '❌ No'}</p>
            </div>
          </div>
          
          {/* Database Info Card */}
          {dbInfo && (
            <div className="card">
              <h2>🗄️ Database Stats</h2>
              <div className="card-content">
                <p><strong>Total Users:</strong> {dbInfo.total_users}</p>
                <p><strong>Database:</strong> {dbInfo.database}</p>
                <p><strong>Status:</strong> <span className="status-good">Connected</span></p>
              </div>
            </div>
          )}
          
          {/* System Info Card */}
          <div className="card">
            <h2>⚙️ System Status</h2>
            <div className="card-content">
              <p><strong>Backend:</strong> FastAPI + SQLite</p>
              <p><strong>API URL:</strong> http://localhost:8000</p>
              <p><strong>Frontend:</strong> React + Axios</p>
              <p><strong>Authentication:</strong> JWT Tokens</p>
              <button 
                onClick={fetchDashboardData}
                className="btn-secondary"
              >
                Refresh Data
              </button>
            </div>
          </div>
          
          {/* Quick Actions Card */}
          <div className="card">
            <h2>🚀 Quick Actions</h2>
            <div className="card-content">
              <button 
                onClick={() => alert('Profile feature coming soon!')}
                className="btn-action"
              >
                View Profile
              </button>
              <button 
                onClick={() => alert('Change password feature coming soon!')}
                className="btn-action"
              >
                Change Password
              </button>
              <button 
                onClick={handleLogout}
                className="btn-action btn-logout-action"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
        
        {/* Token Debug Section (for development) */}
        <div className="debug-section">
          <h3>🔐 Token Debug Info</h3>
          <div className="token-info">
            <p><strong>Token Present:</strong> {authAPI.getToken() ? '✅ Yes' : '❌ No'}</p>
            <p><strong>Stored Username:</strong> {authAPI.getUsername() || 'None'}</p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;