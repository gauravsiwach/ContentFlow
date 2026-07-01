from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.modules.project.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse, ProjectStatusResponse
from app.modules.project.service import create_project, get_project, list_projects, delete_project, update_project, update_project_status, get_project_status
from app.shared.content_types import ContentType, ContentTypeConfig

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project_endpoint(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    return create_project(db, project_data)


@router.get("", response_model=ProjectListResponse)
def list_projects_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all projects."""
    projects = list_projects(db, skip=skip, limit=limit)
    return ProjectListResponse(projects=projects, total=len(projects))


@router.get("/content-types", response_model=List[dict])
def get_content_types():
    """Get all available content types with their configurations."""
    content_types = ContentTypeConfig.get_all_content_types()
    result = []
    for ct in content_types:
        config = ContentTypeConfig.get_config(ct)
        result.append({
            "value": ct.value,
            "display_name": config.get("display_name", ct.value),
            "description": config.get("description", ""),
            "target_audience": config.get("target_audience", ""),
            "age_range": config.get("age_range", "")
        })
    return result


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_endpoint(project_id: str, db: Session = Depends(get_db)):
    """Get project details."""
    return get_project(db, project_id)


@router.delete("/{project_id}", status_code=204)
def delete_project_endpoint(project_id: str, db: Session = Depends(get_db)):
    """Delete project and its assets."""
    delete_project(db, project_id)
    return None


@router.get("/{project_id}/status", response_model=ProjectStatusResponse)
def get_project_status_endpoint(project_id: str, db: Session = Depends(get_db)):
    """Get current project status and available actions."""
    return get_project_status(db, project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(project_id: str, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    """Update project details."""
    return update_project(db, project_id, project_data)


@router.post("/{project_id}/complete", response_model=ProjectResponse)
def mark_project_complete(project_id: str, db: Session = Depends(get_db)):
    """Mark project as completed. Requires a reel to exist."""
    from app.modules.reel.service import ReelService
    reel_service = ReelService(db)
    reel = reel_service.get_reel(project_id)
    if not reel:
        raise HTTPException(status_code=400, detail="No reel found. Generate a reel before marking complete.")
    
    # Directly update status without workflow validation since we already verified reel exists
    project = get_project(db, project_id)
    project.status = "completed"
    db.commit()
    db.refresh(project)
    return project
