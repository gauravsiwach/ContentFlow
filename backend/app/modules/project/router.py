from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.modules.project.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse, ProjectStatusResponse
from app.modules.project.service import create_project, get_project, list_projects, delete_project, update_project, update_project_status, get_project_status

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
