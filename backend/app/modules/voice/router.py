from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import logging
import os

from app.database import get_db
from app.modules.voice.service import VoiceService
from app.modules.voice.schemas import (
    VoiceGenerateRequest,
    VoiceResponse,
    VoiceListResponse,
    VoiceRefineRequest
)
from app.modules.project import service as project_service
from app.workflow.workflow_service import WorkflowService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/{project_id}/voices", tags=["voices"])


@router.post("/generate", response_model=List[VoiceResponse])
async def generate_voices(
    project_id: str,
    request: VoiceGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate voices for all scenes in a project (legacy - use individual scene generation)"""
    try:
        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_generate_voices(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot generate voices: project must have approved images"
            )

        # Get project context
        project = project_service.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Generate voices
        voice_service = VoiceService(db)
        voices = await voice_service.generate_voices(
            project_id=project_id,
            user_instructions=request.user_instructions
        )

        # Update project status
        project_service.update_project_status(db, project_id, "voices_generated")

        return voices

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating voices: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate voices: {str(e)}")


@router.post("/scenes/{scene_id}/generate", response_model=VoiceResponse)
async def generate_scene_voice(
    project_id: str,
    scene_id: str,
    db: Session = Depends(get_db)
):
    """Generate a single voice for a specific scene"""
    try:
        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_generate_voices(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot generate voices: project must have approved images"
            )

        # Get project language
        project = project_service.get_project(db, project_id)

        # Generate voice for the scene
        voice_service = VoiceService(db, language=project.language)
        voice = await voice_service.generate_voice_for_scene(project_id, scene_id)

        # Check if all scenes now have voices
        from app.modules.scene.models import Scene
        scenes = db.query(Scene).filter(Scene.project_id == project_id).all()
        voices = voice_service.get_voices(project_id)

        if len(voices) == len(scenes):
            # All scenes have voices, update project status
            project_service.update_project_status(db, project_id, "voices_generated")
            logger.info(f"All voices generated for project {project_id}, status updated to voices_generated")

        return voice

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating scene voice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate scene voice: {str(e)}")


@router.get("", response_model=VoiceListResponse)
def get_voices(project_id: str, db: Session = Depends(get_db)):
    """Get all voices for a project"""
    try:
        voice_service = VoiceService(db)
        voices = voice_service.get_voices(project_id)
        return VoiceListResponse(voices=voices, total_count=len(voices))
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get voices: {str(e)}")


@router.get("/{scene_id}")
def serve_voice(project_id: str, scene_id: str, db: Session = Depends(get_db)):
    """Serve a voice file for a scene"""
    try:
        logger.info(f"Serving voice for project {project_id}, scene {scene_id}")
        voice_service = VoiceService(db)
        voices = voice_service.get_voices(project_id)
        voice = next((v for v in voices if v.scene_id == scene_id), None)

        if not voice:
            logger.error(f"Voice not found for scene {scene_id}")
            raise HTTPException(status_code=404, detail="Voice not found")

        logger.info(f"Found voice with file_path: {voice.file_path}")

        # Handle relative paths by resolving from backend root
        file_path = voice.file_path
        if file_path.startswith('../'):
            # Resolve relative path from backend root (not app directory)
            # __file__ is in backend/app/modules/voice/router.py
            # We need to go up 3 levels to reach backend/
            backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            file_path = os.path.abspath(os.path.join(backend_root, file_path))
            logger.info(f"Resolved relative path to: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Voice file not found on disk: {file_path}")
            raise HTTPException(status_code=404, detail="Voice file not found on disk: {file_path}")

        logger.info(f"Serving voice file: {file_path}")
        return FileResponse(
            file_path,
            media_type="audio/wav",
            filename=f"scene_{scene_id}.wav"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving voice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve voice: {str(e)}")


@router.post("/{voice_id}/refine", response_model=VoiceResponse)
async def refine_voice(
    project_id: str,
    voice_id: str,
    request: VoiceRefineRequest,
    db: Session = Depends(get_db)
):
    """Refine a voice with new text"""
    try:
        voice_service = VoiceService(db)
        voice = await voice_service.regenerate_voice(voice_id, request.new_text)
        if not voice:
            raise HTTPException(status_code=404, detail="Voice not found")
        return voice
    except Exception as e:
        logger.error(f"Error refining voice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to refine voice: {str(e)}")


@router.post("/approve")
def approve_voices(project_id: str, db: Session = Depends(get_db)):
    """Approve all voices for a project"""
    try:
        voice_service = VoiceService(db)
        voices = voice_service.approve_voices(project_id)

        # Update project status
        project_service.update_project_status(db, project_id, "voices_approved")
        logger.info(f"All voices approved for project {project_id}")

        return {"message": "Voices approved successfully", "count": len(voices)}
    except Exception as e:
        logger.error(f"Error approving voices: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to approve voices: {str(e)}")
