import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

function Dashboard() {
  const [healthStatus, setHealthStatus] = useState('Checking...');
  const [dbStatus, setDbStatus] = useState('Checking...');
  const [storageStatus, setStorageStatus] = useState('Checking...');

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const data = await apiClient.get('/health');
      setHealthStatus(data.status);
      setDbStatus(data.database);
      setStorageStatus(data.storage);
    } catch (error) {
      setHealthStatus('Error');
      setDbStatus('Error');
      setStorageStatus('Error');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>ContentFlow Dashboard</h1>
      <div style={{ marginTop: '2rem' }}>
        <h2>System Status</h2>
        <div style={{ display: 'flex', gap: '2rem', marginTop: '1rem' }}>
          <div>
            <strong>API Status:</strong> {healthStatus}
          </div>
          <div>
            <strong>Database:</strong> {dbStatus}
          </div>
          <div>
            <strong>Storage:</strong> {storageStatus}
          </div>
        </div>
      </div>
      <div style={{ marginTop: '2rem' }}>
        <button 
          onClick={checkHealth}
          style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
        >
          Refresh Status
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
