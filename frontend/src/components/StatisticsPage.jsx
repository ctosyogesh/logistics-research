import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Database, Activity, Loader2, AlertCircle } from 'lucide-react';
import { statsService } from '../services/api';
import './StatisticsPage.css';

const StatisticsPage = () => {
  const [stats, setStats] = useState(null);
  const [health, setHealth] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadStatistics();
    loadHealth();
  }, []);

  const loadStatistics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await statsService.getStats();
      setStats(data);
    } catch (err) {
      setError('Failed to load statistics');
    } finally {
      setIsLoading(false);
    }
  };

  const loadHealth = async () => {
    try {
      const data = await statsService.healthCheck();
      setHealth(data);
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="loading-state">
        <Loader2 className="spin" size={32} />
        <p>Loading statistics...</p>
      </div>
    );
  }

  return (
    <div className="statistics-page">
      <div className="page-header">
        <h2>System Statistics</h2>
        <p>Overview of research activity and knowledge base metrics</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {health && (
        <div className="health-status">
          <Activity size={16} />
          <span className={health.status === 'healthy' ? 'status-healthy' : 'status-error'}>
            System {health.status}
          </span>
        </div>
      )}

      {stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon knowledge">
                <Database size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">{stats.knowledge_base?.total_entries || 0}</div>
                <div className="stat-label">Knowledge Entries</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon research">
                <BarChart3 size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">{stats.research_jobs?.total || 0}</div>
                <div className="stat-label">Total Research Jobs</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon success">
                <TrendingUp size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">{stats.research_jobs?.success_rate || '0%'}</div>
                <div className="stat-label">Success Rate</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon tags">
                <Database size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">{stats.knowledge_base?.total_tags || 0}</div>
                <div className="stat-label">Unique Tags</div>
              </div>
            </div>
          </div>

          <div className="detailed-stats">
            <div className="stat-section">
              <h3>Research Jobs Breakdown</h3>
              <div className="breakdown-grid">
                <div className="breakdown-item">
                  <span className="breakdown-label">Completed</span>
                  <span className="breakdown-value success">
                    {stats.research_jobs?.completed || 0}
                  </span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-label">Failed</span>
                  <span className="breakdown-value error">
                    {stats.research_jobs?.failed || 0}
                  </span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-label">Total</span>
                  <span className="breakdown-value">
                    {stats.research_jobs?.total || 0}
                  </span>
                </div>
              </div>
            </div>

            {stats.knowledge_base?.top_tags && stats.knowledge_base.top_tags.length > 0 && (
              <div className="stat-section">
                <h3>Top Research Topics</h3>
                <div className="tags-chart">
                  {stats.knowledge_base.top_tags.map((item, idx) => (
                    <div key={idx} className="tag-bar">
                      <div className="tag-info">
                        <span className="tag-name">{item.tag}</span>
                        <span className="tag-count">{item.count}</span>
                      </div>
                      <div className="tag-progress">
                        <div
                          className="tag-progress-fill"
                          style={{
                            width: `${(item.count / stats.knowledge_base.top_tags[0].count) * 100}%`
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {stats.knowledge_base?.last_updated && (
              <div className="stat-section">
                <h3>Knowledge Base Activity</h3>
                <p className="last-updated">
                  Last updated: {new Date(stats.knowledge_base.last_updated).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default StatisticsPage;
