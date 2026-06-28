import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectsApi } from '../api/projects';
import NewProjectForm from '../components/NewProjectForm';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewProjectForm, setShowNewProjectForm] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await projectsApi.getProjects();
      setProjects(response.projects || []);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = () => {
    setShowNewProjectForm(true);
  };

  const handleProjectCreated = (project) => {
    loadProjects();
    navigate(`/project/${project.id}`);
  };

  const handleProjectClick = (projectId) => {
    navigate(`/project/${projectId}`);
  };

  const handleDeleteProject = async (projectId, event) => {
    event.stopPropagation();
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await projectsApi.deleteProject(projectId);
        loadProjects();
      } catch (error) {
        console.error('Failed to delete project:', error);
        alert('Failed to delete project');
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status) => {
    const colors = {
      draft: '#9ca3af',
      script_generated: '#3b82f6',
      script_approved: '#10b981',
      scenes_generated: '#3b82f6',
      scenes_approved: '#10b981',
      images_generated: '#3b82f6',
      images_approved: '#10b981',
      voice_generated: '#3b82f6',
      voice_approved: '#10b981',
      reel_generated: '#3b82f6',
      completed: '#10b981',
    };
    return colors[status] || '#9ca3af';
  };

  if (loading) {
    return <div className="dashboard-loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      {showNewProjectForm && (
        <NewProjectForm
          onClose={() => setShowNewProjectForm(false)}
          onSuccess={handleProjectCreated}
        />
      )}
      
      <div className="dashboard-header">
        <h1 className="dashboard-title">ContentFlow Dashboard</h1>
        <button
          onClick={handleCreateProject}
          className="dashboard-button"
        >
          + New Project
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="dashboard-empty">
          <p className="dashboard-empty-text">No projects yet</p>
          <p className="dashboard-empty-subtext">Click "New Project" to get started</p>
        </div>
      ) : (
        <div className="dashboard-grid">
          {projects.map((project) => (
            <div
              key={project.id}
              onClick={() => handleProjectClick(project.id)}
              className="dashboard-card"
            >
              <h3 className="dashboard-card-title">{project.title}</h3>
              <p className="dashboard-card-topic">{project.topic}</p>
              <div className="dashboard-card-meta">
                <span
                  className="dashboard-card-status"
                  style={{ backgroundColor: getStatusColor(project.status) }}
                >
                  {project.status.replace('_', ' ')}
                </span>
                <span className="dashboard-card-date">{formatDate(project.created_at)}</span>
              </div>
              <button
                onClick={(e) => handleDeleteProject(project.id, e)}
                className="dashboard-card-delete"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
