import React, { useState, useEffect } from 'react';
import { Database, Search, Tag, Calendar, Trash2, Eye, Loader2, AlertCircle } from 'lucide-react';
import { knowledgeService } from '../services/api';
import './KnowledgeBasePage.css';

const KnowledgeBasePage = () => {
  const [entries, setEntries] = useState([]);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterTag, setFilterTag] = useState(null);

  useEffect(() => {
    loadEntries();
  }, [filterTag]);

  const loadEntries = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await knowledgeService.listEntries(20, filterTag);
      setEntries(data);
    } catch (err) {
      setError('Failed to load knowledge base entries');
    } finally {
      setIsLoading(false);
    }
  };

  const viewEntry = async (entryId) => {
    try {
      const data = await knowledgeService.getEntry(entryId);
      setSelectedEntry(data);
    } catch (err) {
      setError('Failed to load entry details');
    }
  };

  const deleteEntry = async (entryId) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;
    
    try {
      await knowledgeService.deleteEntry(entryId);
      setEntries(entries.filter(e => e.id !== entryId));
      if (selectedEntry?.id === entryId) {
        setSelectedEntry(null);
      }
    } catch (err) {
      setError('Failed to delete entry');
    }
  };

  const closeModal = () => {
    setSelectedEntry(null);
  };

  const allTags = [...new Set(entries.flatMap(e => e.tags || []))];

  return (
    <div className="knowledge-page">
      <div className="page-header">
        <h2>Knowledge Base</h2>
        <p>Browse and search through your saved research findings</p>
      </div>

      <div className="kb-controls">
        <div className="tag-filters">
          <button
            className={`tag-filter ${!filterTag ? 'active' : ''}`}
            onClick={() => setFilterTag(null)}
          >
            All
          </button>
          {allTags.map(tag => (
            <button
              key={tag}
              className={`tag-filter ${filterTag === tag ? 'active' : ''}`}
              onClick={() => setFilterTag(tag)}
            >
              <Tag size={12} />
              {tag}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {isLoading ? (
        <div className="loading-state">
          <Loader2 className="spin" size={32} />
          <p>Loading knowledge base...</p>
        </div>
      ) : entries.length === 0 ? (
        <div className="empty-state">
          <Database size={48} />
          <h3>No entries found</h3>
          <p>Start by conducting research and saving results to the knowledge base</p>
        </div>
      ) : (
        <div className="entries-grid">
          {entries.map((entry) => (
            <div key={entry.id} className="entry-card">
              <div className="entry-header">
                <h3>{entry.query}</h3>
                <div className="entry-actions">
                  <button
                    onClick={() => viewEntry(entry.id)}
                    className="btn-icon"
                    title="View details"
                  >
                    <Eye size={16} />
                  </button>
                  <button
                    onClick={() => deleteEntry(entry.id)}
                    className="btn-icon delete"
                    title="Delete"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              
              <p className="entry-summary">{entry.summary}</p>
              
              <div className="entry-footer">
                <div className="entry-tags">
                  {entry.tags?.map(tag => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="entry-date">
                  <Calendar size={12} />
                  {new Date(entry.timestamp).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedEntry && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedEntry.query}</h2>
              <button onClick={closeModal} className="modal-close">×</button>
            </div>
            
            <div className="modal-body">
              <div className="modal-section">
                <h4>Summary</h4>
                <p>{selectedEntry.summary}</p>
              </div>

              {selectedEntry.key_findings && selectedEntry.key_findings.length > 0 && (
                <div className="modal-section">
                  <h4>Key Findings</h4>
                  <ul>
                    {selectedEntry.key_findings.map((finding, idx) => (
                      <li key={idx}>{finding}</li>
                    ))}
                  </ul>
                </div>
              )}

              {selectedEntry.sources && selectedEntry.sources.length > 0 && (
                <div className="modal-section">
                  <h4>Sources</h4>
                  <ol className="sources-list">
                    {selectedEntry.sources.map((source, idx) => (
                      <li key={idx}>{source.title}</li>
                    ))}
                  </ol>
                </div>
              )}

              {selectedEntry.full_report && (
                <div className="modal-section">
                  <h4>Full Report</h4>
                  <pre className="full-report-text">{selectedEntry.full_report}</pre>
                </div>
              )}

              <div className="modal-meta">
                <span>Research ID: {selectedEntry.id}</span>
                <span>Created: {new Date(selectedEntry.timestamp).toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KnowledgeBasePage;
