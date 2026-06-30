import { apiClient } from './client';

export const voicesApi = {
  generateVoices: async (projectId, userInstructions = null) => {
    const response = await apiClient.post(`/projects/${projectId}/voices/generate`, {
      user_instructions: userInstructions
    });
    return response;
  },

  generateSceneVoice: async (projectId, sceneId) => {
    const response = await apiClient.post(`/projects/${projectId}/voices/scenes/${sceneId}/generate`);
    return response;
  },

  getVoices: async (projectId) => {
    const response = await apiClient.get(`/projects/${projectId}/voices`);
    return response;
  },

  refineVoice: async (projectId, voiceId, newText) => {
    const response = await apiClient.post(`/projects/${projectId}/voices/${voiceId}/refine`, {
      new_text: newText
    });
    return response;
  },

  approveVoices: async (projectId) => {
    const response = await apiClient.post(`/projects/${projectId}/voices/approve`);
    return response;
  }
};
