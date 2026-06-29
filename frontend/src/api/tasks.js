const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

export async function getTaskStatus(projectId, taskId) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/tasks/${taskId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch task status');
  }
  return response.json();
}

export function pollTaskStatus(projectId, taskId, interval = 2000, timeout = 300000) {
  let attempts = 0;
  const maxAttempts = timeout / interval;

  return new Promise((resolve, reject) => {
    const poll = async () => {
      attempts++;
      try {
        const task = await getTaskStatus(projectId, taskId);
        
        if (task.status === 'completed') {
          resolve(task);
          return;
        }
        
        if (task.status === 'failed') {
          reject(new Error(task.error_message || 'Task failed'));
          return;
        }
        
        if (attempts >= maxAttempts) {
          reject(new Error('Task polling timeout'));
          return;
        }
        
        // Continue polling
        setTimeout(poll, interval);
      } catch (error) {
        reject(error);
      }
    };
    
    poll();
  });
}
