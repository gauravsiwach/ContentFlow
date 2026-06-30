from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import logging
import os

from app.database import get_db
from app.modules.image.service import ImageService
from app.modules.image.schemas import (
    ImageResponse,
    ImageListResponse,
    ImageGenerateRequest,
    ImageRefineRequest
)
from app.modules.project import service as project_service
from app.workflow.workflow_service import WorkflowService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/{project_id}/images", tags=["images"])


@router.post("/generate", response_model=List[ImageResponse])
async def generate_images(
    project_id: str,
    request: ImageGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate images for all scenes in a project (legacy - use individual scene generation)"""
    try:
        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_generate_images(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot generate images: project must have approved scenes"
            )

        # Get project context
        project = project_service.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        project_context = {
            "title": project.title,
            "topic": project.topic,
            "language": project.language,
            "duration": project.duration,
            "content_type": project.content_type
        }

        # Generate images
        image_service = ImageService(db)
        images = await image_service.generate_images(
            project_id=project_id,
            project_context=project_context,
            user_instructions=request.user_instructions
        )

        # Update project status
        project_service.update_project_status(db, project_id, "images_generated")
        logger.info(f"All images generated for project {project_id}, status updated to images_generated")

        return images

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating images: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate images: {str(e)}")


@router.post("/scenes/{scene_id}/generate", response_model=ImageResponse)
async def generate_scene_image(
    project_id: str,
    scene_id: str,
    db: Session = Depends(get_db)
):
    """Generate a single image for a specific scene"""
    try:
        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_generate_images(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot generate images: project must have approved scenes"
            )

        # Generate image for the scene
        image_service = ImageService(db)
        image = await image_service.generate_image_for_scene(project_id, scene_id)

        # Check if all scenes now have images
        from app.modules.scene.models import Scene
        scenes = db.query(Scene).filter(Scene.project_id == project_id).all()
        images = image_service.get_images(project_id)

        if len(images) == len(scenes):
            # All scenes have images, update project status
            project_service.update_project_status(db, project_id, "images_generated")
            logger.info(f"All images generated for project {project_id}, status updated to images_generated")

        return image

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating scene image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate scene image: {str(e)}")


@router.get("", response_model=ImageListResponse)
def get_images(project_id: str, db: Session = Depends(get_db)):
    """Get all images for a project"""
    try:
        image_service = ImageService(db)
        images = image_service.get_images(project_id)
        return ImageListResponse(images=images, total_count=len(images))
    except Exception as e:
        logger.error(f"Error getting images: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get images: {str(e)}")


@router.post("/{image_id}/refine", response_model=ImageResponse)
async def refine_image(
    project_id: str,
    image_id: str,
    request: ImageRefineRequest,
    db: Session = Depends(get_db)
):
    """Regenerate a single image with a new prompt"""
    try:
        image_service = ImageService(db)
        image = await image_service.regenerate_image(image_id, request.new_prompt)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image
    except Exception as e:
        logger.error(f"Error refining image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to refine image: {str(e)}")


@router.post("/approve")
def approve_images(project_id: str, db: Session = Depends(get_db)):
    """Approve all images for a project"""
    try:
        # Get current project status
        project = project_service.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Skip validation if already approved
        if project.status == "images_approved":
            image_service = ImageService(db)
            images = image_service.get_images(project_id)
            return {"message": "Images already approved", "count": len(images)}

        # Validate project state
        workflow = WorkflowService(db)
        if not workflow.can_approve_images(project_id):
            raise HTTPException(
                status_code=409,
                detail="Cannot approve images: project must have generated images"
            )

        image_service = ImageService(db)
        images = image_service.approve_images(project_id)

        # Update project status
        project_service.update_project_status(db, project_id, "images_approved")
        logger.info(f"All images approved for project {project_id}, status updated to images_approved")

        return {"message": "Images approved successfully", "count": len(images)}
    except Exception as e:
        logger.error(f"Error approving images: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to approve images: {str(e)}")


@router.get("/{scene_id}")
def serve_image(project_id: str, scene_id: str, db: Session = Depends(get_db)):
    """Serve an image file for a scene"""
    try:
        logger.info(f"Serving image for project {project_id}, scene {scene_id}")
        image_service = ImageService(db)
        images = image_service.get_images(project_id)
        image = next((img for img in images if img.scene_id == scene_id), None)

        if not image:
            logger.error(f"Image not found for scene {scene_id}")
            raise HTTPException(status_code=404, detail="Image not found")

        logger.info(f"Found image with file_path: {image.file_path}")

        file_path = image.file_path
        if not os.path.exists(file_path):
            logger.error(f"Image file not found on disk: {file_path}")
            raise HTTPException(status_code=404, detail=f"Image file not found on disk: {file_path}")

        logger.info(f"Serving image file: {file_path}")
        return FileResponse(
            file_path,
            media_type="image/png",
            filename=f"scene_{scene_id}.png"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve image: {str(e)}")
