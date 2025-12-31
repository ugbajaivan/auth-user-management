import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="app-container">
          <header className="app-header">
            <h1>🔐 Auth & User Management System</h1>
            <p className="app-subtitle">FastAPI + React + SQLite Authentication</p>
          </header>
          
          <main className="app-main">
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignUpPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/" element={<Navigate to="/login" replace />} />
            </Routes>
          </main>
          
          <footer className="app-footer">
            <p>Backend: FastAPI + SQLite | API running on: http://localhost:8000</p>
          </footer>
        </div>
      </div>
    </Router>
  );
}

export default App;