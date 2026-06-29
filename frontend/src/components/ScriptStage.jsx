import { useState, useEffect } from 'react';
import { getScript, generateScript, updateScript, approveScript, refineScript } from '../api/script';
import './ScriptStage.css';

function ScriptStage({ project, onStatusChange }) {
  const [script, setScript] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState('');
  const [refineInstructions, setRefineInstructions] = useState('');

  useEffect(() => {
    loadScript();
  }, [project.id]);

  const loadScript = async () => {
    try {
      const data = await getScript(project.id);
      setScript(data);
      setEditedContent(data?.content || '');
    } catch (err) {
      if (err.message !== 'Failed to fetch script') {
        setError(err.message);
      }
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await generateScript(project.id);
      setScript(data);
      setEditedContent(data.content);
      onStatusChange('script_generated');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await updateScript(project.id, editedContent);
      setScript(data);
      setIsEditing(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await approveScript(project.id);
      setScript(data);
      onStatusChange('script_approved');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async () => {
    if (!refineInstructions.trim()) {
      setError('Please provide refinement instructions');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const data = await refineScript(project.id, refineInstructions);
      setScript(data);
      setEditedContent(data.content);
      setRefineInstructions('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (project.status === 'draft') {
    return (
      <div className="scriptStage">
        <div className="scriptStage-content">
          <h3 className="scriptStage-title">Script Generation</h3>
          <p className="scriptStage-description">
            Generate a script for your video using AI. The script will be based on your project topic, language, duration, and content type.
          </p>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="scriptStage-button"
          >
            {loading ? 'Generating...' : 'Generate Script'}
          </button>
          {error && <div className="scriptStage-error">{error}</div>}
        </div>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="scriptStage">
        <div className="scriptStage-loading">Loading script...</div>
      </div>
    );
  }

  return (
    <div className="scriptStage">
      <div className="scriptStage-header">
        <h3 className="scriptStage-title">Script</h3>
        {!script.is_approved && !isEditing && (
          <button
            onClick={handleApprove}
            disabled={loading}
            className="scriptStage-button scriptStage-button-approve"
          >
            Approve
          </button>
        )}
      </div>

      {error && <div className="scriptStage-error">{error}</div>}

      {isEditing ? (
        <div className="scriptStage-editor">
          <textarea
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            className="scriptStage-textarea"
            rows={20}
          />
          <div className="scriptStage-actions">
            <button
              onClick={() => {
                setEditedContent(script.content);
                setIsEditing(false);
              }}
              className="scriptStage-button scriptStage-button-cancel"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={loading}
              className="scriptStage-button"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      ) : (
        <div className="scriptStage-viewer">
          <div className="scriptStage-text">{script.content}</div>
          {!script.is_approved && (
            <button
              onClick={() => setIsEditing(true)}
              className="scriptStage-button scriptStage-button-edit"
            >
              Edit
            </button>
          )}
        </div>
      )}

      {!script.is_approved && (
        <div className="scriptStage-refine">
          <h4 className="scriptStage-refine-title">Refine Script</h4>
          <textarea
            value={refineInstructions}
            onChange={(e) => setRefineInstructions(e.target.value)}
            placeholder="Provide instructions to refine the script..."
            className="scriptStage-textarea scriptStage-textarea-small"
            rows={3}
          />
          <button
            onClick={handleRefine}
            disabled={loading}
            className="scriptStage-button"
          >
            {loading ? 'Refining...' : 'Refine'}
          </button>
        </div>
      )}
    </div>
  );
}

export default ScriptStage;
