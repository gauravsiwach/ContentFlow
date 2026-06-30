import './ProgressPanel.css';

function ProgressPanel({ project, onStageClick }) {
  const stages = [
    { key: 'draft', label: 'Draft' },
    { key: 'script_generated', label: 'Script' },
    { key: 'script_approved', label: 'Script ✓' },
    { key: 'scenes_generated', label: 'Scenes' },
    { key: 'scenes_approved', label: 'Scenes ✓' },
    { key: 'images_generated', label: 'Images' },
    { key: 'images_approved', label: 'Images ✓' },
    { key: 'voices_generated', label: 'Voice' },
    { key: 'voices_approved', label: 'Voice ✓' },
    { key: 'reel_generated', label: 'Reel' },
    { key: 'completed', label: 'Completed ✓' },
  ];

  const getCurrentStageIndex = () => {
    return stages.findIndex(stage => stage.key === project.status);
  };

  const currentIndex = getCurrentStageIndex();

  const handleStageClick = (stageKey) => {
    if (onStageClick) {
      onStageClick(stageKey);
    }
  };

  return (
    <div className="progressPanel">
      <h2 className="progressPanel-title">
        Progress
      </h2>
      
      <div className="progressPanel-stages">
        {stages.map((stage, index) => {
          const isCompleted = index < currentIndex;
          const isCurrent = index === currentIndex;
          const isClickable = index <= currentIndex || isCurrent; // Allow clicking current and previous stages

          const stageClass = `progressPanel-stage ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isClickable ? 'clickable' : ''}`;

          return (
            <div
              key={stage.key}
              className={stageClass}
              onClick={() => isClickable && handleStageClick(stage.key)}
              style={{ cursor: isClickable ? 'pointer' : 'default' }}
            >
              <div className="progressPanel-stage-indicator">
                {isCompleted ? '✓' : index + 1}
              </div>
              {stage.label}
            </div>
          );
        })}
      </div>

      <div className="progressPanel-status">
        <h3 className="progressPanel-status-title">
          Current Status
        </h3>
        <p className="progressPanel-status-text">
          {project.status.replace('_', ' ').toUpperCase()}
        </p>
      </div>
    </div>
  );
}

export default ProgressPanel;
