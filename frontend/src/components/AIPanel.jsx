import './AIPanel.css';

function AIPanel({ project }) {
  return (
    <div className="aiPanel">
      <h2 className="aiPanel-title">
        AI Instructions
      </h2>
      
      <div className="aiPanel-feedback">
        <h3 className="aiPanel-feedback-title">
          Refinement Feedback
        </h3>
        <textarea
          placeholder="Provide instructions to refine the current output..."
          className="aiPanel-feedback-textarea"
        />
        <button className="aiPanel-feedback-button">
          Submit Feedback
        </button>
      </div>

      <div className="aiPanel-activity">
        <h3 className="aiPanel-activity-title">
          Activity Log
        </h3>
        <div className="aiPanel-activity-text">
          No recent activity
        </div>
      </div>

      <div className="aiPanel-context">
        <h3 className="aiPanel-context-title">
          Context
        </h3>
        <div className="aiPanel-context-text">
          <div><strong>Topic:</strong> {project.topic}</div>
          <div><strong>Language:</strong> {project.language}</div>
          <div><strong>Duration:</strong> {project.duration}s</div>
          <div><strong>Type:</strong> {project.content_type}</div>
        </div>
      </div>
    </div>
  );
}

export default AIPanel;
