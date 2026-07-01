import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.scene.service import SceneService
from app.modules.scene.schemas import (
    SceneResponse, SceneListResponse, SceneGenerateRequest,
    SceneRefineRequest, SceneUpdate
)
from app.modules.script.service import ScriptService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scene"])

@router.get("/{project_id}/scenes", response_model=SceneListResponse)
def get_scenes(project_id: str, db: Session = Depends(get_db)):
    """Get all scenes for a project"""
    service = SceneService(db)
    scenes = service.get_scenes(project_id)
    
    logger.info(f"get_scenes: Found {len(scenes)} scenes for project {project_id}")
    
    total_duration = sum(scene.duration for scene in scenes)
    
    response = SceneListResponse(
        scenes=scenes,
        total_count=len(scenes),
        total_duration=total_duration
    )
    
    logger.info(f"get_scenes: Returning response with {response.total_count} scenes")
    return response

@router.post("/{project_id}/scenes/generate", response_model=SceneListResponse)
async def generate_scenes(project_id: str, request: SceneGenerateRequest, db: Session = Depends(get_db)):
    """Generate scenes for a project using AI"""
    logger.info(f"Scene generation requested for project: {project_id}")
    service = SceneService(db)
    
    # Get project for context
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if not project:
        logger.error(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    
    logger.info(f"Project found: {project.title}, status: {project.status}")

    # Validate state - can generate from script_approved, scenes_generated, or scenes_approved
    allowed_states = ["script_approved", "scenes_generated", "scenes_approved"]
    if project.status not in allowed_states:
        logger.error(f"Invalid project status for scene generation: {project.status}")
        raise HTTPException(
            status_code=409,
            detail=f"Cannot generate scenes when status is '{project.status}'. Allowed states: {', '.join(allowed_states)}"
        )
    
    # Get script content
    script_service = ScriptService(db)
    script = script_service.get_script(project_id)
    
    if not script:
        logger.error(f"Script not found for project: {project_id}")
        raise HTTPException(status_code=404, detail="Script not found")
    
    logger.info(f"Script found, content length: {len(script.content)}")
    
    try:
        logger.info("Starting scene generation via AI...")
        scenes = await service.generate_scenes(
            project_id,
            {
                "topic": project.topic,
                "language": project.language,
                "duration": project.duration,
                "content_type": project.content_type,
                "additional_context": project.additional_context
            },
            script.content,
            request.user_instructions
        )
        
        logger.info(f"Scenes generated successfully: {len(scenes)} scenes")
        
        # Update project status
        project.status = "scenes_generated"
        db.commit()
        
        total_duration = sum(scene.duration for scene in scenes)
        
        return SceneListResponse(
            scenes=scenes,
            total_count=len(scenes),
            total_duration=total_duration
        )
    except Exception as e:
        logger.error(f"Scene generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}/scenes/{scene_id}", response_model=SceneResponse)
def update_scene(project_id: str, scene_id: str, update_data: SceneUpdate, db: Session = Depends(get_db)):
    """Update a single scene"""
    service = SceneService(db)
    scene = service.update_scene(scene_id, update_data)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return scene

@router.post("/{project_id}/scenes/refine", response_model=SceneListResponse)
async def refine_scenes(project_id: str, refine_data: SceneRefineRequest, db: Session = Depends(get_db)):
    """Refine scenes using AI with user instructions"""
    logger.info(f"Scene refinement requested for project: {project_id}")
    service = SceneService(db)
    
    # Get project for context
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        scenes = await service.refine_scenes(project_id, refine_data.instructions, {
            "topic": project.topic,
            "language": project.language,
            "duration": project.duration,
            "content_type": project.content_type,
            "additional_context": project.additional_context
        })
        
        total_duration = sum(scene.duration for scene in scenes)
        
        return SceneListResponse(
            scenes=scenes,
            total_count=len(scenes),
            total_duration=total_duration
        )
    except Exception as e:
        logger.error(f"Scene refinement failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/scenes/approve", response_model=SceneListResponse)
def approve_scenes(project_id: str, db: Session = Depends(get_db)):
    """Approve all scenes and advance project state"""
    service = SceneService(db)
    scenes = service.approve_scenes(project_id)
    
    if not scenes:
        raise HTTPException(status_code=404, detail="No scenes found for this project")
    
    # Update project status
    from app.modules.project.service import get_project
    project = get_project(db, project_id)
    
    if project:
        project.status = "scenes_approved"
        db.commit()
    
    total_duration = sum(scene.duration for scene in scenes)
    
    return SceneListResponse(
        scenes=scenes,
        total_count=len(scenes),
        total_duration=total_duration
    )
