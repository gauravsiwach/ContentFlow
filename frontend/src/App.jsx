import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ProjectWorkspace from './pages/ProjectWorkspace';
import { AppProvider } from './context/AppContext';
import './App.css';

function App() {
  return (
    <AppProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/project/:projectId" element={<ProjectWorkspace />} />
        </Routes>
      </Router>
    </AppProvider>
  );
}

export default App;
