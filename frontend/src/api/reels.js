const API_BASE = 'http://localhost:8000/api/v1';

export const reelsApi = {
  generateReel: async (projectId, options = {}) => {
    const response = await fetch(`${API_BASE}/projects/${projectId}/reel/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(options)
    });
    if (!response.ok) throw new Error('Failed to generate reel');
    return response.json();
  },

  getReel: async (projectId) => {
    const response = await fetch(`${API_BASE}/projects/${projectId}/reel`);
    if (!response.ok) throw new Error('Failed to get reel');
    return response.json();
  },

  getReelUrl: (projectId) => {
    return `${API_BASE}/projects/${projectId}/reel/serve`;
  }
};
