import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectsApi } from '../api/projects';
import ProgressPanel from '../components/ProgressPanel';
import ContentPanel from '../components/ContentPanel';
import AIPanel from '../components/AIPanel';
import './ProjectWorkspace.css';

function ProjectWorkspace() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      const response = await projectsApi.getProject(projectId);
      setProject(response);
    } catch (error) {
      console.error('Failed to load project:', error);
      setError('Failed to load project');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (targetStatus) => {
    if (targetStatus) {
      try {
        await projectsApi.updateProject(projectId, { status: targetStatus });
      } catch (error) {
        console.error('Failed to update project status:', error);
      }
    }
    loadProject();
  };

  const handleStageClick = async (stageKey) => {
    try {
      await projectsApi.updateProject(projectId, { status: stageKey });
      loadProject();
    } catch (error) {
      console.error('Failed to update project status:', error);
    }
  };

  if (loading) {
    return <div className="workspace-loading">Loading project...</div>;
  }

  if (error) {
    return (
      <div className="workspace-error">
        <p className="workspace-error-text">{error}</p>
        <button onClick={() => navigate('/')} className="workspace-back-button" style={{ marginTop: '1rem' }}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  if (!project) {
    return <div className="workspace-error">Project not found</div>;
  }

  return (
    <div className="workspace">
      <div className="workspace-header">
        <div className="workspace-header-info">
          <h1>{project.title}</h1>
          <p>
            {project.topic} • {project.language} • {project.duration}s
          </p>
        </div>
        <button
          onClick={() => navigate('/')}
          className="workspace-back-button"
        >
          Back to Dashboard
        </button>
      </div>

      <div className="workspace-layout">
        <div className="workspace-panel-left">
          <ProgressPanel project={project} onStageClick={handleStageClick} />
        </div>

        <div className="workspace-panel-center">
          <ContentPanel project={project} onStatusChange={handleStatusChange} />
        </div>

        <div className="workspace-panel-right">
          <AIPanel project={project} />
        </div>
      </div>
    </div>
  );
}

export default ProjectWorkspace;
