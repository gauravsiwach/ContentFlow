import { apiClient } from './client';

export const scenesApi = {
  generateScenes: async (projectId, userInstructions = null) => {
    const response = await apiClient.post(`/projects/${projectId}/scenes/generate`, {
      user_instructions: userInstructions
    });
    return response;
  },

  getScenes: async (projectId) => {
    const response = await apiClient.get(`/projects/${projectId}/scenes`);
    return response;
  },

  updateScene: async (projectId, sceneId, updateData) => {
    const response = await apiClient.put(`/projects/${projectId}/scenes/${sceneId}`, updateData);
    return response;
  },

  refineScenes: async (projectId, instructions) => {
    const response = await apiClient.post(`/projects/${projectId}/scenes/refine`, {
      instructions
    });
    return response;
  },

  approveScenes: async (projectId) => {
    const response = await apiClient.post(`/projects/${projectId}/scenes/approve`);
    return response;
  }
};
