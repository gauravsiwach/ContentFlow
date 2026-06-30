from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.project.models import Project
from app.modules.project.schemas import ProjectCreate, ProjectUpdate
from app.shared.storage import ensure_project_storage, delete_project_storage
from app.shared.exceptions import ProjectNotFoundError, InvalidStateTransitionError


def create_project(db: Session, project_data: ProjectCreate) -> Project:
    """Create a new project."""
    project = Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Create storage directory for the project
    ensure_project_storage(project.id)
    
    return project


def get_project(db: Session, project_id: str) -> Project:
    """Get a project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ProjectNotFoundError(project_id)
    return project


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """List all projects."""
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()


def delete_project(db: Session, project_id: str) -> None:
    """Delete a project and its storage directory."""
    project = get_project(db, project_id)
    
    # Delete storage directory
    delete_project_storage(project_id)
    
    # Delete project from database
    db.delete(project)
    db.commit()


def update_project(db: Session, project_id: str, project_data: ProjectUpdate) -> Project:
    """Update a project."""
    project = get_project(db, project_id)
    
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


def update_project_status(db: Session, project_id: str, new_status: str) -> Project:
    """Update project status with state transition validation."""
    project = get_project(db, project_id)
    
    # Define valid state transitions
    valid_transitions = {
        "draft": ["script_generated"],
        "script_generated": ["script_approved", "script_generated"],
        "script_approved": ["scenes_generated"],
        "scenes_generated": ["scenes_approved", "scenes_generated"],
        "scenes_approved": ["images_generated"],
        "images_generated": ["images_approved", "images_generated"],
        "images_approved": ["voices_generated"],
        "voices_generated": ["voices_approved", "voices_generated"],
        "voices_approved": ["reel_generated"],
        "reel_generated": ["completed"],
        "completed": []
    }
    
    current_status = project.status
    
    # Validate transition
    if new_status not in valid_transitions.get(current_status, []):
        raise InvalidStateTransitionError(current_status, new_status)
    
    project.status = new_status
    db.commit()
    db.refresh(project)
    return project


def get_project_status(db: Session, project_id: str) -> dict:
    """Get project status and available actions."""
    project = get_project(db, project_id)
    
    # Define available actions based on status
    status_actions = {
        "draft": ["generate_script"],
        "script_generated": ["approve_script", "refine_script"],
        "script_approved": ["generate_scenes"],
        "scenes_generated": ["approve_scenes", "refine_scenes"],
        "scenes_approved": ["generate_images"],
        "images_generated": ["approve_images", "refine_images"],
        "images_approved": ["generate_voice"],
        "voices_generated": ["approve_voice", "refine_voice"],
        "voices_approved": ["generate_reel"],
        "reel_generated": ["mark_complete"],
        "completed": []
    }
    
    return {
        "id": project.id,
        "status": project.status,
        "available_actions": status_actions.get(project.status, [])
    }
