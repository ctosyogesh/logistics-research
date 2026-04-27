import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Search, Database, BarChart3, BookOpen } from 'lucide-react';
import ResearchPage from './components/ResearchPage';
import KnowledgeBasePage from './components/KnowledgeBasePage';
import StatisticsPage from './components/StatisticsPage';
import './App.css';

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: Search, label: 'Research' },
    { path: '/knowledge', icon: Database, label: 'Knowledge Base' },
    { path: '/statistics', icon: BarChart3, label: 'Statistics' },
  ];
  
  return (
    <nav className="nav-container">
      <div className="nav-brand">
        <BookOpen className="brand-icon" />
        <h1>Logistics Research Agent</h1>
      </div>
      <div className="nav-links">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ResearchPage />} />
            <Route path="/knowledge" element={<KnowledgeBasePage />} />
            <Route path="/statistics" element={<StatisticsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
