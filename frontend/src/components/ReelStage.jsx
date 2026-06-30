import React, { useState, useEffect } from 'react';
import { reelsApi } from '../api/reels';
import { projectsApi } from '../api/projects';
import './ReelStage.css';

const ReelStage = ({ project, onStatusChange }) => {
  const [reel, setReel] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadReel();
  }, [project.id]);

  const loadReel = async () => {
    try {
      setLoading(true);
      const data = await reelsApi.getReel(project.id);
      setReel(data);
      setError(null);
    } catch (err) {
      if (err.message !== 'Failed to get reel') {
        setError('Failed to load reel');
      }
      setReel(null);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReel = async () => {
    try {
      setGenerating(true);
      setError(null);
      await reelsApi.generateReel(project.id, {
        resolution: '1920x1080',
        fps: 30
      });
      await loadReel();
      onStatusChange();
    } catch (err) {
      setError('Failed to generate reel');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    const url = reelsApi.getReelUrl(project.id);
    const link = document.createElement('a');
    link.href = url;
    link.download = `reel_${project.id}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleMarkComplete = async () => {
    try {
      await projectsApi.markProjectComplete(project.id);
      onStatusChange('completed');
    } catch (err) {
      setError('Failed to mark project as complete');
    }
  };

  if (loading) {
    return (
      <div className="reelStage">
        <div className="reelStage-loading">Loading reel...</div>
      </div>
    );
  }

  return (
    <div className="reelStage">
      <div className="reelStage-header">
        <h2>Reel Generation</h2>
        <p>Generate the final video combining scenes, images, and audio</p>
      </div>

      {error && (
        <div className="reelStage-error">
          {error}
        </div>
      )}

      {!reel && !generating && project.status === 'voices_approved' && (
        <div className="reelStage-empty">
          <p>No reel generated yet</p>
          <button
            className="reelStage-button"
            onClick={handleGenerateReel}
            disabled={generating}
          >
            Generate Reel
          </button>
        </div>
      )}

      {!reel && !generating && project.status !== 'voices_approved' && (
        <div className="reelStage-empty">
          <p>Reel exists but navigated back</p>
          <div className="reelStage-actions">
            <button
              className="reelStage-button reelStage-button-secondary"
              onClick={handleGenerateReel}
              disabled={generating}
            >
              Regenerate Reel
            </button>
            <button
              className="reelStage-button"
              onClick={() => onStatusChange('reel_generated')}
              disabled={generating}
            >
              Move to Reel Review
            </button>
          </div>
        </div>
      )}

      {generating && (
        <div className="reelStage-generating">
          <div className="reelStage-spinner"></div>
          <p>Generating reel... This may take a few minutes</p>
        </div>
      )}

      {reel && !generating && (
        <div className="reelStage-content">
          <div className="reelStage-video">
            <video
              controls
              src={reelsApi.getReelUrl(project.id)}
              className="reelStage-player"
            />
          </div>

          <div className="reelStage-info">
            <div className="reelStage-info-item">
              <span className="reelStage-info-label">Duration:</span>
              <span className="reelStage-info-value">{reel.duration}s</span>
            </div>
            <div className="reelStage-info-item">
              <span className="reelStage-info-label">Resolution:</span>
              <span className="reelStage-info-value">{reel.resolution}</span>
            </div>
            <div className="reelStage-info-item">
              <span className="reelStage-info-label">Format:</span>
              <span className="reelStage-info-value">{reel.format}</span>
            </div>
          </div>

          <div className="reelStage-actions">
            <button
              className="reelStage-button reelStage-button-secondary"
              onClick={handleGenerateReel}
              disabled={generating}
            >
              Regenerate Reel
            </button>
            <button
              className="reelStage-button reelStage-button-secondary"
              onClick={handleMarkComplete}
              disabled={generating}
            >
              Mark Complete
            </button>
            <button
              className="reelStage-button"
              onClick={handleDownload}
            >
              Download Reel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReelStage;
