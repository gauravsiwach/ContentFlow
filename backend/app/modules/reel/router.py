from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse, StreamingResponse
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

        # Update project status only if not already reel_generated
        workflow = WorkflowService(db)
        project = project_service.get_project(db, project_id)
        if project.status != "reel_generated":
            project_service.update_project_status(db, project_id, "reel_generated")
            logger.info(f"Reel generated for project {project_id}, status updated to reel_generated")
        else:
            logger.info(f"Reel regenerated for project {project_id}, status remains reel_generated")

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
def serve_reel(project_id: str, request: Request, db: Session = Depends(get_db)):
    """Serve the reel video file with range request support for browser streaming"""
    try:
        reel_service = ReelService(db)
        reel = reel_service.get_reel(project_id)
        if not reel:
            raise HTTPException(status_code=404, detail="Reel not found")

        file_path = reel.file_path
        logger.info(f"Reel file_path from DB: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"File not found at: {file_path}")
            raise HTTPException(status_code=404, detail="Reel file not found on disk")

        file_size = os.path.getsize(file_path)
        range_header = request.headers.get("range")

        if range_header:
            range_val = range_header.strip().replace("bytes=", "")
            start_str, end_str = range_val.split("-")
            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)
            chunk_size = end - start + 1

            def iter_file():
                with open(file_path, "rb") as f:
                    f.seek(start)
                    remaining = chunk_size
                    while remaining > 0:
                        data = f.read(min(65536, remaining))
                        if not data:
                            break
                        remaining -= len(data)
                        yield data

            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Type": "video/mp4",
            }
            return StreamingResponse(iter_file(), status_code=206, headers=headers)

        def iter_full_file():
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    yield data

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(iter_full_file(), status_code=200, headers=headers)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving reel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve reel: {str(e)}")
