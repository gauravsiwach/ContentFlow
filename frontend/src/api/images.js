import { apiClient } from './client';

export const imagesApi = {
  generateImages: async (projectId, userInstructions = null) => {
    const response = await apiClient.post(`/projects/${projectId}/images/generate`, {
      user_instructions: userInstructions
    });
    return response;
  },

  generateSceneImage: async (projectId, sceneId) => {
    const response = await apiClient.post(`/projects/${projectId}/images/scenes/${sceneId}/generate`);
    return response;
  },

  getImages: async (projectId) => {
    const response = await apiClient.get(`/projects/${projectId}/images`);
    return response;
  },

  refineImage: async (projectId, imageId, newPrompt) => {
    const response = await apiClient.post(`/projects/${projectId}/images/${imageId}/refine`, {
      new_prompt: newPrompt
    });
    return response;
  },

  approveImages: async (projectId) => {
    const response = await apiClient.post(`/projects/${projectId}/images/approve`);
    return response;
  }
};
