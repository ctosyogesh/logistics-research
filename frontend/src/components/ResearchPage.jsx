import React, { useState } from 'react';
import { Search, Loader2, CheckCircle, AlertCircle, Download, Save } from 'lucide-react';
import { researchService } from '../services/api';
import './ResearchPage.css';

const ResearchPage = () => {
  const [query, setQuery] = useState('');
  const [depth, setDepth] = useState('standard');
  const [saveToKB, setSaveToKB] = useState(true);
  const [isResearching, setIsResearching] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a research query');
      return;
    }

    setIsResearching(true);
    setError(null);
    setResult(null);

    try {
      const response = await researchService.conductResearch(query, depth, saveToKB);
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to conduct research. Please try again.');
    } finally {
      setIsResearching(false);
    }
  };

  const downloadReport = () => {
    if (!result?.full_report) return;
    
    const blob = new Blob([result.full_report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research_${result.research_id}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const exampleQueries = [
    "What are the latest trends in autonomous delivery vehicles?",
    "How is blockchain technology transforming supply chain transparency?",
    "What are the best practices for last-mile delivery optimization?",
    "How are AI and machine learning being used in warehouse automation?",
    "What is the impact of sustainability regulations on logistics operations?"
  ];

  return (
    <div className="research-page">
      <div className="page-header">
        <h2>Autonomous Research Agent</h2>
        <p>Ask any logistics-related question and get comprehensive, AI-powered research</p>
      </div>

      <form onSubmit={handleSubmit} className="research-form">
        <div className="form-group">
          <label htmlFor="query">Research Query</label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your logistics research question..."
            rows={4}
            disabled={isResearching}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="depth">Research Depth</label>
            <select
              id="depth"
              value={depth}
              onChange={(e) => setDepth(e.target.value)}
              disabled={isResearching}
            >
              <option value="quick">Quick (3 sources)</option>
              <option value="standard">Standard (5 sources)</option>
              <option value="comprehensive">Comprehensive (8+ sources)</option>
            </select>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={saveToKB}
                onChange={(e) => setSaveToKB(e.target.checked)}
                disabled={isResearching}
              />
              <span>Save to Knowledge Base</span>
            </label>
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isResearching || !query.trim()}
        >
          {isResearching ? (
            <>
              <Loader2 className="spin" size={18} />
              Researching...
            </>
          ) : (
            <>
              <Search size={18} />
              Conduct Research
            </>
          )}
        </button>
      </form>

      {!result && !isResearching && (
        <div className="example-queries">
          <h3>Example Queries</h3>
          <div className="query-list">
            {exampleQueries.map((example, idx) => (
              <button
                key={idx}
                className="query-example"
                onClick={() => setQuery(example)}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {isResearching && (
        <div className="research-progress">
          <div className="progress-indicator">
            <Loader2 className="spin" size={32} />
            <p>AI agents are researching your query...</p>
            <div className="progress-steps">
              <div className="step">🔍 Gathering information from web sources</div>
              <div className="step">🧠 Analyzing and synthesizing data</div>
              <div className="step">✅ Verifying accuracy and quality</div>
              <div className="step">📝 Generating comprehensive report</div>
            </div>
          </div>
        </div>
      )}

      {result && (
        <div className="research-results">
          <div className="result-header">
            <div className="header-left">
              <CheckCircle className="success-icon" size={24} />
              <div>
                <h3>Research Complete</h3>
                <p className="result-meta">
                  {new Date(result.timestamp).toLocaleString()} • {result.research_id}
                </p>
              </div>
            </div>
            <div className="header-actions">
              {result.saved_to_kb && (
                <span className="saved-badge">
                  <Save size={14} />
                  Saved to KB
                </span>
              )}
              <button onClick={downloadReport} className="btn btn-secondary">
                <Download size={16} />
                Download Report
              </button>
            </div>
          </div>

          <div className="result-section">
            <h4>Summary</h4>
            <div className="summary-content">
              {result.summary}
            </div>
          </div>

          {result.key_findings && result.key_findings.length > 0 && (
            <div className="result-section">
              <h4>Key Findings</h4>
              <ul className="findings-list">
                {result.key_findings.map((finding, idx) => (
                  <li key={idx}>{finding}</li>
                ))}
              </ul>
            </div>
          )}

          {result.sources && result.sources.length > 0 && (
            <div className="result-section">
              <h4>Sources Consulted ({result.sources.length})</h4>
              <div className="sources-list">
                {result.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    <span className="source-number">{idx + 1}</span>
                    <span className="source-title">{source.title}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.full_report && (
            <div className="result-section">
              <h4>Full Report</h4>
              <div className="full-report">
                <pre>{result.full_report}</pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResearchPage;
