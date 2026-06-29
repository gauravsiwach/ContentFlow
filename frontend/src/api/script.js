const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

export async function getScript(projectId) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/script`);
  if (!response.ok) {
    if (response.status === 404) return null;
    throw new Error('Failed to fetch script');
  }
  return response.json();
}

export async function generateScript(projectId) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/script/generate`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to generate script');
  }
  return response.json();
}

export async function updateScript(projectId, content) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/script`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  });
  if (!response.ok) {
    throw new Error('Failed to update script');
  }
  return response.json();
}

export async function refineScript(projectId, instructions) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/script/refine`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ instructions }),
  });
  if (!response.ok) {
    throw new Error('Failed to refine script');
  }
  return response.json();
}

export async function approveScript(projectId) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/script/approve`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to approve script');
  }
  return response.json();
}
