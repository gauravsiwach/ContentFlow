import { apiClient } from './client';

export const projectsApi = {
  createProject: async (projectData) => {
    return await apiClient.post('/projects', projectData);
  },

  getProjects: async (skip = 0, limit = 100) => {
    return await apiClient.get(`/projects?skip=${skip}&limit=${limit}`);
  },

  getProject: async (projectId) => {
    return await apiClient.get(`/projects/${projectId}`);
  },

  deleteProject: async (projectId) => {
    return await apiClient.delete(`/projects/${projectId}`);
  },

  getProjectStatus: async (projectId) => {
    return await apiClient.get(`/projects/${projectId}/status`);
  },

  updateProject: async (projectId, projectData) => {
    return await apiClient.put(`/projects/${projectId}`, projectData);
  },
};
