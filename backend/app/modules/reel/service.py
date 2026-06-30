import os
import logging
import subprocess
from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.reel.models import Reel
from app.modules.reel.schemas import ReelCreate, ReelResponse
from app.modules.scene.models import Scene
from app.modules.image.models import Image
from app.modules.voice.models import Voice
from app.config import settings

logger = logging.getLogger(__name__)


class ReelService:
    """Service for reel/video operations"""

    def __init__(self, db: Session):
        self.db = db
        self.ffmpeg_path = settings.FFMPEG_PATH

    def get_reel(self, project_id: str) -> Optional[Reel]:
        """Get reel for a project"""
        return self.db.query(Reel).filter(Reel.project_id == project_id).first()

    def create_reel(self, reel_data: ReelCreate) -> Reel:
        """Create a reel record"""
        reel = Reel(**reel_data.model_dump())
        self.db.add(reel)
        self.db.commit()
        self.db.refresh(reel)
        return reel

    def delete_reel(self, project_id: str) -> None:
        """Delete reel for a project"""
        reel = self.get_reel(project_id)
        if reel:
            # Delete file from disk
            if os.path.exists(reel.file_path):
                try:
                    os.remove(reel.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete reel file: {e}")
            self.db.delete(reel)
            self.db.commit()

    async def generate_reel(self, project_id: str, resolution: str = "1920x1080", fps: int = 30) -> Reel:
        """
        Generate a reel video combining scenes, images, and audio using FFmpeg

        Args:
            project_id: Project ID
            resolution: Video resolution (e.g., "1920x1080")
            fps: Frames per second

        Returns:
            Reel object
        """
        try:
            logger.info(f"Generating reel for project {project_id}")

            # Get all scenes for the project
            scenes = self.db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.scene_number).all()
            if not scenes:
                raise ValueError("No scenes found for project")

            # Get images and voices for each scene
            scene_data = []
            for scene in scenes:
                image = self.db.query(Image).filter(Image.scene_id == scene.id).first()
                voice = self.db.query(Voice).filter(Voice.scene_id == scene.id).first()

                if not image:
                    logger.warning(f"No image found for scene {scene.scene_number}")
                    continue
                if not voice:
                    logger.warning(f"No voice found for scene {scene.scene_number}")
                    continue

                scene_data.append({
                    'scene': scene,
                    'image': image,
                    'voice': voice
                })

            if not scene_data:
                raise ValueError("No complete scenes (with both image and voice) found")

            # Create project storage directory for reels
            project_storage = os.path.join(settings.STORAGE_BASE_PATH, "projects", project_id, "reel")
            os.makedirs(project_storage, exist_ok=True)

            # Output file path
            output_path = os.path.join(project_storage, "reel.mp4")

            # Build FFmpeg command to combine images and audio
            ffmpeg_inputs = []
            filter_complex = []
            current_video = None
            current_audio = None

            for i, data in enumerate(scene_data):
                img_path = data['image'].file_path
                audio_path = data['voice'].file_path

                # Resolve relative paths
                # service.py is at backend/app/modules/reel/service.py
                # Go up 4 levels to get to backend directory
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

                logger.info(f"Backend dir: {backend_dir}")
                logger.info(f"Original img_path: {img_path}")
                logger.info(f"Original audio_path: {audio_path}")

                if img_path.startswith('../'):
                    # Resolve relative to backend directory
                    img_path = os.path.abspath(os.path.join(backend_dir, img_path))
                elif not os.path.isabs(img_path):
                    img_path = os.path.abspath(os.path.join(backend_dir, img_path))

                if audio_path.startswith('../'):
                    audio_path = os.path.abspath(os.path.join(backend_dir, audio_path))
                elif not os.path.isabs(audio_path):
                    audio_path = os.path.abspath(os.path.join(backend_dir, audio_path))

                logger.info(f"Resolved paths - Image: {img_path}, Audio: {audio_path}")

                # Verify files exist
                if not os.path.exists(img_path):
                    raise ValueError(f"Image file not found: {img_path}")
                if not os.path.exists(audio_path):
                    raise ValueError(f"Audio file not found: {audio_path}")

                # Add inputs
                ffmpeg_inputs.extend(['-i', img_path, '-i', audio_path])

                # Build filter complex
                # Split resolution into width and height
                width, height = resolution.split('x')
                img_filter = f"[{2*i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]"
                audio_filter = f"[{2*i+1}:a]adelay=0|0[a{i}]"

                filter_complex.append(img_filter)
                filter_complex.append(audio_filter)

            # Build concatenation inputs (interleaved: v0, a0, v1, a1, v2, a2, ...)
            concat_inputs = ''.join([f"[v{i}][a{i}]" for i in range(len(scene_data))])

            # Final concat filter
            filter_complex.append(f"{concat_inputs}concat=n={len(scene_data)}:v=1:a=1[vout][aout]")

            # Build FFmpeg command
            cmd = [
                self.ffmpeg_path,
                *ffmpeg_inputs,
                '-filter_complex',
                ';'.join(filter_complex),
                '-map',
                '[vout]',
                '-map',
                '[aout]',
                '-c:v',
                'libx264',
                '-preset',
                'medium',
                '-c:a',
                'aac',
                '-b:a',
                '192k',
                '-shortest',
                '-y',
                output_path
            ]

            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")

            # Run FFmpeg
            process = subprocess.run(cmd, capture_output=True, text=True)
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {process.stderr}")
                raise ValueError(f"FFmpeg failed: {process.stderr}")

            # Get video duration using ffprobe
            duration = await self._get_video_duration(output_path)

            # Create reel record
            reel_create = ReelCreate(
                project_id=project_id,
                file_path=f"../storage/projects/{project_id}/reel/reel.mp4",
                duration=duration,
                format="mp4",
                resolution=resolution
            )

            # Delete existing reel if any
            self.delete_reel(project_id)

            # Create new reel
            reel = self.create_reel(reel_create)

            logger.info(f"Reel generated successfully: {output_path}")
            return reel

        except Exception as e:
            logger.error(f"Error generating reel: {e}")
            raise Exception(f"Reel generation failed: {str(e)}")

    async def _get_video_duration(self, video_path: str) -> int:
        """Get video duration using ffprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v',
                'error',
                '-show_entries',
                'format=duration',
                '-of',
                'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return int(duration)
            return None
        except Exception as e:
            logger.error(f"Error getting video duration: {e}")
            return None
