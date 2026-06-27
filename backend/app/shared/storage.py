import os
from pathlib import Path
from app.config import settings


def ensure_storage_dirs():
    """Ensure storage directories exist."""
    base_path = Path(settings.STORAGE_BASE_PATH)
    projects_path = base_path / "projects"
    
    # Create base storage directory
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Create projects directory
    projects_path.mkdir(parents=True, exist_ok=True)
    
    return base_path


def get_project_storage_path(project_id: str) -> Path:
    """Get storage path for a specific project."""
    base_path = Path(settings.STORAGE_BASE_PATH)
    project_path = base_path / "projects" / project_id
    
    # Create project directory if it doesn't exist
    project_path.mkdir(parents=True, exist_ok=True)
    
    return project_path


def ensure_project_storage(project_id: str):
    """Ensure storage directories exist for a specific project."""
    project_path = get_project_storage_path(project_id)
    
    # Create subdirectories for different asset types
    (project_path / "images").mkdir(parents=True, exist_ok=True)
    (project_path / "voice").mkdir(parents=True, exist_ok=True)
    (project_path / "reel").mkdir(parents=True, exist_ok=True)
    
    return project_path


def delete_project_storage(project_id: str):
    """Delete storage directory for a specific project."""
    project_path = get_project_storage_path(project_id)
    
    if project_path.exists():
        # Delete the entire project directory
        import shutil
        shutil.rmtree(project_path)
