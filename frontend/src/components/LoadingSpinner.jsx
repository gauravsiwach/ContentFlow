import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message = 'Loading...', progress = null, size = 'medium' }) => {
  const getProgressText = () => {
    if (progress && progress.current !== undefined && progress.total !== undefined) {
      return `${message} (${progress.current}/${progress.total})`;
    }
    return message;
  };

  const getProgressPercentage = () => {
    if (progress && progress.current !== undefined && progress.total !== undefined) {
      return Math.round((progress.current / progress.total) * 100);
    }
    return 0;
  };

  return (
    <div className={`loading-spinner loading-spinner--${size}`}>
      <div className="loading-spinner__dots">
        <span className="loading-spinner__dot"></span>
        <span className="loading-spinner__dot"></span>
        <span className="loading-spinner__dot"></span>
      </div>
      <p className="loading-spinner__message">{getProgressText()}</p>
      {progress && progress.current !== undefined && progress.total !== undefined && (
        <div className="loading-spinner__progress-bar">
          <div 
            className="loading-spinner__progress-fill" 
            style={{ width: `${getProgressPercentage()}%` }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default LoadingSpinner;
