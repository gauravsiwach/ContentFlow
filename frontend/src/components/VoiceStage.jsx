import { useState, useEffect } from 'react';
import { voicesApi } from '../api/voices';
import { scenesApi } from '../api/scenes';
import './VoiceStage.css';

function VoiceStage({ project, onStatusChange }) {
  const [voices, setVoices] = useState([]);
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generatingSceneId, setGeneratingSceneId] = useState(null);
  const [error, setError] = useState(null);
  const [expandedVoice, setExpandedVoice] = useState(null);
  const [playingVoice, setPlayingVoice] = useState(null);

  const POST_IMAGES_STATUSES = [
    'images_approved', 'voices_generated', 'voices_approved',
    'reel_generated', 'completed'
  ];

  useEffect(() => {
    if (POST_IMAGES_STATUSES.includes(project.status)) {
      loadScenes();
      loadVoices();
    }
  }, [project.status, project.id]);

  const loadScenes = async () => {
    try {
      const data = await scenesApi.getScenes(project.id);
      console.log('Loaded scenes:', data);
      const uniqueScenes = (data.scenes || []).reduce((acc, scene) => {
        if (!acc.some(existing => existing.id === scene.id)) {
          acc.push(scene);
        }
        return acc;
      }, []);
      console.log('Unique scenes:', uniqueScenes);
      setScenes(uniqueScenes);
    } catch (err) {
      console.error('Failed to load scenes:', err);
    }
  };

  const loadVoices = async () => {
    try {
      setLoading(true);
      const data = await voicesApi.getVoices(project.id);
      console.log('Loaded voices:', data);
      setVoices(data.voices || []);
      setError(null);
    } catch (err) {
      setError('Failed to load voices');
      console.error('Failed to load voices:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSceneVoice = async (sceneId) => {
    try {
      setGeneratingSceneId(sceneId);
      await voicesApi.generateSceneVoice(project.id, sceneId);
      await loadVoices();
      onStatusChange();
    } catch (err) {
      setError('Failed to generate voice');
      console.error(err);
    } finally {
      setGeneratingSceneId(null);
    }
  };

  const handleGenerateAllVoices = async () => {
    try {
      setLoading(true);
      for (const scene of scenes) {
        await handleGenerateSceneVoice(scene.id);
      }
    } catch (err) {
      setError('Failed to generate voices');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveVoices = async () => {
    try {
      setLoading(true);
      await voicesApi.approveVoices(project.id);
      onStatusChange('voices_approved');
    } catch (err) {
      setError('Failed to approve voices');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleMoveToReel = async () => {
    try {
      setLoading(true);
      onStatusChange('voices_approved');
    } catch (err) {
      setError('Failed to move to reel');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefineVoice = async (voiceId, newText) => {
    try {
      setLoading(true);
      await voicesApi.refineVoice(project.id, voiceId, newText);
      await loadVoices();
    } catch (err) {
      setError('Failed to refine voice');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayVoice = (voiceId) => {
    if (playingVoice === voiceId) {
      setPlayingVoice(null);
    } else {
      setPlayingVoice(voiceId);
    }
  };

  if (error) {
    return <div className="voice-stage error">{error}</div>;
  }

  if (project.status === 'images_approved') {
    if (voices.length === 0) {
      return (
        <div className="voice-stage">
          <h3>Ready to Generate Voices</h3>
          <p>Generate voiceovers for {scenes.length} scenes using Hindi TTS</p>
          <button
            className="btn btn-primary"
            onClick={handleGenerateAllVoices}
            disabled={loading}
          >
            {loading ? 'Generating All...' : 'Generate All Voices'}
          </button>
          <div className="scene-list">
            {scenes.map((scene) => {
              const hasVoice = voices.some(v => v.scene_id === scene.id);
              return (
                <div key={scene.id} className="scene-item">
                  <span>Scene {scene.scene_number}: {scene.title}</span>
                  {hasVoice ? (
                    <span className="status-done">✓ Done</span>
                  ) : (
                    <button
                      className="btn btn-secondary"
                      onClick={() => handleGenerateSceneVoice(scene.id)}
                      disabled={generatingSceneId === scene.id}
                    >
                      {generatingSceneId === scene.id ? 'Generating...' : 'Generate'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      );
    } else {
      return (
        <div className="voice-stage">
          <div className="voice-header">
            <h3>Voiceovers ({voices.length})</h3>
            <div className="voice-header-actions">
              <button
                className="btn btn-secondary"
                onClick={handleGenerateAllVoices}
                disabled={loading}
              >
                {loading ? 'Regenerating...' : 'Regenerate All Voices'}
              </button>
              <button
                className="btn btn-primary"
                onClick={() => onStatusChange('voices_generated')}
                disabled={loading}
              >
                Move to Voice Review
              </button>
            </div>
          </div>

          <div className="voice-grid">
            {voices.map((voice) => {
              const scene = scenes.find(s => s.id === voice.scene_id);
              const audioUrl = `/api/v1/projects/${project.id}/voices/${voice.scene_id}`;
              return (
                <div
                  key={voice.id}
                  className="voice-card"
                >
                  <div className="voice-info">
                    <h4>Scene {scene?.scene_number || voice.scene_id}: {scene?.title || 'Unknown'}</h4>
                    <p className="voice-text">{voice.text_used}</p>
                    <p className="voice-meta">Voice: {voice.voice_used}</p>
                  </div>
                  <div className="voice-player">
                    <audio
                      src={audioUrl}
                      controls
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }
  }

  if (voices.length === 0 && project.status !== 'images_approved') {
    return <div className="voice-stage">No voices generated yet</div>;
  }

  return (
    <div className="voice-stage">
      <div className="voice-header">
        <h3>Voiceovers ({voices.length})</h3>
        <div className="voice-header-actions">
          {project.status === 'voices_generated' && (
            <button
              className="btn btn-primary"
              onClick={handleApproveVoices}
              disabled={loading}
            >
              Approve All
            </button>
          )}
          {project.status === 'voices_approved' && (
            <>
              <button
                className="btn btn-secondary"
                onClick={handleGenerateAllVoices}
                disabled={loading}
              >
                {loading ? 'Regenerating...' : 'Regenerate All Voices'}
              </button>
              <button
                className="btn btn-primary"
                onClick={handleMoveToReel}
                disabled={loading}
              >
                Move to Reel
              </button>
            </>
          )}
        </div>
      </div>

      <div className="voice-grid">
        {voices.map((voice) => {
          const scene = scenes.find(s => s.id === voice.scene_id);
          const audioUrl = `/api/v1/projects/${project.id}/voices/${voice.scene_id}`;
          console.log('Loading voice:', audioUrl, voice);
          return (
            <div
              key={voice.id}
              className={`voice-card ${expandedVoice === voice.id ? 'expanded' : ''}`}
            >
              <div className="voice-info">
                <h4>Scene {scene?.scene_number || voice.scene_id}: {scene?.title || 'Unknown'}</h4>
                <p className="voice-text">{voice.text_used}</p>
                <p className="voice-meta">Voice: {voice.voice_used}</p>
              </div>
              <div className="voice-player">
                <audio
                  ref={(audio) => {
                    if (audio && playingVoice === voice.id) {
                      audio.play().catch(console.error);
                    } else if (audio && playingVoice !== voice.id) {
                      audio.pause();
                    }
                  }}
                  src={audioUrl}
                  controls
                  onPlay={() => setPlayingVoice(voice.id)}
                  onPause={() => setPlayingVoice(null)}
                  onEnded={() => setPlayingVoice(null)}
                />
              </div>
              <button
                className="btn btn-secondary"
                onClick={() => setExpandedVoice(expandedVoice === voice.id ? null : voice.id)}
              >
                {expandedVoice === voice.id ? '▼' : '▲'}
              </button>
              {expandedVoice === voice.id && (
                <div className="voice-details">
                  <div className="refine-section">
                    <textarea
                      placeholder="Enter new text to refine this voiceover..."
                      className="refine-input"
                      rows={3}
                      defaultValue={voice.text_used}
                    />
                    <button
                      className="btn btn-secondary"
                      onClick={() => {
                        const textarea = document.querySelector('.refine-input');
                        if (textarea.value.trim()) {
                          handleRefineVoice(voice.id, textarea.value.trim());
                          textarea.value = '';
                        }
                      }}
                    >
                      Refine
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default VoiceStage;
