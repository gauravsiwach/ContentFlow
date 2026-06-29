import os
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.image.models import Image
from app.modules.image.schemas import ImageCreate, ImageUpdate
from app.modules.scene.models import Scene
from app.shared.ai.ollama_image_client import OllamaImageClient
from app.config import settings

logger = logging.getLogger(__name__)


class ImageService:
    """Service for image operations"""

    def __init__(self, db: Session, image_client: Optional[OllamaImageClient] = None):
        self.db = db
        self.image_client = image_client or OllamaImageClient()

    def get_images(self, project_id: str) -> List[Image]:
        """Get all images for a project (deduplicated by scene_id)"""
        all_images = self.db.query(Image).filter(Image.project_id == project_id).all()
        # Deduplicate by scene_id, keeping the most recent one
        seen_scene_ids = set()
        unique_images = []
        for image in reversed(all_images):  # Process in reverse to keep most recent
            if image.scene_id not in seen_scene_ids:
                seen_scene_ids.add(image.scene_id)
                unique_images.append(image)
        return list(reversed(unique_images))  # Return in original order

    def create_image(self, image_data: ImageCreate) -> Image:
        """Create a single image"""
        image = Image(
            scene_id=image_data.scene_id,
            project_id=image_data.project_id,
            file_path=image_data.file_path,
            prompt_used=image_data.prompt_used
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def update_image(self, image_id: str, update_data: ImageUpdate) -> Optional[Image]:
        """Update an image"""
        image = self.db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return None

        if update_data.file_path is not None:
            image.file_path = update_data.file_path
        if update_data.prompt_used is not None:
            image.prompt_used = update_data.prompt_used
        if update_data.is_approved is not None:
            image.is_approved = update_data.is_approved

        self.db.commit()
        self.db.refresh(image)
        return image

    def approve_images(self, project_id: str) -> List[Image]:
        """Approve all images for a project"""
        images = self.get_images(project_id)
        for image in images:
            image.is_approved = True
        self.db.commit()
        for image in images:
            self.db.refresh(image)
        return images

    def delete_images(self, project_id: str) -> bool:
        """Delete all images for a project"""
        images = self.get_images(project_id)
        for image in images:
            # Delete file from disk
            if os.path.exists(image.file_path):
                try:
                    os.remove(image.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete image file {image.file_path}: {e}")
            self.db.delete(image)
        self.db.commit()
        return True

    async def generate_images(self, project_id: str, project_context: dict, user_instructions: Optional[str] = None) -> List[Image]:
        """Generate images for all scenes in a project"""
        logger.info(f"Generating images for project: {project_id}")

        # Get all scenes for the project
        scenes = self.db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.scene_number).all()

        if not scenes:
            raise ValueError("No scenes found for project")

        # Delete existing images
        self.delete_images(project_id)

        # Create project storage directory
        project_storage = os.path.join(settings.STORAGE_BASE_PATH, "projects", project_id, "images")
        os.makedirs(project_storage, exist_ok=True)

        # Generate image for each scene
        created_images = []
        for idx, scene in enumerate(scenes):
            try:
                logger.info(f"Generating image for scene {idx + 1}: {scene.title}")

                # Generate image using Ollama
                image_bytes = await self.image_client.generate(prompt=scene.image_prompt)

                # Save image to disk
                file_name = f"scene_{scene.scene_number:02d}.png"
                file_path = os.path.join(project_storage, file_name)
                with open(file_path, "wb") as f:
                    f.write(image_bytes)

                # Create image record
                image_create = ImageCreate(
                    scene_id=scene.id,
                    project_id=project_id,
                    file_path=file_path,
                    prompt_used=scene.image_prompt
                )
                image = self.create_image(image_create)
                created_images.append(image)

                logger.info(f"Image generated for scene {idx + 1}: {file_path}")

            except Exception as e:
                logger.error(f"Failed to generate image for scene {idx + 1}: {e}")
                raise Exception(f"Failed to generate image for scene {idx + 1}: {e}")

        logger.info(f"Generated {len(created_images)} images for project {project_id}")

        # Refresh all images from database to ensure they're attached to session
        for image in created_images:
            self.db.refresh(image)

        return created_images

    async def generate_image_for_scene(self, project_id: str, scene_id: str) -> Image:
        """Generate a single image for a specific scene"""
        logger.info(f"Generating image for scene {scene_id} in project {project_id}")

        # Get the scene
        scene = self.db.query(Scene).filter(Scene.id == scene_id, Scene.project_id == project_id).first()
        if not scene:
            raise ValueError(f"Scene {scene_id} not found in project {project_id}")

        # Check if image already exists for this scene
        existing_image = self.db.query(Image).filter(Image.scene_id == scene_id).first()
        if existing_image:
            # Delete existing image and file
            if os.path.exists(existing_image.file_path):
                try:
                    os.remove(existing_image.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete existing image file: {e}")
            self.db.delete(existing_image)
            self.db.commit()

        # Create project storage directory
        project_storage = os.path.join(settings.STORAGE_BASE_PATH, "projects", project_id, "images")
        os.makedirs(project_storage, exist_ok=True)

        # Generate image using Ollama
        image_bytes = await self.image_client.generate(prompt=scene.image_prompt)

        # Save image to disk
        file_name = f"scene_{scene.scene_number:02d}.png"
        file_path = os.path.join(project_storage, file_name)
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # Create image record
        image_create = ImageCreate(
            scene_id=scene.id,
            project_id=project_id,
            file_path=file_path,
            prompt_used=scene.image_prompt
        )
        image = self.create_image(image_create)

        logger.info(f"Image generated for scene {scene.scene_number}: {file_path}")

        # Refresh to ensure attached to session
        self.db.refresh(image)

        return image

    async def regenerate_image(self, image_id: str, new_prompt: str) -> Optional[Image]:
        """Regenerate a single image with a new prompt"""
        image = self.db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return None

        try:
            logger.info(f"Regenerating image {image_id} with new prompt")

            # Generate new image
            image_bytes = await self.image_client.generate(prompt=new_prompt)

            # Save new image (overwrite old one)
            with open(image.file_path, "wb") as f:
                f.write(image_bytes)

            # Update image record
            image.prompt_used = new_prompt
            self.db.commit()
            self.db.refresh(image)

            logger.info(f"Image regenerated successfully: {image.file_path}")
            return image

        except Exception as e:
            logger.error(f"Failed to regenerate image {image_id}: {e}")
            raise Exception(f"Failed to regenerate image: {e}")
