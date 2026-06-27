from typing import Optional


class ContentFlowError(Exception):
    """Base exception for ContentFlow application."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ProjectNotFoundError(ContentFlowError):
    """Raised when a project is not found."""
    
    def __init__(self, project_id: str):
        super().__init__(f"Project not found: {project_id}", status_code=404)


class InvalidStateTransitionError(ContentFlowError):
    """Raised when an invalid state transition is attempted."""
    
    def __init__(self, current_state: str, target_state: str):
        message = f"Invalid state transition from {current_state} to {target_state}"
        super().__init__(message, status_code=409)


class AIGenerationError(ContentFlowError):
    """Raised when AI generation fails."""
    
    def __init__(self, stage: str, details: Optional[str] = None):
        message = f"AI generation failed for stage: {stage}"
        if details:
            message += f" - {details}"
        super().__init__(message, status_code=500)


class AIServiceUnavailableError(ContentFlowError):
    """Raised when an AI service is unavailable."""
    
    def __init__(self, service: str):
        super().__init__(f"AI service unavailable: {service}", status_code=503)


class StorageError(ContentFlowError):
    """Raised when a storage operation fails."""
    
    def __init__(self, operation: str, details: Optional[str] = None):
        message = f"Storage operation failed: {operation}"
        if details:
            message += f" - {details}"
        super().__init__(message, status_code=500)


class ValidationError(ContentFlowError):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, details: Optional[str] = None):
        message = f"Validation failed for field: {field}"
        if details:
            message += f" - {details}"
        super().__init__(message, status_code=400)
