import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.script.service import ScriptService
from app.modules.script.schemas import (
    ScriptResponse, ScriptGenerateRequest, ScriptRefineRequest,
    ScriptUpdateRequest, ScriptApproveRequest
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["script"])

@router.get("/{project_id}/script", response_model=ScriptResponse)
def get_script(project_id: str, db: Session = Depends(get_db)):
    """Get script for a project"""
    service = ScriptService(db)
    script = service.get_script(project_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script

@router.post("/{project_id}/script/generate", response_model=ScriptResponse)
async def generate_script(project_id: str, db: Session = Depends(get_db)):
    """Generate script for a project using AI"""
    logger.info(f"Script generation requested for project: {project_id}")
    service = ScriptService(db)
    
    # Get project for context
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if not project:
        logger.error(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    
    logger.info(f"Project found: {project.title}, status: {project.status}")

    # Validate state - can generate from draft, script_generated, or script_approved
    allowed_states = ["draft", "script_generated", "script_approved"]
    if project.status not in allowed_states:
        logger.error(f"Invalid project status for script generation: {project.status}")
        raise HTTPException(
            status_code=409,
            detail=f"Cannot generate script when status is '{project.status}'. Allowed states: {', '.join(allowed_states)}"
        )
    
    try:
        logger.info("Starting script generation via AI...")
        script = await service.generate_script(project_id, {
            "topic": project.topic,
            "language": project.language,
            "duration": project.duration,
            "content_type": project.content_type,
            "additional_context": project.additional_context
        })
        
        logger.info("Script generated successfully")
        
        # Update project status
        project.status = "script_generated"
        db.commit()
        
        return script
    except Exception as e:
        logger.error(f"Script generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}/script", response_model=ScriptResponse)
def update_script(project_id: str, update_data: ScriptUpdateRequest, db: Session = Depends(get_db)):
    """Update script content manually"""
    service = ScriptService(db)
    script = service.update_script(project_id, update_data)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script

@router.post("/{project_id}/script/refine", response_model=ScriptResponse)
async def refine_script(project_id: str, refine_data: ScriptRefineRequest, db: Session = Depends(get_db)):
    """Refine script using AI with user instructions"""
    service = ScriptService(db)
    
    # Get project for context
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        script = await service.refine_script(project_id, refine_data.instructions, {
            "topic": project.topic,
            "language": project.language,
            "duration": project.duration,
            "content_type": project.content_type,
            "additional_context": project.additional_context
        })
        
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        
        return script
    except Exception as e:
        logger.error(f"Script refinement failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/script/approve", response_model=ScriptResponse)
def approve_script(project_id: str, db: Session = Depends(get_db)):
    """Approve script and advance project state"""
    service = ScriptService(db)
    script = service.approve_script(project_id)
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    # Update project status
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if project:
        project.status = "script_approved"
        db.commit()
    
    return script
