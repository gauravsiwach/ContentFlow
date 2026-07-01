import { useState, useEffect } from 'react';
import { imagesApi } from '../api/images';
import { scenesApi } from '../api/scenes';
import LoadingSpinner from './LoadingSpinner';
import './ImageStage.css';

function ImageStage({ project, onStatusChange }) {
  const [images, setImages] = useState([]);
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generatingSceneId, setGeneratingSceneId] = useState(null);
  const [generatingProgress, setGeneratingProgress] = useState({ current: 0, total: 0 });
  const [error, setError] = useState(null);
  const [expandedImage, setExpandedImage] = useState(null);

  const POST_SCENES_STATUSES = [
    'scenes_approved', 'images_generated', 'images_approved',
    'voices_generated', 'voices_approved', 'reel_generated', 'completed'
  ];

  useEffect(() => {
    if (POST_SCENES_STATUSES.includes(project.status)) {
      loadScenes();
      loadImages();
    }
  }, [project.status, project.id]);

  const loadScenes = async () => {
    try {
      const data = await scenesApi.getScenes(project.id);
      console.log('Loaded scenes:', data);
      // Deduplicate scenes by id
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

  const loadImages = async () => {
    try {
      setLoading(true);
      const data = await imagesApi.getImages(project.id);
      console.log('Loaded images:', data);
      setImages(data.images || []);
      setError(null);
    } catch (err) {
      setError('Failed to load images');
      console.error('Failed to load images:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSceneImage = async (sceneId) => {
    try {
      setGeneratingSceneId(sceneId);
      await imagesApi.generateSceneImage(project.id, sceneId);
      await loadImages();
      onStatusChange();
    } catch (err) {
      setError('Failed to generate image');
      console.error(err);
    } finally {
      setGeneratingSceneId(null);
    }
  };

  const handleGenerateAllImages = async () => {
    try {
      setLoading(true);
      setGeneratingProgress({ current: 0, total: scenes.length });
      for (let i = 0; i < scenes.length; i++) {
        await handleGenerateSceneImage(scenes[i].id);
        setGeneratingProgress({ current: i + 1, total: scenes.length });
      }
    } catch (err) {
      setError('Failed to generate images');
      console.error(err);
    } finally {
      setLoading(false);
      setGeneratingProgress({ current: 0, total: 0 });
    }
  };

  const handleApproveImages = async () => {
    try {
      setLoading(true);
      await imagesApi.approveImages(project.id);
      onStatusChange('images_approved');
    } catch (err) {
      setError('Failed to approve images');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleMoveToVoices = async () => {
    try {
      setLoading(true);
      onStatusChange('images_approved');
    } catch (err) {
      setError('Failed to move to voices');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefineImage = async (imageId, newPrompt) => {
    try {
      setLoading(true);
      await imagesApi.refineImage(project.id, imageId, newPrompt);
      await loadImages();
    } catch (err) {
      setError('Failed to refine image');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getContentTypeTip = (contentType) => {
    if (contentType === 'comedy_children') {
      return "Images should be cartoon style with bright colors and cute, friendly characters!";
    }
    return null;
  };

  if (loading) {
    return (
      <div className="image-stage loading">
        <LoadingSpinner 
          message="Generating images..." 
          progress={generatingProgress.current > 0 ? generatingProgress : null}
          size="large"
        />
      </div>
    );
  }

  if (error) {
    return <div className="image-stage error">{error}</div>;
  }

  if (project.status === 'scenes_approved') {
    if (images.length === 0) {
      return (
        <div className="image-stage">
          <h3>Ready to Generate Images</h3>
          <p>Generate images for {scenes.length} scenes</p>
          <button
            className="btn btn-primary"
            onClick={handleGenerateAllImages}
            disabled={loading}
          >
            {loading ? 'Generating All...' : 'Generate All Images'}
          </button>
          <div className="scene-list">
            {scenes.map((scene) => {
              const hasImage = images.some(img => img.scene_id === scene.id);
              return (
                <div key={scene.id} className="scene-item">
                  <span>Scene {scene.scene_number}: {scene.title}</span>
                  {hasImage ? (
                    <span className="status-done">✓ Done</span>
                  ) : (
                    <button
                      className="btn btn-secondary"
                      onClick={() => handleGenerateSceneImage(scene.id)}
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
        <div className="image-stage">
          <div className="image-header">
            <h3>Images ({images.length})</h3>
            <div className="image-header-actions">
              <button
                className="btn btn-secondary"
                onClick={handleGenerateAllImages}
                disabled={loading}
              >
                {loading ? 'Regenerating...' : 'Regenerate All Images'}
              </button>
              <button
                className="btn btn-primary"
                onClick={() => onStatusChange('images_generated')}
                disabled={loading}
              >
                Move to Image Review
              </button>
            </div>
          </div>

          {project.content_type === 'comedy_children' && (
            <div className="image-tip">
              💡 {getContentTypeTip(project.content_type)}
            </div>
          )}

          <div className="image-grid">
            {images.map((image) => {
              const imageUrl = `/api/v1/projects/${project.id}/images/${image.scene_id}`;
              return (
                <div
                  key={image.id}
                  className={`image-card ${expandedImage === image.id ? 'expanded' : ''}`}
                >
                  <div className="image-preview">
                    <img
                      src={imageUrl}
                      alt={`Scene ${image.scene_id}`}
                      onError={(e) => {
                        console.error('Failed to load image:', imageUrl);
                        e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect width="100" height="100" fill="%23ccc"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E';
                      }}
                    />
                  </div>
                  <div className="image-info">
                    <h4>Scene {image.scene_id}</h4>
                    <p className="image-prompt">{image.prompt_used}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }
  }

  if (images.length === 0 && project.status !== 'scenes_approved') {
    return <div className="image-stage">No images generated yet</div>;
  }

  return (
    <div className="image-stage">
      <div className="image-header">
        <h3>Images ({images.length})</h3>
        <div className="image-header-actions">
          {project.status === 'images_generated' && (
            <button
              className="btn btn-primary"
              onClick={handleApproveImages}
              disabled={loading}
            >
              Approve All
            </button>
          )}
          {project.status === 'images_approved' && (
            <>
              <button
                className="btn btn-secondary"
                onClick={handleGenerateAllImages}
                disabled={loading}
              >
                {loading ? 'Regenerating...' : 'Regenerate All Images'}
              </button>
              <button
                className="btn btn-primary"
                onClick={handleMoveToVoices}
                disabled={loading}
              >
                Move to Voices
              </button>
            </>
          )}
        </div>
      </div>

      {project.content_type === 'comedy_children' && (
        <div className="image-tip">
          💡 {getContentTypeTip(project.content_type)}
        </div>
      )}

      <div className="image-grid">
        {images.map((image) => {
          const imageUrl = `/api/v1/projects/${project.id}/images/${image.scene_id}`;
          console.log('Loading image:', imageUrl, image);
          return (
            <div
              key={image.id}
              className={`image-card ${expandedImage === image.id ? 'expanded' : ''}`}
            >
              <div className="image-preview">
                <img
                  src={imageUrl}
                  alt={`Scene ${image.scene_id}`}
                  onError={(e) => {
                    console.error('Failed to load image:', imageUrl);
                    e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect width="100" height="100" fill="%23ccc"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E';
                  }}
                />
            </div>
            <div className="image-info">
              <h4>Scene {image.scene_id}</h4>
              <p className="image-prompt">{image.prompt_used}</p>
            </div>
            <button
              className="btn btn-secondary"
              onClick={() => setExpandedImage(expandedImage === image.id ? null : image.id)}
            >
              {expandedImage === image.id ? '▼' : '▲'}
            </button>
            {expandedImage === image.id && (
              <div className="image-details">
                <div className="refine-section">
                  <textarea
                    placeholder="Enter new prompt to refine this image..."
                    className="refine-input"
                    rows={3}
                  />
                  <button
                    className="btn btn-secondary"
                    onClick={() => {
                      const textarea = document.querySelector('.refine-input');
                      if (textarea.value.trim()) {
                        handleRefineImage(image.id, textarea.value.trim());
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

export default ImageStage;
