from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import logging
import os

from app.database import get_db
from app.modules.reel.service import ReelService
from app.modules.reel.schemas import ReelResponse, ReelGenerateRequest
from app.modules.project import service as project_service
from app.workflow.workflow_service import WorkflowService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/{project_id}/reel", tags=["reel"])


@router.post("/generate", response_model=ReelResponse)
async def generate_reel(
    project_id: str,
    request: ReelGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a reel video for a project"""
    try:
        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_generate_reel(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot generate reel: project must have approved voices"
            )

        # Generate reel
        reel_service = ReelService(db)
        reel = await reel_service.generate_reel(
            project_id,
            resolution=request.resolution,
            fps=request.fps
        )

        # Update project status
        project_service.update_project_status(db, project_id, "reel_generated")
        logger.info(f"Reel generated for project {project_id}, status updated to reel_generated")

        return reel

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating reel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate reel: {str(e)}")


@router.get("", response_model=ReelResponse)
def get_reel(project_id: str, db: Session = Depends(get_db)):
    """Get reel for a project"""
    try:
        reel_service = ReelService(db)
        reel = reel_service.get_reel(project_id)
        if not reel:
            raise HTTPException(status_code=404, detail="Reel not found")
        return reel
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting reel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get reel: {str(e)}")


@router.get("/serve")
def serve_reel(project_id: str, db: Session = Depends(get_db)):
    """Serve the reel video file"""
    try:
        reel_service = ReelService(db)
        reel = reel_service.get_reel(project_id)
        if not reel:
            raise HTTPException(status_code=404, detail="Reel not found")

        file_path = reel.file_path
        if file_path.startswith('../'):
            # router.py is at backend/app/modules/reel/router.py
            # Go up 4 levels to get to backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            file_path = os.path.abspath(os.path.join(backend_dir, file_path))
        elif not os.path.isabs(file_path):
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            file_path = os.path.abspath(os.path.join(backend_dir, file_path))

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Reel file not found on disk")

        return FileResponse(
            file_path,
            media_type="video/mp4",
            filename=f"reel_{project_id}.mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Cache-Control": "no-cache"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving reel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve reel: {str(e)}")
