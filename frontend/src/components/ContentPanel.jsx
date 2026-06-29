import './ContentPanel.css';
import ScriptStage from './ScriptStage';

function ContentPanel({ project, onStatusChange }) {
  const getStageContent = () => {
    switch (project.status) {
      case 'draft':
        return {
          title: 'Script Generation',
          message: 'Ready to generate script',
          description: 'Click the button below to start generating the script for your project.',
          action: 'Generate Script',
        };
      case 'script_generated':
        return {
          title: 'Script Review',
          message: 'Script generated',
          description: 'Review the generated script and approve or refine it.',
          action: 'Approve Script',
        };
      case 'script_approved':
        return {
          title: 'Scene Generation',
          message: 'Script approved',
          description: 'Ready to generate scene breakdown.',
          action: 'Generate Scenes',
        };
      case 'scenes_generated':
        return {
          title: 'Scene Review',
          message: 'Scenes generated',
          description: 'Review the generated scenes and approve or refine them.',
          action: 'Approve Scenes',
        };
      case 'scenes_approved':
        return {
          title: 'Image Generation',
          message: 'Scenes approved',
          description: 'Ready to generate images for each scene.',
          action: 'Generate Images',
        };
      case 'images_generated':
        return {
          title: 'Image Review',
          message: 'Images generated',
          description: 'Review the generated images and approve or refine them.',
          action: 'Approve Images',
        };
      case 'images_approved':
        return {
          title: 'Voice Generation',
          message: 'Images approved',
          description: 'Ready to generate voiceover for each scene.',
          action: 'Generate Voice',
        };
      case 'voice_generated':
        return {
          title: 'Voice Review',
          message: 'Voice generated',
          description: 'Review the generated voiceover and approve or refine it.',
          action: 'Approve Voice',
        };
      case 'voice_approved':
        return {
          title: 'Reel Generation',
          message: 'Voice approved',
          description: 'Ready to generate the final reel video.',
          action: 'Generate Reel',
        };
      case 'reel_generated':
        return {
          title: 'Reel Ready',
          message: 'Reel generated',
          description: 'Your reel is ready to preview and download.',
          action: 'Preview Reel',
        };
      case 'completed':
        return {
          title: 'Project Completed',
          message: 'Project completed',
          description: 'Your project has been completed successfully.',
          action: 'Download',
        };
      default:
        return {
          title: 'Unknown Stage',
          message: 'Unknown status',
          description: 'Please check the project status.',
          action: null,
        };
    }
  };

  const content = getStageContent();

  // Show ScriptStage for script-related statuses
  const scriptStages = ['draft', 'script_generated', 'script_approved'];
  if (scriptStages.includes(project.status)) {
    return <ScriptStage project={project} onStatusChange={onStatusChange} />;
  }

  return (
    <div className="contentPanel">
      <h1 className="contentPanel-title">
        {content.title}
      </h1>
      
      <div className="contentPanel-content">
        <h2 className="contentPanel-content-title">
          {content.message}
        </h2>
        <p className="contentPanel-content-description">
          {content.description}
        </p>
        
        {content.action && (
          <button className="contentPanel-button">
            {content.action}
          </button>
        )}
      </div>

      <div className="contentPanel-details">
        <h3 className="contentPanel-details-title">
          Project Details
        </h3>
        <div className="contentPanel-details-grid">
          <div className="contentPanel-details-item">
            <strong>Title:</strong> {project.title}
          </div>
          <div className="contentPanel-details-item">
            <strong>Topic:</strong> {project.topic}
          </div>
          <div className="contentPanel-details-item">
            <strong>Language:</strong> {project.language}
          </div>
          <div className="contentPanel-details-item">
            <strong>Duration:</strong> {project.duration}s
          </div>
          <div className="contentPanel-details-item">
            <strong>Content Type:</strong> {project.content_type}
          </div>
          <div className="contentPanel-details-item">
            <strong>Status:</strong> {project.status.replace('_', ' ')}
          </div>
        </div>
        {project.additional_context && (
          <div className="contentPanel-details-context">
            <strong>Additional Context:</strong>
            <p className="contentPanel-details-context-text">
              {project.additional_context}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ContentPanel;
