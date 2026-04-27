import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const researchService = {
  /**
   * Conduct new research
   */
  conductResearch: async (query, depth = 'standard', saveToKnowledgeBase = true) => {
    const response = await api.post('/api/research', {
      query,
      depth,
      save_to_knowledge_base: saveToKnowledgeBase,
    });
    return response.data;
  },

  /**
   * Get research status
   */
  getResearchStatus: async (researchId) => {
    const response = await api.get(`/api/research/${researchId}/status`);
    return response.data;
  },
};

export const knowledgeService = {
  /**
   * List knowledge base entries
   */
  listEntries: async (limit = 20, tag = null) => {
    const params = { limit };
    if (tag) params.tag = tag;
    const response = await api.get('/api/knowledge', { params });
    return response.data;
  },

  /**
   * Get specific knowledge entry
   */
  getEntry: async (entryId) => {
    const response = await api.get(`/api/knowledge/${entryId}`);
    return response.data;
  },

  /**
   * Delete knowledge entry
   */
  deleteEntry: async (entryId) => {
    const response = await api.delete(`/api/knowledge/${entryId}`);
    return response.data;
  },
};

export const statsService = {
  /**
   * Get system statistics
   */
  getStats: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },

  /**
   * Health check
   */
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
