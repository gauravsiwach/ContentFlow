import React, { useState, useEffect } from 'react';
import { scenesApi } from '../api/scenes';
import './SceneStage.css';

function SceneStage({ project, onStatusChange }) {
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedScene, setExpandedScene] = useState(null);
  const [refineInstructions, setRefineInstructions] = useState('');

  useEffect(() => {
    if (project.status === 'scenes_generated' || project.status === 'scenes_approved') {
      loadScenes();
    }
  }, [project.status, project.id]);

  const loadScenes = async () => {
    try {
      setLoading(true);
      const data = await scenesApi.getScenes(project.id);
      setScenes(data.scenes || []);
      setError(null);
    } catch (err) {
      setError('Failed to load scenes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateScenes = async () => {
    try {
      setLoading(true);
      await scenesApi.generateScenes(project.id);
      onStatusChange();
    } catch (err) {
      setError('Failed to generate scenes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefineScenes = async () => {
    if (!refineInstructions.trim()) return;
    
    try {
      setLoading(true);
      await scenesApi.refineScenes(project.id, refineInstructions);
      setRefineInstructions('');
      onStatusChange();
    } catch (err) {
      setError('Failed to refine scenes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveScenes = async () => {
    try {
      setLoading(true);
      await scenesApi.approveScenes(project.id);
      onStatusChange();
    } catch (err) {
      setError('Failed to approve scenes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSceneExpand = (sceneId) => {
    setExpandedScene(expandedScene === sceneId ? null : sceneId);
  };

  if (project.status === 'script_approved') {
    return (
      <div className="sceneStage">
        <h2>Scene Generation</h2>
        <p>Generate scene breakdown from your approved script.</p>
        <button 
          onClick={handleGenerateScenes}
          disabled={loading}
          className="sceneStage-generateBtn"
        >
          {loading ? 'Generating...' : 'Generate Scenes'}
        </button>
        {error && <div className="sceneStage-error">{error}</div>}
      </div>
    );
  }

  if (project.status === 'scenes_generated' || project.status === 'scenes_approved') {
    return (
      <div className="sceneStage">
        <div className="sceneStage-header">
          <h2>Scenes</h2>
          <div className="sceneStage-summary">
            <span>{scenes.length} scenes</span>
            <span>Total: {scenes.reduce((sum, scene) => sum + scene.duration, 0)}s</span>
          </div>
        </div>

        {loading && <div className="sceneStage-loading">Loading...</div>}
        
        {error && <div className="sceneStage-error">{error}</div>}

        <div className="sceneStage-list">
          {scenes.map((scene) => (
            <div 
              key={scene.id} 
              className={`sceneStage-card ${expandedScene === scene.id ? 'expanded' : ''}`}
            >
              <div className="sceneStage-cardHeader" onClick={() => toggleSceneExpand(scene.id)}>
                <span className="sceneStage-number">Scene {scene.scene_number}</span>
                <span className="sceneStage-title">{scene.title}</span>
                <span className="sceneStage-duration">{scene.duration}s</span>
                <span className="sceneStage-expandIcon">{expandedScene === scene.id ? '▼' : '▶'}</span>
              </div>

              {expandedScene === scene.id && (
                <div className="sceneStage-cardBody">
                  <div className="sceneStage-field">
                    <label>Description:</label>
                    <p>{scene.description}</p>
                  </div>
                  <div className="sceneStage-field">
                    <label>Voiceover:</label>
                    <p>{scene.voiceover_text}</p>
                  </div>
                  <div className="sceneStage-field">
                    <label>Camera Directions:</label>
                    <p>{scene.camera_directions}</p>
                  </div>
                  <div className="sceneStage-field">
                    <label>Visual Description:</label>
                    <p>{scene.visual_description}</p>
                  </div>
                  <div className="sceneStage-field">
                    <label>Image Prompt:</label>
                    <p>{scene.image_prompt}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="sceneStage-actions">
          <div className="sceneStage-refine">
            <textarea
              value={refineInstructions}
              onChange={(e) => setRefineInstructions(e.target.value)}
              placeholder="Instructions for refining scenes..."
              className="sceneStage-refineInput"
            />
            <button 
              onClick={handleRefineScenes}
              disabled={loading || !refineInstructions.trim()}
              className="sceneStage-refineBtn"
            >
              Refine
            </button>
          </div>

          {project.status === 'scenes_generated' && (
            <button 
              onClick={handleApproveScenes}
              disabled={loading}
              className="sceneStage-approveBtn"
            >
              {loading ? 'Approving...' : 'Approve All'}
            </button>
          )}
        </div>
      </div>
    );
  }

  return null;
}

export default SceneStage;
