import { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [currentProject, setCurrentProject] = useState(null);
  const [loading, setLoading] = useState(false);

  const value = {
    currentProject,
    setCurrentProject,
    loading,
    setLoading,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
