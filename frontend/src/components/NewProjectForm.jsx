import { useState, useEffect } from 'react';
import { projectsApi } from '../api/projects';
import { LANGUAGES, DURATIONS } from '../types/projects';
import './NewProjectForm.css';

function NewProjectForm({ onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    topic: '',
    language: 'English',
    duration: 60,
    content_type: 'comedy_children',
    additional_context: '',
  });
  const [contentTypes, setContentTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchContentTypes = async () => {
      try {
        const types = await projectsApi.getContentTypes();
        setContentTypes(types);
        if (types.length > 0) {
          setFormData(prev => ({ ...prev, content_type: types[0].value }));
        }
      } catch (err) {
        console.error('Failed to fetch content types:', err);
      }
    };
    fetchContentTypes();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await projectsApi.createProject(formData);
      onSuccess(response);
      onClose();
    } catch (error) {
      setError(error.message || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  const selectedContentType = contentTypes.find(ct => ct.value === formData.content_type);

  return (
    <div className="newProjectForm-overlay">
      <div className="newProjectForm-container">
        <h2 className="newProjectForm-title">Create New Project</h2>
        
        {error && (
          <div className="newProjectForm-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="newProjectForm-field">
            <label className="newProjectForm-label">
              Title *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="newProjectForm-input"
            />
          </div>

          <div className="newProjectForm-field">
            <label className="newProjectForm-label">
              Topic *
            </label>
            <textarea
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              required
              rows={2}
              className="newProjectForm-textarea"
            />
          </div>

          <div className="newProjectForm-fieldGroup">
            <div className="newProjectForm-field">
              <label className="newProjectForm-label">
                Language
              </label>
              <select
                name="language"
                value={formData.language}
                onChange={handleChange}
                className="newProjectForm-select"
              >
                {LANGUAGES.map(lang => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            <div className="newProjectForm-field">
              <label className="newProjectForm-label">
                Duration
              </label>
              <select
                name="duration"
                value={formData.duration}
                onChange={handleChange}
                className="newProjectForm-select"
              >
                {DURATIONS.map(duration => (
                  <option key={duration} value={duration}>{duration}s</option>
                ))}
              </select>
            </div>

            <div className="newProjectForm-field">
              <label className="newProjectForm-label">
                Content Type
              </label>
              <select
                name="content_type"
                value={formData.content_type}
                onChange={handleChange}
                className="newProjectForm-select"
              >
                {contentTypes.map(ct => (
                  <option key={ct.value} value={ct.value}>{ct.display_name}</option>
                ))}
              </select>
              {selectedContentType && (
                <div className="newProjectForm-description">
                  {selectedContentType.description} ({selectedContentType.age_range})
                </div>
              )}
            </div>
          </div>

          <div className="newProjectForm-field">
            <label className="newProjectForm-label">
              Additional Context (optional)
            </label>
            <textarea
              name="additional_context"
              value={formData.additional_context}
              onChange={handleChange}
              rows={3}
              placeholder="Any additional context or instructions..."
              className="newProjectForm-textarea"
            />
          </div>

          <div className="newProjectForm-buttonGroup">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="newProjectForm-button newProjectForm-button-cancel"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="newProjectForm-button newProjectForm-button-submit"
            >
              {loading ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default NewProjectForm;
